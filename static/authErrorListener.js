document.addEventListener("DOMContentLoaded", function () {
  const authForm = document.querySelector("form");

  authForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    fetch("/auth-submit", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        if (result.status === "success") {
          window.location.href = result.redirect;
        } else {
          showError(result.message);
        }
      })
      .catch((error) => {
        console.error("Возникла проблема с операцией fetch:", error);
        showError("Произошла ошибка при отправке запроса");
      });
  });

  function showError(message) {
    const modal = document.getElementById("errorModal");
    const errorMessage = document.getElementById("errorMessage");

    modal.style.display = "block";
    errorMessage.textContent = message;

    const closeBtn = modal.querySelector(".close");
    closeBtn.onclick = function () {
      modal.style.display = "none";
    };

    window.onclick = function (event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };
  }
});
