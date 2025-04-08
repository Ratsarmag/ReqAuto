document
  .getElementById("supportChatButton")
  .addEventListener("click", function () {
    const supportChat = document.getElementById("supportChat");
    if (supportChat.style.display === "block") {
      supportChat.style.display = "none";
    } else {
      supportChat.style.display = "block";
      fetchUserID();
    }
  });

document.getElementById("sendMessage").addEventListener("click", function () {
  const message = document.getElementById("chatInput").value;
  if (message.trim() !== "") {
    sendMessageToServer(message);
    addMessageToChat(message, "user-message");
    document.getElementById("chatInput").value = "";
  }
});

function addMessageToChat(message, className) {
  const chatBody = document.getElementById("chatBody");
  const messageElement = document.createElement("div");
  messageElement.textContent = message;
  messageElement.className = `chat-box ${className}`;
  chatBody.appendChild(messageElement);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function sendMessageToServer(message) {
  fetch("/send_message", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: userID,
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

function fetchMessages() {
  fetch(`/get_messages/${userID}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((messages) => {
      const chatBody = document.getElementById("chatBody");
      chatBody.innerHTML = "";
      messages.forEach((message) => {
        addMessageToChat(
          message.message,
          message.operator_id ? "operator-message" : "user-message"
        );
      });
    });
}

function fetchUserID() {
  fetch("/get_user_id", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      userID = data.user_id;
      fetchMessages();
    });
}

let userID;
