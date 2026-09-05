import re
from typing import Dict, Any

class QueryUnderstandingAgent:
    """
    1. Query Understanding Agent:
    - Parses user intent (Factual, Procedural, Comparative, Clarification, Unknown)
    - Extracts key entities and technical domain terms
    - Checks for ambiguity or extreme brevity
    """
    def process(self, query_text: str, domain_filter: str = "all") -> Dict[str, Any]:
        cleaned_query = query_text.strip()
        words = cleaned_query.split()
        
        # Determine query category
        query_lower = cleaned_query.lower()
        if any(kw in query_lower for kw in ['how to', 'step', 'procedure', 'process', 'guide', 'instructions']):
            intent = "Procedural"
        elif any(kw in query_lower for kw in ['compare', 'difference', 'versus', 'vs', 'better', 'ratio']):
            intent = "Comparative"
        elif any(kw in query_lower for kw in ['what is', 'where', 'when', 'who', 'definition', 'list', 'show', 'cost', 'protocol']):
            intent = "Factual"
        else:
            intent = "General Inquiry"
            
        # Ambiguity check
        is_ambiguous = False
        ambiguity_reason = ""
        if len(words) <= 2:
            is_ambiguous = True
            ambiguity_reason = "Query is extremely brief and underspecified."
        elif query_lower in ["help", "tell me more", "what should i do", "info"]:
            is_ambiguous = True
            ambiguity_reason = "Query lacks specific topic context."

        # Extract entities / keywords
        keywords = re.findall(r'\b[A-Za-z0-9_-]{3,}\b', cleaned_query)
        stop_words = {'the', 'and', 'for', 'that', 'this', 'with', 'from', 'what', 'how', 'when', 'where', 'which', 'who', 'are'}
        filtered_keywords = [k for k in keywords if k.lower() not in stop_words]

        return {
            "original_query": query_text,
            "cleaned_query": cleaned_query,
            "intent": intent,
            "keywords": filtered_keywords,
            "is_ambiguous": is_ambiguous,
            "ambiguity_reason": ambiguity_reason,
            "target_domain": domain_filter
        }
