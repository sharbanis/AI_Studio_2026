# Layer 1: Jira Fetch SOP (Standard Operating Procedure)

**Layer:** 1 (Architecture/Technical SOPs)  
**Purpose:** Define how to reliably fetch Jira issue data  
**Owner:** jira_client.py  
**Status:** Ready for Phase 3 implementation

---

## Objective
Fetch a Jira issue by ID and extract all relevant requirement data for test plan generation.

## Inputs
```json
{
  "issueKey": "PROJ-123",
  "jiraDomain": "https://sharbaniai2026.atlassian.net",
  "jiraEmail": "sharbanicap@gmail.com",
  "jiraToken": "<your-jira-api-token>",
  "includeLinkedIssues": true,
  "includeSubtasks": true
}
```

## Process Flow

### Step 1: Authenticate & Connect
1. Load credentials from `.env` file
2. Create session with Jira REST API (v3)
3. Set auth headers: Basic Auth (email:token)
4. Set content-type: application/json
5. **Decision:** If auth fails → Flag error, halt process

### Step 2: Fetch Issue Metadata
1. Call: `GET /rest/api/3/issue/{issueKey}`
2. Parameters:
   - `expand`: renderedFields, changelog
   - `fields`: summary, description, status, priority, labels, components, assignee, created, updated
3. **Decision:** If issue not found → Flag error, return None
4. **Decision:** If API rate limit hit → Implement exponential backoff

### Step 3: Extract Core Fields
Required fields to extract:
```
✓ issueKey (e.g., "PROJ-123")
✓ summary (short title)
✓ description (full requirement text)
✓ status (e.g., "In Progress")
✓ priority (e.g., "High")
✓ issueType (e.g., "Story", "Bug", "Task")
✓ labels (e.g., ["auth", "login"])
✓ components (e.g., ["Authentication"])
✓ assignee (owner info)
```

### Step 4: Parse Acceptance Criteria
**Rule 1:** Look for acceptance criteria in these locations:
1. Custom field `customfield_10001` (if configured in Jira)
2. Within description text (pattern: "As a...", "Given...", "When...", "Then...")
3. Bullet points in description starting with "✓" or "•"

**Rule 2:** If acceptance criteria missing:
- Flag as "WARNING: No acceptance criteria found"
- Do NOT generate placeholder criteria
- Mark in dataQuality.flags

### Step 5: Handle Linked Issues & Subtasks
1. **If includeLinkedIssues = true:**
   - Extract issuelinks array
   - Get linked issues (but don't fetch full data)
   - Store as issue IDs only (e.g., ["PROJ-124"])

2. **If includeSubtasks = true:**
   - Extract subtasks array from response
   - Get subtask keys (e.g., ["PROJ-123-1", "PROJ-123-2"])
   - Store for reference (optional: fetch and merge criteria)

### Step 6: Data Quality Assessment
Evaluate the issue for completeness:
```json
{
  "hasMissingAcceptanceCriteria": boolean,
  "hasAmbiguousRequirements": boolean,
  "missingFields": [array of field names],
  "flags": [array of warning strings]
}
```

**Quality Checks:**
- [ ] Description is not empty
- [ ] Acceptance criteria exist (either in custom field or inferred from description)
- [ ] Status is set
- [ ] Priority is set
- [ ] Issue type is recognized (Story/Bug/Task/Epic)

### Step 7: Output & Store
1. Return normalized issue JSON to Layer 2
2. Store raw response in `.tmp/{issueKey}_raw.json` for audit
3. Store normalized in `.tmp/{issueKey}_normalized.json`
4. Log success/warning messages

## Outputs
```json
{
  "issueKey": "PROJ-123",
  "title": "Login should reject invalid credentials",
  "type": "Story",
  "status": "In Progress",
  "priority": "High",
  "summary": "User enters invalid credentials and should see an error",
  "description": "The login form validates user input and blocks access when credentials are incorrect.",
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
    "missingFields": [],
    "flags": []
  }
}
```

## Error Handling

| Error | Action | Result |
|-------|--------|--------|
| Authentication fails | Raise ValueError with clear message | Process halts |
| Issue not found (404) | Log and return None | Proceed with error flag |
| Rate limit (429) | Exponential backoff (1s, 2s, 4s) | Retry up to 3 times |
| Network timeout | Retry once, then fail gracefully | Flag network error |
| Missing required field | Note in dataQuality.flags | Continue processing |

## Determinism & Reproducibility
- **Rule 1:** All extraction is deterministic - same input always produces same output
- **Rule 2:** No LLM guessing in this layer - only data extraction
- **Rule 3:** All assumptions are documented in dataQuality.flags
- **Rule 4:** Dates are stored in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

## Implementation Notes
- Use `requests` library for HTTP calls
- Cache credentials in environment variables (.env)
- Implement retry logic with exponential backoff
- Log all API calls (input/output) for debugging
- Store intermediate files in `.tmp/` for audit trail

## Testing Checklist (Phase 3)
- [ ] Fetch issue with complete data (all fields present)
- [ ] Fetch issue with missing acceptance criteria
- [ ] Fetch issue with special characters in description
- [ ] Handle issue not found (404)
- [ ] Handle rate limiting (429)
- [ ] Verify data normalization correctness
- [ ] Verify linked issues extraction
- [ ] Verify subtasks extraction

---

**SOP Status:** Ready for Phase 3 Implementation  
**Tool:** tools/jira_client.py  
**Next SOP:** Data Normalization SOP
