import React, { useState } from 'react';
import { Upload, FileCode, CheckCircle2, AlertCircle, RefreshCw, Layers, Sliders, Database, Sparkles } from 'lucide-react';

export default function IngestionModule({ API_BASE, onIngestionSuccess }) {
  const [file, setFile] = useState(null);
  const [domain, setDomain] = useState('Cloud Infrastructure & DevOps');
  const [chunkSize, setChunkSize] = useState(500);
  const [chunkOverlap, setChunkOverlap] = useState(50);
  const [loading, setLoading] = useState(false);
  const [seedLoading, setSeedLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [ingestResult, setIngestResult] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setMessage(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage({ type: 'error', text: 'Please select a file (PDF, DOCX, TXT, or CSV).' });
      return;
    }

    setLoading(true);
    setMessage(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('domain', domain);
    formData.append('chunk_size', chunkSize);
    formData.append('chunk_overlap', chunkOverlap);

    try {
      const res = await fetch(`${API_BASE}/api/ingest`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Ingestion failed');
      }

      setIngestResult(data);
      setMessage({ type: 'success', text: `Successfully ingested "${file.name}" into vector store!` });
      setFile(null);
      if (onIngestionSuccess) onIngestionSuccess();
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleSeedDataset = async () => {
    setSeedLoading(true);
    setMessage(null);
    try {
      const res = await fetch(`${API_BASE}/api/seed_sample_docs`, {
        method: 'POST',
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Seeding failed');

      setMessage({ type: 'success', text: `Sample Knowledge Base loaded! Ingested ${data.details.length} documents across 2 domains.` });
      if (onIngestionSuccess) onIngestionSuccess();
    } catch (err) {
      setMessage({ type: 'error', text: err.message });
    } finally {
      setSeedLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem 0', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        
        {/* Left Column: Upload Form & Chunk Settings */}
        <div className="glass-panel" style={{ padding: '2rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Upload color="#6366f1" size={24} />
              <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Document Ingestion Module</h2>
            </div>
            <span style={{ fontSize: '0.75rem', padding: '0.25rem 0.6rem', borderRadius: '12px', background: 'rgba(99, 102, 241, 0.2)', color: '#818cf8', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
              Milestone 1.3
            </span>
          </div>

          <form onSubmit={handleUpload}>
            {/* File Dropzone */}
            <div style={{
              border: file ? '2px dashed #6366f1' : '2px dashed #334155',
              borderRadius: '12px',
              padding: '2rem 1rem',
              textAlign: 'center',
              backgroundColor: file ? 'rgba(99, 102, 241, 0.05)' : 'rgba(15, 23, 42, 0.4)',
              cursor: 'pointer',
              marginBottom: '1.5rem',
              transition: 'all 0.2s ease'
            }}
            onClick={() => document.getElementById('file-input').click()}
            >
              <input
                id="file-input"
                type="file"
                accept=".pdf,.docx,.doc,.txt,.csv"
                style={{ display: 'none' }}
                onChange={handleFileChange}
              />
              <FileCode size={36} color={file ? '#6366f1' : '#64748b'} style={{ marginBottom: '0.75rem' }} />
              {file ? (
                <div>
                  <p style={{ fontWeight: 600, color: '#f8fafc' }}>{file.name}</p>
                  <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.25rem' }}>
                    {(file.size / 1024).toFixed(1)} KB • Ready for extraction
                  </p>
                </div>
              ) : (
                <div>
                  <p style={{ fontWeight: 500, color: '#e2e8f0' }}>Click to select or drag & drop document</p>
                  <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '0.35rem' }}>
                    Supported formats: PDF (PyMuPDF), DOCX (docx), TXT, CSV (pandas)
                  </p>
                </div>
              )}
            </div>

            {/* Domain Selection */}
            <div style={{ marginBottom: '1.25rem' }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, color: '#cbd5e1', marginBottom: '0.4rem' }}>
                Knowledge Domain Classification
              </label>
              <select
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  color: '#f8fafc',
                  fontSize: '0.875rem'
                }}
              >
                <option value="Cloud Infrastructure & DevOps">Cloud Infrastructure & DevOps (Domain 1)</option>
                <option value="Healthcare & Medical Protocols">Healthcare & Medical Protocols (Domain 2)</option>
                <option value="General Enterprise Knowledge">General Enterprise Knowledge</option>
              </select>
            </div>

            {/* LangChain Chunking Strategy Controls */}
            <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.5)', padding: '1rem', borderRadius: '10px', marginBottom: '1.5rem', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                <Sliders size={16} color="#06b6d4" />
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#e2e8f0' }}>
                  LangChain Chunking Configuration
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                    <span>Chunk Size</span>
                    <span style={{ color: '#06b6d4', fontWeight: 600 }}>{chunkSize} chars</span>
                  </div>
                  <input
                    type="range"
                    min="200"
                    max="1500"
                    step="50"
                    value={chunkSize}
                    onChange={(e) => setChunkSize(Number(e.target.value))}
                    style={{ width: '100%' }}
                  />
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                    <span>Chunk Overlap</span>
                    <span style={{ color: '#06b6d4', fontWeight: 600 }}>{chunkOverlap} chars</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="200"
                    step="10"
                    value={chunkOverlap}
                    onChange={(e) => setChunkOverlap(Number(e.target.value))}
                    style={{ width: '100%' }}
                  />
                </div>
              </div>
            </div>

            {/* Ingest Action Button */}
            <button
              type="submit"
              disabled={loading || !file}
              style={{
                width: '100%',
                padding: '0.8rem',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: file ? '#6366f1' : '#334155',
                color: '#ffffff',
                fontWeight: 600,
                fontSize: '0.9rem',
                cursor: file ? 'pointer' : 'not-allowed',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
                transition: 'all 0.2s ease'
              }}
            >
              {loading ? <RefreshCw className="animate-spin" size={18} /> : <Upload size={18} />}
              {loading ? 'Processing Pipeline (Extracting, Chunking & Indexing)...' : 'Upload & Process Ingestion'}
            </button>
          </form>

          {/* Quick Seed Button */}
          <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <span style={{ fontSize: '0.85rem', fontWeight: 500, color: '#94a3b8' }}>
                Quick Evaluation Setup
              </span>
              <Sparkles size={16} color="#f59e0b" />
            </div>
            <button
              onClick={handleSeedDataset}
              disabled={seedLoading}
              style={{
                width: '100%',
                padding: '0.7rem',
                borderRadius: '8px',
                border: '1px solid rgba(245, 158, 11, 0.4)',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                color: '#fbbf24',
                fontWeight: 600,
                fontSize: '0.85rem',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem'
              }}
            >
              {seedLoading ? <RefreshCw size={16} className="animate-spin" /> : <Database size={16} />}
              {seedLoading ? 'Ingesting 2-Domain Benchmark Docs...' : 'Seed Sample Knowledge Base (8 Files)'}
            </button>
          </div>

          {/* Messages */}
          {message && (
            <div style={{
              marginTop: '1.25rem',
              padding: '0.85rem 1rem',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              gap: '0.6rem',
              fontSize: '0.85rem',
              backgroundColor: message.type === 'error' ? 'rgba(244, 63, 94, 0.15)' : 'rgba(16, 185, 129, 0.15)',
              border: message.type === 'error' ? '1px solid rgba(244, 63, 94, 0.3)' : '1px solid rgba(16, 185, 129, 0.3)',
              color: message.type === 'error' ? '#fecdd3' : '#a7f3d0'
            }}>
              {message.type === 'error' ? <AlertCircle size={18} color="#f43f5e" /> : <CheckCircle2 size={18} color="#10b981" />}
              {message.text}
            </div>
          )}
        </div>

        {/* Right Column: Processing Pipeline Specs & Ingestion Inspector */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          
          {/* Architecture Pipeline Spec Box */}
          <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Layers size={18} color="#06b6d4" />
              Ingestion Pipeline Specifications
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.85rem', fontSize: '0.8rem' }}>
              <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155' }}>
                <span style={{ color: '#94a3b8', display: 'block', marginBottom: '0.2rem' }}>Text Extractor</span>
                <span style={{ color: '#e2e8f0', fontWeight: 600 }}>PyMuPDF / docx / pandas</span>
              </div>
              <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155' }}>
                <span style={{ color: '#94a3b8', display: 'block', marginBottom: '0.2rem' }}>Chunk Splitter</span>
                <span style={{ color: '#e2e8f0', fontWeight: 600 }}>LangChain RecursiveSplitter</span>
              </div>
              <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155' }}>
                <span style={{ color: '#94a3b8', display: 'block', marginBottom: '0.2rem' }}>Embedding Vector</span>
                <span style={{ color: '#e2e8f0', fontWeight: 600 }}>all-MiniLM-L6-v2 (384-d)</span>
              </div>
              <div style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155' }}>
                <span style={{ color: '#94a3b8', display: 'block', marginBottom: '0.2rem' }}>Vector Indexing</span>
                <span style={{ color: '#e2e8f0', fontWeight: 600 }}>ChromaDB Persistent Store</span>
              </div>
            </div>
          </div>

          {/* Ingestion Results Preview */}
          {ingestResult ? (
            <div className="glass-panel" style={{ padding: '1.5rem', flex: 1 }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc', marginBottom: '0.75rem' }}>
                Ingested Document Summary
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.75rem', marginBottom: '1rem' }}>
                <div className="glass-card" style={{ padding: '0.75rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#6366f1' }}>{ingestResult.chunks_count}</div>
                  <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Total Chunks</div>
                </div>
                <div className="glass-card" style={{ padding: '0.75rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#06b6d4' }}>{ingestResult.document.raw_char_count}</div>
                  <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Cleaned Chars</div>
                </div>
                <div className="glass-card" style={{ padding: '0.75rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#10b981' }}>{ingestResult.document.file_type.toUpperCase()}</div>
                  <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>File Extension</div>
                </div>
              </div>

              <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: '#cbd5e1', marginBottom: '0.5rem' }}>
                Sample Chunk Passages (First 3):
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '250px', overflowY: 'auto' }}>
                {ingestResult.preview_chunks.map((c, i) => (
                  <div key={i} style={{ padding: '0.65rem', backgroundColor: '#0f172a', borderRadius: '6px', border: '1px solid #334155', fontSize: '0.75rem', fontFamily: 'var(--font-mono)' }}>
                    <span style={{ color: '#6366f1', fontWeight: 600 }}>[Chunk #{c.chunk_index + 1}]</span>: {c.content}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', color: '#64748b', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
              <FileCode size={40} style={{ opacity: 0.4, marginBottom: '0.75rem' }} />
              <p style={{ fontSize: '0.9rem' }}>No recent document ingestion event.</p>
              <p style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>Upload a document or seed the sample knowledge base to inspect vector store indexing.</p>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
