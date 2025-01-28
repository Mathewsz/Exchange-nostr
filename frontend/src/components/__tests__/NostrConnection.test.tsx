import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import NostrConnection from '../NostrConnection';

describe('Componente NostrConnection', () => {
  it('renderiza o botão de login', () => {
    render(<NostrConnection onLogin={jest.fn()} />);
    const loginButton = screen.getByText('Login with Nostr');
    expect(loginButton).toBeInTheDocument();
  });

  it('chama a função onLogin ao clicar no botão', () => {
    const mockOnLogin = jest.fn();
    render(<NostrConnection onLogin={mockOnLogin} />);
    const loginButton = screen.getByText('Login with Nostr');
    fireEvent.click(loginButton);
    expect(mockOnLogin).toHaveBeenCalled();
  });
});