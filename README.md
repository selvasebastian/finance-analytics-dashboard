# finance-analytics-dashboard

A web application that helps users understand their personal finances through an interactive transaction table and summary visualizations (spending by category, income vs. expenses, and budget tracking).

## AI Disclaimer
Artificial intelligence tools were used in the development of this portfolio. Claude (Anthropic) was used to weigh different alternatives, explore possible solutions, and suggest approaches to problems. It was also used to check the code for logical errors, typos and to explain various aspects and features of the programming languages used. Furthermore, it was used to help planning the approaches to create different code elements and to serve as a guide for understanding how certain things work. Claude further assisted with debugging and with checking spelling and writing errors across various documents and was used to check whether the results met the requirements of the assignment. Claude was also used to reformulate statements in the artifacts that have to be handed in alongside the code. Google’s AI-assisted search feature in the browser (not Gemini) was also used to answer questions about how certain things work in programming languages and how to implement certain features. The code itself was written and checked by the author, who takes sole responsibility for it.

## Scope
Core Minimum Viable Product (MVP)
- Transaction table with sorting, search, filtering and pagination
- Manual entry form and CSV import
- Spending by category, income vs. expenses charts
- Overall monthly budget and per-category budgets
- Spending trends over time

Optional (if time is available)
- Comparison of income and expenses accross different accounts (Update: dropped, not implemented)
- Net worth chart (Update implemented)

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
POST       /api/reset                               Reset transactions (additional added feature during the build process).
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

## Dependencies/ Tech stack
Backend
- Flask 3.1.3
- Python 3
- JSON API, 11 routes
- JavaScript

Frontend
- Bootstrap 5.3.0
- jQuery 3.7.0
- DataTables.js 1.13.6
- Chart.js
- CSS
- HTML

Tools
- GitHub
- Microsoft Visual Studio Code
- Google Search aid AI in the browser (see AI Disclaimer above)
- ClaudeAI (see AI Disclaimer below)

Built-in (no installation needed):
- SQLite (Database)

## Manual/ Important Notes
- The system will come with predefined data. By pressing "Reset all transactions" on the transactions page. These predefined transactions will be deleted, the charts reset and the user can start entering their data. However, the start values for the accounts will not be reset. If wished this values can become zero by entering two expenses that will make the account balance of each of the accounts to zero.
- All five fields on the Transactions page for adding new data must obtain inputs. The date and amount fields only accept valid input formats.
- When adding an expense at the Transactions page it is necessary to add a minus before the number, otherwise the system will interpret it wrongly and the charts will be erroneous.
- In order to make additional categories appear in the "Budget per Category" Chart, it is necessary to set a budget on the Charts page for the corresponding category.
- If a transaction leads to a negative balance (spending more than is available), the charts may not display this account correctly. However, this was a deliberate decision since it is possible to overdraw an account and also a normal process for some means of payment (e.g. credit cards) or short types of loans that may be added as additional means of payment in the future.
- The dashboard's charts and the budget form currently use a hardcoded month (2026-08). This was a chosen simplification, because the project is built around a fixed set of sample data.
- The application requires an active internet connection to function, although the backend runs locally. This because of the usage of Bootstrap, jQuery, DataTables.js and Chart.js.
- The "CSV import" does not validate the input. If a row contains a category or account name that does not exist in the system or an invalid amount format or anything else that isn't according to the defined input, the import will fail. Furthermore, it must be said that this application contains no real CSV input and more a field where users can enter data in CSV style.

## Potential further improvements
- User-created account types, for example overdraft account, mortgage account, car loan account
- Naming accounts according to the institution, for example credit card at American Express, because some customers may have several cards or accounts of the same type
- Deletion and editing of single transactions, because currently there is no possibility to edit a transaction if some data was entered falsely.
- Showing customized time horizons of the charts, because now it is only possible to use the default timeframe. Also filtering what categories should be shown in a pie or bar chart is currently not possible, for example showing only basic need categories in the spending by category pie chart.
- Adding further categories and also sub categories. Transport for instance could be split into car and everything that goes alongside it (insurance, fuel, service, repair, etc.) and Transport including everything else. Health could be split into Sport and "real health expenses" like pharmacy or doctor.
- Different default/accounting currencies to scale the system to other regions.
- Adding cash and credit card as well as more transactions into seed.py.
- Spending from a savings account isn't really the purpose of this account type. Therefore, it would be sensible to limit the possible transactions of savings account to transferring money from and to the giro account.
- Bank/Broker/Crypto Exchange API integration for automatic transaction and asset live price import so users can track their net worth.
- Allowing users to add other Assets like Gold or so with their purchasing price and track the unrealized profit.
- Machine learning of user spending behavior and learning what the user pays twice, for instance they have a car insurance and are a member of an ÖAMTC special insurance that covers basically the same.
- Working together with insurances and financial institutions by using affiliate links for promoting products that customers don't have according to their spending habits. 
- Add user login/account. Letting several people have access to a certain views/transactions so accounts that are owned jointly by several people can be managed by all owners.
- Remove hardcoded values and make charts available for all data.
- CSV import uses plain-text field and not a full file upload.
- Expenses need a minus sign when they are added on the transactions page. This is very cumbersome when adding data and therefore the minus should be added automatically. 
- The "Reset all transactions" only removes the transactions of the seed.py but not the initial balances.
- Neither the manual transaction form nor the CSV validate input on the server-side. The browser-side form filters most invalid input before it reaches the server, but this protection is not enforced on the backend.
