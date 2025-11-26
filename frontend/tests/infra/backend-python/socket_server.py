# Run: pip install fastapi "python-socketio[asyncio_client]" "uvicorn[standard]"
import json
import asyncio
import socketio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
sio_app = socketio.ASGIApp(sio, app)

@app.get('/health')
async def health():
    return {'status':'ok'}

@app.post('/v1/engines/run')
async def run_engine(req: Request):
    data = await req.json()
    engineId = data.get('engineId')
    # simulate streaming via SSE (simple)
    async def event_stream():
        for i in range(8):
            chunk = f"{{\"token\": \"token-{i} for {engineId}\"}}\n"
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.3)
        yield 'data: {"done":true}\n\n'
    return StreamingResponse(event_stream(), media_type='text/event-stream')

# Socket.IO example: emit engine events
@sio.event
async def connect(sid, environ):
    print('client connected', sid)
    await sio.emit('server_message', {'msg':'welcome'}, to=sid)

# Background task to emit engine logs
async def background_emit():
    while True:
        await sio.sleep(2)
        await sio.emit('engine_event', {'engine':'engine-01','msg':'tick'})

@sio.event
async def start_bg(sid):
    sio.start_background_task(background_emit)
