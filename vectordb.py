import chromadb
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embedding_model = OllamaEmbeddings(model = "mxbai-embed-large")

vector_store = Chroma(
    collection_name="temp",
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)