import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import WorkflowTimeline from '../components/WorkflowTimeline';
import AgentPanelGrid from '../components/AgentPanelGrid';
import ScoreDashboard from '../components/ScoreDashboard';
import ChatPitchInput from '../components/ChatPitchInput';
import McpPanel from '../components/McpPanel';
import TranscriptModal from '../components/TranscriptModal';
import ComparisonModal from '../components/ComparisonModal';
import SettingsModal from '../components/SettingsModal';
import {
  evaluatePitch,
  fetchMcpStatus,
  getSavedEvaluations,
  saveEvaluationToHistory,
  renameSavedEvaluation,
  deleteSavedEvaluation,
  exportEvaluationDossier,
} from '../services/api';
import {
  Sparkles,
  Flame,
  FileText,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Cpu
} from '../components/Icons';

export default function Dashboard() {
  // Evaluation States
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [activeEvaluationId, setActiveEvaluationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('Initializing Deliberation...');
  const [error, setError] = useState('');

  // Selected debate rounds (1, 2, 3)
  const [selectedRounds, setSelectedRounds] = useState(2);

  // Workflow / Timeline stage filter ('all', 'research', 'round1', 'challenges', 'rebuttals', 'round2', 'judge', 'verdict')
  const [activeTimelineStage, setActiveTimelineStage] = useState('all');

  // History & MCP States
  const [evaluationsHistory, setEvaluationsHistory] = useState([]);
  const [mcpStatus, setMcpStatus] = useState({});

  // Collapsible panels
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mcpCollapsed, setMcpCollapsed] = useState(false);

  // Modals
  const [showTranscript, setShowTranscript] = useState(false);
  const [showCompare, setShowCompare] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  // Initial Load: Stored Evaluations & MCP Status
  useEffect(() => {
    const stored = getSavedEvaluations();
    setEvaluationsHistory(stored);
    if (stored.length > 0) {
      // Auto-load most recent evaluation if available
      setEvaluationResult(stored[0].data);
      setActiveEvaluationId(stored[0].id);
    }

    loadMcpStatus();
  }, []);

  const loadMcpStatus = async () => {
    const status = await fetchMcpStatus();
    setMcpStatus(status);
  };

  // Run Evaluation Flow
  const handleStartEvaluation = async (pitchPayload) => {
    setLoading(true);
    setError('');
    setActiveEvaluationId(null);
    setLoadingStage('MCP Web Intelligence & Benchmark Gathering...');

    // Progress simulation during LLM LangGraph execution
    const progressTimer1 = setTimeout(() => {
      setLoadingStage('⚔️ Round 1: Independent Agent Analysis (VC, Financial, Market)...');
    }, 2500);

    const progressTimer2 = setTimeout(() => {
      setLoadingStage('Adversarial Peer Cross-Challenges & Rebuttals...');
    }, 6000);

    const progressTimer3 = setTimeout(() => {
      setLoadingStage('⚖️ AI Lead Judge Arbitrating Consensus & Verdict...');
    }, 9500);

    try {
      const data = await evaluatePitch(pitchPayload, selectedRounds);
      setEvaluationResult(data);

      // Auto-persist to history
      const savedEntry = saveEvaluationToHistory(data);
      if (savedEntry) {
        setEvaluationsHistory(getSavedEvaluations());
        setActiveEvaluationId(savedEntry.id);
      }
    } catch (err) {
      console.error('Deliberation error:', err);
      setError(
        err.message || 'An error occurred during multi-agent deliberation. Please check backend status.'
      );
    } finally {
      clearTimeout(progressTimer1);
      clearTimeout(progressTimer2);
      clearTimeout(progressTimer3);
      setLoading(false);
      setLoadingStage('');
      loadMcpStatus();
    }
  };

  // History Actions
  const handleSelectRecentEvaluation = (historyItem) => {
    if (!historyItem || !historyItem.data) return;
    setEvaluationResult(historyItem.data);
    setActiveEvaluationId(historyItem.id);
    setError('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleNewEvaluation = () => {
    setEvaluationResult(null);
    setActiveEvaluationId(null);
    setError('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleRenameEvaluation = (id, newName) => {
    const updated = renameSavedEvaluation(id, newName);
    setEvaluationsHistory(updated);
    if (activeEvaluationId === id && evaluationResult) {
      setEvaluationResult({
        ...evaluationResult,
        startup_name: newName,
      });
    }
  };

  const handleDeleteEvaluation = (id) => {
    const updated = deleteSavedEvaluation(id);
    setEvaluationsHistory(updated);
    if (activeEvaluationId === id) {
      if (updated.length > 0) {
        setEvaluationResult(updated[0].data);
        setActiveEvaluationId(updated[0].id);
      } else {
        setEvaluationResult(null);
        setActiveEvaluationId(null);
      }
    }
  };

  const handleSaveCurrentEvaluation = () => {
    if (!evaluationResult) return;
    const savedEntry = saveEvaluationToHistory(evaluationResult);
    if (savedEntry) {
      setEvaluationsHistory(getSavedEvaluations());
      setActiveEvaluationId(savedEntry.id);
    }
  };

  const handleDownloadPdfDossier = () => {
    if (!evaluationResult) return;
    exportEvaluationDossier(evaluationResult);
  };

  // Data decomposition
  const evalData = evaluationResult?.evaluation || evaluationResult?.result || evaluationResult;
  const startupName = evaluationResult?.startup_name || evalData?.startup_name || 'Startup Pitch';
  const pitchInfo = evalData?.pitch || {};
  const research = evalData?.research || {};
  const round1 = evalData?.round_1 || {
    market: evalData?.market_analysis,
    financial: evalData?.financial_analysis,
    vc: evalData?.devils_advocate,
  };
  const challenges = evalData?.challenges || [];
  const rebuttals = evalData?.rebuttals || [];
  const round2 = evalData?.round_2 || round1;
  const judge = evalData?.judge || {};
  const finalVerdictText = evalData?.final_verdict || judge?.overall_assessment || '';

  return (
    <div className="app-layout">
      {/* 1. LEFT SIDEBAR */}
      <Sidebar
        evaluations={evaluationsHistory}
        activeEvaluationId={activeEvaluationId}
        onSelectEvaluation={handleSelectRecentEvaluation}
        onNewEvaluation={handleNewEvaluation}
        onRenameEvaluation={handleRenameEvaluation}
        onDeleteEvaluation={handleDeleteEvaluation}
        onOpenCompare={() => setShowCompare(true)}
        onOpenSettings={() => setShowSettings(true)}
        isCollapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* 2. MAIN WORKSPACE */}
      <main className="main-workspace">
        <div className="workspace-inner">
          {/* Header */}
          <header className="main-header">
            <div className="header-top-row">
              <div className="header-badge">
                <Flame size={14} color="#f43f5e" />
                <span>LANGGRAPH MULTI-AGENT ADVERSARIAL PANEL</span>
              </div>

              <div className="header-meta-actions">
                <button
                  className="btn-ghost-sm"
                  onClick={() => setMcpCollapsed(!mcpCollapsed)}
                  title="Toggle MCP Connectors"
                >
                  <Cpu size={14} color="#818cf8" />
                  <span>MCP Connectors</span>
                </button>
              </div>
            </div>

            <h1 className="header-title">😈 Devil's Advocate Panel</h1>
            <p className="header-subtitle">
              Pitch your idea and get challenged by AI investors. Autonomous multi-agent deliberation with real-time market intelligence.
            </p>
          </header>

          {/* Error Banner */}
          {error && (
            <div className="error-banner glass-panel">
              <AlertCircle size={20} color="#f43f5e" />
              <div className="error-text">
                <strong>Evaluation Issue:</strong>
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Loading View */}
          {loading && (
            <div className="live-deliberation-loading glass-card">
              <div className="loading-orbit">
                <div className="orbit-spinner" />
                <div className="orbit-center">
                  <Flame size={28} color="#f43f5e" />
                </div>
              </div>
              <h2 className="loading-main-text">Multi-Agent Deliberation in Progress</h2>
              <p className="loading-sub-text">{loadingStage}</p>

              <div className="loading-steps-pills">
                <div className="step-pill active">1. MCP Intel</div>
                <div className="step-arrow">→</div>
                <div className="step-pill active">2. 3-Agent Round 1</div>
                <div className="step-arrow">→</div>
                <div className="step-pill active">3. Cross Dispute</div>
                <div className="step-arrow">→</div>
                <div className="step-pill active">4. Rebuttal</div>
                <div className="step-arrow">→</div>
                <div className="step-pill active">5. Round 2</div>
                <div className="step-arrow">→</div>
                <div className="step-pill active">6. AI Judge</div>
              </div>
            </div>
          )}

          {/* Empty Waiting State */}
          {!evalData && !loading && (
            <div className="empty-workspace-state glass-card">
              <div className="empty-state-icon">
                <Flame size={36} color="#f43f5e" />
              </div>
              <h2>Ready for Startup Pitch Deliberation</h2>
              <p>
                Submit your pitch below or choose a sample pitch template to initiate the 3-agent adversarial debate loop (Skeptical VC, Financial Analyst, Market Realist) and receive an AI Lead Judge investment arbitration.
              </p>
            </div>
          )}

          {/* LIVE DEBATE & EVALUATION RESULTS VIEW */}
          {evalData && !loading && (
            <div className="deliberation-results-container">
              {/* Dynamic Workflow Timeline Stepper */}
              <WorkflowTimeline
                activeStage={activeTimelineStage}
                onSelectStage={setActiveTimelineStage}
                isLoading={loading}
                hasEvaluation={true}
                maxRounds={selectedRounds}
              />

              {/* Startup Pitch Info Header Card */}
              {pitchInfo.problem && (
                <div className="startup-overview-card glass-panel">
                  <div className="overview-title-row">
                    <span className="overview-badge">TARGET VENTURE</span>
                    <h3>{startupName}</h3>
                  </div>
                  <div className="overview-details-grid">
                    <div>
                      <strong>Problem:</strong>
                      <p>{pitchInfo.problem}</p>
                    </div>
                    <div>
                      <strong>Solution:</strong>
                      <p>{pitchInfo.solution}</p>
                    </div>
                    {pitchInfo.target_market && (
                      <div>
                        <strong>Target Market:</strong>
                        <p>{pitchInfo.target_market}</p>
                      </div>
                    )}
                    {pitchInfo.business_model && (
                      <div>
                        <strong>Business Model:</strong>
                        <p>{pitchInfo.business_model}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* 1. Score & Judge Verdict Dashboard */}
              {(activeTimelineStage === 'all' || activeTimelineStage === 'verdict' || activeTimelineStage === 'judge') && (
                <section className="deliberation-section">
                  <div className="section-label-header">
                    <span className="section-step-num">STAGE 06</span>
                    <h3>AI Lead Judge Consensus & Scorecard</h3>
                  </div>
                  <ScoreDashboard
                    judgeData={judge}
                    finalVerdictText={finalVerdictText}
                    startupName={startupName}
                    onDownloadPdf={handleDownloadPdfDossier}
                    onSaveEvaluation={handleSaveCurrentEvaluation}
                    onViewTranscript={() => setShowTranscript(true)}
                    onOpenCompare={() => setShowCompare(true)}
                    isSaved={Boolean(activeEvaluationId)}
                  />
                </section>
              )}

              {/* 2. MCP Market Intelligence Gathering */}
              {(activeTimelineStage === 'all' || activeTimelineStage === 'research') && research.summary && (
                <section className="deliberation-section">
                  <div className="section-label-header">
                    <span className="section-step-num">STAGE 01</span>
                    <h3>MCP Real-Time Market Intelligence & Knowledge Base</h3>
                  </div>
                  <div className="research-intel-box glass-panel">
                    <p className="research-summary-text">{research.summary}</p>
                    {research.sources && research.sources.length > 0 && (
                      <div className="sources-container">
                        <strong>Discovered Market Benchmarks & Intelligence Sources:</strong>
                        <ul className="sources-list">
                          {research.sources.map((src, i) => (
                            <li key={i}>
                              <a href={src} target="_blank" rel="noreferrer">
                                {src}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </section>
              )}

              {/* 3. 3-Agent Deliberation Panel Grid (Round 1 or 2) */}
              {(activeTimelineStage === 'all' || activeTimelineStage === 'round1' || activeTimelineStage === 'round2' || activeTimelineStage === 'challenges' || activeTimelineStage === 'rebuttals') && (
                <section className="deliberation-section">
                  <div className="section-label-header">
                    <span className="section-step-num">
                      {activeTimelineStage === 'round1' ? 'STAGE 02' : 'STAGE 05'}
                    </span>
                    <h3>
                      {activeTimelineStage === 'round1'
                        ? 'Debate Round 1: Independent Agent Analysis'
                        : 'Adversarial Agent Panel: Skeptical VC • Financial Analyst • Market Realist'}
                    </h3>
                  </div>
                  <AgentPanelGrid
                    round1Data={round1}
                    round2Data={round2}
                    challenges={challenges}
                    rebuttals={rebuttals}
                    activeRound={activeTimelineStage === 'round1' ? 1 : 2}
                  />
                </section>
              )}
            </div>
          )}
        </div>

        {/* 3. CHAT-STYLE BOTTOM PITCH INPUT */}
        <div className="chat-bottom-anchor">
          <ChatPitchInput
            onSubmitPitch={handleStartEvaluation}
            isLoading={loading}
            selectedRounds={selectedRounds}
            onChangeRounds={setSelectedRounds}
          />
        </div>
      </main>

      {/* 4. RIGHT COLLAPSIBLE MCP CONNECTORS PANEL */}
      <McpPanel
        mcpStatus={mcpStatus}
        isWorking={loading}
        onRefresh={loadMcpStatus}
        isCollapsed={mcpCollapsed}
        onToggleCollapse={() => setMcpCollapsed(!mcpCollapsed)}
      />

      {/* Modals */}
      <TranscriptModal
        isOpen={showTranscript}
        onClose={() => setShowTranscript(false)}
        evaluationData={evaluationResult}
      />

      <ComparisonModal
        isOpen={showCompare}
        onClose={() => setShowCompare(false)}
        evaluations={evaluationsHistory}
        currentEvaluationId={activeEvaluationId}
      />

      <SettingsModal
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
      />
    </div>
  );
}
