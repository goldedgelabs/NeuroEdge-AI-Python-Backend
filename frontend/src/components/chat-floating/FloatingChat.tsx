'use client';
import React, { useState } from 'react';
import ChatStream from '@/components/chat/ChatStream';
import ChatInput from '@/components/chat/ChatInput';
export default function FloatingChat(){ const [open,setOpen]=useState(false); return (<div>{!open && <button onClick={()=>setOpen(true)} className='neuro-floating btn'>NE</button>}{open && (<div className='fixed bottom-6 right-6 w-96 h-96 panel z-50 p-3 flex flex-col'><div className='flex justify-between items-center'><strong>NeuroEdge</strong><button onClick={()=>setOpen(false)} className='btn-ghost'>Close</button></div><div className='flex-1 overflow-auto'><ChatStream /></div><div className='mt-2'><ChatInput/></div></div>)}</div>); }
