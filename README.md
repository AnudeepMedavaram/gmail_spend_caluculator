# Polaris Gmail Spend Intelligence

A local email-processing pipeline that identifies potential spending-related Gmail messages, extracts transaction information, validates transactions, aggregates spending, generates insights, and presents results through a local API and dashboard.

The project uses a deterministic rule-based classifier as the primary system and includes a lightweight TF-IDF + Logistic Regression baseline as a secondary ML signal.

## Architecture

```text
Gmail API
   |
   v
Email Discovery
   |
   v
Email Normalization
   |
   v
Rule-Based Classification
   |
   v
Optional ML Classification Signal
   |
   v
Transaction Extraction
   |
   v
Transaction Validation
   |
   v
JSONL Transaction Storage
   |
   v
Spending Aggregation
   |
   v
Spending Analysis
   |
   +------------------+
   |                  |
   v                  v
Local REST API     Dashboard 

Features
Gmail message discovery
Gmail email normalization
Rule-based transaction classification
Optional TF-IDF and Logistic Regression classification signal
Transaction amount and merchant extraction
Transaction validation
JSONL-based storage
Spending aggregation by:
Category
Merchant
Month
Spending insights and reports
Local HTTP API
Local browser dashboard
Phase 9 regression tests
Synthetic-data ML evaluation

Project Structure
polaris_gmail_spend_intelligence/
├── data/
│   ├── raw/
│   │   └── emails.jsonl
│   └── processed/
│       └── transactions.jsonl
├── src/
│   ├── gmail/
│   ├── ingestion/
│   ├── models/
│   ├── processing/
│   ├── analysis/
│   ├── reporting/
│   ├── api/
│   ├── dashboard/
│   ├── ml/
│   └── testing/
├── credentials.json
├── token.json
├── gmail_auth.py
├── requirements.txt
└── README.md

Requirements
Python 3.10 or newer
Gmail API credentials for Gmail ingestion
Internet access during dependency installation

Installation
Create and activate a virtual environment:
python -m venv .venv
Activate.ps1
Install dependencies:
pip install -r requirements.txt
Dependencies include:
google-api-python-client
google-auth
google-auth-oauthlib
scikit-learn
Gmail Setup
Create a Gmail OAuth client in Google Cloud and download the credentials file.

Place it in the project root as:
credentials.json
Run authentication:
python gmail_auth.py
This creates:
token.json 

The credential and token files are private and are excluded from Git.

Running the Pipeline

Validate Raw Email Data
python -m src.ingestion.validate

Discover and Normalize Gmail Emails
python -m src.ingestion.discover

This stores normalized email data in:
emails.jsonl

Run Phase 4 Transaction Processing
python -m src.processing.run_phase4

The Phase 4 pipeline performs:

Email loading
Rule-based classification
Transaction extraction
Transaction validation
Transaction storage
Validated transactions are stored in:
The Phase 4 pipeline performs:

Email loading
Rule-based classification
Transaction extraction
Transaction validation
Transaction storage
Validated transactions are stored in:
Run Individual Processing Commands
python -m src.processing.run_classifier
python -m src.processing.run_extractor
python -m src.processing.run_validator
python -m src.processing.run_storage

Run Spending Aggregation
python -m src.analysis.run_aggregator

Run Spending Analysis
python -m src.analysis.run_analysis

Generate a Spending Report
python -m src.analysis.run_analysis

Machine Learning Baseline
The project includes a small ML baseline using:
TF-IDF Vectorizer
Logistic Regression

The ML pipeline is:
Email subject + body
    -> TF-IDF features
    -> Logistic Regression
    -> transaction/non_transaction prediction

The ML model is used as a secondary signal. The existing rule-based classifier remains the primary and final decision-maker.

The ML model is trained only on synthetic examples. Private Gmail data is never used for ML training or evaluation.

Train the ML Baseline
python -m src.ml.train
This creates a local model artifact at:
transaction_classifier.pkl

The artifact directory is ignored by Git.

Evaluate the ML Baseline
python -m src.ml.evaluate

The evaluation reports:

Accuracy
Precision
Recall
F1 score
Confusion matrix
The ML evaluation is a prototype baseline and is not claimed to outperform the rule-based classifier.

API
Start the API server:
python -m src.api.server

The API runs at:
http://127.0.0.1:8000

Available endpoints:
GET /health
GET /transactions
GET /summary
GET /insights
GET /report
GET /dashboard

Example PowerShell requests:
Invoke-RestMethod http://127.0.0.1:8000/health | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/summary | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/dashboard | ConvertTo-Json

Dashboard
Start the dashboard in a second terminal:
python -m src.dashboard.server

Open the dashboard in a browser:
http://127.0.0.1:8501

The dashboard displays:

Total spending
Transaction count
Average transaction
Category breakdown
Merchant breakdown
Monthly spending
Spending insights
Stored transactions
API connection status

Testing
Run the Phase 9 test suite:
python -m src.testing.run_tests

The tests cover:

Classification
Extraction
Validation
Storage
Aggregation
Analysis
Compile the complete source tree:
python -m compileall -q src
Compile only the ML package:
python -m compileall -q src/ml

Security and Privacy
The following files and directories are intentionally excluded from Git:
credentials.json
token.json
.env
.venv/
__pycache__/
*.pyc
data/raw/
data/processed/
data/ml_artifacts/

Raw Gmail data may contain private email content and should not be committed to a public repository

Current Limitations
The classifier is rule-based and designed as a practical baseline.
Email formats vary, so extraction will not support every provider or template.
The ML model is trained and evaluated only on a small synthetic dataset.
The API and dashboard are intended for local development.
There is no database, authentication layer, or cloud deployment.
The current Gmail dataset may contain zero transaction candidates.
Phase 5 and Phase 6 runners use sample transactions for smoke testing when no stored transactions are available.

Typical Demo Flow
Open two or three PowerShell terminals.

Terminal 1:
python -m src.processing.run_phase4

Terminal 2:
python -m src.api.server

Terminal 3:
python -m src.dashboard.server

Then open:
http://127.0.0.1:8501

Run the tests separately:
http://127.0.0.1:8501















                
