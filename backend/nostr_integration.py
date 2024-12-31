import json
import asyncio
from typing import Dict, Any, List
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.message_pool import MessagePool

class NostrExchangeClient:
    def __init__(self, relays: List[str] = None):
        self.relay_manager = RelayManager()
        self.message_pool = MessagePool()
        
        # Relays padrão se não forem especificados
        relays = relays or [
            "wss://relay.damus.io",
            "wss://relay.nostr.band",
            "wss://nostr.wine"
        ]
        
        # Adicionar relays
        for relay in relays:
            self.relay_manager.add_relay(relay)
        
        # Configurações de eventos
        self.order_kind = 30000  # Kind customizado para ordens
        self.trade_kind = 30001  # Kind customizado para trades
    
    async def connect(self):
        """Conectar a todos os relays"""
        self.relay_manager.open_connections()
        await asyncio.sleep(1.5)  # Tempo para estabelecer conexões
    
    def create_order_event(self, order_data: Dict[str, Any], private_key: str) -> Event:
        """
        Criar evento Nostr para uma ordem de troca
        
        :param order_data: Dicionário com dados da ordem
        :param private_key: Chave privada do usuário para assinar
        :return: Evento Nostr
        """
        event = Event(
            kind=self.order_kind,
            content=json.dumps(order_data),
            tags=[
                ['p', order_data.get('user_pubkey', '')],  # Pubkey do usuário
                ['t', order_data.get('pair', '')],  # Par de trading
                ['a', str(order_data.get('amount', 0))],  # Quantidade
                ['pr', str(order_data.get('price', 0))],  # Preço
                ['type', order_data.get('type', 'buy')]  # Tipo de ordem
            ]
        )
        event.sign(private_key)
        return event
    
    async def publish_order(self, order_data: Dict[str, Any], private_key: str):
        """
        Publicar ordem em todos os relays
        
        :param order_data: Dados da ordem
        :param private_key: Chave privada para assinatura
        """
        order_event = self.create_order_event(order_data, private_key)
        
        # Publicar em todos os relays
        for relay in self.relay_manager.relays:
            self.relay_manager.publish_event(order_event, relay)
        
        await asyncio.sleep(1)  # Tempo para propagação
    
    async def listen_for_orders(self, user_pubkey: str):
        """
        Escutar ordens relacionadas a um usuário específico
        
        :param user_pubkey: Chave pública do usuário
        :return: Generator de eventos de ordem
        """
        # Filtro para ordens do usuário
        subscription = {
            "kinds": [self.order_kind],
            "authors": [user_pubkey]
        }
        
        self.relay_manager.add_subscription("user_orders", subscription)
        
        while True:
            msg = await self.message_pool.get()
            # Processar mensagens de ordens
            if msg.type == "EVENT":
                event = msg.event
                if event.kind == self.order_kind:
                    yield event
    
    def close(self):
        """Fechar conexões com relays"""
        self.relay_manager.close_connections()

class NostrOrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
    
    def add_order(self, order: Dict[str, Any]):
        """Adicionar ordem ao livro de ordens"""
        if order['type'] == 'buy':
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda x: x['price'], reverse=True)
        else:
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda x: x['price'])
    
    def match_orders(self):
        """
        Tentar casar ordens de compra e venda
        
        :return: Lista de trades realizados
        """
        trades = []
        
        # Lógica simples de casamento de ordens
        while self.buy_orders and self.sell_orders:
            best_buy = self.buy_orders[0]
            best_sell = self.sell_orders[0]
            
            if best_buy['price'] >= best_sell['price']:
                # Ordem casada
                trade_amount = min(best_buy['amount'], best_sell['amount'])
                trade_price = best_sell['price']
                
                trade = {
                    'buyer_pubkey': best_buy['user_pubkey'],
                    'seller_pubkey': best_sell['user_pubkey'],
                    'amount': trade_amount,
                    'price': trade_price
                }
                trades.append(trade)
                
                # Atualizar quantidades
                best_buy['amount'] -= trade_amount
                best_sell['amount'] -= trade_amount
                
                # Remover ordens completamente executadas
                if best_buy['amount'] == 0:
                    self.buy_orders.pop(0)
                if best_sell['amount'] == 0:
                    self.sell_orders.pop(0)
            else:
                break
        
        return trades
