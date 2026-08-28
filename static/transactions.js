// Runs when the page is loaded
document.addEventListener("DOMContentLoaded", function() { 
loadTransactions();
loadAccountOptions();
loadCategoryOptions();
});

// Fetches the transaction data from the API and fills the table
async function loadTransactions() {
    const response = await fetch("/api/transactions");
    const transactions = await response.json();

    // Finds the <tbody> element where the rows will be insterted
    const tableBody = document.querySelector("#transactions-table tbody");

    for (let i = 0; i < transactions.length; i++) {
        const transaction = transactions[i];

    // Converts cents back into euros
    const amountEuros = (transaction.amount_cents / 100).toFixed(2);

    // Builds one table row with the transaction data and adds it to the table
    const row = document.createElement("tr");
    row.innerHTML =
        "<td>" + transaction.date + "</td>" +
        "<td>" + transaction.description + "</td>" + 
        "<td>" + transaction.category + "</td>" +
        "<td>" + transaction.account + "</td>" + 
        "<td>" + amountEuros + " EUR</td>";

    tableBody.appendChild(row);
    }

    // Converts normal Table into DataTable
    $("#transactions-table").DataTable();

}

// Fetches all accounts and fills dropdown for accounts
async function loadAccountOptions() {
    const repsonse = await fetch("/api/accounts");
    const accounts = await repsonse.json();

    //Finds the select element where the options will be inserted
    const accountSelect = document.querySelector("#input-account");

    for (let i = 0; i < accounts.length; i++) {
        const account = accounts[i];

        const option = document.createElement("option");
        option.value = account.id;
        option.textContent = account.name;

        accountSelect.appendChild(option);
    }
}

// Fetches all categories and fills dropdown for categories
async function loadCategoryOptions() {
    const response = await fetch ("/api/categories");
    const categories = await response.json();

    //Finds the select element where the options will be inserted
    const categorySelect = document.querySelector("#input-category");

    for (let i = 0; i < categories.length; i++) {
        const category = categories [i];

        const option = document.createElement("option");
        option.value = category.id;
        option.textContent = category.name;

        categorySelect.appendChild(option);
    }
    
}

// Submit Button of the form to create a new transaction
document.querySelector("#add-transaction-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const newTransaction = {
        date: document.querySelector("#input-date").value,
        description: document.querySelector("#input-description").value,
        amount: document.querySelector("#input-amount").value,
        account_id: document.querySelector("#input-account").value,
        category_id: document.querySelector("#input-category").value,
    };

    await fetch ("/api/transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(newTransaction),
    });

    // Reload the page so that the new transaction appears
    location.reload();
});