from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Homepage
@app.route("/")
def home():
    return "Dashboard is running"

# Returns all transactions as JSON
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

if __name__ == "__main__":
    app.run(debug=True)