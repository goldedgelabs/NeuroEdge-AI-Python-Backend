'use client';
import React, { useState } from 'react';
import { useEngineStore } from '@/stores/engineStore';

export default function EngineDetailClient({id}:{id:string}){
  const engine = useEngineStore(s=>s.find(id));
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [running, setRunning] = useState(false);

  async function run(){
    if(!engine) return;
    setRunning(true);
    try{
      // call backend placeholder
      const base = process.env.NEXT_PUBLIC_TS_BACKEND || '';
      const res = await fetch((base.endsWith('/')?base.slice(0,-1):base) + '/engines/run', {
        method: 'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({engineId: engine.id, input})
      });
      const json = await res.json();
      setOutput(json.result || JSON.stringify(json));
    }catch(e){ setOutput(String(e)); }
    setRunning(false);
  }

  if(!engine) return <div>Engine not found</div>;
  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-xl font-semibold">{engine.name}</h2>
      <p className="text-sm text-muted-foreground">{engine.description}</p>

      <textarea value={input} onChange={e=>setInput(e.target.value)} className="w-full p-2 border rounded mt-4" rows={6} placeholder="Input..." />
      <div className="mt-2 flex gap-2">
        <button onClick={run} className="px-3 py-2 bg-ne-primary text-white rounded" disabled={running}>{running? 'Running...':'Run Engine'}</button>
      </div>

      <div className="mt-4">
        <h3 className="font-medium">Output</h3>
        <pre className="p-3 border rounded bg-white">{output}</pre>
      </div>
    </div>
  );
}
