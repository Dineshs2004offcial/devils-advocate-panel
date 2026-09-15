import React, { useState } from 'react';
import {
  Settings,
  X,
  Cpu,
  Database,
  CheckCircle2,
  Sparkles,
  Check
} from './Icons';

export default function SettingsModal({
  isOpen,
  onClose,
}) {
  const [model, setModel] = useState('gemini-2.5-pro');
  const [temperature, setTemperature] = useState(0.4);
  const [autoSave, setAutoSave] = useState(true);
  const [savedSuccess, setSavedSuccess] = useState(false);

  if (!isOpen) return null;

  const handleSave = () => {
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 800);
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-box modal-md" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <div className="modal-title-wrap">
            <Settings size={20} color="#818cf8" />
            <div>
              <h3>Panel Engine Settings</h3>
              <span>Configure AI debate parameters and MCP persistence</span>
            </div>
          </div>
          <button className="btn-ghost-sm" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        <div className="modal-body">
          {/* LLM Model Provider */}
          <div className="settings-field">
            <label>Primary AI Deliberation Model</label>
            <select value={model} onChange={(e) => setModel(e.target.value)}>
              <option value="gemini-2.5-pro">Google Gemini 2.5 Pro (Recommended)</option>
              <option value="gpt-4o">OpenAI GPT-4o</option>
              <option value="mistral-large">Mistral Large 2</option>
              <option value="llama-3.3-70b">Groq Llama 3.3 70B</option>
            </select>
            <span className="field-hint">Used for 3-agent adversarial loop and AI Lead Judge</span>
          </div>

          {/* Adversarial Sharpness */}
          <div className="settings-field">
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <label>Adversarial Strictness (Temperature)</label>
              <span className="text-accent">{temperature}</span>
            </div>
            <input
              type="range"
              min="0.1"
              max="1.0"
              step="0.05"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
            />
            <span className="field-hint">Lower values yield sharper, more disciplined unit-economics scrutiny</span>
          </div>

          {/* Storage Preferences */}
          <div className="settings-field toggle-field">
            <div>
              <label>Auto-Save Evaluations</label>
              <span className="field-hint">Automatically store completed deliberations to local and PostgreSQL history</span>
            </div>
            <input
              type="checkbox"
              checked={autoSave}
              onChange={(e) => setAutoSave(e.target.checked)}
            />
          </div>

          {/* Engine Status info */}
          <div className="settings-engine-status glass-panel">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <CheckCircle2 size={16} color="#10b981" />
              <strong>LangGraph Multi-Agent Runtime: Online</strong>
            </div>
            <p style={{ margin: '6px 0 0 0', fontSize: '0.8rem', color: '#94a3b8' }}>
              4 MCP microservices connected • Vector RAG ready • Realtime Web intelligence active
            </p>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button className="btn-primary" onClick={handleSave}>
            {savedSuccess ? <Check size={14} /> : null}
            <span>{savedSuccess ? 'Saved!' : 'Apply Preferences'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
