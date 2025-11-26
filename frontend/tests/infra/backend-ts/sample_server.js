// Run: npm install express jsonwebtoken cookie-parser cors
const express = require('express');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const app = express();
app.use(express.json());
app.use(cookieParser());
app.use(require('cors')({ origin:true, credentials:true }));

const SECRET = process.env.JWT_SECRET || 'secret';

app.post('/auth/login', (req,res)=>{
  const { username } = req.body;
  const token = jwt.sign({sub:username}, SECRET, { expiresIn: '15m' });
  const refresh = jwt.sign({sub:username}, SECRET, { expiresIn: '7d' });
  res.cookie('refresh', refresh, { httpOnly:true, sameSite:'lax' });
  res.json({ token });
});

app.post('/auth/refresh', (req,res)=>{
  const r = req.body.refresh || req.cookies.refresh;
  if(!r) return res.status(401).json({error:'no refresh'});
  try{
    const payload = jwt.verify(r, SECRET);
    const token = jwt.sign({sub: payload.sub}, SECRET, { expiresIn:'15m' });
    res.json({ token, refresh: r });
  }catch(e){ return res.status(401).json({error:'invalid'}); }
});

app.get('/health', (req,res)=> res.json({status:'ok'}));

// SSE example for chat stream
app.post('/v1/chat', (req,res)=>{
  const { text } = req.body;
  res.setHeader('Content-Type','text/event-stream');
  res.setHeader('Cache-Control','no-cache');
  let i=0;
  const iv = setInterval(()=>{
    if(i>5){ res.write('data: '+JSON.stringify({done:true})+'\n\n'); clearInterval(iv); res.end(); return; }
    res.write('data: '+JSON.stringify({token: `part-${i} of ${text}`}) + '\n\n');
    i++;
  }, 400);
});

app.listen(4000, ()=> console.log('ts backend listening 4000'));
