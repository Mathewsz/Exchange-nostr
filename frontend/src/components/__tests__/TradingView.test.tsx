import React from 'react';
import { render, screen } from '@testing-library/react';
import TradingView from '../TradingView';

describe('Componente TradingView', () => {
  it('renderiza a visualização de trading', () => {
    render(<TradingView userPubkey="test_pubkey" />);
    const tradingViewContainer = screen.getByTestId('trading-view-container');
    expect(tradingViewContainer).toBeInTheDocument();
  });

  it('renderiza o gráfico de preços', () => {
    render(<TradingView userPubkey="test_pubkey" />);
    const priceChart = screen.getByTestId('price-chart');
    expect(priceChart).toBeInTheDocument();
  });
});