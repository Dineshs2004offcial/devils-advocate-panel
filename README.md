# Devil's Advocate Panel

An adversarial multi-agent AI system designed to simulate an elite Venture Capital investment committee to stress-test startup pitches, business models, financial projections, and market dynamics.

---

## 1. What the Project Does

The **Devil's Advocate Panel** subjects startup pitches to rigorous, multi-perspective adversarial debate before an AI Judge renders a final investment verdict.

### Core Agent Roles
* **VC / Skeptical Agent**: Identifies operational vulnerabilities, valuation red flags, defensibility deficits, and capital inefficiency.
* **Financial Analyst Agent**: Audits unit economics, CAC/LTV dynamics, gross margins, cash burn rate, and financial sustainability.
* **Market Realist Agent**: Evaluates TAM/SAM/SOM, market saturation, incumbent moats, customer acquisition friction, and regulatory risks.
* **AI Judge / Final Evaluator**: Weighs cross-agent debate, web research, and RAG data to render an objective verdict with dynamic scoring (0–100) and actionable recommendations.

### Key Features
* **Stateful Multi-Agent Debate Loop (LangGraph)**: Orchestrates a multi-round debate pipeline:
  $$\text{Web/RAG Research} \longrightarrow \text{Round 1 Analysis} \longrightarrow \text{Cross-Challenge} \longrightarrow \text{Rebuttal} \longrightarrow \text{Round 2 Refinement} \longrightarrow \text{AI Judge Verdict}$$
* **MCP (Model Context Protocol) Connectors**:
  * **Web Research MCP**: Real-time web intelligence via DuckDuckGo / Tavily API.
  * **Knowledge Base MCP**: Local RAG vector store powered by ChromaDB.
  * **PostgreSQL MCP**: Persistent pitch history, debate transcripts, and evaluation sessions.
  * **Executive Report MCP**: PDF, HTML, and Markdown executive dossier exporter.
* **Modern React 19 Dashboard**: High-tech Vite dashboard featuring live multi-agent panel cards, workflow timeline indicators, transcript inspector, pitch comparison modal, and MCP status monitor.
* **Streamlit UI**: Backup web application interface (`streamlit_app.py`).

---

## 2. How to Run It (Both Backend and Frontend Setup Process)

### Prerequisites
* **Python**: 3.10 or higher
* **Node.js**: v18 or higher (npm v9+)
* **PostgreSQL** *(Optional)*: Required for persistent SQL database storage (fallback memory engine available)

---

### Backend Setup Process

1. **Navigate to the Project Root**:
   ```bash
   cd devils_advocate_panel
   ```

2. **Create and Activate a Virtual Environment**:
   * **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Backend Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (see Section 4 for variable details).

5. **Start the FastAPI Backend Server**:
   ```bash
   python -m uvicorn backend.app.main:app --reload --port 8000
   ```
   * **API Base URL**: `http://localhost:8000`
   * **Interactive Swagger Documentation**: `http://localhost:8000/docs`

---

### Frontend Setup Process

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Node Dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vite Development Server**:
   ```bash
   npm run dev
   ```
   * **Frontend App URL**: `http://localhost:5173`

---

### Alternative Streamlit Setup (Optional)

To run the lightweight single-page Streamlit interface:
```bash
# From the project root with venv activated
streamlit run streamlit_app.py
```

---

## 3. What AI Model Used and Y

The Devil's Advocate Panel employs a **multi-tiered LLM routing architecture** combining high-speed open-weights inference and proprietary models:

### Models Used
* **Groq (LLaMA 3.3 70B Versatile / LLaMA 3.1)**: Primary fast-inference model for multi-agent node executions.
* **Google Gemini (Gemini 1.5 Flash / Gemini 3.6 Flash)**: Primary model for deep research synthesis, RAG document processing, and structured context reasoning.
* **OpenAI (GPT-4o / GPT-4o-mini)**: High-accuracy model for final evaluation synthesis and deterministic JSON schema validation.
* **OpenRouter**: Open gateway provider for fallback routing across open-source model providers.

### Why These Models Were Selected
1. **Groq (LLaMA 3.3 70B)**:
   * **Sub-Second Latency**: Multi-agent debate loops require multiple sequential and parallel LLM invocations per pitch. Groq delivers response times under 500ms per turn, eliminating UI latency bottlenecks.
2. **Google Gemini (Gemini 1.5 / 3.6 Flash)**:
   * **Context Window & Cost Efficiency**: Large context capabilities allow processing web search snippets, vector store documents, and long pitch submissions without truncation.
3. **OpenAI (GPT-4o / GPT-4o-mini)**:
   * **Structured Scoring Precision**: Exceptional adherence to complex JSON response formats required for evaluation scoring, risk metrics, and verdict synthesis.
4. **Cascading Fallback Resilience (`invoke_with_fallback` & `ask_ai`)**:
   * To prevent failure from API rate limits or network outages, the system executes an automated failover chain:
     $$\text{Groq} \longrightarrow \text{Gemini} \longrightarrow \text{OpenAI} \longrightarrow \text{OpenRouter} \longrightarrow \text{Structured Fallback}$$

---

## 4. What are the Env Vars and Y We Need

Environment variables are defined in the root `.env` file to control API authentication, database connections, and model selections:

| Environment Variable | Description | Why It Is Needed |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | Groq API Key | Authenticates Groq for ultra-low latency LLaMA 3.3 agent execution across debate rounds. |
| `GOOGLE_API_KEY` / `GEMINI_API_KEY` | Google Gemini API Key | Authenticates Google AI Studio for Gemini Flash model calls in RAG and web research synthesis. |
| `OPENAI_API_KEY` | OpenAI API Key | Authenticates OpenAI services for GPT-4o final verdict evaluation and JSON formatting. |
| `MISTRAL_API_KEY` | Mistral AI API Key | Enables Mistral model integration for alternative reasoning benchmarks. |
| `OPENROUTER_API_KEY` | OpenRouter API Key | Provides fallback access to open-weights LLMs via OpenRouter's unified endpoint. |
| `DATABASE_URL` | PostgreSQL Connection URI | Configures Database Connection (`postgresql+pg8000://...`) to persist user profiles, pitches, debate transcripts, and evaluation logs. |
| `CHROMA_PERSIST_DIR` | Directory Path (`./data/chroma_db`) | Specifies local storage path for ChromaDB vector embeddings used in RAG document retrieval. |
| `EMBEDDING_MODEL` | HuggingFace Model String | Sets the embedding model (`sentence-transformers/all-MiniLM-L6-v2`) used to chunk and vectorize business knowledge files. |
| `TAVILY_API_KEY` | Tavily Web Search Key | Enables real-time web search MCP tool integration for market intelligence and competitor discovery. |

---

## 5. Project Folder Structure and Architecture and Explanation

### Folder Structure

```text
devils_advocate_panel/
├── .env                    # Environment variables configuration
├── docker-compose.yml      # Docker container configuration
├── Dockerfile              # Container build specifications
├── requirements.txt        # Root Python dependencies
├── streamlit_app.py        # Backup Streamlit dashboard application
│
├── backend/                # FastAPI Backend Application
│   ├── requirements.txt    # Backend Python package requirements
│   └── app/
│       ├── main.py         # FastAPI application entrypoint & CORS middleware
│       ├── ai_service.py   # Fallback LLM invocation engine (ask_ai)
│       ├── database.py     # SQLAlchemy DB session setup
│       ├── models.py       # SQLAlchemy ORM models (User, Pitch, Evaluation)
│       ├── schemas.py      # Pydantic data schemas & request/response validation
│       │
│       ├── agents/         # AI Agent Implementations
│       │   ├── devils_advocate.py   # VC / Skeptical Agent logic
│       │   ├── financial_agent.py   # Financial Analyst Agent logic
│       │   ├── market_agent.py      # Market Realist Agent logic
│       │   ├── final_evaluator.py   # AI Judge verdict & scoring engine
│       │   └── panel.py             # Agent execution coordinator
│       │
│       ├── graph/          # LangGraph Workflow Orchestration
│       │   ├── state.py    # DebateState TypedDict definition
│       │   ├── nodes.py    # Multi-agent debate nodes (research, rounds 1 & 2, judge)
│       │   └── graph.py    # LangGraph StateGraph builder & conditional loops
│       │
│       ├── llm/            # LLM Provider Integrations & Factory
│       │   ├── factory.py  # LLM provider factory & fallback runner
│       │   ├── gemini.py   # Google Gemini provider initialization
│       │   ├── mistral.py  # Mistral AI provider initialization
│       │   └── openai.py   # OpenAI provider initialization
│       │
│       ├── mcp/            # Model Context Protocol Connectors
│       │   ├── client.py   # MCP Client connection manager
│       │   ├── server.py   # Local MCP server instance
│       │   ├── web.py      # Web research MCP tool (DuckDuckGo / Tavily)
│       │   ├── postgres.py # Database health & MCP storage queries
│       │   └── filesystem.py # Knowledge base file inspection tool
│       │
│       ├── rag/            # Retrieval-Augmented Generation Engine
│       │   ├── chunking.py   # Document chunking logic
│       │   ├── embeddings.py # SentenceTransformer embedding loader
│       │   ├── ingestion.py  # Vector ingestion into ChromaDB
│       │   └── retriever.py  # Context retriever for knowledge documents
│       │
│       └── routes/         # FastAPI REST API Endpoints
│           ├── evaluation.py # Pitch evaluation & MCP status routes
│           ├── pitch.py      # Pitch creation & retrieval routes
│           └── user.py       # User management routes
│
├── frontend/               # React 19 + Vite Frontend Application
│   ├── package.json        # Frontend Node dependencies & scripts
│   ├── vite.config.js      # Vite build configuration
│   ├── index.html          # HTML entrypoint
│   └── src/
│       ├── main.jsx        # React root renderer
│       ├── App.jsx         # Main application container
│       ├── index.css       # Design tokens, custom animations, glassmorphism CSS
│       ├── pages/
│       │   └── Dashboard.jsx # Main executive evaluation dashboard
│       └── components/
│           ├── AgentCard.jsx         # Individual agent status card
│           ├── AgentPanelGrid.jsx    # Live 4-agent committee grid
│           ├── AnalysisCard.jsx      # Agent breakdown panel
│           ├── ChatPitchInput.jsx    # Pitch submission & template selector
│           ├── ComparisonModal.jsx   # Multi-pitch comparison tool
│           ├── McpPanel.jsx          # Live MCP server status monitor
│           ├── PitchForm.jsx         # Form pitch input component
│           ├── ScoreDashboard.jsx    # Score gauge & breakdown visualization
│           ├── Sidebar.jsx           # Application navigation sidebar
│           ├── TranscriptModal.jsx   # Interactive debate transcript inspector
│           └── VerdictCard.jsx       # Final AI Judge verdict presentation
│
├── data/                   # Data Storage Directory
│   ├── chroma_db/          # Persistent ChromaDB vector database files
│   └── knowledge_base/     # Benchmark business models & startup pitch docs
│
└── docs/                   # System Documentation
    └── langchain-langgraph.md # LangChain & LangGraph integration guide
```

---

### System Architecture & Explanation

```text
                               ┌──────────────────────────┐
                               │  React 19 + Vite Dashboard │
                               └────────────┬─────────────┘
                                            │ REST API
                                            ▼
                               ┌──────────────────────────┐
                               │     FastAPI Backend      │
                               └────────────┬─────────────┘
                                            │
                                            ▼
                               ┌──────────────────────────┐
                               │ LangGraph Debate Engine  │
                               └────────────┬─────────────┘
                                            │
         ┌──────────────────────────────────┼──────────────────────────────────┐
         │                                  │                                  │
         ▼                                  ▼                                  ▼
┌─────────────────┐                ┌──────────────────┐               ┌─────────────────┐
│ Web Research MCP│                │  ChromaDB RAG    │               │  PostgreSQL DB  │
│ (Tavily/DDG)    │                │ (Vector Storage) │               │(Persisted Data) │
└─────────────────┘                └──────────────────┘               └─────────────────┘
```

#### LangGraph Stateful Multi-Agent Execution Flow

1. **`research_node`**: Fetches market data using the Web Research MCP and queries the ChromaDB Vector Store for industry benchmarks.
2. **`round_1_node`**: Executes independent assessments simultaneously across the VC Skeptic, Financial Analyst, and Market Realist agents.
3. **`cross_challenge_node`**: Agents review peer findings and construct counter-arguments targeting weaknesses in other agents' assumptions.
4. **`rebuttal_node`**: Agents defend or modify their initial positions based on received challenges.
5. **`round_2_node`**: Agents refine their assessments incorporating debate insights and counter-evidence.
6. **`loop_controller_node`**: Evaluates debate constraints (`max_rounds = 2`). If rounds remain, loops back to challenge; otherwise proceeds to final verdict.
7. **`judge_node`**: The AI Judge synthesizes the complete debate transcript, research brief, and agent scores to render the final investment decision.
