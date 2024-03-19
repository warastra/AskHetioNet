from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema.document import Document 
from langchain.retrievers import ParentDocumentRetriever

import os
from typing import List, Union
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
# GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


class chromaStore:
    def __init__(self, docs:List[Document], persist_dir:str=None, embeddings=None, text_splitter=None, parent_splitter=None):
        self.llm_embeddings = embeddings or OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.text_splitter = text_splitter or RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
        self.parent_splitter = parent_splitter or RecursiveCharacterTextSplitter(chunk_size=2000)
        self.persist_dir = persist_dir
        self.docs = docs

    def as_retriever(self):
        # doc_pages_split = self.text_splitter.transform_documents(self.docs)
        # self.vector_index = Chroma.from_documents(
        #     doc_pages_split,
        #     self.llm_embeddings,
        #     persist_directory=self.persist_dir
        # )

        store = InMemoryStore()
        vectorstore = Chroma(
            collection_name="split_parents", embedding_function=self.llm_embeddings
        )
        self.retriever = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=store,
            child_splitter=self.text_splitter,
            parent_splitter=self.parent_splitter,
        )
        
        self.retriever.add_documents(self.docs)

        return self.retriever
    

    
         
