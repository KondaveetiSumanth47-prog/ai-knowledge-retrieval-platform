import { useRef, useState } from 'react';

function UploadCard({ onUpload, isUploading, uploadState, selectedFile, setSelectedFile }) {
  const inputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileSelection = (file) => {
    if (!file) return;
    const acceptedTypes = ['.pdf', '.docx', '.txt', '.csv'];
    const extension = `.${file.name.split('.').pop().toLowerCase()}`;

    if (!acceptedTypes.includes(extension)) {
      onUpload(null, 'unsupported');
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    onUpload(file, 'selected');
  };

  return (
    <div className="page-card upload-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Knowledge Base</p>
          <h2>Knowledge Base</h2>
        </div>
      </div>

      <div className="knowledge-summary">
        <div className="summary-pill"><span className="summary-dot blue" />Smart indexing</div>
        <div className="summary-pill"><span className="summary-dot violet" />Document ready</div>
        <div className="summary-pill"><span className="summary-dot green" />Fast retrieval</div>
      </div>

      <p className="section-subtitle">
        Upload documents to add them to your searchable knowledge base.
      </p>

      <div className="supported-formats">
        {['PDF', 'DOCX', 'TXT', 'CSV'].map((format) => (
          <span key={format} className="format-pill">{format}</span>
        ))}
      </div>

      <div
        className={`upload-dropzone ${dragActive ? 'active' : ''}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragActive(false);
          const file = e.dataTransfer.files?.[0];
          handleFileSelection(file);
        }}
      >
        <div className="upload-icon">📄</div>
        <p className="drop-text">Drag &amp; drop your document here</p>
        <p className="drop-subtext">or</p>
        <button
          type="button"
          className="secondary-button"
          onClick={() => inputRef.current?.click()}
        >
          Choose a document
        </button>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt,.csv"
          hidden
          onChange={(e) => handleFileSelection(e.target.files?.[0])}
        />
      </div>

      {selectedFile ? (
        <div className="selected-file-box">
          <span className="selected-label">Selected file:</span>
          <strong>{selectedFile.name}</strong>
        </div>
      ) : null}

      <button
        type="button"
        className="primary-button upload-button"
        onClick={() => onUpload(selectedFile, 'upload')}
        disabled={isUploading || !selectedFile}
      >
        {isUploading ? 'Uploading document...' : 'Upload Document'}
      </button>

      {uploadState.message ? (
        <div className={`status-message ${uploadState.type}`}>{uploadState.message}</div>
      ) : null}

      {uploadState.success && uploadState.details ? (
        <div className="upload-success-panel">
          <div className="success-check">✓</div>
          <div>
            <p className="success-title">Document uploaded successfully</p>
            <div className="success-meta">
              <span>File name: {uploadState.details.filename}</span>
              <span>Number of chunks: {uploadState.details.number_of_chunks}</span>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default UploadCard;
