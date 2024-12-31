import React, { useState, useEffect } from 'react';

interface Order {
  id: string;
  type: 'buy' | 'sell';
  price: number;
  amount: number;
}

const OrderBook: React.FC = () => {
  const [buyOrders, setBuyOrders] = useState<Order[]>([]);
  const [sellOrders, setSellOrders] = useState<Order[]>([]);

  useEffect(() => {
    // Simular carregamento de ordens
    const mockBuyOrders: Order[] = [
      { id: '1', type: 'buy', price: 49000, amount: 0.5 },
      { id: '2', type: 'buy', price: 48500, amount: 0.3 }
    ];

    const mockSellOrders: Order[] = [
      { id: '3', type: 'sell', price: 50000, amount: 0.4 },
      { id: '4', type: 'sell', price: 50500, amount: 0.2 }
    ];

    setBuyOrders(mockBuyOrders);
    setSellOrders(mockSellOrders);
  }, []);

  return (
    <div className="order-book">
      <h2>Livro de Ordens</h2>
      <div className="order-sections">
        <div className="buy-orders">
          <h3>Compra</h3>
          {buyOrders.map(order => (
            <div key={order.id} className="order buy">
              <span>{order.price}</span>
              <span>{order.amount}</span>
            </div>
          ))}
        </div>
        <div className="sell-orders">
          <h3>Venda</h3>
          {sellOrders.map(order => (
            <div key={order.id} className="order sell">
              <span>{order.price}</span>
              <span>{order.amount}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OrderBook;
