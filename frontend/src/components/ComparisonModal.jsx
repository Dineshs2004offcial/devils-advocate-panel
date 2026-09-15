import React, { useState } from 'react';
import {
  Scale,
  X,
  Award,
  BarChart3,
  TrendingUp,
  DollarSign,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle
} from './Icons';

export default function ComparisonModal({
  isOpen,
  onClose,
  evaluations = [],
  currentEvaluationId,
}) {
  const [leftId, setLeftId] = useState(
    currentEvaluationId || (evaluations[0] ? evaluations[0].id : '')
  );
  const [rightId, setRightId] = useState(
    evaluations[1] ? evaluations[1].id : evaluations[0] ? evaluations[0].id : ''
  );

  if (!isOpen) return null;

  const leftItem = evaluations.find((e) => e.id === leftId) || evaluations[0];
  const rightItem = evaluations.find((e) => e.id === rightId) || evaluations[1] || evaluations[0];

  const extractMetrics = (entry) => {
    if (!entry) return null;
    const data = entry.data?.evaluation || entry.data?.result || entry.data || {};
    const name = entry.startup_name || data.startup_name || 'Startup';
    const judge = data.judge || {};
    const verdict = judge.verdict || entry.verdict || 'REVIEW';
    const score = judge.score ?? entry.score ?? 70;
    const strengths = judge.strengths || [];
    const weaknesses = judge.weaknesses || [];
    const recommendation = judge.recommendation || '';

    return {
      name,
      verdict,
      score,
      strengths,
      weaknesses,
      recommendation,
      pitch: data.pitch || {},
    };
  };

  const left = extractMetrics(leftItem);
  const right = extractMetrics(rightItem);

  const getTagClass = (v) => {
    const s = String(v).toUpperCase();
    if (s.includes('INVEST')) return 'badge-tag-invest';
    if (s.includes('REJECT')) return 'badge-tag-reject';
    return 'badge-tag-review';
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-box modal-xl" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <div className="modal-title-wrap">
            <Scale size={22} color="#818cf8" />
            <div>
              <h3>Startup Pitch Benchmark Matrix</h3>
              <span>Side-by-side comparative analysis of AI panel deliberations</span>
            </div>
          </div>
          <button className="btn-ghost-sm" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {/* Selectors */}
        <div className="comparison-selectors-row">
          <div className="selector-col">
            <label>Left Evaluation:</label>
            <select value={leftId} onChange={(e) => setLeftId(e.target.value)}>
              {evaluations.map((e) => (
                <option key={e.id} value={e.id}>
                  {e.startup_name} ({e.verdict || 'REVIEW'} - {e.score || 70}pts)
                </option>
              ))}
            </select>
          </div>

          <div className="vs-divider-badge">VS</div>

          <div className="selector-col">
            <label>Right Evaluation:</label>
            <select value={rightId} onChange={(e) => setRightId(e.target.value)}>
              {evaluations.map((e) => (
                <option key={e.id} value={e.id}>
                  {e.startup_name} ({e.verdict || 'REVIEW'} - {e.score || 70}pts)
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Comparison Matrix */}
        <div className="modal-scroll-body">
          {left && right ? (
            <div className="comparison-grid">
              {/* Left Column */}
              <div className="comparison-card glass-panel">
                <div className="comp-card-header">
                  <h4>{left.name}</h4>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <span className={`badge-tag ${getTagClass(left.verdict)}`}>
                      {left.verdict}
                    </span>
                    <span className="comp-score-pill">{left.score}/100</span>
                  </div>
                </div>

                <div className="comp-metric-row">
                  <span className="metric-label">Problem Solved:</span>
                  <p>{left.pitch.problem || 'N/A'}</p>
                </div>

                <div className="comp-metric-row">
                  <span className="metric-label">Target Market:</span>
                  <p>{left.pitch.target_market || 'N/A'}</p>
                </div>

                <div className="comp-metric-row">
                  <span className="metric-label">Key Strengths:</span>
                  <ul>
                    {left.strengths.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>

                <div className="comp-metric-row">
                  <span className="metric-label">Critical Weaknesses:</span>
                  <ul>
                    {left.weaknesses.map((w, i) => (
                      <li key={i}>{w}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Right Column */}
              <div className="comparison-card glass-panel">
                <div className="comp-card-header">
                  <h4>{right.name}</h4>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <span className={`badge-tag ${getTagClass(right.verdict)}`}>
                      {right.verdict}
                    </span>
                    <span className="comp-score-pill">{right.score}/100</span>
                  </div>
                </div>

                <div className="comp-metric-row">
                  <span className="metric-label">Problem Solved:</span>
                  <p>{right.pitch.problem || 'N/A'}</p>
                </div>

                <div className="comp-metric-row">
                  <span className="metric-label">Target Market:</span>
                  <p>{right.pitch.target_market || 'N/A'}</p>
                </div>

                <div className="comp-metric-row">
                  <span className="metric-label">Key Strengths:</span>
                  <ul>
                    {right.strengths.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>

                <div className="comp-metric-row">
                  <span className="metric-label">Critical Weaknesses:</span>
                  <ul>
                    {right.weaknesses.map((w, i) => (
                      <li key={i}>{w}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            <div className="sidebar-empty-state">
              <p>Need at least 2 evaluations to compare. Run another evaluation first!</p>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>
            Close Comparison
          </button>
        </div>
      </div>
    </div>
  );
}
