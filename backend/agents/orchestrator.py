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
    4. Multi-Agent Orchestration Layer (Milestone 2):
    Coordinates Query Understanding -> Retrieval -> Clarification -> Memory -> Response Generation sequentially per query.
    Tracks latency telemetry and outputs structured trace streams.
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

        # Step 1: Query Understanding Agent
        t0 = time.time()
        qu_res = self.query_agent.process(query_text, domain_filter=domain_filter)
        t1 = time.time()
        add_trace(
            agent_name="1. Query Understanding Agent",
            action=f"Classified query as '{qu_res['intent']}' and assigned resolution path '{qu_res['resolution_path']}'.",
            details={
                "intent": qu_res['intent'],
                "resolution_path": qu_res['resolution_path'],
                "keywords": qu_res['keywords'],
                "is_ambiguous": qu_res['is_ambiguous']
            },
            latency_ms=(t1 - t0) * 1000
        )

        # Step 2: Conversation Memory Agent
        t0 = time.time()
        history = self.memory_agent.get_session_history(session_id) if session_id else []
        formatted_history = self.memory_agent.format_history_context(history)
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

        # Step 3: Retrieval Agent
        t0 = time.time()
        retrieval_res = self.retrieval_agent.process(qu_res, top_k=5)
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

        # Step 4: Clarification Agent
        t0 = time.time()
        clarification_res = self.clarification_agent.process(qu_res, retrieval_res)
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

        # Step 5: Response Generation Agent
        t0 = time.time()
        resp_res = self.response_agent.process(
            query=query_text,
            retrieved_chunks=retrieval_res['retrieved_chunks'],
            resolution_path=qu_res['resolution_path'],
            conversation_history=formatted_history,
            needs_clarification=clarification_res['needs_clarification'],
            clarification_options=clarification_res['clarification_options']
        )
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
            "resolution_path": qu_res['resolution_path'],
            "confidence_score": resp_res['confidence_score'],
            "confidence_level": resp_res['confidence_level'],
            "citations": resp_res['citations'],
            "needs_clarification": clarification_res['needs_clarification'],
            "clarification_options": clarification_res['clarification_options'],
            "filtered_out_count": retrieval_res['filtered_out_count'],
            "total_latency_ms": total_latency_ms,
            "agent_trace": agent_trace
        }
