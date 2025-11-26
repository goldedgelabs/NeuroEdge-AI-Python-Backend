'use client';
import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function AgentHeatmap(){
  const [data, setData] = useState(Array.from({length:7}).map((_,i)=>({name:'A'+i, value:Math.round(Math.random()*100)})));
  useEffect(()=>{
    const id = setInterval(()=> setData(d=> d.map(x=> ({...x, value: Math.max(0, x.value + Math.round((Math.random()-0.5)*20))}))), 2000);
    return ()=> clearInterval(id);
  },[]);
  return (
    <div className="h-48">
      <h3 className="font-medium mb-2">Active Agents</h3>
      <ResponsiveContainer width="100%" height="80%">
        <BarChart data={data}><XAxis dataKey="name"/><YAxis/><Tooltip/><Bar dataKey="value" fill="#06b6d4" /></BarChart>
      </ResponsiveContainer>
    </div>
  );
}
