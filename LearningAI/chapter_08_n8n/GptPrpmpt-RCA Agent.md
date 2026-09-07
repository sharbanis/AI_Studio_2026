You are an expert n8n workflow architect, Jira automation specialist, QA Lead, and AI automation engineer.

Build an end-to-end n8n workflow from scratch that automatically creates and maintains a Production Defect Root Cause Analysis (RCA) in an Excel file whenever a Production Bug is created or identified in Jira.

The workflow must be production-ready, modular, fault-tolerant, auditable, and designed so that the AI NEVER invents RCA information that is not available in Jira or another approved source.

==================================================

BUSINESS OBJECTIVE
==================================================

Whenever a Jira issue representing a Production Bug is created or identified:

Automatically trigger the n8n workflow.

Identify the Jira Production Bug using Jira/JQL.

Fetch the complete Jira issue details.

Fetch relevant comments, worklogs, linked issues, status, priority, severity, labels, components, assignee, reporter, sprint/release information and available custom fields.

Extract all information relevant to the RCA.

Map the Jira information to the required RCA fields.

Use AI only for classification, summarization, normalization and structured analysis.

Do NOT fabricate missing RCA information.

Clearly mark information that is unavailable as:
"Not Available in Jira - Investigation Required"

Create a new RCA record in the Excel RCA file.

If the same Jira defect already exists in the Excel file, update the existing RCA record instead of creating a duplicate.

Maintain an audit trail of when the RCA was created or updated.

Return a clear execution summary.

================================================== 2. JIRA PRODUCTION BUG IDENTIFICATION

Use Jira JQL to identify Production Bugs.

Make the JQL configurable through a Set/Config node.

Default example:

project = YOUR_PROJECT
AND issuetype = Bug
AND environment ~ "Production"
AND statusCategory != Done
ORDER BY created DESC

Also support configurable alternatives such as:

project = YOUR_PROJECT
AND issuetype = Bug
AND labels = production
AND statusCategory != Done
ORDER BY created DESC

The workflow must NOT hard-code project names, issue types, custom field IDs, severity values, or environment values.

Create a configuration section where the following can be changed easily:

Jira Base URL

Jira Project Key

Production label

Production environment value

Bug issue type

Severity field

Priority field

RCA Excel file path