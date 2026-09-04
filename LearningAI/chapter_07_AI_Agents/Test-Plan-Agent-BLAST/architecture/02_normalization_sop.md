# Layer 1: Data Normalization SOP (Standard Operating Procedure)

**Layer:** 1 (Architecture/Technical SOPs)  
**Purpose:** Transform raw Jira data into a consistent internal schema  
**Owner:** normalizer.py (to be built in Phase 3)  
**Status:** Ready for Phase 3 implementation

---

## Objective
Normalize heterogeneous Jira data (markdown, plain text, custom fields) into a standardized JSON schema that can be reliably processed by test generation logic.

## Why Normalization Matters
Jira data is inconsistent:
- Descriptions may be markdown, HTML, or plain text
- Acceptance criteria may be in description, custom fields, or comments
- Labels and components may be empty, single, or multiple
- Dates may be in different formats

**Goal:** Convert ALL variation into one standard format before processing.

## Input (Raw Jira Fetch Output)
```json
{
  "key": "PROJ-123",
  "fields": {
    "summary": "User login validation",
    "description": "As a user, I want to log in with valid credentials...",
    "status": {"name": "In Progress", "id": "3"},
    "priority": {"name": "High", "id": "2"},
    "issuetype": {"name": "Story", "id": "10001"},
    "labels": ["auth", "security"],
    "components": [{"name": "Authentication", "id": "10001"}],
    "assignee": {"displayName": "John Doe", "emailAddress": "john@example.com"},
    "created": "2026-09-01T10:00:00.000-0400",
    "updated": "2026-09-02T15:30:00.000-0400",
    "customfield_10001": "Acceptance Criteria field (if exists)"
  },
  "changelog": {...}
}
```

## Process Flow

### Step 1: Extract Core Fields
Map Jira fields to normalized schema:

```python
normalized = {
    'issueKey': raw['key'],
    'title': raw['fields']['summary'],
    'type': raw['fields']['issuetype']['name'],
    'status': raw['fields']['status']['name'],
    'priority': raw['fields']['priority']['name'],
    'summary': raw['fields']['summary'],
    'description': raw['fields']['description'] or '',
    'assignee': {
        'name': raw['fields']['assignee']['displayName'] if raw['fields']['assignee'] else 'Unassigned',
        'email': raw['fields']['assignee']['emailAddress'] if raw['fields']['assignee'] else None
    },
    'createdAt': normalize_date(raw['fields']['created']),
    'updatedAt': normalize_date(raw['fields']['updated'])
}
```

### Step 2: Normalize Dates to ISO 8601
**Rule:** All dates must be in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

```python
def normalize_date(jira_date_string):
    """Convert Jira date to ISO 8601"""
    # Input: "2026-09-01T10:00:00.000-0400"
    # Output: "2026-09-01T10:00:00Z"
    # Implementation: Use dateutil.parser or datetime
```

### Step 3: Normalize Labels
**Rule:** Labels are always a list of lowercase strings

```python
normalized['labels'] = [
    label.lower().strip()
    for label in (raw['fields'].get('labels', []) or [])
    if label  # Filter empty strings
]
```

### Step 4: Normalize Components
**Rule:** Components are always a list of component names

```python
normalized['components'] = [
    comp['name']
    for comp in (raw['fields'].get('components', []) or [])
]
```

### Step 5: Extract & Normalize Acceptance Criteria
**Priority Order (try in this order):**

1. **Custom Field (customfield_10001)**
   ```python
   criteria = raw['fields'].get('customfield_10001', '')
   ```

2. **Parse from Description (if custom field empty)**
   Apply regex patterns to find:
   - Lines starting with "Given", "When", "Then", "And"
   - Lines starting with "✓", "•", "-"
   - Lines in "Acceptance Criteria:" section
   
3. **Mark as missing if not found**
   ```python
   if not criteria:
       criteria = []
       dataQuality['flags'].append("WARNING: No acceptance criteria found")
   ```

**Acceptance Criteria Normalization:**
```python
def normalize_criteria(criteria_text):
    """Convert criteria text to list of strings"""
    if isinstance(criteria, list):
        return [c.strip() for c in criteria if c.strip()]
    elif isinstance(criteria, str):
        # Split by newlines or special markers
        lines = criteria.split('\n')
        return [line.strip() for line in lines if line.strip()]
    else:
        return []

normalized['acceptanceCriteria'] = normalize_criteria(criteria)
```

### Step 6: Handle Issue Type Special Cases
**Different issue types require different processing:**

| Type | Rule |
|------|------|
| **Story** | Use acceptance criteria, split into test cases |
| **Bug** | Focus on "Steps to Reproduce" and "Expected Result" |
| **Task** | Less structured; use description directly |
| **Epic** | May have multiple linked issues |

### Step 7: Detect Ambiguous or Missing Data
Quality checks to flag potential issues:

```python
dataQuality = {
    'hasMissingAcceptanceCriteria': len(normalized['acceptanceCriteria']) == 0,
    'hasAmbiguousRequirements': detect_ambiguous_language(normalized['description']),
    'missingFields': check_required_fields(normalized),
    'flags': []  # Already populated during extraction
}
```

**Ambiguous Language Detector:**
Look for vague words that indicate unclear requirements:
- "should", "may", "might", "could" (instead of "must", "will")
- "etc.", "and so on"
- "as needed", "if applicable"
- "similar to", "like", "somewhat"

### Step 8: Linked Issues & Subtasks
```python
normalized['linkedIssues'] = [
    link['outwardIssue']['key']
    for link in raw.get('fields', {}).get('issuelinks', [])
    if 'outwardIssue' in link
]

normalized['linkedSubtasks'] = [
    subtask['key']
    for subtask in raw.get('fields', {}).get('subtasks', [])
]
```

## Output (Normalized Schema)
```json
{
  "issueKey": "PROJ-123",
  "title": "User login should validate credentials",
  "type": "Story",
  "status": "In Progress",
  "priority": "High",
  "summary": "User enters invalid credentials and should see an error",
  "description": "The login form validates user input and blocks access when credentials are incorrect.",
  "acceptanceCriteria": [
    "Invalid email format is rejected",
    "Incorrect password shows error message",
    "No session is created"
  ],
  "labels": ["auth", "login"],
  "components": ["Authentication"],
  "assignee": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "createdAt": "2026-09-01T10:00:00Z",
  "updatedAt": "2026-09-02T15:30:00Z",
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

## Determinism & Consistency
- **Rule 1:** Same input always produces identical output
- **Rule 2:** All transformations are reversible (can verify against original)
- **Rule 3:** No probabilistic or NLP processing here
- **Rule 4:** All flags are logged for audit trail

## Edge Cases & Handling

| Scenario | Handling |
|----------|----------|
| Description is None/null | Replace with empty string "" |
| Labels is None/null | Replace with empty list [] |
| No custom field for criteria | Extract from description or flag |
| Issue type not recognized | Log warning, proceed with "Unknown" type |
| Assignee is None | Set to "Unassigned" |
| Date parsing fails | Log error, use current timestamp |
| Circular linked issues | Detect and avoid infinite loops |

## Implementation Notes
- Use Python's `json` module for JSON generation
- Use `datetime.fromisoformat()` for date parsing
- Use regex for pattern matching in descriptions
- Validate output against schema
- Log all transformations for debugging

## Testing Checklist (Phase 3)
- [ ] Normalize issue with all fields present
- [ ] Normalize issue with missing acceptance criteria
- [ ] Normalize issue with None/null values
- [ ] Normalize issue with markdown description
- [ ] Normalize issue with special characters
- [ ] Detect ambiguous language correctly
- [ ] Handle different issue types (Story, Bug, Task)
- [ ] Verify date format conversion
- [ ] Verify linked issues extraction
- [ ] Verify output matches schema

---

**SOP Status:** Ready for Phase 3 Implementation  
**Tool:** tools/normalizer.py (new)  
**Next SOP:** Test Case Generation SOP
