'use client';
import React, { useCallback, useState } from 'react';
import ReactFlow, { addEdge, Background, Controls, MiniMap, Node, Edge } from 'reactflow';

export default function ChainBuilderFlow(){
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const onConnect = useCallback((params:any)=> setEdges(es=> addEdge(params, es)), []);
  const addNode = (type:string)=>{
    const id = 'n_'+Math.random().toString(36).slice(2,6);
    setNodes(ns=>[...ns, { id, position:{x: Math.random()*200, y: Math.random()*200}, data:{label:type} }]);
  };
  return (
    <div className="h-[520px] border rounded">
      <div className="p-2 flex gap-2">
        <button onClick={()=>addNode('Text')}>Add Text</button>
        <button onClick={()=>addNode('Vision')}>Add Vision</button>
      </div>
      <div className="h-[440px]">
        <ReactFlow nodes={nodes} edges={edges} onConnect={onConnect}>
          <MiniMap />
          <Controls />
          <Background />
        </ReactFlow>
      </div>
    </div>
  );
}
