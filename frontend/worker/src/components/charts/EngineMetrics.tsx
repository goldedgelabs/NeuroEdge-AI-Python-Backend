'use client';
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function EngineMetrics(){
  const [data, setData] = useState([{name:'0',value:0}]);
  useEffect(()=>{
    const id = setInterval(()=>{
      setData(d=>[...d.slice(-19), { name: String(d.length), value: Math.round(Math.random()*100) }]);
    }, 1000);
    return ()=> clearInterval(id);
  },[]);
  return (
    <div className="h-48">
      <h3 className="font-medium mb-2">Engine Throughput</h3>
      <ResponsiveContainer width="100%" height="80%">
        <LineChart data={data}><XAxis dataKey="name"/><YAxis/><Tooltip/><Line type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={2} /></LineChart>
      </ResponsiveContainer>
    </div>
  );
}
