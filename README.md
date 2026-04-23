# CRA Payroll Automation Tool

Web-based payroll calculator that automates CRA payroll deductions for Canadian employees. Upload a CSV, get T4-ready Excel reports in seconds.

## Features

- CPP, EI, federal tax, and Ontario provincial tax calculations
- Uses official CRA T4127 formulas (2026 rates)
- Supports monthly, biweekly, and weekly pay periods
- Year-to-date tracking for CPP/EI maximums
- Excel output with Payroll Summary and T4 Preparation sheets
- Employer portions (CPP match + EI 1.4x) and CRA remittance totals

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## CSV Format

Prepare a CSV file with these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Employee Name | Full name | John Smith |
| Gross Pay | This period's gross pay | 5000.00 |
| YTD CPP | Year-to-date CPP deducted | 0.00 |
| YTD EI | Year-to-date EI deducted | 0.00 |
| Pay Periods | Periods per year (12, 26, 52) | 12 |

See `templates/employees.csv` for a sample file.

## Documentation

- [Automation Guide](docs/AUTOMATION_GUIDE.md) — detailed usage instructions
- [Deployment Guide](docs/STREAMLIT_DEPLOYMENT_GUIDE.md) — deploy to Streamlit Cloud (free)
- [Monetization Plan](docs/MONETIZATION_PLAN.md) — business strategy

## Disclaimer

This tool is for estimation purposes. Always verify calculations with a qualified tax professional. Currently supports Ontario provincial taxes only.
