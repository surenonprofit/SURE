document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' || event.keyCode === 13) {
      document.getElementById('send-button').click();
    }
  });

  function openChat() {
    const chatButton = document.querySelector('nav button');
    const chatModal = document.getElementById("chatModal");
    const rect = chatButton.getBoundingClientRect();
    chatModal.style.top = `${rect.bottom}px`;
    chatModal.style.right = `${window.innerWidth - rect.right}px`;
    chatModal.style.display = "block";
  }

  function closeChat() {
    document.getElementById("chatModal").style.display = "none";
  }

  async function sendMessage() {
    const messageInput = document.getElementById("chatInput");
    const message = messageInput.value.trim();
    if (message) {
      // Display user's message
      const chatBody = document.querySelector(".chat-modal-body");
      const userMessageElement = document.createElement("p");
      userMessageElement.textContent = `You: ${message}`;
      chatBody.appendChild(userMessageElement);
      
      // Scroll to the bottom
      chatBody.scrollTop = chatBody.scrollHeight;

      // Clear input
      messageInput.value = "";

      // Send message to API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
      });
      const data = await response.json();
      
      // Display bot's reply
      const botReplyElement = document.createElement("p");
      botReplyElement.textContent = `Bot: ${data.reply}`;
      chatBody.appendChild(botReplyElement);
      
      // Scroll to the bottom
      chatBody.scrollTop = chatBody.scrollHeight;
    }
  }