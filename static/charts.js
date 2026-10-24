// Month that is selected in the dropdown.
let selectedMonth = "";

// Shows the value and the EUR ticker when hover a chart
Chart.defaults.plugins.tooltip.callbacks.label = function(context) {
    if (context.dataset.label) {
        return context.dataset.label + ": " + context.raw.toFixed(2) + " EUR";
    }
    return context.raw.toFixed(2) + " EUR";
};

// Runs when the page is loaded
document.addEventListener("DOMContentLoaded", async function () {

    // Dropdown for the month has to be filled first, because many charts need this data
    await loadMonthOptions();

    loadCategoryChart();
    loadIncomeChart();
    loadMonthlyChart();
    loadTrendsChart();
    loadOverallBudgetChart();
    loadCategoryBudgetChart();
    loadNetWorthChart();
    loadBudgetCategoryOptions();
});

// Fetches all months and fills the dropdown for the month selection
async function loadMonthOptions() {
    const response = await fetch("/api/summary/monthly");
    const months = await response.json();

    // Finds the select element where the options will be inserted
    const monthSelect = document.querySelector("#month-select");

    for (let i = 0; i < months.length; i++) {
        const option = document.createElement("option");
        option.value = months[i].month;
        option.textContent = months[i].month;

        monthSelect.appendChild(option);
    }

    // Newest month is selected first
    if (months.length > 0) {
        selectedMonth = months[months.length - 1].month;
        monthSelect.value = selectedMonth;
    }
}

// When the month selection is changed, the charts have to be reloaded
document.querySelector("#month-select").addEventListener("change", function () {
    selectedMonth = document.querySelector("#month-select").value;
    loadCategoryChart();
    loadIncomeChart();
    loadOverallBudgetChart();
    loadCategoryBudgetChart();
});

// Shows a success or error message above the charts
function showMessage(text, isError) {
    const messageBox = document.querySelector("#message");
    messageBox.textContent = text;

    if (isError) {
        messageBox.className = "alert alert-danger";
    } else {
        messageBox.className = "alert alert-success";
    }
}

// Fetches the category summary and draws a pie chart (Spending by category)
async function loadCategoryChart() {
    const response = await fetch("/api/summary/by-category?month=" + selectedMonth);
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

    // Deletes the old chart if there is one, so that a new chart can be drawn
    if (Chart.getChart(canvas)) {
        Chart.getChart(canvas).destroy();
    }

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
    const response = await fetch("/api/summary/by-category?month=" + selectedMonth);
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

        // Deletes the old chart if there is one, so that a new chart can be drawn
    if (Chart.getChart(canvas)) {
        Chart.getChart(canvas).destroy();
    }

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
        options: {
            scales: {
                y: {
                    title: {
                        display: true,
                        text: "EUR",
                    },
                },
            },
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
        options: {
            scales: {
                y: {
                    title: {
                        display: true,
                        text: "EUR",
                    },
                },
            },
        },
    });
}
    
// Fetches the budgets and monthly spending and draws the overall budget chart
async function loadOverallBudgetChart() {
    const budgetsResponse = await fetch("/api/budgets?month=" + selectedMonth);
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

        if (entry.month === selectedMonth) {
            spentCents = Math.abs(entry.expenses_cents);
        }
    }

    const spentEuros = spentCents / 100;
    const remainingEuros = Math.max(0, (overallLimitCents - spentCents) /100);

    // Finds the canvas element and draws the pie chart
    const canvas = document.querySelector("#overall-budget-chart");

        // Deletes the old chart if there is one, so that a new chart can be drawn
    if (Chart.getChart(canvas)) {
        Chart.getChart(canvas).destroy();
    }

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
    const budgetsResponse = await fetch("/api/budgets?month=" + selectedMonth);
    const budgets = await budgetsResponse.json();

    const categoryResponse = await fetch("/api/summary/by-category?month=" + selectedMonth);
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

    // Deletes the old chart if there is one, so that a new chart can be drawn
    if (Chart.getChart(canvas)) {
        Chart.getChart(canvas).destroy();
    }

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
        options: {
            scales: {
                y: {
                    title: {
                        display: true,
                        text: "EUR",
                    },
                },
            },
        },
    });
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
    const canvas = document.querySelector("#networth-chart");

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

// Fetches all categories and fills the dropdown
async function loadBudgetCategoryOptions() {
    const response = await fetch ("/api/categories");
    const categories = await response.json();

    // Finds the select element where the options will be inserted
    const categorySelect = document.querySelector("#budget-category");
    
    for (let i = 0; i < categories.length; i++) {
        const category = categories[i];

        // Skip income categories
        if (category.kind === "income") {
            continue;
        }

        const option = document.createElement("option");
        option.value = category.id;
        option.textContent = category.name;

        categorySelect.appendChild(option);
    }
}

// Handles submitting the budget form
document.querySelector("#set-budget-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const categoryId = document.querySelector("#budget-category").value;

    let categoryIdToSend = categoryId;
    if (categoryId === "") {
        categoryIdToSend = null;
    }

    const newBudget = {
        month: selectedMonth,
        limit_cents: Math.round(document.querySelector("#budget-limit").value * 100),
        category_id: categoryIdToSend,
    };

    const response = await fetch("/api/budgets", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newBudget)
    });

    const result = await response.json();

    // Shows the error message if something went wrong
    if (result.error) {
        showMessage(result.error, true);
        return;
    }

    // Shows the success message if the budget was set successfully
    showMessage(result.message, false);
    document.querySelector("#set-budget-form").reset();
    loadOverallBudgetChart();
    loadCategoryBudgetChart();

    });
