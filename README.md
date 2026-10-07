# QA Summer Roadmap
 
This repository documents completed work from a self-directed QA automation roadmap, built week by week. See [Progress](#progress) for the topics covered.
 
## What this is
 
A structured, self-directed roadmap for building QA automation skills toward internship-readiness, with a particular focus on public sector and civil service QA/SDET roles. Each week has its own folder with working code, notes, and a written summary of what was covered.
 
## Progress
 
- **[Done] Week 1 — Playwright Basics:** first Playwright UI tests, locators, assertions
- **[Done] Week 2 — Playwright Intermediate + POM:** Page Object Model, fixtures, headless mode
- **[Done] Week 3 — Playwright Polish:** test configuration, test data files, tidied-up test suite (later published standalone as [saucedemo-playwright-tests](https://github.com/livi514/saucedemo-playwright-tests))
- **[Done] Week 4 — API Testing:** pytest + requests API suite against JSONPlaceholder, CRUD coverage, negative tests, performance and security checks (later published standalone as [jsonplaceholder-api-tests](https://github.com/livi514/jsonplaceholder-api-tests))
- **[Done] Week 5 — CI/CD with GitHub Actions:** automated linting and testing, multi-job and cross-platform workflows, scheduled runs, dependency caching.
- **[Done] Week 6 — Test Design Techniques pt1:** Boundary Value Analysis, Equivalence Partitioning
- **[Done] Week 7 — Test Design Techniques pt2:** Decision Tables, State Transition Testing, exploratory heuristics
 
## Repo structure
 
```
QA-portfolio/
├── .github/workflows/       — CI: linting + tests (UI and API), matrix across Ubuntu/Windows/macOS
├── week-1-playwright-basics/
├── week-2-playwright-intermediate/
├── week-3-playwright-polish/   — also published standalone as saucedemo-playwright-tests
├── week-4-api-testing/         — also published standalone as jsonplaceholder-api-tests
├── week-5-ci-cd/                — CI/CD notes (GitHub Actions, workflows, caching, scheduled runs)
├── week-6-bva-ep/                — BVA and EP notes, and practical application using the Open-Meteo API          
├── week-7-test-design-techniques-pt2/ — decision tables, state transitions, and exploratory testing
├── requirements.txt
└── setup.cfg
```
 
Alongside this overall README, each week folder contains its own `README_weekN.md` with a full breakdown of that week's goals, what was built, and what was learned.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/livi514/QA-portfolio.git
   cd QA-portfolio
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   ```
   Windows:
   ```
   .venv\Scripts\activate
   ```
   macOS/Linux:
   ```
   source .venv/bin/activate
   ```

3. Install dependencies (from the repo root):
   ```
   pip install -r requirements.txt
   ```

4. Install Playwright browsers (needed for Weeks 1–3 and Week 7):
   ```
   playwright install
   ```

Each week's own README then only covers navigating into that week's folder and the specific `pytest` commands relevant to it.
 
## CI
 
Linting and tests run automatically on every push and pull request via GitHub Actions, and on a weekly schedule (8am UTC on Mondays) to catch drift independent of new commits. Linting applies to the overall repository; the UI and API test workflows run the Week 3 and Week 4 suites, respectively.
 
![UI Tests](https://github.com/livi514/QA-portfolio/actions/workflows/ui_tests.yml/badge.svg)
![API Tests](https://github.com/livi514/QA-portfolio/actions/workflows/api_tests.yml/badge.svg)
![Lint](https://github.com/livi514/QA-portfolio/actions/workflows/lint.yml/badge.svg)
