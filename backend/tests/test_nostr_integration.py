import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from ..nostr_integration import NostrExchangeClient, NostrOrderBook

@pytest.mark.asyncio
async def test_nostr_client_initialization():
    """Testar inicialização do cliente Nostr"""
    client = NostrExchangeClient()
    
    assert len(client.relay_manager.relays) > 0
    assert client.order_kind == 30000
    assert client.trade_kind == 30001

@pytest.mark.asyncio
async def test_create_order_event():
    """Testar criação de evento de ordem"""
    client = NostrExchangeClient()
    
    order_data = {
        'user_pubkey': 'test_pubkey',
        'pair': 'BTC/USDT',
        'amount': 0.1,
        'price': 50000.0,
        'type': 'buy'
    }
    
    private_key = 'test_private_key'
    
    event = client.create_order_event(order_data, private_key)
    
    assert event.kind == 30000
    assert event.content == str(order_data)
    assert event.tags == [
        ['p', 'test_pubkey'],
        ['t', 'BTC/USDT'],
        ['a', '0.1'],
        ['pr', '50000.0'],
        ['type', 'buy']
    ]

@pytest.mark.asyncio
async def test_order_book():
    """Testar lógica do livro de ordens"""
    order_book = NostrOrderBook()
    
    buy_order = {
        'type': 'buy',
        'price': 50000.0,
        'amount': 0.1,
        'user_pubkey': 'buyer_pubkey'
    }
    
    sell_order = {
        'type': 'sell',
        'price': 49000.0,
        'amount': 0.2,
        'user_pubkey': 'seller_pubkey'
    }
    
    order_book.add_order(buy_order)
    order_book.add_order(sell_order)
    
    assert len(order_book.buy_orders) == 1
    assert len(order_book.sell_orders) == 1
    
    trades = order_book.match_orders()
    
    assert len(trades) == 1
    assert trades[0]['amount'] == 0.1
    assert trades[0]['price'] == 49000.0

@pytest.mark.asyncio
@patch('nostr.relay_manager.RelayManager.publish_event')
async def test_publish_order(mock_publish):
    """Testar publicação de ordem"""
    client = NostrExchangeClient()
    
    order_data = {
        'user_pubkey': 'test_pubkey',
        'pair': 'BTC/USDT',
        'amount': 0.1,
        'price': 50000.0,
        'type': 'buy'
    }
    
    private_key = 'test_private_key'
    
    await client.publish_order(order_data, private_key)
    
    # Verificar se a publicação foi chamada
    assert mock_publish.called
