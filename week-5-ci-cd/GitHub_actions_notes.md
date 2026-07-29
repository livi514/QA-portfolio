# GitHub Actions - Overview

GitHub Actions is a **continuous integration and continuous delivery (CI/CD)** platform built into GitHub that lets you automate your build, test, and deployment pipelines, directly inside a GitHub repository. You can create workflows that run your test suite on every push or pull request, deploy code when a release is created, or even automate small tasks like adding labels to issues.

GitHub Actions goes beyond just DevOps and lets you run workflows when other events happen in your repository. For example, you can run a workflow to automatically add the appropriate labels whenever someone creates a new issue in your repository.

GitHub provides Linux, Windows, and macOS virtual machines to run your workflows, or you can host your own self-hosted runners in your own data center or cloud infrastructure.

## My setup

I created workflows for three related repositories:
-  **QA‑portfolio:** my overall QA Summer Roadmap repo
- **saucedemo-playwright-tests:** UI tests (Weeks 1–3)
- **jsonplaceholder-api-tests:** API tests (Week 4)

Each repo has workflows for running automated tests and checking linting/formatting.

You can configure a GitHub Actions workflow to be triggered when an event occurs in your repository, such as a pull request being opened or an issue being created. For example, I set up all my workflows so that they run on every push and every pull request, so I get immediate feedback whenever I update code.

## Checking workflow results

Let's say you make an edit to your code and push it. You will then be able to see whether it passed (green tick) or failed (red cross) under the Actions tab for your GitHub repository. This is a quick way to see if there are any issues at first glance. However, it's important to check further. A "passed" workflow doesn't always mean that everything worked perfectly.

For example, you may see warnings. When I was trying to set up test reports for QA-portfolio, the workflows "passed" even when the report was not generated. This shows that it's crucial to look at the results of your workflows beyond just checking the tick/cross. Beyond checking that artifacts are generated, it's also crucial to check the format, which is why I downloaded and read through the test reports even when I had passing workflows.

## Workflows

A workflow is a configurable automated process that will run one or more jobs. Workflows are defined by a YAML file checked in to your repository, and will run when triggered by an event in your repository (for example on every push or on every pull request). Alternatively, they can be triggered manually, or at a defined schedule.

Workflows are defined in the .github/workflows directory in a repository. A repository can have multiple workflows, each of which can perform a different set of tasks:
- Building and testing pull requests
- Deploying your application every time a new release is created
- Adding a label whenever a new issue is opened

For example, in my QA-Porfolio repository, I have 3 workflows: UI tests, API tests, and linting.

You can also reference a workflow within another workflow.

Workflows are triggered by events.

Workflows contain jobs, and jobs contain steps.

## Events

An event is a specific activity in a repository that triggers a workflow run. For example, an activity can originate from GitHub when someone creates a pull request, opens an issue, or pushes a commit to a repository. You can also trigger a workflow to run on a schedule, by posting to a REST API, or manually.

## Jobs

A job is a sequence of steps in a workflow that is executed on the same runner. Each step is either a shell script that will be executed, or an action that will be run. Steps are executed in order, and are dependent on each other. Since steps are executed on the same runner, you can share data from one step to another. For example, you can have a step that builds your application, followed by a step that tests that the application was built.

Steps within a job always run sequentially, one after another, on the same runner. GitHub Actions does not support running steps concurrently within a single job. If you need genuine parallel execution (for example, running a long-running service while other work continues), you need separate **jobs**, since jobs run in parallel by default unless you link them with `needs:`.

You can configure a job's dependencies with other jobs. By default, jobs have no dependencies, and run in parallel. When a job takes a dependency on another job, it waits for the dependent job to complete before running. Jobs run in parallel unless you define dependencies using `needs:`.

You can also use a matrix to run the same job multiple times, each with a different combination of variables, like operating systems or language versions. For example, you might configure multiple build jobs for different architectures without any job dependencies and a packaging job that depends on those builds. The build jobs run in parallel, and once they complete successfully, the packaging job runs.

## Writing workflow YAML files:

Give the workflow a name, e.g. "name: UI Tests"
Specify when you want to run the workflow, e.g. "on: [push, pull_request]"
Then, you outline the jobs in the workflow, and the steps for each job. For each step, you have to include the commands needed.

The basic structure looks like this:

```
name: UI Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
(and more steps...)
```

An example of a step uploading a test report:

```
- name: Upload test report
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: ui-test-report
    path: week-3-playwright-polish/report.html
```

## Actions

An action is a predefined, reusable set of jobs or code that performs specific tasks within a workflow, reducing the amount of repetitive code you write in your workflow files. Actions can perform tasks such as:
- Pulling your Git repository from GitHub
- Setting up the correct toolchain for your build environment
- Setting up authentication for your cloud provider

You can write your own actions, or you can find actions to use in your workflows in the GitHub Marketplace.

## Runners

A runner is a server that runs your workflows when they're triggered. Each runner can run a single job at a time. GitHub provides Ubuntu Linux, Microsoft Windows, and macOS runners to run your workflows. Each workflow run executed in a fresh, newly-provisioned virtual machine.

GitHub also offers larger runners, which are available in larger configurations.

If you need a different operating system or require a specific hardware configuration, you can host your own runners.