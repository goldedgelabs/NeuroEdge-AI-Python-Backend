'use client';
import React from 'react';
import { Card } from '@/components/ui/card';

export default function FounderPage(){
  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-semibold">Founder Dashboard</h1>
      <div className="grid md:grid-cols-3 gap-4 mt-4">
        <Card><div className="font-medium">Governance</div><div className="text-sm mt-2">Proposals: 4 active</div></Card>
        <Card><div className="font-medium">Billing & Payouts</div><div className="text-sm mt-2">Next payout in 7 days</div></Card>
        <Card><div className="font-medium">Usage</div><div className="text-sm mt-2">Monthly tokens: 1,234,567</div></Card>
      </div>
    </div>
  );
}
