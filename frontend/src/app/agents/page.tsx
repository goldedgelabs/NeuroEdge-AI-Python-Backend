import AgentsGrid from '@/components/agents/AgentsGrid';
export default function AgentsPage(){
  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Agents</h1>
      <AgentsGrid />
    </div>
  );
}
