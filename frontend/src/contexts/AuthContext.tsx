import React, { createContext, useState, useContext, useEffect } from 'react';
import { authService } from '../services/api';

interface User {
  id: number;
  username: string;
  email: string;
  nostrPubkey: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: {
    username: string, 
    email: string, 
    password: string, 
    nostrPubkey: string
  }) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  login: async () => {},
  register: async () => {},
  logout: () => {},
  isAuthenticated: false,
  error: null
});

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Recuperar dados de autenticação do localStorage
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('access_token');

    if (storedUser && storedToken) {
      setUser(JSON.parse(storedUser));
      setToken(storedToken);
    }
  }, []);

  const login = async (username: string, password: string) => {
    try {
      setError(null);
      const response = await authService.login(username, password);
      
      const userData = {
        id: response.id,
        username: response.username,
        email: response.email,
        nostrPubkey: response.nostr_pubkey
      };

      setUser(userData);
      setToken(response.access_token);

      // Armazenar dados no localStorage
      localStorage.setItem('user', JSON.stringify(userData));
      localStorage.setItem('access_token', response.access_token);
    } catch (err) {
      setError('Falha no login. Verifique suas credenciais.');
      throw err;
    }
  };

  const register = async (userData: {
    username: string, 
    email: string, 
    password: string, 
    nostrPubkey: string
  }) => {
    try {
      setError(null);
      const response = await authService.register(userData);
      
      const newUser = {
        id: response.id,
        username: response.username,
        email: response.email,
        nostrPubkey: response.nostr_pubkey
      };

      setUser(newUser);
      // Não define token automaticamente após registro
    } catch (err) {
      setError('Falha no registro. Tente novamente.');
      throw err;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      login,
      register,
      logout,
      isAuthenticated: !!token,
      error
    }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook personalizado para usar o contexto de autenticação
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  
  return context;
};
