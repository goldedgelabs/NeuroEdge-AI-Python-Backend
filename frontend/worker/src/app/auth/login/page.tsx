'use client';
import React, { useState } from 'react';
export default function LoginPage(){
  const [user, setUser] = useState('user1');
  const [loading, setLoading] = useState(false);
  async function submit(){
    setLoading(true);
    const res = await fetch((process.env.NEXT_PUBLIC_TS_BACKEND || '') + '/auth/login', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username:user})});
    const json = await res.json();
    if(json.token){ localStorage.setItem('ne_token', json.token); alert('logged'); }
    setLoading(false);
  }
  return (<div className='p-6 max-w-md mx-auto'><h2>Login</h2><input value={user} onChange={e=>setUser(e.target.value)} className='w-full p-2 border rounded'/><button onClick={submit} className='mt-2 px-3 py-2 bg-ne-primary text-white'>{loading?'...':'Login'}</button></div>);
}
