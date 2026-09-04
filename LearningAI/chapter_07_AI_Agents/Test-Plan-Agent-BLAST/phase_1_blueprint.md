# 🏗️ Phase 1: Blueprint (Vision & Logic) - COMPLETED

**Status:** ✅ APPROVED by user discovery (2026-09-02)

---

## Discovery Questions - ANSWERS CONFIRMED

### 1. North Star (Singular Desired Outcome)
**Question:** What is the singular desired outcome?

**Answer:**
> "Generate a high-quality test plan from a single Jira issue ID. The Jira issue contains requirement details, and the system will fetch and transform that data into structured test cases."

**Interpretation:**
- Input: One Jira issue ID (e.g., PROJ-123)
- Processing: Fetch issue data, extract requirements, analyze acceptance criteria
- Output: Structured, professional test plan with clear test cases
- Outcome: QA team can execute test plan directly from generated output

---

### 2. Integrations (External Services & Credentials)
**Question:** Which external services do we need? Are keys ready?

**Answer:**
```
JIRA_URL=https://sharbaniai2026.atlassian.net/
JIRA_EMAIL=<your-jira-email>
JIRA_API_TOKEN=<your-jira-api-token>
LLM_PROVIDER=groq
GROQ_API_KEY=<your-groq-api-key>
OLLAMA_URL=http://localhost:11434 (optional fallback)
PYTHON_VERSION=3.10+
```

**Interpretation:**
- **Jira**: Ready - API token authentication confirmed
- **LLM**: Groq (primary), Ollama optional fallback
- **Environment**: Locally hosted
- **Credentials**: Stored in `.env` file (not in code)

---

### 3. Source of Truth
**Question:** Where does the primary data live?

**Answer:**
> "Linked child issues/subtasks"

**Interpretation:**
- **Primary**: Jira issue (summary, description, acceptance criteria)
- **Secondary**: Linked child issues and subtasks (additional context)
- **No other sources**: Avoid external wikis, Confluence, or assumptions
- **Authority**: If it's not in Jira, it doesn't exist in the test plan

---

### 4. Delivery Payload (Output Format & Location)
**Question:** How and where should the final result be delivered?

**Answer:**
> "We would want to host the Test Plan generator agent locally so plan the output accordingly."

**Interpretation:**
- **Deployment**: Web interface (not CLI, not API-only)
- **Hosting**: Local machine (not cloud)
- **Output Formats**:
  - JSON (for programmatic consumption)
  - Markdown (for human reading)
  - HTML (rendered in web UI)
- **Storage**: `.tmp/` directory for intermediate files, persistent storage for approved plans

---

### 5. Behavioral Rules (How the System Should Act)
**Question:** How should the system "act"? (Tone, logic constraints, "Do Not" rules)

**Answer:**
> "If acceptance criteria are missing, should we flag. No security or performance testing details required. Test case description tone - formal. Keep it simple for the Do Not rules like do not add or assume requirements."

**Interpretation:**
1. **Tone & Style**: Formal, professional, precise language
2. **Missing Data Handling**:
   - ❌ DO NOT: Generate dummy test cases
   - ✅ DO: Flag gaps with clear warnings
3. **Scope Constraints**:
   - ❌ DO NOT: Include security testing (unless in Jira)
   - ❌ DO NOT: Include performance testing (unless in Jira)
   - ✅ DO: Include only what's in Jira
4. **Requirement Handling**:
   - ❌ DO NOT: Assume hidden requirements
   - ❌ DO NOT: Invent new features
   - ✅ DO: Reference Jira as proof
5. **Simplicity**: Keep test cases simple, clear, actionable

---

## Test Case Categories (Confirmed - ALL INCLUDED)

The system will generate test cases in **4 categories**:

### 1. Happy Path (Positive Scenarios)
- Requirement works as specified
- Expected outcomes are achieved
- All acceptance criteria pass
- **Example**: Valid credentials grant access

### 2. Negative Scenarios (Error Handling)
- Invalid inputs are rejected
- Error messages are shown
- System fails gracefully
- **Example**: Wrong password shows error message

### 3. Edge Cases (Boundary Conditions)
- Empty fields, special characters
- Maximum/minimum values
- Boundary limits
- **Example**: Empty email field shows validation error

### 4. Regression Cases (Existing Functionality)
- Core features still work
- UI elements render correctly
- No breakage from changes
- **Example**: Login page loads without errors

---

## Technology Stack (Confirmed)

| Component | Choice |
|-----------|--------|
| Language | Python 3.10+ |
| Web Framework | Flask or FastAPI |
| Frontend | HTML/CSS/JavaScript |
| LLM Engine | Groq API (primary) |
| Fallback LLM | Ollama (http://localhost:11434) |
| Jira Integration | REST API + API Token |
| Data Format | JSON + Markdown |
| Storage | File-based (.tmp/, .env) |
| Deployment | Local web server |

---

## Data Schema - CONFIRMED

### Input Payload
```json
{
  "jiraIssueId": "PROJ-123",
  "jiraDomain": "https://sharbaniai2026.atlassian.net",
  "authMethod": "api_token",
  "includeLinkedIssues": true,
  "includeSubtasks": true,
  "outputFormat": "json_and_markdown",
  "testCaseCategories": ["happy_path", "negative", "edge_cases", "regression"]
}
```

### Normalized Internal Schema (After Jira Fetch)
```json
{
  "issueKey": "PROJ-123",
  "title": "Login should reject invalid credentials",
  "type": "Story",
  "status": "In Progress",
  "priority": "High",
  "summary": "User enters invalid credentials and should see an error",
  "description": "...",
  "acceptanceCriteria": [
    "Invalid email format is rejected",
    "Incorrect password shows an error message",
    "No session is created"
  ],
  "labels": ["auth"],
  "components": ["Authentication"],
  "linkedIssues": ["PROJ-124"],
  "linkedSubtasks": [],
  "dataQuality": {
    "hasMissingAcceptanceCriteria": false,
    "hasAmbiguousRequirements": false,
    "flags": []
  }
}
```

### Output Schema (Test Plan JSON)
```json
{
  "metadata": {
    "project": "PROJ",
    "issueKey": "PROJ-123",
    "generatedAt": "2026-09-02T10:00:00Z",
    "llmProvider": "groq",
    "dataQualityFlags": []
  },
  "testPlan": {
    "objective": "Verify invalid credentials are rejected and user feedback is shown",
    "scope": ["Login form validation", "Error messaging", "Access restriction"],
    "environment": "QA/Staging",
    "preconditions": ["User account exists"],
    "testCases": [
      {
        "id": "TC-001-HAPPY",
        "category": "happy_path",
        "title": "Valid credentials should grant access",
        "steps": ["Open login page", "Enter valid email", "Enter correct password", "Click login"],
        "expectedResult": "User is logged in and directed to dashboard",
        "priority": "High"
      }
    ]
  }
}
```

---

## Architecture Overview (3-Layer Model)

### Layer 1: Architecture (SOPs in Markdown)
- `architecture/jira_fetch_sop.md` - Jira API interaction
- `architecture/data_normalization_sop.md` - Parse and normalize
- `architecture/test_generation_sop.md` - Create test cases
- `architecture/validation_sop.md` - Quality checks

### Layer 2: Navigation (Decision Making)
- Orchestrate layer 1 and layer 3 operations
- Route data between fetchers, transformers, and generators
- Decide when to request clarification vs. flag gaps

### Layer 3: Tools (Deterministic Python Scripts)
- `tools/jira_client.py` - Fetch from Jira API
- `tools/data_normalizer.py` - Transform to internal schema
- `tools/test_case_generator.py` - Use LLM to generate test cases
- `tools/validator.py` - Quality checks and gap detection

### Layer 4: Web UI (New)
- `app.py` - Flask/FastAPI server
- `templates/` - HTML forms and results display
- `static/` - CSS and JavaScript

---

## Execution Flow (Confirmed)

```
User Input (Jira Issue ID)
    ↓
[Layer 1: Jira Fetch] → Get issue data
    ↓
[Layer 1: Normalize] → Map to internal schema, flag gaps
    ↓
[Layer 2: Decision] → Check data quality, decide if ready
    ↓
[Layer 1: Generation] → Use Groq to create test cases
    ↓
[Layer 1: Validation] → Verify against source, format output
    ↓
[Layer 4: Web UI] → Display JSON + Markdown to user
    ↓
User Output (Test Plan)
```

---

## Next Steps (Phases 2-4)

### Phase 2: L - Link (Connectivity)
- [ ] Test Jira API connection with provided credentials
- [ ] Verify Groq API key works
- [ ] Create minimal Jira fetch tool
- [ ] Test fetch with real issue

### Phase 3: A - Architect (3-Layer Build)
- [ ] Write Layer 1 SOPs for each operation
- [ ] Build Layer 2 navigation/orchestration
- [ ] Build Layer 3 tools (jira_client, normalizer, generator, validator)
- [ ] Integrate all layers

### Phase 4: S - Stylize (UI & Refinement)
- [ ] Create web UI (Flask/FastAPI app)
- [ ] Format Markdown output nicely
- [ ] Format JSON output with proper schema
- [ ] Test end-to-end with real Jira issue
- [ ] User acceptance testing

---

## Success Criteria for Phase 1: BLUEPRINT ✅

- [x] Confirmed singular desired outcome (North Star)
- [x] Identified all integrations and confirmed credentials ready
- [x] Defined source of truth (Jira + linked issues)
- [x] Specified delivery format and hosting (Web UI, local)
- [x] Documented all behavioral rules and constraints
- [x] Defined test case categories (all 4 types)
- [x] Confirmed technology stack
- [x] Created normalized data schema (input → internal → output)
- [x] Described 3-layer architecture
- [x] Outlined execution flow

**Phase 1 Status:** ✅ COMPLETE - Ready to move to Phase 2: Link

---

**Document Created:** 2026-09-02
**Last Updated:** 2026-09-02
**Next Phase:** Phase 2 - Connectivity & Link Verification
