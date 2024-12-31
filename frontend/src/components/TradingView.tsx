import React, { useState } from 'react';

interface TradingViewProps {
  userPubkey: string;
}

const TradingView: React.FC<TradingViewProps> = ({ userPubkey }) => {
  const [orderType, setOrderType] = useState<'buy' | 'sell'>('buy');
  const [price, setPrice] = useState<string>('');
  const [amount, setAmount] = useState<string>('');

  const handleSubmitOrder = () => {
    // Lógica para submeter ordem via Nostr
    const orderData = {
      type: orderType,
      price: parseFloat(price),
      amount: parseFloat(amount),
      userPubkey
    };

    console.log('Ordem submetida:', orderData);
    // Aqui você faria a chamada para o backend/Nostr
  };

  return (
    <div className="trading-view">
      <h2>Negociar</h2>
      <div className="order-type-selector">
        <button 
          className={orderType === 'buy' ? 'active' : ''}
          onClick={() => setOrderType('buy')}
        >
          Comprar
        </button>
        <button 
          className={orderType === 'sell' ? 'active' : ''}
          onClick={() => setOrderType('sell')}
        >
          Vender
        </button>
      </div>

      <div className="order-form">
        <input 
          type="number" 
          placeholder="Preço" 
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />
        <input 
          type="number" 
          placeholder="Quantidade" 
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <button onClick={handleSubmitOrder}>
          {orderType === 'buy' ? 'Comprar' : 'Vender'}
        </button>
      </div>
    </div>
  );
};

export default TradingView;
