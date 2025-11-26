// src/lib/secure-storage.ts

/**
 * Local AES-GCM secure storage for NeuroEdge
 * Used by: encrypted-db-adapter, offline-db, message queue
 */

const KEY_DB = "neuroedge-secure-key";
const KEY_STORE = "keys";
const KEY_ID = "master-key-v1";

//
// ---------- IndexedDB Helpers ----------
//

async function openKeyDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(KEY_DB, 1);

    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(KEY_STORE)) {
        db.createObjectStore(KEY_STORE);
      }
    };

    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function storeRawKey(raw: ArrayBuffer): Promise<void> {
  const db = await openKeyDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(KEY_STORE, "readwrite");
    const store = tx.objectStore(KEY_STORE);
    const r = store.put(raw, KEY_ID);

    r.onsuccess = () => resolve();
    r.onerror = () => reject(r.error);
  });
}

//
// ---------- Exported getRawKey() (Needed for UI key-status) ----------
//

export async function getRawKey(): Promise<ArrayBuffer | null> {
  const db = await openKeyDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(KEY_STORE, "readonly");
    const store = tx.objectStore(KEY_STORE);
    const r = store.get(KEY_ID);

    r.onsuccess = () => resolve(r.result || null);
    r.onerror = () => reject(r.error);
  });
}

//
// ---------- Utils ----------
//

function str2ab(str: string): ArrayBuffer {
  return new TextEncoder().encode(str).buffer;
}

function ab2str(buf: ArrayBuffer): string {
  return new TextDecoder().decode(buf);
}

function bufToBase64(buf: ArrayBuffer): string {
  return btoa(String.fromCharCode(...new Uint8Array(buf)));
}

function base64ToBuf(base64: string): ArrayBuffer {
  const bin = atob(base64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return arr.buffer;
}

//
// ---------- Master Key Management ----------
//

/**
 * Initializes or loads the AES-GCM master key
 */
export async function initMasterKey(passphrase?: string): Promise<CryptoKey> {
  if (passphrase) {
    // PBKDF2 derivation
    const baseKey = await crypto.subtle.importKey(
      "raw",
      str2ab(passphrase),
      { name: "PBKDF2" },
      false,
      ["deriveKey"]
    );

    const salt = str2ab("neuroedge-salt-v1"); // can be user-specific

    const key = await crypto.subtle.deriveKey(
      {
        name: "PBKDF2",
        salt,
        iterations: 250_000,
        hash: "SHA-256",
      },
      baseKey,
      {
        name: "AES-GCM",
        length: 256,
      },
      true,
      ["encrypt", "decrypt"]
    );

    // save raw key
    const raw = await crypto.subtle.exportKey("raw", key);
    await storeRawKey(raw);

    return key;
  }

  //
  // No passphrase → load saved key or generate new one
  //
  const existing = await getRawKey();
  if (existing) {
    return crypto.subtle.importKey(
      "raw",
      existing,
      { name: "AES-GCM" },
      true,
      ["encrypt", "decrypt"]
    );
  }

  // generate new key
  const key = await crypto.subtle.generateKey(
    { name: "AES-GCM", length: 256 },
    true,
    ["encrypt", "decrypt"]
  );

  const raw = await crypto.subtle.exportKey("raw", key);
  await storeRawKey(raw);

  return key;
}

//
// ---------- Encryption ----------
//

export async function encryptJSON(obj: any): Promise<string> {
  const key = await initMasterKey();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const data = new TextEncoder().encode(JSON.stringify(obj));

  const ct = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    data
  );

  return JSON.stringify({
    iv: bufToBase64(iv.buffer),
    cipher: bufToBase64(ct),
  });
}

//
// ---------- Decryption ----------
//

export async function decryptJSON(payload: string): Promise<any> {
  const parsed = JSON.parse(payload);

  const ivBuf = base64ToBuf(parsed.iv);
  const cipherBuf = base64ToBuf(parsed.cipher);

  const key = await initMasterKey();

  const plain = await crypto.subtle.decrypt(
    {
      name: "AES-GCM",
      iv: new Uint8Array(ivBuf),
    },
    key,
    cipherBuf
  );

  return JSON.parse(ab2str(plain));
      }
