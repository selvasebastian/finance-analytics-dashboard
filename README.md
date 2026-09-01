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
- Spending trends over time

Optional (if time is available)
- Comparison of income and expenses accross different accounts (Update: dropped, not implemented)
- Net worth chart

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
1. Clone the repository:
```
git clone https://github.com/selvasebastian/finance-analytics-dashboard
cd finance-analytics-dashboard
```

2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install flask
```

4. Set up the database:
```
sqlite3 finance.db < schema.sql
python3 seed.py
```

5. Start the server:
```
python3 app.py
```

6. Open the app in a browser:
```
http://127.0.0.1:5000
```

## Dependencies

Backend
- Flask 3.1.3

Frontend
- Bootstrap 5.3.0
- jQuery 3.7.0
- DataTables.js 1.13.6
- Chart.js

Built-in (no installation needed):
- SQLite

## Manual/ Important Notes
- The system will come with predefined data. By pressing "Reset all transactions" on the transactions page. These predefined transactions will be deleted, the charts reset and the user can start entering their data. However, the start values for the accounts will not be reset. If wished this values can become zero by entering two expenses that will make the account balance of each of the accounts to zero.
- All five fields on the Transactions page for adding new data must obtain inputs.
- When adding an expense at the Transactions page it is necessary to add a minus before the number, otherwise the system will interpret it wrongly and the charts will be erroneous.
- In order to make additional categories appear in the "Budget per Category" Chart, it is necessary to set a budget on the Charts page for the corresponding category.
- If a transaction leads to a negative balance (spending more than is available), the charts may not display this account correctly. However, this was a deliberate decision since it is possible to overdraw in account and also a normal process for some means of payment (e.g. credit cards) or short types of loans that may be added as additional means of payment in the future.

## Potential further improvements
- to be completed