# Adding Chat history to v4
import os
from fastapi import FastAPI
from open_ai_graph_qa import graph_QA
from ai_search import Search_QA, wiki_QA
from pydantic import BaseModel, Field
from typing import List, Dict

bijak_memilih_graph = graph_QA(db_name='neo4j')
bijak_memilih_search = Search_QA(agent_type='ReAct')
bijak_memilih_wiki = wiki_QA(chroma_db_dir='capres_vectors')



class body(BaseModel):
    question: str
    chat_history:List[Dict]=None

app = FastAPI()

@app.post("/ask/")
async def root(body:body):

    # Ask a question and get an answer
    # question = "Apakah partai demokrat menentang atau mendukung UU minerba? sebutkan alasannya"
    graph_answer = bijak_memilih_graph.ask(body.question, body.chat_history)
    # if 'tidak ditemukan' in answer['query_engine_response'].response:
    search_answer = bijak_memilih_search.ask(body.question, body.chat_history)
    wiki_answer = bijak_memilih_wiki.ask(body.question, body.chat_history)
    # answer = ganjar_chat.chain_tools(body.question)
    
    # answer = agent_executor.invoke({"input": body.question})['output']
    return [graph_answer, search_answer, wiki_answer]