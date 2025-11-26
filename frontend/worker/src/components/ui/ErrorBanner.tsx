'use client';
import React from 'react';
export default function ErrorBanner({msg}:{msg:string}){
  return <div className='w-full bg-red-50 border border-red-200 text-red-800 p-3 rounded'>{msg}</div>;
}
