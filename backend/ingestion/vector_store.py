import math
from typing import List, Dict, Any, Optional
from config import CHROMA_DB_DIR
from ingestion.embedder import EmbeddingGenerator

try:
    import chromadb
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False

class MemoryVectorStore:
    """In-memory cosine similarity vector store fallback when ChromaDB wheel is unzipping"""
    def __init__(self):
        self.store = []

    def add(self, ids: List[str], embeddings: List[List[float]], documents: List[str], metadatas: List[Dict[str, Any]]):
        for i in range(len(ids)):
            self.store.append({
                "id": ids[i],
                "embedding": embeddings[i],
                "document": documents[i],
                "metadata": metadatas[i]
            })

    def query(self, query_embeddings: List[List[float]], n_results: int = 5, where: Optional[Dict[str, Any]] = None):
        q_vec = query_embeddings[0]
        scored = []
        for item in self.store:
            meta = item['metadata']
            if where and where.get('domain'):
                if meta.get('domain') != where['domain']:
                    continue

            # Cosine similarity calculation
            doc_vec = item['embedding']
            dot = sum(a * b for a, b in zip(q_vec, doc_vec))
            norm_q = math.sqrt(sum(a * a for a in q_vec)) or 1.0
            norm_d = math.sqrt(sum(b * b for b in doc_vec)) or 1.0
            sim = dot / (norm_q * norm_d)
            dist = 1.0 - sim

            scored.append((dist, item['id'], item['document'], meta))

        scored.sort(key=lambda x: x[0])
        top = scored[:n_results]

        return {
            "ids": [[t[1] for t in top]],
            "documents": [[t[2] for t in top]],
            "metadatas": [[t[3] for t in top]],
            "distances": [[t[0] for t in top]]
        }

    def delete(self, where: Dict[str, Any]):
        doc_id = where.get('document_id')
        if doc_id:
            self.store = [item for item in self.store if item['metadata'].get('document_id') != doc_id]

class VectorStoreManager:
    """
    Manages persistent ChromaDB vector store collection (with in-memory fallback).
    """
    def __init__(self, collection_name: str = "knowledge_base"):
        self.collection_name = collection_name
        self.embedder = EmbeddingGenerator()
        if HAS_CHROMADB:
            try:
                self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
                self.collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                self.using_chroma = True
            except Exception as e:
                print(f"Warning: ChromaDB init error ({e}), using MemoryVectorStore.")
                self.collection = MemoryVectorStore()
                self.using_chroma = False
        else:
            print("Notice: chromadb importing, using MemoryVectorStore.")
            self.collection = MemoryVectorStore()
            self.using_chroma = False

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]], doc_metadata: Dict[str, Any]):
        if not chunks:
            return

        ids = [c['id'] for c in chunks]
        documents = [c['content'] for c in chunks]
        metadatas = [
            {
                "document_id": c['document_id'],
                "chunk_index": c['chunk_index'],
                "filename": doc_metadata.get('filename', ''),
                "domain": doc_metadata.get('domain', ''),
                "file_type": doc_metadata.get('file_type', '')
            }
            for c in chunks
        ]

        if self.using_chroma:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
        else:
            self.collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    def similarity_search(self, query_text: str, top_k: int = 5, domain_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.generate_single_embedding(query_text)
        
        where_clause = None
        if domain_filter and domain_filter.lower() != 'all':
            where_clause = {"domain": domain_filter}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause
        )

        retrieved_items = []
        if results and results.get('ids') and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                doc_id = results['ids'][0][i]
                content = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                similarity_score = max(0.0, min(1.0, 1.0 - distance))

                retrieved_items.append({
                    "chunk_id": doc_id,
                    "content": content,
                    "document_id": meta.get('document_id'),
                    "chunk_index": meta.get('chunk_index'),
                    "filename": meta.get('filename'),
                    "domain": meta.get('domain'),
                    "file_type": meta.get('file_type'),
                    "score": round(similarity_score, 4)
                })

        return retrieved_items

    def delete_document_chunks(self, document_id: str):
        if self.using_chroma:
            self.collection.delete(where={"document_id": document_id})
        else:
            self.collection.delete(where={"document_id": document_id})
