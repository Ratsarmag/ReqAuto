function getDayDeclension(number) {
  number = Math.abs(number) % 100;
  let declension;

  if (number >= 11 && number <= 19) {
    declension = "дней";
  } else {
    const lastDigit = number % 10;
    switch (lastDigit) {
      case 1:
        declension = "день";
        break;
      case 2:
      case 3:
      case 4:
        declension = "дня";
        break;
      default:
        declension = "дней";
    }
  }

  return declension;
}

document.addEventListener("DOMContentLoaded", function () {
  const avgCompletionTimeElement = document.getElementById("avgCompletionTime");
  if (avgCompletionTimeElement) {
    const avgCompletionTime = parseFloat(
      avgCompletionTimeElement.getAttribute("data-time")
    );
    const declension = getDayDeclension(avgCompletionTime);
    avgCompletionTimeElement.textContent = `${avgCompletionTime} ${declension}`;
  }
});
