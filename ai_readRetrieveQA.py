from ai_search import ai_output, default_QA, get_summarize_refine_prompt
from tools.chromaStore import chromaStore
from tools.gsearch_tools import gsearch, engine_list

from llama_index.tools.tool_spec.load_and_search.base import LoadAndSearchToolSpec
from llama_hub.tools.google_search.base import GoogleSearchToolSpec
from llama_index.agent import OpenAIAgent
import openai

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import re
from typing import Union, List
import os, logging
from dotenv import load_dotenv, find_dotenv
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
SERPAPI_API_KEY = os.environ.get('SERPAPI_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
# GOOGLE_API_KEY = ''

def answer_check(answer):
    s = re.search('(?i)no information|provided text|contain information|no relevant', answer['query_engine_response'])
    if s is None and len(answer['sources']) > 0:
        return 200
    else:
        return 404

class simpleSearch_QA(default_QA):
    def __init__(self, engine_type:str='whole_web'):
        """
        engine_type: any of "whole_web", "climate", or "indo_news"
        """
        super().__init__()
        self.cx = engine_list[engine_type]
        google_spec = GoogleSearchToolSpec(key=GOOGLE_API_KEY, engine=self.cx)
        openai.api_key = "sk-your-key"

        # Wrap the google search tool as it returns large payloads
        tools = LoadAndSearchToolSpec.from_defaults(
            google_spec.to_tool_list()[0],
        ).to_tool_list()

        self.agent = OpenAIAgent.from_tools(tools, verbose=True)

    
    def ask(self, query:str, chat_history_dict=None):
        history_modified_query = self.synthesize_qn_with_chat_history(query, chat_history_dict)

        # print(history_modified_query)
        try:
            answer =  self.agent.chat(history_modified_query)
            answer = answer.response
        except Exception as e:
            print(e)
            client = openai.OpenAI(api_key=OPENAI_API_KEY)

            # messages.append({"role": "user", "content": prompt})

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                temperature=0,
                # messages = messages
                messages=[
                    {"role": "system", "content": "You are a knowledgeable candidate for indonesian presidential election. You are also good at refining answers from your assistants into a single coherent answer."},
                    {"role": "user", "content": query}
                ]
            )
            answer = completion.choices[0].message.content

        return {'query_engine_response':answer, 
                'raw_query_str':query,
                'query_with_context':history_modified_query,
                'entities':[],
                'sources':[]}

class thematicSearch_QA(default_QA):
    def __init__(self, engine_type:str='workforce'):
        """
        engine_type: any of "whole_web", "climate", or "indo_news"
        """
        super().__init__()
        self.embeddings = OpenAIEmbeddings(model='text-embedding-ada-002',openai_api_key=OPENAI_API_KEY)
        # self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
        self.search_engine = gsearch(engine_type=engine_type)

    def load_articles(self, query, start_date:Union[str, None]="2023-01-01", articles=[]):
        search_res = self.search_engine.search(query=query, start_date=start_date)
        # urls = [x['url'] for x in search_res]
        if len(articles)>0:
            current_urls = [x.metadata['source'] for x in articles]
            search_res = [x for x in search_res if x['url'] not in current_urls]
            copy_articles = articles.copy()
        else:
            copy_articles = []
        copy_articles.extend(self.search_engine.read_articles(search_res))
        return copy_articles
    
    def load_query_engine(self, query):
        queried_articles = self.load_articles(query)
        logging.info(queried_articles)
        q_keyterms = self.entity_extraction(query)
        for terms in q_keyterms:
            queried_articles = self.load_articles(query=terms, articles=queried_articles)
            logging.info(queried_articles)

        try:
            chroma_store = chromaStore(docs=queried_articles)
            query_engine = RetrievalQA.from_chain_type(
                    chain_type='map_reduce',
                    retriever=chroma_store.as_retriever(),
                    llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo-1106"),
                    return_source_documents=True
                )
            return query_engine
        except IndexError:
            return None

    def ask(self, query:str, chat_history_dict=None):
        history_modified_query = self.synthesize_qn_with_chat_history(query, chat_history_dict)
        query_engine = self.load_query_engine(history_modified_query)
        if query_engine is None:
            return {
                'query_engine_response':'No relevant documents found', 
                'raw_query_str':query,
                'query_with_context':history_modified_query,
                'entities':[],
                'sources':[]
            }
        
        answer = query_engine(history_modified_query)
        sources = list(set([x.metadata['source'] for x in answer['source_documents']]))
        entities = list(set([x.metadata['title'] for x in answer['source_documents']]))
        
        return {
                'query_engine_response':answer['result'], 
                'raw_query_str':query,
                'query_with_context':history_modified_query,
                'entities':entities,
                'sources':sources
            }