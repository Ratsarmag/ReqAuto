document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/roles")
    .then((response) => response.json())
    .then((roles) => {
      const userRows = document.querySelectorAll(".admin-table tbody tr");
      userRows.forEach((row) => {
        const roleId = row.cells[4].textContent.trim();
        const roleName = roles.find((role) => role.ID == roleId).roleName;
        row.cells[4].textContent = roleName;
      });
    });
});

function deleteUser(userId) {
  const modal = document.getElementById("deleteModal");
  const confirmDelete = document.getElementById("confirmDelete");
  const cancelDelete = document.getElementById("cancelDelete");
  const closeBtn = modal.querySelector(".close");

  modal.style.display = "block";

  closeBtn.onclick = function () {
    modal.style.display = "none";
  };

  cancelDelete.onclick = function () {
    modal.style.display = "none";
  };

  confirmDelete.onclick = function () {
    fetch(`/delete_user/${userId}`, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          location.reload();
        } else {
          console.error("Ошибка при удалении пользователя:", data.message);
        }
      });
    modal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
}
