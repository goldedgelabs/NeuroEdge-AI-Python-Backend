'use client';
import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

export default function ReplicationChart(){
  const [percent, setPercent] = useState(70);
  useEffect(()=>{
    const id = setInterval(()=> setPercent(p=> Math.min(100, Math.max(0, p + (Math.random()-0.5)*6))), 3000);
    return ()=> clearInterval(id);
  },[]);
  const data = [{name:'synced', value: percent}, {name:'pending', value: 100-percent}];
  const colors = ['#34d399', '#f97316'];
  return (
    <div className="h-48">
      <h3 className="font-medium mb-2">Replication Progress</h3>
      <ResponsiveContainer width="100%" height="80%">
        <PieChart><Pie data={data} dataKey="value" innerRadius={40} outerRadius={60}>{data.map((d,i)=><Cell key={i} fill={colors[i%colors.length]} />)}</Pie></PieChart>
      </ResponsiveContainer>
    </div>
  );
}
