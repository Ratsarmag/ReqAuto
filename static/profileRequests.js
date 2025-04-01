document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/user-repair-requests")
    .then((response) => response.json())
    .then((data) => {
      displayRequests(data);
    })
    .catch((error) => console.error("Ошибка при загрузке заявок:", error));
});

function displayRequests(requests) {
  const container = document.getElementById("requests-container");
  container.innerHTML = "";
  requests.forEach((request) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
            <p class="h2" style="font-weight: bold">Заявка #${
              request.number
            }</p>
            <p class="h3" style="margin-top: 5px">Имя: ${request.firstName} ${
      request.lastName
    }</p>
            <p class="h3" style="margin-top: 5px">Телефон: ${request.phone}</p>
            <p class="h3" style="margin-top: 5px">Автомобиль: ${
              request.carMake
            } ${request.carModel}</p>
            <p class="h3" style="margin-top: 5px">Описание проблемы: ${
              request.defectsDescription
            }</p>
            <p class="h3" style="margin-top: 5px">Статус заявки: ${getStatusColor(
              request.status
            )}</p>
            <p class="h3" style="margin-top: 5px">Дата создания: ${new Date(
              request.created_at
            ).toLocaleString()}</p>
            ${
              request.accepted_at
                ? `<p class="h3" style="margin-top: 5px">Дата принятия в работу: ${new Date(
                    request.accepted_at
                  ).toLocaleString()}</p>`
                : ""
            }
            ${
              request.completed_at
                ? `<p class="h3" style="margin-top: 5px">Дата завершения: ${new Date(
                    request.completed_at
                  ).toLocaleString()}</p>`
                : ""
            }
        `;
    container.appendChild(card);
  });
}

function getStatusColor(statusText) {
  const colors = {
    "новая заявка": "blue",
    "в работе": "#ff9640",
    завершена: "#004D00",
  };

  const color = colors[statusText.toLowerCase()] || "black";

  return `<span style="color: ${color}">${statusText}</span>`;
}
