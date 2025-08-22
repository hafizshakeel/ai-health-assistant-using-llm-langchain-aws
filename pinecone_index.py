from dotenv import load_dotenv
import os
from src.helper import *
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# Load environment variables from .env file
load_dotenv()

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Set environment variables for the libraries to use
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# Load, filter, and chunk documents
path = "data"
extracted_data = load_pdf_files(path)
filterd_data = filter_to_minimal_docs(extracted_data)
chunk_of_texts = text_split(filterd_data)

# Download embeddings model
embeddings = download_hf_embeddings()

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create Pinecone index if it doesn't exist
index_name = "medical-chatbot-app"

if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension=384,  # Dimension of the embeddings
        metric= "cosine",  #  Metric for measuring similarity
        spec=ServerlessSpec(cloud="aws", region="us-east-1") # Serverless configuration
    )


index = pc.Index(index_name)

# Create Pinecone vector store from documents
docs_search = PineconeVectorStore.from_documents(
    documents=chunk_of_texts, embedding=embeddings, index_name=index_name
)

print("Pinecone index created and documents added successfully.")
