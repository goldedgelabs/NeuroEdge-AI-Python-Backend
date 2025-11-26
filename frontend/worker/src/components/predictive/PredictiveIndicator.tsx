'use client';
import React from 'react';

export default function PredictiveIndicator({label, score}:{label:string, score:number}){
  return (
    <div className="p-2 border rounded inline-flex items-center gap-3">
      <div className="font-medium">{label}</div>
      <div className="text-xs text-muted-foreground">Confidence: {Math.round(score*100)}%</div>
    </div>
  );
}
