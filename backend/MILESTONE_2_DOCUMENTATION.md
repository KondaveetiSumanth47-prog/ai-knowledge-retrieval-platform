# Milestone 2 Documentation

## Project Title

Development of AI-Based Knowledge Retrieval Platform with Query Resolution System

## Milestone 2: Multi-Agent Query Resolution

### Objective

The objective of Milestone 2 is to implement a multi-agent query resolution system that understands the user's query, retrieves relevant information from the knowledge base, and generates a grounded response.

---

## 1. Query Understanding Agent

The Query Understanding Agent analyzes the user's question and classifies it into one of four categories:

- Factual
- Procedural
- Comparative
- Ambiguous

The agent also determines the routing of the query.

### Routing

- Factual → Retrieval
- Procedural → Retrieval
- Comparative → Retrieval
- Ambiguous → Clarification

### Output

The agent produces:

- Query
- Query type
- Classification confidence
- Routing decision

### File

`backend/query_understanding_agent.py`

---

## 2. Retrieval Agent

The Retrieval Agent performs semantic search on the knowledge base.

### Main Functions

- Converts the query into an embedding
- Searches the ChromaDB vector store
- Retrieves Top-K results
- Filters low-relevance results
- Calculates relevance scores
- Preserves source and chunk metadata
- Handles no-result situations

### Retrieved Information

Each result contains:

- Text
- Source document
- Chunk ID
- Chunk index
- Distance
- Relevance score

### File

`backend/retrieval_agent.py`

---

## 3. Response Generation Agent

The Response Generation Agent generates answers using the retrieved knowledge.

### Main Functions

- Uses retrieved information as context
- Generates grounded answers using Groq LLM
- Prevents unsupported information from being added
- Provides source attribution
- Provides confidence information
- Handles insufficient information

### LLM

Groq API with a supported LLM model.

The API key is stored securely in the `.env` file and is not included in the source code.

### File

`backend/response_generation_agent.py`

---

## 4. Multi-Agent Orchestration

The complete query processing flow is:

User Query
→ Query Understanding Agent
→ Retrieval Agent
→ Response Generation Agent
→ Final Answer

The agents communicate using structured data.

### Orchestration Flow

1. User submits a question.
2. Query Understanding Agent classifies the question.
3. The query is routed according to its classification.
4. Retrieval Agent searches the knowledge base.
5. Relevant chunks are selected.
6. Response Generation Agent receives the query and retrieved information.
7. The LLM generates a grounded answer.
8. The system returns the answer, sources, confidence, and status.

---

## 5. Testing

The following query categories were tested.

### Factual Query

Example:

"What is Machine Learning?"

Result:

- Query type: Factual
- Routing: Retrieval
- Status: Success

### Procedural Query

Example:

"How does RAG work?"

Result:

- Query type: Procedural
- Routing: Retrieval
- Status: Success

### Comparative Query

Example:

"What is the difference between AI and Machine Learning?"

Result:

- Query type: Comparative
- Routing: Retrieval
- Status: Success

### Information-Unavailable Query

Example:

"What is quantum computing?"

Result:

- No relevant information retrieved
- System does not invent an answer
- Appropriate insufficient-information response generated

### Ambiguous Query

Example:

"Tell me about it"

Result:

- Query type: Ambiguous
- Routing: Clarification

---

## 6. M2 Components

| Component | Status |
|---|---|
| Query Understanding Agent | Completed |
| Retrieval Agent | Completed |
| Response Generation Agent | Completed |
| Multi-Agent Orchestration | Completed |
| Groq LLM Integration | Completed |
| Source Attribution | Completed |
| Confidence Indicator | Completed |
| No-Result Handling | Completed |
| Query Classification Testing | Passed |
| End-to-End Testing | Passed |

---

## 7. Milestone 2 Conclusion

Milestone 2 successfully implements the multi-agent query resolution pipeline.

The system can classify user queries, retrieve relevant information from the knowledge base, generate grounded answers using the LLM, provide source information and confidence, and handle unavailable or ambiguous queries appropriately.

The implementation is ready for the next milestone.