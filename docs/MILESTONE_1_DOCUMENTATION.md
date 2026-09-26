# Milestone 1 Documentation

## Overview
This project is a beginner-friendly AI knowledge retrieval platform. Milestone 1 focuses on building the core retrieval pipeline: upload documents, extract text, split content into chunks, generate embeddings, store them in a vector database, and retrieve relevant information for user queries.

The current implementation is working and validated. It focuses on retrieval, not final answer generation from an LLM. That distinction is important for Milestone 1.

---

## 1. RAG Architecture

### What is RAG?
RAG stands for Retrieval-Augmented Generation. It is a method where a system first searches a knowledge base for relevant information and then uses that information to answer a question.

In simple terms, instead of relying only on the model’s training memory, the system looks up the most relevant facts from stored documents first.

### Why RAG is used in this project
This project is designed for domain-specific knowledge retrieval. The goal is to make the system answer questions based on uploaded documents, not just general knowledge. RAG is useful because:
- it keeps answers tied to source documents
- it works well for local knowledge bases
- it is easier to update than retraining a model
- it supports document-based search and evidence-based retrieval

### End-to-end RAG flow used in this project
User Question
↓
Query Processing
↓
Question Embedding
↓
Vector Search
↓
Relevant Document Chunks
↓
Response Generation

In the current Milestone 1 implementation, the system successfully completes the retrieval path up to relevant chunks. It does not yet implement a final LLM-generated answer in the full sense of a generative response model.

### Current project status
- Designed for RAG: Yes
- Implemented in Milestone 1: Retrieval pipeline and semantic search are implemented
- Final LLM answer generation: Not yet implemented in this milestone

---

## 2. Semantic Similarity
Semantic similarity means comparing the meaning of text rather than only checking whether the same words appear.

Example:
- "What is machine learning?"
- "Explain machine learning in simple words"

These questions are meaningfully similar even though the wording is different.

Why this matters:
- keyword matching misses context
- semantic similarity helps match meaning
- it works better when users ask natural-language questions

This project uses embeddings to compare the meaning of the user query with the meaning of stored text chunks.

---

## 3. Embeddings
An embedding is a numerical representation of text. Instead of storing raw words only, the system turns each chunk into a vector that captures its meaning.

The embedding represents the semantic features of the text in a high-dimensional numerical form. Similar ideas produce embeddings that are close together in vector space.

In this project:
- the question is converted into an embedding
- each document chunk is converted into an embedding
- ChromaDB compares these vectors to find the closest matches

Sentence Transformers are used because they are simple to use for local semantic embedding generation and work well for this project’s retrieval task.

### Embeddings in ChromaDB
The vector database stores:
- chunk text
- chunk metadata
- the numerical embedding for each chunk

When a user asks a question, the system embeds that question and performs similarity search against stored document embeddings.

---

## 4. Chunking
The current chunking strategy uses:
- chunk_size = 500
- chunk_overlap = 50

### Why documents are divided into chunks
Large documents are difficult to retrieve efficiently as one big block. Chunking helps the system:
- find more precise matches
- reduce the amount of irrelevant text retrieved
- maintain manageable search units
- keep source tracking easier for each text fragment

### Why chunk size matters
A chunk that is too large may contain too much unrelated content. A chunk that is too small may lose context and reduce the quality of retrieval. The chosen size is a practical balance for this project.

### Why overlap is used
Overlap helps keep nearby information connected. If a sentence is cut at the boundary between chunks, some meaning may be lost. Overlap reduces this risk but still keeps the chunks small enough for search.

### Advantages and limitations of the current strategy
Advantages:
- easy to understand and implement
- works well with the project size and sample documents
- suitable for simple RAG retrieval testing

Limitations:
- fixed-size chunking is not context-aware
- very large or highly structured documents may not split optimally
- retrieval quality depends on document quality and chunk boundaries

---

## 5. Vector Search
Vector search means searching by meaning, not by exact text match.

In this project, ChromaDB stores embeddings and performs similarity search using those vectors. The process is:
1. user question is embedded
2. stored chunk embeddings are compared
3. the most similar chunks are returned
4. the top results are ranked by similarity

### Top-K retrieval
Top-K means the system returns the K most relevant results. For example:
- Top-1 returns the single best matching chunk
- Top-3 returns the three best matches
- Top-5 returns the five best matches

This is useful for measuring retrieval quality and balancing relevance against noise.

---

## 6. Multi-Agent Query Resolution
The system is designed with future multi-agent query resolution patterns in mind. The following agent roles are planned for architecture, but not all are implemented in Milestone 1.

### 1. Query Understanding Agent
Responsible for understanding the intent behind a question, identifying key concepts, and classifying the query type.

- Designed for the architecture: Yes
- Implemented in Milestone 1: Not fully implemented

### 2. Retrieval Agent
Responsible for fetching the most relevant chunks from the vector database.

- Designed for the architecture: Yes
- Implemented in Milestone 1: Yes, basic retrieval is implemented

### 3. Response Generation Agent
Responsible for producing a final natural-language answer from the retrieved content.

- Designed for the architecture: Yes
- Implemented in Milestone 1: Not yet implemented

### 4. Clarification Agent
Responsible for asking the user follow-up questions when a query is unclear or ambiguous.

- Designed for the architecture: Yes
- Implemented in Milestone 1: Not yet implemented

### 5. Conversation Memory Agent
Responsible for holding short-term or session context across questions.

- Designed for the architecture: Yes
- Implemented in Milestone 1: Not yet implemented

### Important distinction
The multi-agent architecture is conceptually designed for the longer-term system, but Milestone 1 only includes the retrieval foundation and the working document ingestion pipeline.

---

## 7. Web Speech API
The Web Speech API is relevant to the project because it can support voice-based interaction in a browser.

### Speech-to-Text
The browser listens to microphone input and converts speech into text. This would allow users to speak questions instead of typing them.

### Text-to-Speech
The browser converts text into spoken output. This would allow the system to respond with voice instead of only text.

### Planned use in the project
This is a useful future enhancement for accessible and conversational interaction, especially for hands-free use cases.

### Current milestone status
This feature is planned for a later milestone and is not implemented in the current Milestone 1 working system.

---

## 8. Technology Choices

| Technology | Purpose | Reason for Selection |
| --- | --- | --- |
| React.js | Frontend interface | Used for a modern, interactive dashboard and user experience |
| Flask | Backend API | Lightweight and easy to use for /upload and /ask routes |
| Python | Core app logic | Used for document processing, embeddings, and retrieval |
| PyMuPDF | PDF extraction | Reads text from PDF files reliably for this project |
| python-docx | DOCX extraction | Reads text content from Word documents |
| pandas | CSV processing | Converts CSV content into readable text for indexing |
| Sentence Transformers | Embedding generation | Produces semantic vector representations for queries and chunks |
| ChromaDB | Vector database | Stores embeddings and performs similarity-based retrieval |
| SQLite | Optional architecture support | Can be used for lightweight app metadata in future versions |
| Git/GitHub | Version control and project management | Helps track code changes and collaboration |
| Web Speech API | Future speech interaction | Planned for voice input/output in later milestones |

Note: LangChain is not currently used in the implemented Milestone 1 flow and is not required for the working project.

---

## 9. Milestone 1 Scope and Realistic Limitations
The current implementation is a solid retrieval foundation, but it has realistic limitations:
- basic fixed-size chunking is used
- retrieval is implemented, but final LLM answer generation is not yet complete
- multi-agent orchestration is planned but not fully built yet
- voice interaction is still a future feature
- evaluation data is small and sample-based
- retrieval quality depends on document quality and domain coverage
- there is no advanced confidence scoring or citation generation yet

---

## 10. Future Improvements
The project roadmap can evolve with:
- Query Understanding Agent
- Retrieval Agent improvements
- Response Generation Agent
- Clarification Agent
- Conversation Memory
- Groq/Llama integration
- Voice interaction support
- Better chunking strategies
- Confidence scoring
- Citation generation
- Analytics and knowledge-gap detection

---

## 11. Validation Summary
The current Milestone 1 application has been validated through actual runtime testing for:
- PDF upload and retrieval
- DOCX upload and retrieval
- TXT upload and retrieval
- CSV upload and retrieval
- Embedding generation
- ChromaDB indexing and similarity search
- Retrieval accuracy checks across education and technology domains

This milestone is therefore a functioning retrieval system rather than a complete multi-agent answer generation system.

---

## 12. Final Milestone 1 Position
Milestone 1 successfully establishes the foundational retrieval architecture:
- document ingestion
- text extraction
- chunking
- embeddings
- vector search
- source-aware retrieval

What it does not yet include is:
- complete final answer generation by an LLM
- fully implemented multi-agent orchestration
- voice interaction
- advanced confidence and citation logic

This is aligned with the actual project status and should be documented clearly for mentor review.
