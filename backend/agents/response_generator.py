import os
from typing import List, Dict, Any
from config import GROQ_API_KEY, GROQ_MODEL

class ResponseGenerationAgent:
    """
    5. Response Generation Agent:
    - Generates grounded, cited answers using Groq LLM (Llama 3)
    - Fallback template synthesis when API key is unsupplied
    - Computes overall response confidence score
    """
    def __init__(self):
        self.groq_client = None
        if GROQ_API_KEY:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=GROQ_API_KEY)
            except Exception as e:
                print(f"Warning: Could not initialize Groq client: {e}")

    def process(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        conversation_history: str = "",
        needs_clarification: bool = False,
        clarification_options: List[str] = None
    ) -> Dict[str, Any]:

        if needs_clarification:
            opts_str = "\n".join([f"- {opt}" for opt in (clarification_options or [])])
            answer = f"I need a bit more clarification to give you an exact answer:\n\n{opts_str}"
            return {
                "answer": answer,
                "confidence_score": 0.20,
                "citations": []
            }

        if not retrieved_chunks:
            answer = "I'm sorry, but I couldn't find any relevant information in the uploaded knowledge base to answer your query accurately."
            return {
                "answer": answer,
                "confidence_score": 0.10,
                "citations": []
            }

        # Build context from chunks
        context_passages = []
        citations = []
        for idx, chunk in enumerate(retrieved_chunks[:5]):
            citation_label = f"[{idx + 1}] Source: {chunk['filename']} (Domain: {chunk['domain']})"
            context_passages.append(f"{citation_label}\n{chunk['content']}")
            citations.append(chunk)

        context_str = "\n\n".join(context_passages)

        # Attempt Groq API generation
        answer = None
        if self.groq_client:
            try:
                system_prompt = (
                    "You are an expert AI Knowledge Retrieval Assistant. "
                    "Answer the user's question accurately based strictly on the provided context passages. "
                    "Cite sources using [Source: filename] or [1], [2] corresponding to the passages. "
                    "If the answer is not contained in the passages, state clearly that the information is unavailable."
                )
                user_prompt = f"Context Passages:\n{context_str}\n\nUser Question: {query}"
                
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=GROQ_MODEL,
                    temperature=0.2,
                    max_tokens=600,
                )
                answer = chat_completion.choices[0].message.content.strip()
            except Exception as e:
                print(f"Groq API call failed: {e}. Falling back to grounded context synthesizer.")

        # Grounded Fallback Synthesizer if Groq API is omitted or failed
        if not answer:
            answer = self._synthesize_grounded_response(query, retrieved_chunks)

        # Calculate confidence score based on top retrieval vector similarity and context length
        top_score = retrieved_chunks[0]['score'] if retrieved_chunks else 0.0
        confidence = round(min(0.98, max(0.25, top_score * 0.95 + 0.10)), 2)

        return {
            "answer": answer,
            "confidence_score": confidence,
            "citations": citations
        }

    def _synthesize_grounded_response(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        """Grounded fallback response generator using extracted passage snippets"""
        top_chunk = chunks[0]
        response_parts = [
            f"Based on **{top_chunk['filename']}** ({top_chunk['domain']}), here is the relevant information regarding your query:\n"
        ]
        
        for idx, c in enumerate(chunks[:3]):
            content_snippet = c['content'].strip()
            if len(content_snippet) > 300:
                content_snippet = content_snippet[:300] + "..."
            response_parts.append(f"• **[{c['filename']}]**: \"{content_snippet}\"")
            
        return "\n\n".join(response_parts)
