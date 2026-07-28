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
