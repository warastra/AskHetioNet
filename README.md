# AskHetioNet
A chatbot interface to ask questions reagrding informations contained in HetioNet, a biomedical knowledge graph intended to explore drug repurposing. See Reference for more information on HetioNet.
Under the hood, an LLM will convert user's natural language query to a relevant cypher query and summarize the answer from the cypher query output. 
The current version need to copy HetioNet to your own Neo4j Aura instance. The future direction is to directly read from the [publicly hosted version on Neo4j](https://neo4j.het.io/browser/)

## Setup
1. Clone this repository
2. Download and extract the zipped hetionet JSON available at the [HetioNet github repo](https://github.com/hetio/hetionet/tree/main/hetnet/json)
3. Run the `preprocessing_script.py` to create CSV files to be uploaded to your own Neo4j Aura instance
4. Upload the csv files to Neo4j Aura instance and setup the schema
   ![image](https://github.com/warastra/AskHetioNet/assets/36398445/a556def7-97df-4aa4-aff2-f33c4e5ed82f)

## Usage Example
### As Python script
```
from hetio_graph_qa import graph_QA
from dotenv import load_dotenv
import os

load_dotenv()
AURA_URI = os.environ.get('AURA_URI')
AURA_USER = os.environ.get('AURA_USER')
AURA_PASS = os.environ.get('AURA_PASS')  

askHET = graph_QA(
    url = AURA_URI, # Aura instance URL
    user=AURA_USER, # Aura instance username
    pwd=AURA_PASS,  # Aura instance password
    db='neo4j'      # Aura instance database name, the default is 'neo4j'
)

answer = askHET.ask('Name three genes in chromosome 2 associated with disease that attacks both digestive system and hematopoietic system?')
print(answer)
```
### Streamlit Interface
1. to start the fastAPI server locally, run the `main_v8.py`. for example, in terminal run command `python main_v8.py`.
2. to start the streamlit app, open another terminal and run command `streamlit run streamlit_interface.py`
3. start `localhost:8501` on a browser

![image](https://github.com/warastra/AskHetioNet/assets/36398445/42fcc6b8-fb38-42f3-a93b-a2bf9b67831d)

# References
> Systematic integration of biomedical knowledge prioritizes drugs for repurposing
> Daniel Scott Himmelstein, Antoine Lizee, Christine Hessler, Leo Brueggeman, Sabrina L Chen, Dexter Hadley, Ari Green, Pouya Khankhanian, Sergio E Baranzini
> eLife (2017-09-22) https://git.dhimmel.com/rephetio-manuscript/
> DOI: 10.7554/elife.26726 · PMID: 28936969 · PMCID: PMC5640425
