import React from 'react';
import { render, screen } from '@testing-library/react';
import OrderBook from '../OrderBook';

describe('Componente OrderBook', () => {
  it('renderiza o livro de ordens', () => {
    render(<OrderBook />);
    const orderBookContainer = screen.getByTestId('order-book-container');
    expect(orderBookContainer).toBeInTheDocument();
  });

  it('renderiza ordens de compra e venda', () => {
    render(<OrderBook />);
    const buyOrders = screen.getByTestId('buy-orders');
    const sellOrders = screen.getByTestId('sell-orders');
    expect(buyOrders).toBeInTheDocument();
    expect(sellOrders).toBeInTheDocument();
  });
});