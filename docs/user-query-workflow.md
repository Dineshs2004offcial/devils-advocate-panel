# User Query Workflow

This describes the flow after a user submits a startup pitch.

```text
User enters pitch
       |
       v
React Frontend
       |
       | HTTP request
       v
FastAPI Route
       |
       v
Evaluation Service / Graph
       |
       v
LangGraph State
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
Structured Result
       |
       v
React Dashboard
```

## Frontend Result

The UI can display agent analyses, debate rounds, challenges, rebuttals, overall score, weaknesses, improvement suggestions and final verdict.
