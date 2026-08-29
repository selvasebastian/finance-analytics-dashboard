// Runs when the pag is loaded
document.addEventListener("DOMContentLoaded", function () {
    loadCategoryChart();
    loadIncomeChart();
    loadMonthlyChart();
});

// Fetches the category summary and draws a pie chart (Spending by category)
async function loadCategoryChart() {
    const response = await fetch("/api/summary/by-category?month=2026-08");
    const summary = await response.json();

    const labels = [];
    const values = [];

    for (let i = 0; i < summary.length; i++) {
        const entry = summary[i];

        // This chart should only show the spending categories
        if (entry.category === "Salary" || entry.category === "Other Earnings") {
            continue;
        }

        labels.push(entry.category);
        values.push(Math.abs(entry.total_cents / 100));
    }

    // Finds the canvas elements and draws the pie chart
    const canvas = document.querySelector("#category-chart");

    new Chart(canvas, {
        type: "pie",
        data: {
            labels: labels, 
            datasets: [{
               data:values,
             }]
        },
    });
}

// Fetches the category summary and draws a pie chart (Spending by income)
async function loadIncomeChart() {
    const response = await fetch("/api/summary/by-category?month=2026-08");
    const summary = await response.json();

    const labels = [];
    const values = [];

    for (let i = 0; i < summary.length; i++) {
        const entry = summary[i];

        // This chart should only show the income categories
        if (entry.category === "Salary" || entry.category === "Other Earnings") {
        labels.push(entry.category);
        values.push(entry.total_cents / 100);
        }
    }

    // Finds the canvas elements and draws the pie chart
    const canvas = document.querySelector("#income-chart");

    new Chart(canvas, {
        type: "pie",
        data: {
            labels: labels, 
            datasets: [{
               data:values,
            }]
        },
    });
}

// Fetches the monthly summary and draws a bar chart (Income vs. Expenses)
async function loadMonthlyChart() {
    const response = await fetch("/api/summary/monthly");
    const summary = await response.json(); 

    const labels = [];
    const incomeValues = [];
    const expenseValues = [];

    for (let i = 0; i < summary.length; i++) {
        const entry = summary[i];

        labels.push(entry.month);
        incomeValues.push(entry.income_cents / 100);
        expenseValues.push(Math.abs(entry.expenses_cents / 100));
    }
 
    // Finds the canvas elements and draws the bar chart
    const canvas = document.querySelector("#monthly-chart");

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels, 
            datasets: [
                {
                    label: "Income",
                    data: incomeValues,
                },
                {
                    label: "Expenses",
                    data: expenseValues,
                }
            ]
        },
    });
}