# LLM Project Constitution

## Purpose
This file defines the schema, behavioral rules, and architectural boundaries for the Jira-driven test plan creator.

## 1. Project Objective
Given a Jira issue ID, the system must:
- fetch the issue data from Jira,
- interpret the requirement and acceptance criteria,
- create a structured test plan,
- return an output that is traceable to the source requirement.

## 2. Core Rules
1. Use Jira as the source of truth.
2. Never invent requirements that are not present in the issue.
3. Distinguish between evidence, assumptions, and missing data.
4. If the requirement is ambiguous, flag the ambiguity instead of guessing.
5. Prefer deterministic extraction and structured output over free-form hallucination.
6. Keep output reviewable for QA and engineering teams.

## 3. Recommended Input Schema
```json
{
  "jiraIssueId": "PROJ-123",
  "jiraDomain": "https://your-company.atlassian.net",
  "authMethod": "api_token",
  "fields": [
    "summary",
    "description",
    "status",
    "priority",
    "labels",
    "components",
    "customfield_10001",
    "assignee"
  ],
  "includeLinkedIssues": true,
  "outputFormat": "markdown"
}
```

## 4. Recommended Normalized Schema
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
  "labels": ["auth", "security"],
  "components": ["Authentication"],
  "risks": ["Brute-force attempts", "UX ambiguity"],
  "linkedIssues": ["PROJ-124"]
}
```

## 5. Recommended Output Schema for Test Plan
```json
{
  "project": "PROJ",
  "issueKey": "PROJ-123",
  "objective": "Verify invalid credentials are rejected and user feedback is shown",
  "scope": [
    "Login form validation",
    "Error messaging",
    "Access restriction"
  ],
  "environment": "QA/Staging",
  "preconditions": [
    "User account exists",
    "Browser is available"
  ],
  "testCases": [
    {
      "id": "TC-01",
      "title": "Invalid password should display error",
      "steps": [
        "Open login page",
        "Enter valid email",
        "Enter wrong password",
        "Click login"
      ],
      "expectedResult": "Error is displayed and no access is granted",
      "priority": "High"
    }
  ],
  "risks": [
    "Missing validation copy",
    "Incorrect error handling"
  ]
}
```

## 6. Decision Rules for Test Generation
- Generate happy-path, negative-path, edge-case, and regression scenarios.
- Use acceptance criteria as the source for expected results.
- If a field is missing, generate a gap note rather than a fabricated result.
- Separate functional coverage from non-functional checks such as security, performance, and resilience.
- Prioritize the highest-risk scenarios first.

## 7. Architecture
This project should follow the B.L.A.S.T. structure with a simple deterministic flow:

### Layer 1: Architecture
- Define the data contracts in markdown and JSON.
- Document assumptions and handling of edge cases.
- Keep transformation logic well-structured and reviewable.

### Layer 2: Navigation / Decision Layer
- Orchestrate retrieval, normalization, and generation steps.
- Decide whether the system should request clarification when evidence is missing.

### Layer 3: Tools
- Use deterministic scripts to call the Jira API.
- Parse response payloads into a normalized schema.
- Generate Markdown or JSON output from that normalized model.

## 8. Behavioral Guardrails
- Never claim a test is valid without mapping it to an observable requirement.
- Do not invent user flows outside the Jira description unless explicitly marked as assumptions.
- Keep output concise and professional.
- Present missing data as a clear gap or risk note.
- Favor structure, traceability, and reproducibility over stylistic creativity.

## 9. Example Execution Flow
1. User provides issue key such as PROJ-123.
2. System calls Jira issue endpoint.
3. System extracts title, description, status, priority, labels, and custom fields.
4. System maps raw data into normalized schema.
5. System generates test cases from acceptance criteria and use cases.
6. System validates the generated output against the source issue.
7. System returns a final test plan with risk notes and gaps.

## 10. Final Principle
The system should behave like a careful QA analyst: evidence-driven, requirement-aware, and perfectly transparent about missing information.
