export async function getStreamURL(){
  // prefer worker proxy if set
  const base = (process.env.NEXT_PUBLIC_BACKEND_PROXY) || (process.env.NEXT_PUBLIC_TS_BACKEND);
  if(!base) return null;
  // assume endpoint /v1/chat/stream
  const url = base.replace(/\/$/, '') + '/v1/chat/stream';
  return url;
}

export async function selectHealthyBackend(){
  // simplistic: check TS, then PY, then GO
  const candidates = [
    process.env.NEXT_PUBLIC_TS_BACKEND,
    process.env.NEXT_PUBLIC_PY_BACKEND,
    process.env.NEXT_PUBLIC_GO_BACKEND
  ].filter(Boolean);
  for(const b of candidates){
    try{
      const res = await fetch(b + '/health');
      if(res.ok) return { baseURL: b };
    }catch{}
  }
  return { baseURL: candidates[0] || '' };
}
