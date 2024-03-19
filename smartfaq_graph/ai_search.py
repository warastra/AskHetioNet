from langchain import hub
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import SelfAskOutputParser, ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from langchain.chains import LLMMathChain

from langchain.agents import AgentType, Tool, initialize_agent, AgentExecutor
from langchain.agents import AgentExecutor
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from openai import OpenAI as OpenAI_cli
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from langchain.chains import RetrievalQA
from pydantic import BaseModel
from typing import List, Dict

from kg_prompts import chat_history_template, entity_classification_template, entity_classification_parser
from agent_prompts import self_ask_w_search_prompt, ReAct_agent_PROMPT, get_summarize_refine_prompt
from agent_prompts import entity_extract_prompt, keyterm_extraction_parser
import os, json
from dotenv import load_dotenv, find_dotenv
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
SERPAPI_API_KEY = os.environ.get('SERPAPI_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

SERPAPI_PARAMS = {
    "gl": "id",
    "lr": "lang_id|lang_en",
}

class req_body(BaseModel):
    q: str # query/question
    chat_history:List[Dict]=None

class ai_output(BaseModel):
    query_engine_response: str
    raw_query_str:str
    query_with_context:str
    entities:List
    sources:List

class default_QA:
    def __init__(self):
        pass

    def synthesize_qn_with_chat_history(self, query, chat_history_dict):
        chat_hist_client = OpenAI_cli(api_key=OPENAI_API_KEY)
        if  chat_history_dict is not None:
            
            chat_history = ''
            for chat in chat_history_dict:
                chat_format = '{}:{}'.format(chat['role'], chat['content'])
                chat_history += chat_format + '\n'

            prompt = chat_history_template.format(chat_history=chat_history, question=query)
            
            completion = chat_hist_client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                temperature=0,
                messages=[
                    {"role": "system", "content": "You are a helpful and truthful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

             
        else:
            # return query
            prompt = """translate the following question to english
            Question: {question}
            English Translation: 
            """.format(question=query)
            completion = chat_hist_client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                temperature=0,
                messages=[
                    {"role": "system", "content": "You are a helpful and truthful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
        return completion.choices[0].message.content
    
    def get_entities_with_llm(self, query, node_names):
        prompt = entity_classification_template.format(node_names=node_names, question=query)
        client = OpenAI_cli(api_key=OPENAI_API_KEY)

        # messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            temperature=0,
            # messages = messages
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        print(completion.choices[0].message.content)
        modified_query, entities = entity_classification_parser(completion.choices[0].message.content)
        return modified_query, entities
    
    def entity_extraction(self, query):
        prompt = entity_extract_prompt.format(query=query)
        client = OpenAI_cli(api_key=OPENAI_API_KEY)

        # messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            temperature=0,
            # messages = messages
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        print(completion.choices[0].message.content)
        keyterms = keyterm_extraction_parser(completion.choices[0].message.content)
        return keyterms


class Search_QA(default_QA):
    def __init__(self, agent_type='ReAct'):
        super().__init__()
        self.agent_type = agent_type
        self.search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY, params=SERPAPI_PARAMS)
        self.agent_executor = self.build_agent_executor()
        
    def get_agent_type(self):
        return self.agent_type
    
    def build_agent_executor(self):
        if self.agent_type=='self-ask':
            agent_prompt = self_ask_w_search_prompt
            llm_with_stop = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY).bind(stop=["\nIntermediate answer:"])
            tools = [
                Tool(
                    name="Intermediate Answer",
                    func=self.search.run,
                    description="useful for when you need to ask with search",
                )
            ]
            agent = (
                {
                    "input": lambda x: x["input"],
                    # Use some custom observation_prefix/llm_prefix for formatting
                    "agent_scratchpad": lambda x: format_log_to_str(
                        x["intermediate_steps"],
                        observation_prefix="\nIntermediate answer: ",
                        llm_prefix="",
                    ),
                }
                | agent_prompt
                | llm_with_stop
                | SelfAskOutputParser()
            )
        
        # else use ReAct
        else:
            agent_prompt = ReAct_agent_PROMPT
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")
            llm_with_stop = llm.bind(stop=["\nObservation"])
            llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

            tools = [
                Tool(
                    name="Search",
                    func=self.search.run,
                    description="useful for when you need to answer questions about current events. You should ask targeted questions",
                ),
                Tool(
                    name="Calculator",
                    func=llm_math_chain.run,
                    description="useful for when you need to answer questions about math"
                )
            ]

            agent_prompt = agent_prompt.partial(
                tools=render_text_description(tools),
                tool_names=", ".join([t.name for t in tools]),
            )

            agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
                }
                | agent_prompt
                | llm_with_stop
                | ReActSingleInputOutputParser()
            )
            
        return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=7)

    
    def ask(self, query:str, chat_history_dict=None):
        history_modified_query = self.synthesize_qn_with_chat_history(query, chat_history_dict)

        # print(history_modified_query)
        answer =  self.agent_executor.invoke(
            {"input": history_modified_query}
        )

        return {'query_engine_response':answer['output'], 
                'raw_query_str':answer['input'],
                'query_with_context':history_modified_query,
                'entities':[],
                'sources':[]}

class wiki_QA(default_QA):
    
    def __init__(self, chroma_db_dir):
        super().__init__()
        self.figure_list = ['Ganjar Pranowo', 'Mahfud MD', 'Anies Baswedan', 'Muhaimin Iskandar', 'Prabowo Subianto', 'Gibran Rakabuming']
        self.vector_dir = chroma_db_dir

        # self.refine_chain = load_qa_chain(
        #     llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106"),
        #     chain_type="refine"
        # )
        self.embeddings = OpenAIEmbeddings(model='text-embedding-ada-002',openai_api_key=OPENAI_API_KEY)
        
        self.vectordb = Chroma(persist_directory=self.vector_dir, embedding_function=self.embeddings)
        self.query_engine = RetrievalQA.from_chain_type(
                chain_type='refine',
                retriever=self.vectordb.as_retriever(),
                llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106"),
                return_source_documents=True
            )

    def ask(self, query:str, chat_history_dict=None):
        history_modified_query = self.synthesize_qn_with_chat_history(query, chat_history_dict)
        answer = self.query_engine(history_modified_query)
        sources = list(set([x.metadata['source'] for x in answer['source_documents']]))
        entities = list(set([x.metadata['title'] for x in answer['source_documents']]))
        
        return {'query_engine_response':answer['result'], 
                'raw_query_str':answer['query'],
                'query_with_context':history_modified_query,
                'entities':entities,
                'sources':sources}
    
def refine_QA(answers:List[ai_output]):
    query_str = answers[0]['query_with_context']
    answer_list = [x['query_engine_response'] for x in answers]
    sources = [x['sources'] for x in answers if x is not None]
    prompt = get_summarize_refine_prompt(query=query_str, answer_list=answer_list)
    client = OpenAI_cli(api_key=OPENAI_API_KEY)

    # messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0,
        # messages = messages
        messages=[
            {"role": "system", "content": "You are a knowledgeable candidate for indonesian presidential election. You are also good at refining answers from your assistants into a single coherent answer."},
            {"role": "user", "content": prompt}
        ]
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content, sources
