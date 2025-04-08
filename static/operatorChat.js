document.addEventListener("DOMContentLoaded", function () {
  const chatContainer = document.getElementById("chatContainer");
  const operatorInput = document.getElementById("operatorInput");
  const user_id = chatContainer.getAttribute("data-user-id");

  function fetchMessages() {
    fetch(`/get_messages/${user_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((messages) => {
        chatContainer.innerHTML = "";
        messages.forEach((message) => {
          addMessageToChat(message);
        });
      });
  }

  document
    .getElementById("sendOperatorMessage")
    .addEventListener("click", function () {
      const message = operatorInput.value;
      if (message.trim() !== "") {
        sendMessageToServer(message);
        addMessageToChat({
          user_id: user_id,
          operator_id: true,
          message: message,
          timestamp: new Date().toISOString(),
        });
        operatorInput.value = "";
      }
    });

  function addMessageToChat(message) {
    const messageElement = document.createElement("div");
    messageElement.className = `message ${
      message.operator_id ? "operator-message" : "user-message"
    }`;

    const utcDate = new Date(message.timestamp);
    const mskDate = new Date(utcDate.getTime() + 3 * 60 * 60 * 1000);
    const formattedTime = mskDate.toLocaleString("ru-RU", {
      hour12: false,
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

    messageElement.innerHTML = `
            <p>${message.message}</p>
            <small>${formattedTime}</small>
        `;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function sendMessageToServer(message) {
    fetch("/send_message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: user_id,
        operator_id: true,
        message: message,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          fetchMessages();
        }
      });
  }

  fetchMessages();
});
