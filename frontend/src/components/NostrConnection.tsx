import React, { useState } from 'react';

interface NostrConnectionProps {
  onLogin: (pubkey: string) => void;
}

const NostrConnection: React.FC<NostrConnectionProps> = ({ onLogin }) => {
  const [privateKey, setPrivateKey] = useState('');

  const handleLogin = async () => {
    try {
      // Lógica de login com Nostr
      // Aqui você implementaria a geração de chave pública a partir da chave privada
      const publicKey = await generatePublicKey(privateKey);
      onLogin(publicKey);
    } catch (error) {
      console.error('Erro no login Nostr', error);
    }
  };

  const generatePublicKey = async (privateKey: string): Promise<string> => {
    // Implementação de geração de chave pública
    // Esta é uma implementação mock, substitua com lógica real de Nostr
    return privateKey.slice(0, 64);
  };

  return (
    <div className="nostr-connection">
      <h2>Conectar com Nostr</h2>
      <input 
        type="password" 
        placeholder="Chave Privada Nostr"
        value={privateKey}
        onChange={(e) => setPrivateKey(e.target.value)}
      />
      <button onClick={handleLogin}>
        Conectar
      </button>
    </div>
  );
};

export default NostrConnection;
