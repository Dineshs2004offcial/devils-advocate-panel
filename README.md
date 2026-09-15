# 😈 Devil's Advocate Panel

> **Pitch your idea. Get challenged by AI investors who won't go easy on you.**

Devil's Advocate Panel is a **multi-agent AI startup evaluation system** that stress-tests business ideas, startup pitches, business models, and financial assumptions.

Instead of relying on a single AI response, the system uses multiple specialized AI perspectives:

- 🧑‍💼 **Skeptical VC** — challenges scalability, competition, assumptions, and investment risks
- 💰 **Financial Analyst** — evaluates revenue, costs, profitability, and funding risks
- 📊 **Market Analyst** — evaluates market opportunity, customer demand, competition, and market risks
- ⚖️ **AI Reviewer** — combines the agent analyses and produces a final investment recommendation

The project is built using FastAPI, LangChain, LangGraph, RAG, PostgreSQL, MCP, and multiple LLM providers.

---

 🚀 What Does It Do?

A user submits a startup pitch containing:

- Startup name
- Problem
- Solution
- Target market
- Business model
- Funding requirement

The system sends the pitch to multiple AI agents.

 Current workflow

'
                Startup Pitch
                     │
                     ▼
                FastAPI API
                     │
                     ▼
              AI Agent Panel
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Market      Financial   Devil's
      Analyst     Analyst     Advocate
          │          │          │
          └──────────┼──────────┘
                     ▼
               AI Reviewer
                     │
                     ▼
              Final Verdict


The goal is to identify weaknesses that a founder may overlook before presenting an idea to investors.

---

# 🧠 How It Works

## 1. User submits a pitch

The user sends a startup pitch to the FastAPI backend.

Example:


{
  "startup_name": "EcoKart",
  "problem": "Plastic waste from online shopping is increasing.",
  "solution": "An online marketplace for eco-friendly products with sustainable packaging.",
  "target_market": "Environment-conscious urban consumers and Gen Z.",
  "business_model": "Seller commission and premium customer subscription.",
  "funding_amount": 500000
}


## 2. Market Analyst

The Market Analyst evaluates:

- Market opportunity
- Customer demand
- Competition
- Market risks

---

## 3. Financial Analyst

The Financial Analyst evaluates:

- Revenue potential
- Cost considerations
- Profitability
- Funding risks
- Financial weaknesses

---

## 4. Devil's Advocate

The Devil's Advocate aggressively challenges the startup.

It looks for:

- Critical assumptions
- Weaknesses
- Failure scenarios
- Competitive threats
- Reasons the startup could fail
- Questions investors should ask

---

## 5. AI Reviewer

The final AI reviewer receives the three analyses and produces:

- Overall assessment
- Key strengths
- Major risks
- Investment recommendation
- Short reasoning

Possible recommendations:
INVEST
REVIEW
REJECT


# ⚔️ Planned Multi-Agent Debate Loop

The project architecture is being extended toward a deeper debate workflow:


Research
   │
   ▼
⚔️ Debate Round 1
   │
   ▼
Cross Challenge
   │
   ▼
🔄 Rebuttal
   │
   ▼
⚔️ Debate Round 2
   │
   ▼
⚖️ AI Judge
   │
   ▼
🏆 Final Verdict


### Debate Round 1

Each agent independently analyzes the startup.

### Cross Challenge

Agents challenge assumptions made by the other agents.

### Rebuttal

Agents respond to the challenges and revise their positions.

### Debate Round 2

Agents perform a second analysis using the previous arguments, challenges, rebuttals, and research.

### AI Judge

The judge evaluates the complete debate and produces the final verdict.

> **Status:** The multi-round debate loop is part of the project's development roadmap and should only be marked as fully implemented after the LangGraph loop is integrated into the production evaluation path.

---

# 🤖 AI Models

The project supports multiple LLM providers.

## Primary Model

The current AI service first attempts to use **Google Gemini**.

The configured default model is:

gemini-3.6-flash


If that model fails, the service attempts fallback Gemini models:


gemini-2.5-flash
gemini-1.5-flash
gemini-1.5-pro


The project then falls back to OpenAI when a Google/Gemini provider is unavailable.

The current implementation reads the Gemini model from:

GEMINI_MODEL=gemini-3.6-flash


And the OpenAI model from:


OPENAI_MODEL=gpt-4o-mini


The LLM factory also supports:

- Gemini
- OpenAI
- Mistral
- Groq
- OpenRouter

---

# ❓ Why Gemini?

Gemini is used as the primary provider because the project needs an LLM that can efficiently handle repeated startup-analysis prompts across multiple agents.

The application also implements provider fallback so the evaluation workflow is less dependent on a single LLM provider.

The architecture allows the model to be changed through environment variables without rewriting the agents.

For example:

GEMINI_MODEL=your-model


This makes the LLM layer configurable.



# 🔌 MCP

The project contains an MCP layer for connecting AI agents with external tools and data.

Current MCP structure:

app/
└── mcp/
    ├── client.py
    ├── filesystem.py
    ├── postgres.py
    └── web.py

### MCP Components

| Component | Purpose |
|---|---|
| `client.py` | MCP client integration |
| `filesystem.py` | File/knowledge-base access |
| `postgres.py` | PostgreSQL-related access |
| `web.py` | Web research integration |

The purpose of MCP is to separate AI reasoning from external tool access.

Conceptually:

AI Agent
   │
   ▼
MCP Client
   │
   ├── Web Research
   ├── Filesystem
   └── PostgreSQL



# 📚 RAG

The project also contains a Retrieval-Augmented Generation pipeline.


Knowledge Base
      │
      ▼
Document Ingestion
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
Vector Search
      │
      ▼
Relevant Context
      │
      ▼
AI Agent


The current embedding implementation uses:


sentence-transformers/all-MiniLM-L6-v2


with normalized embeddings on CPU.

RAG allows relevant knowledge to be retrieved and supplied to the AI workflow instead of relying entirely on the model's internal knowledge.


🏗️ Architecture


flowchart

    A[👤 User] --> B[FastAPI]

    B --> C[AI Agent Panel]

    C --> D[📊 Market Analyst]
    C --> E[💰 Financial Analyst]
    C --> F[😈 Devil's Advocate]

    D --> G[⚖️ AI Reviewer]
    E --> G
    F --> G

    G --> H[🏆 Final Verdict]

    I[RAG Knowledge Base] --> C
    J[MCP Tools] --> C
    K[(PostgreSQL)] --> C



# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend language |
| FastAPI | REST API |
| LangChain | LLM application framework |
| LangGraph | Agent workflow/orchestration |
| Google Gemini | Primary LLM provider |
| OpenAI | LLM fallback/alternative |
| Mistral | Alternative LLM provider |
| Groq | Alternative LLM provider |
| OpenRouter | Alternative model routing |
| RAG | Knowledge retrieval |
| ChromaDB | Vector database support |
| Sentence Transformers | Embeddings |
| PostgreSQL | Application database |
| SQLAlchemy | Database ORM |
| MCP | External tool integration |
| Streamlit | Current frontend/demo entry point |

The repository's dependency file includes FastAPI, Uvicorn, Streamlit, LangChain, LangGraph, provider integrations, PostgreSQL drivers, pgvector, Tavily, ChromaDB, and Sentence Transformers. :contentReference[oaicite:2]{index=2}


# 📁 Project Structure


devils-advocate-panel/
│
├── backend/
│   └── app/
│       │
│       ├── agents/
│       │   ├── financial_agent.py
│       │   ├── market_agent.py
│       │   ├── devils_advocate.py
│       │   └── panel.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── prompts.py
│       │
│       ├── graph/
│       │
│       ├── llm/
│       │   ├── gemini.py
│       │   ├── openai.py
│       │   ├── mistral.py
│       │   └── factory.py
│       │
│       ├── mcp/
│       │   ├── client.py
│       │   ├── filesystem.py
│       │   ├── postgres.py
│       │   └── web.py
│       │
│       ├── rag/
│       │   ├── ingestion.py
│       │   ├── chunking.py
│       │   ├── embeddings.py
│       │   └── retriever.py
│       │
│       ├── routes/
│       │   ├── user.py
│       │   ├── pitch.py
│       │   └── evaluation.py
│       │
│       ├── schemas/
│       │
│       ├── services/
│       │
│       └── main.py
│
├── data/
│   └── knowledge_base/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── streamlit_app.py
└── README.md


The repository currently contains the backend, knowledge-base data, tests, Docker configuration, requirements, and Streamlit entry point. :contentReference[oaicite:3]{index=3}



# 🔐 Environment Variables

Create a `.env` file inside the backend/project environment.

## LLM Configuration

### Gemini

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash


GOOGLE_API_KEY can also be used by the current AI service as an alternative name for the Gemini key.

### OpenAI

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini


### Mistral

MISTRAL_API_KEY=your_mistral_api_key
MISTRAL_MODEL=mistral-small-latest

### Groq

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b


### OpenRouter

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openrouter/free


The project configuration defines these provider keys and model defaults, while the LLM factory selects the requested provider. :contentReference[oaicite:4]{index=4}


## Database


DATABASE_URL=postgresql+pg8000://username:password@localhost:5432/devils_advocate


If `DATABASE_URL` is not provided, the current code contains a local PostgreSQL fallback configuration.

**Do not commit your real database password or API keys.**

Add `.env` to `.gitignore`.

---

# ⚙️ Installation

## 1. Clone the repository


git clone https://github.com/Dineshs2004offcial/devils-advocate-panel.git
cd devils-advocate-panel


## 2. Create a virtual environment

### Windows


python -m venv venv
venv\Scripts\activate


### Linux / macOS


python3 -m venv venv
source venv/bin/activate


## 3. Install dependencies


pip install -r requirements.txt


---

# 🔑 Configure Environment Variables

Create:

.env


Example:


GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash

OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini

DATABASE_URL=postgresql+pg8000://postgres:password@localhost:5432/devils_advocate


Only configure the providers you actually want to use.

---

# ▶️ Run the Backend

Move into the backend directory:


cd backend


Start FastAPI:


uvicorn app.main:app --reload


The API will normally be available at:


http://127.0.0.1:8000


Swagger API documentation:


http://127.0.0.1:8000/docs


The application exposes health endpoints including:


GET /
GET /health


The current FastAPI application also registers pitch and evaluation routes. :contentReference[oaicite:5]{index=5}

---

# 📡 API Endpoints

## Submit Pitch


POST /pitch/


or:

```http
POST /pitch
```

## Evaluate Startup


POST /evaluation/


The current evaluation endpoint accepts the startup pitch and passes it to the agent panel. :contentReference[oaicite:6]{index=6}

---

# 🧪 Sample Input


{
  "startup_name": "EcoKart",
  "problem": "Plastic waste from online shopping is increasing.",
  "solution": "An online marketplace for eco-friendly products with sustainable packaging.",
  "target_market": "Environment-conscious urban consumers and Gen Z.",
  "business_model": "Seller commission and premium customer subscription.",
  "funding_amount": 500000
}




# 📤 Sample Output

A simplified response looks like:

`
{
  "startup_name": "EcoKart",
  "evaluation": {
    "market_analysis": {
      "agent": "Market Analyst",
      "analysis": "..."
    },
    "financial_analysis": {
      "agent": "Financial Analyst",
      "analysis": "..."
    },
    "devils_advocate": {
      "agent": "Devil's Advocate",
      "analysis": "..."
    },
    "final_verdict": "..."
  }
}


The current panel implementation runs the market, financial, and Devil's Advocate analyses before asking the final reviewer to produce a recommendation. :contentReference[oaicite:7]{index=7}

---

# 🖥️ Frontend

The repository currently contains:


streamlit_app.py


The planned product interface is a one-page AI dashboard containing:


┌──────────────────────────────────────────────┐
│ 😈 Devil's Advocate Panel                   │
├──────────────┬───────────────────────────────┤
│ Recent       │ Startup Pitch                 │
│ Evaluations  │                               │
│              │ ⚔️ Agent Analysis             │
│ + New Chat   │                               │
│              │ 💰 Financial                  │
│ EcoKart      │ 📊 Market                     │
│ HealthAI     │ 😈 Devil's Advocate           │
│ FinTech      │                               │
│              │ ⚖️ Final Verdict              │
└──────────────┴───────────────────────────────┘


The frontend can be extended to display the multi-round debate workflow and MCP connector status.



# 🧪 Testing

The project contains a test structure for areas including:


tests/
├── test_agents.py
├── test_gemini.py
├── test_rag.py
├── test_graph.py
└── test_tools.py


Run tests with:

pytest

---

# 🔄 AI Provider Fallback

The project includes an LLM fallback mechanism.

The current AI service attempts:


1. Gemini
      ↓
2. Alternative Gemini models
      ↓
3. OpenAI
      ↓
4. Graceful fallback response


This helps the application continue operating when a configured provider or model fails.

The provider factory additionally supports Gemini, OpenAI, Mistral, Groq, and OpenRouter. :contentReference[oaicite:8]{index=8}

---

# 📊 RAG Embeddings

The current RAG embedding implementation uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

and runs embeddings on CPU with normalized vectors. :contentReference[oaicite:9]{index=9}

---

# 🔮 Future Improvements

Planned improvements include:

- ⚔️ Multi-round agent debate
- 🔄 Cross-agent challenge and rebuttal loop
- ⚖️ Dedicated impartial judge agent
- 📡 Streaming agent responses
- 🔌 More MCP connectors
- 📄 Automated PDF reports
- 📊 Evaluation comparison
- 💾 Evaluation history
- 🔐 Authentication
- 🚀 Production deployment
- 🎨 Advanced one-page frontend dashboard

---

# 🛡️ Security

Never commit:


.env
API keys
Database passwords
Access tokens
Private credentials

Use environment variables for all secrets.

---

# 📌 Project Status

| Component | Status |
|---|---|
| FastAPI backend | ✅ Implemented |
| Startup pitch API | ✅ Implemented |
| Market Agent | ✅ Implemented |
| Financial Agent | ✅ Implemented |
| Devil's Advocate Agent | ✅ Implemented |
| AI Reviewer | ✅ Implemented |
| Gemini integration | ✅ Implemented |
| OpenAI fallback | ✅ Implemented |
| RAG components | 🚧 In Progress |
| MCP layer | 🚧 In Progress |
| Multi-round debate loop | 🚧 In Progress |
| Cross Challenge | 🚧 In Progress |
| Rebuttal loop | 🚧 In Progress |
| One-page advanced frontend | 🚧 In Progress |
| PDF reporting | 🔮 Planned |

---

# 👨‍💻 Author

* DINESH S *

GitHub:

https://github.com/Dineshs2004offcial

Repository:

https://github.com/Dineshs2004offcial/devils-advocate-panel

---

# ⭐ Why This Project?

Traditional startup evaluation often depends on a single opinion.

Devil's Advocate Panel takes a different approach:



The goal is not simply to tell a founder that their idea is good.

The goal is to **find the reasons it might fail before the market does.
