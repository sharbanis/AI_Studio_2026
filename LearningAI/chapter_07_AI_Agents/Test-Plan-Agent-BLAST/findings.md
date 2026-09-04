# Findings: Jira-Based Test Plan Creator

## Summary of Findings
The core process is feasible and grounded in a clear source-of-truth pattern:

- Jira is the primary source of requirement context.
- The issue key, summary, description, acceptance criteria, labels, priority, and custom fields are the main inputs for building the test plan.
- The main challenge is not the API call itself, but transforming unstructured Jira content into a structured, testable QA artifact.
- A reliable system must behave conservatively: when requirements are unclear, highlight the gap instead of assuming hidden business logic.

## What We Can Retrieve from Jira
A Jira issue typically contains the following useful information:

- issue key, such as PROJ-123
- summary/title
- description
- issue type
- status
- priority
- labels
- components
- assignee
- reporter
- custom fields
- acceptance criteria (if stored in description or custom field)
- linked issues, subtasks, and dependencies

This is enough to build an initial test plan for many Agile teams. For stronger output quality, it is useful to query related issue metadata as well.

## Recommended Jira Request Pattern
Use the Jira REST API with basic auth or API token authentication.

### Example 1: Fetch a specific issue by key
```bash
curl -u "your-email@example.com:your-api-token" \
  -H "Accept: application/json" \
  "https://your-company.atlassian.net/rest/api/3/issue/PROJ-123?expand=renderedFields,transitions,operations,editmeta,changelog"
```

### Example 2: Search for issues and related metadata
```bash
curl -u "your-email@example.com:your-api-token" \
  -H "Accept: application/json" \
  "https://your-company.atlassian.net/rest/api/3/search?jql=project=PROJ AND issuekey='PROJ-123'&fields=summary,description,status,priority,labels,components,customfield_10001,assignee"
```

### Example 3: Use a project-level query to collect multiple tickets
```bash
curl -u "your-email@example.com:your-api-token" \
  -H "Accept: application/json" \
  "https://your-company.atlassian.net/rest/api/3/search?jql=project=PROJ ORDER BY created DESC&maxResults=50&fields=key,summary,status,priority,labels"
```

## Key Findings

### 1. Requirement data is usually in the issue body
Most Jira stories contain requirement logic in the description or in custom acceptance-criteria fields. The test plan builder should parse the issue body, not just the title.

### 2. The plan should be evidence-based
The system should only generate test cases for behavior that is visible in the Jira issue. This avoids hallucinated requirements.

### 3. We need a normalization layer
Jira data is heterogeneous: some fields are plain text, some are markdown, some are custom objects. We should normalize these into a standard internal JSON model before generating the final plan.

### 4. Acceptance criteria should drive the test matrix
The best test plans come from acceptance criteria, happy paths, edge cases, negative scenarios, and regression areas.

### 5. Not all Jira issues are equally useful
Some tickets are bug reports, some are feature requests, and some are epics. The system should detect issue type and format the test plan accordingly.

## Recommended Internal Data Model
```json
{
  "issueKey": "PROJ-123",
  "summary": "Login page should reject invalid credentials",
  "description": "User enters invalid email and password. System should show validation message.",
  "issueType": "Story",
  "status": "In Progress",
  "priority": "High",
  "labels": ["login", "security"],
  "acceptanceCriteria": [
    "User enters invalid email and password",
    "The system displays an error message",
    "No access is granted"
  ],
  "components": ["Authentication"],
  "linkedIssues": ["PROJ-124"]
}
```

## Implementation Interpretation
The system should take the following workflow:
1. Receive Jira issue key from the user.
2. Call Jira API with authentication.
3. Fetch issue details and fields relevant to test creation.
4. Transform raw Jira content into a normalized requirement model.
5. Use the model to generate a test plan by prompt or deterministic rule engine.
6. Validate the plan against the original issue text before final delivery.

## Risks to Watch
- The issue description may use markdown tables or plain text with inconsistent formatting.
- Custom fields may need project-specific logic.
- Some acceptance criteria may be missing or stored in a different field than expected.
- Permissions may restrict access to certain issues or fields.

## Final Finding
The project is a good fit for a two-step architecture: fetch and normalize Jira data first, then generate QA-ready test plans from normalized requirements. This keeps the workflow deterministic and resilient.
