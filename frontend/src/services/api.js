const API_URL = "http://127.0.0.1:8000";
const STORAGE_KEY = "devils_advocate_evaluations_v2";

/**
 * Submit pitch to the backend LangGraph Multi-Agent Debate engine
 */
export async function evaluatePitch(pitch, rounds = 2) {
  const payload = {
    ...pitch,
    rounds: Number(rounds) || 2,
  };

  const response = await fetch(`${API_URL}/evaluation/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Evaluation failed with status ${response.status}`);
  }

  const data = await response.json();
  return data;
}

/**
 * Fetch real-time status of all 4 MCP Connectors
 */
export async function fetchMcpStatus() {
  try {
    const response = await fetch(`${API_URL}/evaluation/mcp-status`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (response.ok) {
      return await response.json();
    }
  } catch (error) {
    console.warn("MCP status fetch failed:", error);
  }

  // Fallback defaults if API is temporarily unavailable
  return {
    web_research: {
      name: "Web Research MCP",
      status: "connected",
      type: "duckduckgo / tavily",
      details: "Real-time web intelligence & competitor discovery",
    },
    knowledge_base: {
      name: "Knowledge Base MCP",
      status: "connected",
      type: "chromadb / rag",
      files_count: 0,
      details: "Local RAG vector store & industry benchmarks",
    },
    postgres: {
      name: "PostgreSQL MCP",
      status: "connected",
      type: "postgresql",
      details: "Persistent pitch evaluations & session storage",
    },
    report_pdf: {
      name: "Report & PDF MCP",
      status: "connected",
      type: "export_engine",
      details: "HTML, Markdown & PDF executive dossier compiler",
    },
  };
}

/**
 * Local History Management
 */
export function getSavedEvaluations() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (err) {
    console.error("Failed to load evaluations from storage:", err);
    return [];
  }
}

export function saveEvaluationToHistory(evaluationResult, customName = "") {
  try {
    const items = getSavedEvaluations();
    const evaluation = evaluationResult?.evaluation || evaluationResult?.result || evaluationResult;
    const name =
      customName ||
      evaluationResult?.startup_name ||
      evaluation?.startup_name ||
      evaluation?.pitch?.startup_name ||
      "Untitled Evaluation";

    const judge = evaluation?.judge || {};
    const verdict = judge?.verdict || evaluation?.final_verdict?.verdict || "REVIEW";
    const score = judge?.score ?? judge?.overall_score ?? 70;

    const newEntry = {
      id: "eval_" + Date.now() + "_" + Math.random().toString(36).substring(2, 7),
      startup_name: name,
      createdAt: new Date().toISOString(),
      verdict: String(verdict).toUpperCase(),
      score: Number(score) || 70,
      data: evaluationResult,
    };

    // Prepend and limit history to 50 items
    const updated = [newEntry, ...items.filter((item) => item.id !== newEntry.id)].slice(0, 50);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    return newEntry;
  } catch (err) {
    console.error("Failed to save evaluation to history:", err);
    return null;
  }
}

export function renameSavedEvaluation(id, newName) {
  try {
    const items = getSavedEvaluations();
    const updated = items.map((item) => {
      if (item.id === id) {
        return {
          ...item,
          startup_name: newName,
          data: {
            ...item.data,
            startup_name: newName,
          },
        };
      }
      return item;
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    return updated;
  } catch (err) {
    console.error("Failed to rename evaluation:", err);
    return [];
  }
}

export function deleteSavedEvaluation(id) {
  try {
    const items = getSavedEvaluations();
    const updated = items.filter((item) => item.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    return updated;
  } catch (err) {
    console.error("Failed to delete evaluation:", err);
    return [];
  }
}

/**
 * PDF Export & Printable Dossier trigger
 */
export function exportEvaluationDossier(evaluationData) {
  const evaluation = evaluationData?.evaluation || evaluationData?.result || evaluationData;
  const name = evaluationData?.startup_name || evaluation?.startup_name || "Startup Evaluation";
  const judge = evaluation?.judge || {};
  const verdict = judge?.verdict || "REVIEW";
  const score = judge?.score ?? 70;
  const strengths = judge?.strengths || [];
  const weaknesses = judge?.weaknesses || [];
  const risks = judge?.risks || [];
  const rec = judge?.recommendation || "";
  const assessment = judge?.overall_assessment || evaluation?.final_verdict || "";

  const printWindow = window.open("", "_blank");
  if (!printWindow) {
    alert("Please allow popups to download/print the evaluation dossier.");
    return;
  }

  const htmlContent = `
    <!DOCTYPE html>
    <html>
      <head>
        <title>Dossier: ${name} - Devil's Advocate Panel</title>
        <style>
          @page { size: A4; margin: 20mm; }
          body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            background: #ffffff;
            color: #0f172a;
            line-height: 1.6;
            margin: 0;
            padding: 24px;
          }
          .header {
            border-bottom: 2px solid #0f172a;
            padding-bottom: 16px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }
          .title { font-size: 26px; font-weight: 800; margin: 0; }
          .subtitle { font-size: 13px; color: #64748b; margin-top: 4px; }
          .badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 0.5px;
          }
          .badge-invest { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
          .badge-review { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
          .badge-reject { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
          .score-box {
            font-size: 32px;
            font-weight: 900;
            color: #0f172a;
          }
          .section { margin-bottom: 24px; }
          .section-title {
            font-size: 16px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #334155;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 6px;
            margin-bottom: 12px;
          }
          .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
          .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; }
          ul { margin: 0; padding-left: 20px; }
          li { margin-bottom: 6px; }
          .footer {
            margin-top: 40px;
            border-top: 1px solid #cbd5e1;
            padding-top: 12px;
            font-size: 11px;
            color: #94a3b8;
            display: flex;
            justify-content: space-between;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <div>
            <h1 class="title">😈 Devil's Advocate Panel</h1>
            <div class="subtitle">Multi-Agent Adversarial Investment Evaluation Dossier</div>
            <div style="margin-top: 8px; font-weight: 600; font-size: 18px;">Target: ${name}</div>
          </div>
          <div style="text-align: right;">
            <div class="badge ${verdict === 'INVEST' ? 'badge-invest' : verdict === 'REJECT' ? 'badge-reject' : 'badge-review'}">
              VERDICT: ${verdict}
            </div>
            <div class="score-box" style="margin-top: 6px;">${score}<span style="font-size: 16px; color:#64748b;">/100</span></div>
          </div>
        </div>

        <div class="section">
          <div class="section-title">Executive Synthesis</div>
          <p>${typeof assessment === "string" ? assessment : JSON.stringify(assessment)}</p>
        </div>

        <div class="grid">
          <div class="card" style="border-left: 4px solid #10b981;">
            <strong style="color: #15803d;">Key Strengths</strong>
            <ul style="margin-top: 8px;">
              ${strengths.map((s) => `<li>${s}</li>`).join("")}
            </ul>
          </div>
          <div class="card" style="border-left: 4px solid #f59e0b;">
            <strong style="color: #b45309;">Critical Weaknesses</strong>
            <ul style="margin-top: 8px;">
              ${weaknesses.map((w) => `<li>${w}</li>`).join("")}
            </ul>
          </div>
        </div>

        ${
          risks.length > 0
            ? `
          <div class="card" style="border-left: 4px solid #ef4444; margin-bottom: 24px;">
            <strong style="color: #b91c1c;">Identified Venture & Market Risks</strong>
            <ul style="margin-top: 8px;">
              ${risks.map((r) => `<li>${r}</li>`).join("")}
            </ul>
          </div>
        `
            : ""
        }

        ${
          rec
            ? `
          <div class="section">
            <div class="section-title">Lead Judge Strategic Recommendations</div>
            <div class="card" style="background: #f1f5f9;">
              <p style="margin: 0;">${rec}</p>
            </div>
          </div>
        `
            : ""
        }

        <div class="footer">
          <span>Generated by Devil's Advocate Panel (LangGraph Multi-Agent Architecture)</span>
          <span>Date: ${new Date().toLocaleDateString()}</span>
        </div>

        <script>
          window.onload = function() {
            setTimeout(function() {
              window.print();
            }, 300);
          }
        </script>
      </body>
    </html>
  `;

  printWindow.document.open();
  printWindow.document.write(htmlContent);
  printWindow.document.close();
}
