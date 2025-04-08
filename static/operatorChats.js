document.addEventListener("DOMContentLoaded", function () {
  const chatsList = document.getElementById("chatsList");

  function fetchAllChats() {
    fetch("/get_all_chats", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((userIds) => {
        chatsList.innerHTML = "";
        userIds.forEach((userId) => {
          const chatElement = document.createElement("div");
          chatElement.className = "chat-item";
          chatElement.innerHTML = `<a href="/operator_chat/${userId}" class="h3">Чат с пользователем ${userId}</a>`;
          chatsList.appendChild(chatElement);
        });
      });
  }

  fetchAllChats();
});
