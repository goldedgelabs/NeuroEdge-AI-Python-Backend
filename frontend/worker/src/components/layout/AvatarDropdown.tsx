'use client';
import React from 'react';
export default function AvatarDropdown(){
  return (
    <div className='relative inline-block text-left'>
      <button className='w-8 h-8 rounded-full bg-gray-300'>A</button>
      <div className='absolute right-0 mt-2 w-48 bg-white border rounded shadow p-2'>
        <div className='py-1 text-sm'><a href='/profile'>Profile</a></div>
        <div className='py-1 text-sm'><a href='/settings'>Settings</a></div>
        <div className='py-1 text-sm'><a href='/billing'>Billing</a></div>
        <div className='py-1 text-sm'><a href='/founder'>Founder</a></div>
        <div className='py-1 text-sm'><button onClick={()=>alert('Logout')}>Logout</button></div>
      </div>
    </div>
  );
}
