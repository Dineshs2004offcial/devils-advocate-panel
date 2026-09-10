# Devil's Advocate Panel

A multi-agent AI panel designed to challenge, stress-test, and rigorously evaluate startup pitches, business plans, and financial models.

## Project Structure

```text
devils_advocate_panel/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── prompts.py
│   │   │
│   │   ├── graph/
│   │   │   ├── state.py
│   │   │   ├── main_graph.py
│   │   │   │
│   │   │   └── subgraphs/
│   │   │       │
│   │   │       ├── router/
│   │   │       │   ├── state.py
│   │   │       │   ├── nodes.py
│   │   │       │   └── graph.py
│   │   │       │
│   │   │       ├── supervisor/
│   │   │       │   ├── state.py
│   │   │       │   ├── nodes.py
│   │   │       │   └── graph.py
│   │   │       │
│   │   │       ├── vc/
│   │   │       │   ├── state.py
│   │   │       │   ├── nodes.py
│   │   │       │   ├── prompts.py
│   │   │       │   └── graph.py
│   │   │       │
│   │   │       ├── financial/
│   │   │       │   ├── state.py
│   │   │       │   ├── nodes.py
│   │   │       │   ├── prompts.py
│   │   │       │   └── graph.py
│   │   │       │
│   │   │       ├── market/
│   │   │       │   ├── state.py
│   │   │       │   ├── nodes.py
│   │   │       │   ├── prompts.py
│   │   │       │   └── graph.py
│   │   │       │
│   │   │       └── evaluator/
│   │   │           ├── state.py
│   │   │           ├── nodes.py
│   │   │           ├── prompts.py
│   │   │           └── graph.py
│   │   │
│   │   ├── llm/
│   │   │   ├── gemini.py
│   │   │   ├── openai.py
│   │   │   ├── mistral.py
│   │   │   └── factory.py
│   │   │
│   │   ├── rag/
│   │   │   ├── ingestion.py
│   │   │   ├── chunking.py
│   │   │   ├── embeddings.py
│   │   │   ├── retriever.py
│   │   │   ├── hybrid_search.py
│   │   │   └── reranker.py
│   │   │
│   │   ├── tools/
│   │   │   ├── calculator.py
│   │   │   ├── financial.py
│   │   │   ├── web_search.py
│   │   │   └── scraper.py
│   │   │
│   │   ├── mcp/
│   │   │   ├── client.py
│   │   │   ├── postgres.py
│   │   │   ├── web.py
│   │   │   └── filesystem.py
│   │   │
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── models.py
│   │   │   ├── repositories.py
│   │   │   └── migrations/
│   │   │
│   │   ├── schemas/
│   │   │   ├── pitch.py
│   │   │   ├── agent.py
│   │   │   ├── session.py
│   │   │   └── verdict.py
│   │   │
│   │   ├── services/
│   │   │   ├── pitch_service.py
│   │   │   ├── research_service.py
│   │   │   ├── evaluation_service.py
│   │   │   └── pdf_service.py
│   │   │
│   │   └── utils/
│   │       ├── helpers.py
│   │       └── validators.py
│   │
│   ├── tests/
│   │   ├── test_gemini.py
│   │   ├── test_agents.py
│   │   ├── test_rag.py
│   │   ├── test_graph.py
│   │   └── test_tools.py
│   │
│   ├── requirements.txt
│   ├── .env
│   └── .gitignore
│
├── data/
│   └── knowledge_base/
│       ├── startup/
│       ├── finance/
│       ├── market/
│       └── vc/
│
├── streamlit_app.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```
