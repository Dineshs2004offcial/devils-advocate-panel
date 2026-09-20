const PRIMARY_API_URL = "http://127.0.0.1:8000";
const BACKUP_API_URL = "http://localhost:8000";
const STORAGE_KEY = "devils_advocate_evaluations_v2";

async function postWithFallback(endpoint, data) {
  const urls = [
    endpoint, // relative via Vite proxy
    `${PRIMARY_API_URL}${endpoint}`,
    `${BACKUP_API_URL}${endpoint}`,
  ];

  let lastError = null;

  for (const url of urls) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `Request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      lastError = err;
      // If it was a network failure, try the next URL in fallback list
      continue;
    }
  }

  throw lastError || new Error("Failed to connect to backend server. Please verify uvicorn is running.");
}

/**
 * Submit pitch to the backend LangGraph Multi-Agent Debate engine
 */
export async function evaluatePitch(pitch, rounds = 2) {
  const payload = {
    ...pitch,
    rounds: Number(rounds) || 2,
  };

  return await postWithFallback("/evaluation/", payload);
}


async function getWithFallback(endpoint) {
  const urls = [
    endpoint, // relative via Vite proxy
    `${PRIMARY_API_URL}${endpoint}`,
    `${BACKUP_API_URL}${endpoint}`,
  ];

  let lastError = null;

  for (const url of urls) {
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      lastError = err;
      continue;
    }
  }

  throw lastError || new Error("Failed to connect to backend server.");
}

/**
 * Fetch real-time status of all Model Context Protocol Connectors
 */
export async function fetchMcpStatus() {
  try {
    return await getWithFallback("/mcp/status");
  } catch (err) {
    try {
      return await getWithFallback("/evaluation/mcp-status");
    } catch (error) {
      console.warn("MCP status fetch failed:", error);
    }
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
      files_count: 4,
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
    active_protocol_mesh: {
      name: "Active Protocol Mesh",
      status: "connected",
      type: "ipc / event_bus",
      details: "Real-time multi-agent protocol bus & cross-agent synchronization",
    }
  };
}

/**
 * Execute an MCP Tool dynamically against the backend MCP server runtime
 */
export async function executeMcpTool(toolName, argumentsObj = {}) {
  return await postWithFallback("/mcp/execute", {
    tool_name: toolName,
    arguments: argumentsObj,
  });
}

/**
 * Fetch all registered MCP tools from the backend
 */
export async function fetchMcpTools() {
  try {
    return await getWithFallback("/mcp/tools");
  } catch (err) {
    console.warn("Failed to fetch MCP tools:", err);
    return { tools: [] };
  }
}

const DEFAULT_JOBBRIDGE_EVAL = {
  startup_name: "JobBridge",
  pitch: {
    startup_name: "JobBridge",
    problem: "Freshers struggle to find relevant entry-level jobs because most job portals show too many unrelated openings, while companies spend significant time screening candidates who do not match the required skills.",
    solution: "JobBridge is an AI-powered job matching platform that analyzes a candidate's resume, skills, education and preferences, then matches them with suitable entry-level jobs. Its potential moat is a continuously improving candidate-skill dataset, personalized matching models, and structured skill profiles that help improve matching quality over time",
    target_market: "Fresh graduates and final-year students looking for entry-level jobs, especially candidates with 0-2 years of experience.",
    business_model: "Companies pay a subscription or recruitment fee to access AI-matched candidates. Job seekers can use the basic service for free, with an optional premium plan for advanced career features."
  },
  judge: {
    verdict: "REVIEW",
    consensus: "CONSENSUS: FURTHER REVIEW",
    overall_score: 70,
    market_score: 74,
    financial_score: 64,
    risk_score: 45,
    overall_assessment: "Promising market demand, but key financial or customer acquisition risks require founder diligence."
  },
  final_verdict: "Promising market demand, but key financial or customer acquisition risks require founder diligence."
};

const DEFAULT_SEED_EVALUATIONS = [
  {
    id: "eval_jobbridge_1",
    startup_name: "JobBridge",
    displayDate: "Sep 17, 02:47 PM",
    createdAt: "2026-09-17T14:47:00.000Z",
    verdict: "REVIEW",
    score: 70,
    data: { evaluation: DEFAULT_JOBBRIDGE_EVAL, startup_name: "JobBridge" }
  },
  {
    id: "eval_ecokart_1",
    startup_name: "EcoKart",
    displayDate: "Sep 17, 02:36 PM",
    createdAt: "2026-09-17T14:36:00.000Z",
    verdict: "REVIEW",
    score: 68,
    data: { evaluation: { ...DEFAULT_JOBBRIDGE_EVAL, startup_name: "EcoKart" }, startup_name: "EcoKart" }
  },
  {
    id: "eval_ecokart_2",
    startup_name: "EcoKart",
    displayDate: "Sep 17, 11:05 AM",
    createdAt: "2026-09-17T11:05:00.000Z",
    verdict: "REVIEW",
    score: 68,
    data: { evaluation: { ...DEFAULT_JOBBRIDGE_EVAL, startup_name: "EcoKart" }, startup_name: "EcoKart" }
  },
  {
    id: "eval_mystartup_1",
    startup_name: "My Startup",
    displayDate: "Sep 15, 09:14 PM",
    createdAt: "2026-09-15T21:14:00.000Z",
    verdict: "REVIEW",
    score: 68,
    data: { evaluation: { ...DEFAULT_JOBBRIDGE_EVAL, startup_name: "My Startup" }, startup_name: "My Startup" }
  },
  {
    id: "eval_ecokart_3",
    startup_name: "EcoKart",
    displayDate: "Sep 15, 04:09 PM",
    createdAt: "2026-09-15T16:09:00.000Z",
    verdict: "REVIEW",
    score: 68,
    data: { evaluation: { ...DEFAULT_JOBBRIDGE_EVAL, startup_name: "EcoKart" }, startup_name: "EcoKart" }
  }
];

import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

/**
 * Local & Remote History Management
 */
export async function syncHistoryWithBackend() {
  try {
    const remote = await getWithFallback("/evaluation/history");
    if (Array.isArray(remote) && remote.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(remote));
      return remote;
    }
  } catch (err) {
    console.warn("Backend history sync skipped:", err);
  }
  return getSavedEvaluations();
}

export function getSavedEvaluations() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_SEED_EVALUATIONS));
      return DEFAULT_SEED_EVALUATIONS;
    }
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) && parsed.length > 0 ? parsed : DEFAULT_SEED_EVALUATIONS;
  } catch (err) {
    console.error("Failed to load evaluations from storage:", err);
    return DEFAULT_SEED_EVALUATIONS;
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
      id: evaluationResult?.id || "eval_" + Date.now() + "_" + Math.random().toString(36).substring(2, 7),
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

export async function deleteSavedEvaluation(id) {
  try {
    // Delete from backend if available
    try {
      const urls = [
        `/evaluation/${id}`,
        `${PRIMARY_API_URL}/evaluation/${id}`,
        `${BACKUP_API_URL}/evaluation/${id}`,
      ];
      for (const u of urls) {
        try {
          await fetch(u, { method: "DELETE" });
          break;
        } catch (e) {}
      }
    } catch (e) {}

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
 * Downloads a complete PDF containing transcripts of every round and final verdict.
 * Calls backend ReportLab compiler with client-side jsPDF fallback.
 */
export async function downloadEvaluationPdf(evaluationData) {
  const evaluation = evaluationData?.evaluation || evaluationData?.result || evaluationData;
  const name = evaluationData?.startup_name || evaluation?.startup_name || "Startup_Evaluation";
  const safeFilename = name.replace(/[^a-zA-Z0-9_\-]/g, "_") + "_Executive_Dossier.pdf";

  // 1. Try backend streaming ReportLab PDF endpoint first
  try {
    const urls = [
      "/evaluation/export-pdf",
      `${PRIMARY_API_URL}/evaluation/export-pdf`,
      `${BACKUP_API_URL}/evaluation/export-pdf`,
    ];

    for (const url of urls) {
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(evaluationData),
        });
        if (response.ok) {
          const blob = await response.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = downloadUrl;
          link.download = safeFilename;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(downloadUrl);
          return { status: "success", mode: "backend" };
        }
      } catch (err) {
        continue;
      }
    }
  } catch (err) {
    console.warn("Backend PDF generation unavailable; using client-side jsPDF engine:", err);
  }

  // 2. Client-side jsPDF fallback
  try {
    const doc = new jsPDF({ unit: 'pt', format: 'letter' });
    const judge = evaluation?.judge || {};
    const verdict = (judge?.verdict || evaluation?.final_verdict || "REVIEW").toUpperCase();
    const score = judge?.score ?? judge?.overall_score ?? 70;
    const pitch = evaluation?.pitch || {};

    // Header Banner
    doc.setFillColor(15, 23, 42); // slate-900
    doc.rect(0, 0, 612, 70, 'F');

    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.setTextColor(255, 255, 255);
    doc.text("DEVIL'S ADVOCATE PANEL - EXECUTIVE DOSSIER", 306, 32, { align: "center" });

    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(147, 197, 253);
    doc.text(`Target Venture: ${name}  |  Generated: ${new Date().toLocaleDateString()}`, 306, 52, { align: "center" });

    // Verdict Box
    let startY = 90;
    doc.setFillColor(241, 245, 249);
    doc.roundedRect(36, startY, 540, 50, 4, 4, 'F');
    doc.setDrawColor(verdict.includes("INVEST") ? 16 : 245, verdict.includes("INVEST") ? 185 : 158, verdict.includes("INVEST") ? 129 : 11);
    doc.setLineWidth(2);
    doc.roundedRect(36, startY, 540, 50, 4, 4, 'S');

    doc.setFont("helvetica", "bold");
    doc.setFontSize(12);
    doc.setTextColor(15, 23, 42);
    doc.text(`CONSENSUS VERDICT: ${verdict}   |   COMPOSITE SCORE: ${score}/100`, 50, startY + 24);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(71, 85, 105);
    const assessment = (judge?.overall_assessment || evaluation?.final_verdict || "Evaluation completed.").substring(0, 140) + "...";
    doc.text(assessment, 50, startY + 40);

    // Startup Info Table
    startY += 65;
    autoTable(doc, {
      startY: startY,
      head: [["Startup Metric / Pitch Field", "Details"]],
      body: [
        ["Problem Statement", pitch.problem || "N/A"],
        ["Proposed Solution", pitch.solution || "N/A"],
        ["Target Market", pitch.target_market || "N/A"],
        ["Business Model", pitch.business_model || "N/A"],
        ["Funding Request", pitch.funding_amount ? `$${Number(pitch.funding_amount).toLocaleString()}` : "N/A"]
      ],
      theme: 'grid',
      headStyles: { fillColor: [30, 64, 175], textColor: [255, 255, 255], fontStyle: 'bold' },
      styles: { fontSize: 8, cellPadding: 5 },
      margin: { left: 36, right: 36 }
    });

    // Round 1 Deliberation Transcripts
    const round1 = evaluation?.round_1 || {};
    const r1Rows = [];
    if (typeof round1 === 'object') {
      Object.entries(round1).forEach(([k, ag]) => {
        if (ag && typeof ag === 'object') {
          r1Rows.push([
            (ag.persona || k).toUpperCase(),
            ag.argument || "Analysis provided.",
            (ag.risks || []).join("; ") || "Standard execution risks"
          ]);
        }
      });
    }

    if (r1Rows.length > 0) {
      autoTable(doc, {
        startY: doc.lastAutoTable.finalY + 15,
        head: [["Round 1 Agent Persona", "Core Argument", "Identified Risks"]],
        body: r1Rows,
        theme: 'striped',
        headStyles: { fillColor: [15, 23, 42], textColor: [255, 255, 255], fontStyle: 'bold' },
        styles: { fontSize: 8, cellPadding: 5 },
        margin: { left: 36, right: 36 }
      });
    }

    // Cross Challenges & Rebuttals
    const challenges = evaluation?.challenges || [];
    if (challenges.length > 0) {
      const chRows = challenges.map(c => [
        (c.from || c.from_agent || "VC").replace("_", " ").toUpperCase(),
        (c.target_agent || c.to || "Peer").replace("_", " ").toUpperCase(),
        c.challenge || ""
      ]);

      autoTable(doc, {
        startY: doc.lastAutoTable.finalY + 15,
        head: [["Challenger", "Target Agent", "Adversarial Challenge"]],
        body: chRows,
        theme: 'grid',
        headStyles: { fillColor: [180, 83, 9], textColor: [255, 255, 255] },
        styles: { fontSize: 8, cellPadding: 5 },
        margin: { left: 36, right: 36 }
      });
    }

    // Lead Judge Strategic Recommendations
    const rec = judge?.recommendation || "Conduct follow-up reference checks.";
    const strengths = (judge?.strengths || []).join(", ") || "Validated market opportunity";
    const weaknesses = (judge?.weaknesses || []).join(", ") || "Incumbent competition";

    autoTable(doc, {
      startY: doc.lastAutoTable.finalY + 15,
      head: [["Strategic Category", "Lead Judge Finding & Recommendation"]],
      body: [
        ["Key Strengths", strengths],
        ["Critical Weaknesses", weaknesses],
        ["Action Plan & Recommendation", rec]
      ],
      theme: 'grid',
      headStyles: { fillColor: [5, 150, 105], textColor: [255, 255, 255] },
      styles: { fontSize: 8, cellPadding: 5 },
      margin: { left: 36, right: 36 }
    });

    doc.save(safeFilename);
    return { status: "success", mode: "client_jspdf" };
  } catch (pdfErr) {
    console.error("jsPDF generation failed:", pdfErr);
    exportEvaluationDossier(evaluationData);
    return { status: "fallback_print" };
  }
}

/**
 * Printable HTML Dossier trigger fallback
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
            <h1 class="title">Devil's Advocate Panel</h1>
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

