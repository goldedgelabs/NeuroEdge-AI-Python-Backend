'use client';
import React from 'react';
import Link from 'next/link';
import { Engine } from '@/stores/engineStore';

export default function EngineCard({engine}:{engine:Engine}){
  return (
    <div className="p-4 border rounded shadow-sm" data-testid={`engine-item-${engine.id}`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-semibold">{engine.name}</h3>
          <p className="text-sm text-muted-foreground mt-1">{engine.description}</p>
        </div>
        <div className="text-xs">{engine.status}</div>
      </div>
      <div className="mt-3 flex gap-2">
        <Link href={`/engines/${engine.id}`} className="text-sm underline">Open</Link>
      </div>
    </div>
  );
}
