document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const chatMessages = document.getElementById('chat-messages');
    const textInput = document.getElementById('text-input');
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');
    let isRecording = false;

    // WebSocket event handlers
    socket.on('connect', () => {
        addMessage('JARVIS is online and ready to assist you.', 'jarvis');
    });

    socket.on('jarvis_response', (data) => {
        addMessage(data.text, 'jarvis');
    });

    socket.on('error', (data) => {
        addMessage('Error: ' + data.message, 'jarvis');
    });

    // UI event handlers
    sendBtn.addEventListener('click', sendMessage);
    textInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    voiceBtn.addEventListener('click', toggleVoiceRecording);

    function sendMessage() {
        const message = textInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            socket.emit('text_input', { text: message });
            textInput.value = '';
        }
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function toggleVoiceRecording() {
        if (!isRecording) {
            startVoiceRecording();
        } else {
            stopVoiceRecording();
        }
    }

    function startVoiceRecording() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onstart = () => {
                isRecording = true;
                voiceBtn.style.background = 'var(--accent-color)';
            };

            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                addMessage(text, 'user');
                socket.emit('voice_input', { text: text });
            };

            recognition.onend = () => {
                isRecording = false;
                voiceBtn.style.background = 'var(--primary-color)';
            };

            recognition.start();
        } else {
            addMessage('Voice recognition is not supported in your browser.', 'jarvis');
        }
    }

    function stopVoiceRecording() {
        // The recognition will automatically stop when it detects the end of speech
        isRecording = false;
        voiceBtn.style.background = 'var(--primary-color)';
    }
}); 