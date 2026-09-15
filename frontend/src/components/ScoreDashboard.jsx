import React, { useState } from 'react';
import {
  Award,
  BarChart3,
  TrendingUp,
  DollarSign,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  Download,
  Bookmark,
  FileText,
  Scale,
  Sparkles,
  Check
} from './Icons';

export default function ScoreDashboard({
  judgeData = {},
  finalVerdictText = '',
  startupName = 'Startup',
  onDownloadPdf,
  onSaveEvaluation,
  onViewTranscript,
  onOpenCompare,
  isSaved = false,
}) {
  const [justSaved, setJustSaved] = useState(false);

  const judge = judgeData || {};
  const verdictRaw = (
    judge.verdict ||
    (typeof finalVerdictText === 'string' && finalVerdictText.includes('INVEST')
      ? 'INVEST'
      : typeof finalVerdictText === 'string' && finalVerdictText.includes('REJECT')
      ? 'REJECT'
      : 'REVIEW')
  ).toUpperCase();

  const isInvest = verdictRaw.includes('INVEST') && !verdictRaw.includes('REJECT');
  const isReject = verdictRaw.includes('REJECT');
  const verdict = isInvest ? 'INVEST' : isReject ? 'REJECT' : 'REVIEW';

  const overallScore = Number(judge.score ?? judge.overall_score ?? 72);
  const marketScore = Number(judge.market_score ?? Math.min(100, Math.round(overallScore * 1.05)));
  const financialScore = Number(judge.financial_score ?? Math.max(40, Math.round(overallScore * 0.92)));
  const riskScore = Number(judge.risk_score ?? Math.max(35, 100 - overallScore + 15));

  const strengths = Array.isArray(judge.strengths) ? judge.strengths : [];
  const weaknesses = Array.isArray(judge.weaknesses) ? judge.weaknesses : [];
  const risks = Array.isArray(judge.risks) ? judge.risks : [];
  const recommendations = judge.recommendation || judge.recommendations || '';
  const assessment = judge.overall_assessment || finalVerdictText || 'Evaluation synthesis completed.';

  const handleSaveClick = () => {
    onSaveEvaluation();
    setJustSaved(true);
    setTimeout(() => setJustSaved(false), 2500);
  };

  const getVerdictTheme = () => {
    if (verdict === 'INVEST') {
      return {
        badgeBg: 'rgba(16, 185, 129, 0.15)',
        badgeBorder: 'rgba(16, 185, 129, 0.4)',
        textColor: '#10b981',
        title: 'CONSENSUS: INVEST',
        desc: 'High conviction investment thesis. Defensible moat with favorable unit economics.',
      };
    }
    if (verdict === 'REJECT') {
      return {
        badgeBg: 'rgba(244, 63, 94, 0.15)',
        badgeBorder: 'rgba(244, 63, 94, 0.4)',
        textColor: '#f43f5e',
        title: 'CONSENSUS: REJECT',
        desc: 'Critical fatal flaws in CAC, moat defensibility, or existential margin erosion identified.',
      };
    }
    return {
      badgeBg: 'rgba(245, 158, 11, 0.15)',
      badgeBorder: 'rgba(245, 158, 11, 0.4)',
      textColor: '#f59e0b',
      title: 'CONSENSUS: FURTHER REVIEW',
      desc: 'Promising market demand, but key financial or customer acquisition risks require founder diligence.',
    };
  };

  const theme = getVerdictTheme();

  return (
    <div className="score-dashboard-container glass-card">
      {/* Top Banner with Verdict & Action Toolbar */}
      <div className="score-top-banner">
        <div className="verdict-main-callout">
          <div
            className="verdict-pill-giant"
            style={{
              backgroundColor: theme.badgeBg,
              borderColor: theme.badgeBorder,
              color: theme.textColor,
            }}
          >
            <Award size={26} color={theme.textColor} />
            <div>
              <span className="verdict-label-sub">AI LEAD JUDGE VERDICT</span>
              <h2 className="verdict-heading">{theme.title}</h2>
            </div>
          </div>
          <p className="verdict-sub-desc">{theme.desc}</p>
        </div>

        {/* Action Toolbar */}
        <div className="dashboard-action-toolbar">
          <button
            className="btn-toolbar btn-save"
            onClick={handleSaveClick}
            title="Save Evaluation"
          >
            {justSaved || isSaved ? <Check size={15} color="#10b981" /> : <Bookmark size={15} />}
            <span>{justSaved ? 'Saved!' : isSaved ? 'Saved' : 'Save'}</span>
          </button>

          <button
            className="btn-toolbar btn-pdf"
            onClick={onDownloadPdf}
            title="Export PDF Dossier"
          >
            <Download size={15} />
            <span>Download PDF</span>
          </button>

          <button
            className="btn-toolbar btn-transcript"
            onClick={onViewTranscript}
            title="View Full Transcript"
          >
            <FileText size={15} />
            <span>Transcript</span>
          </button>

          <button
            className="btn-toolbar btn-compare"
            onClick={onOpenCompare}
            title="Compare with other pitches"
          >
            <Scale size={15} />
            <span>Compare</span>
          </button>
        </div>
      </div>

      {/* 4 Score Metrics Grid */}
      <div className="scores-metrics-grid">
        {/* Overall Score */}
        <div className="score-metric-box metric-overall">
          <div className="metric-header">
            <BarChart3 size={18} color="#818cf8" />
            <span>Overall Score</span>
          </div>
          <div className="metric-body">
            <span className="metric-number text-indigo">{overallScore}</span>
            <span className="metric-total">/100</span>
          </div>
          <div className="metric-progress-bar">
            <div
              className="progress-fill bg-indigo"
              style={{ width: `${overallScore}%` }}
            />
          </div>
        </div>

        {/* Market Score */}
        <div className="score-metric-box metric-market">
          <div className="metric-header">
            <TrendingUp size={18} color="#38bdf8" />
            <span>Market Demand</span>
          </div>
          <div className="metric-body">
            <span className="metric-number text-sky">{marketScore}</span>
            <span className="metric-total">/100</span>
          </div>
          <div className="metric-progress-bar">
            <div
              className="progress-fill bg-sky"
              style={{ width: `${marketScore}%` }}
            />
          </div>
        </div>

        {/* Financial Score */}
        <div className="score-metric-box metric-financial">
          <div className="metric-header">
            <DollarSign size={18} color="#10b981" />
            <span>Financial Viability</span>
          </div>
          <div className="metric-body">
            <span className="metric-number text-emerald">{financialScore}</span>
            <span className="metric-total">/100</span>
          </div>
          <div className="metric-progress-bar">
            <div
              className="progress-fill bg-emerald"
              style={{ width: `${financialScore}%` }}
            />
          </div>
        </div>

        {/* Risk Score */}
        <div className="score-metric-box metric-risk">
          <div className="metric-header">
            <ShieldAlert size={18} color="#f43f5e" />
            <span>Risk & Vulnerability</span>
          </div>
          <div className="metric-body">
            <span className="metric-number text-rose">{riskScore}</span>
            <span className="metric-total">/100</span>
          </div>
          <div className="metric-progress-bar">
            <div
              className="progress-fill bg-rose"
              style={{ width: `${riskScore}%` }}
            />
          </div>
        </div>
      </div>

      {/* Synthesis & Strategic Evaluation */}
      <div className="synthesis-section">
        <div className="synthesis-header">
          <Sparkles size={16} color="#818cf8" />
          <h3>Executive Arbitrated Synthesis</h3>
        </div>
        <p className="synthesis-text">
          {typeof assessment === 'string' ? assessment : JSON.stringify(assessment)}
        </p>
      </div>

      {/* Strengths / Weaknesses / Recommendations 3-Col Grid */}
      <div className="evaluation-insights-grid">
        {/* Strengths */}
        <div className="insight-card insight-strengths">
          <div className="insight-header">
            <CheckCircle2 size={16} color="#10b981" />
            <h4>Core Strengths & Moats</h4>
          </div>
          <ul>
            {strengths.length > 0 ? (
              strengths.map((item, idx) => <li key={idx}>{item}</li>)
            ) : (
              <li>Solid product vision with addressable customer cohort</li>
            )}
          </ul>
        </div>

        {/* Weaknesses */}
        <div className="insight-card insight-weaknesses">
          <div className="insight-header">
            <AlertTriangle size={16} color="#f59e0b" />
            <h4>Critical Weaknesses</h4>
          </div>
          <ul>
            {weaknesses.length > 0 ? (
              weaknesses.map((item, idx) => <li key={idx}>{item}</li>)
            ) : (
              <li>Scalability limitations under aggressive market expansion</li>
            )}
          </ul>
        </div>

        {/* Recommendations */}
        <div className="insight-card insight-recommendations">
          <div className="insight-header">
            <Award size={16} color="#818cf8" />
            <h4>Strategic Action Plan</h4>
          </div>
          <p className="recommendations-text">
            {typeof recommendations === 'string' && recommendations
              ? recommendations
              : Array.isArray(recommendations) && recommendations.length > 0
              ? recommendations.join(' ')
              : 'Require validated unit economics CAC/LTV proof and founder IP defensibility before term sheet commitment.'}
          </p>
        </div>
      </div>
    </div>
  );
}
