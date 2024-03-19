# Adding Chat history to v4
import os
from fastapi import FastAPI
from open_ai_graph_qa import graph_QA
from pydantic import BaseModel, Field
from typing import List, Dict

bijak_memilih = graph_QA(db_name='neo4j')


class body(BaseModel):
    question: str
    chat_history:List[Dict]=None

app = FastAPI()

@app.post("/ask/")
async def root(body:body):

    # Ask a question and get an answer
    # question = "Apakah partai demokrat menentang atau mendukung UU minerba? sebutkan alasannya"
    answer = bijak_memilih.ask(body.question, body.chat_history)
    # answer = ganjar_chat.chain_tools(body.question)
    
    # answer = agent_executor.invoke({"input": body.question})['output']
    return answer