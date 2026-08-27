-- Current account balance is not saved, but later calculated (opening_balance_cents + sum all transactions)
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    opening_balance_cents INTEGER NOT NULL DEFAULT 0
);

-- Categories for Transactions, kind is either income or expense
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    kind VARCHAR NOT NULL
);

-- Single Transactions, cent amounts get stored, negative amount = expensive, positive amount = income
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date DATE NOT NULL,
    description VARCHAR NOT NULL,
    amount_cents INTEGER NOT NULL,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    category_id INTEGER NOT NULL REFERENCES categories (id)
);

-- Budgets per month, category id is not NOT Null because NULL = overall budget for the month
CREATE TABLE budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month VARCHAR NOT NULL,
    limit_amount_cents INTEGER NOT NULL,
    category_id INTEGER REFERENCES categories (id),
    UNIQUE(month, category_id)
);

-- Indices for faster querys
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_account ON transactions(account_id, transaction_date);
CREATE INDEX idx_transactions_category ON transactions (category_id, transaction_date);