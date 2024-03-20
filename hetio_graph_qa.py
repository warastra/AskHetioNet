from typing import List, Callable, Dict

from llama_index import ServiceContext
from llama_index.storage.storage_context import StorageContext
from llama_index.graph_stores import Neo4jGraphStore
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding
from llama_index.query_engine import KnowledgeGraphQueryEngine

from llama_index.response_synthesizers import get_response_synthesizer, CompactAndRefine
from hetio_prompts import entity_labels_parser, entity_labels_classification_template, \
                                    entity_matching_parser, entity_matching_template, \
                                    graph_q_with_ER_prompt, refine_prompt
from neo4j import GraphDatabase
from openai import OpenAI as OpenAI_cli
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def ask_llm(prompt:str, parser:Callable):
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
    try:
        answer = parser(completion.choices[0].message.content)
        return answer 
    except Exception as e:
        print(e)
        print(completion.choices[0].message.content)

def get_entity_labels_with_llm(query, node_types):
    prompt = entity_labels_classification_template.format(node_types=node_types, question=query)
    entity_labels = ask_llm(prompt, entity_labels_parser)
    return entity_labels

def match_entity_with_llm(query:str, entity_labels:Dict, node_names_dict:Dict):
    try:
        matched_entities = {}
        for entity in entity_labels.keys():
            node_names = node_names_dict[entity_labels[entity]]
            prompt = entity_matching_template.format(node_names=node_names, entity=entity)
            matched_entity = ask_llm(prompt, entity_matching_parser)
            matched_entities.update(matched_entity)

        for match in matched_entities.keys():
            modified_query = query.replace(match, matched_entities[match])
    except Exception as e:
        print(e)
        modified_query = query
    return modified_query

class graph_QA():
    def __init__(self, url, user, pwd, db):
        self.url = url
        self.user = user
        self.pwd = pwd
        self.db = db
        graph_store = Neo4jGraphStore(
            url=self.url,
            username=self.user,
            password=self.pwd,
            database=self.db
        )
        self.graph_store_node_labels = self.get_nodetypes()
        self.graph_store_node_names_by_label = self.get_node_names_by_type()
        self.storage_context = StorageContext.from_defaults(graph_store=graph_store)

        self.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)
        self.embedding_llm = OpenAIEmbedding(model="text-embedding-ada-002", temperature=0, api_key=OPENAI_API_KEY)
        self.service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model=self.embedding_llm
        )

        self.response_synth = self.build_response_synth()
        self.query_engine = self.kg_query_engine()

    def build_response_synth(self):
        synth = CompactAndRefine(service_context=self.service_context, refine_template=refine_prompt, verbose=True)
        return synth
    
    def get_nodetypes(self):
        with GraphDatabase.driver(self.url, auth=(self.user, self.pwd)) as driver:
            records, summary, keys = driver.execute_query(
                "call db.labels()",
                database_=self.db
            )
            node_types = [x.data()['label'] for x in records if isinstance(x.data()['label'], str)]
        return node_types
    
    def get_node_names_by_type(self):
        names_by_type = {}
        for node_type in self.graph_store_node_labels:
            with GraphDatabase.driver(self.url, auth=(self.user, self.pwd)) as driver:
                records, summary, keys = driver.execute_query(
                    f"MATCH (p:{node_type}) RETURN p as {node_type}",
                    database_=self.db
                )
            node_names = [x.data()[node_type] for x in records if isinstance(x.data()[node_type], str)]
            names_by_type[node_type] = node_names
        return names_by_type
    
    def kg_query_engine(self):
        query_engine = KnowledgeGraphQueryEngine(
            storage_context=self.storage_context,
            service_context=self.service_context,
            response_synthesizer=self.response_synth,
            llm=self.llm,
            verbose=True,
        )
        
        query_engine.update_prompts({
            'graph_query_synthesis_prompt':graph_q_with_ER_prompt,
            # 'graph_response_answer_prompt':graph_response_answer_prompt
        })
        return query_engine
    
    def ask(self, query:str, test=False):
        entity_labels = get_entity_labels_with_llm(query=query, node_types=self.graph_store_node_labels)
        modified_query = match_entity_with_llm(query=query, entity_labels=entity_labels, node_names_dict=self.graph_store_node_names_by_label)
        try:
            answer = self.query_engine.query(modified_query)
        except:
            {'query_engine_response':'Failure during graphstore query', 
                    'raw_query_str':query,
                    'query_with_context':modified_query}
        if test:
            return answer 
        else:
            return {'query_engine_response':answer.response, 
                    'raw_query_str':query,
                    'query_with_context':modified_query}

