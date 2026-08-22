# Understanding the RICE POT Prompt - Plan


| **R**ole | Senior QA architect persona (15yr, CRM/Salesforce domain) — this biases output toward production patterns |
| **I**nstructions | Enterprise Selenium + Java + Maven + TestNG framework; valid + invalid login tests; TestNG annotations; exception handling; PageFactory + `@FindBy`; xpath **only** |
| **C**ontext | Target: `login.salesforce.com/?locale=in` (Indian locale, may serve different HTML). Login has username, password, submit, remember-me |
| **E**xample | Shows the exact code pattern expected — `@FindBy(xpath = "...")`, `PageFactory.initElements()`, action methods like `doLogin()` |
| **P**arameters | External credentials provided separately; production-grade precision demanded |
| **O**utput | Exactly 3 code files + Maven project. No explanations, no comments, no fluff |
| **T**one | Terse, precise, enterprise-grade. No `Thread.sleep`, no bad practices |

**The core tension**: "Enterprise-level framework" implies many files (base classes, utilities, config), but "Output: 1 Page Object, 2 TestNG scripts, Maven project" caps the deliverable count. My plan resolves this by building a full enterprise scaffold but keeping the user-facing deliverable focused on the 3 core files + `pom.xml`.

---

## Plan: Salesforce Login Selenium Framework (RICE POT)

**TL;DR** — Build inside `chapter_02/RICE_POT_SeleniumAdvanceFramework/`. Deliver: 1 Page Object (xpath-only `@FindBy`), 2 TestNG scripts (valid + invalid login), Maven `pom.xml`, plus enterprise scaffold (BaseTest, ConfigReader, WaitUtils). Live DOM fetched first.

### Phase 1: Scaffolding

| Step | What | Depends On |
|---|---|---|
| 1 | **Fetch live DOM** from `login.salesforce.com/?locale=in` to extract real xpaths | — |
| 2 | Create Maven directory structure under `chapter_02/RICE_POT_SeleniumAdvanceFramework/` | — |
| 3 | Create `pom.xml` (Selenium 4.x, TestNG 7.x, WebDriverManager 5.x, Maven Surefire) | Step 2 |

### Phase 2: Utilities & Config

| Step | What |
|---|---|
| 4 | `config.properties` — `base.url`, `valid.username=PLACEHOLDER`, `browser=chrome`, wait timeouts |
| 5 | `ConfigReader.java` — singleton, loads from classpath |
| 6 | `WaitUtils.java` — `WebDriverWait` wrapper; zero `Thread.sleep` |

### Phase 3: Base Test

| Step | What |
|---|---|
| 7 | `BaseTest.java` — `@BeforeTest` (WebDriverManager init, maximize, navigate), `@AfterTest` (quit), protected `driver` + `loginPage` fields |

### Phase 4: Page Object

| Step | What |
|---|---|
| 8 | `LoginPage.java` — `@FindBy(xpath="...")` for all elements; `PageFactory.initElements()`; action methods (`enterUsername`, `enterPassword`, `clickLogin`, `doLogin`, `getErrorMessageText`, `isErrorMessageDisplayed`, `checkRememberMe`); all wrapped in try-catch |

### Phase 5: Test Scripts

| Step | What | Tests |
|---|---|---|
| 9 | `ValidLoginTest.java` (extends BaseTest) | 3 tests: valid credentials, remember-me checked, UI elements rendered |
| 10 | `InvalidLoginTest.java` (extends BaseTest) | 5 tests: wrong password, empty username, empty password, both empty, invalid email format |

### Phase 6: Suite Config

| Step | What |
|---|---|
| 11 | `testng.xml` at project root — suite referencing both test classes |

### Phase 7: Verification

| Step | What |
|---|---|
| 12 | `mvn compile` — zero errors |
| 13 | `mvn test` with placeholders — validates xpaths, browser launches, no NPE |
| 14 | Grep checks: no `By.id/name/cssSelector/className`, no `Thread.sleep`, no comments in Java files |

### Key Decisions

- **xpath with `@id` allowed** — `//input[@id='username']` is valid xpath. "Don't use ID" means no `By.id()` strategy.
- **`config.properties` with placeholders** — credentials filled in when provided; no hardcoding.
- **Live DOM fetch is Step 1** — Salesforce can serve different HTML to the Indian locale; fetched DOM is authoritative.
- **8 total test cases** — 3 valid + 5 invalid, covering happy path and edge cases.

### Further Considerations

1. **CAPTCHA/SSO risk**: If the target Salesforce org has CAPTCHA or SSO, automated login will fail. This is a known limitation.
2. **Headless mode**: Add `headless=true/false` config flag for CI/CD readiness (not in initial deliverable but easy to add).
3. **Cross-browser**: Structure supports it; add `FirefoxDriver`/`EdgeDriver` branches in BaseTest when needed.
