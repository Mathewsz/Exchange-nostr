import { useState, useCallback } from 'react';

type NotificationType = 'success' | 'error' | 'warning' | 'info';

interface Notification {
  id: number;
  message: string;
  type: NotificationType;
}

export const useNotification = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = useCallback((
    message: string, 
    type: NotificationType = 'info', 
    duration: number = 3000
  ) => {
    const id = Date.now();
    const newNotification: Notification = { id, message, type };

    setNotifications(prev => [...prev, newNotification]);

    // Remover notificação após duração
    setTimeout(() => {
      setNotifications(prev => 
        prev.filter(notification => notification.id !== id)
      );
    }, duration);

    return id;
  }, []);

  const removeNotification = useCallback((id: number) => {
    setNotifications(prev => 
      prev.filter(notification => notification.id !== id)
    );
  }, []);

  return {
    notifications,
    addNotification,
    removeNotification
  };
};
