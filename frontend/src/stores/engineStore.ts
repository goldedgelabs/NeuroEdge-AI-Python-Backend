import create from 'zustand';
import enginesData from '@/data/engines.json';

export type Engine = {
  id: string;
  name: string;
  description: string;
  params: Record<string, any>;
  status: string;
};

type EngineState = {
  engines: Engine[];
  page: number;
  perPage: number;
  total: number;
  setPage: (p:number)=>void;
  getPage: ()=>Engine[];
  find: (id:string)=>Engine | undefined;
};

export const useEngineStore = create<EngineState>((set, get)=>({
  engines: (enginesData as any).engines,
  page: 1,
  perPage: 12,
  total: (enginesData as any).engines.length,
  setPage: (p)=>set({page:p}),
  getPage: ()=> {
    const {page, perPage, engines} = get();
    const start = (page-1)*perPage;
    return engines.slice(start, start+perPage);
  },
  find: (id)=> get().engines.find(e=>e.id===id)
}));
