"""
LedgerPilot — Ledger Core
The double-entry engine. Every transaction becomes a journal entry with
equal debits and credits, posted to accounts from the chart.
Stored in SQLite so the books persist.
"""

import sqlite3
from datetime import date
from chart_of_accounts import get_account


class Ledger:
    def __init__(self, db_path: str = "ledgerpilot.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT NOT NULL,
                description TEXT NOT NULL,
                source TEXT DEFAULT 'manual'
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS entry_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id INTEGER NOT NULL REFERENCES journal_entries(id),
                account_code TEXT NOT NULL,
                debit REAL DEFAULT 0,
                credit REAL DEFAULT 0
            )
        """)
        self.conn.commit()

    def post_entry(self, entry_date: str, description: str, lines: list, source: str = "manual") -> int:
        """
        Post a journal entry. `lines` is a list of dicts:
            [{"account": "5020", "debit": 2400.00},
             {"account": "1010", "credit": 2400.00}]

        Enforces the one unbreakable rule: total debits == total credits.
        Returns the entry id.
        """
        total_debits = round(sum(l.get("debit", 0) for l in lines), 2)
        total_credits = round(sum(l.get("credit", 0) for l in lines), 2)

        if total_debits != total_credits:
            raise ValueError(
                f"Entry doesn't balance: debits {total_debits} != credits {total_credits}. "
                "Every entry must have equal debits and credits — that's double-entry."
            )
        if total_debits == 0:
            raise ValueError("Entry has no amounts.")

        # Validate every account exists in the chart before posting anything
        for line in lines:
            get_account(line["account"])

        cur = self.conn.execute(
            "INSERT INTO journal_entries (entry_date, description, source) VALUES (?, ?, ?)",
            (entry_date, description, source),
        )
        entry_id = cur.lastrowid
        for line in lines:
            self.conn.execute(
                "INSERT INTO entry_lines (entry_id, account_code, debit, credit) VALUES (?, ?, ?, ?)",
                (entry_id, line["account"], line.get("debit", 0), line.get("credit", 0)),
            )
        self.conn.commit()
        return entry_id

    def account_balance(self, account_code: str) -> float:
        """
        Balance of one account. Sign convention follows the account's normal side:
        assets/expenses grow with debits; liabilities/equity/income grow with credits.
        """
        acct = get_account(account_code)
        row = self.conn.execute(
            "SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM entry_lines WHERE account_code = ?",
            (account_code,),
        ).fetchone()
        debits, credits = row
        if acct["normal_side"] == "debit":
            return round(debits - credits, 2)
        return round(credits - debits, 2)

    def trial_balance(self) -> dict:
        """
        Every account with activity and its balance, plus the global check:
        total debits must equal total credits across the whole ledger.
        """
        rows = self.conn.execute(
            """SELECT account_code, COALESCE(SUM(debit),0), COALESCE(SUM(credit),0)
               FROM entry_lines GROUP BY account_code"""
        ).fetchall()
        accounts = {}
        total_debits = total_credits = 0.0
        for code, debits, credits in rows:
            acct = get_account(code)
            balance = round(debits - credits, 2) if acct["normal_side"] == "debit" else round(credits - debits, 2)
            accounts[code] = {"name": acct["name"], "type": acct["type"], "balance": balance}
            total_debits += debits
            total_credits += credits
        return {
            "accounts": accounts,
            "total_debits": round(total_debits, 2),
            "total_credits": round(total_credits, 2),
            "balanced": round(total_debits, 2) == round(total_credits, 2),
        }

    def close(self):
        self.conn.close()
