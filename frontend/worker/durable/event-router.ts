export class EventRouter {
  constructor(state, env){
    this.state = state;
    this.env = env;
    this.clients = new Set();
  }
  async fetch(req){
    const url = new URL(req.url);
    if(url.pathname === '/connect'){
      const [client, server] = Object.values(new WebSocketPair());
      server.accept();
      this.clients.add(server);
      server.addEventListener('close', ()=> this.clients.delete(server));
      server.addEventListener('message', evt => {
        // broadcast
        for(const c of this.clients) try{ c.send(evt.data); }catch{}
      });
      return new Response(null, { status: 101, webSocket: client });
    }
    if(url.pathname === '/publish' && req.method === 'POST'){
      const body = await req.text();
      for(const c of this.clients) try{ c.send(body); }catch{}
      return new Response('ok');
    }
    return new Response('not found', { status:404 });
  }
}
