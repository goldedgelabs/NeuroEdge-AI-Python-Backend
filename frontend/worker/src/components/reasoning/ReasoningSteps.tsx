'use client';
import React from 'react';
export default function ReasoningSteps({steps}:{steps:string[]}){
  return (
    <div className="p-3 border rounded bg-white">
      <div className="font-medium mb-2">System Reasoning (summarized)</div>
      <ol className="list-decimal pl-5 space-y-2 text-sm">
        {steps.map((s,i)=> <li key={i}>{s}</li>)}
      </ol>
    </div>
  );
}
