'use client';
import React from 'react';
export function Toast({msg}:{msg:string}){ return <div className='fixed bottom-6 right-6 bg-black text-white px-4 py-2 rounded'>{msg}</div>; }
export default Toast;
