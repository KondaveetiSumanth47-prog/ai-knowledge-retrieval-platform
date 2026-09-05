import sqlite3
import json
from datetime import datetime
from config import SQLITE_DB_PATH

def get_db():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            domain TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            chunk_count INTEGER DEFAULT 0,
            raw_char_count INTEGER DEFAULT 0,
            upload_time TEXT NOT NULL,
            filepath TEXT NOT NULL
        );
    """)
    
    # Chunks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            document_id TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            start_char INTEGER DEFAULT 0,
            end_char INTEGER DEFAULT 0,
            token_estimate INTEGER DEFAULT 0,
            FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
        );
    """)
    
    # Conversation Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT DEFAULT 'New Conversation',
            created_at TEXT NOT NULL
        );
    """)
    
    # Conversation Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            agent_trace TEXT,
            citations TEXT,
            confidence_score REAL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        );
    """)
    
    # Evaluation Logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eval_logs (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            total_queries INTEGER NOT NULL,
            top_1_accuracy REAL NOT NULL,
            top_3_accuracy REAL NOT NULL,
            top_5_accuracy REAL NOT NULL,
            detailed_results TEXT NOT NULL
        );
    """)
    
    conn.commit()
    conn.close()

def save_document(doc_data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO documents (id, filename, file_type, domain, file_size, chunk_count, raw_char_count, upload_time, filepath)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        doc_data['id'],
        doc_data['filename'],
        doc_data['file_type'],
        doc_data['domain'],
        doc_data['file_size'],
        doc_data['chunk_count'],
        doc_data['raw_char_count'],
        doc_data['upload_time'],
        doc_data['filepath']
    ))
    conn.commit()
    conn.close()

def save_chunks(chunks_list):
    conn = get_db()
    cursor = conn.cursor()
    for chunk in chunks_list:
        cursor.execute("""
            INSERT INTO chunks (id, document_id, chunk_index, content, start_char, end_char, token_estimate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            chunk['id'],
            chunk['document_id'],
            chunk['chunk_index'],
            chunk['content'],
            chunk.get('start_char', 0),
            chunk.get('end_char', 0),
            chunk.get('token_estimate', len(chunk['content']) // 4)
        ))
    conn.commit()
    conn.close()

def get_all_documents():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents ORDER BY upload_time DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_document_by_id(doc_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_chunks_for_document(doc_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_index ASC", (doc_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_document(doc_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chunks WHERE document_id = ?", (doc_id,))
    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()

def save_eval_run(eval_data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO eval_logs (id, timestamp, total_queries, top_1_accuracy, top_3_accuracy, top_5_accuracy, detailed_results)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        eval_data['id'],
        eval_data['timestamp'],
        eval_data['total_queries'],
        eval_data['top_1_accuracy'],
        eval_data['top_3_accuracy'],
        eval_data['top_5_accuracy'],
        json.dumps(eval_data['detailed_results'])
    ))
    conn.commit()
    conn.close()

def get_latest_eval_logs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eval_logs ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d['detailed_results'] = json.loads(d['detailed_results'])
        results.append(d)
    return results

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
