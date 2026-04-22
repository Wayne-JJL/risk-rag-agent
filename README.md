# Risk RAG Agent

A minimal business-oriented RAG agent for metric explanation, troubleshooting, action-first answers, and source-grounded responses.

## Overview

Risk RAG Agent is a small but complete RAG + Agent demo designed for business-facing AI application scenarios.

Instead of building a generic chatbot, this project focuses on two more practical capabilities:

- **Metric explanation**, such as AUC, PSI, KS, and overdue rate
- **Troubleshooting and rule-based Q&A**, such as missing rate anomalies, distribution drift, ETL issues, and dashboard refresh failures

The project demonstrates a full workflow from routing to retrieval to answer generation:

- query routing
- tool selection
- local knowledge loading
- text chunking
- embedding-based retrieval
- top-k recall
- grounded answer generation
- action-first response style
- source citation

## What this project can do

### 1. Metric explanation
Examples:
- What is AUC?
- How is overdue rate calculated?
- What should I check first if AUC drops while PSI rises?

### 2. Troubleshooting and knowledge Q&A
Examples:
- What should I check first if a dashboard is not updated?
- How do I troubleshoot distribution drift?
- How do I locate a consistency issue?
- What should I do if a field missing rate suddenly increases?

### 3. Action-first answers
For questions like:
- “what should I do”
- “how to troubleshoot”
- “how to locate”
- “what should I check first”

the agent prioritizes **actionable steps** instead of only giving conceptual explanations.

### 4. Source-grounded responses
For retrieval-based answers, the system returns answers grounded in local knowledge documents and includes source references.

### 5. Boundary control
The agent explicitly handles unsupported requests such as real-time weather, news, prices, and other external live information.

---

## Architecture

```text
User Query
  ↓
Router
  ├── metric       → metric tool
  ├── rule         → RAG retrieval
  ├── identity     → fixed response
  ├── unsupported  → fixed response
  └── chat         → normal chat
  ↓
Tool / Retrieval Layer
  ├── metrics.json
  └── local knowledge txt files
       ↓
       chunking
       ↓
       embedding
       ↓
       top-k retrieval
  ↓
LLM Answer Generation
  ↓
Final Answer
  ├── conclusion
  ├── evidence
  ├── suggestions / actions
  └── citations