# Development Standards

## Project Overview

CRA Payroll Deductions Calculator — a Streamlit web app for Canadian accountants to calculate payroll deductions (CPP, EI, federal/provincial tax) and generate T4-ready Excel reports. All 13 provinces/territories supported.

- **Live:** https://accounting-3pns7vsk95pikojyhccgv4.streamlit.app/
- **Auth:** Google OAuth via Supabase
- **CI:** GitHub Actions runs unit tests on every push to main

## Architecture

```
app.py              — Streamlit UI (auth, forms, display)
payroll.py          — Calculation engine (CPP, EI, tax, Excel output)
provinces.py        — Provincial tax configs (brackets, BPA, surtax, health premiums)
```

Business logic lives in `payroll.py` and `provinces.py` — never in `app.py`. The UI layer (`app.py`) imports from the logic layer, not the other way around. This separation allows unit tests to run without Streamlit.

## Development Rules

### Before writing code
- Read the files you're changing. Don't guess at structure.
- Check if an existing function or pattern handles what you need.
- For any new feature: write the plan, get approval, then implement.

### Code changes
- Make minimal, targeted changes. Don't refactor or "improve" code you weren't asked to touch.
- Keep UI simple and trustworthy — no flashy colors, minimal emoji, clean layouts.
- Don't add dependencies unless absolutely necessary. Prefer standard library solutions.
- All CRA rates, brackets, and formulas go in `provinces.py` or `payroll.py`, never hardcoded in `app.py`.

### Testing
- Every new feature must include tests before it's considered done.
- Unit tests go in `test_payroll.py` — test calculation logic, Excel output, province configs.
- E2E browser tests go in `test_e2e.py` — test UI flows via Playwright.
- Production smoke tests go in `test_production.py` — test the live deployment.
- Run `python -m pytest test_payroll.py test_e2e.py` before committing.
- CI runs `test_payroll.py` automatically on push.

### Testing with Playwright
- Use Playwright to verify UI changes instead of asking the user to check manually.
- Take screenshots (`page.screenshot()`) to visually verify renders.
- E2E tests must clear `.session.json` in the fixture to ensure logged-out state.

### Git workflow
- Commit after each logical change, not in large batches.
- Commit messages: short first line describing what changed and why.
- Push to main — auto-deploys to Streamlit Cloud.
- Run tests before pushing.

### Credentials and secrets
- Never commit secrets, API keys, or tokens.
- Local secrets: `.streamlit/secrets.toml` and `.env` (both gitignored).
- Streamlit Cloud secrets: set in the app dashboard.
- Session data: `.session.json` (gitignored).

## Running locally

```bash
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.headless true
```

## Running tests

```bash
# Unit tests (fast, no server needed)
python -m pytest test_payroll.py -v

# E2E tests (needs Streamlit running on port 8501)
python -m pytest test_e2e.py -v

# All tests
python -m pytest test_payroll.py test_e2e.py -v

# Production smoke tests (hits live deployment)
python -m pytest test_production.py -v
```

## Key decisions

- **Streamlit** chosen for fast prototyping and free hosting. May migrate to FastAPI + proper frontend when charging users.
- **Supabase** for auth (Google OAuth). Free tier. Session persisted via server-side `.session.json` file — works for single-user local dev. Will need database-backed sessions for multi-user production.
- **No ORM or database tables yet** for app data (clients, employees, payroll history). Auth only. Database schema will be added when persistence features are built.
- **Provincial tax rates** are 2025 values. Will need updating when CRA publishes 2026 rates.
