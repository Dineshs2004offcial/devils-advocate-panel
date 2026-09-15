import React from "react";

function AgentCard({ title, icon, analysis }) {
  return (
    <div className="agent-card">
      <div className="agent-header">
        <span className="agent-icon">{icon}</span>
        <h3>{title}</h3>
      </div>
      <div className="agent-content">
        {analysis || "No analysis available."}
      </div>
    </div>
  );
}

export default AgentCard;
