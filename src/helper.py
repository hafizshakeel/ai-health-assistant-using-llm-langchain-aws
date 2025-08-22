"""
Helper functions for loading, filtering, splitting text, and downloading embeddings.
"""

from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings 
import torch
device = torch.device("cuda" if torch.cuda.is_available else 'cpu')

# load all pdf files from a directory
def load_pdf_files(path):
    loader = DirectoryLoader(path, glob="*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    return docs

 
 # filter the docs to only keep the page_content and source metadata
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(page_content=doc.page_content, metadata={"source": src})
        )
    return minimal_docs


# text splitting 
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 100)
    chunk_of_texts = text_splitter.split_documents(minimal_docs)
    return chunk_of_texts

# download huggingface embeddings
def download_hf_embeddings():
    model = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name = model,
        # model_kwargs = {"device": device }
    )
    return embeddings


