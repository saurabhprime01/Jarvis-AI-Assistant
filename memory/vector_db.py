import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings
from loguru import logger
import os

class VectorMemory:
    def __init__(self):
        self.persist_directory = settings.VECTOR_DB_PATH
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)
        
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name="jarvis_memory")

    def add_memory(self, content: str, metadata: dict = None):
        """Adds a memory to the vector store."""
        try:
            # Simple ID generation
            mem_id = f"mem_{self.collection.count() + 1}"
            self.collection.add(
                documents=[content],
                metadatas=[metadata or {}],
                ids=[mem_id]
            )
            logger.info(f"Memory added: {mem_id}")
        except Exception as e:
            logger.error(f"Error adding to vector memory: {e}")

    def search_memories(self, query: str, n_results: int = 3):
        """Searches for relevant memories."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error searching vector memory: {e}")
            return None

vector_memory = VectorMemory()
