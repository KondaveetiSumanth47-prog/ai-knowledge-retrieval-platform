import math
import hashlib
from typing import List
from config import EMBEDDING_MODEL_NAME

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

class FallbackHashEmbedder:
    """Generates normalized 384-d vector embeddings using hashing when SentenceTransformers wheel is unzipping"""
    def encode(self, texts: List[str]) -> List[List[float]]:
        results = []
        for text in texts:
            vec = [0.0] * 384
            words = text.lower().split()
            for w in words:
                h = int(hashlib.md5(w.encode('utf-8')).hexdigest(), 16)
                idx = h % 384
                val = (h % 1000) / 1000.0 - 0.5
                vec[idx] += val
            norm = math.sqrt(sum(v*v for v in vec)) or 1.0
            results.append([v / norm for v in vec])
        return results

class EmbeddingGenerator:
    """
    Singleton wrapper around SentenceTransformers model (with hash embedder fallback).
    """
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingGenerator, cls).__new__(cls)
            if HAS_SENTENCE_TRANSFORMERS:
                try:
                    print(f"Loading SentenceTransformers model: {EMBEDDING_MODEL_NAME}...")
                    cls._model = SentenceTransformer(EMBEDDING_MODEL_NAME)
                    print("Embedding model loaded successfully.")
                except Exception as e:
                    print(f"Warning: SentenceTransformers init error ({e}), using FallbackHashEmbedder.")
                    cls._model = FallbackHashEmbedder()
            else:
                print("Notice: sentence-transformers importing, using FallbackHashEmbedder.")
                cls._model = FallbackHashEmbedder()
        return cls._instance

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        if hasattr(self._model, 'encode'):
            embeddings = self._model.encode(texts)
            if hasattr(embeddings, 'tolist'):
                return embeddings.tolist()
            return embeddings
        return []

    def generate_single_embedding(self, text: str) -> List[float]:
        return self.generate_embeddings([text])[0]
