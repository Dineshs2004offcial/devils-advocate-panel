import React, { useState } from 'react';
import {
  Send,
  Sparkles,
  Sliders,
  ChevronUp,
  ChevronDown,
  Loader2,
  Zap,
  Target,
  Briefcase,
  DollarSign
} from './Icons';

const SAMPLE_PITCHES = [
  {
    name: 'MediVision AI',
    problem: 'Diagnostic radiologist shortage and severe scanning delays in regional hospitals.',
    solution: 'Real-time AI computer vision triaging scans with 99.2% acute anomaly detection.',
    target_market: 'Tier 1 & Tier 2 Hospital Networks and Outpatient Radiology Clinics.',
    business_model: 'B2B annual SaaS subscription ($45k/yr/facility) + volume-based scan tiers.',
    funding_amount: 750000,
  },
  {
    name: 'FinOps Sentinel',
    problem: 'Enterprises bleed 30%+ of cloud spend on idle GPUs and inefficient multi-cloud clusters.',
    solution: 'Autonomous agent that right-sizes Kubernetes nodes & buys spot instances dynamically.',
    target_market: 'Series B+ tech companies and enterprise DevOps engineering teams.',
    business_model: 'Gain-share pricing: 20% of net cloud cost savings delivered each month.',
    funding_amount: 1200000,
  },
  {
    name: 'EcoGrid Dynamics',
    problem: 'Renewable microgrid operators suffer 22% battery degradation from unpredictable load peaks.',
    solution: 'Edge AI controller predicting microgrid demand spikes 4 hours in advance.',
    target_market: 'Commercial solar & battery operators and industrial park utilities.',
    business_model: 'Hardware edge gateway ($3k) + monthly SaaS license per megawatt managed.',
    funding_amount: 500000,
  },
  {
    name: 'CyberShield X',
    problem: 'AI-generated spear-phishing bypasses legacy email filters in 40% of targeted attacks.',
    solution: 'Zero-trust linguistic deception detection simulating attacker LLM behaviors.',
    target_market: 'Fintech, healthcare, and critical infrastructure enterprises.',
    business_model: 'Per-seat monthly subscription ($8/seat/mo with 500 seat minimum).',
    funding_amount: 1500000,
  },
];

export default function ChatPitchInput({
  onSubmitPitch,
  isLoading = false,
  selectedRounds = 2,
  onChangeRounds,
}) {
  const [expanded, setExpanded] = useState(false);
  const [pitchData, setPitchData] = useState({
    startup_name: '',
    problem: '',
    solution: '',
    target_market: '',
    business_model: '',
    funding_amount: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPitchData((prev) => ({ ...prev, [name]: value }));
  };

  const handleLoadSample = (sample) => {
    setPitchData(sample);
    setExpanded(true);
  };

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (isLoading) return;

    if (!pitchData.startup_name && !pitchData.problem && !pitchData.solution) {
      alert('Please enter at least a startup name or core concept.');
      return;
    }

    const payload = {
      startup_name: pitchData.startup_name || 'InnovateX AI',
      problem: pitchData.problem || pitchData.solution || 'Startup problem statement',
      solution: pitchData.solution || pitchData.problem || 'Innovative AI-powered solution',
      target_market: pitchData.target_market || 'B2B Enterprise Customers',
      business_model: pitchData.business_model || 'B2B SaaS Subscription',
      funding_amount: Number(pitchData.funding_amount) || 500000,
      rounds: selectedRounds,
    };

    onSubmitPitch(payload);
  };

  const handleQuickKey = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="chat-pitch-bar-container">
      {/* Sample Pitches Pill Selector & Round Selector */}
      <div className="chat-top-controls">
        <div className="sample-pitches-row">
          <span className="sample-label">
            <Sparkles size={14} color="#818cf8" />
            <span>Sample Pitches:</span>
          </span>
          <div className="samples-scroll">
            {SAMPLE_PITCHES.map((sample, idx) => (
              <button
                key={idx}
                type="button"
                className="sample-pitch-pill"
                onClick={() => handleLoadSample(sample)}
                disabled={isLoading}
              >
                {sample.name}
              </button>
            ))}
          </div>
        </div>

        {/* Round Selector */}
        <div className="round-selector-wrap">
          <span className="round-label">Debate Rounds:</span>
          <div className="round-buttons-group">
            {[1, 2, 3].map((r) => (
              <button
                key={r}
                type="button"
                className={`btn-round-opt ${selectedRounds === r ? 'active' : ''}`}
                onClick={() => onChangeRounds(r)}
                disabled={isLoading}
                title={`${r} Round${r > 1 ? 's' : ''} ${r === 1 ? '(Fast)' : r === 2 ? '(Standard)' : '(Deep Deliberation)'}`}
              >
                {r} {r === 1 ? 'Fast' : r === 2 ? 'In-Depth' : 'War Room'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Expandable Advanced Fields Drawer */}
      {expanded && (
        <div className="pitch-drawer-expanded glass-card">
          <div className="drawer-header">
            <h4>Structured Pitch Blueprint</h4>
            <button
              type="button"
              className="btn-ghost-sm"
              onClick={() => setExpanded(false)}
            >
              <ChevronDown size={15} />
              <span>Collapse</span>
            </button>
          </div>

          <div className="drawer-grid">
            <div className="drawer-field">
              <label>Startup Name</label>
              <input
                type="text"
                name="startup_name"
                value={pitchData.startup_name}
                onChange={handleInputChange}
                placeholder="e.g., MediVision AI"
                onKeyDown={handleQuickKey}
              />
            </div>

            <div className="drawer-field">
              <label>Target Market</label>
              <input
                type="text"
                name="target_market"
                value={pitchData.target_market}
                onChange={handleInputChange}
                placeholder="e.g., Hospital radiology networks"
                onKeyDown={handleQuickKey}
              />
            </div>

            <div className="drawer-field">
              <label>Business Model</label>
              <input
                type="text"
                name="business_model"
                value={pitchData.business_model}
                onChange={handleInputChange}
                placeholder="e.g., Annual B2B SaaS license"
                onKeyDown={handleQuickKey}
              />
            </div>

            <div className="drawer-field">
              <label>Funding Target ($)</label>
              <input
                type="number"
                name="funding_amount"
                value={pitchData.funding_amount}
                onChange={handleInputChange}
                placeholder="e.g., 750000"
                onKeyDown={handleQuickKey}
              />
            </div>

            <div className="drawer-field full-span">
              <label>Core Problem Statement</label>
              <textarea
                name="problem"
                rows="2"
                value={pitchData.problem}
                onChange={handleInputChange}
                placeholder="What critical customer pain point are you solving?"
                onKeyDown={handleQuickKey}
              />
            </div>

            <div className="drawer-field full-span">
              <label>Solution & Defensible Moat</label>
              <textarea
                name="solution"
                rows="2"
                value={pitchData.solution}
                onChange={handleInputChange}
                placeholder="How does your technology solve it uniquely?"
                onKeyDown={handleQuickKey}
              />
            </div>
          </div>
        </div>
      )}

      {/* Chat-Style Main Input Bar */}
      <form className="chat-input-bar-form" onSubmit={handleSubmit}>
        <button
          type="button"
          className={`btn-toggle-drawer ${expanded ? 'active' : ''}`}
          onClick={() => setExpanded(!expanded)}
          title="Toggle Full Pitch Form"
        >
          <Sliders size={18} />
          <span>{expanded ? 'Less Fields' : 'Pitch Details'}</span>
          {expanded ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
        </button>

        <div className="chat-input-wrapper">
          <input
            type="text"
            className="chat-main-input"
            name="solution"
            value={pitchData.solution || pitchData.problem || ''}
            onChange={(e) => {
              const val = e.target.value;
              setPitchData((prev) => ({
                ...prev,
                solution: val,
                problem: prev.problem || val,
                startup_name: prev.startup_name || 'My Startup',
              }));
            }}
            placeholder="Pitch your startup idea... (e.g. 'AI copilot for B2B clinical trials to cut recruitment time 70%')"
            onKeyDown={handleQuickKey}
            disabled={isLoading}
          />
        </div>

        <button
          type="submit"
          className="btn-start-eval"
          disabled={isLoading || (!pitchData.startup_name && !pitchData.solution && !pitchData.problem)}
        >
          {isLoading ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              <span>Deliberating...</span>
            </>
          ) : (
            <>
              <Send size={16} />
              <span>Start Evaluation</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
