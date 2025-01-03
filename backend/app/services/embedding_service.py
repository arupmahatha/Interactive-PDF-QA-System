from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List

class EmbeddingService:
    def __init__(self):
        # Using all-MiniLM-L6-v2 - a lightweight but effective embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None

    def create_embeddings(self, documents: List[dict]):
        """
        Creates and stores embeddings in ChromaDB
        """
        texts = [doc["content"] for doc in documents]
        metadatas = [{
            "page_number": doc["page_number"],
            "source": doc["source"]
        } for doc in documents]

        self.vector_store = Chroma.from_texts(
            texts=texts,
            metadatas=metadatas,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
        
    def similarity_search(self, query: str, k: int = 3):
        """
        Performs similarity search to find relevant documents
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
            
        return self.vector_store.similarity_search(query, k=k) 