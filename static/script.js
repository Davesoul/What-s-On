// static/script.js
async function sendMessage() {
    const userInputElement = document.getElementById("user-input");
    const userInput = userInputElement.value.trim();
    if (!userInput) return;

    // Display user's message in chat box
//    displayMessage("You: " + userInput, "user-message");

    // Show typing indicator
    const typingIndicator = document.getElementById("typing-indicator");
    typingIndicator.style.display = "flex";

    // Send message to backend
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_input: userInput })
        });

        const data = await response.json();

        // Hide typing indicator
        typingIndicator.style.display = "none";
        displayMessage(data.response, "grid-item");
    } catch (error) {
        typingIndicator.style.display = "none";
        displayMessage("Error: Could not reach LLM", "bot-message");
    }

    // Clear input and re-enable button
    userInputElement.value = "";
}

//function displayMessage(text, className) {
//    const chatBox = document.getElementById("chat-box");
//    const messageElement = document.createElement("p");
//    messageElement.className = className;
//    const timeStamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
//    messageElement.textContent = text;
//    messageElement.setAttribute("data-time", timeStamp);
//    chatBox.appendChild(messageElement);
//
//    // Smooth scroll to the bottom of the chat box
//    chatBox.scrollTop = chatBox.scrollHeight;
//}
document.addEventListener("DOMContentLoaded", () => {
  const body = document.getElementsByTagName('body')[0];
const userInputElement0 = document.getElementById("user-input");
const userInput0 = userInputElement0.value.trim();

body.addEventListener("keydown", (event) => {
  if (event.key === "/") {
    userInputElement0.focus();
    console.log(userInput0); // Perform the desired action with the trimmed input
  }
});

userInputElement0.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    const userInput0 = userInputElement0.value.trim();
    console.log(userInput0); // Perform the desired action with the trimmed input
  }
});

});

function displayMessage(text, className) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("p");
    messageElement.className = className;
    const timeStamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    messageElement.textContent = text;
    speakResponse(text)
    messageElement.setAttribute("data-time", timeStamp);
    chatBox.appendChild(messageElement);

    // Smooth scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;

    adjustGridSizes()


}


function adjustGridSizes() {
    const gridItems = document.querySelectorAll('.grid-item');

    gridItems.forEach(item => {
        // Calculate size based on content length
        const contentLength = item.textContent.length;
        if (contentLength > 100) {
            item.style.gridColumn = "span 2"; // Makes the item span 2 columns
        } else if (contentLength > 200) {
            item.style.gridColumn = "span 3"; // Spans 3 columns
        } else {
            item.style.gridColumn = "span 1"; // Default size
        }
    });
}

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';

// Handle Speech Synthesis
function speakResponse(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
}