import React, { useState, useEffect } from 'react';
import { FileText, Trash2, Eye, RefreshCw, Database, Layers, Search, X } from 'lucide-react';

export default function DocumentBrowser({ API_BASE }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [docChunks, setDocChunks] = useState([]);
  const [chunksLoading, setChunksLoading] = useState(false);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/documents`);
      const data = await res.json();
      setDocuments(data.documents || []);
    } catch (err) {
      console.error('Failed to fetch documents:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleDelete = async (docId) => {
    if (!window.confirm('Are you sure you want to delete this document and all its vector chunks?')) return;
    try {
      await fetch(`${API_BASE}/api/documents/${docId}`, { method: 'DELETE' });
      fetchDocuments();
    } catch (err) {
      alert(`Delete failed: ${err.message}`);
    }
  };

  const handleInspectChunks = async (doc) => {
    setSelectedDoc(doc);
    setChunksLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/documents/${doc.id}`);
      const data = await res.json();
      setDocChunks(data.chunks || []);
    } catch (err) {
      console.error('Failed to fetch chunks:', err);
    } finally {
      setChunksLoading(false);
    }
  };

  const filteredDocs = documents.filter(
    (d) =>
      d.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.domain.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ padding: '2rem 0', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Database size={22} color="#6366f1" />
            Knowledge Base Documents
          </h2>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
            Browse ingested PDF, DOCX, TXT, and CSV documents indexed in SQLite and ChromaDB.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <div style={{ position: 'relative' }}>
            <Search size={16} color="#64748b" style={{ position: 'absolute', left: '10px', top: '10px' }} />
            <input
              type="text"
              placeholder="Filter by title or domain..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                padding: '0.5rem 0.75rem 0.5rem 2.2rem',
                borderRadius: '8px',
                backgroundColor: '#0f172a',
                border: '1px solid #334155',
                color: '#f8fafc',
                fontSize: '0.85rem'
              }}
            />
          </div>

          <button
            onClick={fetchDocuments}
            style={{
              padding: '0.5rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid #334155',
              backgroundColor: '#1e293b',
              color: '#cbd5e1',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              fontSize: '0.85rem'
            }}
          >
            <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
            Refresh
          </button>
        </div>
      </div>

      {/* Document Table */}
      <div className="glass-panel" style={{ overflow: 'hidden' }}>
        {loading ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>
            <RefreshCw className="animate-spin" size={24} style={{ marginBottom: '0.5rem' }} />
            <p>Loading documents repository...</p>
          </div>
        ) : filteredDocs.length === 0 ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#64748b' }}>
            <FileText size={36} style={{ opacity: 0.4, marginBottom: '0.5rem' }} />
            <p style={{ fontSize: '0.9rem' }}>No documents found matching search criteria.</p>
          </div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
            <thead>
              <tr style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', color: '#94a3b8', fontSize: '0.75rem', textTransform: 'uppercase' }}>
                <th style={{ padding: '0.85rem 1.25rem' }}>Filename</th>
                <th style={{ padding: '0.85rem 1.25rem' }}>Domain</th>
                <th style={{ padding: '0.85rem 1.25rem' }}>Format</th>
                <th style={{ padding: '0.85rem 1.25rem' }}>Chunks</th>
                <th style={{ padding: '0.85rem 1.25rem' }}>Raw Size</th>
                <th style={{ padding: '0.85rem 1.25rem' }}>Upload Date</th>
                <th style={{ padding: '0.85rem 1.25rem', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredDocs.map((doc) => (
                <tr key={doc.id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)', transition: 'background 0.2s' }}>
                  <td style={{ padding: '1rem 1.25rem', fontWeight: 600, color: '#f8fafc' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <FileText size={16} color="#6366f1" />
                      {doc.filename}
                    </div>
                  </td>
                  <td style={{ padding: '1rem 1.25rem', color: '#cbd5e1' }}>
                    <span style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem', borderRadius: '12px', backgroundColor: 'rgba(6, 182, 212, 0.1)', color: '#22d3ee', border: '1px solid rgba(6, 182, 212, 0.2)' }}>
                      {doc.domain}
                    </span>
                  </td>
                  <td style={{ padding: '1rem 1.25rem' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#818cf8', textTransform: 'uppercase' }}>
                      {doc.file_type}
                    </span>
                  </td>
                  <td style={{ padding: '1rem 1.25rem', fontWeight: 600, color: '#10b981' }}>
                    {doc.chunk_count} chunks
                  </td>
                  <td style={{ padding: '1rem 1.25rem', color: '#94a3b8', fontSize: '0.8rem' }}>
                    {doc.raw_char_count} chars
                  </td>
                  <td style={{ padding: '1rem 1.25rem', color: '#64748b', fontSize: '0.75rem' }}>
                    {new Date(doc.upload_time).toLocaleString()}
                  </td>
                  <td style={{ padding: '1rem 1.25rem', textAlign: 'right' }}>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                      <button
                        onClick={() => handleInspectChunks(doc)}
                        title="View Chunks"
                        style={{ padding: '0.4rem', borderRadius: '6px', border: '1px solid #334155', backgroundColor: '#0f172a', color: '#06b6d4', cursor: 'pointer' }}
                      >
                        <Eye size={14} />
                      </button>
                      <button
                        onClick={() => handleDelete(doc.id)}
                        title="Delete Document"
                        style={{ padding: '0.4rem', borderRadius: '6px', border: '1px solid rgba(244, 63, 94, 0.3)', backgroundColor: 'rgba(244, 63, 94, 0.1)', color: '#f43f5e', cursor: 'pointer' }}
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Chunk Viewer Modal */}
      {selectedDoc && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(4px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 100
        }}>
          <div className="glass-panel" style={{ width: '90%', maxWidth: '800px', maxHeight: '80vh', display: 'flex', flexDirection: 'column', padding: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '0.75rem' }}>
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: '#f8fafc' }}>
                  Document Chunk Viewer
                </h3>
                <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                  {selectedDoc.filename} • {docChunks.length} chunks indexed in ChromaDB
                </p>
              </div>
              <button
                onClick={() => setSelectedDoc(null)}
                style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
              >
                <X size={20} />
              </button>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {chunksLoading ? (
                <div style={{ textAlign: 'center', padding: '2rem', color: '#94a3b8' }}>
                  <RefreshCw className="animate-spin" size={24} />
                  <p style={{ marginTop: '0.5rem' }}>Fetching chunk segments...</p>
                </div>
              ) : docChunks.length === 0 ? (
                <p style={{ color: '#64748b', textAlign: 'center', padding: '2rem' }}>No chunks found.</p>
              ) : (
                docChunks.map((c) => (
                  <div key={c.id} style={{ padding: '0.85rem', backgroundColor: '#0f172a', borderRadius: '8px', border: '1px solid #334155' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#818cf8', fontWeight: 600, marginBottom: '0.35rem' }}>
                      <span>Chunk #{c.chunk_index + 1}</span>
                      <span style={{ color: '#64748b' }}>~{c.token_estimate} tokens</span>
                    </div>
                    <p style={{ fontSize: '0.825rem', color: '#e2e8f0', fontFamily: 'var(--font-mono)', lineHeight: '1.4' }}>
                      {c.content}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
