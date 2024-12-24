function submitRegistrationForm() {
  $.ajax({
    type: "POST",
    url: "/register",
    data: $("#registration-form").serialize(),
    success: function (response) {
      if (response.status === "success") {
        // Показываем сообщение об успехе
        showMessage(response.message);

        // Перенаправляем пользователя на страницу авторизации
        setTimeout(function () {
          window.location.href = response.redirect_url;
        }, 2000); // Ждем 2 секунды перед перенаправлением
      } else {
        // Обработка ошибок
        showMessage(response.message, "error");
      }
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
      showMessage("Произошла ошибка при регистрации.", "error");
    },
  });
}
