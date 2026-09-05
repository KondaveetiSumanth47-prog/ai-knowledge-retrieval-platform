import React from 'react';
import { Database, Bot, FileText, BarChart3, Sparkles } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'ingest', label: 'Document Ingestion (M1.3)', icon: Database },
    { id: 'query', label: 'Multi-Agent Query UI (Voice/Text)', icon: Bot },
    { id: 'documents', label: 'Knowledge Base Browser', icon: FileText },
    { id: 'eval', label: 'Retrieval Benchmark (M1.4)', icon: BarChart3 },
  ];

  return (
    <header style={{
      borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      backdropFilter: 'blur(10px)',
      position: 'sticky',
      top: 0,
      zIndex: 50,
      padding: '0.75rem 2rem'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            background: 'linear-gradient(135deg, #6366f1, #06b6d4)',
            padding: '0.5rem',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Sparkles size={22} color="#fff" />
          </div>
          <div>
            <h1 style={{ fontSize: '1.25rem', fontWeight: 700, letterSpacing: '-0.02em', background: 'linear-gradient(to right, #ffffff, #94a3b8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              RAG Knowledge Retrieval Platform
            </h1>
            <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '-2px' }}>
              Multi-Agent Query System & Chunking Engine (Milestone 1)
            </p>
          </div>
        </div>

        <nav style={{ display: 'flex', gap: '0.5rem' }}>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.6rem 1rem',
                  borderRadius: '8px',
                  border: 'none',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  backgroundColor: isActive ? 'rgba(99, 102, 241, 0.2)' : 'transparent',
                  color: isActive ? '#818cf8' : '#94a3b8',
                  outline: isActive ? '1px solid rgba(99, 102, 241, 0.4)' : 'none'
                }}
              >
                <Icon size={18} color={isActive ? '#818cf8' : '#94a3b8'} />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
