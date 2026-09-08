# Polaris Gmail Spend Intelligence

A local Gmail spending intelligence pipeline that identifies transaction-related emails, extracts spending information, validates transactions, and generates spending insights through an API and dashboard.

The project combines a **rule-based transaction classifier** with a lightweight **machine-learning baseline using TF-IDF and Logistic Regression**.

---

## Project Overview

The goal of this project is to build an end-to-end pipeline that can turn unstructured Gmail messages into structured spending information.

The system performs:

1. Gmail message ingestion
2. Email normalization
3. Transaction classification
4. Transaction information extraction
5. Transaction validation
6. Local JSONL storage
7. Spending aggregation
8. Spending analysis
9. API exposure
10. Dashboard visualization
11. Automated smoke testing

The ML component is intentionally lightweight and is used as a **secondary classification signal** rather than replacing the deterministic rule-based system.

---

## Architecture

```text
                         Gmail
                           │
                           ▼
                    Email Ingestion
                           │
                           ▼
                     Normalization
                           │
                           ▼
              ┌────────────────────────┐
              │ Transaction Classifier │
              │                        │
              │ Rule-based + ML signal │
              └────────────┬───────────┘
                           │
                           ▼
                    Transaction
                     Extraction
                           │
                           ▼
                      Validation
                           │
                           ▼
                    JSONL Storage
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
        Aggregation                  Analysis
             │                           │
             └─────────────┬─────────────┘
                           ▼
                        Report
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
                API              Dashboard 




                
