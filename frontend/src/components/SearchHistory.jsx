function SearchHistory({ searches, onSelect }) {
  const safeSearches = Array.isArray(searches) ? searches : [];

  return (
    <div className="page-card history-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Recent activity</p>
          <h2>Recent Searches</h2>
        </div>
      </div>

      {safeSearches.length === 0 ? (
        <div className="empty-state small-empty">
          <div className="empty-icon">🕘</div>
          <p>No recent searches yet.</p>
        </div>
      ) : (
        <div className="history-list">
          {safeSearches.map((entry, index) => {
            const question = typeof entry === 'string' ? entry : entry.question;
            const date = typeof entry === 'string' ? new Date().toISOString() : entry.date;
            const results = typeof entry === 'string' ? 0 : entry.results ?? 0;
            const status = typeof entry === 'string' ? 'Recent' : entry.status || 'Recent';

            return (
              <button
                type="button"
                key={`${question}-${index}`}
                className="history-item"
                onClick={() => onSelect(question)}
              >
                <div className="history-top-row">
                  <span className="history-dot" aria-hidden="true">•</span>
                  <span className="history-question">{question}</span>
                </div>
                <div className="history-meta-row">
                  <span>{new Date(date).toLocaleString()}</span>
                  <span className="history-status">{status}</span>
                  <span>{results} results</span>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default SearchHistory;
