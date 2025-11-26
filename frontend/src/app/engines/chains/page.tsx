import ChainBuilderFlow from '@/components/engine/ChainBuilderFlow';
export default function ChainsPage(){
  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Engine Chain Builder</h1>
      <ChainBuilderFlow />
    </div>
  );
}
