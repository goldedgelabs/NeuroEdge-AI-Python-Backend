import ClientAgentDetail from '@/components/agents/AgentDetailClient';
export default function AgentDetail({params}:{params:{id:string}}){
  return <ClientAgentDetail id={params.id} />;
}
