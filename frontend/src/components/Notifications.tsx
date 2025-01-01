import React from 'react';
import { useNotification } from '../hooks/useNotification';

const Notifications: React.FC = () => {
  const { notifications, removeNotification } = useNotification();

  return (
    <div 
      className="notifications-container" 
      data-testid="notifications-container"
    >
      {notifications.map(notification => (
        <div 
          key={notification.id} 
          className={`notification notification-${notification.type}`}
          onClick={() => removeNotification(notification.id)}
          data-testid="notification"
        >
          {notification.message}
        </div>
      ))}
    </div>
  );
};

export default Notifications;
