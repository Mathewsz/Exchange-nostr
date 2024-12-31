import React, { useState, useEffect } from 'react';

interface WalletManagerProps {
  userPubkey: string;
}

interface Wallet {
  currency: string;
  balance: number;
}

const WalletManager: React.FC<WalletManagerProps> = ({ userPubkey }) => {
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [depositAmount, setDepositAmount] = useState<{[key: string]: string}>({});

  useEffect(() => {
    // Simular carregamento de carteiras
    const mockWallets: Wallet[] = [
      { currency: 'BTC', balance: 0.5 },
      { currency: 'USDT', balance: 1000 }
    ];

    setWallets(mockWallets);
  }, [userPubkey]);

  const handleDeposit = (currency: string) => {
    const amount = parseFloat(depositAmount[currency] || '0');
    
    // Lógica de depósito
    console.log(`Depositar ${amount} ${currency} para ${userPubkey}`);
    
    // Resetar input após depósito
    setDepositAmount(prev => ({...prev, [currency]: ''}));
  };

  return (
    <div className="wallet-manager">
      <h2>Carteiras</h2>
      {wallets.map(wallet => (
        <div key={wallet.currency} className="wallet">
          <h3>{wallet.currency}</h3>
          <p>Saldo: {wallet.balance}</p>
          
          <div className="deposit-section">
            <input 
              type="number" 
              placeholder={`Depositar ${wallet.currency}`}
              value={depositAmount[wallet.currency] || ''}
              onChange={(e) => setDepositAmount(prev => ({
                ...prev, 
                [wallet.currency]: e.target.value
              }))}
            />
            <button onClick={() => handleDeposit(wallet.currency)}>
              Depositar
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default WalletManager;
