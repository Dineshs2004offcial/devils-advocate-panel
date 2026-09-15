# LangChain & LangGraph Integration

This document describes how LangChain and LangGraph are used together in the Devil's Advocate Panel system.

- **LangChain** handles LLM-oriented building blocks such as prompt templates, model interaction, structured AI operations, and provider abstractions.
- **LangGraph** manages stateful multi-agent workflow orchestration, branching execution, debate loops, and shared state.

---

## LangChain (LLM Execution & Building Blocks)

LangChain provides the underlying abstractions for agent roles, model interactions, and structured outputs.

```text
Agent Role
   |
   v
Prompt
   |
   v
LLM
   |
   v
Structured Agent Response
```

LangGraph handles workflow orchestration, while LangChain handles LLM-oriented components.

---

## LangGraph (Workflow & State Management)

LangGraph manages the multi-agent debate workflow and shared state across execution steps.

```text
START
  |
  v
Pitch Analysis
  |
  +--> VC Agent
  +--> Financial Agent
  +--> Market Agent
  |
  v
Devil's Advocate
  |
  v
Cross Challenge
  |
  v
Rebuttal
  |
  v
Final Evaluator
  |
  v
END
```

State may contain the pitch, agent analyses, challenges, rebuttals, round information, scores, weaknesses and final verdict.

The exact state fields match `backend/app/graph/state.py`.
