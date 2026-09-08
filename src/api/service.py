from typing import Any

from src.analysis.analysis import build_insights
from src.analysis.aggregator import build_spending_summary
from src.agents.spending_agent import run_spending_agent
from src.processing.storage import load_transactions
from src.reporting.report import generate_report


def build_dashboard() -> dict[str, Any]:
    """Load stored transactions and build all Phase 5-6 outputs."""

    transactions = load_transactions()
    return build_dashboard_from_transactions(transactions)


def build_dashboard_from_transactions(
    transactions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build dashboard output for real or explicitly synthetic transactions."""

    agent_result = run_spending_agent(transactions)
    transactions = agent_result["transactions"]
    summary = build_spending_summary(transactions)
    analysis = build_insights(transactions, summary)
    analysis["recurring_payments"] = agent_result["recurring_payments"]
    analysis["unusual_transactions"] = agent_result["unusual_transactions"]
    analysis["upcoming_payments"] = agent_result["upcoming_payments"]
    analysis["insights"].extend(agent_result["agent_insights"])
    report = generate_report(summary, analysis["insights"])

    return {
        "transactions": transactions,
        "summary": summary,
        "analysis": analysis,
        "agent": {
            "name": "spending_agent",
            "type": "deterministic coordinator",
        },
        "report": report,
    }


def build_demo_dashboard() -> dict[str, Any]:
    """Build an explicitly synthetic dashboard demonstration payload."""

    transactions = [
        {
            "message_id": "demo-netflix-jan",
            "merchant": "Netflix",
            "amount": 15.99,
            "currency": "USD",
            "date": "2026-01-05",
            "transaction_type": "subscription",
        },
        {
            "message_id": "demo-netflix-feb",
            "merchant": "Netflix",
            "amount": 15.99,
            "currency": "USD",
            "date": "2026-02-05",
            "transaction_type": "subscription",
        },
        {
            "message_id": "demo-adobe-jan",
            "merchant": "Adobe",
            "amount": 20.00,
            "currency": "USD",
            "date": "2026-01-12",
            "transaction_type": "subscription",
        },
        {
            "message_id": "demo-adobe-feb",
            "merchant": "Adobe",
            "amount": 600.00,
            "currency": "USD",
            "date": "2026-02-12",
            "transaction_type": "subscription",
        },
        {
            "message_id": "demo-airbnb-feb",
            "merchant": "Airbnb",
            "amount": 350.00,
            "currency": "USD",
            "date": "2026-02-18",
            "transaction_type": "purchase",
        },
        {
            "message_id": "demo-spotify-oct",
            "merchant": "Spotify",
            "amount": 12.99,
            "currency": "USD",
            "date": "2026-10-05",
            "transaction_type": "subscription",
        },
    ]

    result = build_dashboard_from_transactions(transactions)
    result["demo"] = True
    return result


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