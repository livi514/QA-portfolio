# Scheduled Runs (GitHub Actions)

## What they are

Scheduled runs let a workflow trigger automatically at a set time, using the schedule event and cron syntax, rather than only running on push or pull_request.

YAML example:

```
on:
  schedule:
    - cron: '0 6 * * 1'
```

Cron syntax has five fields: minute hour day-of-month month day-of-week

Examples:
- `0 6 * * *` → every day at 06:00
- `0 6 * * 1` → every Monday at 06:00
- `0 */6 * * *` → every 6 hours

Combining with existing triggers.

Scheduled runs are additive, meaning that they don't replace push/pull_request, they just add another way the workflow can start:

```
on: [push, pull_request, schedule]
```

## Things to remember

- **Times are always UTC.** This means that I need to convert to local time when deciding what time I actually want it to run.
- **Scheduled runs only run on the default branch** (usually `main`), not on other branches.
- **"Best effort" timing.** GitHub can delay scheduled runs during high load, so it's not guaranteed to the exact minute. This is fine for daily/weekly checks, not for anything time-critical.
- **Scheduled runs are auto-disabled after 60 days of repo inactivity.** GitHub turns off scheduled workflows on stale repos. This is worth remembering for portfolio repos I might not touch for a while.

## Why this is useful for my repos

Normally, my workflows only run when I push or open a PR. But some things can break without me touching any code, specifically, when tests depend on an external system I don't control:
- saucedemo-playwright-tests and jsonplaceholder-api-tests both hit live external targets (saucedemo.com, JSONPlaceholder's API). If either changes something (markup, response structure, headers), I'd currently only find out next time I happen to push, which could be weeks later.
- A scheduled run catches this proactively instead of me discovering it's broken by accident.
- This mirrors a real QA/ops concept: regression detection independent of my own release cycle (like nightly builds or scheduled smoke tests against a staging environment in a real job).
- For QA-portfolio, a scheduled run gives one combined health-check signal instead of me needing to remember to check three repos separately.

## Cadence: why weekly, not daily

"CI minutes" = GitHub Actions' usage quota for running workflows. Private repos/orgs get a limited monthly allowance; public repos (like mine) get unlimited minutes on standard runners, so cost isn't really the issue for me specifically.

The real reasoning is proportionality, not expense:

- Daily runs across 3 repos × a 3-OS matrix = a lot of checks reporting "still fine" for no real benefit
- Weekly still catches drift within a reasonable window, without over-running checks nobody needs that often

Decision: weekly scheduled runs, 8am UTC on Monday mornings.