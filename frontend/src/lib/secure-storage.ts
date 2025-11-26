// src/lib/secure-storage.ts
const KEY_DB = 'neuroedge-secure-key';
const KEY_STORE = 'keys';
const KEY_ID = 'master-key-v1';

async function openKeyDB() {
  return new Promise<IDBDatabase>((resolve, reject) => {
    const req = indexedDB.open(KEY_DB, 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(KEY_STORE)) db.createObjectStore(KEY_STORE);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function storeRawKey(raw: ArrayBuffer) {
  const db = await openKeyDB();
  return new Promise<void>((res, rej) => {
    const tx = db.transaction(KEY_STORE, 'readwrite');
    const store = tx.objectStore(KEY_STORE);
    const r = store.put(raw, KEY_ID);
    r.onsuccess = () => res();
    r.onerror = () => rej(r.error);
  });
}

async function getRawKey() {
  const db = await openKeyDB();
  return new Promise<ArrayBuffer | null>((res, rej) => {
    const tx = db.transaction(KEY_STORE, 'readonly');
    const store = tx.objectStore(KEY_STORE);
    const r = store.get(KEY_ID);
    r.onsuccess = () => res(r.result || null);
    r.onerror = () => rej(r.error);
  });
}

function str2ab(str: string) {
  return new TextEncoder().encode(str).buffer;
}
function ab2str(buf: ArrayBuffer) {
  return new TextDecoder().decode(buf);
}
function bufToBase64(buf: ArrayBuffer) {
  return btoa(String.fromCharCode(...new Uint8Array(buf)));
}
function base64ToBuf(b64: string) {
  const bin = atob(b64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return arr.buffer;
}

// Derive key from passphrase (PBKDF2)
export async function initMasterKey(passphrase?: string) {
  if (passphrase) {
    // derive via PBKDF2
    const salt = str2ab('neuroedge-salt-v1'); // you can make this user-specific
    const baseKey = await crypto.subtle.importKey('raw', str2ab(passphrase), { name: 'PBKDF2' }, false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey(
      { name: 'PBKDF2', salt, iterations: 250_000, hash: 'SHA-256' },
      baseKey,
      { name: 'AES-GCM', length: 256 },
      true,
      ['encrypt', 'decrypt']
    );
    // export and store raw key
    const raw = await crypto.subtle.exportKey('raw', key);
    await storeRawKey(raw);
    return key;
  } else {
    // Try to load existing key
    const existing = await getRawKey();
    if (existing) {
      return await crypto.subtle.importKey('raw', existing, { name: 'AES-GCM' }, true, ['encrypt', 'decrypt']);
    }
    // else create a new random key and store it
    const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt']);
    const raw = await crypto.subtle.exportKey('raw', key);
    await storeRawKey(raw);
    return key;
  }
}

export async function encryptJSON(obj: any) {
  const key = await initMasterKey(); // ensures a key
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const data = new TextEncoder().encode(JSON.stringify(obj));
  const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, data);
  // store iv + cipher in base64
  return JSON.stringify({ iv: bufToBase64(iv.buffer), cipher: bufToBase64(ct) });
}

export async function decryptJSON(payload: string) {
  const parsed = JSON.parse(payload);
  const iv = base64ToBuf(parsed.iv);
  const cipher = base64ToBuf(parsed.cipher);
  const key = await initMasterKey();
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: new Uint8Array(iv) }, key, cipher);
  return JSON.parse(ab2str(plain));
}
