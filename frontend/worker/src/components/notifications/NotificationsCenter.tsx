'use client';
import React from 'react';
import { useNotifications } from '@/stores/notificationsStore';

export default function NotificationsCenter(){
  const notes = useNotifications(s=>s.notifications);
  return (
    <div className="p-3 w-80 bg-white border rounded shadow">
      <div className="font-semibold mb-2">Notifications</div>
      <div className="space-y-2 max-h-64 overflow-auto">
        {notes.map(n=> (
          <div key={n.id} className="p-2 border rounded">
            <div className="font-medium">{n.title}</div>
            <div className="text-sm text-muted-foreground">{n.body}</div>
          </div>
        ))}
        {notes.length===0 && <div className="text-sm text-muted-foreground">No notifications</div>}
      </div>
    </div>
  );
}
