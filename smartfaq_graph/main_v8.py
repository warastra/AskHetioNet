import os
from fastapi import FastAPI, Depends
from ai_search import req_body, refine_QA
from ai_readRetrieveQA import thematicSearch_QA, simpleSearch_QA, answer_check
from pydantic import BaseModel, create_model
from typing import List, Dict
import logging
logging.basicConfig(filename='main_v8_log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
import uvicorn
import re

# bijak_memilih_graph = graph_QA(db_name='neo4j')
# bijak_memilih_search = Search_QA(agent_type='ReAct')
# bijak_memilih_wiki = wiki_QA(chroma_db_dir='capres_vectors')
thematic = thematicSearch_QA(engine_type='climate')
simpleSearch = simpleSearch_QA(engine_type='whole_web')


class body(BaseModel):
    question: str
    chat_history:List[Dict]=None

app = FastAPI()

query_params = {"q": (str, "me"), "chat_history":(List[Dict], None)}
query_model = create_model("Query", **query_params) 

# dory cos No chat history
@app.get("/thematic_search/")
async def get_thematic_answer(params: query_model = Depends()):
    
    params_as_dict = params.dict()
    query = params_as_dict['q']
    chat_history = params_as_dict['chat_history']
    logging.info(f" query: {query}")
    error_flag = False
    try:
        thematic_answer = thematic.ask(query, chat_history)
    except Exception as e:
        print(e)
        error_flag = True
        thematic_answer ={
            'query_engine_response':'No relevant documents found', 
            'raw_query_str':query,
            'query_with_context':query,
            'entities':[],
            'sources':[]
        }
    temp_answer_status_code = answer_check(thematic_answer)
    if  error_flag or temp_answer_status_code != 200:
        print('ThematicSearch unable to find answer, expanding search scope..')
        search_answer = simpleSearch.ask(query, chat_history)
        # wiki_answer = bijak_memilih_wiki.ask(query, chat_history)
        answer_list = [search_answer]
        refined_answer, summarized_sources = refine_QA(answer_list)
        summarized_sources = [item for sublist in summarized_sources for item in sublist]
        
    else:
        answer_list = [thematic_answer]
        refined_answer, summarized_sources = refine_QA(answer_list)
        summarized_sources = [item for sublist in summarized_sources for item in sublist]
    
    str_src = ','.join(summarized_sources)
    logging.info(f" query: {query} \nanswer: {refined_answer}\nsource:{str_src}")
    # answer = agent_executor.invoke({"input": body.question})['output']
    return {
        'refined_answer':refined_answer,
        'sources':summarized_sources,
        'raw_answers':answer_list
    }

    # return thematic_answer

@app.post("/thematic_search_with_history/")
async def get_thematic_answer_w_hist(body:req_body):
    query = body.q
    chat_history = body.chat_history
    logging.info(f" query: {query}")
    error_flag = False
    try:
        thematic_answer = thematic.ask(query, chat_history)
    except Exception as e:
        print(e)
        error_flag = True
        thematic_answer ={
            'query_engine_response':'No relevant documents found', 
            'raw_query_str':query,
            'query_with_context':query,
            'entities':[],
            'sources':[]
        }
    temp_answer_status_code = answer_check(thematic_answer['query_engine_response'])
    if  error_flag or temp_answer_status_code != 200:
        print('ThematicSearch unable to find answer, expanding search scope..')
        search_answer = simpleSearch.ask(query, chat_history)
        # wiki_answer = bijak_memilih_wiki.ask(query, chat_history)
        answer_list = [thematic_answer, search_answer]
        refined_answer, summarized_sources = refine_QA(answer_list)
        summarized_sources = [item for sublist in summarized_sources for item in sublist]
        
    else:
        answer_list = [thematic_answer]
        refined_answer, summarized_sources = refine_QA(answer_list)
        summarized_sources = [item for sublist in summarized_sources for item in sublist]
    
    str_src = ','.join(summarized_sources)
    logging.info(f" query: {query} \nanswer: {refined_answer}\nsource:{str_src}")
    # answer = agent_executor.invoke({"input": body.question})['output']
    return {
        'refined_answer':refined_answer,
        'sources':summarized_sources,
        'raw_answers':answer_list
    }

if __name__ == "__main__":
    uvicorn.run("main_v8:app", host="0.0.0.0", port=8001, reload=True)