import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from ingestion.extractor import DocumentExtractor
from ingestion.cleaner import TextCleaner
from ingestion.chunker import DocumentChunker
from ingestion.embedder import EmbeddingGenerator
from ingestion.vector_store import VectorStoreManager
from database import save_document, save_chunks

class IngestionPipeline:
    """
    Complete Knowledge Base Ingestion Pipeline:
    Document Upload -> Text Extraction -> Cleaning -> Chunking -> Embedding -> Vector Store Indexing -> Metadata DB
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunker = DocumentChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStoreManager()

    def process_file(self, file_path: str, filename: str, domain: str = "General", custom_chunk_size: Optional[int] = None, custom_chunk_overlap: Optional[int] = None) -> Dict[str, Any]:
        """
        Executes end-to-end ingestion pipeline for a document file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = os.path.getsize(file_path)
        ext = os.path.splitext(filename)[1].lower().strip('.')
        file_type = ext

        # 1. Text Extraction
        raw_text = DocumentExtractor.extract(file_path, file_type=file_type)

        # 2. Text Cleaning & Normalization
        cleaned_text = TextCleaner.clean(raw_text)

        # 3. Document Chunking
        doc_id = f"doc_{uuid.uuid4().hex[:10]}"
        if custom_chunk_size and custom_chunk_overlap is not None:
            local_chunker = DocumentChunker(chunk_size=custom_chunk_size, chunk_overlap=custom_chunk_overlap)
            chunks = local_chunker.chunk_text(cleaned_text, document_id=doc_id)
        else:
            chunks = self.chunker.chunk_text(cleaned_text, document_id=doc_id)

        chunk_contents = [c['content'] for c in chunks]

        # 4. Embedding Generation
        embeddings = self.embedder.generate_embeddings(chunk_contents)

        # 5. Metadata Object
        doc_metadata = {
            "id": doc_id,
            "filename": filename,
            "file_type": file_type,
            "domain": domain,
            "file_size": file_size,
            "chunk_count": len(chunks),
            "raw_char_count": len(cleaned_text),
            "upload_time": datetime.now().isoformat(),
            "filepath": file_path
        }

        # 6. Save to SQLite Database
        save_document(doc_metadata)
        save_chunks(chunks)

        # 7. Index in ChromaDB Vector Store
        self.vector_store.add_chunks(chunks, embeddings, doc_metadata)

        return {
            "status": "success",
            "document": doc_metadata,
            "chunks_count": len(chunks),
            "preview_chunks": chunks[:3]
        }
