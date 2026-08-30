// Runs when the page is loaded
document.addEventListener("DOMContentLoaded", function () {
    loadRecentTransactions();
    loadNetWorthChart();
    loadBudgetChart();
});

// Fetches the transaction data from the API and fills the table
async function loadRecentTransactions() {
    const response = await fetch("/api/transactions");
    const transactions = await response.json();

    // Finds the <tbody> element where the rows will be insterted
    const tableBody = document.querySelector("#recent-table tbody");

    for (let i = 0; i < 5; i++) {
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
}

// Fetches account balances and draws a pie chart of the net worth
async function loadNetWorthChart() {
    const netWorthResponse = await fetch("/api/summary/net-worth");
    const netWorth = await netWorthResponse.json();

    const labels = [];
    const values = [];

    // Get account names and their balances
    for (let i = 0; i < netWorth.length; i++) {
        const entry = netWorth[i];

        labels.push(entry.account);
        values.push(entry.balance_cents / 100);
    }

    // Finds the canvas element and draws the pie chart
    const canvas = document.querySelector("#home-networth-chart");

    new Chart(canvas, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values,
            }],
        },
    });
}

// Fetches the budgets and monthly spending and draws the overall budget chart
async function loadBudgetChart() {
    const budgetsResponse = await fetch("/api/budgets?month=2026-08");
    const budgets = await budgetsResponse.json();

    const monthlyResponse = await fetch("/api/summary/monthly");
    const monthlySummary = await monthlyResponse.json();

    // Find the overall budget
    let overallLimitCents = 0;
    for (let i = 0; i < budgets.length; i++) {
        const budget = budgets[i];

        if (budget.category_id === null) {
            overallLimitCents = budget.limit_cents;
        }
    }

    // Find how much was spent in August
    let spentCents = 0;
    for (let i = 0; i < monthlySummary.length; i++) {
        const entry = monthlySummary[i];

        if (entry.month === "2026-08") {
            spentCents = Math.abs(entry.expenses_cents);
        }
    }

    const spentEuros = spentCents / 100;
    const remainingEuros = Math.max(0, (overallLimitCents - spentCents) /100);

    // Finds the canvas element and draws the pie chart
    const canvas = document.querySelector("#home-budget-chart");

    new Chart(canvas, {
        type: "pie",
        data: {
            labels: ["Spent", "Remaining"],
            datasets: [{
                data: [spentEuros, remainingEuros]
            }],
        },
    });
}