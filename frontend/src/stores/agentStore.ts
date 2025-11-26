import create from 'zustand';
import agentsData from '@/data/agents.json';

export type Agent = { id:string; name:string; status:string; events:number };

type AgentState = {
  agents: Agent[];
  page:number;
  perPage:number;
  total:number;
  setPage:(p:number)=>void;
  getPage:()=>Agent[];
  find:(id:string)=>Agent|undefined;
};

export const useAgentStore = create<AgentState>((set,get)=>({
  agents: (agentsData as any).agents,
  page:1, perPage:12, total:(agentsData as any).agents.length,
  setPage:(p)=>set({page:p}),
  getPage:()=>{ const {page,perPage,agents}=get(); const s=(page-1)*perPage; return agents.slice(s,s+perPage); },
  find:(id)=> get().agents.find(a=>a.id===id)
}));
