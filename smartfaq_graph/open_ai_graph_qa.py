from typing import List, Dict

from llama_index import (
    KnowledgeGraphIndex,
    LLMPredictor,
    ServiceContext,
    SimpleDirectoryReader,
)
from llama_index.storage.storage_context import StorageContext
from llama_index.graph_stores import Neo4jGraphStore
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding

from llama_index.retrievers import KnowledgeGraphRAGRetriever
from llama_index.query_engine import KnowledgeGraphQueryEngine, RetrieverQueryEngine
from llama_index.prompts import PromptTemplate
from llama_index.prompts.prompt_type import PromptType

from llama_index.response_synthesizers import get_response_synthesizer, CompactAndRefine
from kg_prompts import new_graph_q_synthesis_promptTemplate
from kg_prompts import entity_classification_template, entity_classification_parser, graph_q_with_ER_prompt, refine_prompt, graph_response_answer_prompt, chat_history_template
from ai_search import default_QA
from neo4j import GraphDatabase
from openai import OpenAI as OpenAI_cli
from pydantic import BaseModel
from typing import List

import os, re, json
from dotenv import load_dotenv, find_dotenv
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# NEO4J_URL = os.environ.get('NEO4J_URL')
# NEO4J_USER = os.environ.get('NEO4J_USER')
# NEO4J_PASS = os.environ.get('NEO4J_PASS')   

NEO4J_URL = os.environ.get('NEO4J_LOCAL_HOST')
NEO4J_USER = os.environ.get('NEO4J_LOCAL_USER')
NEO4J_PASS = os.environ.get('NEO4J_LOCAL_PASS') 

# def catch(func, *args, handle=lambda e : e, **kwargs):
#     try:
#         return func(*args, **kwargs)
#     except Exception as e:
#         return handle(e)


class graph_QA(default_QA):
    def __init__(self, db_name:str, chat_limit=5):
        super().__init__()
        graph_store = Neo4jGraphStore(
            username=NEO4J_USER,
            password=NEO4J_PASS,
            url=NEO4J_URL,
            database=db_name,
        )
        self.storage_context = StorageContext.from_defaults(graph_store=graph_store)

        self.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)
        self.embedding_llm = OpenAIEmbedding(model="text-embedding-ada-002", temperature=0, api_key=OPENAI_API_KEY)
        self.service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model=self.embedding_llm
        )

        self.chat_limit = chat_limit

        # get node names if the graph is not too big
        self.ER_max_node_count = 1000
        self.graph_node_count = self.get_node_count()
        if self.graph_node_count <= self.ER_max_node_count:
            self.node_names = self.get_all_node_names()

        self.source_dict = self.get_sources_dict()
        self.response_synth = self.build_response_synth()
        self.query_engine = self.kg_query_engine()

    def build_response_synth(self):
        synth = CompactAndRefine(service_context=self.service_context, refine_template=refine_prompt, verbose=True)
        return synth

    def get_node_count(self):
        with GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASS)) as driver:
            records, summary, keys = driver.execute_query(
                "MATCH (p) RETURN count(p) as node_count",
                database_="neo4j",
            )
        return records[0].data()['node_count']
    
    def get_all_node_names(self):
        with GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASS)) as driver:
            records, summary, keys = driver.execute_query(
                "MATCH (p) RETURN p.name AS name",
                database_="neo4j",
            )
            node_names = [x.data()['name'] for x in records if isinstance(x.data()['name'], str)]
        return ', '.join(node_names)
    
    def get_sources_dict(self):
        with GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASS)) as driver:
            records, summary, keys = driver.execute_query(
                "MATCH (p:Political_party) RETURN p.name AS name, p.source as source",
                database_="neo4j",
            )
            party_source_dict = {x.data()['name']:x.data()['source'] for x in records if isinstance(x.data()['name'], str)}
        return party_source_dict

    def graph_rag_query_engine(self):
        graph_rag_retriever = KnowledgeGraphRAGRetriever(
            storage_context=self.storage_context,
            service_context=self.service_context,
            llm=self.llm,
            verbose=True,
            with_nl2graphquery=True
        )

        if self.graph_node_count > self.ER_max_node_count:
            updated_graph_q_prompt = new_graph_q_synthesis_promptTemplate
        else: 
            updated_graph_q_prompt = graph_q_with_ER_prompt

        graph_rag_retriever._kg_query_engine.update_prompts({
            'graph_query_synthesis_prompt':updated_graph_q_prompt,
            # 'graph_response_answer_prompt':graph_response_answer_prompt
        })
        
        query_engine = RetrieverQueryEngine.from_args(
            graph_rag_retriever, service_context=self.service_context
            # , response_synthesizer=self.response_synth
        )

        return query_engine
    
    def kg_query_engine(self):
        query_engine = KnowledgeGraphQueryEngine(
            storage_context=self.storage_context,
            service_context=self.service_context,
            response_synthesizer=self.response_synth,
            llm=self.llm,
            verbose=True,
        )
        
        if self.graph_node_count > self.ER_max_node_count:
            updated_graph_q_prompt = new_graph_q_synthesis_promptTemplate
        else: 
            updated_graph_q_prompt = graph_q_with_ER_prompt
            
        query_engine.update_prompts({
            'graph_query_synthesis_prompt':updated_graph_q_prompt,
            'graph_response_answer_prompt':graph_response_answer_prompt
        })
        return query_engine
    
    def get_source(self, entities):
        m = []
        for x in entities:
            try:
                new_src = self.source_dict[x]
                if new_src not in m:
                    m.append(self.source_dict[x])
            except:
                pass
        return m

    
    def ask(self, query:str, chat_history_dict=None, test=False):
        
        if chat_history_dict:
            # chat_history_dict=json.loads(chat_history_dict)
            history_modified_query = self.synthesize_qn_with_chat_history(query, chat_history_dict)
        else:
            history_modified_query = query
        
        # if chat_history_dict:
        #     chat_history_dict =json.loads(chat_history_dict)
            
            # if len([x for x in chat_history_dict if x['role']=='user']) > self.chat_limit:
            #     return {"query_engine_response":{"response":"maaf anda sudah melewati limit percakapan"}, "sources":[]}
        #     else:
        #         messages.extend(chat_history_dict)

        # if self.graph_node_count <= self.ER_max_node_count:
        modified_query, entities = self.get_entities_with_llm(history_modified_query, self.node_names)
        # print(entities)
        sources = self.get_source(entities)
        try:
            answer = self.query_engine.query(modified_query)
        except:
            {'query_engine_response':'kalb', 
                    'raw_query_str':query,
                    'query_with_context':modified_query,
                    'entities':entities,
                    'sources':sources}
        # return answer
        if test:
            return answer 
        else:
            return {'query_engine_response':answer.response, 
                    'raw_query_str':query,
                    'query_with_context':modified_query,
                    'entities':entities,
                    'sources':sources}
        
        # else:
        #     return {'query_engine_response':self.query_engine.query(query)}

