# VWO Login Module Test Plan Prompt

**R - Role:**
Role: Act as a Seasoned Test Manager with extensive experience in enterprise software quality assurance, test strategy formulation, and standard compliance.

**I - Intent (Task & Scope):**
Your task is to collaborate conceptually with a Project Manager to create an industry-level, standard Master Test Plan defining the comprehensive testing approach for the Login module. The Test Plan must thoroughly detail the following core sections:
Standard Test Plan Parameters
#	Test Plan Parameter	What it covers
1	Test Plan ID & Version	Unique identifier, version, author, date and document history
2	Objective	What the testing is intended to achieve
3	Scope	Features/modules that will and will not be tested
4	Testing Strategy / Approach	Overall approach: functional, regression, integration, API, automation, UAT, etc.
5	Test Types	Functional, integration, system, regression, performance, security, usability, compatibility, etc.
6	Test Environment	Application version, servers, browsers, OS, devices, databases, APIs, etc.
7	Test Data	Data required for testing, including positive, negative and boundary data
8	Entry Criteria	Conditions that must be satisfied before testing starts
9	Exit Criteria	Conditions that must be satisfied before testing is considered complete
10	Test Deliverables	Test plan, test cases, execution reports, defect reports, test summary report, metrics, etc.
11	Roles & Responsibilities	QA, developers, BA, product owner, automation engineers, business users, etc.
12	Schedule & Milestones	Test preparation, execution, regression, UAT, release dates
13	Defect Management	Defect lifecycle, severity/priority, triage process and reporting
14	Tools	JIRA, Azure DevOps, TestRail, Postman, Selenium/Playwright, CI/CD tools, etc.
15	Risks & Mitigation	Potential testing risks and how they will be addressed
16	Assumptions & Dependencies	External systems, environments, requirements, teams, data, APIs, etc.
17	Test Metrics & Reporting	Test execution %, pass/fail rate, defect density, severity distribution, coverage, leakage, etc.
18	Entry/Exit Approval	Stakeholders responsible for approving test start and release readiness

**C - Context & Constraints:**
 Base this entire Test Plan strictly on the requirements for the VWO Login page ([https://app.vwo.com/#/login](https://app.vwo.com/#/login)).
•	Constraint 1: Work exclusively with the specific requirements listed in the requirement doc attached.
•	Constraint 2: Do not assume undocumented software behavior or architectural layers.
•	Constraint 3: If any critical technical detail required for a section is missing from the provided context, explicitly write "Information not provided in requirement" rather than inventing details.

**E - Expectations:**
 The final Test Plan must ensure that all explicit functional, security, and session validation bounds of the login module can be successfully and measurably tested. It must integrate standard QA metrics and industry-level verification parameters.

**P - Parameters (Core Inputs):**
 Ensure your strategies map directly to these 5 core requirements in the attached requirement doc

**O - Output Format:**
 Generate the Test Plan in a highly structured, clean Markdown format. Use professional corporate headings (#, ##, ###), tables for criteria/estimations, and blockquotes for highlights so the output is cleanly formatted and ready to be exported directly into a PDF document.

**T - Tolerance (Anti-Hallucination Guardrails):**
•	STRICT POLICY: Do not assume default, "typical," or generic system behaviors.
•	If the requirement does not mention a database type, server environment, or specific tool names, do not invent them; mark them as "Not Specified in Input Context."
•	Zero tolerance for hallucinating features, UI layouts, or back-end behaviors. Stick entirely to the facts provided.

