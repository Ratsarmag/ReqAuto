document.addEventListener("DOMContentLoaded", function () {
  const notificationsToggle = document.getElementById("notifications-toggle");
  const notificationsContainer = document.getElementById(
    "notifications-container"
  );

  notificationsToggle.addEventListener("click", function () {
    if (
      notificationsContainer.style.display === "none" ||
      notificationsContainer.style.display === ""
    ) {
      notificationsContainer.style.display = "block";
      markAllAsRead(); // Пометить все уведомления как прочитанные
      loadNotifications();
    } else {
      notificationsContainer.style.display = "none";
    }
  });

  function toSentenceCase(text) {
    return text
      .split(". ")
      .map((sentence) => {
        return (
          sentence.charAt(0).toUpperCase() + sentence.slice(1).toLowerCase()
        );
      })
      .join(". ");
  }

  function loadNotifications() {
    fetch("/api/notifications")
      .then((response) => response.json())
      .then((data) => {
        notificationsContainer.innerHTML = "";
        data.forEach((notification) => {
          const notificationElement = document.createElement("div");
          notificationElement.className = "notification";

          const date = new Date(notification.created_at);
          const options = { hour: "2-digit", minute: "2-digit" };
          const formattedTime = date.toLocaleTimeString(undefined, options);
          const formattedMessage = toSentenceCase(notification.message);

          notificationElement.innerHTML = `
                    <span>${formattedMessage}</span>
                    <span class="notification-time">${formattedTime}</span>
                `;

          if (!notification.read) {
            const indicator = document.createElement("span");
            indicator.className = "unread-indicator";
            notificationElement.appendChild(indicator);
          }

          notificationsContainer.appendChild(notificationElement);
        });
      });
  }

  function markAllAsRead() {
    fetch("/api/notifications/mark-all-as-read", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      if (!response.ok) {
        console.error("Ошибка при пометке уведомлений как прочитанных");
      }
    });
  }
});
