import unittest

from clarification_agent import ClarificationAgent
from conversation_memory_agent import ConversationMemoryAgent


class Milestone3Tests(unittest.TestCase):
    def test_clarification_agent_ambiguous_query(self):
        agent = ClarificationAgent()
        result = agent.evaluate_query("Tell me about it.")
        self.assertTrue(result["requires_clarification"])
        self.assertIn("which topic", result["clarification_question"].lower())

    def test_clarification_agent_incomplete_query(self):
        agent = ClarificationAgent()
        result = agent.evaluate_query("Explain the architecture")
        self.assertTrue(result["requires_clarification"])

    def test_clarification_agent_context_dependent_query(self):
        agent = ClarificationAgent()
        result = agent.evaluate_query("How does it work?")
        self.assertTrue(result["requires_clarification"])

    def test_clarification_agent_multi_part_query(self):
        agent = ClarificationAgent()
        result = agent.evaluate_query("Compare RAG and fine-tuning and also explain use cases")
        self.assertTrue(result["requires_clarification"])

    def test_clarification_agent_clear_query(self):
        agent = ClarificationAgent()
        result = agent.evaluate_query("What is RAG?")
        self.assertFalse(result["requires_clarification"])

    def test_conversation_memory_handles_follow_up_context(self):
        memory = ConversationMemoryAgent(session_id="session-1")
        memory.add_exchange(
            "What is RAG?",
            "RAG stands for Retrieval-Augmented Generation.",
            topic="RAG",
            sources=["technology.txt"],
        )

        context = memory.get_relevant_context("How does it work?")
        self.assertIn("RAG", context["topic"])
        self.assertTrue(context["relevant"])

    def test_conversation_memory_handles_topic_switching(self):
        memory = ConversationMemoryAgent(session_id="session-2")
        memory.add_exchange("What is RAG?", "RAG is a retrieval technique.", topic="RAG")
        memory.add_exchange("What is ChromaDB?", "ChromaDB is a vector database.", topic="ChromaDB")

        context = memory.get_relevant_context("Why is it used?")
        self.assertIn("ChromaDB", context["topic"])


if __name__ == "__main__":
    unittest.main()
