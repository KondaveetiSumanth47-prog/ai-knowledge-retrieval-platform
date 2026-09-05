from typing import List, Dict, Any

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

class NativeTextSplitter:
    """Fallback recursive text splitter matching LangChain behavior"""
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50, separators: List[str] = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "; ", ", ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        # Find best separator
        separator = ""
        for s in self.separators:
            if s == "" or s in text:
                separator = s
                break

        splits = text.split(separator) if separator else list(text)
        final_chunks = []
        current_chunk = []
        current_len = 0

        for split in splits:
            item = split + (separator if separator else "")
            if current_len + len(item) > self.chunk_size and current_chunk:
                chunk_str = "".join(current_chunk).strip()
                if chunk_str:
                    final_chunks.append(chunk_str)
                # Overlap logic
                overlap_len = 0
                new_start = []
                for item_prev in reversed(current_chunk):
                    if overlap_len + len(item_prev) <= self.chunk_overlap:
                        new_start.insert(0, item_prev)
                        overlap_len += len(item_prev)
                    else:
                        break
                current_chunk = new_start
                current_len = overlap_len

            current_chunk.append(item)
            current_len += len(item)

        if current_chunk:
            chunk_str = "".join(current_chunk).strip()
            if chunk_str:
                final_chunks.append(chunk_str)

        return final_chunks

class DocumentChunker:
    """
    Splits text into chunks using LangChain RecursiveCharacterTextSplitter (or NativeTextSplitter fallback).
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        if HAS_LANGCHAIN:
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=["\n\n", "\n", ". ", "; ", ", ", " ", ""],
                keep_separator=True
            )
        else:
            self.splitter = NativeTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

    def chunk_text(self, text: str, document_id: str) -> List[Dict[str, Any]]:
        """
        Splits raw text into chunk objects with positional metadata.
        """
        if not text.strip():
            return []
            
        raw_chunks = self.splitter.split_text(text)
        chunk_objects = []
        
        current_pos = 0
        for idx, chunk_str in enumerate(raw_chunks):
            start_pos = text.find(chunk_str, current_pos)
            if start_pos == -1:
                start_pos = current_pos
            end_pos = start_pos + len(chunk_str)
            current_pos = max(start_pos + 1, current_pos)
            
            chunk_objects.append({
                "id": f"{document_id}_chunk_{idx}",
                "document_id": document_id,
                "chunk_index": idx,
                "content": chunk_str,
                "start_char": start_pos,
                "end_char": end_pos,
                "token_estimate": max(1, len(chunk_str) // 4)
            })
            
        return chunk_objects
