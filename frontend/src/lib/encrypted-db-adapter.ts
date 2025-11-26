// src/lib/encrypted-db-adapter.ts
import { addEncryptedRow } from '@/lib/offline-db';
import { encryptJSON, decryptJSON, getRawKey } from '@/lib/secure-storage';

/**
 * Save a message object encrypted in the DB.
 * msg: { role, text, createdAt, status }
 */
export async function addEncryptedMessage(msg: any) {
  const cipher = await encryptJSON(msg);
  return addEncryptedRow(cipher);
}

/**
 * Return decrypted messages (uses secure-storage.decryptJSON)
 */
export async function getDecryptedMessages() {
  // we delegate to offline-db.getAllDecryptedMessages for batch decryption,
  // but in case you want to directly read raw rows and decrypt here, you can implement it.
  const { getAllDecryptedMessages } = await import('@/lib/offline-db');
  return getAllDecryptedMessages();
}

/**
 * Helper to check if a key exists (for UI)
 */
export async function hasStoredKey(): Promise<boolean> {
  const raw = await getRawKey();
  return !!raw;
}
