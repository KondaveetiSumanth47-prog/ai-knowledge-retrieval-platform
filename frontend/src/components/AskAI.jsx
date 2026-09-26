import { useMemo, useState } from 'react';

function AskAI({
  question,
  setQuestion,
  onAsk,
  loading,
  results,
  isEmptyState,
  errorMessage,
  emptyMessage,
  answerDetails,
  clarificationState,
  selectedTopK,
  setSelectedTopK,
  voiceState,
  onVoiceStart,
  onVoiceStop,
  onSpeakAnswer,
  onPauseSpeech,
  onResumeSpeech,
  onStopSpeech,
}) {
  const answer = answerDetails?.answer || '';
  const queryType = answerDetails?.queryType || '';
  const classificationConfidence =
    answerDetails?.classificationConfidence ?? null;

  const sources = Array.isArray(answerDetails?.sources)
    ? answerDetails.sources
    : [];

  const confidence =
    answerDetails?.confidence || {
      label: 'Low',
      score: 0,
    };

  const status = answerDetails?.status || '';
  const hints =
    answerDetails?.conversationContext || null;

  const responseTopK =
    [1, 3, 5].includes(Number(selectedTopK))
      ? Number(selectedTopK)
      : 3;

  const [showEvidence, setShowEvidence] =
    useState(false);

  const evidenceItems = useMemo(() => {
    if (
      Array.isArray(
        answerDetails?.retrievedChunks
      ) &&
      answerDetails.retrievedChunks.length > 0
    ) {
      return answerDetails.retrievedChunks;
    }

    return Array.isArray(results) ? results : [];
  }, [answerDetails, results]);

  const lowConfidence =
    confidence?.label?.toLowerCase() === 'low';

  const hasClarification = Boolean(
    clarificationState?.pending &&
      clarificationState.question
  );

  const handleTopKChange = (value) => {
    const normalizedValue = Number(value);

    if ([1, 3, 5].includes(normalizedValue)) {
      setSelectedTopK(normalizedValue);
    }
  };

  return (
    <div
      className="page-card ask-card"
      id="ask-ai"
    >
      <p className="section-subtitle">
        Ask questions based on your uploaded
        knowledge.
      </p>

      <div className="ask-box">
        <input
          type="text"
          className="question-input"
          value={question}
          placeholder={
            hasClarification
              ? 'Type the missing information...'
              : 'Ask something about your documents...'
          }
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              onAsk();
            }
          }}
        />
      </div>

      <div
        className="retrieval-selector"
        aria-label="Retrieval results selector"
      >
        <span className="retrieval-label">
          Retrieval Results:
        </span>

        {[1, 3, 5].map((option) => (
          <button
            key={option}
            type="button"
            className={`topk-button ${
              Number(selectedTopK) === option
                ? 'selected'
                : ''
            }`}
            onClick={() =>
              handleTopKChange(option)
            }
            aria-pressed={
              Number(selectedTopK) === option
            }
          >
            Top-{option}
          </button>
        ))}
      </div>

      <div className="ask-actions">
        <button
          type="button"
          className="primary-button"
          onClick={onAsk}
          disabled={loading}
        >
          {loading
            ? 'Searching...'
            : hasClarification
            ? 'Submit Clarification'
            : 'Ask AI'}
        </button>

        <button
          type="button"
          className="secondary-button"
          onClick={onVoiceStart}
        >
          🎤 Start Voice
        </button>

        <button
          type="button"
          className="secondary-button"
          onClick={onVoiceStop}
        >
          ⏹ Stop
        </button>
      </div>

      {hasClarification ? (
        <div className="clarification-box">
          <div className="clarification-title">
            Need a quick clarification
          </div>

          <p>
            {clarificationState.question}
          </p>
        </div>
      ) : null}

      {voiceState?.transcript ? (
        <div className="status-message success">
          Recognized Query: “
          {voiceState.transcript}
          ”
        </div>
      ) : null}

      {voiceState?.error ? (
        <div className="status-message error">
          {voiceState.error}
        </div>
      ) : null}

      {errorMessage ? (
        <div className="status-message error">
          {errorMessage}
        </div>
      ) : null}

      {answer || queryType || status ? (
        <div
          className="result-item response-panel"
          style={{ marginTop: '1rem' }}
        >
          <div className="result-number">
            AI Response
          </div>

          {answer ? (
            <div className="answer-block">
              <strong>Answer:</strong>{' '}
              {answer}
            </div>
          ) : null}

          <div className="response-meta-row">
            {queryType ? (
              <span>
                <strong>Query type:</strong>{' '}
                {queryType}
              </span>
            ) : null}

            <span>
              <strong>Retrieval:</strong>{' '}
              Top-{responseTopK}
            </span>

            {classificationConfidence !== null ? (
              <span>
                <strong>
                  Classification confidence:
                </strong>{' '}
                {Number(
                  classificationConfidence
                ).toFixed(2)}
              </span>
            ) : null}

            {sources.length > 0 ? (
              <span>
                <strong>Sources:</strong>{' '}
                {sources.join(', ')}
              </span>
            ) : null}

            {confidence &&
            (confidence.label ||
              confidence.score !==
                undefined) ? (
              <span>
                <strong>Confidence:</strong>{' '}
                {confidence.label || 'Low'} (
                {Number(
                  confidence.score || 0
                ).toFixed(2)}
                )
              </span>
            ) : null}

            {status ? (
              <span>
                <strong>Status:</strong>{' '}
                {status}
              </span>
            ) : null}
          </div>

          {lowConfidence ? (
            <div className="low-confidence-banner">
              Low confidence: no sufficient
              supporting information was found
              in the knowledge base.
            </div>
          ) : null}

          <div className="speech-controls">
            <button
              type="button"
              className="secondary-button"
              onClick={onSpeakAnswer}
            >
              🔊 Read Answer
            </button>

            <button
              type="button"
              className="secondary-button"
              onClick={onPauseSpeech}
            >
              ⏸ Pause
            </button>

            <button
              type="button"
              className="secondary-button"
              onClick={onResumeSpeech}
            >
              ▶ Resume
            </button>

            <button
              type="button"
              className="secondary-button"
              onClick={onStopSpeech}
            >
              ⏹ Stop
            </button>
          </div>

          {hints && hints.summary ? (
            <div className="context-note">
              <strong>Context:</strong>{' '}
              {hints.summary}
            </div>
          ) : null}

          <div className="transparency-panel">
            <button
              type="button"
              className="transparency-toggle"
              onClick={() =>
                setShowEvidence(
                  (open) => !open
                )
              }
            >
              {showEvidence
                ? 'Hide Supporting Evidence'
                : 'View Supporting Evidence'}
            </button>

            {showEvidence ? (
              <div className="evidence-list">
                {evidenceItems.length > 0 ? (
                  evidenceItems.map(
                    (item, index) => (
                      <div
                        className="evidence-item"
                        key={`${item?.source || 'source'}-${
                          item?.chunk_id ||
                          index
                        }`}
                      >
                        <div className="evidence-line">
                          <strong>
                            Source:
                          </strong>{' '}
                          {item?.source ||
                            'Unknown source'}
                        </div>

                        <div className="evidence-line">
                          <strong>
                            Chunk ID:
                          </strong>{' '}
                          {item?.chunk_id ||
                            'Unknown'}
                        </div>

                        <div className="evidence-line">
                          <strong>
                            Chunk Index:
                          </strong>{' '}
                          {item?.chunk_index ??
                            index}
                        </div>

                        <div className="evidence-line">
                          <strong>
                            Relevance:
                          </strong>{' '}
                          {item?.relevance_score ??
                            item?.score ??
                            'N/A'}
                        </div>

                        <div className="evidence-line">
                          <strong>
                            Distance:
                          </strong>{' '}
                          {item?.distance ??
                            'N/A'}
                        </div>

                        <div className="evidence-line">
                          <strong>
                            Citation:
                          </strong>{' '}
                          {item?.citation ||
                            item?.source ||
                            'Unknown'}
                        </div>

                        <div className="evidence-text">
                          <strong>
                            Retrieved Text:
                          </strong>

                          <p>
                            {item?.text ||
                              'No content available.'}
                          </p>
                        </div>
                      </div>
                    )
                  )
                ) : (
                  <div className="evidence-empty">
                    No sufficient supporting
                    information was found in
                    the knowledge base.
                  </div>
                )}
              </div>
            ) : null}
          </div>
        </div>
      ) : null}

      <div className="results-header">
        <h3>Retrieved Information</h3>
      </div>

      {loading ? (
        <div className="loading-state">
          <span
            className="loader"
            aria-hidden="true"
          />

          <span>
            Searching knowledge base...
          </span>
        </div>
      ) : isEmptyState ? (
        <div className="empty-state">
          <div className="empty-icon">
            🔎
          </div>

          <h3>
            {emptyMessage ||
              'No search results yet'}
          </h3>

          {!emptyMessage && (
            <p>
              Ask a question to retrieve
              information from your knowledge
              base.
            </p>
          )}
        </div>
      ) : (
        <div className="results-list">
          {results.map((result, index) => (
            <div
              key={`${result?.source || 'source'}-${index}`}
              className="result-item"
            >
              <div className="result-number">
                Result {index + 1}
              </div>

              <p className="result-text">
                {result?.text ||
                  'No content available.'}
              </p>

              <div className="result-meta">
                <span
                  className="meta-icon"
                  aria-hidden="true"
                >
                  📄
                </span>

                <span>
                  Source:{' '}
                  {result?.source ||
                    'Unknown source'}
                </span>

                {result?.chunk_index !==
                  undefined &&
                result?.chunk_index !==
                  null ? (
                  <span className="chunk-label">
                    Chunk:{' '}
                    {result.chunk_index}
                  </span>
                ) : null}

                {result?.relevance_score !==
                  undefined &&
                result?.relevance_score !==
                  null ? (
                  <span className="chunk-label">
                    Relevance:{' '}
                    {result.relevance_score}
                  </span>
                ) : null}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AskAI;