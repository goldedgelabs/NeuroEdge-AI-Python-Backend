import { useState } from 'react';
export function useAuth(){
  const [token, setToken] = useState(typeof window !== 'undefined' ? localStorage.getItem('ne_token') : null);
  function login(t:string){ localStorage.setItem('ne_token', t); setToken(t); }
  function logout(){ localStorage.removeItem('ne_token'); setToken(null); }
  return { token, login, logout };
}
