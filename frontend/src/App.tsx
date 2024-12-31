import React, { useState } from 'react';
import OrderBook from './components/OrderBook';
import TradingView from './components/TradingView';
import NostrConnection from './components/NostrConnection';
import WalletManager from './components/WalletManager';

const App: React.FC = () => {
  const [userPubkey, setUserPubkey] = useState<string>('');

  const handleNostrLogin = (pubkey: string) => {
    setUserPubkey(pubkey);
  };

  return (
    <div className="app-container">
      <header>
        <h1>Nostr Decentralized Exchange</h1>
        {!userPubkey && (
          <NostrConnection onLogin={handleNostrLogin} />
        )}
      </header>

      {userPubkey && (
        <main>
          <div className="trading-section">
            <TradingView userPubkey={userPubkey} />
            <OrderBook />
          </div>
          <WalletManager userPubkey={userPubkey} />
        </main>
      )}

      <footer>
        <p>Powered by Nostr Protocol</p>
      </footer>
    </div>
  );
};

export default App;
