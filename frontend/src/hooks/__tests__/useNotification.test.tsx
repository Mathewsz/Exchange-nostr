import { renderHook, act } from '@testing-library/react-hooks';
import { useNotification } from '../useNotification';

describe('useNotification', () => {
  it('deve adicionar uma notificação', () => {
    const { result } = renderHook(() => useNotification());

    act(() => {
      result.current.addNotification('Teste de notificação');
    });

    expect(result.current.notifications).toHaveLength(1);
    expect(result.current.notifications[0].message).toBe('Teste de notificação');
  });

  it('deve remover uma notificação', () => {
    const { result } = renderHook(() => useNotification());

    let notificationId: number;

    act(() => {
      notificationId = result.current.addNotification('Teste de notificação');
    });

    act(() => {
      result.current.removeNotification(notificationId);
    });

    expect(result.current.notifications).toHaveLength(0);
  });

  it('deve adicionar notificação com tipo específico', () => {
    const { result } = renderHook(() => useNotification());

    act(() => {
      result.current.addNotification('Erro', 'error');
    });

    expect(result.current.notifications[0].type).toBe('error');
  });
});
