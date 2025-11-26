// src/types/chat.ts
export interface ChatMessage {
  id?: number;
  role: 'user'|'assistant'|'system';
  text: string;
  createdAt: number;
  status?: 'queued'|'sent'|'failed'|'local';
}
