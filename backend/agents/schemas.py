from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DocumentSchema(BaseModel):
    id: str
    filename: str
    file_type: str
    domain: str
    file_size: int
    chunk_count: int
    raw_char_count: int
    upload_time: str

class ChunkSchema(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    start_char: int
    end_char: int
    token_estimate: int

class EmbeddingSchema(BaseModel):
    chunk_id: str
    vector: List[float]
    model_name: str

class QuerySchema(BaseModel):
    query_text: str
    domain_filter: Optional[str] = "all"
    session_id: Optional[str] = None
    use_voice: Optional[bool] = False

class RetrievalResultSchema(BaseModel):
    chunk_id: str
    content: str
    document_id: str
    chunk_index: int
    filename: str
    domain: str
    file_type: str
    score: float

class AgentTraceStep(BaseModel):
    agent_name: str
    action: str
    details: Dict[str, Any]
    timestamp: str

class ResponseSchema(BaseModel):
    answer: str
    confidence_score: float
    citations: List[RetrievalResultSchema]
    needs_clarification: bool
    clarification_options: List[str]
    agent_trace: List[AgentTraceStep]
