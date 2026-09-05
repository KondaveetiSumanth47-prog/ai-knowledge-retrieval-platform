import sqlite3
from typing import List, Dict, Any
from database import get_db

class ConversationMemoryAgent:
    """
    4. Conversation Memory Agent:
    - Stores and retrieves multi-turn dialogue history for session context
    """
    def get_session_history(self, session_id: str, max_turns: int = 5) -> List[Dict[str, Any]]:
        if not session_id:
            return []
            
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender, content, timestamp FROM messages 
            WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?
        """, (session_id, max_turns * 2))
        rows = cursor.fetchall()
        conn.close()
        
        history = [dict(r) for r in reversed(rows)]
        return history

    def format_history_context(self, history: List[Dict[str, Any]]) -> str:
        if not history:
            return "No previous conversation turns."
            
        formatted = []
        for msg in history:
            role = "User" if msg['sender'] == 'user' else "Assistant"
            formatted.append(f"{role}: {msg['content']}")
            
        return "\n".join(formatted)
