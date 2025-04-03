document.addEventListener("DOMContentLoaded", function () {
  const requestsByHourData = JSON.parse(
    document.getElementById("requestsByHourData").textContent
  );

  const labels = requestsByHourData.map((item) => item.hour + 3 + ":00");
  const data = requestsByHourData.map((item) => item.count);

  const trace = {
    x: labels,
    y: data,
    type: "bar",
  };

  const layout = {
    title: "Количество заявок по часам",
    xaxis: { title: "Часы" },
    yaxis: { title: "Количество заявок", range: [0, 50] },
  };

  Plotly.newPlot("requestsByHourChart", [trace], layout);
});
