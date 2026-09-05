import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
CHROMA_DB_DIR = os.path.join(DATA_DIR, "chroma_db")
SQLITE_DB_PATH = os.path.join(DATA_DIR, "knowledge_base.db")
SAMPLE_DOCS_DIR = os.path.join(BASE_DIR, "sample_docs")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

# Ingestion settings
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Groq API settings
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama3-8b-8192"
