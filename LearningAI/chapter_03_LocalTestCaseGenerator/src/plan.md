## Plan: Jira Test Case Generator — Streamlit App

**TL;DR**: Two-screen Streamlit app. Chat screen takes "create test cases for JIRA-102", fetches the ticket from Jira REST API, merges details into the existing `templates/testcase_creator.md` template, generates test cases via the user-selected LLM provider (Ollama `gemma3:1b` or Groq) with **bidirectional automatic fallback**, and renders the output in chat. The app works as long as **at least one provider is available**. Credentials flow: `.env` → `config.json` (runtime persistence).

### Architecture

```
User: "create test cases for JIRA-102"
  → app.py parses JIRA-102 via regex
  → jira_client.py ──GET /rest/api/2/issue/JIRA-102──▶ Jira
  → templates/testcase_creator.md loaded
  → llm_client.py ──try selected provider (ollama/groq)──▶ Local / Cloud
                   ──fallback to other provider──────────▶ Cloud / Local
  → Test cases rendered in chat
```

### Phases

| Phase | Steps | Dependency |
|-------|-------|------------|
| **1. Foundation** | Create `.env`, update .gitignore, create `requirements.txt` | None — all parallel |
| **2. Core Modules** | `config_store.py` → `jira_client.py` → `llm_client.py` | Sequential (each builds on prior) |
| **3. Screens** | `app.py` (Chat), `pages/settings.py` (Settings) | Depends on Phase 2 |
| **4. Polish** | Prompt refinement, startup validation | Depends on Phase 3 |

### Files to Create/Modify

| File | What |
|------|------|
| `chapter_03_Local_TC_Generator/.env` | **Create** — user's Jira/Groq credentials |
| `chapter_03_Local_TC_Generator/app.py` | **Create** — Chat screen: parse Jira key, orchestrate fetch→template→LLM→render |
| `chapter_03_Local_TC_Generator/pages/settings.py` | **Create** — Settings form + Test Connection buttons |
| `chapter_03_Local_TC_Generator/config_store.py` | **Create** — `.env` loader + `config.json` read/write |
| `chapter_03_Local_TC_Generator/jira_client.py` | **Create** — `fetch_ticket(key)` → `{summary, description, acceptance_criteria}` |
| `chapter_03_Local_TC_Generator/llm_client.py` | **Create** — `generate(prompt)` with bidirectional fallback (selected provider first, then the other), plus `get_available_provider()` |
| `chapter_03_Local_TC_Generator/requirements.txt` | **Create** — `streamlit`, `requests`, `python-dotenv` |
| `templates/testcase_creator.md` | **Reuse** — already exists |
| .gitignore (root) | **Update** — add `.env`, `config.json` |

### Key Design Decisions

- **Persistence**: `.env` seeds initial values, `config.json` is the runtime store updated by Settings UI (both git-ignored)
- **Provider selection**: Settings radio lets the user pick their preferred provider (Ollama or Groq)
- **Bidirectional fallback**: `generate()` tries the selected provider first, then automatically falls back to the other — so the app works with at least one reachable provider
- **Groq model**: `llama-3.1-8b-instant` (fast, cheap, good structured output)
- **Ticket key regex**: `\b[A-Z]+-\d+\b` matches standard Jira keys
- **No database**: JSON file is sufficient per the prompt's "no unnecessary abstraction" rule
- **Template path**: Read relative to `app.py`'s directory (`templates/testcase_creator.md`)

### Verification

1. **Per-module**: Test `config_store` reads `.env`, `jira_client` fetches a real ticket, `llm_client` responds via the selected provider and falls back to the other when the selected one is unavailable
2. **Full flow**: `streamlit run app.py` → Settings → pick provider + save credentials → Chat → "create test cases for VALID-KEY" → verify complete output
3. **Edge cases**: No Jira key in message, invalid key (404), both providers down, only one provider available (Ollama or Groq), empty settings on startup

### Excluded

No multi-user auth, no deployment, no streaming, no batch processing, no CSV/PDF export — single-user internal tool only.

---