import re
from collections import deque
from datetime import datetime


class ConversationMemoryAgent:
    def __init__(self, session_id=None, max_history=6):
        self.session_id = session_id or "default-session"
        self.max_history = max_history
        self.memory = deque(maxlen=max_history)

    def _normalize_topic(self, topic):
        if not topic:
            return "general"

        value = str(topic).strip()

        return value if value else "general"

    def _infer_topic_from_text(self, text):
        if not text:
            return "general"

        query = str(text).strip().lower()

        known_topics = [
            "retrieval augmented generation",
            "machine learning",
            "artificial intelligence",
            "large language model",
            "query understanding",
            "conversation memory",
            "knowledge retrieval",
            "vector database",
            "vector store",
            "document ingestion",
            "text-to-speech",
            "speech recognition",
            "web speech api",
            "chromadb",
            "embedding",
            "embeddings",
            "retrieval",
            "rag",
            "llm",
        ]

        for topic in known_topics:
            if topic in query:
                if topic == "rag":
                    return "RAG"

                if topic == "llm":
                    return "LLM"

                return topic.title()

        match = re.search(
            r"what is\s+(.+?)(?:\?|$)",
            query
        )

        if match:
            topic = match.group(1).strip()

            topic = re.sub(
                r"\b(a|an|the)\b",
                "",
                topic
            ).strip()

            return topic.title() if topic else "general"

        match = re.search(
            r"how does\s+(.+?)\s+work(?:\?|$)",
            query
        )

        if match:
            return match.group(1).strip().title()

        return "general"

    def add_exchange(
        self,
        query,
        response,
        topic=None,
        sources=None,
        clarification=None,
        refined_query=None
    ):
        normalized_topic = (
            self._normalize_topic(topic)
            if topic is not None
            else "general"
        )

        if normalized_topic == "general":
            normalized_topic = self._infer_topic_from_text(query)

        entry = {
            "query": query,
            "response": response,
            "topic": self._normalize_topic(normalized_topic),
            "sources": list(sources or []),
            "clarification": clarification,
            "refined_query": refined_query,
            "timestamp": datetime.utcnow().isoformat(
                timespec="seconds"
            ),
        }

        self.memory.append(entry)

        return entry

    def get_recent_context(self, limit=3):
        return list(self.memory)[-limit:]

    def _contains_follow_up_reference(self, query):
        query_lower = (query or "").strip().lower()

        follow_up_patterns = [
            r"\bit\b",
            r"\bthis\b",
            r"\bthat\b",
            r"\bthey\b",
            r"\bthem\b",
            r"\bthose\b",
            r"\bthese\b",
            r"\bearlier\b",
            r"\babove\b",
            r"\bprevious\b",
            r"\bsame\b",
        ]

        for pattern in follow_up_patterns:
            if re.search(pattern, query_lower):
                return True

        follow_up_phrases = [
            "how does it work",
            "how does this work",
            "how does that work",
            "what are its types",
            "what are its type",
            "what is its use",
            "what is it used for",
            "why is it used",
            "explain it",
            "explain this",
            "tell me more",
            "give more details",
            "more details",
            "what about it",
        ]

        return any(
            phrase in query_lower
            for phrase in follow_up_phrases
        )

    def get_relevant_context(self, current_query):
        query_text = (current_query or "").strip().lower()

        context = {
            "relevant": False,
            "topic": "general",
            "summary": "No previous context available.",
            "recent_queries": [],
            "recent_responses": [],
            "supporting_sources": [],
        }

        if not self.memory:
            return context

        recent_entries = list(self.memory)[-3:]

        follow_up = self._contains_follow_up_reference(
            query_text
        )

        relevant = None

        for item in reversed(self.memory):
            item_query = (
                item.get("query") or ""
            ).strip().lower()

            item_topic = self._normalize_topic(
                item.get("topic")
            )

            if not item_query and not item.get("response"):
                continue

            if follow_up and item_topic != "general":
                relevant = item
                break

            if item_topic != "general" and item_topic.lower() in query_text:
                relevant = item
                break

            if (
                item_query
                and len(item_query) > 5
                and item_query in query_text
            ):
                relevant = item
                break

        if relevant is None:
            last_item = self.memory[-1]

            last_topic = self._normalize_topic(
                last_item.get("topic")
            )

            if last_topic != "general" and follow_up:
                relevant = last_item

        if relevant is not None:
            topic = self._normalize_topic(
                relevant.get("topic")
            )

            context = {
                "relevant": True,
                "topic": topic,
                "summary": (
                    relevant.get("response")
                    or relevant.get("query")
                    or "Relevant context found."
                ),
                "recent_queries": [
                    entry.get("query")
                    for entry in recent_entries
                ],
                "recent_responses": [
                    entry.get("response")
                    for entry in recent_entries
                ],
                "supporting_sources": (
                    relevant.get("sources") or []
                ),
            }

        return context

    def build_context_for_query(self, current_query):
        context = self.get_relevant_context(
            current_query
        )

        return {
            "session_id": self.session_id,
            "current_query": current_query,
            "conversation_context": context,
            "history": self.get_recent_context(),
        }