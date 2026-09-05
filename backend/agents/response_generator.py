import os
from typing import List, Dict, Any
from config import GROQ_API_KEY, GROQ_MODEL

class ResponseGenerationAgent:
    """
    3. Response Generation Agent (Milestone 2):
    - Synthesizes grounded answers tailored to resolution paths:
      * factual_direct
      * procedural_workflow
      * comparative_matrix
      * ambiguous_clarification
    - Computes dynamic confidence score & indicator badge (High, Medium, Low).
    - Enforces source attribution citations.
    """
    def __init__(self):
        self.groq_client = None
        if GROQ_API_KEY:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=GROQ_API_KEY)
            except Exception as e:
                print(f"Notice: Groq client init: {e}")

    def process(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        resolution_path: str = "factual_direct",
        conversation_history: str = "",
        needs_clarification: bool = False,
        clarification_options: List[str] = None
    ) -> Dict[str, Any]:

        if needs_clarification:
            opts_str = "\n".join([f"• {opt}" for opt in (clarification_options or [])])
            answer = f"### ❓ Clarification Needed\nI need additional context to resolve your request accurately:\n\n{opts_str}"
            return {
                "answer": answer,
                "confidence_score": 0.20,
                "confidence_level": "Low",
                "citations": []
            }

        if not retrieved_chunks:
            answer = "I'm sorry, but no relevant document chunks meeting the confidence threshold were found in the ingested knowledge base."
            return {
                "answer": answer,
                "confidence_score": 0.10,
                "confidence_level": "Low",
                "citations": []
            }

        # Format context passages
        context_passages = []
        citations = []
        for idx, chunk in enumerate(retrieved_chunks[:5]):
            citation_label = f"[{idx + 1}] Source File: {chunk['filename']} (Domain: {chunk['domain']})"
            context_passages.append(f"{citation_label}\n{chunk['content']}")
            citations.append(chunk)

        context_str = "\n\n".join(context_passages)

        answer = None
        if self.groq_client:
            try:
                path_instructions = {
                    "factual_direct": "Provide a clear, concise factual answer directly addressing the question.",
                    "procedural_workflow": "Structure the answer as a step-by-step numbered workflow with clear headers.",
                    "comparative_matrix": "Structure the answer as a clear comparative matrix/bullet comparison comparing the key elements."
                }.get(resolution_path, "Provide a clear factual answer.")

                system_prompt = (
                    f"You are an expert AI Knowledge Retrieval Assistant. {path_instructions}\n"
                    "Base your answer strictly on the provided context passages.\n"
                    "Cite sources using [Source: filename] corresponding to the passages."
                )
                user_prompt = f"Context Passages:\n{context_str}\n\nUser Question: {query}"
                
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=GROQ_MODEL,
                    temperature=0.2,
                    max_tokens=700,
                )
                answer = chat_completion.choices[0].message.content.strip()
            except Exception as e:
                print(f"Groq API call fallback: {e}")

        # Path-tailored grounded fallback if Groq API is not set
        if not answer:
            answer = self._synthesize_path_tailored_response(query, retrieved_chunks, resolution_path)

        # Dynamic Confidence Score Calculation
        top_score = retrieved_chunks[0]['score'] if retrieved_chunks else 0.0
        avg_top3 = (sum(c['score'] for c in retrieved_chunks[:3]) / min(3, len(retrieved_chunks))) if retrieved_chunks else 0.0
        
        confidence = round(min(0.98, max(0.20, (top_score * 0.60) + (avg_top3 * 0.40))), 2)

        if confidence >= 0.75:
            confidence_level = "High"
        elif confidence >= 0.45:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"

        return {
            "answer": answer,
            "confidence_score": confidence,
            "confidence_level": confidence_level,
            "citations": citations
        }

    def _synthesize_path_tailored_response(self, query: str, chunks: List[Dict[str, Any]], path: str) -> str:
        top_chunk = chunks[0]
        
        if path == "procedural_workflow":
            header = f"### 📋 Procedural Workflow Guide (Source: {top_chunk['filename']})\n"
            steps = []
            for idx, c in enumerate(chunks[:3]):
                steps.append(f"**Step {idx + 1}**: Source `{c['filename']}`\n\"{c['content'].strip()}\"")
            return header + "\n\n".join(steps)

        elif path == "comparative_matrix":
            header = f"### 📊 Comparative Analysis Matrix (Source: {top_chunk['filename']})\n"
            items = []
            for idx, c in enumerate(chunks[:4]):
                items.append(f"• **[{c['filename']} - {c['domain']}]**:\n  \"{c['content'].strip()}\"")
            return header + "\n\n".join(items)

        else:  # factual_direct
            header = f"### 💡 Grounded Direct Answer (Source: {top_chunk['filename']})\n"
            snippets = []
            for c in chunks[:3]:
                snippets.append(f"• **[{c['filename']}]**: \"{c['content'].strip()}\"")
            return header + "\n\n".join(snippets)
