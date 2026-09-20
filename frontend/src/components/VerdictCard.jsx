import React, { useState } from 'react';
import { Award, CheckCircle2, AlertTriangle, ShieldAlert, Sparkles, Download, FileText, Loader2 } from './Icons';
import { downloadEvaluationPdf, exportEvaluationDossier } from '../services/api';

export default function VerdictCard({ verdict, judgeData, evaluationData }) {
  const [downloading, setDownloading] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  if (!verdict && !judgeData) return null;

  const judge = judgeData || {};
  const verdictText = (judge.verdict || (typeof verdict === 'string' && verdict.includes('INVEST') ? 'INVEST' : typeof verdict === 'string' && verdict.includes('REJECT') ? 'REJECT' : 'REVIEW')).toUpperCase();
  
  const score = judge.score ?? 70;
  const assessment = judge.overall_assessment || (typeof verdict === 'string' ? verdict : '');
  const strengths = judge.strengths || [];
  const weaknesses = judge.weaknesses || [];
  const risks = judge.risks || [];
  const recommendation = judge.recommendation || '';

  const getVerdictStyle = () => {
    if (verdictText.includes('INVEST')) {
      return {
        bg: 'rgba(16, 185, 129, 0.12)',
        border: '#10b981',
        color: '#10b981',
        label: 'RECOMMENDATION: INVEST',
        badgeClass: 'badge-emerald',
      };
    }
    if (verdictText.includes('REJECT')) {
      return {
        bg: 'rgba(239, 68, 68, 0.12)',
        border: '#ef4444',
        color: '#ef4444',
        label: 'RECOMMENDATION: REJECT',
        badgeClass: 'badge-red',
      };
    }
    return {
      bg: 'rgba(245, 158, 11, 0.12)',
      border: '#f59e0b',
      color: '#f59e0b',
      label: 'RECOMMENDATION: FURTHER REVIEW',
      badgeClass: 'badge-amber',
    };
  };

  const style = getVerdictStyle();

  const handleDownloadPdf = async () => {
    setDownloading(true);
    setDownloadSuccess(false);
    try {
      const dataToExport = evaluationData || {
        verdict: verdictText,
        score: score,
        judge: judge,
        final_verdict: assessment
      };
      await downloadEvaluationPdf(dataToExport);
      setDownloadSuccess(true);
      setTimeout(() => setDownloadSuccess(false), 4000);
    } catch (err) {
      console.error("PDF download error:", err);
      exportEvaluationDossier(evaluationData || { judge, verdict });
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="verdict-container" style={{ borderTop: `4px solid ${style.border}` }}>
      {/* Header Banner */}
      <div className="verdict-top-banner" style={{ backgroundColor: style.bg }}>
        <div className="verdict-title-group">
          <div className="verdict-icon-wrap" style={{ borderColor: style.border }}>
            <Award size={24} color={style.color} />
          </div>
          <div>
            <span className="verdict-badge" style={{ color: style.color }}>
              LEAD JUDGE FINAL VERDICT
            </span>
            <h2 className="verdict-decision" style={{ color: style.color }}>
              {verdictText}
            </h2>
          </div>
        </div>

        {/* Score Badge & Action Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button
            onClick={handleDownloadPdf}
            disabled={downloading}
            id="download-pdf-button"
            className="action-btn"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '10px 18px',
              background: style.color,
              color: '#ffffff',
              border: 'none',
              borderRadius: '8px',
              fontWeight: '600',
              fontSize: '13px',
              cursor: downloading ? 'wait' : 'pointer',
              boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
              transition: 'all 0.2s ease',
            }}
          >
            {downloading ? (
              <>
                <Loader2 size={16} className="spin" />
                <span>Compiling PDF...</span>
              </>
            ) : downloadSuccess ? (
              <>
                <CheckCircle2 size={16} color="#ffffff" />
                <span>PDF Downloaded!</span>
              </>
            ) : (
              <>
                <Download size={16} />
                <span>Export Executive PDF</span>
              </>
            )}
          </button>

          <div className="verdict-score-box">
            <span className="score-label">OVERALL SCORE</span>
            <div className="score-value">
              <span className="score-num" style={{ color: style.color }}>{score}</span>
              <span className="score-total">/100</span>
            </div>
          </div>
        </div>
      </div>

      {/* Assessment Body */}
      <div className="verdict-body">
        {assessment && (
          <div className="verdict-assessment-section">
            <h4 className="verdict-section-title">
              <Sparkles size={16} color="#3b82f6" />
              Executive Synthesis
            </h4>
            <p className="verdict-text">{assessment}</p>
          </div>
        )}

        {/* Strengths & Weaknesses Grid */}
        {(strengths.length > 0 || weaknesses.length > 0 || risks.length > 0) && (
          <div className="verdict-grid">
            {strengths.length > 0 && (
              <div className="verdict-column strengths-col">
                <h5>
                  <CheckCircle2 size={16} color="#10b981" />
                  Key Strengths
                </h5>
                <ul>
                  {strengths.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            )}

            {weaknesses.length > 0 && (
              <div className="verdict-column weaknesses-col">
                <h5>
                  <AlertTriangle size={16} color="#f59e0b" />
                  Key Weaknesses
                </h5>
                <ul>
                  {weaknesses.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            )}

            {risks.length > 0 && (
              <div className="verdict-column risks-col">
                <h5>
                  <ShieldAlert size={16} color="#ef4444" />
                  Critical Risks
                </h5>
                <ul>
                  {risks.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Strategic Recommendation */}
        {recommendation && (
          <div className="recommendation-box" style={{ borderColor: `${style.border}50` }}>
            <h5>Strategic Action Plan & Recommendation</h5>
            <p>{recommendation}</p>
          </div>
        )}
      </div>
    </div>
  );
}
