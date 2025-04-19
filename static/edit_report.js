document.addEventListener("DOMContentLoaded", function () {
  const reportForm = document.getElementById("report-form");
  const reportIdInput = document.getElementById("report-id");

  reportForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const data = {
      id: reportIdInput.value,
      description: document.getElementById("report-description").value,
      diagnostics: document.getElementById("report-diagnostics").value,
      materials: document.getElementById("report-materials").value,
      tools_used: document.getElementById("report-tools").value,
      complexity: document.getElementById("report-complexity").value,
      total_cost: document.getElementById("report-total-cost").value,
      recommendations: document.getElementById("report-recommendations").value,
      before_photos: document.getElementById("report-before-photos").value,
      after_photos: document.getElementById("report-after-photos").value,
      mechanic_comments: document.getElementById("report-mechanic-comments")
        .value,
    };

    fetch("/update_report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          alert("Отчет успешно сохранен!");
          window.location.href = "/mechanic_reports";
        }
      });
  });
});
