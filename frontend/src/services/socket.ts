import { io, Socket } from 'socket.io-client';

let socket: Socket | null = null;

export function connectSocket(baseUrl:string){
  if(socket) return socket;
  socket = io(baseUrl, { transports:['websocket'] });
  socket.on('connect', ()=> console.log('socket connected', socket?.id));
  socket.on('disconnect', ()=> console.log('socket disconnected'));
  return socket;
}

export function getSocket(){ return socket; }
