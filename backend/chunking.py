def split_text(text, chunk_size=500, chunk_overlap=50):
    if not isinstance(text, str):
        text = str(text or "")

    cleaned_text = text.strip()
    if not cleaned_text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size - 1)

    chunks = []
    start = 0

    while start < len(cleaned_text):
        end = min(start + chunk_size, len(cleaned_text))
        chunk = cleaned_text[start:end]
        if chunk.strip():
            chunks.append(chunk)

        if end == len(cleaned_text):
            break

        start = max(start + 1, end - chunk_overlap)

    return chunks