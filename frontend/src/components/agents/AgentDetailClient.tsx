'use client';
import React, { useState, useEffect } from 'react';
import { useAgentStore } from '@/stores/agentStore';

export default function AgentDetailClient({id}:{id:string}){
  const agent = useAgentStore(s=>s.find(id));
  const [logs, setLogs] = useState<string[]>([]);
  useEffect(()=>{
    // fake logs
    const timer = setInterval(()=> setLogs(l=> [`Event ${Math.random().toFixed(3)}`, ...l].slice(0,50)), 2500);
    return ()=> clearInterval(timer);
  },[]);
  if(!agent) return <div>Not found</div>;
  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-xl font-semibold">{agent.name}</h2>
      <div className="mt-4">
        <h3 className="font-medium">Logs</h3>
        <div className="mt-2 space-y-2">
          {logs.map((l,i)=><div key={i} className="p-2 border rounded bg-white">{l}</div>)}
        </div>
      </div>
    </div>
  );
}
