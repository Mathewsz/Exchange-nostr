import { useState, useEffect, useCallback } from 'react';

interface WebSocketHook {
  sendMessage: (message: any) => void;
  lastMessage: any;
  readyState: number;
  error: Error | null;
}

export const useWebSocket = (url: string): WebSocketHook => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const [error, setError] = useState<Error | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CONNECTING);

  useEffect(() => {
    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        setSocket(ws);
        setReadyState(WebSocket.OPEN);
      };

      ws.onmessage = (event) => {
        try {
          const parsedMessage = JSON.parse(event.data);
          setLastMessage(parsedMessage);
        } catch (parseError) {
          console.error('Erro ao parsear mensagem WebSocket:', parseError);
        }
      };

      ws.onerror = (errorEvent) => {
        console.error('WebSocket error:', errorEvent);
        setError(new Error('WebSocket connection error'));
        setReadyState(WebSocket.CLOSED);
      };

      ws.onclose = (event) => {
        console.log('WebSocket closed:', event);
        setSocket(null);
        setReadyState(WebSocket.CLOSED);
      };

      return () => {
        ws.close();
      };
    } catch (connectionError) {
      console.error('Erro ao conectar WebSocket:', connectionError);
      setError(connectionError instanceof Error ? connectionError : new Error(String(connectionError)));
      return () => {};
    }
  }, [url]);

  const sendMessage = useCallback((message: any) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket não está aberto. Não foi possível enviar mensagem.');
    }
  }, [socket]);

  return {
    sendMessage,
    lastMessage,
    readyState,
    error
  };
};

export const NostrWebSocketService = {
  TRADE_SOCKET_URL: process.env.REACT_APP_TRADE_WEBSOCKET_URL || 'ws://localhost:8000/ws/trade',
  
  createTradeConnection: (userPubkey: string) => {
    const { sendMessage, lastMessage, readyState, error } = useWebSocket(
      `${NostrWebSocketService.TRADE_SOCKET_URL}?pubkey=${userPubkey}`
    );

    return {
      sendOrder: (orderData: any) => sendMessage({
        ...orderData,
        userPubkey
      }),
      lastTrade: lastMessage,
      connectionStatus: readyState,
      error
    };
  }
};
