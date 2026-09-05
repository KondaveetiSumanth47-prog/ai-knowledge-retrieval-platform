import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, VolumeX, Send, Bot, User, Sparkles, AlertCircle, FileText, ChevronRight, CheckCircle2, Cpu, Filter, Clock } from 'lucide-react';

export default function QueryWorkspace({ API_BASE }) {
  const [query, setQuery] = useState('');
  const [domainFilter, setDomainFilter] = useState('all');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(true);
  const [activeTrace, setActiveTrace] = useState(null);
  
  const chatEndRef = useRef(null);
  const recognitionRef = useRef(null);

  // Initialize Web Speech API Speech Recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setQuery(transcript);
        setIsListening(false);
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    } else {
      setSpeechSupported(false);
    }
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const toggleListening = () => {
    if (!recognitionRef.current) return;
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const speakText = (text) => {
    if (!('speechSynthesis' in window)) return;

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const cleanText = text.replace(/[*#_`\[\]]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const handleSendQuery = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim() || loading) return;

    const userMsg = { sender: 'user', content: query };
    setMessages((prev) => [...prev, userMsg]);
    const currentQuery = query;
    setQuery('');
    setLoading(true);
    setActiveTrace(null);

    try {
      const res = await fetch(`${API_BASE}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: currentQuery,
          domain: domainFilter
        })
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || 'Query resolution failed');

      const botMsg = {
        sender: 'bot',
        content: data.answer,
        intent: data.intent,
        resolution_path: data.resolution_path,
        confidence: data.confidence_score,
        confidence_level: data.confidence_level,
        citations: data.citations,
        agent_trace: data.agent_trace,
        filtered_out_count: data.filtered_out_count,
        total_latency_ms: data.total_latency_ms,
        needs_clarification: data.needs_clarification,
        clarification_options: data.clarification_options
      };

      setMessages((prev) => [...prev, botMsg]);
      setActiveTrace(data.agent_trace);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', content: `Error processing query: ${err.message}`, isError: true }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem 0', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 440px', gap: '1.5rem', height: 'calc(100vh - 140px)' }}>
        
        {/* Main Conversation Panel */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
          
          {/* Header Controls */}
          <div style={{
            padding: '1rem 1.5rem',
            borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            backgroundColor: 'rgba(15, 23, 42, 0.4)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Bot size={20} color="#6366f1" />
              <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>Multi-Agent Resolution Workspace</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', color: '#94a3b8' }}>
                <span>Domain Filter:</span>
                <select
                  value={domainFilter}
                  onChange={(e) => setDomainFilter(e.target.value)}
                  style={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #334155',
                    color: '#f8fafc',
                    borderRadius: '6px',
                    padding: '0.25rem 0.5rem',
                    fontSize: '0.8rem'
                  }}
                >
                  <option value="all">All Domains</option>
                  <option value="Cloud Infrastructure & DevOps">Cloud Infrastructure & DevOps</option>
                  <option value="Healthcare & Medical Protocols">Healthcare & Medical Protocols</option>
                </select>
              </div>
            </div>
          </div>

          {/* Messages Stream */}
          <div style={{ flex: 1, padding: '1.5rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            {messages.length === 0 ? (
              <div style={{ textAlign: 'center', margin: 'auto', color: '#64748b', maxWidth: '440px' }}>
                <Sparkles size={40} color="#6366f1" style={{ opacity: 0.5, marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.1rem', color: '#e2e8f0', fontWeight: 600 }}>Web Speech & Multi-Agent Interface</h3>
                <p style={{ fontSize: '0.85rem', marginTop: '0.5rem', lineHeight: '1.4' }}>
                  Ask questions in plain text or voice. The system classifies your query (Factual, Procedural, Comparative, Ambiguous), routes to a resolution path, and returns cited answers.
                </p>
                <div style={{ marginTop: '1rem', display: 'flex', flexWrap: 'wrap', gap: '0.4rem', justifyContent: 'center' }}>
                  <button
                    onClick={() => setQuery("What is the token expiration time in OAuth2 authentication?")}
                    style={{ fontSize: '0.75rem', padding: '0.35rem 0.55rem', borderRadius: '6px', backgroundColor: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.2)', color: '#818cf8', cursor: 'pointer' }}
                  >
                    Factual: OAuth2 Expiration
                  </button>
                  <button
                    onClick={() => setQuery("What are the automated rollback triggers during production deployment?")}
                    style={{ fontSize: '0.75rem', padding: '0.35rem 0.55rem', borderRadius: '6px', backgroundColor: 'rgba(6, 182, 212, 0.1)', border: '1px solid rgba(6, 182, 212, 0.2)', color: '#22d3ee', cursor: 'pointer' }}
                  >
                    Procedural: Rollback Steps
                  </button>
                  <button
                    onClick={() => setQuery("Compare AWS EC2 compute cost versus GCP GKE compute cost.")}
                    style={{ fontSize: '0.75rem', padding: '0.35rem 0.55rem', borderRadius: '6px', backgroundColor: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.2)', color: '#fbbf24', cursor: 'pointer' }}
                  >
                    Comparative: AWS vs GCP
                  </button>
                </div>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  style={{
                    display: 'flex',
                    gap: '0.85rem',
                    justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start'
                  }}
                >
                  {msg.sender === 'bot' && (
                    <div style={{
                      width: '34px',
                      height: '34px',
                      borderRadius: '50%',
                      backgroundColor: 'rgba(99, 102, 241, 0.2)',
                      border: '1px solid rgba(99, 102, 241, 0.4)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      <Bot size={18} color="#818cf8" />
                    </div>
                  )}

                  <div style={{
                    maxWidth: '82%',
                    padding: '1rem',
                    borderRadius: '12px',
                    backgroundColor: msg.sender === 'user' ? '#4f46e5' : 'rgba(30, 41, 59, 0.9)',
                    border: msg.sender === 'user' ? 'none' : '1px solid rgba(255, 255, 255, 0.08)',
                    color: '#f8fafc',
                    fontSize: '0.9rem',
                    lineHeight: '1.5'
                  }}>
                    {msg.sender === 'bot' && (
                      <div style={{ marginBottom: '0.65rem', paddingBottom: '0.5rem', borderBottom: '1px solid rgba(255, 255, 255, 0.06)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
                            {/* Intent Badge */}
                            <span style={{
                              fontSize: '0.7rem',
                              fontWeight: 700,
                              padding: '0.15rem 0.5rem',
                              borderRadius: '4px',
                              backgroundColor: msg.intent === 'Factual' ? 'rgba(99, 102, 241, 0.2)' :
                                               msg.intent === 'Procedural' ? 'rgba(6, 182, 212, 0.2)' :
                                               msg.intent === 'Comparative' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(244, 63, 94, 0.2)',
                              color: msg.intent === 'Factual' ? '#818cf8' :
                                     msg.intent === 'Procedural' ? '#22d3ee' :
                                     msg.intent === 'Comparative' ? '#fbbf24' : '#f43f5e',
                              border: '1px solid rgba(255, 255, 255, 0.1)'
                            }}>
                              {msg.intent} Query
                            </span>

                            {/* Resolution Path Badge */}
                            <span style={{ fontSize: '0.68rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                              [{msg.resolution_path}]
                            </span>
                          </div>

                          {/* TTS Speaker */}
                          <button
                            onClick={() => speakText(msg.content)}
                            title="Read aloud using Web Speech API"
                            style={{ background: 'none', border: 'none', color: isSpeaking ? '#f43f5e' : '#94a3b8', cursor: 'pointer' }}
                          >
                            {isSpeaking ? <VolumeX size={16} /> : <Volume2 size={16} />}
                          </button>
                        </div>

                        {/* Confidence Score Bar & Metrics */}
                        {msg.confidence !== undefined && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.35rem', fontSize: '0.725rem' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                              <span style={{ color: '#94a3b8' }}>Confidence:</span>
                              <span style={{
                                fontWeight: 700,
                                color: msg.confidence_level === 'High' ? '#34d399' : msg.confidence_level === 'Medium' ? '#fbbf24' : '#f43f5e'
                              }}>
                                {(msg.confidence * 100).toFixed(0)}% ({msg.confidence_level})
                              </span>
                            </div>

                            {msg.total_latency_ms && (
                              <div style={{ display: 'flex', alignItems: 'center', gap: '0.2rem', color: '#64748b' }}>
                                <Clock size={12} />
                                {msg.total_latency_ms} ms
                              </div>
                            )}

                            {msg.filtered_out_count > 0 && (
                              <div style={{ display: 'flex', alignItems: 'center', gap: '0.2rem', color: '#f59e0b' }}>
                                <Filter size={12} />
                                Filtered {msg.filtered_out_count} low-score chunks
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )}

                    <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>

                    {/* Citations List */}
                    {msg.citations && msg.citations.length > 0 && (
                      <div style={{ marginTop: '0.75rem', paddingTop: '0.5rem', borderTop: '1px solid rgba(255, 255, 255, 0.06)' }}>
                        <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#94a3b8', display: 'block', marginBottom: '0.35rem' }}>
                          Retrieved Source Citations ({msg.citations.length}):
                        </span>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                          {msg.citations.map((c, i) => (
                            <span
                              key={i}
                              style={{
                                fontSize: '0.7rem',
                                padding: '0.2rem 0.5rem',
                                borderRadius: '4px',
                                backgroundColor: '#0f172a',
                                border: '1px solid #334155',
                                color: '#06b6d4',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.3rem'
                              }}
                            >
                              <FileText size={12} />
                              {c.filename} (Score: {(c.score * 100).toFixed(0)}%)
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {msg.sender === 'user' && (
                    <div style={{
                      width: '34px',
                      height: '34px',
                      borderRadius: '50%',
                      backgroundColor: '#6366f1',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      <User size={18} color="#fff" />
                    </div>
                  )}
                </div>
              ))
            )}

            {loading && (
              <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', color: '#94a3b8', fontSize: '0.85rem' }}>
                <Bot size={20} className="animate-spin" color="#6366f1" />
                <span>Multi-Agent Orchestrator executing sequential pipeline routing...</span>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Input & Voice Controls */}
          <form onSubmit={handleSendQuery} style={{ padding: '1rem 1.5rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', backgroundColor: 'rgba(15, 23, 42, 0.6)' }}>
            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
              
              {speechSupported && (
                <button
                  type="button"
                  onClick={toggleListening}
                  className={isListening ? 'recording-pulse' : ''}
                  title={isListening ? 'Stop listening' : 'Speak using Web Speech API STT'}
                  style={{
                    padding: '0.7rem',
                    borderRadius: '8px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    backgroundColor: isListening ? '#f43f5e' : 'rgba(30, 41, 59, 0.8)',
                    color: '#fff',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  {isListening ? <MicOff size={18} /> : <Mic size={18} />}
                </button>
              )}

              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={isListening ? 'Listening to voice input...' : 'Ask a factual, procedural, comparative, or general question...'}
                style={{
                  flex: 1,
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  color: '#f8fafc',
                  fontSize: '0.9rem',
                  outline: 'none'
                }}
              />

              <button
                type="submit"
                disabled={loading || !query.trim()}
                style={{
                  padding: '0.75rem 1.25rem',
                  borderRadius: '8px',
                  border: 'none',
                  backgroundColor: query.trim() ? '#6366f1' : '#334155',
                  color: '#fff',
                  fontWeight: 600,
                  fontSize: '0.875rem',
                  cursor: query.trim() ? 'pointer' : 'not-allowed',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem'
                }}
              >
                <Send size={16} />
                Send
              </button>
            </div>
          </form>
        </div>

        {/* Right Side: Multi-Agent Execution Trace Stream */}
        <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 600, color: '#f8fafc', marginBottom: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Sparkles size={16} color="#06b6d4" />
            Live Multi-Agent Execution Trace
          </h3>

          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {activeTrace ? (
              activeTrace.map((step, idx) => (
                <div
                  key={idx}
                  className="glass-card agent-step-active"
                  style={{ padding: '0.85rem', borderRadius: '8px' }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                    <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#06b6d4' }}>
                      {step.agent_name}
                    </span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', fontSize: '0.68rem', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                      <span>{step.latency_ms} ms</span>
                      <span>•</span>
                      <span>{step.timestamp}</span>
                    </div>
                  </div>

                  <p style={{ fontSize: '0.78rem', color: '#e2e8f0', marginBottom: '0.4rem' }}>
                    {step.action}
                  </p>

                  <div style={{ backgroundColor: '#0f172a', padding: '0.5rem', borderRadius: '4px', fontSize: '0.7rem', fontFamily: 'var(--font-mono)', color: '#94a3b8', border: '1px solid #1e293b' }}>
                    {Object.entries(step.details).map(([k, v]) => (
                      <div key={k} style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        <span style={{ color: '#818cf8' }}>{k}:</span> {typeof v === 'object' ? JSON.stringify(v) : String(v)}
                      </div>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <div style={{ textAlign: 'center', margin: 'auto', color: '#64748b', padding: '1rem' }}>
                <Bot size={32} style={{ opacity: 0.3, marginBottom: '0.5rem' }} />
                <p style={{ fontSize: '0.8rem' }}>Agent execution steps & latency telemetry will stream here live during query resolution.</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
