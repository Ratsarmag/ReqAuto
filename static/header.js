document.addEventListener("DOMContentLoaded", function () {
  const nav = document.querySelector("nav ul");
  const toggleMenu = document.querySelector(".toggle-menu-button");
  const logo = document.querySelector(".logo");

  toggleMenu.addEventListener("click", function () {
    if (nav.style.display === "flex") {
      nav.style.display = "none";
      this.textContent = "☰";
      logo.style.order = "1";
    } else {
      nav.style.display = "flex";
      this.textContent = "✖";
      logo.style.order = "0";
    }
  });
});
