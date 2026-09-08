from typing import Any

from src.analysis.analysis import build_insights
from src.analysis.aggregator import build_spending_summary
from src.processing.storage import load_transactions
from src.reporting.report import generate_report


def build_dashboard() -> dict[str, Any]:
    """Load stored transactions and build all Phase 5-6 outputs."""

    transactions = load_transactions()
    summary = build_spending_summary(transactions)
    analysis = build_insights(transactions, summary)
    report = generate_report(summary, analysis["insights"])

    return {
        "transactions": transactions,
        "summary": summary,
        "analysis": analysis,
        "report": report,
    }


def get_health() -> dict[str, Any]:
    """Return a lightweight API and pipeline health response."""

    transactions = load_transactions()

    return {
        "status": "ok",
        "phase": 7,
        "transaction_count": len(transactions),
    }


def get_transactions() -> list[dict[str, Any]]:
    """Return stored validated transactions."""

    return load_transactions()


def get_summary() -> dict[str, Any]:
    """Return the Phase 5 spending summary."""

    return build_dashboard()["summary"]


def get_insights() -> dict[str, Any]:
    """Return the Phase 5 spending analysis and insights."""

    return build_dashboard()["analysis"]


def get_report() -> dict[str, str]:
    """Return the Phase 6 human-readable report."""

    return {"report": build_dashboard()["report"]}