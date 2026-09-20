import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Search,
  Network,
  Database,
  FileText,
  Cpu,
  Radio,
  ChevronRight
} from './Icons';

/**
 * Reusable MCPConnectorCard Component
 * Displays only connector name, status badge, and short description on the main page.
 * Provides interactive hover states and navigates directly to the dedicated detail route on click.
 */
export default function MCPConnectorCard({
  id,
  name,
  route,
  status = 'connected',
  shortDescription = '',
  iconName = 'Cpu',
  accentColor = '#818cf8',
  isWorking = false,
  onClick,
  className = ''
}) {
  const navigate = useNavigate();

  const handleClick = (e) => {
    if (onClick) {
      onClick(e);
    } else if (route) {
      navigate(route);
    }
  };

  // Render appropriate icon based on string iconName
  const renderIcon = () => {
    switch (iconName?.toLowerCase()) {
      case 'search':
        return <Search size={16} color={accentColor || '#38bdf8'} />;
      case 'network':
        return <Network size={16} color={accentColor || '#a855f7'} />;
      case 'database':
        return <Database size={16} color={accentColor || '#10b981'} />;
      case 'filetext':
      case 'file':
        return <FileText size={16} color={accentColor || '#f59e0b'} />;
      case 'radio':
        return <Radio size={16} color={accentColor || '#818cf8'} />;
      case 'cpu':
      default:
        return <Cpu size={16} color={accentColor || '#818cf8'} />;
    }
  };

  // Compute status badge styling
  const getStatusBadge = () => {
    if (isWorking) {
      return {
        label: '🟡 Working',
        className: 'status-working'
      };
    }
    const s = String(status || '').toLowerCase();
    if (s === 'connected' || s === 'ok' || s === 'ready') {
      return {
        label: '🟢 Connected',
        className: 'status-connected'
      };
    }
    if (s === 'error' || s === 'failed') {
      return {
        label: '🔴 Error',
        className: 'status-error'
      };
    }
    return {
      label: '🟢 Connected',
      className: 'status-connected'
    };
  };

  const badge = getStatusBadge();

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={handleClick}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleClick(e);
        }
      }}
      className={`mcp-connector-card glass-panel clickable-card ${className}`}
      style={{
        '--card-accent': accentColor || '#818cf8'
      }}
      title={`Open ${name} details`}
    >
      <div className="mcp-card-header">
        <div className="mcp-connector-id">
          <div className="mcp-card-icon-wrap">
            {renderIcon()}
          </div>
          <h4>{name}</h4>
        </div>
        <div className="mcp-header-right">
          <span className={`mcp-badge ${badge.className}`}>
            {badge.label}
          </span>
          <span className="mcp-card-arrow">
            <ChevronRight size={14} />
          </span>
        </div>
      </div>

      {shortDescription && (
        <p className="mcp-desc">{shortDescription}</p>
      )}
    </div>
  );
}
