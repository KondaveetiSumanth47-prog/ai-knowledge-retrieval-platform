import React, { useState } from 'react';
import Navbar from './components/Navbar';
import IngestionModule from './components/IngestionModule';
import QueryWorkspace from './components/QueryWorkspace';
import AgentArchitectureView from './components/AgentArchitectureView';
import DocumentBrowser from './components/DocumentBrowser';
import EvaluationDashboard from './components/EvaluationDashboard';

const API_BASE = 'http://localhost:5000';

export default function App() {
  const [activeTab, setActiveTab] = useState('query');

  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'var(--bg-dark)' }}>
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main style={{ padding: '0 1rem' }}>
        {activeTab === 'ingest' && (
          <IngestionModule API_BASE={API_BASE} />
        )}
        
        {activeTab === 'query' && (
          <QueryWorkspace API_BASE={API_BASE} />
        )}

        {activeTab === 'agents' && (
          <AgentArchitectureView API_BASE={API_BASE} />
        )}
        
        {activeTab === 'documents' && (
          <DocumentBrowser API_BASE={API_BASE} />
        )}
        
        {activeTab === 'eval' && (
          <EvaluationDashboard API_BASE={API_BASE} />
        )}
      </main>
    </div>
  );
}
