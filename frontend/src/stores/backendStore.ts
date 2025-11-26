import create from 'zustand';

type BackendState = {
  current: string;
  setCurrent: (s:string)=>void;
  health: Record<string, boolean>;
  setHealth: (k:string,v:boolean)=>void;
};

export const useBackendStore = create<BackendState>((set)=>({
  current: process.env.NEXT_PUBLIC_TS_BACKEND || '',
  setCurrent: (s)=>set({current:s}),
  health: {},
  setHealth: (k,v)=>set((st)=>({ health: {...st.health, [k]: v} }))
}));
