# Task Plan: Jira-to-Test-Plan Creator

## Objective
Create a deterministic project that accepts a Jira issue ID and produces a structured test plan for QA and validation.

## Protocol Used
B.L.A.S.T. Protocol 0: Initialization

## Primary Goal
Build a system that can:
- read a Jira issue ID,
- fetch the correct issue details and related metadata from Jira,
- interpret requirement context, acceptance criteria, and technical constraints,
- generate a clear, actionable test plan,
- deliver the result in a high-quality Markdown or JSON structure suitable for QA execution.

## Scope
This phase is focused on discovery, schema definition, and implementation planning. No full coding work is started until the input/output contract and rules are agreed.

## Checklist

### Phase 0: Discovery and Setup
- [x] Confirm project objective: create a test plan creator from Jira ID
- [x] Use the B.L.A.S.T. initialization framework
- [x] Set up required memory documents in the project folder
- [ ] Validate the exact Jira data fields required for a useful plan
- [ ] Define JSON schema for the input payload and test plan output

### Phase 1: Jira Integration
- [ ] Confirm Jira authentication method (API token or OAuth)
- [ ] Verify API endpoint and project domain
- [ ] Fetch issue details by issue key
- [ ] Extract summary, description, acceptance criteria, labels, components, priority, status, and linked issues
- [ ] Handle missing or partial fields safely

### Phase 2: Requirement Analysis
- [ ] Parse Jira description into functional and non-functional requirements
- [ ] Separate explicit requirements from implicit assumptions
- [ ] Identify test scenarios: positive, negative, edge, regression, security, performance
- [ ] Turn acceptance criteria into measurable test assertions

### Phase 3: Test Plan Generation
- [ ] Define test plan structure (objective, scope, assumptions, environment, test cases)
- [ ] Generate test cases with ID, steps, expected result, and priority
- [ ] Add risk-based prioritization and regression coverage
- [ ] Ensure output is readable for QA and engineering teams

### Phase 4: Validation and Hardening
- [ ] Validate generated plan against the source Jira issue
- [ ] Check for missing information and ask for clarification if required
- [ ] Add deterministic fallback rules for incomplete Jira data
- [ ] Save and version the output in a clean format

## Success Criteria
The project is considered successful when:
1. A user can pass a Jira issue key such as PROJ-123.
2. The system fetches the matching Jira issue payload.
3. The system extracts business rules, acceptance criteria, and testable requirements.
4. The system generates a useful test plan with clear test cases and expected outcomes.
5. The output remains deterministic and does not fabricate unverified requirements.

## Key Decisions
- Source of truth: Jira issue and ticket metadata.
- Delivery format: Markdown and/or structured JSON.
- Core rule: never invent requirements; only convert evidence from Jira into a test plan.
- Quality rule: if data is missing, the system should flag the gap instead of guessing.

## Proposed Implementation Path
1. Define Jira API contract.
2. Build connector to fetch issue payload.
3. Design extraction logic for requirements and acceptance criteria.
4. Build LLM prompt schema for converting issue data into a QA test plan.
5. Generate output in Markdown and JSON.
6. Validate against real issue examples.

## Risks and Constraints
- Jira fields may vary by project configuration.
- Custom fields may not be available in the default issue schema.
- User stories may contain ambiguous wording and incomplete acceptance criteria.
- API rate limits or permissions may block full data retrieval.

## Open Questions
- Which Jira instance or domain is being used?
- Which fields are mandatory for the generated plan?
- Do we include only issue-level data or also linked child issues and subtasks?
- Should output be only Markdown, or also JSON for automation use?
