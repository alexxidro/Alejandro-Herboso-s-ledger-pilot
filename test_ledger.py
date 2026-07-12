

"""
LedgerPilot — Day 1 test.
Posts the transactions you know cold and verifies the books balance.
Run:  python test_ledger.py
"""

import os
from ledger import Ledger

DB = "test_books.db"
if os.path.exists(DB):
    os.remove(DB)  # fresh books each test run

ledger = Ledger(DB)

# 1. Pay rent — Debit Rent (destination), Credit Checking (source)
ledger.post_entry("2026-06-05", "Rent — WeWork", [
    {"account": "5020", "debit": 2400.00},
    {"account": "1010", "credit": 2400.00},
])

# 2. Stripe revenue lands — Debit Checking, Credit Revenue
ledger.post_entry("2026-06-03", "Stripe deposit", [
    {"account": "1010", "debit": 8420.50},
    {"account": "4010", "credit": 8420.50},
])

# 3. Buy MacBook — asset-for-asset trade, no expense
ledger.post_entry("2026-06-23", "Apple — MacBook", [
    {"account": "1500", "debit": 1899.00},
    {"account": "1010", "credit": 1899.00},
])

# 4. Loan payment with principal/interest split — a 3-line entry
ledger.post_entry("2026-06-28", "Loan payment", [
    {"account": "2500", "debit": 420.00},
    {"account": "5110", "debit": 80.00},
    {"account": "1010", "credit": 500.00},
])

# 5. Prove the engine REJECTS an unbalanced entry
try:
    ledger.post_entry("2026-06-30", "Bad entry", [
        {"account": "5020", "debit": 100.00},
        {"account": "1010", "credit": 90.00},
    ])
    print("FAIL: unbalanced entry was accepted!")
except ValueError as e:
    print(f"✓ Unbalanced entry correctly rejected: {e}\n")

# Trial balance — the moment of truth
tb = ledger.trial_balance()
print("TRIAL BALANCE")
print("-" * 55)
for code, info in sorted(tb["accounts"].items()):
    print(f"{code}  {info['name']:<28} {info['balance']:>12,.2f}")
print("-" * 55)
print(f"Total debits:  {tb['total_debits']:>12,.2f}")
print(f"Total credits: {tb['total_credits']:>12,.2f}")
print(f"BALANCED: {tb['balanced']}")

# Sanity checks
assert tb["balanced"], "Books don't balance!"
assert ledger.account_balance("1010") == 8420.50 - 2400.00 - 1899.00 - 500.00
assert ledger.account_balance("2500") == -420.00  # loan reduced by principal
print("\n✓ All checks passed. The ledger core works.")
ledger.close()

