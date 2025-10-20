document.addEventListener('DOMContentLoaded', () => {
    const bubble = document.getElementById('chatbot-bubble');
    const chatbotWindow = document.getElementById('chatbot-window');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');
    const messagesContainer = document.getElementById('chatbot-messages');

    // --- Constants for Session Storage ---
    const CHAT_HISTORY_KEY = 'chatbot_history';
    const CHAT_WINDOW_STATE_KEY = 'chatbot_window_state';

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

    // --- Function to reset backend conversation state ---
    const resetBackendConversation = async () => {
        try {
            await fetch('/chatbot/api/reset_chatbot_session/', {
                method: 'POST',
                headers: {
                    // CSRF token is not needed if view is csrf_exempt
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });
        } catch (error) {
            console.error('Error resetting chatbot session:', error);
        }
    };

    // --- Chat History Management ---
    const getChatHistory = () => JSON.parse(sessionStorage.getItem(CHAT_HISTORY_KEY)) || [];
    const saveChatHistory = (history) => sessionStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(history));

    // Function to fetch the welcome message
    const fetchWelcomeMessage = async () => {
        try {
            const response = await fetch('/chatbot/api/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ message: 'Hola' }) // Trigger the "saludo" intent
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            addMessage(data.response, 'bot', data.suggestions);

        } catch (error) {
            console.error("Error fetching welcome message:", error);
            addMessage("Hola, bienvenido. No pude cargar las sugerencias iniciales.", 'bot');
        }
    };

    // Toggle chat window and save state
    const toggleWindow = () => {
        const isOpening = chatbotWindow.classList.contains('hidden');
        chatbotWindow.classList.toggle('hidden');
        bubble.classList.toggle('hidden');

        if (isOpening) {
            sessionStorage.setItem(CHAT_WINDOW_STATE_KEY, 'open');
            if (getChatHistory().length === 0) {
                fetchWelcomeMessage();
            }
        } else {
            sessionStorage.setItem(CHAT_WINDOW_STATE_KEY, 'closed');
        }
    };

    bubble.addEventListener('click', toggleWindow);
    closeBtn.addEventListener('click', toggleWindow);

    // Reusable function to send a message
    const sendMessage = async (messageText) => {
        if (!messageText) return;

        addMessage(messageText, 'user');
        input.value = '';

        try {
            const response = await fetch('/chatbot/api/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ message: messageText })
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            addMessage(data.response, 'bot', data.suggestions);

        } catch (error) {
            console.error("Error fetching chatbot response:", error);
            addMessage("Lo siento, hubo un error al conectar con el servidor.", 'bot');
        }
    };

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        sendMessage(input.value.trim());
    });

    // Function to add a message to the UI and optionally save it to history
    function addMessage(message, sender, suggestions = [], isFromHistory = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chatbot-message', sender);
        messageElement.innerHTML = message;
        messagesContainer.appendChild(messageElement);

        const suggestionsContainer = document.getElementById('chatbot-suggestions') || createSuggestionsContainer();
        suggestionsContainer.innerHTML = '';

        if (suggestions && suggestions.length > 0) {
            suggestions.forEach(suggestionText => {
                const button = document.createElement('button');
                button.classList.add('suggestion-btn');
                button.textContent = suggestionText;
                button.addEventListener('click', () => sendMessage(suggestionText));
                suggestionsContainer.appendChild(button);
            });
        }

        if (!isFromHistory) {
            const history = getChatHistory();
            history.push({ message, sender, suggestions });
            saveChatHistory(history);
        }

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function createSuggestionsContainer() {
        const container = document.createElement('div');
        container.id = 'chatbot-suggestions';
        messagesContainer.parentNode.insertBefore(container, messagesContainer.nextSibling);
        return container;
    }

    // --- Load Chat State on Page Load ---
    function loadChatState() {
        const windowState = sessionStorage.getItem(CHAT_WINDOW_STATE_KEY);
        if (windowState === 'open') {
            chatbotWindow.classList.remove('hidden');
            bubble.classList.add('hidden');
        }

        const history = getChatHistory();
        if (history.length > 0) {
            history.forEach(item => {
                addMessage(item.message, item.sender, item.suggestions, true);
            });
        }
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // --- Initial setup ---
    resetBackendConversation(); // Reset backend state on every page load
    loadChatState(); // Load frontend state from session storage
});