document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/repair-requests")
    .then((response) => response.json())
    .then((data) => {
      const container = document.getElementById("requests-container");
      data.forEach((request) => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
                        <p class="h2" style="font-weight: bold">Заявка #${request.id}</p>
                        <p class="h3" style="margin-top: 5px">Имя: ${request.firstName} ${request.lastName}</p>
                        <p class="h3" style="margin-top: 5px">Телефон: ${request.phone}</p>
                        <p class="h3" style="margin-top: 5px">Автомобиль: ${request.carMake} ${request.carModel}</p>
                        <p class="h3" style="margin-top: 5px">Описание проблемы: ${request.defectsDescription}</p>
                        <p class="h3" style="margin-top: 5px">Статус заявки: ${request.status}</p>
                        <button onclick="editRequest(${request.id})" class="button submit-button h3">Редактировать</button>
                        <button onclick="acceptRequest(${request.id})" class="button submit-button h3" style="margin-left: 10px">Принять в работу</button>
                    `;
        container.appendChild(card);
      });
    });
});

function editRequest(id) {}

function acceptRequest(id) {}
