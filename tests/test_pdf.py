import pytest
from app.services.pdf_service import generate_evaluation_pdf
from app.mcp.report import compile_executive_dossier, export_markdown_summary


def test_pdf_generation_complete_evaluation():
    sample_data = {
        "startup_name": "HealthSync AI",
        "pitch": {
            "startup_name": "HealthSync AI",
            "problem": "Radiologist fatigue",
            "solution": "AI screening assist",
            "target_market": "Tier 1 Hospital systems",
            "business_model": "Annual B2B SaaS license",
            "funding_amount": 1000000.0
        },
        "round_1": {
            "devils_advocate": {
                "persona": "Skeptical VC",
                "argument": "High regulatory overhead and liability risks.",
                "strengths": ["Clear acute customer pain"],
                "weaknesses": ["Incumbent PACS vendor lock-in"],
                "risks": ["FDA clearance delay"],
                "questions": ["How do you bypass hospital procurement committees?"]
            },
            "financial_agent": {
                "persona": "Financial Analyst",
                "argument": "Attractive margins if compute is optimized.",
                "strengths": ["Predictable recurring SaaS revenue"],
                "weaknesses": ["Heavy up-front GPU cluster expense"],
                "risks": ["Long DSO on enterprise contracts"],
                "questions": ["What is your expected net retention?"]
            },
            "market_agent": {
                "persona": "Market Realist",
                "argument": "Healthcare IT adoption is notoriously slow.",
                "strengths": ["Immense TAM"],
                "weaknesses": ["Clinical inertia"],
                "risks": ["Regulatory mandate shifts"],
                "questions": ["What is your clinical trial timeline?"]
            }
        },
        "challenges": [
            {
                "from": "devils_advocate",
                "to": "market_agent",
                "target_agent": "Market Realist",
                "challenge": "Hospitals take 18 months to close pilots; how does the startup survive?"
            }
        ],
        "rebuttals": [
            {
                "persona": "Market Realist",
                "rebuttal": "We target outpatient imaging centers first with 30-day closings.",
                "revised_position": "Focus on imaging center beachhead before Tier 1 enterprise."
            }
        ],
        "round_2": {
            "devils_advocate": {
                "persona": "Skeptical VC",
                "argument": "Outpatient strategy reduces initial sales cycle to viable window."
            }
        },
        "judge": {
            "verdict": "INVEST",
            "score": 82,
            "overall_score": 82,
            "overall_assessment": "Strong beachhead strategy mitigating hospital procurement friction.",
            "strengths": ["Massive market demand", "Defensible outpatient beachhead"],
            "weaknesses": ["GPU compute cost sensitivity"],
            "risks": ["HIPAA & regulatory compliance"],
            "recommendation": "Fund initial seed round conditioned on 3 signed clinic pilots."
        }
    }

    pdf_bytes = generate_evaluation_pdf(sample_data, startup_name="HealthSync AI")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    # Check standard PDF magic header
    assert pdf_bytes.startswith(b"%PDF-")


def test_pdf_generation_minimal_fallback():
    minimal_data = {
        "startup_name": "SimpleCo",
        "final_verdict": "REVIEW"
    }
    pdf_bytes = generate_evaluation_pdf(minimal_data)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF-")


def test_mcp_report_pdf_and_markdown():
    dossier = compile_executive_dossier(evaluation_id="eval_test", format="pdf")
    assert dossier["status"] == "ready"
    assert dossier["format"] == "pdf"
    assert "pdf_base64" in dossier
    assert len(dossier["pdf_base64"]) > 100

    summary = export_markdown_summary(evaluation_id="eval_test")
    assert summary["format"] == "markdown"
    assert "Executive Investment Committee Dossier" in summary["content"]
