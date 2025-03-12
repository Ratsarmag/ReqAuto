function submitRegistrationForm() {
  $.ajax({
    type: "POST",
    url: "/register",
    data: $("#registration-form").serialize(),
    success: function (response) {
      if (response.status === "success") {
        showMessage(response.message);
        setTimeout(function () {
          window.location.href = response.redirect_url;
        }, 2000);
      } else {
        showMessage(response.message, "error");
      }
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
      showMessage("Произошла ошибка при регистрации.", "error");
    },
  });
}
