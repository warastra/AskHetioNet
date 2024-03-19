from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import WikipediaLoader
from langchain.embeddings.openai import OpenAIEmbeddings

import  os
from dotenv import load_dotenv, find_dotenv
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

entities = ['Ganjar Pranowo', 'Mahfud MD', 'Anies Baswedan', 'Muhaimin Iskandar', 'Prabowo Subianto', 'Gibran Rakabuming']
docs = []
for ent in entities:
    docs.append(WikipediaLoader(query=ent, load_max_docs=1, lang='id').load()[0])

llm_embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
doc_pages_split = text_splitter.transform_documents(docs)

chroma_db_dir = 'capres_vectors'
vector_index = Chroma.from_documents(
            doc_pages_split,
            llm_embeddings,
            persist_directory=chroma_db_dir
        ).as_retriever()

query = "apa saja aplikasi yg pernah dibangun gibran?"
print(query)
sub_docs = vector_index.similarity_search(query)
print('vector search', [(x.page_content[:20], x.metadata) for x in sub_docs])