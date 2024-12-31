from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List, Dict

from .nostr_integration import NostrExchangeClient, NostrOrderBook
from .routes import router as api_router
from .config import settings

class NostrDecentralizedExchange:
    def __init__(self):
        self.app = FastAPI(
            title="Nostr Decentralized Exchange",
            description="Descentralized crypto exchange using Nostr protocol"
        )
        
        # Configurações CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Adicionar rotas
        self.app.include_router(api_router, prefix="/api/v1")
        
        # Componentes Nostr
        self.nostr_client = NostrExchangeClient(settings.NOSTR_RELAYS)
        self.order_book = NostrOrderBook()
        
        # WebSocket para ordens em tempo real
        self.active_connections: List[WebSocket] = []
        
        # Configurar rotas WebSocket
        self.setup_websocket_routes()
    
    def setup_websocket_routes(self):
        @self.app.websocket("/ws/trade")
        async def websocket_trade(websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)
            
            try:
                while True:
                    data = await websocket.receive_json()
                    await self.process_trade_event(data, websocket)
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
    
    async def process_trade_event(self, event_data: Dict, websocket: WebSocket):
        """
        Processar eventos de trade via WebSocket
        
        :param event_data: Dados do evento
        :param websocket: Conexão WebSocket
        """
        try:
            # Adicionar ordem ao livro de ordens
            self.order_book.add_order(event_data)
            
            # Tentar casar ordens
            trades = self.order_book.match_orders()
            
            if trades:
                # Notificar todos os clientes conectados sobre trades
                for conn in self.active_connections:
                    await conn.send_json({"trades": trades})
                
                # Publicar trades no Nostr
                for trade in trades:
                    await self.nostr_client.publish_order(
                        trade, 
                        private_key=event_data.get('private_key', '')
                    )
        
        except Exception as e:
            await websocket.send_json({"error": str(e)})
    
    async def start_nostr_listener(self, user_pubkey: str):
        """
        Iniciar listener de ordens do Nostr para um usuário
        
        :param user_pubkey: Chave pública do usuário
        """
        await self.nostr_client.connect()
        
        async for event in self.nostr_client.listen_for_orders(user_pubkey):
            # Processar eventos de ordem do Nostr
            order_data = event.content
            self.order_book.add_order(order_data)

# Instância global da exchange
nostr_exchange = NostrDecentralizedExchange()
app = nostr_exchange.app

# Inicialização assíncrona
@app.on_event("startup")
async def startup_event():
    # Você pode adicionar lógica de inicialização aqui
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Fechar conexões Nostr
    nostr_exchange.nostr_client.close()
