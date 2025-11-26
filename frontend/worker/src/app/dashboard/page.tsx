'use client';
import React from 'react';
import EngineMetrics from '@/components/charts/EngineMetrics';
import AgentHeatmap from '@/components/charts/AgentHeatmap';
import ReplicationChart from '@/components/charts/ReplicationChart';
import { Card } from '@/components/ui/card';

export default function DashboardPage(){
  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Realtime Dashboard</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card><EngineMetrics /></Card>
        <Card><AgentHeatmap /></Card>
        <Card><ReplicationChart /></Card>
      </div>
      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card><div className="p-4">Health & Logs (streaming)</div></Card>
        <Card><div className="p-4">System Trace</div></Card>
      </div>
    </div>
  );
}
