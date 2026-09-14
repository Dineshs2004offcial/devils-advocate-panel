# AI Regulation: EU AI Act and Global Landscape (2026)

## EU AI Act — Applies to US SaaS Companies Too
Regulation (EU) 2024/1689, the EU AI Act, has extraterritorial reach: if any of a company's paying customers, or those customers' end users, are located in the EU, the Act's obligations can apply regardless of where the company is headquartered or where its servers are located (Article 2 scope) — a US-based sales/marketing SaaS company selling to any EU customer should assume applicability rather than assuming it is out of scope by virtue of being a US company.

## Enforcement Timeline
- In force since August 1, 2024 (prohibited-practice bans and AI-literacy duties already apply; GPAI/general-purpose-AI-model rules are active now)
- Article 50 transparency obligations begin August 2, 2026
- Stand-alone high-risk system obligations begin December 2, 2027
- Product-embedded high-risk system obligations begin August 2, 2028
This phased timeline means compliance planning needs to be staged against specific future dates, not treated as a single "go live" event.

## Penalty Structure
Two-tier fine ceiling: up to €15 million or 3% of global annual turnover for high-risk-system obligation violations (Art. 99(4)); up to €35 million or 7% of global annual turnover for prohibited AI practices (Art. 99(3)) — the 7% ceiling for prohibited practices is a materially larger maximum penalty than GDPR's already-substantial fine structure.

## How the AI Act Differs From GDPR (A Common Founder Misconception)
Most US founders' mental model of the EU AI Act is borrowed from GDPR experience — expecting something like "a few cookie banners, a privacy-policy update, maybe a Data Processing Addendum." The AI Act is structurally different: it regulates the *product* itself, not just the data it processes. It assigns distinct obligations by role (provider, deployer, distributor, importer, authorized representative) and imposes pre-market conformity assessments, technical documentation requirements, post-market monitoring, and EU-database registration before a high-risk system can lawfully reach a European user.

## Which Sales/Marketing SaaS Use Cases Risk "High-Risk" Classification
For most B2B SaaS specifically, the practical high-risk exposure comes through Annex III categories most relevant to this space: employment/worker-management features (e.g., AI-driven rep performance scoring or coaching tools that materially affect employment decisions), and credit-scoring/pricing-decision features if a product's outputs materially influence consumer-facing pricing or credit decisions. Pure B2B sales-engagement/CRM features (cadence sequencing, lead scoring for a company's own prospects) are less likely to fall into Annex III high-risk categories than employment-decision or credit/insurance-pricing features specifically.

## US State-Level AI Regulation (Complementary, Not a Substitute)
Colorado's AI Act (effective June 30, 2026, delayed by SB25B-004) and Virginia's comparable law require impact assessments for high-risk AI systems in credit, employment, housing, and education contexts — see the CCPA/US Privacy document for detail on how these interact with existing state privacy law.

## Compliance Cost Data Point
Retrofitting AI Act compliance artifacts into an already-built product is estimated to add 10-20% additional engineering time; building the same artifacts in from the architecture stage costs closer to 3-5% marginal engineering time — a strong practical argument for addressing AI Act compliance requirements during initial product architecture rather than after a feature ships.

Sources: Beancount.io "The EU AI Act Lands on U.S. SaaS Companies This August: A Practical Compliance Guide"; Wavect "GDPR + EU AI Act Stacking" (English and Spanish editions); TraeAI compliance-frameworks resource (penalty structure, Colorado/Virginia detail, retrofitting-cost estimate).
