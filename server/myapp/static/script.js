let chatSocket = null;

function connect() {
    const chatSocket = new WebSocket('ws://'+ window.location.host+ '/ws/data/');
    
    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data.message;
        document.getElementById('temperature').textContent = message; // Adjust depending on message content
    }


    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}

connect();