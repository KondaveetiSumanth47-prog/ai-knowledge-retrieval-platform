import React, { useState, useEffect } from 'react';
import { Cpu, Bot, Database, Search, MessageSquare, Layers, ShieldCheck, Sparkles, CheckCircle2, RefreshCw } from 'lucide-react';

export default function AgentArchitectureView({ API_BASE }) {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/agents/status`)
      .then((res) => res.json())
      .then((data) => setAgents(data.agents || []))
      .catch((err) => console.error('Failed to load agent status:', err))
      .finally(() => setLoading(false));
  }, [API_BASE]);

  const agentCards = [
    {
      id: 'query_understanding',
      name: '1. Query Understanding Agent',
      icon: Cpu,
      color: '#6366f1',
      badge: 'Classifier & Router',
      desc: 'Parses incoming user query, extracts domain keywords, classifies intent (Factual, Procedural, Comparative, Ambiguous), and routes to the designated resolution path.'
    },
    {
      id: 'retrieval',
      name: '2. Retrieval Agent',
      icon: Search,
      color: '#06b6d4',
      badge: 'Hybrid Search & Filter',
      desc: 'Executes ChromaDB semantic vector search, calculates hybrid relevance scores (70% vector similarity + 30% keyword density), and filters out low-confidence results (<0.35).'
    },
    {
      id: 'clarification',
      name: '3. Clarification Agent',
      icon: ShieldCheck,
      color: '#f59e0b',
      badge: 'Threshold Guard',
      desc: 'Evaluates context sufficiency and similarity threshold. Triggers dynamic follow-up clarification options if the query is ambiguous or context is missing.'
    },
    {
      id: 'memory',
      name: '4. Conversation Memory Agent',
      icon: Database,
      color: '#10b981',
      badge: 'Dialogue State',
      desc: 'Maintains multi-turn conversation dialogue history in SQLite database to support context-aware follow-up queries across user sessions.'
    },
    {
      id: 'response_generator',
      name: '5. Response Generation Agent',
      icon: Sparkles,
      color: '#ec4899',
      badge: 'Grounded Synthesizer',
      desc: 'Synthesizes grounded answers tailored to resolution paths (Factual Direct, Procedural Workflow, Comparative Matrix) via Groq Llama-3 with citations & confidence indicator meters.'
    }
  ];

  return (
    <div style={{ padding: '2rem 0', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', backgroundColor: 'rgba(99, 102, 241, 0.15)', border: '1px solid rgba(99, 102, 241, 0.3)', padding: '0.35rem 0.85rem', borderRadius: '20px', color: '#818cf8', fontSize: '0.8rem', fontWeight: 600, marginBottom: '0.75rem' }}>
          <Layers size={14} /> Multi-Agent Orchestration Architecture
        </div>
        <h2 style={{ fontSize: '1.75rem', fontWeight: 700, background: 'linear-gradient(to right, #ffffff, #cbd5e1)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          AI Agent Layer & Sequential Resolution Flow
        </h2>
        <p style={{ fontSize: '0.875rem', color: '#94a3b8', maxWidth: '700px', margin: '0.5rem auto 0 auto' }}>
          Every query passes through 5 specialized AI sub-agents managed by a central stateful orchestrator, coordinating intent classification, hybrid vector retrieval, threshold guarding, and grounded synthesis.
        </p>
      </div>

      {/* Interactive Workflow Diagram */}
      <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2.5rem', position: 'relative', overflow: 'hidden' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '1rem' }}>
          <span style={{ fontSize: '0.9rem', fontWeight: 600, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Bot size={18} color="#6366f1" /> Sequential Multi-Agent Execution Pipeline
          </span>
          <span style={{ fontSize: '0.75rem', color: '#10b981', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <CheckCircle2 size={14} /> Multi-Agent Orchestrator Active
          </span>
        </div>

        {/* Pipeline Step Nodes */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1rem', position: 'relative' }}>
          {agentCards.map((agent, index) => {
            const Icon = agent.icon;
            return (
              <div
                key={agent.id}
                className="glass-card"
                style={{
                  padding: '1.25rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.75rem',
                  position: 'relative',
                  borderTop: `4px solid ${agent.color}`
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '8px',
                    backgroundColor: `${agent.color}20`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <Icon size={18} color={agent.color} />
                  </div>
                  <span style={{ fontSize: '0.65rem', fontWeight: 700, padding: '0.15rem 0.4rem', borderRadius: '4px', backgroundColor: '#0f172a', color: agent.color, border: `1px solid ${agent.color}40` }}>
                    {agent.badge}
                  </span>
                </div>

                <h3 style={{ fontSize: '0.85rem', fontWeight: 700, color: '#f8fafc', lineHeight: '1.3' }}>
                  {agent.name}
                </h3>

                <p style={{ fontSize: '0.75rem', color: '#94a3b8', lineHeight: '1.45', flex: 1 }}>
                  {agent.desc}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Detailed Classification Taxonomy & Resolution Paths */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Cpu size={18} color="#6366f1" /> Query Classification Taxonomy
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.8rem' }}>
            <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#818cf8', fontWeight: 600, marginBottom: '0.2rem' }}>
                <span>Factual Query</span>
                <span>Path: factual_direct</span>
              </div>
              <p style={{ color: '#94a3b8' }}>Direct lookup requests for definitions, parameters, SLA numbers, or storage conditions.</p>
            </div>

            <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#22d3ee', fontWeight: 600, marginBottom: '0.2rem' }}>
                <span>Procedural Query</span>
                <span>Path: procedural_workflow</span>
              </div>
              <p style={{ color: '#94a3b8' }}>Multi-step workflow queries requiring ordered step-by-step instructions or protocols.</p>
            </div>

            <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#fbbf24', fontWeight: 600, marginBottom: '0.2rem' }}>
                <span>Comparative Query</span>
                <span>Path: comparative_matrix</span>
              </div>
              <p style={{ color: '#94a3b8' }}>Cross-document comparison queries evaluating cost, uptime, or protocol differences.</p>
            </div>

            <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: '#f43f5e', fontWeight: 600, marginBottom: '0.2rem' }}>
                <span>Ambiguous Query</span>
                <span>Path: ambiguous_clarification</span>
              </div>
              <p style={{ color: '#94a3b8' }}>Underspecified or extremely brief queries triggering interactive clarification options.</p>
            </div>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Search size={18} color="#06b6d4" /> Retrieval & Response Synthesis
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.8rem', color: '#cbd5e1' }}>
            <div style={{ backgroundColor: '#0f172a', padding: '0.85rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <h4 style={{ color: '#06b6d4', fontWeight: 600, marginBottom: '0.25rem' }}>Hybrid Relevance Ranking</h4>
              <p style={{ color: '#94a3b8', fontSize: '0.78rem' }}>
                Combines dense vector similarity (70%) with keyword overlap density (30%) to rank top passage matches accurately.
              </p>
            </div>

            <div style={{ backgroundColor: '#0f172a', padding: '0.85rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <h4 style={{ color: '#f59e0b', fontWeight: 600, marginBottom: '0.25rem' }}>Low-Confidence Result Filtering</h4>
              <p style={{ color: '#94a3b8', fontSize: '0.78rem' }}>
                Chunks falling below the 0.35 similarity threshold are automatically filtered out to eliminate hallucination.
              </p>
            </div>

            <div style={{ backgroundColor: '#0f172a', padding: '0.85rem', borderRadius: '8px', border: '1px solid #334155' }}>
              <h4 style={{ color: '#ec4899', fontWeight: 600, marginBottom: '0.25rem' }}>Dynamic Confidence Indicators</h4>
              <p style={{ color: '#94a3b8', fontSize: '0.78rem' }}>
                Computes overall response confidence (%) and classifies output as High (&gt;75%), Medium (45-74%), or Low (&lt;45%).
              </p>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}
