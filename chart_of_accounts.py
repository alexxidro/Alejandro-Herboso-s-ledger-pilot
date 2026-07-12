"""
LedgerPilot — Chart of Accounts
The master list of every account transactions can be filed into.
Account types determine debit/credit behavior and statement placement.
"""

# Account types and their normal balance side.
# Debits INCREASE: assets, expenses. Credits INCREASE: liabilities, equity, income.
ACCOUNT_TYPES = {
    "asset":     {"normal_side": "debit",  "statement": "balance_sheet"},
    "liability": {"normal_side": "credit", "statement": "balance_sheet"},
    "equity":    {"normal_side": "credit", "statement": "balance_sheet"},
    "income":    {"normal_side": "credit", "statement": "income_statement"},
    "expense":   {"normal_side": "debit",  "statement": "income_statement"},
}

# The chart itself. Numbering convention: 1xxx assets, 2xxx liabilities,
# 3xxx equity, 4xxx income, 5xxx expenses.
CHART_OF_ACCOUNTS = {
    # ---- ASSETS ----
    "1010": {"name": "Checking Account",        "type": "asset"},
    "1020": {"name": "Savings Account",         "type": "asset"},
    "1050": {"name": "Undeposited Funds",       "type": "asset"},
    "1200": {"name": "Accounts Receivable",     "type": "asset"},
    "1500": {"name": "Equipment",               "type": "asset"},

    # ---- LIABILITIES ----
    "2010": {"name": "Accounts Payable",        "type": "liability"},
    "2100": {"name": "Credit Card Payable",     "type": "liability"},
    "2500": {"name": "Loan Payable",            "type": "liability"},

    # ---- EQUITY ----
    "3010": {"name": "Owner's Equity",          "type": "equity"},
    "3020": {"name": "Owner's Draw",            "type": "equity"},
    "3900": {"name": "Retained Earnings",       "type": "equity"},

    # ---- INCOME ----
    "4010": {"name": "Service Revenue",         "type": "income"},
    "4020": {"name": "Product Sales",           "type": "income"},

    # ---- EXPENSES ----
    "5010": {"name": "Payroll Expense",         "type": "expense"},
    "5020": {"name": "Rent",                    "type": "expense"},
    "5030": {"name": "Software & Subscriptions","type": "expense"},
    "5040": {"name": "Meals & Entertainment",   "type": "expense"},
    "5050": {"name": "Office Supplies",         "type": "expense"},
    "5060": {"name": "Utilities",               "type": "expense"},
    "5070": {"name": "Travel",                  "type": "expense"},
    "5080": {"name": "Insurance",               "type": "expense"},
    "5090": {"name": "Professional Services",   "type": "expense"},
    "5100": {"name": "Bank Fees",               "type": "expense"},
    "5110": {"name": "Interest Expense",        "type": "expense"},
    "5900": {"name": "Uncategorized / Ask Client", "type": "expense"},
}


def get_account(code: str) -> dict:
    """Look up an account by code. Raises if it doesn't exist —
    you can't post to an account that isn't in the chart."""
    if code not in CHART_OF_ACCOUNTS:
        raise ValueError(f"Account {code} not in chart of accounts")
    acct = CHART_OF_ACCOUNTS[code]
    return {"code": code, **acct, **ACCOUNT_TYPES[acct["type"]]}


def accounts_by_type(acct_type: str) -> list:
    """All accounts of a given type — used by the statement generator."""
    return [
        {"code": code, **info}
        for code, info in CHART_OF_ACCOUNTS.items()
        if info["type"] == acct_type
    ]
