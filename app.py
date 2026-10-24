from flask import Flask, jsonify, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Connects to the database
def get_connection():
    conn = sqlite3.connect("finance.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Checks if a text is a real date
def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False

#Checks all values of one transaction before it is saved
def validate_transaction(cur, date, description, amount, account_id, category_id):
    if not is_valid_date(date):
        return None, "Invalid date format. Please use YYYY-MM-DD."

    if description.strip() == "":
        return None, "Description cannot be empty."
    if len(description.strip()) > 100:
        return None, "Description cannot be longer than 100 characters."

    # Convert amount into cents
    try:
        amount_cents = round(float(amount) * 100)
    except (ValueError):
        return None, "Amount must be a number."
    if amount_cents == 0:
        return None, "Amount cannot be zero."

    # Check if the account exists
    cur.execute("SELECT id FROM accounts WHERE id = :id", {"id": account_id})
    if cur.fetchone() is None:
        return None, "Account does not exist."

    # Check if the category exists
    cur.execute("SELECT kind FROM categories WHERE id = :id", {"id": category_id})
    category_row = cur.fetchone()
    if category_row is None:
        return None, "Category does not exist."

    # Sign is determined by the category
    if category_row[0] =="expense":
        amount_cents = -abs(amount_cents)
    else:
        amount_cents = abs(amount_cents)

    transaction = {
        "date": date,
        "description": description.strip(),
        "amount_cents": amount_cents,
        "account_id": account_id,
        "category_id": category_id,
    }

    return transaction, None

# Homepage
@app.route("/")
def home():
    return render_template("home.html")

# Shows the transactions page
@app.route("/transactions")
def transactions_page():
    return render_template("transactions.html")

# Shows the charts page
@app.route("/charts")
def charts_page():
    return render_template("charts.html")

# GET/api/transactions - lists all transactions with account- and category names
@app.route("/api/transactions")
def get_transactions():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Get every transaction with the account and category name
    cur.execute(
        "SELECT transactions.id, transactions.transaction_date, transactions.description, transactions.amount_cents, accounts.name, categories.name "
        "FROM transactions "
        "JOIN accounts ON transactions.account_id = accounts.id "
        "JOIN categories ON transactions.category_id = categories.id "
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
    conn = get_connection()
    cur = conn.cursor()

    # Read the JSON data
    data = request.get_json()

    # Check values and set minus sign for expenses
    transaction, error = validate_transaction(cur, data["date"], data["description"], data["amount"], data["account_id"], data["category_id"])
    if error is not None:
        conn.close()
        return jsonify({"error": error})

    # Adds a row in transaction with the validated values
    cur.execute(
        "INSERT INTO transactions (transaction_date, description, amount_cents, account_id, category_id) "
        "VALUES (:date, :description, :amount_cents, :account_id, :category_id)",
        transaction
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Transaction created"})

# GET /api/categories - lists all categories
@app.route("/api/categories")
def get_categories():
    # Conntect to database
    conn = get_connection()
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
    conn = get_connection()
    cur = conn.cursor()

    # Get every account with its balance
    cur.execute("SELECT accounts.id, accounts.name, accounts.type, accounts.opening_balance_cents + COALESCE(SUM(transactions.amount_cents), 0) "
                "FROM accounts "
                "LEFT JOIN transactions ON transactions.account_id = accounts.id "
                "GROUP BY accounts.id")

    rows = cur.fetchall()
    conn.close()

    # Create a dictionary for each row so it can be converted to JSON
    accounts = []
    for row in rows:
        account = {
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "balance_cents": row[3],
        }
        accounts.append(account)

    return jsonify(accounts)

# POST /api/accounts - creates a new account
@app.route("/api/accounts", methods=["POST"])
def create_account():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Read the JSON data
    data = request.get_json()
    name = data["name"].strip()
    account_type = data["type"]
    opening_balance = data["opening_balance"]

    # Check values
    if name == "":
        conn.close()
        return jsonify({"error": "Account name cannot be empty."})
    if len(name) > 50:
        conn.close()
        return jsonify({"error": "Account name cannot be longer than 50 characters."})
    if account_type not in ["checking", "savings", "cash", "credit"]:
        conn.close()
        return jsonify({"error": "Account type does not exist."})

    # Convert opening balance into cents
    try:
        opening_balance_cents = round(float(opening_balance) * 100)
    except (ValueError):
        conn.close()
        return jsonify({"error": "Opening balance must be a number."})

    # Check if the account name already exists
    cur.execute("SELECT id FROM accounts WHERE name = :name", {"name": name})
    if cur.fetchone() is not None:
        conn.close()
        return jsonify({"error": "Account name already exists."})

    # Adds the new account
    cur.execute(
        "INSERT INTO accounts (name, type, opening_balance_cents) "
        "VALUES (:name, :type, :opening_balance_cents)",
        {
            "name": name,
            "type": account_type,
            "opening_balance_cents": opening_balance_cents
        }
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Account created"})

# GET /api/summary/by-category?month=YYYY-MM - Spending and income totals per category.
@app.route("/api/summary/by-category")
def get_summary_by_category():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Read the month from the URL
    month = request.args.get("month")

    # Sum the amount for each category in the concerned month
    cur.execute(
        "SELECT categories.name, SUM(transactions.amount_cents) "
        "FROM transactions "
        "JOIN categories ON transactions.category_id = categories.id "
        "WHERE transactions.transaction_date LIKE :month_pattern "
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

# GET /api/summary/monthly - Income versus expenses per month
@app.route("/api/summary/monthly")
def get_summary_monthly():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Group all transactions by month and sum income and expenses
    cur.execute(
        "SELECT substr(transaction_date, 1, 7) AS month, "
        "SUM(CASE WHEN amount_cents > 0 THEN amount_cents ELSE 0 END), "
        "SUM(CASE WHEN amount_cents < 0 THEN amount_cents ELSE 0 END) "
        "FROM transactions "
        "GROUP BY month "
        "ORDER BY month"
    )

    rows = cur.fetchall()
    conn.close()
    
    #Create a dictionary for each row so it can be converted to JSON
    summary = []
    for row in rows:
        entry = {
            "month": row[0],
            "income_cents": row[1],
            "expenses_cents": row [2],
        }
        summary.append(entry)

    return jsonify(summary)

# GET /api/budgets?month=YYYY-MM - reads the budget for the corresponding month
@app.route("/api/budgets")
def get_budgets():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Read the month from the URL
    month = request.args.get("month")

    # Get the budgets for the for the concerned month with the category name
    cur.execute(
        "SELECT budgets.id, budgets.limit_amount_cents, budgets.category_id, categories.name "
        "FROM budgets "
        "LEFT JOIN categories ON budgets.category_id = categories.id "
        "WHERE budgets.month = :month",
        {"month": month}
    )

    rows = cur.fetchall()
    conn.close()

    # Create a dictionary for each row so it can be converted to JSON
    budgets = []
    for row in rows:
        budget = {
            "id": row[0],
            "limit_cents": row[1],
            "category_id": row[2],
            "category": row[3],
        }
        budgets.append(budget)
    return jsonify(budgets)

# PUT /api/budgets?month=YYYY-MM - sets the budget for the corresponding month
@app.route("/api/budgets", methods=["PUT"])
def set_budget():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Read the JSON data
    data = request.get_json()

    # Deletes the budget for this month and category (if one exists)
    cur.execute(
        "DELETE FROM budgets WHERE month = :month AND category_id IS :category_id",
        {"month": data["month"], "category_id": data.get("category_id")}
    )

    # Inserts the new budget
    cur.execute(
        "INSERT INTO budgets (month, limit_amount_cents, category_id) "
        "VALUES (:month, :limit, :category_id)",
        {
            "month": data["month"],
            "limit": data["limit_cents"],
            "category_id": data.get("category_id"),
        }
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Budget saved"})

# GET /api/summary/net-worth - balance per account
@app.route("/api/summary/net-worth")
def get_net_worth():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Get every account with its balance
    cur.execute(
        "SELECT accounts.name, accounts.opening_balance_cents + COALESCE(SUM(transactions.amount_cents), 0) "
        "FROM accounts "
        "LEFT JOIN transactions ON transactions.account_id = accounts.id "
        "GROUP BY accounts.id"
        )

    rows = cur.fetchall()
    conn.close()

    # Create a dictionary for each row so it can be converted to JSON
    net_worth = []
    for row in rows:
        entry = {
            "account": row[0],
            "balance_cents": row[1],
        }
        net_worth.append(entry)

    return jsonify(net_worth)

# POST /api/reset - deletes all transactions so that user can clean up before entering their on transactions

@app.route("/api/reset", methods=["POST"])
def reset_transaction():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Delete every transaction
    cur.execute("DELETE FROM transactions")

    conn.commit()
    conn.close()

    return jsonify({"message": "All transactions deleted"})

# POST /api/transactions/import - creates transactions from CSV text
@app.route("/api/transactions/import", methods=["POST"])
def import_transactions():
    # Connect to database
    conn = get_connection()
    cur = conn.cursor()

    # Read the JSON data and expects input in form of a "csv_text" field
    data = request.get_json()
    csv_text = data["csv_text"]

    # Split the text into individuals lines
    lines = csv_text.strip().split("\n")

    # Check every line
    checked_transactions = []
    line_number = 0
    for line in lines:
        line_number = line_number + 1

        # Skip empty lines and the header line
        if line.strip() == "" or line.startswith("date,"):
            continue

        # Split the line into fields
        fields = line.split(",")
        if len(fields) != 5:
            conn.close()
            return jsonify({"error": "Line" + str(line_number) + ": needs 5 fields (date, description, amount, category, account)." })

        date = fields[0].strip()
        description = fields[1]
        amount = fields[2].strip()
        category_name = fields[3].strip()
        account_name = fields[4].strip()

        # Look up the account id
        cur.execute("SELECT id FROM accounts WHERE name = :name", {"name": account_name})
        account_row = cur.fetchone()
        if account_row is None:
            conn.close()
            return jsonify({"error": "Line" + str(line_number) + ": account " + account_name + " does not exist."})

        # Look up the category id
        cur.execute("SELECT id FROM categories WHERE name = :name", {"name": category_name})
        category_row = cur.fetchone()
        if category_row is None:
            conn.close()
            return jsonify({"error": "Line" + str(line_number) + ": category " + category_name + " does not exist."})

        # Check values
        transaction, error = validate_transaction(cur, date, description, amount, account_row[0], category_row[0])
        if error is not None:
            conn.close()
            return jsonify({"error": "Line" + str(line_number) + ": " + error})

        checked_transactions.append(transaction)

    # Save transactions
    for transaction in checked_transactions:
        cur.execute(
            "INSERT INTO transactions (transaction_date, description, amount_cents, account_id, category_id) "
            "VALUES (:date, :description, :amount_cents, :account_id, :category_id)",
            transaction
        )

    conn.commit()
    conn.close()

    return jsonify({"message": str(len(checked_transactions)) + " transactions imported."})   

if __name__ == "__main__":
    app.run(debug=True)
