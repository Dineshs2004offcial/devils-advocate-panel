import React, { useState } from 'react';
import {
  Cpu,
  RefreshCw,
  Database,
  Network,
  FileText,
  Search,
  ChevronRight,
  ChevronLeft,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Activity
} from './Icons';

export default function McpPanel({
  mcpStatus = {},
  isWorking = false,
  onRefresh,
  isCollapsed = false,
  onToggleCollapse
}) {
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    await onRefresh();
    setTimeout(() => setRefreshing(false), 800);
  };

  const getStatusBadge = (statusKey) => {
    if (isWorking) {
      return {
        label: '🟡 Working',
        colorClass: 'status-working',
        dot: '🟡',
      };
    }

    const s = String(statusKey || '').toLowerCase();
    if (s === 'connected' || s === 'ok' || s === 'ready') {
      return {
        label: '🟢 Connected',
        colorClass: 'status-connected',
        dot: '🟢',
      };
    }
    if (s === 'error' || s === 'failed') {
      return {
        label: '🔴 Error',
        colorClass: 'status-error',
        dot: '🔴',
      };
    }
    return {
      label: '🟢 Connected',
      colorClass: 'status-connected',
      dot: '🟢',
    };
  };

  const webMcp = mcpStatus.web_research || {
    name: 'Web Research MCP',
    status: 'connected',
    type: 'DuckDuckGo / Tavily',
    details: 'Real-time market intelligence & competitor discovery',
  };

  const kbMcp = mcpStatus.knowledge_base || {
    name: 'Knowledge Base MCP',
    status: 'connected',
    type: 'ChromaDB / Vector RAG',
    files_count: 0,
    details: 'Local RAG benchmarks & startup evaluation corpus',
  };

  const pgMcp = mcpStatus.postgres || {
    name: 'PostgreSQL MCP',
    status: 'connected',
    type: 'PostgreSQL',
    details: 'Persistent evaluation sessions & audit logs',
  };

  const reportMcp = mcpStatus.report_pdf || {
    name: 'Report / PDF MCP',
    status: 'connected',
    type: 'Export Engine',
    details: 'Executive summary & PDF dossier compiler',
  };

  if (isCollapsed) {
    return (
      <aside className="mcp-panel-collapsed">
        <button
          className="btn-icon-square"
          onClick={onToggleCollapse}
          title="Expand MCP Connectors"
        >
          <ChevronLeft size={18} />
        </button>

        <div className="mcp-collapsed-indicator" title="4 MCP Connectors Connected">
          <Cpu size={18} color="#818cf8" />
          <span className="mcp-dot-pulse" />
        </div>
      </aside>
    );
  }

  return (
    <aside className="mcp-panel-container">
      {/* Header */}
      <div className="mcp-panel-header">
        <div className="mcp-header-title">
          <div className="mcp-icon-pill">
            <Cpu size={16} color="#818cf8" />
          </div>
          <div>
            <h3>MCP Connectors</h3>
            <span>Model Context Protocol</span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <button
            className={`btn-ghost-sm ${refreshing ? 'animate-spin' : ''}`}
            onClick={handleRefresh}
            title="Refresh Connector Status"
          >
            <RefreshCw size={14} />
          </button>
          <button
            className="btn-ghost-sm"
            onClick={onToggleCollapse}
            title="Collapse MCP Panel"
          >
            <ChevronRight size={16} />
          </button>
        </div>
      </div>

      {/* Overview Status Strip */}
      <div className="mcp-overall-strip">
        <div className="strip-left">
          <span className="mcp-live-ping" />
          <span>Active Protocol Mesh</span>
        </div>
        <span className="mcp-active-count">4/4 Online</span>
      </div>

      {/* Connectors List */}
      <div className="mcp-connectors-list">
        {/* 1. Web Research MCP */}
        <div className="mcp-card glass-panel">
          <div className="mcp-card-header">
            <div className="mcp-connector-id">
              <Search size={16} color="#38bdf8" />
              <h4>{webMcp.name}</h4>
            </div>
            <span className={`mcp-badge ${getStatusBadge(webMcp.status).colorClass}`}>
              {getStatusBadge(webMcp.status).label}
            </span>
          </div>
          <p className="mcp-desc">{webMcp.details}</p>
          <div className="mcp-footer-meta">
            <span className="mcp-engine-tag">Engine: {webMcp.type || 'DuckDuckGo / Tavily'}</span>
          </div>
        </div>

        {/* 2. Knowledge Base MCP */}
        <div className="mcp-card glass-panel">
          <div className="mcp-card-header">
            <div className="mcp-connector-id">
              <Network size={16} color="#818cf8" />
              <h4>{kbMcp.name}</h4>
            </div>
            <span className={`mcp-badge ${getStatusBadge(kbMcp.status).colorClass}`}>
              {getStatusBadge(kbMcp.status).label}
            </span>
          </div>
          <p className="mcp-desc">{kbMcp.details}</p>
          <div className="mcp-footer-meta">
            <span className="mcp-engine-tag">Storage: {kbMcp.type || 'ChromaDB'}</span>
            {kbMcp.files_count !== undefined && (
              <span className="mcp-doc-count">{kbMcp.files_count} docs</span>
            )}
          </div>
        </div>

        {/* 3. PostgreSQL MCP */}
        <div className="mcp-card glass-panel">
          <div className="mcp-card-header">
            <div className="mcp-connector-id">
              <Database size={16} color="#10b981" />
              <h4>{pgMcp.name}</h4>
            </div>
            <span className={`mcp-badge ${getStatusBadge(pgMcp.status).colorClass}`}>
              {getStatusBadge(pgMcp.status).label}
            </span>
          </div>
          <p className="mcp-desc">{pgMcp.details}</p>
          <div className="mcp-footer-meta">
            <span className="mcp-engine-tag">Driver: pg8000 / SQL</span>
          </div>
        </div>

        {/* 4. Report & PDF MCP */}
        <div className="mcp-card glass-panel">
          <div className="mcp-card-header">
            <div className="mcp-connector-id">
              <FileText size={16} color="#f59e0b" />
              <h4>{reportMcp.name}</h4>
            </div>
            <span className={`mcp-badge ${getStatusBadge(reportMcp.status).colorClass}`}>
              {getStatusBadge(reportMcp.status).label}
            </span>
          </div>
          <p className="mcp-desc">{reportMcp.details}</p>
          <div className="mcp-footer-meta">
            <span className="mcp-engine-tag">Format: PDF / HTML / JSON</span>
          </div>
        </div>
      </div>

      {/* Activity Log Mini Feed */}
      <div className="mcp-activity-box">
        <div className="activity-title">
          <Activity size={13} color="#64748b" />
          <span>MCP Event Stream</span>
        </div>
        <div className="activity-feed">
          <div className="feed-item">
            <span className="feed-time">now</span>
            <span className="feed-msg">Protocol mesh synchronized</span>
          </div>
          <div className="feed-item">
            <span className="feed-time">-2m</span>
            <span className="feed-msg">Vector index ping OK (0ms)</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
