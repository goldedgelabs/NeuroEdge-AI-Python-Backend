'use client';
import React, { useEffect, useState } from 'react';
export default function ThemeToggle(){
  const [dark, setDark] = useState(false);
  useEffect(()=>{ if(dark) document.documentElement.classList.add('dark'); else document.documentElement.classList.remove('dark'); },[dark]);
  return <button onClick={()=>setDark(!dark)} className='px-2 py-1 border rounded'>Toggle Theme</button>;
}
