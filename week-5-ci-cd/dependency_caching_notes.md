# Dependency Caching (GitHub Actions)

## The problem it solves

Every workflow run starts on a **completely fresh runner**, meaning a separate filesystem, nothing installed, nothing left over from last time (this is the same reason each job needs its own `checkout` + `setup-python` steps, even within one workflow).

That means every single run has to redo the same expensive setup work from scratch:
- `pip install -r requirements.txt` — re-downloads and re-installs every package, every time
- `playwright install` — re-downloads entire browser binaries (chromium, firefox, webkit), every time

Multiply this by:
- Every push and PR
- Every job in a matrix (3 OSes = 3x the installs)
- The fact that most of the time, **nothing in `requirements.txt` has actually changed** between runs

Most of that install work is pure repetition. Caching exists to stop repeating it unnecessarily.

## The core idea

Caching lets a workflow **save specific files/folders after a run, and restore them at the start of a later run**, instead of regenerating them from scratch every time.

For dependencies specifically: instead of re-downloading and reinstalling every package, GitHub Actions can restore a previously-saved copy of those installed packages, *if* it can confirm nothing has changed that would make the old copy invalid.

## How it decides whether to use the cache: the cache key

Every cache is saved under a **key**, which is a string that acts as its identifier. The key is typically built from something that changes only when the dependencies actually change, most commonly a **hash of the requirements file**:

```yaml
key: playwright-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
```

- `hashFiles('requirements.txt')` generates a fingerprint of that file's exact contents.
- If `requirements.txt` hasn't changed since the last run → same hash → same key → **cache hit** → restore the saved packages instead of reinstalling.
- If `requirements.txt` *has* changed (e.g. I added a new dependency) → different hash → different key → **cache miss** → no matching cache found, so it installs fresh, then saves a new cache under the new key for next time.

This is why the cache is safe to rely on: it's not "assume nothing changed," it's "only reuse this if a fingerprint check proves nothing changed."

`runner.os` is included in the key too, because installed packages/binaries aren't necessarily portable between Ubuntu/Windows/macOS — so each OS in the matrix gets its own separate cache, not one shared cache across all three.

## Two ways to apply it

**1. Built into `setup-python` (simplest)**

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.13'
    cache: 'pip'
```

This one line handles the pip-caching logic automatically — keys it off `requirements.txt` under the hood, no manual key-writing needed.

**2. `actions/cache` directly (more control)**

Needed when caching something that isn't just pip packages, e.g. Playwright's downloaded browser binaries, which live in a different location than pip packages and are arguably the *slowest* part of UI test setup, not the pip install itself.

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/ms-playwright
    key: playwright-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
```

- `path` = what to actually save/restore (the cache doesn't know what "Playwright browsers" means, just a folder path)
- `key` = the fingerprint that decides hit vs. miss

## Why this matters for my repos specifically

- Before adding dependency cachig, the matrix jobs (3 OSes) reinstalled everything 3x per run, for setup work that's usually identical to last time.
- Playwright's browser downloads are a heavier, slower install than plain pip packages, so the biggest potential time-save is caching those specifically in `saucedemo-playwright-tests`.
- `jsonplaceholder-api-tests` is simpler (no browsers), so plain `cache: 'pip'` covers it.
- Net effect: faster CI runs, without changing what's actually being tested. This is a "make CI faster" change, not a "change test behaviour" change.