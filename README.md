# Polaris Gmail Spend Intelligence

> Turn everyday Gmail receipts and payment emails into a clear picture of where your money goes.

Polaris is a local **AI/ML-powered spending intelligence prototype** that reads Gmail messages, identifies transaction-related emails, extracts spending information, and turns it into useful spending summaries and insights.

The project combines **deterministic rules with Machine Learning** to make transaction detection more reliable while keeping the system explainable.

---

## 💡 What Does Polaris Do?

Instead of manually searching through emails for receipts and payment confirmations, Polaris processes them automatically:

**Gmail → Find transactions → Extract details → Validate → Analyze spending → View insights**

For example:

```text
Amazon payment email
        ↓
Transaction detected
        ↓
Merchant: Amazon
Amount:   $49.99
Date:     2026-08-28
        ↓
Added to spending analysis
        ↓
Shopping spending increases
🤖 AI / ML Component

The project uses a hybrid approach.

Rule-Based Classifier

Identifies transaction emails using signals such as:

Payment-related keywords
Merchant information
Amount patterns
Currency patterns
Transaction-related language
Machine Learning Classifier

A lightweight ML baseline was added using:

TF-IDF for converting email text into numerical features
Logistic Regression for transaction classification

The ML model acts as a secondary signal while the rule-based system remains the final decision maker.

                 Email
                   ↓
          Rule-Based Classifier
                   ↓
          ML Classifier
       TF-IDF + Logistic Regression
                   ↓
            ML Signal
                   ↓
          Final Decision

This design keeps the system interpretable, lightweight, and easy to debug.

ML Baseline Results

Evaluated on a small synthetic dataset:

Metric	Score
Accuracy	75.0%
Precision	66.7%
Recall	100.0%
F1 Score	80.0%

These results are treated as a baseline because the current ML dataset is intentionally small.

🏗️ System Architecture
Gmail
  │
  ▼
Ingestion & Normalization
  │
  ▼
Transaction Classification
  │
  ├── Rule-Based Detection
  └── ML Supporting Signal
  │
  ▼
Transaction Extraction
  │
  ▼
Validation
  │
  ▼
Local JSONL Storage
  │
  ▼
Spending Aggregation
  │
  ▼
Analysis & Insights
  │
  ├── REST API
  └── Dashboard
✨ Key Features
📧 Gmail API integration
🔍 Transaction email detection
🤖 TF-IDF + Logistic Regression ML baseline
🧾 Transaction extraction
✅ Data validation
📊 Spending aggregation and analysis
💡 Automatic spending insights
🌐 Local REST API
📈 Browser-based dashboard
🧪 Automated pipeline testing
🔒 Local processing for private Gmail data
📁 Project Structure
polaris_gmail_spend_intelligence/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── ml_artifacts/
│
├── src/
│   ├── gmail/          # Gmail integration
│   ├── ingestion/      # Email ingestion
│   ├── models/         # Data models
│   ├── processing/     # Classification & extraction
│   ├── ml/             # ML training & evaluation
│   ├── analysis/       # Spending analysis
│   ├── reporting/      # Reports
│   ├── api/            # REST API
│   ├── dashboard/      # Web dashboard
│   └── testing/        # Pipeline tests
│
├── requirements.txt
├── .gitignore
└── README.md
🚀 Getting Started
1. Create a virtual environment
python -m venv .venv

Windows PowerShell:

.\.venv\Scripts\Activate.ps1
2. Install dependencies
pip install -r requirements.txt
3. Train and evaluate the ML baseline
python -m src.ml.train
python -m src.ml.evaluate
4. Run the spending pipeline
python -m src.processing.run_phase4
python -m src.analysis.run_aggregator
python -m src.analysis.run_analysis
python -m src.reporting.run_report
5. Run tests
python -m src.testing.run_tests
6. Start the API
python -m src.api.server

API:

http://127.0.0.1:8000

7. Start the dashboard
python -m src.dashboard.server

Dashboard:

http://127.0.0.1:8501

🛠️ Tech Stack

Python · Gmail API · scikit-learn · TF-IDF · Logistic Regression · JSONL · REST API · HTML/CSS/JavaScript

🔐 Privacy

Gmail data is processed locally.

Private credentials, tokens, raw Gmail data, generated transaction data, and ML artifacts are excluded from the Git repository.

⚠️ Current Limitations

This is a prototype, not a production financial application.

Email formats differ between merchants.
Transaction extraction does not support every receipt format.
The current ML dataset is small and synthetic.
The rule-based classifier remains the final decision mechanism.
🔮 Future Improvements
Larger real-world labeled dataset
Better merchant normalization
Duplicate transaction detection
Improved transaction extraction
Stronger ML evaluation
Transformer/NLP-based classification
Database-backed storage
Scheduled Gmail processing
👨‍💻 Author

Anudeep Medavaram














                
