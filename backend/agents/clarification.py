from typing import Dict, Any, List

class ClarificationAgent:
    """
    3. Clarification Agent:
    - Evaluates if query or retrieval confidence is ambiguous or insufficient
    - Generates dynamic follow-up questions / options for the user
    """
    def process(self, query_understanding: Dict[str, Any], retrieval_results: Dict[str, Any]) -> Dict[str, Any]:
        needs_clarification = False
        options: List[str] = []
        reason = ""

        if query_understanding.get('is_ambiguous'):
            needs_clarification = True
            reason = query_understanding.get('ambiguity_reason', 'Ambiguous query.')
            options = [
                "Could you specify which domain protocol or guidelines you are asking about?",
                "Please provide more context or key terminology regarding your question.",
                "Would you like to search across all uploaded knowledge base documents?"
            ]
        elif not retrieval_results.get('sufficient_context'):
            needs_clarification = True
            reason = "No sufficiently relevant document chunks were found in the knowledge base."
            options = [
                "Please rephrase your question using different key phrases.",
                "Ensure that relevant documents covering this topic have been ingested.",
                "Try selecting 'All Domains' in the domain filter dropdown."
            ]

        return {
            "needs_clarification": needs_clarification,
            "clarification_reason": reason,
            "clarification_options": options
        }
