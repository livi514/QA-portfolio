# QA Summer Roadmap - Week 5

## Introduction 

Week 5 of my QA Summer Roadmap focuses on CI/CD with GitHub Actions, which was a fairly new concept for me. Before setting this up, I had to run tests manually every time, repeating the same setup steps and terminal commands whenever I wanted feedback on my code.

My initial goal was to create YAML workflows to run UI and API tests automatically, generate test reports for each workflow, and add the relevant status badges to my READMEs.

By the end of the week, though, I'd gone well beyond these goals, also covering multi-job and cross-platform workflows, scheduled runs, and dependency caching. I now have workflows set up across three repositories: QA-Portfolio (this repository), as well as saucedemo-playwright-tests and jsonplaceholder-api-tests, covering linting and test automation across three operating systems.

## What I did

I started with basic test workflows for all three repos (QA-portfolio, saucedemo-playwright-tests, and jsonplaceholder-api-tests). This introduced me to the process of setting up a YAML file and how to check the status of my workflows on GitHub.

I then wanted to practice setting up workflows further, by also adding a linting workflow to each repository.

Upon reviewing some CI/CD and GitHub Actions theory and trying to identify ways to expand my practical work further, I came across multi-job and cross-platform workflows. Initially, my workflows had only been running on Ubuntu, so I expanded them to run across all three available operating systems.

I also considered how I could use multi-job workflows more deliberately. I decided to combine the lint and test workflows in saucedemo-playwright-tests and jsonplaceholder-api-tests into a single two-job workflow with a lint→test dependency. This means a set of linters runs first, and the tests only run if linting passes.

However, I kept the three workflows in QA-portfolio separate, since they cover distinct responsibilities. Unlike in the other two repos, they also apply to different directories: linting covers the whole repository, while the UI tests only apply to `week-3-playwright-polish` and the API tests only apply to `week-4-api-testing`.

After this, I identified another issue. At that point, my workflows only ran on pushes and pull requests, but I wanted them to run more regularly, for example, even if I hadn't touched a repository in several weeks. My tests depend on external resources that could change without my knowledge, so the best way to stay aware of that was to set up scheduled runs. I scheduled my workflows to run at 8am UTC every Monday.

Finally, I added dependency caching. This was something I explored out of curiosity, and I was glad to find it addressed a problem I'd already noticed: long execution times in my matrix runs.

## What I learned

### Testing Beyond My Machine

GitHub Actions allows you to run your workflows across multiple operating systems, so you are not just limited to the OS of your local machine. Without CI, cross-platform testing wouldn't be realistic for one person to do. For example, my workflow, which used bash-specific multi-line syntax, failed on the Windows runner, since Windows defaults to PowerShell, not Bash. I fixed this by adding `shell: bash` to the relevant steps, forcing them to run in Bash regardless of the runner's OS.

### Convenience vs. Reality

One thing that I really appreciated about GitHub Actions was the visual clarity of the tick / cross system for seeing whether a workflow passed or failed at a glance. However, this system is misleadingly simple. A cross is fairly conclusive: it essentially guarantees something is wrong, even though you still have to investigate the specific issue or which specific step failed. Ticks, on the other hand, are far less conclusive. For example, I encountered an issue when trying to generate test reports, where the workflow was shown as passing, despite the report not being generated. This example shows the importance of checking the results of workflows further, including checking for any warnings, and downloading and reading through any generated artifacts.

### Removing Reliance on my own Memory and Effort

One thing this week made clear was how easily external changes could slip past me. My tests depend on resources outside my control, and without scheduled runs, discovering that something had changed came down to luck: I'd only catch it if I happened to run the tests around the same time something broke. Scheduling replaces this luck with regularity, removing my reliance on memory to manually check things outside of pushes or pull requests.

## Key takeaways from this week 

This week taught me two skills that feel almost like opposites (zoom in vs. zoom out), but actually complement each other. QA Engineers have a duty to users, to provide them with a high-quality product, and both these skills are crucial when it comes to achieving this.

On one hand, you need the ability to cover all possibilities and look at the big picture. You need to understand how all components of the system work together, as well as being able to cover the different behaviours and environments that users might have. An example of this from this week was using the cross-platform testing, which allowed me to test operating systems beyond the one on my local machine. 

On the other hand, you need to have a keen attention to detail, and be able to investigate beyond just what you see on the surface. For example, when I was initially trying to generate test reports, my workflows were shown as "passing" despite the reports not being generated properly. This undermined my trust in my own processes and showed how a "passing" status could mislead the development team. 

Attention to detail is also crucial to maintain a high-quality user experience. This includes security, for example, in week 4, JSONPlaceholder was missing crucial security headers such as Strict-Transport-Security. Strict-Transport-Security (HSTS) tells the browser to always use HTTPS with the site. Without it, the site could fall back to HTTP, which is unencrypted. A user's connection could be intercepted before upgrading to HTTPS, especially on something like public WiFi, potentially exposing sensitive information, such as login credentials.

Overall, my takeaway from this week is that broad coverage is worthless if you're not rigorous enough to actually verify each result properly. Big-picture thinking and attention to detail aren't separate skills, they depend on each other.

## Checking Workflows

Unlike previous weeks, there are no tests to run manually here — the workflows in `.github/workflows/` run automatically. This section covers how to check their results.

**Workflow files:** located in `.github/workflows/` at the repo root — `ui_tests.yml`, `api_tests.yml`, and `lint.yml`.

**Viewing results on GitHub:**
1. Go to the **Actions** tab on the repository
2. Select a workflow run to see its jobs
3. Click into a specific job to see its individual steps and logs

**What to actually check, beyond the tick/cross:**
- A green tick means the checks you wrote passed. It doesn't guarantee everything worked as expected. Click into individual steps to confirm each one actually ran and did what it was supposed to, not just that the job as a whole didn't fail.
- Download and read through any generated test report artifacts, rather than assuming a pass means the report is complete or correctly formatted.
- For matrix runs (tests across Ubuntu, Windows, and macOS), check all three OS results individually, as a pass on one doesn't guarantee a pass on the others.
- If you want to confirm dependency caching is working, expand the "Cache" step in a job's logs. It will explicitly say `Cache restored from key: ...` (hit) or `Cache not found for input keys: ...` (miss). Note the first run after adding caching will always be a miss.

**Triggering a run manually:** each workflow includes `workflow_dispatch`, so you can trigger a run on demand from the Actions tab (select the workflow → "Run workflow") without waiting for a push, PR, or the Monday schedule.