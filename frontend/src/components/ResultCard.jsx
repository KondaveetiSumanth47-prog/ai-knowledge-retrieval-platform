function ResultCard({ result, index }) {
  const source = result?.source || 'Unknown source';
  const chunkText = result?.chunk_index ?? null;

  return (
    <article className="result-card">
      <div className="result-header">
        <div className="result-badge">Result {index + 1}</div>
      </div>

      <p className="result-text">{result?.text || 'No content available.'}</p>

      <div className="result-meta">
        <span className="meta-icon" aria-hidden="true">📄</span>
        <span>Source: {source}</span>
        {chunkText !== null && chunkText !== undefined ? (
          <span className="chunk-label">Chunk: {chunkText}</span>
        ) : null}
      </div>
    </article>
  );
}

export default ResultCard;
