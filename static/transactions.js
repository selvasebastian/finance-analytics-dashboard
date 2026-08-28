// Runs when the page is loaded
document.addEventListener("DOMContentLoaded", function() { 
loadTransactions();
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