# Polaris Gmail Spend Intelligence

A local, rule-based pipeline that discovers Gmail messages, identifies potential spending emails, extracts and validates transactions, aggregates spending, and exposes the results through a local API and dashboard.

## Pipeline

```text
Gmail -> normalization -> classification -> extraction -> validation
      -> JSONL storage -> aggregation -> analysis -> report/API/dashboard
```

The current implementation is a practical baseline. It does not guarantee support for every email format.

## Setup

Use Python 3.10+ and create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

For Gmail ingestion, place a Google OAuth client file at `credentials.json`. Run `python gmail_auth.py` once to create the local `token.json`. These files are private and ignored by Git.

Raw Gmail data is stored in `data/raw/` and generated transactions are stored in `data/processed/`. Both directories are ignored by Git.

## Commands

Validate the raw dataset:

```powershell
python -m src.ingestion.validate
```

Run ingestion after Gmail authentication:

```powershell
python -m src.ingestion.discover
```

Run the Phase 4 transaction pipeline:

```powershell
python -m src.processing.run_phase4
```

Run individual processing checks:

```powershell
python -m src.processing.run_classifier
python -m src.processing.run_extractor
python -m src.processing.run_validator
python -m src.processing.run_storage
```

Run aggregation, analysis, and reporting:

```powershell
python -m src.analysis.run_aggregator
python -m src.analysis.run_analysis
python -m src.reporting.run_report
```

Run tests:

```powershell
python -m src.testing.run_tests
```

## API and Dashboard

Start the API:

```powershell
python -m src.api.server
```

The API runs at `http://127.0.0.1:8000` and provides `/health`, `/transactions`, `/summary`, `/insights`, `/report`, and `/dashboard`.

In another terminal, start the dashboard:

```powershell
python -m src.dashboard.server
```

Open `http://127.0.0.1:8501` in a browser.

## Current Data Limitation

The checked-out Gmail sample currently contains no transaction candidates, so reports and the dashboard may show zero stored transactions. The Phase 5 and Phase 6 runners include sample data for smoke testing.