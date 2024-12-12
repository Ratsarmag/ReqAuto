let allRequests = [];

document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/repair-requests")
    .then((response) => response.json())
    .then((data) => {
      allRequests = data;
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
    card.id = `request-${request.id}`;
    card.innerHTML = `
      <p class="h2" style="font-weight: bold">Заявка #${request.id}</p>
      <p class="h3" style="margin-top: 5px">Имя: ${request.firstName} ${
      request.lastName
    }</p>
      <p class="h3" style="margin-top: 5px">Телефон: ${request.phone}</p>
      <p class="h3" style="margin-top: 5px">Автомобиль: ${request.carMake} ${
      request.carModel
    }</p>
      <p class="h3" style="margin-top: 5px">Описание проблемы: ${
        request.defectsDescription
      }</p>
      <p class="h3" style="margin-top: 5px">Статус заявки: ${getStatusColor(
        request.status
      )}</p>
      <button onclick="editRequest(${
        request.id
      })" class="button submit-button h3">Редактировать</button>
      ${
        request.isAccepted
          ? ""
          : `<button id="accept-request-${request.id}" onclick="acceptRequest(${request.id})" class="button submit-button h3">Принять в работу</button>`
      }
    `;
    container.appendChild(card);
  });
}

function filterRequests() {
  const query = document.getElementById("searchInput").value.toLowerCase();
  let filteredRequests = [];

  if (query.includes("№") || query.includes("#")) {
    const requestNumber = query.match(/№(\d+)|#(\d+)/);
    if (requestNumber) {
      const number = requestNumber[1] || requestNumber[2];
      filteredRequests = allRequests.filter(
        (request) => request.id.toString() === number
      );
    }
  } else {
    filteredRequests = allRequests.filter((request) => {
      return (
        request.firstName.toLowerCase().includes(query) ||
        request.lastName.toLowerCase().includes(query) ||
        request.phone.toLowerCase().includes(query) ||
        request.carMake.toLowerCase().includes(query) ||
        request.carModel.toLowerCase().includes(query) ||
        request.defectsDescription.toLowerCase().includes(query)
      );
    });
  }
  displayRequests(filteredRequests);
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

function editRequest(id) {
  fetch(`/api/repair-requests/${id}`)
    .then((response) => response.json())
    .then((data) => {
      const modal = document.getElementById("editModal");
      const form = document.getElementById("editForm");
      const closeBtn = modal.querySelector(".close");

      document.getElementById("editRequestId").value = id;
      document.getElementById("editFirstName").value = data.firstName;
      document.getElementById("editLastName").value = data.lastName;
      document.getElementById("editPhone").value = data.phone;

      fetch(`/api/car-make/${data.carMakeID}`)
        .then((response) => response.json())
        .then((carMakeData) => {
          document.getElementById("editCarMake").value = carMakeData.carMake;
        });

      fetch(`/api/car-model/${data.carModelID}`)
        .then((response) => response.json())
        .then((carModelData) => {
          document.getElementById("editCarModel").value = carModelData.carModel;
        });

      document.getElementById("editDefectsDescription").value =
        data.defectsDescription;

      modal.style.display = "block";

      closeBtn.onclick = function () {
        modal.style.display = "none";
      };

      window.onclick = function (event) {
        if (event.target == modal) {
          modal.style.display = "none";
        }
      };

      form.onsubmit = function (event) {
        event.preventDefault();
        const formData = new FormData(form);
        fetch(`/api/repair-requests/${id}/edit`, {
          method: "POST",
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              modal.style.display = "none";
              const card = document.getElementById(`request-${id}`);
              if (card) {
                card.querySelector(".request-id").textContent = `Заявка #${id}`;
                card.querySelector("h2").textContent = `${formData.get(
                  "firstName"
                )} ${formData.get("lastName")}`;
                card.querySelector(
                  "p:nth-of-type(1)"
                ).textContent = `Phone: ${formData.get("phone")}`;
                card.querySelector(
                  "p:nth-of-type(2)"
                ).textContent = `Car: ${formData.get("carMake")} ${formData.get(
                  "carModel"
                )}`;
                card.querySelector(
                  "p:nth-of-type(3)"
                ).textContent = `Defects: ${formData.get(
                  "defectsDescription"
                )}`;
              }
            } else {
              console.error("Не удалось редактировать заявку:", data.message);
            }
          });
      };
    });
}

function acceptRequest(id) {
  const modal = document.getElementById("assignModal");
  const form = document.getElementById("assignForm");
  const closeBtn = modal.querySelector(".close");
  const mechanicSelect = document.getElementById("assignMechanic");

  document.getElementById("assignRequestId").value = id;

  fetch("/api/mechanics")
    .then((response) => response.json())
    .then((data) => {
      mechanicSelect.innerHTML = '<option value="">Выберите механика</option>';
      data.forEach((mechanic) => {
        const option = document.createElement("option");
        option.value = mechanic.ID;
        option.textContent = `${mechanic.firstName} ${mechanic.lastName}`;
        mechanicSelect.appendChild(option);
      });
    });

  modal.style.display = "block";

  closeBtn.onclick = function () {
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

  form.onsubmit = function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    fetch(`/api/repair-requests/${id}/accept`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          modal.style.display = "none";
          const card = document.getElementById(`request-${id}`);
          if (card) {
            card.querySelector(
              ".request-status"
            ).textContent = `Статус: ${data.new_status}`;
            const acceptButton = document.getElementById(
              `accept-request-${id}`
            );
            if (acceptButton) {
              acceptButton.remove();
            }
          }
        } else {
          console.error("Не удалось принять заявку в работу:", data.message);
        }
      });
  };
}
