'use client';
import React from 'react';
import { useEngineStore } from '@/stores/engineStore';
import EngineCard from './EngineCard';
import { Button } from '@/components/ui/button';

export default function EngineList(){
  const list = useEngineStore(s=>s.getPage());
  const page = useEngineStore(s=>s.page);
  const perPage = useEngineStore(s=>s.perPage);
  const total = useEngineStore(s=>s.total);
  const setPage = useEngineStore(s=>s.setPage);
  const pages = Math.ceil(total/perPage);
  return (
    <div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {list.map(e=> <EngineCard key={e.id} engine={e} />)}
      </div>
      <div className="mt-4 flex justify-between items-center">
        <div className="text-sm">Page {page} of {pages}</div>
        <div className="flex gap-2">
          <Button onClick={()=>setPage(Math.max(1,page-1))} data-testid="engines-prev">Prev</Button>
          <Button onClick={()=>setPage(Math.min(pages,page+1))} data-testid="engines-next">Next</Button>
        </div>
      </div>
    </div>
  );
}
