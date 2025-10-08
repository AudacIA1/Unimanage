document.addEventListener('DOMContentLoaded', () => {
    const bubble = document.getElementById('chatbot-bubble');
    const window = document.getElementById('chatbot-window');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');
    const messagesContainer = document.getElementById('chatbot-messages');

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Toggle chat window
    const toggleWindow = () => {
        window.classList.toggle('hidden');
        bubble.classList.toggle('hidden');
    };

    bubble.addEventListener('click', toggleWindow);
    closeBtn.addEventListener('click', toggleWindow);

    // Reusable function to send a message
    const sendMessage = async (messageText) => {
        if (!messageText) return;

        // Add user message to UI and clear suggestions
        addMessage(messageText, 'user');
        input.value = '';

        // Send message to backend
        try {
            const response = await fetch('/chatbot/api/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ message: messageText })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            // Add bot response to UI, now with suggestions
            addMessage(data.response, 'bot', data.suggestions);

        } catch (error) {
            console.error("Error fetching chatbot response:", error);
            addMessage("Lo siento, hubo un error al conectar con el servidor.", 'bot');
        }
    };

    // Handle form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        sendMessage(input.value.trim());
    });

    // Function to add a message to the chat window
    function addMessage(message, sender, suggestions = []) {
        // Add message bubble
        const messageElement = document.createElement('div');
        messageElement.classList.add('chatbot-message', sender);
        messageElement.innerHTML = message; // Use innerHTML to render HTML tags from the bot
        messagesContainer.appendChild(messageElement);

        // Handle suggestions
        let suggestionsContainer = document.getElementById('chatbot-suggestions');
        if (!suggestionsContainer) {
            suggestionsContainer = document.createElement('div');
            suggestionsContainer.id = 'chatbot-suggestions';
            // Insert after messages, before input
            messagesContainer.parentNode.insertBefore(suggestionsContainer, messagesContainer.nextSibling);
        }
        // Clear previous suggestions
        suggestionsContainer.innerHTML = '';

        if (suggestions && suggestions.length > 0) {
            suggestions.forEach(suggestionText => {
                const button = document.createElement('button');
                button.classList.add('suggestion-btn');
                button.textContent = suggestionText;
                button.addEventListener('click', () => {
                    sendMessage(suggestionText);
                });
                suggestionsContainer.appendChild(button);
            });
        }

        // Scroll to the bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});
