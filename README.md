# AI-Based Knowledge Retrieval Platform with Multi-Agent Query Resolution System

An end-to-end Retrieval-Augmented Generation (RAG) platform featuring document ingestion (PDF, DOCX, TXT, CSV), text cleaning, LangChain chunking, SentenceTransformers embedding, ChromaDB vector storage, SQLite metadata DB, a 5-Agent query processing framework, Web Speech API voice interface, and an empirical 100% accuracy retrieval benchmark.

---

## 🌟 Key Features

- **Multi-Format Knowledge Base Ingestion**: Parses PDF (PyMuPDF), Word DOCX (`python-docx`), Plain Text TXT (multi-encoding fallback), and CSV (`pandas` / structured data reader).
- **LangChain Text Chunking**: Adaptive `RecursiveCharacterTextSplitter` with configurable chunk size (default 500 chars) and overlap (default 50 chars).
- **Dense Vector Search**: Embeds document passages into 384-dimensional vectors using `sentence-transformers/all-MiniLM-L6-v2` indexed in **ChromaDB**.
- **5-Agent Query Processing Architecture**:
  1. **Query Understanding Agent**: Classifies queries (**Factual**, **Procedural**, **Comparative**, **Ambiguous**) and routes to resolution paths (`factual_direct`, `procedural_workflow`, `comparative_matrix`, `ambiguous_clarification`).
  2. **Retrieval Agent**: Executes ChromaDB similarity search, hybrid relevance ranking (70% Cosine Vector + 30% Keyword Density), and low-confidence result filtering (<0.35 threshold).
  3. **Clarification Agent**: Evaluates similarity thresholds and triggers dynamic follow-up clarification options if queries are ambiguous.
  4. **Conversation Memory Agent**: Maintains session dialogue context in SQLite.
  5. **Response Generation Agent**: Synthesizes grounded answers tailored to resolution paths via Groq Llama-3 (or grounded fallback engine) with source attribution citations and confidence indicator meters.
- **Web Speech API Voice UI**: Browser-native Speech-to-Text (`SpeechRecognition` mic recording) and Text-to-Speech (`SpeechSynthesis` audio playback).
- **Retrieval Accuracy Benchmark Dashboard**: Evaluates Top-1, Top-3, and Top-5 accuracy metrics across Cloud Infrastructure & Healthcare domain datasets (**100.0% Accuracy Verified**).

---

## 🏗 System Architecture Diagram

```
                      +---------------------------------------+
                      |       React Web & Voice UI            |
                      | (Web Speech API - STT & TTS Voice UI) |
                      +------------------+--------------------+
                                         | REST / SSE APIs
                                         v
                      +---------------------------------------+
                      |         Flask Backend Server          |
                      +----+-----------------------------+----+
                           |                             |
                           v                             v
       +-----------------------------------+  +-----------------------------------+
       | Knowledge Base Ingestion Pipeline |  |     AI Multi-Agent Layer          |
       |  - Extraction (PyMuPDF, docx,     |  |  - 1. Query Understanding Agent   |
       |    pandas, TXT)                   |  |  - 2. Retrieval Agent (ChromaDB)  |
       |  - Cleaning & Normalization       |  |  - 3. Clarification Agent         |
       |  - LangChain Text Chunking        |  |  - 4. Conversation Memory Agent   |
       |  - SentenceTransformers Embedding |  |  - 5. Response Generation Agent   |
       |  - ChromaDB Vector Indexing       |  |  - Multi-Agent Orchestrator       |
       |  - SQLite Metadata DB             |  +------------------+----------------+
       +-----------------+-----------------+                     |
                         |                                       v
                         +-------------------------> [ Groq LLM API (Llama 3) ]
```

---

## 💻 Technical Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React.js (Vite) + Lucide Icons | Web user interface & dashboard |
| **Backend** | Python 3.13 + Flask + Flask-CORS | REST API server & pipeline coordinator |
| **PDF Parser** | PyMuPDF (`pymupdf` / `fitz`) | PDF page text extraction |
| **DOCX Parser** | `python-docx` | Word document paragraph & table extraction |
| **TXT Parser** | Python native | Multi-encoding text reader |
| **CSV Parser** | `pandas` / native CSV | Tabular record formatting |
| **Chunking** | LangChain `RecursiveCharacterTextSplitter` | Document text chunking |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) | 384-dimensional vector generation |
| **Vector DB** | ChromaDB | Local persistent vector storage & similarity search |
| **Metadata DB** | SQLite3 (`knowledge_base.db`) | Document & chunk metadata tracking |
| **LLM Model** | Groq API + Llama-3 | Grounded response generation |
| **Voice UI** | Web Speech API | Speech-to-Text & Text-to-Speech |
| **Version Control**| Git | Codebase version management |

---

## 📂 Repository Directory Structure

```
rag-multiagent-platform/
├── backend/
│   ├── app.py                      # Flask REST API Endpoints
│   ├── config.py                   # System Configurations & Paths
│   ├── database.py                 # SQLite Schema Definitions & Operations
│   ├── create_sample_docs.py       # Multi-Domain Sample Dataset Generator
│   ├── seed_and_evaluate.py        # Seed Database & Run Accuracy Benchmark
│   ├── ingestion/
│   │   ├── extractor.py            # PDF, DOCX, TXT, CSV Extractor
│   │   ├── cleaner.py              # Text Normalization & Cleaning
│   │   ├── chunker.py              # LangChain Text Splitter
│   │   ├── embedder.py             # SentenceTransformers Embedder
│   │   ├── vector_store.py         # ChromaDB Vector Store Manager
│   │   └── pipeline.py             # End-to-End Ingestion Pipeline
│   ├── agents/
│   │   ├── schemas.py              # Data Models & Schemas
│   │   ├── query_understanding.py  # Query Classification & Path Routing Agent
│   │   ├── retrieval.py            # Hybrid Retrieval & Relevance Ranking Agent
│   │   ├── clarification.py        # Ambiguity & Threshold Guard Agent
│   │   ├── memory.py               # Dialogue State Conversation Memory Agent
│   │   ├── response_generator.py   # Grounded Synthesis & Citation Agent
│   │   └── orchestrator.py         # Sequential Multi-Agent Orchestrator
│   ├── eval/
│   │   └── evaluate.py             # RAG Accuracy Benchmark Suite
│   └── sample_docs/
│       ├── domain1_it_cloud/       # Cloud & DevOps PDF, DOCX, TXT, CSV Files
│       └── domain2_healthcare/     # Healthcare PDF, DOCX, TXT, CSV Files
└── frontend/
    ├── src/
    │   ├── App.jsx                 # Main Application Container
    │   ├── components/
    │   │   ├── Navbar.jsx          # Top Navigation Bar
    │   │   ├── IngestionModule.jsx # Drag & Drop Ingestion & Chunking UI
    │   │   ├── QueryWorkspace.jsx  # Voice/Text Query UI & Agent Trace Stream
    │   │   ├── AgentArchitectureView.jsx # Visual Multi-Agent Architecture
    │   │   ├── DocumentBrowser.jsx # Document Repository & Chunk Viewer Modal
    │   │   └── EvaluationDashboard.jsx # RAG Retrieval Accuracy Dashboard
    │   └── index.css               # Modern Glassmorphism Styling
    └── package.json
```

---

## 📊 Benchmark Retrieval Accuracy Results

Automated evaluation benchmark across **10 test queries** spanning **Factual**, **Procedural**, **Comparative**, and **Unavailable** query types across Cloud Infrastructure & Healthcare domain datasets:

```
================ BENCHMARK RESULTS ================
Total Evaluated Queries  : 10
Top-1 Retrieval Accuracy : 100.0%
Top-3 Retrieval Accuracy : 100.0%
Top-5 Retrieval Accuracy : 100.0%
====================================================
```

---

## 🚀 Setup & Installation Instructions

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
python database.py
python create_sample_docs.py
python seed_and_evaluate.py
python app.py
```
*Backend server will start on `http://localhost:5000`.*

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Frontend web application will start on `http://localhost:5173`.*

---

## 📜 License
MIT License.
