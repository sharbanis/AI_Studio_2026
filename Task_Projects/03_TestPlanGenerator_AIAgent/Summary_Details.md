# Test Plan AI Agent — Summary & Architecture

## What It Does

A locally hosted web app that turns a Jira issue into a complete QA test plan. You give it a Jira issue ID (like `KAN-2`), and it fetches the issue, understands the requirement, and generates test cases across four categories using an LLM.

## High-Level Flow

1. **Input** — User enters a Jira issue key in the web page.
2. **Fetch** — Reads the issue from Jira (title, description, acceptance criteria).
3. **Normalize** — Converts messy Jira data into a clean, consistent format.
4. **Generate** — An LLM (Groq) writes test cases for each category.
5. **Validate** — Checks quality, coverage, and removes duplicates.
6. **Output** — Returns a test plan as JSON + Markdown, downloadable from the page.

## Architecture (Layered)

The system is built in four layers so each job is separate and easy to reason about.

| Layer | Component | Responsibility |
|-------|-----------|----------------|
| 1 — UI | `app.py`, `templates/`, `static/` | Flask web interface, buttons, downloads |
| 2 — Orchestration | `navigation.py` | Runs the pipeline in the right order |
| 3 — Tools | `tools/` | The actual work: fetch, normalize, generate, validate |
| 4 — Rules | `architecture/` SOPs | Documented procedures and error handling |

### Layer 3 Tools (the core)

- `jira_client.py` — Talks to the Jira REST API, fetches issues.
- `normalizer.py` — Converts raw Jira data into a standard internal schema.
- `groq_client.py` — Connects to the Groq LLM API.
- `test_generator.py` — Builds prompts and parses LLM responses into test cases.
- `validator.py` — Checks coverage, priorities, duplicates; formats output.

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        USER (Browser)                       │
│          Enters issue key  →  e.g. "PROJ-123"              │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP POST /api/generate
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Layer 1: Flask Web App (app.py)             │
│          Receives request, returns JSON + downloads         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│        Layer 2: Orchestrator (navigation.py)                │
│   Coordinates: Fetch → Normalize → Generate → Validate      │
└───────┬───────────────┬───────────────┬──────────────┬──────┘
        │               │               │              │
        ▼               ▼               ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Jira Client │ │  Normalizer  │ │ Groq Client  │ │  Validator   │
│ (fetch issue)│ │ (clean data) │ │ (LLM calls)  │ │(check quality)│
└──────┬───────┘ └──────────────┘ └──────┬───────┘ └──────┬───────┘
       │                                 │               │
       ▼                                 ▼               │
┌──────────────┐                ┌──────────────────┐     │
│  Jira API    │                │    Groq LLM API  │     │
│ (source of   │                │  (test case gen) │     │
│   truth)     │                └──────────────────┘     │
└──────────────┘                                        │
                                                        ▼
                                    ┌──────────────────────────────┐
                                    │  OUTPUT: Test Plan (JSON+MD) │
                                    │  - 4 test case categories    │
                                    │  - coverage & priorities     │
                                    └──────────────────────────────┘
```

## Test Case Categories

The agent generates four types of test cases for every issue:

- **Happy Path** — Valid inputs work correctly.
- **Negative** — Invalid inputs are handled gracefully.
- **Edge Cases** — Boundary conditions and extreme values.
- **Regression** — Existing functionality still works.

## Key Design Principles

- **Jira is the source of truth** — no invented requirements.
- **Deterministic pipeline** — the LLM is only one step, wrapped by validation.
- **Conservative by default** — missing data is flagged, not guessed.
- **Two outputs** — human-readable Markdown and machine-readable JSON.

## How to Run

```powershell
cd LearningAI\chapter_07_AI_Agents\Test-Plan-Agent-BLAST
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in the browser.
