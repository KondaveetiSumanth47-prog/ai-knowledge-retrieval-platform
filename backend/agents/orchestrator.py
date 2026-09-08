import time
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
    M2.4 — Multi-Agent Orchestration Layer:
    Sequentially coordinates: User Query -> Query Understanding -> Retrieval -> Response Generation -> Final Response.
    Implements robust error handling for classification failures, retrieval failures, empty results, and generation failures.
    """
    def __init__(self, vector_store: VectorStoreManager = None):
        self.query_agent = QueryUnderstandingAgent()
        self.retrieval_agent = RetrievalAgent(vector_store=vector_store)
        self.clarification_agent = ClarificationAgent()
        self.memory_agent = ConversationMemoryAgent()
        self.response_agent = ResponseGenerationAgent()

    def process_query(self, query_text: str, domain_filter: str = "all", session_id: str = None) -> Dict[str, Any]:
        pipeline_start = time.time()
        agent_trace: List[Dict[str, Any]] = []

        def add_trace(agent_name: str, action: str, details: Dict[str, Any], latency_ms: float):
            agent_trace.append({
                "agent_name": agent_name,
                "action": action,
                "details": details,
                "latency_ms": round(latency_ms, 2),
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
            })

        # Step 1: Query Understanding Agent (with Error Handling)
        t0 = time.time()
        try:
            qu_res = self.query_agent.process(query_text, domain_filter=domain_filter)
        except Exception as e:
            qu_res = {
                "original_query": query_text,
                "cleaned_query": query_text.strip(),
                "intent": "Factual",
                "query_type": "factual",
                "classification_confidence": 0.50,
                "resolution_path": "factual_direct",
                "keywords": query_text.split(),
                "is_ambiguous": False,
                "target_domain": domain_filter,
                "error": str(e)
            }
        t1 = time.time()
        add_trace(
            agent_name="1. Query Understanding Agent",
            action=f"Classified query as '{qu_res['intent']}' and assigned path '{qu_res['resolution_path']}'.",
            details={
                "intent": qu_res['intent'],
                "resolution_path": qu_res['resolution_path'],
                "classification_confidence": qu_res.get('classification_confidence', 0.95),
                "is_ambiguous": qu_res['is_ambiguous']
            },
            latency_ms=(t1 - t0) * 1000
        )

        # Step 2: Conversation Memory Agent (with Error Handling)
        t0 = time.time()
        try:
            history = self.memory_agent.get_session_history(session_id) if session_id else []
            formatted_history = self.memory_agent.format_history_context(history)
        except Exception as e:
            history = []
            formatted_history = ""
        t1 = time.time()
        add_trace(
            agent_name="4. Conversation Memory Agent",
            action="Loaded session dialogue history state.",
            details={
                "turns_retrieved": len(history) // 2,
                "has_context": bool(history)
            },
            latency_ms=(t1 - t0) * 1000
        )

        # Step 3: Retrieval Agent (with Error Handling)
        t0 = time.time()
        try:
            retrieval_res = self.retrieval_agent.process(qu_res, top_k=5)
        except Exception as e:
            retrieval_res = {
                "retrieved_chunks": [],
                "total_retrieved": 0,
                "filtered_out_count": 0,
                "top_score": 0.0,
                "sufficient_context": False,
                "error": str(e)
            }
        t1 = time.time()
        add_trace(
            agent_name="2. Retrieval Agent",
            action="Executed vector search, hybrid relevance ranking, and low-confidence filtering.",
            details={
                "total_retrieved": retrieval_res['total_retrieved'],
                "filtered_out_count": retrieval_res['filtered_out_count'],
                "top_score": retrieval_res['top_score'],
                "sufficient_context": retrieval_res['sufficient_context']
            },
            latency_ms=(t1 - t0) * 1000
        )

        # Step 4: Clarification Agent (with Error Handling)
        t0 = time.time()
        try:
            clarification_res = self.clarification_agent.process(qu_res, retrieval_res)
        except Exception as e:
            clarification_res = {
                "needs_clarification": False,
                "clarification_reason": "",
                "clarification_options": []
            }
        t1 = time.time()
        add_trace(
            agent_name="3. Clarification Agent",
            action="Verified response readiness and threshold criteria.",
            details={
                "needs_clarification": clarification_res['needs_clarification'],
                "reason": clarification_res['clarification_reason']
            },
            latency_ms=(t1 - t0) * 1000
        )

        # Step 5: Response Generation Agent (with Error Handling)
        t0 = time.time()
        try:
            resp_res = self.response_agent.process(
                query=query_text,
                retrieved_chunks=retrieval_res['retrieved_chunks'],
                resolution_path=qu_res['resolution_path'],
                conversation_history=formatted_history,
                needs_clarification=clarification_res['needs_clarification'],
                clarification_options=clarification_res['clarification_options']
            )
        except Exception as e:
            resp_res = {
                "answer": f"An error occurred during response generation: {str(e)}",
                "confidence_score": 0.0,
                "confidence_level": "Low",
                "citations": []
            }
        t1 = time.time()
        add_trace(
            agent_name="5. Response Generation Agent",
            action=f"Synthesized grounded answer ({qu_res['resolution_path']}) with citations.",
            details={
                "confidence_score": resp_res['confidence_score'],
                "confidence_level": resp_res['confidence_level'],
                "citations_count": len(resp_res['citations'])
            },
            latency_ms=(t1 - t0) * 1000
        )

        total_latency_ms = round((time.time() - pipeline_start) * 1000, 2)

        return {
            "query": query_text,
            "answer": resp_res['answer'],
            "intent": qu_res['intent'],
            "query_type": qu_res.get('query_type', 'factual'),
            "classification_confidence": qu_res.get('classification_confidence', 0.95),
            "resolution_path": qu_res['resolution_path'],
            "routing_information": qu_res.get('routing_information', {}),
            "confidence_score": resp_res['confidence_score'],
            "confidence_level": resp_res['confidence_level'],
            "citations": resp_res['citations'],
            "needs_clarification": clarification_res['needs_clarification'],
            "clarification_options": clarification_res['clarification_options'],
            "filtered_out_count": retrieval_res['filtered_out_count'],
            "total_latency_ms": total_latency_ms,
            "agent_trace": agent_trace
        }
