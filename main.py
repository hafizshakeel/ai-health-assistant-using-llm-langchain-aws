from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from src.helper import download_hf_embeddings
from src.prompt import system_prompt
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG components at startup
embeddings = download_hf_embeddings()
index_name = "medical-chatbot-app"
docs_search = PineconeVectorStore.from_existing_index(
    index_name=index_name, 
    embedding=embeddings
)
retriever = docs_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# Initialize LLM and chain
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_tokens=500,
    api_key=GROQ_API_KEY
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, chain)

class Query(BaseModel):
    question: str
    conversation_history: Optional[List[dict]] = None

class Response(BaseModel):
    answer: str
    sources: Optional[List[str]] = None

@app.post("/ask", response_model=Response)
async def ask_question(query: Query):
    try:
        # Process the query through RAG chain
        response = rag_chain.invoke({
            "input": query.question
        })
        
        # Extract sources from retrieved documents
        sources = []
        if response.get("context"):
            sources = [doc.metadata.get("source", "Unknown") for doc in response["context"]]
        
        return Response(
            answer=response["answer"],
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)