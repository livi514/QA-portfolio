# Writing Workflows / YAML Files  

When writing a GitHub Actions workflow, the basic structure always follows the same pattern:

1. **Give the workflow a name**  
This is just a label so you can recognise it in the Actions tab.
   Example:  
   `name: UI Tests`

2. **Define the events that trigger it**
Define what events should cause the workflow to run.  
   Example:  
   `on: [push, pull_request]`
  
You can also use more advanced triggers later, like:
- `on: schedule:` (cron jobs)
- `on: workflow_dispatch` (manual trigger)
- `on: issues:` (issue automation)
- `on: release:` (deployment pipelines)
(Note to self: I've only used push/pull_request so far. I want to experiment with scheduled workflows and manual triggers.)

3. **Define the jobs and steps**  

## Jobs and Steps

A workflow can have multiple jobs, and each job can have multiple steps.
So far, I've only used single-job workflows, but multi-job workflows are useful for:
- running tests in parallel (e.g. API + UI tests)
- building on one job, then deploying in another
- running a matrix of environments, then combining results

### Defining a job

To start defining jobs, use the `jobs:` keyword.  
Then give the job a name (e.g. `test`) and specify the runner environment:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

The `runs-on` keyword tells GitHub which runner to use.
Common options:
- `ubuntu-latest`
- `windows-latest`
- `macos-latest`
You can also use self-hosted runners later.

### Defining steps

Each step starts with a dash (`-`).

You can give steps names using `name:`: to make logs easier to read.

For example:

```yaml
- name: Set up Python
```
Steps use two main keywords: `uses` and `run`.

#### `uses`:

Calls a pre-built GitHub Action.
Example:

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
```

#### `run`:

Executes shell commands directly.
Example:

```yaml
- name: Install dependencies
  run: pip install -r requirements.txt
```

#### Passing configuration with `with`:

You can also pass configuration to actions using `with:` — for example, specifying a Python version:

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.13'
```

#### Uploading artifacts

```yaml
- name: Upload test report
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: ui-test-report
    path: week-3-playwright-polish/report.html
```

## Full YAML Example

```yaml
name: UI Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Install browsers
        run: playwright install --with-deps chromium firefox webkit

      - name: Run tests
        run: pytest week-3-playwright-polish/tests \
             --html=week-3-playwright-polish/report.html \
             --self-contained-html

      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: ui-test-report
          path: week-3-playwright-polish/report.html
```
## Multi-Job Workflows

Multi-job workflows allow you to run multiple jobs inside a single workflow file.
Each job is isolated, has its own runner, and can run either:
- in parallel (default)
- in sequence usnign `needs:`

This is useful when a workflow has multiple phases or multiple variations of the same task.

## Why multi-job workflows exist

Multi-job workflows are designed for situations where one workflow needs to perform several related tasks that belong together.

Examples:

### Build → Test → Deploy
A classic CI/CD pipeline:
- Job 1: build the app
- Job 2: run tests (depends on build)
- Job 3: deploy (depends on tests)

### Lint → Test
A simple two‑phase pipeline:
- Job 1: lint the code
- Job 2: run tests only if linting passes

### Test across multiple environments
Same tests, different OS or Python versions:
- Job 1: test on Ubuntu
- Job 2: test on Windows
- Job 3: test on macOS

### Fan‑out / fan‑in patterns

Advanced pipelines:
- Job 1: generate artifacts
- Job 2–4: run parallel jobs using those artifacts
- Job 5: combine results

## How jobs work in multi-job workflows

Jobs run on separate machines. This means that each job gets its own fresh runner:
- separate filesystem
- separate environment
- separate logs 
This is why jobs don't share state unless you explicitly specify dependencies.

Steps run sequentially inside a job, but jobs themselves run in parallel unless you specify dependencies.

Use `needs:` to control order, for example:

```
jobs:
  lint:
    runs-on: ubuntu-latest

  tests:
    runs-on: ubuntu-latest
    needs: lint
```

This makes `tests` wait for `lint` to finish.

## When multi-job workflowws do not make sense

Multi‑job workflows are not for combining unrelated tasks.

For example, in this repo:
- UI tests
- API tests
- Linting

These are different responsibilities, so they belong in separate workflows, not separate jobs inside one workflow.

Multi‑job workflows are for one workflow with multiple phases, not for merging everything into one giant file.

## Multi-job workflow vs multiple workflows 

| Concept | When to use it | Example |
| --- | --- | --- |
| **Multi‑job workflow** | One workflow with multiple phases or variations of the same task | Lint → Test, Test on 3 OSes |
| **Multiple workflows** | Completely different tasks | UI tests, API tests, Linting |

## Cross-Platform Workflows 

Running workflows across multiple operating systems (Ubuntu, macOS, Windows) is a great way to make your CI pipeline more robust. It also exposes weird OS-specific behaviour you wouldn't notice otherwise, suhc as Windows being slower or macOS resolving paths differently.

This is where matrix strategies and shell selection become important.

### Matrix strategy (multi-OS testing)

You can run the same job on multiple OSes using a matrix:
```
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
```

This automatically creates three jobs:
- ui-tests (ubuntu-latest)
- ui-tests (windows-latest)
- ui-tests (macos-latest)
All running in parallel.

This is how I have chosen to practice multi-job workflows in this repo.

### Shell differences

One of the biggest issues I came across when setting up cross-platform workflows for this repository, is that the various GitHub runners use different default shells:
- Ubuntu → Bash
- macOS → Bash
- Windows → PowerShell (!!!)

PowerShell does not understand:
- --html=report.html
- --self-contained-html
- \ line continuation
- most Bash syntax

So commands that work perfectly on Ubuntu/macOS will explode on Windows with errors like:
`Missing expression after unary operator '--'`

Fix: force Bash on Windows 
`shell: bash`

This makes your test commands behave consistently across all OSes.

### Performance differences (Windows is slower)

Windows runners have slower network performance, so API tests with strict timing thresholds may fail:
`AssertionError: /users took 1.10s`

Ubuntu and macOS passed my initial performance test (with the threshold set to 1.0), because their network latency was lower. However, Windows was a bit too slow.

I had several fix options:
- increase the threshold (e.g., 1.5s) - this is the option I chose!
- skip performance tests on Windows
- only run API tests on Ubuntu / macOS

This was a real-world CI issue, not a bug in my code.

