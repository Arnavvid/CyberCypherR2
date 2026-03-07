from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# Embedding model (via Ollama)
embeddings = OllamaEmbeddings(
    model="mxbai-embed-large"
)

# Persistent vector database
vectordb = Chroma(
    collection_name="network_incidents",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


def telemetry_to_text(t):

    return f"""
    Network telemetry snapshot:

    Latency: {t['latency']} ms
    Packet Loss: {t['packet_loss']} %
    Throughput: {t['throughput']} Mbps
    Device Health: {t['device_health']}
    Routing Status: {t['routing_status']}
    """


def add_incident(telemetry, diagnosis, tool):

    text = telemetry_to_text(telemetry)

    doc = Document(
        page_content=text,
        metadata={
            "diagnosis": diagnosis,
            "tool": tool
        }
    )

    vectordb.add_documents([doc])


def search_similar(telemetry, k=3):

    query = telemetry_to_text(telemetry)

    results = vectordb.similarity_search(query, k=k)

    incidents = []

    for doc in results:
        incidents.append({
            "text": doc.page_content,
            "diagnosis": doc.metadata["diagnosis"],
            "tool": doc.metadata["tool"]
        })

    return incidents