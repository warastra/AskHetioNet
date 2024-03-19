# Adding Chat history to v4
import os
from fastapi import FastAPI, Depends
from open_ai_graph_qa import graph_QA
from ai_search import Search_QA, wiki_QA, refine_QA, req_body as body
from ai_readRetrieveQA import thematicSearch_QA
from pydantic import BaseModel, create_model
from typing import List, Dict

bijak_memilih_graph = graph_QA(db_name='neo4j')
bijak_memilih_search = Search_QA(agent_type='ReAct')
bijak_memilih_wiki = wiki_QA(chroma_db_dir='capres_vectors')
climate = thematicSearch_QA()


app = FastAPI()

@app.post("/ask/")
async def root(body:body):

    # Ask a question and get an answer
    # question = "Apakah partai demokrat menentang atau mendukung UU minerba? sebutkan alasannya"
    graph_answer = bijak_memilih_graph.ask(body.q, body.chat_history)
    # if 'tidak ditemukan' in answer['query_engine_response'].response:
    search_answer = bijak_memilih_search.ask(body.q, body.chat_history)
    wiki_answer = bijak_memilih_wiki.ask(body.q, body.chat_history)
    # answer = ganjar_chat.chain_tools(body.q)
    answer_list = [graph_answer, search_answer, wiki_answer]
    refined_answer, summarized_sources = refine_QA(answer_list)
    
    # answer = agent_executor.invoke({"input": body.q})['output']
    return {
        'refined_answer':refined_answer,
        'sources':summarized_sources,
        'raw_answers':answer_list
    }

query_params = {"q": (str, "me"), "chat_history":(List[Dict], None)}

query_model = create_model("Query", **query_params) 

@app.get("/search/")
async def get_answer(params: query_model = Depends()):
    params_as_dict = params.dict()
    query = params_as_dict['q']
    chat_history = params_as_dict['chat_history']
    # Ask a question and get an answer
    # question = "Apakah partai demokrat menentang atau mendukung UU minerba? sebutkan alasannya"
    graph_answer = bijak_memilih_graph.ask(query, chat_history)
    # if 'tidak ditemukan' in answer['query_engine_response'].response:
    search_answer = bijak_memilih_search.ask(query, chat_history)
    wiki_answer = bijak_memilih_wiki.ask(query, chat_history)
    # answer = ganjar_chat.chain_tools(body.q)
    answer_list = [graph_answer, search_answer, wiki_answer]
    refined_answer, summarized_sources = refine_QA(answer_list)
    
    # answer = agent_executor.invoke({"input": body.q})['output']
    return {
        'refined_answer':refined_answer,
        'sources':summarized_sources,
        'raw_answers':answer_list
    }

@app.get("/climate_search/")
async def get_climate_answer(params: query_model = Depends()):
    params_as_dict = params.dict()
    query = params_as_dict['q']
    chat_history = params_as_dict['chat_history']
    # Ask a question and get an answer
    # question = "Apakah partai demokrat menentang atau mendukung UU minerba? sebutkan alasannya"
    climate_answer = climate.ask(query, chat_history)
    # if 'tidak ditemukan' in answer['query_engine_response'].response:
    search_answer = bijak_memilih_search.ask(query, chat_history)
    wiki_answer = bijak_memilih_wiki.ask(query, chat_history)
    # answer = ganjar_chat.chain_tools(body.q)
    answer_list = [climate_answer, search_answer, wiki_answer]
    refined_answer, summarized_sources = refine_QA(answer_list)
    
    # answer = agent_executor.invoke({"input": body.q})['output']
    return {
        'refined_answer':refined_answer,
        'sources':summarized_sources,
        'raw_answers':answer_list
    }