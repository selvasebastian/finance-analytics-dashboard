// Runs when the page is loaded
document.addEventListener("DOMContentLoaded", function() { 
loadTransactions();
loadAccountOptions();
loadCategoryOptions();
loadFilterCategoryOptions();
});

// Shows a succes or error message above the form
function showMessage(text, isError){
    const messageBox = document.querySelector("#message");
    messageBox.textContent = text;

    if (isError) {
        messageBox.className = "alert alert-danger";
    } else {
        messageBox.className = "alert alert-success";
    }
}

// Fetches the transaction data from the API and fills the table
async function loadTransactions() {
    const response = await fetch("/api/transactions");
    const transactions = await response.json();

    // Removes the old DataTable (if there is one), so that the table can be built again
    if ($.fn.DataTable.isDataTable("#transactions-table")) {
        $("#transactions-table").DataTable().destroy();
    }

    // Finds the <tbody> element where the rows will be inserted
    const tableBody = document.querySelector("#transactions-table tbody");

    // Deletes old rows
    tableBody.innerHTML = "";

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

    // Deletes old options
    accountSelect.innerHTML = '<option value="">Account</option>';


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

    const response = await fetch("/api/transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newTransaction),
    });
    const result = await response.json();

    // Shows the error message if something went wrong
    if (result.error) {
        showMessage(result.error, true);
        return;
    }

    // Shows a success message, epmties the form and reloads the table
    showMessage("Transaction added.", false);
    document.querySelector("#add-transaction-form").reset();
    loadTransactions();
});

// Submit Button of the form to create a new account
document.querySelector("#add-account-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const newAccount = {
        name: document.querySelector("#account-name").value,
        type: document.querySelector("#account-type").value,
        opening_balance: document.querySelector("#account-opening-balance").value,
    };

    const response = await fetch("/api/accounts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newAccount),
    });
    const result = await response.json();

    // Shows the error message if something went wrong
    if (result.error) {
        showMessage(result.error, true);
        return;
    }

    // Shows a success message, epmties the form and reloads the dropdown
    showMessage(result.message, false);
    document.querySelector("#add-account-form").reset();
    loadAccountOptions();
});

// Handles clicking the reset button
document.querySelector("#reset-button").addEventListener("click", async function (){
    const response = await fetch("/api/reset", {
        method: "POST",
    });
    const result = await response.json();

    // Shows succes message and loads table again
    showMessage(result.message, false);
    loadTransactions();
});

// Fetches all categories and fills the filter dropdown
async function loadFilterCategoryOptions() {
    const response = await fetch ("/api/categories");
    const categories = await response.json();

    //Finds the select element where the options will be inserted
    const filterSelect = document.querySelector("#filter-category");

    for (let i = 0; i < categories.length; i++) {
        const category = categories [i];

        const option = document.createElement("option");
        option.value = category.name;
        option.textContent = category.name;

        filterSelect.appendChild(option);
    }
    
}

// Filters the transaction table when a category is selected
document.querySelector("#filter-category").addEventListener("change", function () {
    const selectedCategory = document.querySelector("#filter-category").value;
    const table = $("#transactions-table").DataTable();
    table.search(selectedCategory).draw();
});

// Handles clicking the import button
document.querySelector("#import-button").addEventListener("click", async function () {
    const csvText = document.querySelector("#csv-input").value;

    const response = await fetch("/api/transactions/import", {
        method: "POST",
        headers :{"Content-Type": "application/json"},
        body: JSON.stringify({ csv_text: csvText })
    });
    const result = await response.json();

    // Shows the error message if something went wrong
    if (result.error) {
        showMessage(result.error, true);
        return;
    }
    
    // Shows a success message, epmties the form and reloads the table
    showMessage(result.message, false);
    document.querySelector("#csv-input").value = "";
    loadTransactions();
});
