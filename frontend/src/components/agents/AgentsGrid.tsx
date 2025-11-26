'use client';
import React from 'react';
import AgentCard from './AgentCard';
import { useAgentStore } from '@/stores/agentStore';

export default function AgentsGrid(){
  const list = useAgentStore(s=>s.getPage());
  const page = useAgentStore(s=>s.page);
  const setPage = useAgentStore(s=>s.setPage);
  const total = useAgentStore(s=>s.total);
  const perPage = useAgentStore(s=>s.perPage);
  const pages = Math.ceil(total/perPage);
  return (
    <div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {list.map(a=> <AgentCard key={a.id} agent={a} />)}
      </div>
      <div className="mt-4 flex justify-between items-center">
        <div>Page {page} of {pages}</div>
        <div className="flex gap-2">
          <button onClick={()=>setPage(Math.max(1,page-1))}>Prev</button>
          <button onClick={()=>setPage(Math.min(pages,page+1))}>Next</button>
        </div>
      </div>
    </div>
  );
}
