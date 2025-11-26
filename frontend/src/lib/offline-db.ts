import Dexie from 'dexie';

export interface ChatMessage {
  id?: number;
  role: 'user'|'assistant'|'system';
  text: string;
  createdAt: number;
  status?: 'queued'|'sent'|'failed'|'local';
}

class NeuroDB extends Dexie {
  messages!: Dexie.Table<ChatMessage, number>;
  queue!: Dexie.Table<any, number>;
  constructor() {
    super('neuroedge_db');
    this.version(1).stores({
      messages: '++id,role,createdAt',
      queue: '++id,createdAt'
    });
  }
}

export const db = new NeuroDB();

export async function addMessageToDB(msg: ChatMessage) {
  await db.messages.add(msg);
}

export async function addToQueue(payload:any) {
  await db.queue.add({ payload, createdAt: Date.now() });
}

export async function getQueueItems() { return db.queue.toArray(); }

export async function removeQueueItem(id:number) { return db.queue.delete(id); }
