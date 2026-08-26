# finance-analytics-dashboard

A web application that helps users understand their personal finances through an interactive transaction table and summary visualizations (spending by category, income vs. expenses, and budget tracking).

## Tech stack
- Frontend: HTML, CSS, Bootstrap, DataTables.js, Chart.js
- Backend: Python, Flask
- Database: SQLite

## Scope
Core Minimum Viable Product (MVP)
- Transaction table with sorting, search, filtering and pagination
- Manual entry form and CSV import
- Spending by category, income vs. expenses charts
- Overall monthly budget and per-category budgets

Planned, not part of the MVP
- Spending trends over time
- Account comparison and net worth chart

## Data model
Tables: accounts, categories, transactions, budgets

Conventions:
- All monetary values are stored as integer cents.
- transactions.amount_cents: negative = expense, positive = income.
- Account balances are not stored. They are derived as opening_balance_cents + SUM(transactions.amount_cents).
- budgets.category_id is nullable. NULL denotes the overall monthly budget and a value denotes a per-category budget.
- budgets.month uses the format YYYY-MM and is unique per (month, category_id).
- categories.kind: income or expense.
- accounts.type: checking, savings, cash or credit.

```
## API routes
GET, POST  /api/transactions                        Lists or creates transactions.
POST       /api/transactions/import                 CSV upload, creates multiple transactions.
GET        /api/categories                          All categories with id, name and kind.
GET        /api/accounts                            All accounts with derived current balance.
GET, PUT   /api/budgets?month=YYYY-MM               Reads or sets budgets for the given month.
GET        /api/summary/by-category?month=YYYY-MM   Spending and income totals per category.
GET        /api/summary/monthly                     Income vs. expenses per month.
GET        /api/summary/net-worth                   Balance per account (optional feature).
```

All amounts are returned as integer cents.

## CSV import format
Expected columns: date, description, amount, category, account
- date: YYYY-MM-DD
- amount: decimal with a point, negative for expenses, for example: -10.49
- category and account: must match existing entries by name

## Setup
to be completed
