# LedgerPilot

An automated bookkeeping engine: raw bank CSVs in, categorized double-entry books,
reconciliation, and a monthly close report out.

## Status: Week 1 — Ledger Core ✅

- [x] Chart of accounts (typed accounts, debit/credit behavior)
- [x] Double-entry ledger with balance enforcement (SQLite)
- [x] Trial balance with global debit=credit check
- [ ] Week 2: CSV ingestion + rules-based categorization
- [ ] Week 2: AI categorization layer (Anthropic API) with review queue
- [ ] Week 3: Bank reconciliation module
- [ ] Week 4: P&L / Balance Sheet generation + close report
- [ ] Week 4: Streamlit interface

## Run the test

```bash
python test_ledger.py
```

Posts sample transactions (rent, revenue, an asset purchase, a split loan payment),
proves unbalanced entries are rejected, and prints a balanced trial balance.

## Design principles

1. **Every entry balances.** Debits = credits, enforced at post time. Non-negotiable.
2. **No posting to unknown accounts.** The chart of accounts is the source of truth.
3. **Uncertain transactions go to a review queue** (account 5900), never guessed.
