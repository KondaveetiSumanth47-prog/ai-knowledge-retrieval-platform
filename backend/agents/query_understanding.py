import re
from typing import Dict, Any

class QueryUnderstandingAgent:
    """
    M2.1 — Query Understanding Agent:
    - Analyzes incoming user query.
    - Classifies query into categories: Factual, Procedural, Comparative, or Ambiguous.
    - Generates structured output containing query_type, classification_confidence, and routing_information.
    - Routes factual, procedural, and comparative queries to appropriate resolution paths.
    - Detects ambiguous queries and marks them for clarification handling.
    """
    def process(self, query_text: str, domain_filter: str = "all") -> Dict[str, Any]:
        cleaned_query = query_text.strip()
        words = cleaned_query.split()
        query_lower = cleaned_query.lower()

        # 1. Ambiguity Detection (M2.1)
        is_ambiguous = False
        ambiguity_reason = ""
        
        if len(words) <= 2 and query_lower not in ['oauth2 token', 'insulin storage', 'triage levels']:
            is_ambiguous = True
            ambiguity_reason = "Query is extremely brief (2 words or less)."
        elif query_lower in ["help", "tell me more", "what should i do", "info", "protocols", "architecture"]:
            is_ambiguous = True
            ambiguity_reason = "Query lacks specific topic context or entity."

        # 2. Classification Taxonomy & Routing Information (M2.1)
        classification_confidence = 0.95
        if is_ambiguous:
            intent = "Ambiguous"
            resolution_path = "ambiguous_clarification"
            classification_confidence = 0.90
        elif any(kw in query_lower for kw in ['how to', 'step', 'procedure', 'process', 'guide', 'instructions', 'protocol', 'trigger', 'reconciliation']):
            intent = "Procedural"
            resolution_path = "procedural_workflow"
            classification_confidence = 0.95
        elif any(kw in query_lower for kw in ['compare', 'difference', 'versus', 'vs', 'better', 'ratio', 'cost versus', 'cost comparison']):
            intent = "Comparative"
            resolution_path = "comparative_matrix"
            classification_confidence = 0.95
        elif any(kw in query_lower for kw in ['what is', 'where', 'when', 'who', 'definition', 'list', 'show', 'cost', 'temperature', 'expiry', 'units', 'sla']):
            intent = "Factual"
            resolution_path = "factual_direct"
            classification_confidence = 0.95
        else:
            intent = "Factual"
            resolution_path = "factual_direct"
            classification_confidence = 0.75

        # 3. Entity & Keyword Extraction
        keywords = re.findall(r'\b[A-Za-z0-9_-]{3,}\b', cleaned_query)
        stop_words = {
            'the', 'and', 'for', 'that', 'this', 'with', 'from', 'what', 'how', 
            'when', 'where', 'which', 'who', 'are', 'tell', 'show', 'give', 'does'
        }
        filtered_keywords = [k for k in keywords if k.lower() not in stop_words]

        return {
            "original_query": query_text,
            "cleaned_query": cleaned_query,
            "intent": intent,
            "query_type": intent.lower(),
            "classification_confidence": classification_confidence,
            "resolution_path": resolution_path,
            "routing_information": {
                "destination_path": resolution_path,
                "requires_clarification": is_ambiguous,
                "extracted_entities": filtered_keywords
            },
            "keywords": filtered_keywords,
            "is_ambiguous": is_ambiguous,
            "ambiguity_reason": ambiguity_reason,
            "target_domain": domain_filter
        }
