import React from 'react';
import {
  FileText,
  Sparkles,
  Flame,
  RotateCcw,
  TrendingUp,
  Scale,
  Award,
  CheckCircle2,
  Loader2
} from './Icons';

const WORKFLOW_STEPS = [
  { id: 'research', title: 'Research', icon: FileText, label: 'MCP Intel' },
  { id: 'round1', title: 'Debate Round 1', icon: Sparkles, label: 'Round 1', emoji: '⚔️' },
  { id: 'challenges', title: 'Cross Challenge', icon: Flame, label: 'Cross Challenge' },
  { id: 'rebuttals', title: 'Rebuttal', icon: RotateCcw, label: 'Rebuttal', emoji: '🔄' },
  { id: 'round2', title: 'Debate Round 2', icon: TrendingUp, label: 'Round 2', emoji: '⚔️' },
  { id: 'judge', title: 'AI Judge', icon: Scale, label: 'AI Judge', emoji: '⚖️' },
  { id: 'verdict', title: 'Final Verdict', icon: Award, label: 'Final Verdict', emoji: '🏆' },
];

export default function WorkflowTimeline({
  activeStage = 'all',
  onSelectStage,
  isLoading = false,
  hasEvaluation = false,
  maxRounds = 2
}) {
  return (
    <div className="workflow-stepper-container glass-card">
      <div className="stepper-header">
        <div className="stepper-title-wrap">
          <span className="live-pulse-dot" />
          <span className="stepper-title">Autonomous Multi-Agent Deliberation Pipeline</span>
        </div>
        <button
          className={`timeline-filter-btn ${activeStage === 'all' ? 'active' : ''}`}
          onClick={() => onSelectStage('all')}
        >
          View Full Timeline
        </button>
      </div>

      <div className="stepper-track">
        {WORKFLOW_STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isSelected = activeStage === step.id;
          const isDone = hasEvaluation;
          const isCurrentLoading = isLoading && idx === 1; // Visual feedback during loading

          return (
            <React.Fragment key={step.id}>
              <div
                className={`step-node ${isSelected ? 'selected' : ''} ${isDone ? 'completed' : ''} ${isLoading ? 'deliberating' : ''}`}
                onClick={() => onSelectStage(step.id)}
                title={`Click to focus: ${step.title}`}
              >
                <div className="step-icon-circle">
                  {isLoading && isSelected ? (
                    <Loader2 size={16} className="animate-spin text-accent" />
                  ) : isDone ? (
                    <CheckCircle2 size={16} color="#10b981" />
                  ) : (
                    <Icon size={16} />
                  )}
                </div>

                <div className="step-details">
                  <span className="step-number">0{idx + 1}</span>
                  <span className="step-label">
                    {step.emoji ? `${step.emoji} ` : ''}
                    {step.label}
                  </span>
                </div>
              </div>

              {idx < WORKFLOW_STEPS.length - 1 && (
                <div className={`step-connector ${isDone ? 'completed' : ''}`}>
                  <div className="connector-line" />
                  <span className="connector-arrow">↓</span>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
