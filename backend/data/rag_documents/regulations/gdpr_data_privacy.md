# GDPR & Data Privacy for B2B SaaS

## Baseline
GDPR (General Data Protection Regulation) has applied across the EU since 2018 and remains the anchor privacy framework any B2B SaaS company handling EU personal data must comply with, regardless of where the company itself is headquartered — extraterritorial reach is a defining feature of GDPR, not an edge case.

## GDPR Now Explicitly Covers AI Models Trained on Personal Data
The European Data Protection Board's Opinion 28/2024 (issued December 17, 2024) placed AI models trained on personal data squarely under GDPR scrutiny — directly relevant to any sales/marketing SaaS product using customer or prospect data to train or fine-tune AI features (e.g., predictive lead scoring, conversation-intelligence models).

## Enforcement Scale
EU data protection authorities issued approximately €1.2 billion in GDPR fines in 2024 alone, bringing the cumulative total since 2018 to roughly €5.88 billion — enforcement has not softened over time, and fine amounts have generally trended upward as authorities gain enforcement experience. The largest documented AI-specific GDPR fine to date is €30.5 million against Clearview AI (Dutch DPA, September 2024); Italy's data protection authority (Garante) issued a €15 million fine against OpenAI in December 2024, which was later overturned on appeal in March 2026 — illustrating that even major AI-specific GDPR enforcement actions can be successfully contested, not merely accepted as final.

## The "EU Headquarters = Compliant" Myth
Industry-specific commentary on conversation-intelligence tools (Gong/Chorus-category products) explicitly flags a common but incorrect assumption: having a European headquarters does not by itself establish GDPR compliance. The substantive compliance questions are where call audio/data is actually processed, which AI model provider(s) ingest transcripts as sub-processors, and whether the full sub-processor chain is auditable and would survive a Data Protection Impact Assessment (DPIA) review — headquarters location addresses tax domicile, not data-processing compliance.

## Works Council / DACH-Region Friction
In Germany, Austria, and France specifically, the recording bot/mechanism itself (for conversation-intelligence products) has become a primary procurement blocker, driven by works-council data-protection scrutiny that goes beyond baseline GDPR requirements — a specific regional go-to-market consideration for any conversation-intelligence or call-recording sales-tech product expanding into DACH markets.

## Practical Compliance Posture for a Sales/Marketing SaaS Startup
- Maintain GDPR Article 30 records of processing activities from the start (a specifically cited gap for startups still working toward SOC 2 Type II, per compliance-industry sources)
- Map every AI feature that touches personal data against GDPR Article 22 (automated decision-making) exposure
- Treat sub-processor transparency (naming exactly which AI model providers process customer/prospect data) as a first-class sales-enablement asset for enterprise deals, not just a legal-team artifact

Sources: RevenueGrid "7 GDPR-Compliant Alternatives to Gong and Chorus" (EDPB Opinion 28/2024, DACH works-council detail); Wavect "GDPR + EU AI Act Stacking" (English and Spanish editions, 2026); TraeAI compliance-frameworks resource (fine figures, Clearview AI and OpenAI/Garante cases).
