import React, { useState } from 'react';
import {
  Plus,
  Search,
  Trash2,
  Edit2,
  Sparkles,
  Settings,
  Scale,
  Check,
  X,
  Flame,
  Award,
  ChevronLeft,
  ChevronRight,
  Database
} from './Icons';

export default function Sidebar({
  evaluations = [],
  activeEvaluationId,
  onSelectEvaluation,
  onNewEvaluation,
  onRenameEvaluation,
  onDeleteEvaluation,
  onOpenCompare,
  onOpenSettings,
  isCollapsed = false,
  onToggleCollapse
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState('');

  const filteredEvaluations = evaluations.filter((item) => {
    const name = (item.startup_name || item.name || '').toLowerCase();
    const verdict = (item.verdict || '').toLowerCase();
    const query = searchQuery.toLowerCase();
    return name.includes(query) || verdict.includes(query);
  });

  const startEditing = (e, item) => {
    e.stopPropagation();
    setEditingId(item.id);
    setEditName(item.startup_name);
  };

  const saveRename = (e, id) => {
    e.stopPropagation();
    if (editName.trim()) {
      onRenameEvaluation(id, editName.trim());
    }
    setEditingId(null);
  };

  const cancelRename = (e) => {
    e.stopPropagation();
    setEditingId(null);
  };

  const handleDelete = (e, id) => {
    e.stopPropagation();
    if (window.confirm('Delete this evaluation record?')) {
      onDeleteEvaluation(id);
    }
  };

  const getVerdictTagClass = (verdict) => {
    const v = String(verdict || '').toUpperCase();
    if (v.includes('INVEST')) return 'badge-tag-invest';
    if (v.includes('REJECT')) return 'badge-tag-reject';
    return 'badge-tag-review';
  };

  const formatDate = (isoString) => {
    if (!isoString) return 'Recent';
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return 'Recent';
    }
  };

  if (isCollapsed) {
    return (
      <aside className="sidebar-collapsed">
        <button
          className="btn-icon-square"
          onClick={onToggleCollapse}
          title="Expand Sidebar"
        >
          <ChevronRight size={18} />
        </button>

        <button
          className="btn-icon-square btn-accent-glow"
          onClick={onNewEvaluation}
          title="New Evaluation"
        >
          <Plus size={18} />
        </button>

        <button
          className="btn-icon-square"
          onClick={onOpenCompare}
          title="Compare Evaluations"
        >
          <Scale size={18} />
        </button>

        <div style={{ marginTop: 'auto' }}>
          <button
            className="btn-icon-square"
            onClick={onOpenSettings}
            title="Settings"
          >
            <Settings size={18} />
          </button>
        </div>
      </aside>
    );
  }

  return (
    <aside className="sidebar-container">
      {/* Brand Header */}
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="brand-logo-glow">
            <Flame size={20} color="#f43f5e" />
          </div>
          <div className="brand-text">
            <h2>Devil's Advocate</h2>
            <span>Adversarial AI Panel</span>
          </div>
        </div>
        <button
          className="btn-ghost-sm"
          onClick={onToggleCollapse}
          title="Collapse Sidebar"
        >
          <ChevronLeft size={16} />
        </button>
      </div>

      {/* New Evaluation Action */}
      <div className="sidebar-action-wrap">
        <button
          className="btn-new-eval"
          onClick={onNewEvaluation}
        >
          <Plus size={17} />
          <span>New Evaluation</span>
        </button>
      </div>

      {/* Search Bar */}
      <div className="sidebar-search">
        <Search size={15} color="#64748b" className="search-icon" />
        <input
          type="text"
          placeholder="Search evaluations..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        {searchQuery && (
          <button
            className="search-clear-btn"
            onClick={() => setSearchQuery('')}
          >
            <X size={13} />
          </button>
        )}
      </div>

      {/* History List */}
      <div className="sidebar-history-section">
        <div className="sidebar-section-title">
          <span>Recent Evaluations</span>
          <span className="count-pill">{filteredEvaluations.length}</span>
        </div>

        <div className="history-items-scroll">
          {filteredEvaluations.length === 0 ? (
            <div className="sidebar-empty-state">
              <Database size={24} color="#475569" />
              <p>{searchQuery ? 'No matching evaluations' : 'No evaluations saved yet'}</p>
            </div>
          ) : (
            filteredEvaluations.map((item) => {
              const isActive = item.id === activeEvaluationId;
              const isEditing = item.id === editingId;

              return (
                <div
                  key={item.id}
                  className={`history-card ${isActive ? 'active' : ''}`}
                  onClick={() => !isEditing && onSelectEvaluation(item)}
                >
                  <div className="history-card-top">
                    {isEditing ? (
                      <div className="rename-inline-box" onClick={(e) => e.stopPropagation()}>
                        <input
                          type="text"
                          value={editName}
                          onChange={(e) => setEditName(e.target.value)}
                          autoFocus
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') saveRename(e, item.id);
                            if (e.key === 'Escape') cancelRename(e);
                          }}
                        />
                        <button className="btn-save-rename" onClick={(e) => saveRename(e, item.id)}>
                          <Check size={13} />
                        </button>
                        <button className="btn-cancel-rename" onClick={cancelRename}>
                          <X size={13} />
                        </button>
                      </div>
                    ) : (
                      <>
                        <h4 className="startup-item-title" title={item.startup_name}>
                          {item.startup_name}
                        </h4>
                        <div className="history-card-actions">
                          <button
                            className="btn-item-action"
                            title="Rename"
                            onClick={(e) => startEditing(e, item)}
                          >
                            <Edit2 size={13} />
                          </button>
                          <button
                            className="btn-item-action btn-delete"
                            title="Delete"
                            onClick={(e) => handleDelete(e, item.id)}
                          >
                            <Trash2 size={13} />
                          </button>
                        </div>
                      </>
                    )}
                  </div>

                  <div className="history-card-bottom">
                    <span className="history-date">{formatDate(item.createdAt)}</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      {item.score && (
                        <span className="history-score-tag">{item.score} pts</span>
                      )}
                      <span className={`badge-tag ${getVerdictTagClass(item.verdict)}`}>
                        {item.verdict || 'REVIEW'}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Compare Mode Launcher */}
      <div className="sidebar-compare-wrap">
        <button
          className="btn-compare-link"
          onClick={onOpenCompare}
        >
          <Scale size={15} />
          <span>Compare Evaluations</span>
        </button>
      </div>

      {/* User Profile & Settings at Bottom */}
      <div className="sidebar-footer">
        <div className="user-profile-card">
          <div className="user-avatar">
            <span>AI</span>
            <div className="avatar-status-dot" />
          </div>
          <div className="user-info">
            <span className="user-name">Venture Partner</span>
            <span className="user-role">LangGraph Panelist</span>
          </div>
          <button
            className="btn-settings-trigger"
            onClick={onOpenSettings}
            title="Panel Settings"
          >
            <Settings size={17} />
          </button>
        </div>
      </div>
    </aside>
  );
}
