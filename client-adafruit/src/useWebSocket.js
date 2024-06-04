import { useState, useEffect, useRef } from 'react';

function useWebSocket(url, onMessage) {
    const [socket, setSocket] = useState(null);
    const socketRef = useRef(null);

    useEffect(() => {
        // Create WebSocket connection.
        const webSocket = new WebSocket(url);

        // Store WebSocket reference to use for cleanup
        socketRef.current = webSocket;

        // Set socket state
        setSocket(webSocket);

        // Define WebSocket event listeners
        webSocket.onopen = () => {
            console.log('WebSocket Connected');
        };

        webSocket.onmessage = (event) => {
            console.log('Message from server ', event.data);
            if (onMessage) {
                onMessage(event.data);
            }
        };

        webSocket.onerror = (error) => {
            console.error('WebSocket Error ', error);
            console.log("Closing the socket.");
            webSocket.close();
        };

        webSocket.onclose = () => {
            console.log('WebSocket Disconnected');
            // Automatically try to reconnect on connection loss
            setTimeout(function() {
                console.log("Reconnecting...");
                setSocket(new WebSocket(url));
            }, 2000);
        };

        // Cleanup function
        // return () => {
        //     if (socketRef.current) {
        //         socketRef.current.close();
        //     }
        // };

    }, [url. onMessage]); // Re-run this effect if the URL changes

    return socketRef.current;
}

export default useWebSocket;
