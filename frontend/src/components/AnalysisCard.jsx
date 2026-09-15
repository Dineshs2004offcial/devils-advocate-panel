import React, { useState } from 'react';
import { Copy, Check, TrendingUp, DollarSign, Flame, ChevronDown, ChevronUp, CheckCircle2, AlertTriangle, ShieldAlert } from './Icons';

const CARD_STYLES = {
  market: {
    title: 'Market Realist',
    icon: TrendingUp,
    color: '#3b82f6',
    borderClass: 'border-blue',
    badge: 'Market & Customer Demand',
    badgeClass: 'badge-blue',
  },
  financial: {
    title: 'Financial Analyst',
    icon: DollarSign,
    color: '#10b981',
    borderClass: 'border-emerald',
    badge: 'Unit Economics & Runway',
    badgeClass: 'badge-emerald',
  },
  devil: {
    title: 'Skeptical VC / Devil’s Advocate',
    icon: Flame,
    color: '#ef4444',
    borderClass: 'border-red',
    badge: 'Defensibility & Blindspots',
    badgeClass: 'badge-red',
  },
  vc: {
    title: 'Skeptical VC / Devil’s Advocate',
    icon: Flame,
    color: '#ef4444',
    borderClass: 'border-red',
    badge: 'Defensibility & Moat',
    badgeClass: 'badge-red',
  },
};

export default function AnalysisCard({ type = 'market', data, round = 1, isExpandedDefault = true }) {
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(isExpandedDefault);

  const style = CARD_STYLES[type] || CARD_STYLES.market;
  const IconComponent = style.icon;

  const isObject = typeof data === 'object' && data !== null;
  const persona = isObject ? (data.persona || style.title) : style.title;
  const argument = isObject ? (data.argument || data.analysis || JSON.stringify(data)) : (typeof data === 'string' ? data : 'No analysis provided.');
  const strengths = isObject && Array.isArray(data.strengths) ? data.strengths : [];
  const weaknesses = isObject && Array.isArray(data.weaknesses) ? data.weaknesses : [];
  const risks = isObject && Array.isArray(data.risks) ? data.risks : [];
  const questions = isObject && Array.isArray(data.questions) ? data.questions : [];

  const handleCopy = () => {
    const copyText = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    navigator.clipboard.writeText(copyText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formattedLines = typeof argument === 'string' ? argument.split('\n').filter((line) => line.trim().length > 0) : [];

  return (
    <div
      className="glass-panel agent-debate-card"
      style={{
        borderTop: `3px solid ${style.color}`,
      }}
    >
      {/* Header */}
      <div className="agent-card-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            className="agent-icon-wrap"
            style={{
              backgroundColor: `${style.color}15`,
              borderColor: `${style.color}40`,
            }}
          >
            <IconComponent size={18} color={style.color} />
          </div>
          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc' }}>
              {persona}
            </h3>
            <div style={{ display: 'flex', gap: '6px', marginTop: '3px' }}>
              <span className={`badge ${style.badgeClass}`}>
                {style.badge}
              </span>
              {round && (
                <span className="badge badge-subtle">
                  Round {round}
                </span>
              )}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <button
            type="button"
            onClick={handleCopy}
            className="btn btn-secondary"
            title="Copy Analysis"
            style={{ padding: '6px 10px', fontSize: '0.8rem' }}
          >
            {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
            <span style={{ fontSize: '0.75rem' }}>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="btn btn-secondary"
            style={{ padding: '6px 8px' }}
          >
            {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
        </div>
      </div>

      {/* Content Area */}
      {isExpanded && (
        <div className="agent-card-content">
          {/* Main argument */}
          <div className="agent-argument-box">
            {formattedLines.map((line, index) => (
              <p key={index} style={{ marginBottom: '8px' }}>
                {line.replace(/^###?\s*/, '')}
              </p>
            ))}
          </div>

          {/* Structured highlights if present */}
          {(strengths.length > 0 || weaknesses.length > 0 || risks.length > 0) && (
            <div className="agent-highlights-grid">
              {strengths.length > 0 && (
                <div className="agent-highlight-group">
                  <div className="agent-highlight-title" style={{ color: '#10b981' }}>
                    <CheckCircle2 size={14} color="#10b981" /> Strengths
                  </div>
                  <ul>
                    {strengths.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              )}

              {weaknesses.length > 0 && (
                <div className="agent-highlight-group">
                  <div className="agent-highlight-title" style={{ color: '#f59e0b' }}>
                    <AlertTriangle size={14} color="#f59e0b" /> Weaknesses
                  </div>
                  <ul>
                    {weaknesses.map((w, i) => (
                      <li key={i}>{w}</li>
                    ))}
                  </ul>
                </div>
              )}

              {risks.length > 0 && (
                <div className="agent-highlight-group">
                  <div className="agent-highlight-title" style={{ color: '#ef4444' }}>
                    <ShieldAlert size={14} color="#ef4444" /> Risks
                  </div>
                  <ul>
                    {risks.map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {questions.length > 0 && (
            <div className="agent-questions-box">
              <strong>Key Question for Founders:</strong>
              <ul>
                {questions.map((q, i) => (
                  <li key={i}>{q}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
