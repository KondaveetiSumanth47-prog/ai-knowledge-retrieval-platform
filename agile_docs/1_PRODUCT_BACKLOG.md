# Agile Product Backlog - AI Knowledge Retrieval Platform

**Project Name**: AI-Based Knowledge Retrieval Platform with Multi-Agent Query Resolution System  
**Product Owner**: Mentorship Project Team  
**Scrum Master**: Agile Lead  
**Repository**: `rag-multiagent-platform`

---

## 📋 Epic Overview

- **Epic 1: Knowledge Base Ingestion Engine (Completed - Milestone 1)**
- **Epic 2: Core Multi-Agent Query Resolution Pipeline (Completed - Milestone 2)**
- **Epic 3: Voice UI & Interactive Workspace (Completed - Milestone 1/2)**
- **Epic 4: RAG Retrieval Accuracy & Benchmarking Suite (Completed - Milestone 1/2)**
- **Epic 5: Advanced Re-Ranking & Production Optimization (Planned - Milestone 3)**

---

## 🎯 User Stories & Backlog Items

| Story ID | Epic | User Story Statement | Story Points | Acceptance Criteria | Status |
| :--- | :--- | :--- | :---: | :--- | :---: |
| **US-101** | Epic 1 | As a User, I want to upload PDF, DOCX, TXT, and CSV documents so that the system can index enterprise knowledge. | 5 | Supports PyMuPDF, python-docx, TXT, and pandas extraction with error handling. | **DONE** |
| **US-102** | Epic 1 | As a User, I want text split into chunks with configurable size and overlap so that retrieval yields precise passages. | 3 | LangChain `RecursiveCharacterTextSplitter` configured with sliders (200-1500 chars). | **DONE** |
| **US-103** | Epic 1 | As a System, I want text chunks converted to vector embeddings and stored persistently in ChromaDB & SQLite. | 5 | `all-MiniLM-L6-v2` dense vectors indexed in ChromaDB; metadata stored in SQLite. | **DONE** |
| **US-201** | Epic 2 | As a System, I want a Query Understanding Agent to classify queries as Factual, Procedural, Comparative, or Ambiguous. | 5 | Query classified correctly and routed to resolution path (`factual_direct`, `procedural_workflow`, etc.). | **DONE** |
| **US-202** | Epic 2 | As a System, I want a Retrieval Agent to rank chunks using hybrid scoring and filter out low-confidence results. | 5 | Hybrid score (70% Cosine + 30% Keyword Density) applied; chunks <0.35 threshold removed. | **DONE** |
| **US-203** | Epic 2 | As a System, I want a Response Generation Agent to synthesize path-tailored answers with source citations & confidence meters. | 5 | Answers formatted as steps/tables with exact file citations and High/Medium/Low confidence badge. | **DONE** |
| **US-204** | Epic 2 | As a System, I want a Multi-Agent Orchestrator to coordinate agent execution sequentially and log latency telemetry. | 3 | Sequential execution logged with per-agent latency in milliseconds (`latency_ms`). | **DONE** |
| **US-301** | Epic 3 | As a User, I want to dictate queries via microphone and hear answers read aloud using Web Speech API. | 5 | Speech-to-Text (`SpeechRecognition`) and Text-to-Speech (`SpeechSynthesis`) integrated. | **DONE** |
| **US-302** | Epic 3 | As a User, I want a Knowledge Base Browser with a `View Chunks` button to inspect document chunk segments. | 3 | Table renders 18 documents with cyan `View Chunks` modal button. | **DONE** |
| **US-401** | Epic 4 | As a User, I want an automated retrieval accuracy benchmark evaluating Top-1, Top-3, and Top-5 recall across domains. | 5 | Automated 10-query benchmark suite verifies 100% accuracy score. | **DONE** |
| **US-501** | Epic 5 | As a System, I want Cross-Encoder Re-Ranking model integration to optimize top 10 passage selection. | 8 | Cross-Encoder model reranks initial vector recall set. | **PLANNED** |
| **US-502** | Epic 5 | As a System, I want BM25 sparse keyword indexing combined with ChromaDB dense vectors for hybrid search. | 5 | BM25 index integrated with vector similarity search. | **PLANNED** |

---

## 📈 Story Point Scale Reference
- **1 Point**: Trivial tweak (CSS change, label edit)
- **2 Points**: Simple component update or minor bug fix
- **3 Points**: Standard API endpoint or UI view component
- **5 Points**: Core agent implementation, vector indexer, or pipeline algorithm
- **8 Points**: Complex model integration, multi-system orchestration, or major infrastructure change
