async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");

  const userText = input.value;
  if (!userText) return;

  chatBox.innerHTML += `<p><b>You:</b> ${userText}</p>`;
  input.value = "";

  const response = await fetch("https://krishna-ai-backend.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userText })
  });

  const data = await response.json();
  chatBox.innerHTML += `<p><b>Krishna:</b><br>${data.reply}</p>`;
}
