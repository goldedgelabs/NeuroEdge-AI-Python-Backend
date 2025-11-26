export async function sendChatMessage(text:string){
  const backend = (process.env.NEXT_PUBLIC_BACKEND_PROXY) || process.env.NEXT_PUBLIC_TS_BACKEND || '';
  const url = (backend.endsWith('/') ? backend.slice(0,-1) : backend) + '/v1/chat';
  const res = await fetch(url, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({text}) });
  if(!res.ok) throw new Error('send failed');
  return res.json();
}
