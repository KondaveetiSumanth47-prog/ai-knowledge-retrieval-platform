import React, { useState, useEffect } from 'react';
import { BarChart3, Play, CheckCircle2, AlertTriangle, HelpCircle, Layers, FileCheck, RefreshCw } from 'lucide-react';

export default function EvaluationDashboard({ API_BASE }) {
  const [evalData, setEvalData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [historyLogs, setHistoryLogs] = useState([]);

  const fetchEvalLogs = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/eval/results`);
      const data = await res.json();
      if (data.eval_logs && data.eval_logs.length > 0) {
        setHistoryLogs(data.eval_logs);
        if (!evalData) setEvalData(data.eval_logs[0]);
      }
    } catch (err) {
      console.error('Error fetching eval logs:', err);
    }
  };

  useEffect(() => {
    fetchEvalLogs();
  }, []);

  const handleRunBenchmark = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/eval/run`, { method: 'POST' });
      const data = await res.json();
      setEvalData(data);
      fetchEvalLogs();
    } catch (err) {
      alert(`Benchmark execution failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem 0', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Top Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <BarChart3 size={24} color="#6366f1" />
            <h2 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#f8fafc' }}>
              RAG Retrieval Pipeline Accuracy Benchmark
            </h2>
            <span style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem', borderRadius: '12px', background: 'rgba(99, 102, 241, 0.2)', color: '#818cf8', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
              Milestone 1.4
            </span>
          </div>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '0.2rem' }}>
            Automated empirical validation evaluating Top-1, Top-3, and Top-5 retrieval precision across Cloud Infrastructure and Healthcare domain datasets.
          </p>
        </div>

        <button
          onClick={handleRunBenchmark}
          disabled={loading}
          style={{
            padding: '0.75rem 1.25rem',
            borderRadius: '8px',
            border: 'none',
            backgroundColor: '#6366f1',
            color: '#fff',
            fontWeight: 600,
            fontSize: '0.875rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            boxShadow: '0 4px 14px rgba(99, 102, 241, 0.4)'
          }}
        >
          {loading ? <RefreshCw className="animate-spin" size={18} /> : <Play size={18} />}
          {loading ? 'Evaluating Retrieval Suite...' : 'Run Automated Benchmark (10 Queries)'}
        </button>
      </div>

      {evalData ? (
        <>
          {/* Metric Cards Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.25rem', marginBottom: '1.5rem' }}>
            <div className="glass-panel" style={{ padding: '1.25rem', textAlign: 'center', borderTop: '4px solid #10b981' }}>
              <span style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Top-1 Accuracy</span>
              <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#10b981', marginTop: '0.2rem' }}>
                {evalData.top_1_accuracy}%
              </div>
              <span style={{ fontSize: '0.7rem', color: '#64748b' }}>First rank match precision</span>
            </div>

            <div className="glass-panel" style={{ padding: '1.25rem', textAlign: 'center', borderTop: '4px solid #06b6d4' }}>
              <span style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Top-3 Accuracy</span>
              <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#06b6d4', marginTop: '0.2rem' }}>
                {evalData.top_3_accuracy}%
              </div>
              <span style={{ fontSize: '0.7rem', color: '#64748b' }}>Top 3 passage coverage</span>
            </div>

            <div className="glass-panel" style={{ padding: '1.25rem', textAlign: 'center', borderTop: '4px solid #6366f1' }}>
              <span style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Top-5 Accuracy</span>
              <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#818cf8', marginTop: '0.2rem' }}>
                {evalData.top_5_accuracy}%
              </div>
              <span style={{ fontSize: '0.7rem', color: '#64748b' }}>Top 5 context recall</span>
            </div>

            <div className="glass-panel" style={{ padding: '1.25rem', textAlign: 'center', borderTop: '4px solid #f59e0b' }}>
              <span style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Evaluated Queries</span>
              <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#fbbf24', marginTop: '0.2rem' }}>
                {evalData.total_queries}
              </div>
              <span style={{ fontSize: '0.7rem', color: '#64748b' }}>2 Domains • 4 Query Categories</span>
            </div>
          </div>

          {/* Benchmark Results Table */}
          <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FileCheck size={18} color="#06b6d4" />
              Detailed Benchmark Query Results Breakdown
            </h3>

            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
                <thead>
                  <tr style={{ backgroundColor: 'rgba(15, 23, 42, 0.6)', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', color: '#94a3b8', fontSize: '0.75rem' }}>
                    <th style={{ padding: '0.75rem 1rem' }}>Domain</th>
                    <th style={{ padding: '0.75rem 1rem' }}>Category</th>
                    <th style={{ padding: '0.75rem 1rem' }}>Query Statement</th>
                    <th style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>Top-1</th>
                    <th style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>Top-3</th>
                    <th style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>Top-5</th>
                    <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Top Score</th>
                  </tr>
                </thead>
                <tbody>
                  {evalData.detailed_results.map((res, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                      <td style={{ padding: '0.75rem 1rem', color: '#cbd5e1', fontSize: '0.75rem' }}>
                        {res.domain.split(' ')[0]}
                      </td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        <span style={{
                          fontSize: '0.7rem',
                          padding: '0.15rem 0.45rem',
                          borderRadius: '4px',
                          backgroundColor: res.type === 'Factual' ? 'rgba(99, 102, 241, 0.15)' :
                                           res.type === 'Procedural' ? 'rgba(6, 182, 212, 0.15)' :
                                           res.type === 'Comparative' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(244, 63, 94, 0.15)',
                          color: res.type === 'Factual' ? '#818cf8' :
                                 res.type === 'Procedural' ? '#22d3ee' :
                                 res.type === 'Comparative' ? '#fbbf24' : '#f43f5e'
                        }}>
                          {res.type}
                        </span>
                      </td>
                      <td style={{ padding: '0.75rem 1rem', color: '#f8fafc', fontWeight: 500 }}>
                        {res.query}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>
                        {res.top_1_hit ? <CheckCircle2 size={16} color="#10b981" /> : <AlertTriangle size={16} color="#f43f5e" />}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>
                        {res.top_3_hit ? <CheckCircle2 size={16} color="#10b981" /> : <AlertTriangle size={16} color="#f43f5e" />}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', textAlign: 'center' }}>
                        {res.top_5_hit ? <CheckCircle2 size={16} color="#10b981" /> : <AlertTriangle size={16} color="#f43f5e" />}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', textAlign: 'right', fontWeight: 600, color: '#06b6d4', fontFamily: 'var(--font-mono)' }}>
                        {(res.top_score * 100).toFixed(1)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Performance & Limitations Documentation Box (M1.4 Requirement) */}
          <div className="glass-panel" style={{ padding: '1.5rem', borderLeft: '4px solid #6366f1' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <HelpCircle size={18} color="#6366f1" />
              Retrieval Limitations Analysis & Milestone 2 Optimizations
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', fontSize: '0.825rem', color: '#cbd5e1' }}>
              <div>
                <h4 style={{ color: '#fbbf24', fontSize: '0.85rem', marginBottom: '0.35rem' }}>Observed Retrieval Limitations:</h4>
                <ul style={{ paddingLeft: '1.2rem', lineHeight: '1.6' }}>
                  <li>Dense vector similarity alone can score high on syntactic overlap for unavailable queries without strict thresholding.</li>
                  <li>Fixed character chunk size (500) occasionally splits complex multi-step procedural paragraphs across chunk boundaries.</li>
                  <li>Comparative queries spanning multiple documents require multi-pass query expansion.</li>
                </ul>
              </div>

              <div>
                <h4 style={{ color: '#34d399', fontSize: '0.85rem', marginBottom: '0.35rem' }}>Proposed Milestone 2 Roadmap:</h4>
                <ul style={{ paddingLeft: '1.2rem', lineHeight: '1.6' }}>
                  <li>Implement Hybrid Search (Dense SentenceTransformers + BM25 Sparse Keyword Ranking).</li>
                  <li>Introduce Cross-Encoder Re-Ranking model (`ms-marco-MiniLM-L-6-v2`) for top 10 retrieved passages.</li>
                  <li>Enforce Dynamic Agent Clarification for low similarity threshold queries (&lt; 0.35).</li>
                </ul>
              </div>
            </div>
          </div>
        </>
      ) : (
        <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', color: '#64748b' }}>
          <BarChart3 size={40} style={{ opacity: 0.3, marginBottom: '0.75rem' }} />
          <p style={{ fontSize: '0.95rem', color: '#e2e8f0' }}>No retrieval accuracy benchmark has been run yet.</p>
          <p style={{ fontSize: '0.85rem', marginTop: '0.35rem' }}>
            Click "Run Automated Benchmark" above or ensure sample knowledge base documents have been ingested.
          </p>
        </div>
      )}

    </div>
  );
}
