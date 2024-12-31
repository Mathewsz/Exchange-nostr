from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from nostr.event import Event
from nostr.relay_manager import RelayManager
from typing import List, Dict

class NostrExchange:
    def __init__(self):
        self.app = FastAPI()
        self.relay_manager = RelayManager()
        self.active_connections: List[WebSocket] = []
        self.order_book: Dict = {
            'bids': [],
            'asks': []
        }
        
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.websocket("/ws/trade")
        async def websocket_trade(websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)
            try:
                while True:
                    data = await websocket.receive_json()
                    await self.process_trade_event(data)
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
    
    async def process_trade_event(self, event_data: Dict):
        # Lógica de processamento de ordens usando Nostr
        nostr_event = Event(
            pubkey=event_data.get('pubkey'),
            kind=event_data.get('kind', 1),
            content=str(event_data)
        )
        self.relay_manager.publish(nostr_event)

nostr_exchange = NostrExchange()
app = nostr_exchange.app
