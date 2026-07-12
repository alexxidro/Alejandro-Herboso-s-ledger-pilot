"""
LedgerPilot — Reconciliation (ledger-pilot copy)
Provides `reconcile` used by the Streamlit app.
"""

def reconcile(bank_transactions: list, ledger_entries: list) -> dict:
    matched = []
    unmatched_bank = list(bank_transactions)
    unmatched_ledger = list(ledger_entries)
    duplicates = []
    transpositions = []

    def parse_date(date_str: str):
        from datetime import datetime
        return datetime.strptime(date_str, "%Y-%m-%d")

    for bank_line in list(unmatched_bank):
        for ledger_line in list(unmatched_ledger):
            if (bank_line.get("amount") == ledger_line.get("amount") and
                abs((parse_date(bank_line.get("date")) - parse_date(ledger_line.get("date"))).days) <= 3):
                matched.append({"bank": bank_line, "ledger": ledger_line, "status": "matched"})
                unmatched_bank.remove(bank_line)
                unmatched_ledger.remove(ledger_line)
                break

            diff = abs(bank_line.get("amount") - ledger_line.get("amount"))
            if diff > 0 and diff % 9 == 0 and abs((parse_date(bank_line.get("date")) - parse_date(ledger_line.get("date"))).days) <= 3:
                transpositions.append({"bank": bank_line, "ledger": ledger_line, "difference": diff, "status": "possible_transposition"})
                unmatched_bank.remove(bank_line)
                unmatched_ledger.remove(ledger_line)
                break

    seen_amounts = {}
    for entry in unmatched_ledger:
        key = (entry.get("amount"), entry.get("date"))
        if key in seen_amounts:
            duplicates.append({"entry": entry, "status": "duplicate_in_ledger"})
        seen_amounts[key] = entry

    return {
        "matched": matched,
        "unmatched_bank": unmatched_bank,
        "unmatched_ledger": unmatched_ledger,
        "duplicates": duplicates,
        "transpositions": transpositions,
    }
