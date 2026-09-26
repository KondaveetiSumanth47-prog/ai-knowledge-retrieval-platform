# System Architecture

## 1. Overall Flow

User
↓
React Frontend
↓
Flask API
↓
Document Upload
↓
Document Processing
↓
Cleaning / Chunking
↓
Embedding Generation
↓
ChromaDB
↓
Semantic Retrieval

This is the operational architecture for the implemented Milestone 1 system.

---

## 2. Query Flow

User Question
↓
Query Understanding Agent
↓
Multi-Agent Orchestrator
↓
Retrieval Agent
↓
Response Generation Agent
↓
Answer + Citation + Confidence

The current project implements the retrieval layer and supports the question-answer workflow through semantic retrieval. The multi-agent orchestration and final answer generation are planned for later milestones.

---

## 3. Main Components

### Frontend
The frontend is a React dashboard that allows users to:
- upload a document
- view the knowledge base
- ask a question
- receive retrieved relevant chunks

Technology: React + Vite

### Flask API
The backend provides the main API endpoints:
- /upload
- /ask
- /

The API interacts with the document reader, chunking logic, embeddings, and vector store.

### Document Processing Layer
This layer handles:
- extraction from PDF, DOCX, TXT, and CSV files
- cleaning and normalization of text
- chunk splitting using fixed-size chunking with overlap

### Embedding Layer
The embedding generation layer converts text into semantic vectors using Sentence Transformers.

### Vector Store Layer
ChromaDB stores:
- chunk text
- metadata
- embeddings

This supports semantic similarity search over the knowledge base.

### Retrieval Layer
The retrieval layer searches the vector database and returns the top relevant chunks for a user query.

This is the most mature implementation in Milestone 1.

---

## 4. Agent Responsibilities

| Agent | Responsibility | Milestone Status |
| --- | --- | --- |
| Query Understanding Agent | Understands the user’s intent and identifies important concepts in the question | Designed for Milestone 1; implementation planned for later |
| Retrieval Agent | Finds relevant chunks from the knowledge base using vector similarity | Basic retrieval functionality already exists in Milestone 1 |
| Response Generation Agent | Produces the final natural-language answer using retrieved context | Planned for Milestone 2 |
| Clarification Agent | Asks follow-up questions when the query is unclear | Planned for Milestone 2 |
| Conversation Memory Agent | Maintains conversational continuity and context | Planned for Milestone 2 |

---

## 5. Orchestration Flow

The conceptual orchestration is:

1. User submits a question
2. Query Understanding Agent interprets intent
3. Multi-Agent Orchestrator selects the next action
4. Retrieval Agent searches the vector store
5. Relevant chunks are ranked and returned
6. Response Generation Agent processes the final answer when implemented
7. Clarification Agent may ask a follow-up if required
8. Conversation Memory Agent stores short-term context

In the current project, Step 4 is the part that is active and verified.

---

## 6. Conceptual Data Models

### Document
- document_id
- filename
- file_type
- upload_time
- status

### Chunk
- chunk_id
- document_id
- chunk_index
- text
- metadata

### Embedding
- embedding_id
- chunk_id
- vector

### Query
- query_id
- question
- timestamp

### Retrieval Result
- chunk_id
- text
- source
- similarity/relevance information if available

### Response
- answer
- source
- confidence
- timestamp

These are conceptual models for the architecture. They are not new database tables added to the backend schema unless they already exist as part of the current implementation.

---

## 7. File-Level Architecture Mapping

- [backend/app.py](backend/app.py): Flask API endpoints
- [backend/document_reader.py](backend/document_reader.py): file extraction logic
- [backend/chunking.py](backend/chunking.py): fixed-size chunking
- [backend/embeddings.py](backend/embeddings.py): Sentence Transformer embedding generation
- [backend/vector_store.py](backend/vector_store.py): ChromaDB storage and queries
- [backend/rag_pipeline.py](backend/rag_pipeline.py): retrieval processing
- [frontend/src/App.jsx](frontend/src/App.jsx): user dashboard and request handling

---

## 8. Design Principles
- keep the system simple and educational
- support multiple document types
- preserve source metadata for traceability
- focus on retrieval accuracy before answer generation
- keep the backend stable and working while documenting the architecture

---

## 9. Milestone 1 Reality Check
Milestone 1 is a retrieval-focused foundation, not a full autonomous multi-agent system. The architecture is designed for future AI agents, but the implemented product is currently a working document retrieval system with semantic search at its core.
