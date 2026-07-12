"""
LedgerPilot — Categorizer (ledger-pilot copy)
"""

import csv
from chart_of_accounts import CHART_OF_ACCOUNTS

CATEGORIZATION_RULES = {
    "PEPCO": "5060",
    "VERIZON": "5060",
    "STRIPE": "4010",
    "ACH": "4010",
    "GUSTO": "5010",
    "RENT": "5020",
    "OFFICE DEPOT": "5050",
    "AMAZON": "5050",
    "UBER": "5070",
    "HOTEL": "5070",
    "AIRBNB": "5070",
    "COFFEE": "5040",
    "RESTAURANT": "5040",
    "STARBUCKS": "5040",
}


def categorize_transaction(description: str, amount: float) -> dict:
    desc_upper = (description or "").upper()
    for keyword, account_code in CATEGORIZATION_RULES.items():
        if keyword in desc_upper:
            return {
                "description": description,
                "amount": amount,
                "account_code": account_code,
                "account_name": CHART_OF_ACCOUNTS[account_code]["name"],
                "confidence": "high",
                "rule_matched": keyword,
            }
    return {
        "description": description,
        "amount": amount,
        "account_code": "5900",
        "account_name": CHART_OF_ACCOUNTS["5900"]["name"],
        "confidence": "low",
        "rule_matched": None,
    }


def categorize_csv(csv_path: str) -> dict:
    categorized = []
    review_queue = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get("description") or row.get("Description") or ""
            amt = float(row.get("amount") or row.get("Amount") or 0)
            result = categorize_transaction(desc, amt)
            if result["confidence"] == "high":
                categorized.append(result)
            else:
                review_queue.append(result)
    return {"categorized": categorized, "review_queue": review_queue}
