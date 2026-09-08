# Polaris Gmail Spend Intelligence

> Turning a noisy inbox into a clear picture of where money goes.

Polaris is a local-first spending intelligence product built around a simple belief: financial data is already hiding in the inbox, but it is difficult to search, structure, and understand.

The system discovers spending-related Gmail messages, extracts transaction details, validates them, summarizes spending, and presents the result through a local API and dashboard.

This repository is the focused baseline: explainable rules first, a small ML experiment second, and a complete path from email to insight.

## Why Polaris

Most inboxes contain receipts, invoices, payment confirmations, subscription notices, newsletters, and financial articles side by side. Keyword search can find some of them, but it cannot reliably distinguish a real charge from an article discussing prices.

Polaris creates a structured transaction layer from that noise:

- **Discover** relevant Gmail messages.
- **Classify** transaction candidates with transparent rules.
- **Extract** merchant, amount, currency, date, and transaction type.
- **Validate** the extracted record before storage.
- **Analyze** spending by category, merchant, and month.
- **Highlight** recurring payments, unusual amounts, and first-time merchants.
- **Expose** the result through a local API and dashboard.

## Architecture and Technical Decisions

```text
Gmail
      -> Email discovery
      -> Normalization
      -> Rule-based classification
      -> Optional ML supporting signal
      -> Transaction extraction
      -> Validation
      -> JSONL storage
      -> Aggregation and insights
      -> Local API and dashboard
```

The rule-based classifier remains the primary decision-maker because it is easy to inspect and debug. JSONL storage keeps the prototype simple and local, while the API and dashboard are implemented with Python's standard library to minimize dependencies. The ML package is an isolated TF-IDF + Logistic Regression baseline trained only on synthetic examples. It provides supporting evidence; it does not replace the deterministic pipeline.

The project also includes a lightweight deterministic spending agent. It coordinates category assignment, recurring-payment detection, unusual-payment explanations, and Gmail traceability links. It is not an LLM and does not call an external AI service.

## Repository Layout

```text
src/
├── gmail/       Gmail authentication and API access
├── ingestion/   Discovery, normalization, and dataset checks
├── models/      Email model and Gmail payload parser
├── processing/  Classification, extraction, validation, and storage
├── analysis/    Spending aggregation and insights
├── reporting/   Human-readable reports
├── api/         Local HTTP API
├── dashboard/   Local browser dashboard
├── ml/          Synthetic-data ML baseline
└── testing/     Regression tests
```

## How to Run Locally

Requires Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

For Gmail ingestion, add a Google OAuth client file named `credentials.json` to the project root, then authenticate once:

```powershell
python gmail_auth.py
```

The generated `token.json`, credentials, raw Gmail data, processed data, and ML artifacts are excluded from Git.

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

The dashboard also shows recurring payments, transactions worth attention, and links back to the source Gmail message when a message ID is available.

## AI and Agent Components

The project does not use an LLM or external generative-AI API. It uses two lightweight, explainable components:

1. **ML baseline:** TF-IDF plus Logistic Regression classifies synthetic email text as `transaction` or `non_transaction`. It was chosen as a transparent, low-cost baseline and is used only as supporting evidence for the rule-based classifier.
2. **Deterministic spending agent:** `src/agents/spending_agent.py` coordinates category assignment, recurring-payment detection, unusual-payment explanations, and Gmail traceability links. It was chosen to keep financial decisions inspectable and private; it does not call an external AI service.

The optional ML baseline follows this flow:

```text
Synthetic subject + body
      -> TF-IDF features
      -> Logistic Regression
      -> transaction probability and class
```

Train it:

```powershell
python -m src.ml.train
```

Evaluate it on a held-out synthetic split:

```powershell
python -m src.ml.evaluate
```

The ML model supports the deterministic classifier; it does not replace it or claim superiority.

## Testing

```powershell
python -m src.testing.run_tests
python -m compileall -q src
```

## Data and Privacy

Polaris is local-first. Gmail credentials, OAuth tokens, raw email content, processed transactions, and generated ML artifacts should not be committed to a public repository.

Ignored private/generated paths include:

```text
credentials.json
token.json
data/raw/
data/processed/
data/ml_artifacts/
.venv/
__pycache__/
```

## Current Scope

This is an explainable prototype rather than a production finance platform. It does not include cloud deployment, a database, authentication, an LLM, or an external AI API. Email formats vary, so extraction will not support every provider or template.

The current Gmail sample may contain zero transaction candidates. The analysis and reporting runners include sample transactions for smoke testing when no processed transactions are available.

## Project Status

The core pipeline, local API, dashboard, ML baseline, and regression tests are implemented. The next product milestone would be improving coverage with a larger, privacy-safe labeled dataset and measuring performance against a meaningful validation set.