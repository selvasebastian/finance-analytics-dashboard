from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Homepage
@app.route("/")
def home():
    return "Dashboard is running"

# Shows the transactions page
@app.route("/transactions")
def transactions_page():
    return render_template("transactions.html")

# GET/api/transactions - lists all transactions with account- and category names
@app.route("/api/transactions")
def get_transactions():
    # Connect to database
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()

    # Get every transaction with the account and category name
    cur.execute(
        "SELECT transactions.id, transactions.transaction_date, transactions.description, transactions.amount_cents," "accounts.name, categories.name "
        "FROM transactions, accounts, categories "
        "WHERE transactions.account_id = accounts.id AND transactions.category_id = categories.id "
        "ORDER BY transactions.transaction_date DESC")

    rows = cur.fetchall()
    conn.close()

    # Create a dictionary for each row so it can be converted to JSON
    transactions =[]
    for row in rows:
        transaction = {
            "id": row[0],
            "date": row[1],
            "description": row[2],
            "amount_cents": row[3],
            "account": row[4],
            "category": row [5],
        }
        transactions.append(transaction)

    return jsonify(transactions)

# POST /api/transactions - creates one transaction
@app.route("/api/transactions", methods=["POST"])
def create_transaction():
    # Conntect to database
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()

    # Read the JSON data
    data = request.get_json()

    # Convert the euro amount into cents
    amount_cents = round(float(data["amount"]) * 100)

    # Adds a row in transactions with corresponding values
    cur.execute(
        "INSERT INTO transactions (transaction_date, description, amount_cents, account_id, category_id)"
        "VALUES (:date, :description, :amount_cents, :account_id, :category_id)",
        {
        "date": data["date"],
        "description": data["description"],
        "amount_cents": amount_cents,
        "account_id": data["account_id"],
        "category_id": data ["category_id"],
        }
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Transaction created"})

# GET /api/categories - lists all categories
@app.route("/api/categories")
def get_categories():
    # Conntect to database
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()

    # get every category
    cur.execute("SELECT id, name, kind FROM categories ORDER BY name")

    rows = cur.fetchall()
    conn.close()

    # Create a dictionary for each row so it can be converted to JSON
    categories = []
    for row in rows:
        category = {
            "id": row[0],
            "name": row[1],
            "kind": row[2],
        }
        categories.append(category)
    return jsonify(categories)

# Get /api/accounts - lists all accounts
@app.route("/api/accounts")
def get_accounts():
    # Connect to database
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()

    # Get every accounts
    cur.execute("SELECT id, name, type FROM accounts ORDER BY name")

    rows = cur.fetchall()
    conn.close()

    # Create a dictionary for each row so it can be converted to JSON
    accounts = []
    for row in rows:
        account = {
            "id": row[0],
            "name": row[1],
            "type": row[2],
        }
        accounts.append(account)

    return jsonify(accounts)

# GET /api/summary/by-category?month=YYYY-MM - Spending and income totals per category.
@app.route("/api/summary/by-category")
def get_summary_by_category():
    # Connect to database
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()

    # Read the month from the URL
    month = request.args.get("month")

    # Sum the amount for each category in the concerned month
    cur.execute(
        "SELECT categories.name, SUM(transactions.amount_cents) "
        "FROM transactions, categories "
        "WHERE transactions.category_id = categories.id "
        "AND transactions.transaction_date LIKE :month_pattern "
        "GROUP BY categories.name",
        {"month_pattern": month + "%"}
    )

    rows = cur.fetchall()
    conn.close()

    #Create a dictionary for each row so it can be converted to JSON
    summary = []
    for row in rows:
        entry = {
            "category": row[0],
            "total_cents": row[1],
        }
        summary.append(entry)
    return jsonify(summary)

if __name__ == "__main__":
    app.run(debug=True)
