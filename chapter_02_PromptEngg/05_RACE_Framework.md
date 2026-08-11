/*

**Task** - Bug Report for the invalid login at the app.vwo.com using RACE framework
 R — Role
 A — Action
 C — Context
 E — Expectation

R — Role A — Action C — Context E — Expectation
*/
 **Prompt**
 /*
 Create a Bug Report for the invalid login at the app.vwo.com
 R — Role - As a 15-year QA automation engineer with functional testing experience. 
 A — Action - So create a bug report in std Jira format properly with the proper context covering mandatory details .  And make sure steps, expected result, actual result and everything is basically mentioned properly in the Jira ticket or bug report that you are creating. 
 C — Context - For the invalid login, whenever I enter invalid email and invalid password, if I click on submit button, I am getting error message: account not found on app.vwo.com , Screenshot attached 
 E — Expectation - Create a bug report in the Jira format. It should be Jira compatible so that I can copy paste and directly it will be visible in Jira. */

 **output**
Bug Report: Invalid Login Error Message for app.vwo.com
Summary
Invalid login attempt on app.vwo.com displays the error message “account not found” when the user enters an invalid email and invalid password. This is a functional bug because the system should provide a standard authentication error message or handle invalid credentials gracefully without implying the account is missing when the input is invalid.

Issue Type
Bug

Priority
Medium

Severity
Major

Environment
Application: app.vwo.com
Browser: Chrome / any supported browser
OS: Windows 10 / latest
Date: 2026-08-11
User Role: End user / login user
Component
Authentication / Login / User Access

Affects Version
Current Production / Latest build

Reporter
QA Automation Engineer

Assignee
TBD

Status
Open

Description
When a user enters an invalid email and an invalid password on the login page of app.vwo.com and clicks the Submit button, the application displays the error message: “account not found”. This message is misleading and could be considered incorrect behavior because the login failure is caused by invalid credentials, not necessarily because the account does not exist.

The expected behavior is that the system should either:

show a standard invalid credentials warning, or
clearly indicate that the email/password combination is incorrect, without implying that the account itself is absent.
Steps to Reproduce
Open the application URL: https://app.vwo.com
Navigate to the login page.
Enter an invalid email address in the email field, for example: invalid.user@example.com
Enter an invalid password in the password field, for example: WrongPassword123!
Click the Submit button.
Observe the error displayed on the screen.
Expected Result
The system should display a standard invalid credentials error such as:

“Invalid email or password”
“Please check your email and password”
“Authentication failed”
This message should not suggest that the account does not exist unless the system has confirmed that the email is not registered.

Actual Result
The system displays:

“account not found”
This is misleading because the user may have entered a valid existing account email with a wrong password, or a non-existent email; the system does not provide clear or accurate feedback.

Root Cause (Likely)
The application appears to be returning a generic authentication failure message that is incorrectly mapped to the “account not found” state for invalid credentials. This may be due to improper handling of login validation responses or backend error mapping.

Evidence
Screenshot attached showing the validation message:

“account not found”
Impact
Confusing user experience
Reduces trust in the login flow
Makes troubleshooting difficult for users
May lead to incorrect assumptions about account existence
Acceptance Criteria
The login page should display a clear and accurate error message for invalid credentials.
The message should not imply that the account does not exist unless the account truly does not exist.
The behavior should be consistent for both invalid email and invalid password scenarios.
The error message should be user-friendly and technically accurate.
Suggested Fix
Validate the response from the authentication layer and map invalid credential errors to a generic “Invalid email or password” message.
Review backend error handling to ensure account existence and credential mismatch errors are not conflated.
Jira Copy-Paste Version
Title: BUG: Invalid login on app.vwo.com displays misleading "account not found" message for invalid credentials

Description:
When a user enters an invalid email and invalid password on app.vwo.com and clicks the Submit button, the system displays the error message "account not found". This is misleading and inaccurate because the user may have entered an incorrect password for an existing account, or a non-existent email. The system should display a standard invalid credentials message instead.

Steps to Reproduce:

Open https://app.vwo.com
Navigate to the login page
Enter an invalid email address, for example: invalid.user@example.com
Enter an invalid password, for example: WrongPassword123!
Click Submit
Observe the error message
Expected Result:
The application should display a standard invalid credentials validation message such as "Invalid email or password" or "Please check your email and password".

Actual Result:
The application displays "account not found".

Environment:

Application: app.vwo.com
Browser: Chrome / latest
OS: Windows 10
User Role: End user
Priority: Medium
Severity: Major
Issue Type: Bug

Impact:

Misleading login feedback
Reduced user confidence
Incorrect perception of account existence
Poor usability
Acceptance Criteria:

Invalid credentials should show an accurate validation message
The message should not imply the account does not exist unless that has been confirmed
The behavior should be consistent for invalid email and invalid password combinations

