# QA Summer Roadmap — QA Portfolio
 
**Work in progress**. 

This repository documents a self-directed 12-week QA automation roadmap, built week by week. Some sections are complete and polished; others are still in progress, and might shift slightly as I go. See [Progress](#progress) below for exactly where things stand.
 
## What this is
 
A structured, self-directed roadmap for building QA automation skills toward internship-readiness, with a particular focus on public sector and civil service QA/SDET roles. Each week has its own folder with working code, notes, and a written summary of what was covered.
 
## Progress
 
- **[Done] Week 1 — Playwright Basics:** first Playwright UI tests, locators, assertions
- **[Done] Week 2 — Playwright Intermediate + POM:** Page Object Model, fixtures, headless mode
- **[Done] Week 3 — Playwright Polish:** test configuration, test data files, tidied-up test suite (later published standalone as [saucedemo-playwright-tests](https://github.com/livi514/saucedemo-playwright-tests))
- **[Done] Week 4 — API Testing:** pytest + requests API suite against JSONPlaceholder, CRUD coverage, negative tests, performance and security checks (later published standalone as [jsonplaceholder-api-tests](https://github.com/livi514/jsonplaceholder-api-tests))
- **[In progress] Week 5 — CI/CD with GitHub Actions:** automated linting and testing, multi-job and cross-platform workflows, scheduled runs, dependency caching — core setup working, README and final polish still underway
- **[Not started] Week 6 — Test Design Techniques:** Boundary Value Analysis, Equivalence Partitioning, Decision Tables, State Transition Testing, exploratory heuristics
- **[Not started] Week 7 — SQL for QA (Part 1):** SELECT, WHERE, ORDER BY, filtering
- **[Not started] Week 8 — SQL for QA (Part 2):** joins, aggregations, validating test data with SQL
- **[Not started] Week 9 — Accessibility Testing:** WCAG, Axe DevTools, keyboard navigation, colour contrast
- **[Not started] Week 10 — QA Documentation:** test plans, test cases, bug reports, exploratory testing summaries
- **[Not started] Week 11 — Finalise QA Portfolio Repo:** proofreading and finalising this repository
- **[Not started] Week 12 — LinkedIn + CV Polish:** updating profile and CV with new skills

Note: this plan may adapt as I go. Some weeks might take longer than planned, or get adjusted based on what I find most valuable as I progress.
 
## Repo structure
 
```
QA-portfolio/
├── .github/workflows/       — CI: linting + tests (UI and API), matrix across Ubuntu/Windows/macOS
├── week-1-playwright-basics/
├── week-2-playwright-intermediate/
├── week-3-playwright-polish/   — also published standalone as saucedemo-playwright-tests
├── week-4-api-testing/         — also published standalone as jsonplaceholder-api-tests
├── week-5-ci-cd/                — CI/CD notes (GitHub Actions, workflows, caching, scheduled runs)
├── requirements.txt
└── setup.cfg
```
 
Alongside this overall README, each week folder contains its own `README_weekN.md` with a full breakdown of that week's goals, what was built, and what was learned.
 
## CI
 
Linting and tests run automatically on every push and pull request via GitHub Actions, and on a weekly schedule (8am UTC on Mondays) to catch drift independent of new commits. Linting and testing workflows are kept separate here, as linting applies to the overall repository while the testing workflows only apply to specific folders.
 
![UI Tests](https://github.com/livi514/QA-portfolio/actions/workflows/ui_tests.yml/badge.svg)
![API Tests](https://github.com/livi514/QA-portfolio/actions/workflows/api_tests.yml/badge.svg)
![Lint](https://github.com/livi514/QA-portfolio/actions/workflows/lint.yml/badge.svg)