import { use } from 'react';
import { useRouter } from 'next/navigation';
import { useEngineStore } from '@/stores/engineStore';
import ClientEngineDetail from '@/components/engine/EngineDetailClient';

export default function EngineDetailPage({ params }:{params:{id:string}}){
  return <ClientEngineDetail id={params.id} />;
}
