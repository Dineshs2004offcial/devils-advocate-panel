import io
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


def generate_evaluation_pdf(evaluation_data: Dict[str, Any], startup_name: Optional[str] = None) -> bytes:
    """
    Generates a professional executive investment dossier PDF using ReportLab Platypus.
    Contains startup overview, round-by-round deliberation transcripts, cross-challenges,
    rebuttals, score breakdowns, and final lead judge verdict.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor("#0f172a") # Slate 900
    accent_blue = colors.HexColor("#1e40af")   # Blue 800
    accent_emerald = colors.HexColor("#065f46")# Emerald 800
    accent_amber = colors.HexColor("#92400e")  # Amber 800
    accent_red = colors.HexColor("#991b1b")    # Red 800
    text_dark = colors.HexColor("#1e293b")     # Slate 800
    text_muted = colors.HexColor("#64748b")    # Slate 500
    card_bg = colors.HexColor("#f8fafc")       # Slate 50
    border_color = colors.HexColor("#cbd5e1")  # Slate 300

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#ffffff"),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#93c5fd"),
        alignment=TA_CENTER
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=accent_blue,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        alignment=TA_LEFT
    )

    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=primary_color
    )

    quote_style = ParagraphStyle(
        'QuoteStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155")
    )

    # Normalize evaluation data
    eval_dict = evaluation_data.get("evaluation") or evaluation_data.get("result") or evaluation_data
    resolved_name = (
        startup_name or 
        evaluation_data.get("startup_name") or 
        eval_dict.get("startup_name") or 
        eval_dict.get("pitch", {}).get("startup_name") or 
        "Startup Venture"
    )
    
    judge = eval_dict.get("judge") or {}
    verdict = str(judge.get("verdict") or eval_dict.get("final_verdict", "REVIEW")).upper()
    if "INVEST" in verdict:
        verdict_badge_color = accent_emerald
        verdict_text = "INVEST"
    elif "REJECT" in verdict:
        verdict_badge_color = accent_red
        verdict_text = "REJECT"
    else:
        verdict_badge_color = accent_amber
        verdict_text = "FURTHER REVIEW"

    score = judge.get("score") if judge.get("score") is not None else judge.get("overall_score", 70)
    try:
        score_val = float(score)
    except (ValueError, TypeError):
        score_val = 70.0

    pitch_info = eval_dict.get("pitch") or {}
    if not isinstance(pitch_info, dict):
        pitch_info = {}

    story = []

    # 1. Header Banner
    header_text = f"<b>DEVIL'S ADVOCATE PANEL</b><br/><font size=14>Executive Investment Deliberation Dossier</font>"
    header_sub = f"Startup: <b>{resolved_name}</b> | Generated: {datetime.now(timezone.utc).strftime('%B %d, %Y - %H:%M UTC')} | Consensus Mode: Multi-Agent"
    
    header_table_data = [
        [Paragraph(header_text, title_style)],
        [Paragraph(header_sub, subtitle_style)]
    ]
    header_table = Table(header_table_data, colWidths=[540])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # 2. Executive Verdict Box
    assessment_text = judge.get("overall_assessment") or str(eval_dict.get("final_verdict") or "Comprehensive adversarial evaluation completed.")
    recommendation_text = judge.get("recommendation") or "Conduct targeted founder cross-examination on key unit economic sensitivities."

    verdict_summary_html = f"""
    <b>EXECUTIVE CONSENSUS:</b> <font color="{verdict_badge_color.hexval()}"><b>{verdict_text}</b></font> &nbsp;|&nbsp; 
    <b>OVERALL SCORE:</b> <font color="{verdict_badge_color.hexval()}"><b>{int(score_val)}/100</b></font><br/><br/>
    <b>Executive Synthesis:</b> {assessment_text}<br/><br/>
    <b>Strategic Action Plan:</b> {recommendation_text}
    """
    verdict_table = Table([[Paragraph(verdict_summary_html, body_style)]], colWidths=[540])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1.5, verdict_badge_color),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 10))

    # 3. Startup Overview Metadata Table
    story.append(Paragraph("1. Startup Pitch Overview", section_heading))
    overview_data = [
        [Paragraph("<b>Company / Project:</b>", bold_label), Paragraph(str(resolved_name), body_style)],
        [Paragraph("<b>Problem:</b>", bold_label), Paragraph(str(pitch_info.get("problem", "N/A")), body_style)],
        [Paragraph("<b>Solution:</b>", bold_label), Paragraph(str(pitch_info.get("solution", "N/A")), body_style)],
        [Paragraph("<b>Target Market:</b>", bold_label), Paragraph(str(pitch_info.get("target_market", "N/A")), body_style)],
        [Paragraph("<b>Business Model:</b>", bold_label), Paragraph(str(pitch_info.get("business_model", "N/A")), body_style)],
        [Paragraph("<b>Funding Target:</b>", bold_label), Paragraph(f"${pitch_info.get('funding_amount', 0):,.2f}" if isinstance(pitch_info.get("funding_amount"), (int, float)) else str(pitch_info.get("funding_amount", "N/A")), body_style)],
    ]
    ov_table = Table(overview_data, colWidths=[120, 420])
    ov_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(ov_table)
    story.append(Spacer(1, 10))

    # 4. Lead Judge Breakdown (Strengths, Weaknesses, Risks)
    strengths = judge.get("strengths") or []
    weaknesses = judge.get("weaknesses") or []
    risks = judge.get("risks") or []

    if strengths or weaknesses or risks:
        story.append(Paragraph("2. Strategic Diligence Assessment", section_heading))
        str_p = "<br/>".join([f"• {s}" for s in strengths]) if strengths else "None noted."
        weak_p = "<br/>".join([f"• {w}" for w in weaknesses]) if weaknesses else "None noted."
        risk_p = "<br/>".join([f"• {r}" for r in risks]) if risks else "None noted."

        analysis_data = [
            [Paragraph("<b>Key Strengths</b>", bold_label), Paragraph("<b>Key Weaknesses</b>", bold_label), Paragraph("<b>Critical Risks</b>", bold_label)],
            [Paragraph(str_p, body_style), Paragraph(weak_p, body_style), Paragraph(risk_p, body_style)],
        ]
        an_table = Table(analysis_data, colWidths=[180, 180, 180])
        an_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
            ('BACKGROUND', (0, 1), (-1, 1), card_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(an_table)
        story.append(Spacer(1, 10))

    # 5. Round 1 Agent Analyses Transcript
    round_1 = eval_dict.get("round_1") or {}
    if isinstance(round_1, dict) and round_1:
        story.append(Paragraph("3. Round 1: Multi-Agent Analysis Transcript", section_heading))
        for key, agent_info in round_1.items():
            if not isinstance(agent_info, dict):
                continue
            persona = agent_info.get("persona") or key.replace("_", " ").title()
            argument = agent_info.get("argument") or "No initial argument provided."
            ag_strengths = agent_info.get("strengths") or []
            ag_weaknesses = agent_info.get("weaknesses") or []
            ag_risks = agent_info.get("risks") or []
            ag_questions = agent_info.get("questions") or []

            card_content = f"<b>{persona.upper()}</b><br/>"
            card_content += f"<b>Main Argument:</b> {argument}<br/>"
            if ag_strengths:
                card_content += f"<b>Strengths:</b> {', '.join(ag_strengths)}<br/>"
            if ag_weaknesses:
                card_content += f"<b>Weaknesses:</b> {', '.join(ag_weaknesses)}<br/>"
            if ag_risks:
                card_content += f"<b>Risks:</b> {', '.join(ag_risks)}<br/>"
            if ag_questions:
                card_content += f"<b>Diligence Questions:</b> {'; '.join(ag_questions)}<br/>"

            ag_table = Table([[Paragraph(card_content, body_style)]], colWidths=[540])
            ag_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), card_bg),
                ('BOX', (0, 0), (-1, -1), 0.5, border_color),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(ag_table)
            story.append(Spacer(1, 6))

    # 6. Cross-Challenge Transcript
    challenges = eval_dict.get("challenges") or []
    if isinstance(challenges, list) and challenges:
        story.append(Spacer(1, 4))
        story.append(Paragraph("4. Adversarial Cross-Challenges Transcript", section_heading))
        ch_rows = [[Paragraph("<b>From Agent</b>", bold_label), Paragraph("<b>Target Agent</b>", bold_label), Paragraph("<b>Adversarial Challenge</b>", bold_label)]]
        for ch in challenges:
            if not isinstance(ch, dict):
                continue
            from_a = ch.get("from") or ch.get("from_agent") or "Agent"
            to_a = ch.get("target_agent") or ch.get("to") or ch.get("to_agent") or "Peer Agent"
            ch_text = ch.get("challenge") or ch.get("argument") or ""
            ch_rows.append([
                Paragraph(str(from_a).replace("_", " ").title(), body_style),
                Paragraph(str(to_a).replace("_", " ").title(), body_style),
                Paragraph(str(ch_text), quote_style)
            ])
        ch_table = Table(ch_rows, colWidths=[100, 110, 330])
        ch_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
            ('BACKGROUND', (0, 1), (-1, -1), card_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(ch_table)
        story.append(Spacer(1, 8))

    # 7. Rebuttals & Round 2 Refinements Transcript
    rebuttals = eval_dict.get("rebuttals") or []
    round_2 = eval_dict.get("round_2") or {}
    if rebuttals or round_2:
        story.append(Paragraph("5. Rebuttals & Round 2 Position Revisions", section_heading))
        if isinstance(rebuttals, list) and rebuttals:
            for reb in rebuttals:
                if not isinstance(reb, dict):
                    continue
                persona = reb.get("persona") or reb.get("agent", "Agent")
                reb_text = reb.get("rebuttal") or reb.get("defense") or ""
                rev_pos = reb.get("revised_position") or reb.get("adjusted_stance") or ""

                reb_content = f"<b>Rebuttal by {persona}:</b> {reb_text}<br/>"
                if rev_pos:
                    reb_content += f"<b>Revised Position:</b> {rev_pos}"

                reb_table = Table([[Paragraph(reb_content, body_style)]], colWidths=[540])
                reb_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(reb_table)
                story.append(Spacer(1, 4))

        if isinstance(round_2, dict) and round_2:
            for key, r2_data in round_2.items():
                if not isinstance(r2_data, dict):
                    continue
                persona = r2_data.get("persona") or key.replace("_", " ").title()
                arg = r2_data.get("argument") or ""
                r2_content = f"<b>Round 2 Synthesis ({persona}):</b> {arg}"
                r2_table = Table([[Paragraph(r2_content, body_style)]], colWidths=[540])
                r2_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), card_bg),
                    ('BOX', (0, 0), (-1, -1), 0.5, border_color),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(r2_table)
                story.append(Spacer(1, 4))

    # 8. Footer Note
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceAfter=8))
    footer_text = "CONFIDENTIAL INVESTMENT COMMITTEE MEMORANDUM • COMPILED VIA DEVIL'S ADVOCATE MULTI-AGENT ADVERSARIAL ENGINE"
    story.append(Paragraph(footer_text, ParagraphStyle(
        'FooterNotice',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=text_muted,
        alignment=TA_CENTER
    )))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
