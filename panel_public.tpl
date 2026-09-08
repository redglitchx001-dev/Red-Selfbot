<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RED SELFBOT - 2026</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@700;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --red:#ff0044; --pink:#ff6688; --green:#00ff88; --amber:#ffbd2e;
  --bg:#06060a; --card:rgba(22,22,34,.85); --line:rgba(255,0,60,.28);
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:#ddd;font-family:'JetBrains Mono',monospace;min-height:100vh;overflow-x:hidden}
/* ---------- cyberpunk background: animated grid + scanline + glow ---------- */
body::before{content:'';position:fixed;inset:-48px;background-image:linear-gradient(rgba(255,0,60,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(255,0,60,.055) 1px,transparent 1px);background-size:48px 48px;pointer-events:none;z-index:0;animation:grid 22s linear infinite}
@keyframes grid{0%{transform:translate(0,0)}100%{transform:translate(48px,48px)}}
body::after{content:'';position:fixed;left:0;right:0;top:0;height:2px;background:linear-gradient(90deg,transparent,var(--red),var(--pink),transparent);animation:scan 6s linear infinite;z-index:2;opacity:.65;pointer-events:none}
@keyframes scan{0%{top:-2px}100%{top:100vh}}
.glow-orb{position:fixed;width:52vw;height:52vw;border-radius:50%;pointer-events:none;z-index:0;filter:blur(90px);opacity:.14;background:radial-gradient(circle,var(--red),transparent 65%);top:-22vw;right:-16vw;animation:orb 14s ease-in-out infinite alternate}
.glow-orb.b{left:-20vw;right:auto;top:auto;bottom:-24vw;background:radial-gradient(circle,var(--pink),transparent 65%);animation-duration:18s}
@keyframes orb{0%{transform:translate(0,0) scale(1)}100%{transform:translate(-6vw,4vw) scale(1.15)}}
.wrap{position:relative;z-index:1;max-width:760px;margin:0 auto;padding:26px 18px 60px}
/* ---------- ASCII art (pyfiglet ansi_shadow + ▓▒░ shading) ---------- */
pre.art{font-size:clamp(.5rem,2.4vw,1.05rem);line-height:1.08;font-weight:700;display:inline-block;text-align:center;margin:0 auto;
  background:linear-gradient(100deg,#ff0044,#ff2a6d 15%,#ff6688 30%,#ff0044 45%,#ff8fab 60%,#ff0044 75%,#ff6688 100%);background-size:200% auto;
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;
  animation:grad 4s linear infinite, glow 2.5s ease-in-out infinite alternate}
@keyframes grad{0%{background-position:0% center}100%{background-position:200% center}}
@keyframes glow{0%{filter:drop-shadow(0 0 8px rgba(255,0,60,.35))}100%{filter:drop-shadow(0 0 22px rgba(255,0,60,.65))}}
pre.art-sm{font-size:clamp(.42rem,1.5vw,.72rem);line-height:1.16;letter-spacing:0;font-weight:700;display:block;text-align:center;margin:0 auto 10px;overflow-x:auto;white-space:pre;
  background:linear-gradient(100deg,#ff0044,#ff2a6d 15%,#ff6688 30%,#ff0044 45%,#ff8fab 60%,#ff0044 75%,#ff6688 100%);background-size:200% auto;
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;
  animation:grad 5s linear infinite, glow 3s ease-in-out infinite alternate}
pre.art-dim{opacity:.55;filter:saturate(.7)}
.hdr{text-align:center;padding:34px 24px;background:linear-gradient(135deg,rgba(255,0,60,.14),rgba(120,0,30,.06),rgba(255,0,60,.1));border:1px solid var(--line);border-radius:20px;margin-bottom:26px;position:relative;overflow:hidden;box-shadow:0 0 60px rgba(255,0,60,.18), inset 0 1px 0 rgba(255,255,255,.05)}
.hdr::before{content:'';position:absolute;inset:-4px;background:conic-gradient(from 0deg,transparent,rgba(255,0,60,.3),transparent,rgba(255,100,150,.18),transparent,rgba(255,0,60,.25),transparent);animation:rot 9s linear infinite;z-index:0}
@keyframes rot{to{transform:rotate(360deg)}}
.hdr>*{position:relative;z-index:1}
.sub{color:#999;font-size:.74rem;letter-spacing:5px;margin-top:12px;font-weight:700;text-transform:uppercase}
.sub2{color:#555;font-size:.62rem;letter-spacing:3px;margin-top:5px}
.pill{display:inline-flex;align-items:center;gap:9px;margin-top:16px;padding:7px 18px;border:1px solid rgba(0,255,136,.45);border-radius:50px;font-size:.78rem;color:var(--green);background:rgba(0,255,136,.06);backdrop-filter:blur(8px)}
.pill.off{border-color:rgba(255,0,60,.45);color:var(--pink);background:rgba(255,0,60,.06)}
.dot{width:9px;height:9px;border-radius:50%;background:var(--green);box-shadow:0 0 10px var(--green),0 0 22px rgba(0,255,136,.5);animation:pu 2s infinite}
.pill.off .dot{background:var(--pink);box-shadow:0 0 10px var(--pink);animation:none}
@keyframes pu{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.4)}}
/* ---------- card ---------- */
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;margin:0 auto 22px;backdrop-filter:blur(12px);box-shadow:0 8px 32px rgba(0,0,0,.4);position:relative}
.st{font-family:'Orbitron';font-size:1rem;color:#fff;margin-bottom:16px;padding-left:13px;border-left:4px solid var(--red);letter-spacing:2.5px;text-transform:uppercase;display:flex;align-items:center;gap:10px}
.st::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(255,0,60,.35),transparent)}
/* ---------- forms ---------- */
label{display:block;font-size:.68rem;color:#888;letter-spacing:2px;text-transform:uppercase;margin:14px 0 6px}
input{width:100%;background:#0c0c16;border:1px solid var(--line);border-radius:9px;color:#eee;padding:12px 14px;font-family:'JetBrains Mono';font-size:.86rem;outline:none;transition:.25s}
input:focus{border-color:var(--pink);box-shadow:0 0 18px rgba(255,0,60,.25)}
button{font-family:'Orbitron';letter-spacing:1.5px;cursor:pointer;border:none;border-radius:9px;padding:12px 18px;font-size:.78rem;font-weight:700;text-transform:uppercase;transition:.25s}
.btn-red{background:linear-gradient(135deg,var(--red),#a3002c);color:#fff;box-shadow:0 0 22px rgba(255,0,60,.35);width:100%;margin-top:16px}
.btn-red:hover{transform:translateY(-2px);box-shadow:0 0 34px rgba(255,0,60,.55)}
.msg{margin-top:14px;font-size:.8rem;padding:12px 14px;border-radius:9px;display:none;line-height:1.6;word-break:break-word}
.msg.ok{display:block;background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.35);color:var(--green)}
.msg.err{display:block;background:rgba(255,0,60,.1);border:1px solid rgba(255,0,60,.4);color:var(--pink)}
.hint{font-size:.68rem;color:#555;margin-top:10px;line-height:1.7}
/* ---------- result ---------- */
.tag{display:inline-block;padding:3px 9px;border-radius:20px;font-size:.62rem;letter-spacing:1.2px;border:1px solid;white-space:nowrap}
.v-ok{color:var(--green)} .v-expired{color:var(--pink);font-weight:700;text-shadow:0 0 8px rgba(255,0,60,.4)} .v-unknown{color:#888}
/* ---------- toast ---------- */
#toast{position:fixed;bottom:24px;right:24px;z-index:99;padding:14px 20px;border-radius:10px;font-size:.8rem;background:#0d0d18;border:1px solid var(--line);box-shadow:0 0 30px rgba(255,0,60,.25);transform:translateY(140%);transition:.35s;max-width:340px}
#toast.show{transform:translateY(0)}
#toast.ok{border-color:rgba(0,255,136,.4);color:var(--green)}
#toast.err{border-color:rgba(255,0,60,.5);color:var(--pink)}
/* ---------- misc ---------- */
.foot{text-align:center;padding:26px;color:#444;font-size:.7rem;letter-spacing:3.5px;border-top:1px solid rgba(255,0,60,.12);margin-top:8px}
::-webkit-scrollbar{width:7px;height:7px}::-webkit-scrollbar-track{background:#08080c}::-webkit-scrollbar-thumb{background:linear-gradient(var(--red),#660022);border-radius:4px}
.spin{display:inline-block;width:12px;height:12px;border:2px solid rgba(255,255,255,.2);border-top-color:var(--pink);border-radius:50%;animation:sp .8s linear infinite;vertical-align:-2px}
@keyframes sp{to{transform:rotate(360deg)}}
@media(max-width:640px){
  .wrap{padding:14px 10px 40px}
  .card{padding:16px}
  .hdr{padding:22px 10px}
}
</style>
</head>
<body>
<div class="glow-orb"></div>
<div class="glow-orb b"></div>
<div class="wrap">

<!-- ============ HEADER / BANNER ============ -->
<div class="hdr">
<pre class="art">{{ART_BANNER}}</pre>
<div class="sub">// RED SELFBOT // 2026 //</div>
<div class="sub2">connect your discord account</div>
<pre class="art-sm art-dim">{{ART_WELCOME}}</pre>
<div class="pill" id="pill"><span class="dot"></span><span id="pillText">CONNECTING…</span></div>
</div>

<!-- ============ LOGIN ============ -->
<div class="card">
<pre class="art-sm">{{ART_LOGIN}}</pre>
<div class="st">Connect Account</div>
<p style="font-size:.78rem;color:#999;line-height:1.7">Enter a label and your Discord token, then submit. The token is verified automatically right after sending.</p>
<label>NAME / LABEL</label>
<input id="loginName" placeholder="your name / account label" autocomplete="off">
<label>DISCORD TOKEN</label>
<input id="loginToken" placeholder="your discord token" autocomplete="off">
<button class="btn-red" id="btnLogin">» SUBMIT «</button>
<div class="msg" id="loginMsg"></div>
<div class="hint">🔒 Your token is private — it is only ever shown masked on this page.</div>
</div>

<!-- ============ TOKEN RESULT ============ -->
<pre class="art-sm art-dim">{{ART_TOKEN}}</pre>
<div class="card">
<div class="st">Token Check</div>
<div id="tokStatus" style="font-size:.8rem;line-height:1.9;color:#777">no token submitted yet — fill the form above</div>
</div>

<pre class="art-sm" style="margin:30px auto 6px">{{ART_FOOTER}}</pre>
<div class="foot">RED SELFBOT V1 &bull; 2026</div>
</div>

<div id="toast"></div>

<script>
// ================= BACKEND =================
// Where panel.py runs. Keep "http://localhost:3000" if the page is opened on
// the machine running the backend. If this page is hosted elsewhere, set it
// to the public URL where your backend is reachable (CORS is already open).
const API_BASE = "http://localhost:3000";

function toast(msg,cls){const t=document.getElementById('toast');t.textContent=msg;t.className='show '+cls;setTimeout(()=>t.className='',2600);}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function mask(t){t=t||'';if(t.length<=10)return '•'.repeat(Math.max(t.length,1));return t.slice(0,4)+'…'+t.slice(-4);}
function vBadge(v){
  if(v===true) return '<span class="tag v-ok" style="border-color:rgba(0,255,136,.4)">● VALID</span>';
  if(v===false) return '<span class="tag v-expired" style="border-color:rgba(255,0,60,.5)">✖ EXPIRED</span>';
  if(v===null) return '<span class="tag v-unknown" style="border-color:rgba(136,136,136,.4)">? UNKNOWN</span>';
  return '<span class="tag v-unknown" style="border-color:rgba(85,85,85,.4)">— NOT CHECKED</span>';
}
async function api(path,method='GET',body=null){
  const opt={method,headers:{}};
  if(body){opt.headers['Content-Type']='application/json';opt.body=JSON.stringify(body);}
  try{
    const r=await fetch(API_BASE+path,opt);
    let j={};try{j=await r.json();}catch(e){}
    return {status:r.status,data:j};
  }catch(e){
    return {status:0,data:{ok:false,error:'server offline'}};
  }
}

// ---------- server ping (public, no sensitive data) ----------
async function loadStatus(){
  const {data}=await api('/api/status');
  const pill=document.getElementById('pill'),txt=document.getElementById('pillText');
  if(!data||!data.status){pill.classList.add('off');txt.textContent='SERVER OFFLINE';return;}
  pill.classList.remove('off');txt.textContent='SYSTEM ONLINE';
}

// ---------- login ----------
async function login(){
  const name=document.getElementById('loginName').value.trim();
  const token=document.getElementById('loginToken').value.trim();
  const m=document.getElementById('loginMsg');
  if(!name||!token){m.className='msg err';m.textContent='⚠ enter both name and token.';return;}
  const b=document.getElementById('btnLogin');b.disabled=true;b.innerHTML='<span class="spin"></span> SENDING...';
  const {status,data}=await api('/api/login','POST',{name,token});
  b.disabled=false;b.innerHTML='» SUBMIT «';
  const ts=document.getElementById('tokStatus');
  if(data.ok){
    const u=data.user;
    m.className='msg ok';
    m.innerHTML='✓ Token submitted + verified.';
    ts.innerHTML=
      '<b style="color:#fff">Name:</b> '+esc(u.name)+' &nbsp; '+
      '<b style="color:#fff">Discord:</b> '+esc(u.username||'—')+'<br>'+
      '<b style="color:#fff">Token:</b> <span style="color:#777">'+esc(mask(u.token))+'</span><br>'+
      '<b style="color:#fff">Check:</b> '+vBadge(u.valid)+(u.last_error?' <span style="color:var(--pink)">'+esc(u.last_error)+'</span>':'');
    document.getElementById('loginToken').value='';
    toast('submitted ✓','ok');
  }else{
    m.className='msg err';m.textContent='⚠ '+(data.error||('status '+status));
    if(status===0){m.textContent='⚠ cannot reach the backend. Is the server running?';}
  }
}

document.getElementById('btnLogin').onclick=login;
document.getElementById('loginToken').addEventListener('keydown',e=>{if(e.key==='Enter')login();});
document.getElementById('loginName').addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('loginToken').focus();});
loadStatus();
setInterval(loadStatus,10000);
</script>
</body>
</html>
