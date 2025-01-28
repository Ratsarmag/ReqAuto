document.querySelector("form").addEventListener("submit", function (e) {
  e.preventDefault();

  const firstName = document.getElementById("firstName").value;
  const lastName = document.getElementById("lastName").value;
  const phone = document.getElementById("phone").value;

  if (!validateName(firstName)) {
    showError(
      "Имя",
      "Имя должно быть от 2 до 50 символов и содержать только буквы."
    );
  }

  if (!validateName(lastName)) {
    showError(
      "Фамилия",
      "Фамилия должна быть от 2 до 50 символов и содержать только буквы."
    );
  }

  if (!validatePhone(phone)) {
    showError(
      "Телефон",
      "Пожалуйста, введите корректный номер телефона (11 цифр, начинается с 7). Например, 79001231212"
    );
  }

  if (allFieldsValid()) {
    alert("Форма успешно отправлена");
    this.submit();
  }
});

function validateName(name) {
  return /^[а-яё]{2,50}$/i.test(name);
}

function validatePhone(phone) {
  return /^\d{11}$/.test(phone) && phone.startsWith("7");
}

function allFieldsValid() {
  return (
    validateName(document.getElementById("firstName").value) &&
    validateName(document.getElementById("lastName").value) &&
    validatePhone(document.getElementById("phone").value)
  );
}

function showError(field, message) {
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
