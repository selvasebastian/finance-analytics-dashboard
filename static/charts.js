// Runs when the pag is loaded
document.addEventListener("DOMContentLoaded", function () {
    loadCategoryChart();
    loadIncomeChart();
    loadMonthlyChart();
    loadTrendsChart();
    loadOverallBudgetChart();
    loadCategoryBudgetChart();
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

// Fetches the monthly summary and draws a line chart of spending over time
async function loadTrendsChart() {
    const response = await fetch("/api/summary/monthly");
    const summary = await response.json(); 

    const labels = [];
    const expenseValues = [];

    for (let i = 0; i < summary.length; i++) {
        const entry = summary[i];

        labels.push(entry.month);
        expenseValues.push(Math.abs(entry.expenses_cents / 100));
    }
 
    // Finds the canvas elements and draws the line chart
    const canvas = document.querySelector("#trends-chart");

    new Chart(canvas, {
        type: "line",
        data: {
            labels: labels, 
            datasets: [
                {
                    label: "Spending per Month",
                    data: expenseValues,
                }
            ]
        },
    });
}

// Fetches the budgets and monthly spending and draws the overall budget chart
async function loadOverallBudgetChart() {
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

    // Finds the canvs element and draws the pie chart
    const canvas = document.querySelector("#overall-budget-chart");

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

// Fetches the budgets and category spending and draws a bar chart per category
async function loadCategoryBudgetChart() {
    const budgetsResponse = await fetch("/api/budgets?month=2026-08");
    const budgets = await budgetsResponse.json();

    const categoryResponse = await fetch("/api/summary/by-category?month=2026-08");
    const categorySummary = await categoryResponse.json();

    const labels = [];
    const limitValues = [];
    const spentValues = [];

    // Loop through every budget, skip the overall one and the matching category
    for (let i = 0; i < budgets.length; i++) {
        const budget = budgets[i];

        //Skip the overall budget
        if (budget.category_id === null) {
            continue;
        }

        // Find how much was spent in a category
        let spentCents = 0;
        for (let a = 0; a < categorySummary.length; a++) {
            const entry = categorySummary[a];

            if(entry.category === budget.category) {
                spentCents = Math.abs(entry.total_cents);
            }
        }

        labels.push(budget.category);
        limitValues.push(budget.limit_cents / 100);
        spentValues.push(spentCents / 100);
    }

    // Finds the canvas element and draws the bar chart
    const canvas = document.querySelector("#category-budget-chart");

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Budget",
                    data: limitValues,
                },
                {
                    label: "Spent",
                    data: spentValues,
                },
            ],
        },
    });
}