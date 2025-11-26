import Link from 'next/link';
export default function Home() {
  return (
    <main className="max-w-5xl mx-auto p-6">
      <h1 className="text-3xl font-bold">NeuroEdge</h1>
      <p className="mt-2">Frontend ready to connect to your backends.</p>
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Link href="/chat" className="p-4 border rounded">Chat</Link>
        <Link href="/engines" className="p-4 border rounded">Engines</Link>
        <Link href="/agents" className="p-4 border rounded">Agents</Link>
      </div>
    </main>
  );
}
