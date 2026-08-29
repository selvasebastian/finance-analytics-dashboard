// Runs when the pag is loaded
document.addEventListener("DOMContentLoaded", function () {
    loadCategoryChart();
});

// Fetches the category summary and draws a pie chart
async function loadCategoryChart() {
    const response = await fetch("/api/summary/by-category?month=2026-08");
    const summary = await response.json();

    const labels = [];
    const values = [];

    for (let i = 0; i < summary.length; i++) {
        const entry = summary[i];

        // This chart should only show the spending categories
        if (entry.category === "Income") {
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