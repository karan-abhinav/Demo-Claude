# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a personal expense-tracker web app built with Flask and SQLite. It is a **teaching/scaffold project** — most of the data and auth layer is intentionally unimplemented, with comments marking what students are expected to build (e.g. `database/db.py` says "Students will write this file in Step 1", `app.py` placeholder routes say "coming in Step N"). **Do not implement a stub unless the active task explicitly targets that step** — these are deliberate checkpoints, not oversights.

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run dev server — serves at http://127.0.0.1:5001, debug mode on
python app.py

# Run all tests
pytest

# Run a specific test file
pytest tests/test_foo.py

# Run a specific test by name
pytest -k "test_name"

# Run tests with output visible
pytest -s
```

There is no build step, linter, or frontend tooling configured (no webpack/vite, no ESLint/Prettier). `pytest`/`pytest-flask` are already in `requirements.txt` but no `tests/` directory exists yet.

## Architecture

- **`app.py`** — single Flask entry point; every route lives here directly (no blueprints). Implemented routes (`/`, `/register`, `/login`, `/terms`) call `render_template()`. Unimplemented feature routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<int:id>/edit`, `/expenses/<int:id>/delete`) currently `return` a placeholder string instead of a template — that's expected until their step is implemented.
- **`database/db.py`** — reserved data-layer module, currently an empty stub (only a docstring-style comment) describing three functions to be built: `get_db()` (SQLite connection with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON` — SQLite has FK enforcement off by default, so this must run on every connection), `init_db()` (creates tables via `CREATE TABLE IF NOT EXISTS`), `seed_db()` (dev sample data). No DB connection is currently wired into `app.py`.
- **`templates/`** — Jinja2 templates. `base.html` is the shared shell (navbar + footer, with `{% block title %}` / `{% block head %}` / `{% block content %}` / `{% block scripts %}`); every page template must `{% extends "base.html" %}`. Internal links always use `url_for('<endpoint>')`, never hardcoded paths — one exception currently in `base.html`'s footer (`href="#"` for a not-yet-built Privacy Policy page).
- **`static/css/style.css`** — single global stylesheet. Design tokens are CSS custom properties on `:root` (colors: `--ink*`, `--paper*`, `--accent*`, `--danger*`, `--border*`; fonts: `--font-display` = DM Serif Display for headings, `--font-body` = DM Sans for body text; radii: `--radius-sm/md/lg`). New UI should reuse these variables rather than introducing new colors/fonts. Reusable page patterns already established: `.hero` (landing), `.auth-section`/`.auth-card` (login/register), `.feature-card`, `.legal-section`/`.legal-card` (terms-style content pages) — all render as white/paper cards with a border and radius on the warm paper background.
- **`static/js/main.js`** — empty stub; vanilla JS only, no frameworks/npm packages.

**Where new things belong:**
- New routes → `app.py` only, no blueprints
- DB logic → `database/db.py` only, never inline in route functions
- New pages → new `.html` file extending `base.html`
- Page-specific styles → a new `.css` file, not inline `<style>` tags

## Tech constraints

- **Flask only** — no FastAPI, no Django, no other web frameworks
- **SQLite only** — no PostgreSQL, no SQLAlchemy ORM, no external DB
- **Vanilla JS only** — no React, no jQuery, no npm packages
- **No new pip packages** without flagging it — keep `requirements.txt` in sync
- Python 3.10+ assumed — f-strings and `match` statements are fine

## Code style

- Python: PEP 8, snake_case for all variables and functions
- DB queries: always parameterized (`?` placeholders) — never f-strings in SQL
- Route functions: one responsibility — fetch data, render template, done
- Error handling: use `abort()` for HTTP errors, not bare `return "error string"`

## Implemented vs stub routes

| Route | Status |
|---|---|
| `GET /` | Implemented — renders `landing.html` |
| `GET /register` | Implemented — renders `register.html` (form not yet wired to POST/DB) |
| `GET /login` | Implemented — renders `login.html` (form not yet wired to POST/DB) |
| `GET /terms` | Implemented — renders `terms.html` |
| `GET /logout` | Stub — Step 3 |
| `GET /profile` | Stub — Step 4 |
| `GET /expenses/add` | Stub — Step 7 |
| `GET /expenses/<id>/edit` | Stub — Step 8 |
| `GET /expenses/<id>/delete` | Stub — Step 9 |

## Warnings and things to avoid

- **Never use a raw string return for a stub route** once it's implemented — always render a template
- **Never hardcode URLs** in templates — always use `url_for()`
- **`database/db.py` is currently empty** — do not assume its helpers exist until the step that implements them
- The app runs on **port 5001**, not Flask's default 5000 — don't change this
