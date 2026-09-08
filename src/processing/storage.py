import json
from pathlib import Path
from typing import List


TRANSACTIONS_FILE = Path(
    "data/processed/transactions.jsonl"
)


def ensure_output_directory() -> None:
    """
    Create the processed-data directory if it does not exist.
    """

    TRANSACTIONS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


def save_transactions(
    transactions: List[dict],
) -> None:
    """
    Save validated transactions as JSONL.

    Each transaction is stored as one JSON object per line.
    """

    ensure_output_directory()

    with TRANSACTIONS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        for transaction in transactions:

            file.write(
                json.dumps(
                    transaction,
                    ensure_ascii=False,
                )
                + "\n"
            )


def load_transactions() -> List[dict]:
    """
    Load stored transactions from JSONL.
    """

    if not TRANSACTIONS_FILE.exists():
        return []

    transactions = []

    with TRANSACTIONS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            transactions.append(
                json.loads(line)
            )

    return transactions


if __name__ == "__main__":
    print(
        "storage.py provides transaction storage functions."
    )