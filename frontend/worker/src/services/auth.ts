export async function secureFetch(url:string, opts: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('ne_token') : null;
  const headers = new Headers(opts.headers || {});
  if(token) headers.set('Authorization', 'Bearer '+token);
  const res = await fetch(url, {...opts, headers, credentials: 'include'});
  if(res.status === 401){
    // try refresh
    const refreshed = await tryRefresh();
    if(refreshed){
      const newToken = localStorage.getItem('ne_token');
      if(newToken) headers.set('Authorization', 'Bearer '+newToken);
      return fetch(url, {...opts, headers, credentials: 'include'});
    }
  }
  return res;
}

async function tryRefresh(){
  try{
    const refresh = localStorage.getItem('ne_refresh');
    if(!refresh) return false;
    const base = process.env.NEXT_PUBLIC_TS_BACKEND || '';
    const res = await fetch((base.endsWith('/')?base.slice(0,-1):base) + '/auth/refresh', {
      method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({refresh})
    });
    if(!res.ok) return false;
    const json = await res.json();
    localStorage.setItem('ne_token', json.token);
    localStorage.setItem('ne_refresh', json.refresh);
    return true;
  }catch(e){ return false; }
}
