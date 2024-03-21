import os
from fastapi import FastAPI, Depends
from hetio_graph_qa import graph_QA
from pydantic import create_model
import logging
logging.basicConfig(filename='main_v8_log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
import uvicorn
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

AURA_URI = os.environ.get('AURA_URI')
AURA_USER = os.environ.get('AURA_USER')
AURA_PASS = os.environ.get('AURA_PASS')   
HETIONET_URL='bolt://neo4j.het.io:7687'

hetionetQA = graph_QA(
        url = AURA_URI, # Aura instance URL
        user=AURA_USER, # Aura instance username
        pwd=AURA_PASS,  # Aura instance password
        db='neo4j'      # Aura instance database name, the default is 'neo4j'
    )
app = FastAPI()

query_params = {"q": (str, "me")}
query_model = create_model("Query", **query_params) 

# dory cos No chat history
@app.get("/ask_hetionet/")
async def get_hetio_answer(params: query_model = Depends()):
    
    params_as_dict = params.dict()
    query = params_as_dict['q']
    logging.info(f" query: {query}")
    try:
        answer = hetionetQA.ask(query)
    except Exception as e:
        print(e)
        answer ={
            'query_engine_response':'No information found', 
            'raw_query_str':query,
            'query_with_context':query
        }
    return answer

if __name__ == "__main__":
    print('starting local FastAPI server with Uvicorn')
    uvicorn.run("main_v8:app", host="0.0.0.0", port=8001, reload=True)