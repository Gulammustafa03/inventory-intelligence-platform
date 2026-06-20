document.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/dashboard/analytics/data");
  const data = await response.json();

  const colors = {
    green: "#7CEA9C",
    mint: "#55D6BE",
    blue: "#2E5EAA",
    grape: "#5B4E77",
    deep: "#593959",
    border: "#E5E7EB",
    text: "#0F172A",
    muted: "#64748B",
    warning: "#F59E0B",
    danger: "#EF4444",
    surface: "#FFFFFF",
  };

  Chart.defaults.color = colors.muted;
  Chart.defaults.font.family = "Inter, system-ui, sans-serif";
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.tooltip.backgroundColor = colors.text;
  Chart.defaults.plugins.tooltip.padding = 12;
  Chart.defaults.plugins.tooltip.cornerRadius = 12;

  const grid = {
    borderColor: colors.border,
    color: colors.border,
    drawTicks: false,
  };

  const makeChart = (id, config) => {
    const element = document.getElementById(id);
    if (!element) {
      return null;
    }
    return new Chart(element, config);
  };

  makeChart("categoryChart", {
    type: "bar",
    data: {
      labels: data.inventoryByCategory.labels,
      datasets: [{
        label: "Units",
        data: data.inventoryByCategory.values,
        borderRadius: 12,
        backgroundColor: [colors.green, colors.mint, colors.blue, colors.grape, colors.deep],
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { x: { grid: { display: false } }, y: { grid, border: { display: false } } },
    },
  });

  makeChart("quantityChart", {
    type: "line",
    data: {
      labels: data.productQuantities.labels.length ? data.productQuantities.labels : ["No products"],
      datasets: [{
        label: "Quantity",
        data: data.productQuantities.values.length ? data.productQuantities.values : [0],
        borderColor: colors.blue,
        backgroundColor: `${colors.mint}33`,
        fill: true,
        tension: .38,
        pointBackgroundColor: colors.green,
        pointBorderColor: colors.surface,
        pointBorderWidth: 3,
      }],
    },
    options: {
      responsive: true,
      scales: { x: { grid: { display: false } }, y: { grid, border: { display: false } } },
    },
  });

  makeChart("lowStockChart", {
    type: "doughnut",
    data: {
      labels: data.lowStockStats.labels,
      datasets: [{
        data: data.lowStockStats.values,
        backgroundColor: [colors.danger, colors.green],
        borderColor: colors.surface,
        borderWidth: 6,
        hoverOffset: 8,
      }],
    },
    options: {
      responsive: true,
      cutout: "72%",
    },
  });

  makeChart("monthlySalesChart", {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [{
        label: "Revenue",
        data: [18, 24, 21, 32, 36, 42],
        borderColor: colors.deep,
        backgroundColor: `${colors.green}33`,
        fill: true,
        tension: .4,
      }],
    },
    options: {
      responsive: true,
      scales: { x: { grid: { display: false } }, y: { grid, border: { display: false } } },
    },
  });

  makeChart("supplierChart", {
    type: "radar",
    data: {
      labels: ["Quality", "Speed", "Coverage", "Cost", "Reliability"],
      datasets: [{
        label: "Supplier SLA",
        data: [92, 84, 88, 76, 94],
        borderColor: colors.blue,
        backgroundColor: `${colors.mint}55`,
        pointBackgroundColor: colors.green,
      }],
    },
    options: {
      responsive: true,
      scales: { r: { grid: { color: colors.border }, angleLines: { color: colors.border } } },
    },
  });
});
