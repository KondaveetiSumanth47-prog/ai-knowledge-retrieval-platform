from datetime import datetime
from typing import Dict, Any, List

from agents.query_understanding import QueryUnderstandingAgent
from agents.retrieval import RetrievalAgent
from agents.clarification import ClarificationAgent
from agents.memory import ConversationMemoryAgent
from agents.response_generator import ResponseGenerationAgent
from ingestion.vector_store import VectorStoreManager

class MultiAgentOrchestrator:
    """
    Multi-Agent Orchestrator:
    Routes incoming user query through the 5 specialized sub-agents:
    1. Query Understanding Agent -> Intent & Ambiguity Detection
    2. Conversation Memory Agent -> Context Retrieval
    3. Retrieval Agent -> ChromaDB Vector Similarity Search & Re-ranking
    4. Clarification Agent -> Threshold & Option Verification
    5. Response Generation Agent -> Groq / Grounded Synthesis & Citations
    """
    def __init__(self, vector_store: VectorStoreManager = None):
        self.query_agent = QueryUnderstandingAgent()
        self.retrieval_agent = RetrievalAgent(vector_store=vector_store)
        self.clarification_agent = ClarificationAgent()
        self.memory_agent = ConversationMemoryAgent()
        self.response_agent = ResponseGenerationAgent()

    def process_query(self, query_text: str, domain_filter: str = "all", session_id: str = None) -> Dict[str, Any]:
        agent_trace: List[Dict[str, Any]] = []

        def add_trace(agent_name: str, action: str, details: Dict[str, Any]):
            agent_trace.append({
                "agent_name": agent_name,
                "action": action,
                "details": details,
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
            })

        # Step 1: Query Understanding Agent
        qu_res = self.query_agent.process(query_text, domain_filter=domain_filter)
        add_trace(
            agent_name="1. Query Understanding Agent",
            action="Analyzed query intent, extracted keywords & checked ambiguity.",
            details={
                "intent": qu_res['intent'],
                "keywords": qu_res['keywords'],
                "is_ambiguous": qu_res['is_ambiguous'],
                "target_domain": qu_res['target_domain']
            }
        )

        # Step 2: Conversation Memory Agent
        history = self.memory_agent.get_session_history(session_id) if session_id else []
        formatted_history = self.memory_agent.format_history_context(history)
        add_trace(
            agent_name="4. Conversation Memory Agent",
            action="Fetched session dialogue history.",
            details={
                "turns_retrieved": len(history) // 2,
                "has_context": bool(history)
            }
        )

        # Step 3: Retrieval Agent
        retrieval_res = self.retrieval_agent.process(qu_res, top_k=5)
        add_trace(
            agent_name="2. Retrieval Agent",
            action="Executed semantic vector search and re-ranking in ChromaDB.",
            details={
                "total_retrieved": retrieval_res['total_retrieved'],
                "top_similarity_score": retrieval_res['top_score'],
                "sufficient_context": retrieval_res['sufficient_context']
            }
        )

        # Step 4: Clarification Agent
        clarification_res = self.clarification_agent.process(qu_res, retrieval_res)
        add_trace(
            agent_name="3. Clarification Agent",
            action="Evaluated response readiness and clarification criteria.",
            details={
                "needs_clarification": clarification_res['needs_clarification'],
                "reason": clarification_res['clarification_reason']
            }
        )

        # Step 5: Response Generation Agent
        resp_res = self.response_agent.process(
            query=query_text,
            retrieved_chunks=retrieval_res['retrieved_chunks'],
            conversation_history=formatted_history,
            needs_clarification=clarification_res['needs_clarification'],
            clarification_options=clarification_res['clarification_options']
        )
        add_trace(
            agent_name="5. Response Generation Agent",
            action="Synthesized grounded answer with citations and confidence score.",
            details={
                "confidence_score": resp_res['confidence_score'],
                "citations_count": len(resp_res['citations'])
            }
        )

        return {
            "query": query_text,
            "answer": resp_res['answer'],
            "confidence_score": resp_res['confidence_score'],
            "citations": resp_res['citations'],
            "needs_clarification": clarification_res['needs_clarification'],
            "clarification_options": clarification_res['clarification_options'],
            "agent_trace": agent_trace
        }
