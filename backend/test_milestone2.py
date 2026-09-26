import os
import unittest

from query_understanding_agent import QueryUnderstandingAgent
from retrieval_agent import RetrievalAgent
from response_generation_agent import ResponseGenerationAgent


class Milestone2Tests(unittest.TestCase):
    def test_query_understanding_classification(self):
        agent = QueryUnderstandingAgent()

        expected = {
            "What is RAG?": "factual",
            "How does RAG work?": "procedural",
            "What is the difference between AI and Machine Learning?": "comparative",
            "Tell me about it": "ambiguous",
        }

        for question, expected_type in expected.items():
            result = agent.classify_query(question)
            self.assertEqual(result["query_type"], expected_type)
            self.assertIn("routing", result)
            self.assertGreaterEqual(result["classification_confidence"], 0.0)

    def test_retrieval_agent_result_quality(self):
        agent = RetrievalAgent(top_k=3, distance_threshold=0.60)

        cases = [
            ("What is RAG?", "factual"),
            ("How does RAG work?", "procedural"),
            ("What is the difference between AI and Machine Learning?", "comparative"),
            ("What is quantum computing?", "factual"),
        ]

        for query, query_type in cases:
            result = agent.retrieve(query, {"query_type": query_type})
            self.assertIn("results", result)
            self.assertIn("status", result)
            self.assertIn("query_type", result)

            for item in result["results"]:
                self.assertIn("text", item)
                self.assertIn("source", item)
                self.assertIn("distance", item)
                self.assertIn("relevance_score", item)

            if query == "What is quantum computing?":
                self.assertEqual(result["status"], "no_relevant_information")

    def test_response_generation_agent_handles_auth_failure(self):
        original = os.environ.get("GROQ_API_KEY")
        os.environ["GROQ_API_KEY"] = "invalid-key"

        try:
            agent = ResponseGenerationAgent()
            response = agent.generate_response(
                "What is RAG?",
                [{"text": "RAG is retrieval augmented generation.", "source": "sample.txt", "relevance_score": 0.8}],
                "factual",
            )
            self.assertEqual(response["status"], "llm_authentication_failed")
            self.assertIn("GROQ_API_KEY", response["answer"])
        finally:
            if original is None:
                os.environ.pop("GROQ_API_KEY", None)
            else:
                os.environ["GROQ_API_KEY"] = original


if __name__ == "__main__":
    unittest.main()
