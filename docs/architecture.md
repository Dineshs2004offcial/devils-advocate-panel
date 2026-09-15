# System Architecture

Devil's Advocate Panel is an AI-powered startup pitch evaluation system.

```text
React Frontend
      |
      v
FastAPI Backend
      |
      v
LangGraph Orchestrator
      |
      +--> VC Agent
      +--> Financial Agent
      +--> Market Agent
      +--> Devil's Advocate Agent
      |
      v
Debate / Rebuttal Loop
      |
      v
Final Evaluator
      |
      v
Structured Verdict
      |
      v
Frontend Dashboard
```

## Main Layers

- Frontend — React/Vite interface
- Routes — FastAPI HTTP endpoints
- Agents — specialized AI reasoning roles
- Graph — LangGraph workflow and state
- MCP — external tool/data access
- RAG — retrieval and knowledge augmentation
- Database — persistent application data
- Schemas — request/response validation
- Tests — agent and graph tests
