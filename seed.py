import sqlite3

conn = sqlite3.connect("finance.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# Creates the tables from schema.sql (old tables are deleted first)
schema_file = open("schema.sql")
cur.executescript(schema_file.read())
schema_file.close()

# Creates two new accounts
cur.execute("INSERT INTO accounts (name, type, opening_balance_cents) VALUES ('Giro', 'checking', 150000)")
cur.execute("INSERT INTO accounts (name, type, opening_balance_cents) VALUES ('Savings', 'savings', 500000)")
cur.execute("INSERT INTO accounts (name, type, opening_balance_cents) VALUES ('Cash', 'cash', 10000)")
cur.execute("INSERT INTO accounts (name, type, opening_balance_cents) VALUES ('Credit Card', 'credit', 0)")

# Creates eight categories
cur.execute("INSERT INTO categories (name, kind) VALUES ('Salary', 'income')")
cur.execute("INSERT INTO categories (name, kind) VALUES ('Other Earnings', 'income')")
cur.execute("INSERT INTO categories (name, kind) VALUES ('Groceries & Household', 'expense')")
cur.execute("INSERT INTO categories (name, kind) VALUES ('Housing', 'expense')")
cur.execute("INSERT INTO categories (name, kind) VALUES ('Transport', 'expense')")
cur.execute("INSERT INTO categories (name, kind) VALUES ('Leisure', 'expense')")
cur.execute("INSERT INTO categories (name, kind) VALUES ('Health', 'expense')")
cur.execute("INSERT INTO categories (name, kind) VALUES ('Insurance', 'expense')")

conn.commit()

# Looks up the id of an account by its name
def get_account_id(name):
    cur.execute("SELECT id FROM accounts WHERE name = ?", (name,))
    row = cur.fetchone()
    return row[0]

# Looks up the id of a category by its name
def get_category_id(name):
    cur.execute("SELECT id FROM categories WHERE name = ?", (name,))
    row = cur.fetchone()
    return row[0]

# One entry per transaction, grouped by month
transactions_by_month = {
    "2026-06": [
        {"date": "2026-06-01", "description": "Salary", "amount": 3200.00, "account": "Giro","category": "Salary"},
        {"date": "2026-06-01", "description": "Rent", "amount": -950.00, "account": "Giro", "category": "Housing"},
        {"date": "2026-06-02", "description": "MPreis", "amount": -64.20, "account": "Giro", "category":"Groceries & Household"},
        {"date": "2026-06-04", "description": "Cinema", "amount": -24.00, "account":"Giro", "category": "Leisure"},
        {"date": "2026-06-05", "description": "ÖBB", "amount": -89.00, "account": "Giro", "category": "Transport"},
        {"date": "2026-06-08", "description": "Billa", "amount": -52.30, "account": "Giro", "category": "Groceries & Household"},
        {"date": "2026-06-08", "description": "Bar Moose", "amount": -61.00, "account": "Giro", "category": "Leisure"},
        {"date": "2026-06-12", "description": "Fuel", "amount": -59.00, "account": "Savings", "category": "Transport"},
        {"date": "2026-06-15", "description": "Hofer", "amount": -74.80, "account": "Giro", "category": "Groceries & Household"},
        {"date": "2026-06-18", "description": "Gym", "amount": -45.00, "account": "Giro", "category": "Health"},
    ],
    "2026-07": [
        {"date": "2026-07-01", "description": "Salary", "amount": 3200.00, "account": "Giro", "category": "Salary"},
        {"date": "2026-07-01", "description": "Rent", "amount": -950.00, "account": "Giro", "category": "Housing"},
        {"date": "2026-07-03", "description": "MPreis", "amount": -58.70, "account": "Giro", "category": "Groceries & Household"},
        {"date": "2026-07-05", "description": "ÖBB", "amount": -89.00, "account": "Giro", "category": "Transport"},
        {"date": "2026-07-08", "description": "Billa", "amount": -88.50, "account": "Giro", "category": "Groceries & Household"},
        {"date": "2026-07-10", "description": "Cinema", "amount": -24.00, "account": "Giro", "category": "Leisure"},
        {"date": "2026-07-16", "description": "Fuel", "amount": -57.00, "account": "Savings", "category": "Transport"},
        {"date": "2026-07-24", "description": "Dividend payment", "amount": 45.00, "account": "Savings", "category": "Other Earnings"},   
    ],
    "2026-08": [
        {"date": "2026-08-01", "description": "Salary", "amount": 3200.00, "account": "Giro", "category": "Salary"},
        {"date": "2026-08-01", "description": "Rent", "amount": -950.00, "account": "Giro", "category": "Housing"},
        {"date": "2026-08-03", "description": "MPreis", "amount": -64.20, "account": "Giro", "category": "Groceries & Household"},
        {"date": "2026-08-05", "description": "Liability Insurance", "amount": -15.00, "account": "Giro", "category": "Insurance"},
        {"date": "2026-08-07", "description": "ÖBB", "amount": -89.00, "account": "Giro", "category": "Transport"},
        {"date": "2026-08-07", "description": "Billa", "amount": -112.85, "account": "Giro", "category": "Groceries & Household"},
        {"date": "2026-08-14", "description": "Restaurant Wal", "amount": -97.50, "account": "Giro", "category": "Leisure"},
        {"date": "2026-08-18", "description": "Gym", "amount": -111.50, "account": "Giro", "category": "Health"},
        {"date": "2026-08-22", "description": "Dividend payout", "amount": 52.00, "account": "Savings", "category": "Other Earnings"},
    ],
    "2026-09": [
        {"date": "2026-09-01", "description": "Salary", "amount": 3200.00, "account": "Giro", "category": "Salary"},
        {"date": "2026-09-01", "description": "Rent", "amount": -950.00, "account": "Giro", "category": "Housing"},
        {"date": "2026-09-02", "description": "Bakery", "amount": -5.20, "account": "Cash", "category": "Groceries & Household"},
    ],
    "2026-10": [
        {"date": "2026-10-01", "description": "Salary", "amount": 3200.00, "account": "Giro", "category": "Salary"},
        {"date": "2026-10-01", "description": "Rent", "amount": -950.00, "account": "Giro", "category": "Housing"},
        {"date": "2026-10-03", "description": "MPreis", "amount": -12.00, "account": "Cash", "category": "Groceries & Household"},
        {"date": "2026-10-05", "description": "ÖBB", "amount": -89.00, "account": "Giro", "category": "Transport"},
    ],
}

# Insert every transaction and converting each euro amount into integer cents
total_inserted = 0
for month in transactions_by_month:
    entries = transactions_by_month[month]
    for entry in entries:
        amount_cents = round(entry["amount"] * 100)
        account_id = get_account_id(entry["account"])
        category_id = get_category_id(entry["category"])
        cur.execute(
            "INSERT INTO transactions (transaction_date, description, amount_cents, account_id, category_id)" "VALUES (:date, :description, :amount_cents, :account_id, :category_id)", 
            {
                "date": entry["date"],
                "description": entry["description"],
                "amount_cents": amount_cents,
                "account_id": account_id,
                "category_id": category_id,
            }
        )
        total_inserted = total_inserted + 1
conn.commit()

# Sets budget for the every month and category
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, NULL)", {"month": "2026-06", "limit": 200000})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-06", "limit": 40000, "category_id": get_category_id("Groceries & Household")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-06", "limit": 100000, "category_id": get_category_id("Housing")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-06", "limit": 10000, "category_id": get_category_id("Transport")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-06", "limit": 15000, "category_id": get_category_id("Leisure")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-06", "limit": 50000, "category_id": get_category_id("Health")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-06", "limit": 20000, "category_id": get_category_id("Insurance")})

cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, NULL)", {"month": "2026-07", "limit": 200000})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-07", "limit": 40000, "category_id": get_category_id("Groceries & Household")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-07", "limit": 100000, "category_id": get_category_id("Housing")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-07", "limit": 10000, "category_id": get_category_id("Transport")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-07", "limit": 15000, "category_id": get_category_id("Leisure")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-07", "limit": 50000, "category_id": get_category_id("Health")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-07", "limit": 20000, "category_id": get_category_id("Insurance")})

cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, NULL)", {"month": "2026-08", "limit": 200000})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-08", "limit": 40000, "category_id": get_category_id("Groceries & Household")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-08", "limit": 100000, "category_id": get_category_id("Housing")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-08", "limit": 10000, "category_id": get_category_id("Transport")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-08", "limit": 15000, "category_id": get_category_id("Leisure")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-08", "limit": 50000, "category_id": get_category_id("Health")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-08", "limit": 20000, "category_id": get_category_id("Insurance")})

cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, NULL)", {"month": "2026-09", "limit": 200000})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-09", "limit": 40000, "category_id": get_category_id("Groceries & Household")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-09", "limit": 100000, "category_id": get_category_id("Housing")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-09", "limit": 10000, "category_id": get_category_id("Transport")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-09", "limit": 15000, "category_id": get_category_id("Leisure")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-09", "limit": 50000, "category_id": get_category_id("Health")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-09", "limit": 20000, "category_id": get_category_id("Insurance")})

cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, NULL)", {"month": "2026-10", "limit": 200000})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-10", "limit": 40000, "category_id": get_category_id("Groceries & Household")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-10", "limit": 100000, "category_id": get_category_id("Housing")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-10", "limit": 10000, "category_id": get_category_id("Transport")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-10", "limit": 15000, "category_id": get_category_id("Leisure")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-10", "limit": 50000, "category_id": get_category_id("Health")})
cur.execute("INSERT INTO budgets (month, limit_amount_cents, category_id) VALUES (:month, :limit, :category_id)", {"month": "2026-10", "limit": 20000, "category_id": get_category_id("Insurance")})

conn.commit()
conn.close()

print(f"{total_inserted} transaction inserted.")
