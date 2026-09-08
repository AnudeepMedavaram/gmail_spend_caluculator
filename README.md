# Polaris Gmail Spend Intelligence

A local Gmail spending intelligence pipeline that converts email messages into structured transaction data and spending insights.

The project combines **rule-based classification** with a lightweight **ML baseline using TF-IDF and Logistic Regression**.

---

## Project Overview

The pipeline processes Gmail messages through:

Gmail
  ↓
Ingestion & Normalization
  ↓
Rule-based Classification + ML Signal
  ↓
Transaction Extraction
  ↓
Validation
  ↓
JSONL Storage
  ↓
Aggregation & Analysis
  ↓
Report
  ↓
API + Dashboard 

Machine Learning

The ML component is used as a secondary classification signal rather than replacing the existing rule-based classifier.

Email
  ↓
Rule-based Classifier
  ↓
ML Classifier
(TF-IDF + Logistic Regression)
  ↓
Supporting ML Signal
  ↓
Final Rule-based Decision 

Project Structure
polaris_gmail_spend_intelligence/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── ml_artifacts/
│
├── src/
│   ├── gmail/
│   ├── ingestion/
│   ├── models/
│   ├── processing/
│   ├── ml/
│   ├── analysis/
│   ├── reporting/
│   ├── api/
│   ├── dashboard/
│   └── testing/
│
├── requirements.txt
├── .gitignore
└── README.md 
Setup
python -m venv .venv

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

For Gmail ingestion, configure Google OAuth credentials locally. Private credentials, tokens, raw Gmail data, generated transactions, and ML artifacts are excluded from Git. 
Running
Train ML model
python -m src.ml.train
python -m src.ml.evaluate
Run transaction pipeline
python -m src.processing.run_phase4
Run analysis
python -m src.analysis.run_aggregator
python -m src.analysis.run_analysis
python -m src.reporting.run_report
Run tests
python -m src.testing.run_tests
Start API
python -m src.api.server

API:

http://127.0.0.1:8000
Start Dashboard
python -m src.dashboard.server

Dashboard:

http://127.0.0.1:8501
Technology Stack
Python
scikit-learn
TF-IDF
Logistic Regression
Gmail API
JSONL
REST API
HTML/CSS/JavaScript
Limitations

This is a practical prototype rather than a production-grade financial system.

Email formats vary between merchants.
Transaction extraction does not cover every possible receipt format.
The ML dataset is currently small and synthetic.
Rule-based classification remains the final decision mechanism.
Gmail data is processed locally for privacy.
Future Improvements
Larger labeled dataset
Better transaction extraction
Merchant normalization
Duplicate transaction detection
Improved ML evaluation
Transformer/NLP-based classification
Database-backed storage
Scheduled Gmail ingestion

Author
Anudeep Medavaram




                
