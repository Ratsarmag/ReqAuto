document.addEventListener("DOMContentLoaded", function () {
  const carousel = document.getElementById("promotionsCarousel");
  const cards = document.querySelectorAll(".promotion-card");
  const indicatorContainer = document.getElementById("carouselIndicator");
  let currentIndex = 0;
  let interval;
  let isDragging = false;
  let startX, currentX;

  for (let i = 0; i < cards.length; i++) {
    const dot = document.createElement("div");
    dot.addEventListener("click", () => goToSlide(i));
    indicatorContainer.appendChild(dot);
  }

  updateIndicator();

  function showCard(index) {
    const translateX = -index * 100;
    cards.forEach((card) => {
      card.style.transform = `translateX(${translateX}%)`;
    });
    updateIndicator();
  }

  function goToSlide(index) {
    currentIndex = index;
    showCard(currentIndex);
  }

  function nextCard() {
    currentIndex = (currentIndex + 1) % cards.length;
    showCard(currentIndex);
  }

  function prevCard() {
    currentIndex = (currentIndex - 1 + cards.length) % cards.length;
    showCard(currentIndex);
  }

  function updateIndicator() {
    const dots = document.querySelectorAll(".carousel-indicator div");
    dots.forEach((dot, index) => {
      dot.classList.toggle("active", index === currentIndex);
    });
  }

  function startCarousel() {
    interval = setInterval(nextCard, 10000);
  }

  function stopCarousel() {
    clearInterval(interval);
  }

  function handleMouseDown(e) {
    isDragging = true;
    startX = e.clientX || e.touches[0].clientX;
    stopCarousel();
  }

  function handleMouseMove(e) {
    if (!isDragging) return;
    currentX = e.clientX || e.touches[0].clientX;
    const deltaX = currentX - startX;
    const threshold = 100; // Distance to trigger a swipe

    if (deltaX > threshold) {
      prevCard();
      isDragging = false;
      startCarousel();
    } else if (deltaX < -threshold) {
      nextCard();
      isDragging = false;
      startCarousel();
    }
  }

  function handleMouseUp() {
    if (isDragging) {
      isDragging = false;
      startCarousel();
    }
  }

  carousel.addEventListener("mousedown", handleMouseDown);
  carousel.addEventListener("touchstart", handleMouseDown);

  carousel.addEventListener("mousemove", handleMouseMove);
  carousel.addEventListener("touchmove", handleMouseMove);

  carousel.addEventListener("mouseup", handleMouseUp);
  carousel.addEventListener("touchend", handleMouseUp);

  startCarousel();
});
