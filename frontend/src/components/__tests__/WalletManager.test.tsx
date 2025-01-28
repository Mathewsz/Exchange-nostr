import React from 'react';
import { render, screen } from '@testing-library/react';
import WalletManager from '../WalletManager';

describe('Componente WalletManager', () => {
  it('renderiza o gerenciador de carteira', () => {
    render(<WalletManager userPubkey="test_pubkey" />);
    const walletManagerContainer = screen.getByTestId('wallet-manager-container');
    expect(walletManagerContainer).toBeInTheDocument();
  });

  it('renderiza o saldo da carteira', () => {
    render(<WalletManager userPubkey="test_pubkey" />);
    const walletBalance = screen.getByTestId('wallet-balance');
    expect(walletBalance).toBeInTheDocument();
  });
});