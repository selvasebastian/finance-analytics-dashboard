from flask import Flask, jsonify, render_template
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
        "SELECT transactions.id, transactions.transaction_date, transactions.description, transactions.amount_cents," "accounts.name, categories.name " "FROM transactions, accounts, categories " "WHERE transactions.account_id = accounts.id AND transactions.category_id = categories.id " "ORDER BY transactions.transaction_date DESC")

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

if __name__ == "__main__":
    app.run(debug=True)
