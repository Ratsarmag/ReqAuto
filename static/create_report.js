document.addEventListener("DOMContentLoaded", function () {
  const reportForm = document.getElementById("report-form");
  const requestIdInput = document.getElementById("report-request-id");
  const draftBlock = document.getElementById("draft-block");

  // Загрузка черновика из localStorage
  function loadDraft() {
    const draft = localStorage.getItem(`report_draft_${requestIdInput.value}`);
    if (draft) {
      const data = JSON.parse(draft);
      Object.keys(data).forEach((key) => {
        const field = document.getElementById(`report-${key}`);
        if (field) {
          field.value = data[key];
        }
      });
      draftBlock.innerHTML = `<p>Черновик загружен.</p>`;
    }
  }

  // Сохранение черновика в localStorage
  function saveDraft() {
    const data = {
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
    localStorage.setItem(
      `report_draft_${requestIdInput.value}`,
      JSON.stringify(data)
    );
    draftBlock.innerHTML = `<p>Черновик сохранен.</p>`;
  }

  // Отправка отчета
  reportForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const requestId = requestIdInput.value;
    saveDraft(); // Сохранение черновика перед отправкой

    const data = {
      request_id: requestId,
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

    fetch("/submit_report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          alert("Отчет успешно отправлен!");
          window.location.href = "/mechanic_dashboard"; // Перенаправление на страницу механика
        }
      });
  });

  // Сохранение черновика при изменении полей
  reportForm.addEventListener("input", saveDraft);

  // Загрузка черновика при загрузке страницы
  loadDraft();
});
