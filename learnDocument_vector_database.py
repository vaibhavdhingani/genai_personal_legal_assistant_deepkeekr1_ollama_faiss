from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os

## Upload and load PDF
pdf_directory = "pdfs/"
def upload_pdf(file):
    with open(pdf_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(pdf_directory+file_path.name)
    documents = loader.load()
    return documents

## Create Chunks for Vector database
def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    add_start_index = True
    )
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks

## Setup Embedding Model (Using DeepSeek R1 with Ollama)
ollama_model_name="deepseek-r1:8b"
def get_embedding_model(ollama_model_name):
    embeddings = OllamaEmbeddings(model=ollama_model_name)
    return embeddings

## Index Document, Store embedding in FAISS
FAISS_DB_PATH="vectrostore/db_faiss"

def create_vector_store(uploaded_file):
    upload_pdf(uploaded_file)
    documents = load_pdf(uploaded_file)
    text_chunks = create_chunks(documents)
    faiss_db=FAISS.from_documents(text_chunks, get_embedding_model(ollama_model_name))
    faiss_db.save_local(FAISS_DB_PATH)
    os.remove(pdf_directory+uploaded_file.name)
    return faiss_db