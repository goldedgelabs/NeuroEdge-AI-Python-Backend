import create from 'zustand';
export type Notification = { id:string; title:string; body:string; time:number; seen?:boolean };
type State = { notifications: Notification[]; push: (n:Notification)=>void; markSeen:(id:string)=>void; clear:()=>void };
export const useNotifications = create<State>((set)=>({ notifications: [], push:(n)=>set(s=>({notifications:[n,...s.notifications]})), markSeen:(id)=>set(s=>({notifications:s.notifications.map(n=> n.id===id?{...n,seen:true}:n)})), clear:()=>set({notifications:[]}) }));
