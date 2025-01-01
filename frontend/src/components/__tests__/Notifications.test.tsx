import React from 'react';
import { render, screen } from '@testing-library/react';
import Notifications from '../Notifications';
import { useNotification } from '../../hooks/useNotification';

// Mock do hook de notificação
jest.mock('../../hooks/useNotification', () => ({
  useNotification: jest.fn()
}));

describe('Componente de Notificações', () => {
  it('renderiza sem notificações', () => {
    (useNotification as jest.Mock).mockReturnValue({
      notifications: [],
      removeNotification: jest.fn()
    });

    render(<Notifications />);
    const container = screen.getByTestId('notifications-container');
    expect(container.children.length).toBe(0);
  });

  it('renderiza múltiplas notificações', () => {
    (useNotification as jest.Mock).mockReturnValue({
      notifications: [
        { id: 1, message: 'Notificação 1', type: 'success' },
        { id: 2, message: 'Notificação 2', type: 'error' }
      ],
      removeNotification: jest.fn()
    });

    render(<Notifications />);
    const notifications = screen.getAllByTestId('notification');
    expect(notifications.length).toBe(2);
  });
});
