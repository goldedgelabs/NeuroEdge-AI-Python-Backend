import EngineList from '@/components/engine/EngineList';

export default function EnginesPage(){
  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Engines</h1>
      <EngineList />
    </div>
  );
}
