# LedgerPilot

An automated bookkeeping engine: raw bank CSVs in, categorized double-entry books,
reconciliation, and a monthly close report out.

## Status: completed

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
