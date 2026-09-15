import React, { useState } from 'react';
import {
  FileText,
  X,
  Copy,
  Check,
  Download,
  Flame,
  DollarSign,
  TrendingUp,
  Award,
  Sparkles
} from './Icons';

export default function TranscriptModal({
  isOpen,
  onClose,
  evaluationData,
}) {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !evaluationData) return null;

  const evaluation = evaluationData.evaluation || evaluationData.result || evaluationData;
  const name = evaluationData.startup_name || evaluation?.startup_name || 'Startup Pitch';
  const pitch = evaluation?.pitch || {};
  const research = evaluation?.research || {};
  const round1 = evaluation?.round_1 || {};
  const challenges = evaluation?.challenges || [];
  const rebuttals = evaluation?.rebuttals || [];
  const round2 = evaluation?.round_2 || {};
  const judge = evaluation?.judge || {};
  const verdict = evaluation?.final_verdict || judge?.overall_assessment || '';

  const getFullMarkdown = () => {
    let md = `# DEVIL'S ADVOCATE PANEL: FULL TRANSCRIPT\n`;
    md += `Target Startup: ${name}\n`;
    md += `Date: ${new Date().toLocaleString()}\n\n`;

    md += `## 1. STARTUP BLUEPRINT\n`;
    md += `- Name: ${name}\n`;
    md += `- Problem: ${pitch.problem || 'N/A'}\n`;
    md += `- Solution: ${pitch.solution || 'N/A'}\n`;
    md += `- Target Market: ${pitch.target_market || 'N/A'}\n`;
    md += `- Business Model: ${pitch.business_model || 'N/A'}\n`;
    md += `- Funding Target: $${pitch.funding_amount || 'N/A'}\n\n`;

    if (research.summary) {
      md += `## 2. MCP MARKET RESEARCH\n${research.summary}\n\n`;
    }

    md += `## 3. ROUND 1: INDEPENDENT ANALYSIS\n`;
    if (round1.vc) md += `### Skeptical VC\n${round1.vc.argument || round1.vc.analysis || ''}\n\n`;
    if (round1.financial) md += `### Financial Analyst\n${round1.financial.argument || round1.financial.analysis || ''}\n\n`;
    if (round1.market) md += `### Market Realist\n${round1.market.argument || round1.market.analysis || ''}\n\n`;

    if (challenges.length > 0) {
      md += `## 4. CROSS CHALLENGES\n`;
      challenges.forEach((c) => {
        md += `- [${c.from} → ${c.target_agent || c.to}]: ${c.challenge}\n`;
      });
      md += `\n`;
    }

    if (rebuttals.length > 0) {
      md += `## 5. AGENT REBUTTALS\n`;
      rebuttals.forEach((r) => {
        md += `- [${r.persona || r.agent}]: ${r.rebuttal}\n`;
        if (r.revised_position) md += `  Revised Posture: ${r.revised_position}\n`;
      });
      md += `\n`;
    }

    if (round2.vc || round2.financial || round2.market) {
      md += `## 6. ROUND 2: SYNTHESIZED POSITIONS\n`;
      if (round2.vc) md += `### Skeptical VC\n${round2.vc.argument || round2.vc.analysis || ''}\n\n`;
      if (round2.financial) md += `### Financial Analyst\n${round2.financial.argument || round2.financial.analysis || ''}\n\n`;
      if (round2.market) md += `### Market Realist\n${round2.market.argument || round2.market.analysis || ''}\n\n`;
    }

    md += `## 7. AI LEAD JUDGE ARBITRATION\n`;
    md += `Verdict: ${judge.verdict || 'REVIEW'}\n`;
    md += `Overall Score: ${judge.score ?? 70}/100\n`;
    md += `Assessment: ${judge.overall_assessment || verdict}\n`;
    if (judge.recommendation) md += `Recommendations: ${judge.recommendation}\n`;

    return md;
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(getFullMarkdown());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([getFullMarkdown()], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${name.replace(/\s+/g, '_')}_Transcript.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-box modal-lg" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-wrap">
            <FileText size={20} color="#818cf8" />
            <div>
              <h3>Debate Transcript & Audit Log</h3>
              <span>{name} • Complete LangGraph Multi-Agent Record</span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button className="btn-toolbar" onClick={handleCopy}>
              {copied ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
            <button className="btn-toolbar" onClick={handleDownload}>
              <Download size={14} />
              <span>Export .MD</span>
            </button>
            <button className="btn-ghost-sm" onClick={onClose}>
              <X size={18} />
            </button>
          </div>
        </div>

        <div className="modal-scroll-body transcript-content">
          {/* Section: Pitch */}
          <div className="transcript-section">
            <h4 className="transcript-section-title">1. Startup Blueprint</h4>
            <div className="transcript-card">
              <p><strong>Startup Name:</strong> {name}</p>
              <p><strong>Problem:</strong> {pitch.problem || 'N/A'}</p>
              <p><strong>Solution:</strong> {pitch.solution || 'N/A'}</p>
              <p><strong>Target Market:</strong> {pitch.target_market || 'N/A'}</p>
              <p><strong>Business Model:</strong> {pitch.business_model || 'N/A'}</p>
              <p><strong>Funding:</strong> ${pitch.funding_amount || 'N/A'}</p>
            </div>
          </div>

          {/* Section: Research */}
          {research.summary && (
            <div className="transcript-section">
              <h4 className="transcript-section-title">2. MCP Intelligence Gathering</h4>
              <div className="transcript-card">
                <p>{research.summary}</p>
              </div>
            </div>
          )}

          {/* Section: Round 1 */}
          <div className="transcript-section">
            <h4 className="transcript-section-title">3. Round 1: Independent Agent Analyses</h4>
            <div className="transcript-grid">
              {round1.vc && (
                <div className="transcript-card border-rose">
                  <strong className="text-rose">Skeptical VC:</strong>
                  <p>{round1.vc.argument || round1.vc.analysis || ''}</p>
                </div>
              )}
              {round1.financial && (
                <div className="transcript-card border-emerald">
                  <strong className="text-emerald">Financial Analyst:</strong>
                  <p>{round1.financial.argument || round1.financial.analysis || ''}</p>
                </div>
              )}
              {round1.market && (
                <div className="transcript-card border-sky">
                  <strong className="text-sky">Market Realist:</strong>
                  <p>{round1.market.argument || round1.market.analysis || ''}</p>
                </div>
              )}
            </div>
          </div>

          {/* Section: Challenges */}
          {challenges.length > 0 && (
            <div className="transcript-section">
              <h4 className="transcript-section-title">4. Peer Cross-Challenges</h4>
              <div className="transcript-card">
                {challenges.map((c, i) => (
                  <div key={i} className="transcript-bullet">
                    <span className="bullet-tag">[{c.from} → {c.target_agent || c.to}]</span>
                    <span>{c.challenge}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Section: Rebuttals */}
          {rebuttals.length > 0 && (
            <div className="transcript-section">
              <h4 className="transcript-section-title">5. Agent Rebuttals & Stance Revisions</h4>
              <div className="transcript-card">
                {rebuttals.map((r, i) => (
                  <div key={i} className="transcript-bullet">
                    <span className="bullet-tag">[{r.persona || r.agent}]</span>
                    <span>{r.rebuttal}</span>
                    {r.revised_position && (
                      <div style={{ marginTop: '4px', color: '#94a3b8', fontSize: '0.85rem' }}>
                        ↳ <em>Revised: {r.revised_position}</em>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Section: Judge */}
          <div className="transcript-section">
            <h4 className="transcript-section-title">6. Final AI Lead Judge Arbitration</h4>
            <div className="transcript-card border-indigo">
              <p><strong>Verdict:</strong> {judge.verdict || 'REVIEW'}</p>
              <p><strong>Score:</strong> {judge.score ?? 70}/100</p>
              <p><strong>Assessment:</strong> {judge.overall_assessment || verdict}</p>
              {judge.recommendation && (
                <p><strong>Recommendation:</strong> {judge.recommendation}</p>
              )}
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
