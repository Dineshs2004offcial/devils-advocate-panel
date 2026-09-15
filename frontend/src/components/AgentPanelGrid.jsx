import React, { useState } from 'react';
import {
  Flame,
  DollarSign,
  TrendingUp,
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  RotateCcw,
  Zap
} from './Icons';

const AGENTS_META = {
  vc: {
    key: 'vc',
    title: 'Skeptical VC',
    role: 'Devil’s Advocate & Defensibility',
    icon: Flame,
    color: '#f43f5e',
    badgeClass: 'badge-rose',
    defaultRisk: 'High Risk',
    riskScore: 82,
    riskClass: 'risk-high',
  },
  financial: {
    key: 'financial',
    title: 'Financial Analyst',
    role: 'Unit Economics & Capital Runway',
    icon: DollarSign,
    color: '#10b981',
    badgeClass: 'badge-emerald',
    defaultRisk: 'Moderate Risk',
    riskScore: 60,
    riskClass: 'risk-moderate',
  },
  market: {
    key: 'market',
    title: 'Market Realist',
    role: 'Customer Demand & Moat Feasibility',
    icon: TrendingUp,
    color: '#38bdf8',
    badgeClass: 'badge-sky',
    defaultRisk: 'Moderate Risk',
    riskScore: 52,
    riskClass: 'risk-moderate',
  },
};

function AgentCard({
  agentKey,
  analysisData,
  challenges = [],
  rebuttals = [],
  roundNumber = 1,
}) {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(true);

  const meta = AGENTS_META[agentKey] || AGENTS_META.market;
  const IconComponent = meta.icon;

  const data = analysisData || {};
  const persona = data.persona || meta.title;
  const argumentText = data.argument || data.analysis || (typeof data === 'string' ? data : 'Analysis pending.');
  const strengths = Array.isArray(data.strengths) ? data.strengths : [];
  const weaknesses = Array.isArray(data.weaknesses) ? data.weaknesses : [];
  const risks = Array.isArray(data.risks) ? data.risks : [];
  const questions = Array.isArray(data.questions) ? data.questions : [];

  // Filter challenges related to this agent
  const agentChallenges = challenges.filter(
    (c) =>
      (c.from && c.from.toLowerCase().includes(agentKey)) ||
      (c.to && c.to.toLowerCase().includes(agentKey)) ||
      (c.target_agent && c.target_agent.toLowerCase().includes(agentKey))
  );

  // Filter rebuttals related to this agent
  const agentRebuttals = rebuttals.filter(
    (r) =>
      (r.persona && r.persona.toLowerCase().includes(agentKey)) ||
      (r.agent && r.agent.toLowerCase().includes(agentKey))
  );

  // Risk computation
  let riskLevel = 'Moderate';
  let riskScore = 55;
  let riskClass = 'risk-moderate';
  if (risks.length >= 2 || agentKey === 'vc') {
    riskLevel = 'Elevated';
    riskScore = 78;
    riskClass = 'risk-high';
  } else if (weaknesses.length === 0 && strengths.length > 2) {
    riskLevel = 'Low';
    riskScore = 30;
    riskClass = 'risk-low';
  }

  const handleCopy = () => {
    const text = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const paragraphs = typeof argumentText === 'string'
    ? argumentText.split('\n').filter((p) => p.trim().length > 0)
    : [];

  return (
    <div
      className="agent-deliberation-card glass-panel"
      style={{ '--agent-accent': meta.color }}
    >
      {/* Top Header */}
      <div className="agent-card-topbar">
        <div className="agent-identity">
          <div className="agent-icon-badge" style={{ backgroundColor: `${meta.color}18`, borderColor: `${meta.color}40` }}>
            <IconComponent size={20} color={meta.color} />
          </div>
          <div>
            <div className="agent-title-row">
              <h3>{persona}</h3>
              <span className={`status-pill ${meta.badgeClass}`}>Active Deliberation</span>
            </div>
            <span className="agent-role-sub">{meta.role}</span>
          </div>
        </div>

        <div className="agent-card-controls">
          <button
            className="btn-tiny"
            onClick={handleCopy}
            title="Copy Agent Brief"
          >
            {copied ? <Check size={13} color="#10b981" /> : <Copy size={13} />}
          </button>
          <button
            className="btn-tiny"
            onClick={() => setExpanded(!expanded)}
            title={expanded ? "Collapse" : "Expand"}
          >
            {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </button>
        </div>
      </div>

      {/* Risk Meter Indicator */}
      <div className="agent-risk-strip">
        <div className="risk-label-group">
          <span className="risk-text-label">Agent Risk Assessment:</span>
          <span className={`risk-level-tag ${riskClass}`}>{riskLevel} ({riskScore}%)</span>
        </div>
        <div className="risk-track-bar">
          <div
            className={`risk-fill ${riskClass}`}
            style={{ width: `${riskScore}%` }}
          />
        </div>
      </div>

      {expanded && (
        <div className="agent-card-body">
          {/* Analysis Thesis */}
          <div className="agent-thesis-section">
            <span className="section-mini-heading">Deliberation Stance & Core Argument</span>
            <div className="thesis-text-box">
              {paragraphs.map((p, i) => (
                <p key={i}>{p.replace(/^###?\s*/, '')}</p>
              ))}
            </div>
          </div>

          {/* Strengths / Weaknesses / Risks */}
          {(strengths.length > 0 || weaknesses.length > 0 || risks.length > 0) && (
            <div className="agent-points-grid">
              {strengths.length > 0 && (
                <div className="point-box point-strength">
                  <div className="point-header">
                    <CheckCircle2 size={14} color="#10b981" />
                    <span>Moat Strengths</span>
                  </div>
                  <ul>
                    {strengths.map((s, idx) => (
                      <li key={idx}>{s}</li>
                    ))}
                  </ul>
                </div>
              )}

              {weaknesses.length > 0 && (
                <div className="point-box point-weakness">
                  <div className="point-header">
                    <AlertTriangle size={14} color="#f59e0b" />
                    <span>Critiques & Gaps</span>
                  </div>
                  <ul>
                    {weaknesses.map((w, idx) => (
                      <li key={idx}>{w}</li>
                    ))}
                  </ul>
                </div>
              )}

              {risks.length > 0 && (
                <div className="point-box point-risk">
                  <div className="point-header">
                    <ShieldAlert size={14} color="#f43f5e" />
                    <span>Identified Risks</span>
                  </div>
                  <ul>
                    {risks.map((r, idx) => (
                      <li key={idx}>{r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Peer Cross-Challenges */}
          {agentChallenges.length > 0 && (
            <div className="agent-dispute-section">
              <span className="section-mini-heading">⚔️ Cross Challenges</span>
              <div className="dispute-list">
                {agentChallenges.map((c, i) => (
                  <div key={i} className="dispute-pill">
                    <div className="dispute-meta">
                      <span className="dispute-from">{c.from || 'Agent'}</span>
                      <span className="dispute-arrow">→</span>
                      <span className="dispute-to">{c.target_agent || c.to || 'Peer'}</span>
                    </div>
                    <p className="dispute-text">{c.challenge}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Rebuttal / Defense */}
          {agentRebuttals.length > 0 && (
            <div className="agent-rebuttal-section">
              <span className="section-mini-heading">🔄 Rebuttal & Position Defense</span>
              <div className="rebuttal-items">
                {agentRebuttals.map((r, i) => (
                  <div key={i} className="rebuttal-box">
                    <p className="rebuttal-quote">"{r.rebuttal}"</p>
                    {r.revised_position && (
                      <div className="revised-stance">
                        <strong>Revised Posture:</strong> {r.revised_position}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Questions for founders */}
          {questions.length > 0 && (
            <div className="agent-questions-section">
              <span className="section-mini-heading">Investor Diligence Question:</span>
              <ul className="questions-list">
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

export default function AgentPanelGrid({
  round1Data = {},
  round2Data = {},
  challenges = [],
  rebuttals = [],
  activeRound = 2,
}) {
  const activeData = activeRound === 1 ? round1Data : round2Data || round1Data;

  const vcData = activeData.vc || activeData.devils_advocate || {};
  const financialData = activeData.financial || activeData.financial_analysis || {};
  const marketData = activeData.market || activeData.market_analysis || {};

  return (
    <div className="agent-panel-grid">
      <AgentCard
        agentKey="vc"
        analysisData={vcData}
        challenges={challenges}
        rebuttals={rebuttals}
        roundNumber={activeRound}
      />
      <AgentCard
        agentKey="financial"
        analysisData={financialData}
        challenges={challenges}
        rebuttals={rebuttals}
        roundNumber={activeRound}
      />
      <AgentCard
        agentKey="market"
        analysisData={marketData}
        challenges={challenges}
        rebuttals={rebuttals}
        roundNumber={activeRound}
      />
    </div>
  );
}
