import React from 'react';
import { render, act, renderHook } from '@testing-library/react';
import { AuthProvider, useAuth } from '../AuthContext';
import { authService } from '../../services/api';

// Mock do serviço de autenticação
jest.mock('../../services/api', () => ({
  authService: {
    login: jest.fn(),
    register: jest.fn()
  }
}));

const mockUser = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  nostrPubkey: 'pubkey123'
};

const mockLoginResponse = {
  ...mockUser,
  access_token: 'fake_token'
};

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  it('deve realizar login com sucesso', async () => {
    (authService.login as jest.Mock).mockResolvedValue(mockLoginResponse);

    const wrapper: React.FC = ({ children }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.login('testuser', 'password');
    });

    expect(result.current.user).toEqual(mockUser);
    expect(result.current.token).toBe('fake_token');
    expect(result.current.isAuthenticated).toBe(true);
  });

  it('deve realizar logout', async () => {
    (authService.login as jest.Mock).mockResolvedValue(mockLoginResponse);

    const wrapper: React.FC = ({ children }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.login('testuser', 'password');
      result.current.logout();
    });

    expect(result.current.user).toBeNull();
    expect(result.current.token).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('deve tratar erro de login', async () => {
    (authService.login as jest.Mock).mockRejectedValue(new Error('Login failed'));

    const wrapper: React.FC = ({ children }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      try {
        await result.current.login('testuser', 'wrongpassword');
      } catch (error) {
        expect(result.current.error).toBe('Falha no login. Verifique suas credenciais.');
      }
    });
  });
});
