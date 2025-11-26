'use client';
import React from 'react';
import { Card } from '@/components/ui/card';

export default function BillingPage(){
  return (
    <div className="max-w-4xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-semibold">Billing</h1>
      <Card>
        <div className="flex justify-between items-center">
          <div><strong>Current Plan:</strong> Founder</div>
          <div>Usage: <strong>12,345 tokens</strong></div>
        </div>
      </Card>
      <Card>
        <h3 className="font-medium">Payment Methods</h3>
        <div className="mt-2 text-sm text-muted-foreground">No payment methods configured.</div>
      </Card>
    </div>
  );
}
