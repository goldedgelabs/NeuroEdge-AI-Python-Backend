'use client';
import React from 'react';
import Link from 'next/link';
import { Agent } from '@/stores/agentStore';

export default function AgentCard({agent}:{agent:Agent}){
  return (
    <div className="p-3 border rounded" data-testid={`agent-card-${agent.id}`}>
      <div className="flex justify-between">
        <div>
          <div className="font-semibold">{agent.name}</div>
          <div className="text-sm text-muted-foreground">Events: {agent.events}</div>
        </div>
        <div className="flex flex-col gap-2">
          <Link href={`/agents/${agent.id}`}><button className="text-sm underline">Open</button></Link>
          <button onClick={()=>alert('Run '+agent.id)} className="text-sm">Run</button>
        </div>
      </div>
    </div>
  );
}
