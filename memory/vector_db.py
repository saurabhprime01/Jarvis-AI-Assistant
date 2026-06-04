import os
from app.core.config import settings
from loguru import logger
import google.generativeai as genai

class VectorMemory:
    def __init__(self):
        self.use_pinecone = bool(settings.PINECONE_API_KEY)
        self.index = None
        self.chroma_client = None
        self.collection = None

        if self.use_pinecone:
            logger.info("Initializing Pinecone Cloud Vector DB...")
            try:
                from pinecone import Pinecone, ServerlessSpec
                self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
                
                # Check if index exists, else create it
                existing_indexes = [idx.name for idx in self.pc.list_indexes()]
                if settings.PINECONE_INDEX not in existing_indexes:
                    logger.info(f"Creating Pinecone index: {settings.PINECONE_INDEX}")
                    self.pc.create_index(
                        name=settings.PINECONE_INDEX,
                        dimension=768,  # Gemini text-embedding-004 dimension
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud="aws",
                            region="us-east-1"
                        )
                    )
                self.index = self.pc.Index(settings.PINECONE_INDEX)
                # Configure generative ai key if not done
                if settings.GOOGLE_API_KEY:
                    genai.configure(api_key=settings.GOOGLE_API_KEY)
            except Exception as e:
                logger.error(f"Failed to initialize Pinecone, falling back to local ChromaDB: {e}")
                self.use_pinecone = False

        if not self.use_pinecone:
            logger.info("Initializing local ChromaDB Vector store...")
            import chromadb
            self.persist_directory = settings.VECTOR_DB_PATH
            if not os.path.exists(self.persist_directory):
                os.makedirs(self.persist_directory)
            self.chroma_client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.chroma_client.get_or_create_collection(name="jarvis_memory")

    def _get_gemini_embedding(self, text: str) -> list:
        """Helper to generate vector embeddings using Gemini model."""
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating Gemini embedding: {e}")
            raise e

    def add_memory(self, content: str, metadata: dict = None):
        """Adds a memory to the vector store (Pinecone or ChromaDB)."""
        try:
            if self.use_pinecone:
                embedding = self._get_gemini_embedding(content)
                # Generate unique ID based on timestamp or count
                import time
                mem_id = f"mem_{int(time.time() * 1000)}"
                self.index.upsert(
                    vectors=[
                        {
                            "id": mem_id,
                            "values": embedding,
                            "metadata": {**(metadata or {}), "text": content}
                        }
                    ]
                )
                logger.info(f"Memory added to Pinecone: {mem_id}")
            else:
                mem_id = f"mem_{self.collection.count() + 1}"
                self.collection.add(
                    documents=[content],
                    metadatas=[metadata or {}],
                    ids=[mem_id]
                )
                logger.info(f"Memory added to ChromaDB: {mem_id}")
        except Exception as e:
            logger.error(f"Error adding to vector memory: {e}")

    def search_memories(self, query: str, n_results: int = 3):
        """Searches for relevant memories (Pinecone or ChromaDB)."""
        try:
            if self.use_pinecone:
                embedding = self._get_gemini_embedding(query)
                results = self.index.query(
                    vector=embedding,
                    top_k=n_results,
                    include_metadata=True
                )
                # Format response similarly to ChromaDB
                formatted_docs = []
                formatted_metadatas = []
                for match in results.get("matches", []):
                    meta = match.get("metadata", {})
                    text = meta.pop("text", "")
                    formatted_docs.append(text)
                    formatted_metadatas.append(meta)
                
                return {
                    "documents": [formatted_docs],
                    "metadatas": [formatted_metadatas]
                }
            else:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
                return results
        except Exception as e:
            logger.error(f"Error searching vector memory: {e}")
            return None

vector_memory = VectorMemory()
