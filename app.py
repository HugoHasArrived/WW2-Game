from flask import Flask, Response, request, jsonify

app = Flask(__name__)

GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ashes of the Dead — Alcatraz Escape</title>
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#030506;color:#eee;font-family:Consolas,monospace;overflow:hidden}body{display:grid;place-items:center}.shell{position:relative;width:min(100vw,1280px);aspect-ratio:16/9;background:#080b0e;overflow:hidden;box-shadow:0 0 70px #000}canvas{display:block;width:100%;height:100%;image-rendering:pixelated;image-rendering:crisp-edges;background:#080b0e}.layer{position:absolute;inset:0}.hidden{display:none!important}.notice,.menu,.pause{display:grid;place-items:center;background:rgba(2,3,4,.96);z-index:50}.cutscene{display:grid;place-items:center;background:rgba(0,0,0,.12);z-index:50}.panel{max-width:900px;padding:34px;border:2px solid #555b5d;background:linear-gradient(180deg,#0b0e10,#060809);box-shadow:0 0 90px #000,0 0 12px rgba(150,145,130,.12);position:relative;overflow:hidden}.panel:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.018) 0,rgba(255,255,255,.018) 1px,transparent 1px,transparent 5px);pointer-events:none}.panel:after{content:'';position:absolute;left:-20%;top:0;width:30%;height:100%;background:rgba(180,180,160,.025);transform:skewX(-18deg);animation:menuScan 5s linear infinite;pointer-events:none}.panel h1{letter-spacing:8px;margin:0 0 12px;font-size:42px;text-shadow:4px 4px #000,0 0 22px rgba(190,190,170,.12)}.panel p{color:#aaa;line-height:1.65}.panel button{font:inherit;color:#ddd;background:#101416;border:1px solid #62696b;padding:13px 25px;margin:7px;cursor:pointer;position:relative;transition:.12s;box-shadow:inset 0 0 0 1px rgba(255,255,255,.025)}.panel button:hover{background:#1b2022;border-color:#9a9a8d;transform:translateY(-1px);box-shadow:0 0 18px rgba(150,145,130,.12)}.name{display:flex;flex-wrap:wrap;justify-content:center}.title{text-align:center;letter-spacing:7px;font-size:36px}.subtitle{text-align:center;color:#888;letter-spacing:4px;margin-bottom:20px}.controls{font-size:12px;color:#777;text-align:center;line-height:1.8;margin-top:18px}.menu-intro{text-align:center;color:#666;font-size:11px;letter-spacing:2px;margin:10px 0 18px}.menu-warning{text-align:center;color:#7d4b48;font-size:10px;letter-spacing:3px;margin-top:20px}.menu-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.menu-grid button{width:100%;margin:0}.menu-pixel{height:42px;margin:8px 0 16px;background:repeating-linear-gradient(90deg,#161b1d 0,#161b1d 7px,#0b0e10 7px,#0b0e10 11px);border-top:1px solid #303638;border-bottom:1px solid #303638;opacity:.8}@keyframes menuScan{0%{left:-35%}100%{left:120%}}.cutscene{padding:35px;text-align:center}.cutline{max-width:930px;font-size:clamp(18px,2.6vw,32px);line-height:1.55;text-shadow:3px 3px #000;margin-top:250px}.cutmeta{position:absolute;bottom:20px;right:20px;color:#666;font-size:12px}.hud{pointer-events:none;z-index:10}.hudtop{position:absolute;left:18px;right:18px;top:14px;display:flex;justify-content:space-between;text-shadow:2px 2px #000;font-size:12px}.bar{width:190px;height:9px;border:1px solid #777;background:#111;margin:3px 0 8px}.fill{height:100%;width:100%}.hp{background:#a84a46}.stam{background:#8b8f76}.san{background:#716b91}.objective{position:absolute;left:18px;top:105px;max-width:440px;color:#ddd;text-shadow:2px 2px #000}.message{position:absolute;left:50%;bottom:55px;transform:translateX(-50%);padding:9px 16px;background:rgba(5,7,8,.82);border:1px solid #454b4f;color:#ddd}.prompt{position:absolute;left:50%;bottom:24px;transform:translateX(-50%);color:#bbb;text-shadow:2px 2px #000}.cross{position:absolute;left:50%;top:50%;width:12px;height:12px;transform:translate(-50%,-50%);opacity:.7}.cross:before,.cross:after{content:"";position:absolute;background:#ddd}.cross:before{width:12px;height:1px;top:5px}.cross:after{height:12px;width:1px;left:5px}.watch{color:#b7aaa4}.inventory{position:absolute;right:18px;top:95px;background:rgba(4,5,6,.84);border:1px solid #3e4447;padding:10px;min-width:210px;font-size:12px}.map{position:absolute;right:18px;bottom:18px;width:190px;height:70px;border:1px solid #555;background:rgba(0,0,0,.55)}.fade{position:absolute;inset:0;background:#000;opacity:0;pointer-events:none;z-index:40}.vignette{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.72) 100%);opacity:.8}.warning{position:absolute;left:50%;top:22%;transform:translateX(-50%);font-size:22px;letter-spacing:4px;color:#c9b9b0;text-shadow:0 0 12px #000,3px 3px #000}.privacy-small{font-size:11px;color:#777;margin-top:18px}
</style>
</head>
<body>
<div class="shell">
<canvas id="game" width="1280" height="720"></canvas>
<div id="notice" class="layer notice"><div class="panel"><h1>PRIVACY & SAFETY NOTICE</h1><p>This is a fictional horror game. It does not access your camera, microphone, files, passwords, contacts, browser history, accounts, or identity. The game server can see the network address used to connect to it, and NIGHTWATCH may display limited browser/device information. Location is only read after you explicitly grant browser location permission.</p><p>Any surveillance screens, names, locations, network messages, or similar information shown during gameplay are <b>fictional game effects</b>. <b>The Smiler is fictional and cannot actually watch you.</b></p><button id="accept">I UNDERSTAND — ENTER THE GAME</button><div class="privacy-small">You can open this notice again from the pause menu.</div></div></div>
<div id="menu" class="layer menu hidden"><div class="panel"><div class="title">ASHES OF THE DEAD</div><div class="subtitle">THE ALCATRAZ ESCAPE</div><div class="menu-intro">ALCATRAZ ISLAND • 11:47 PM • SAN FRANCISCO BAY</div><div class="menu-pixel"></div><p style="text-align:center">Three detectives. One island. Nobody is coming.</p><div class="name menu-grid"><button data-name="Julia">JULIA<br><small>DETECTIVE</small></button><button data-name="May">MAY<br><small>DETECTIVE</small></button><button data-name="Yumi">YUMI<br><small>DETECTIVE</small></button></div><div style="text-align:center;color:#8b857a;font-size:11px;line-height:1.7;margin:14px 0">SURVIVAL MATTERS: SEARCH ROOMS, SAVE AMMO, USE MEDKITS, FOLLOW CLUES, TALK TO SURVIVORS, AND NEVER ASSUME A DARK ROOM IS EMPTY.</div><div class="menu-warning">HEADPHONES RECOMMENDED • LIGHTS OFF • KEEP YOUR EYES ON THE CORRIDOR</div><div class="controls">A / D or ARROWS — MOVE &nbsp; SHIFT — RUN &nbsp; SPACE / W — JUMP<br>E — INTERACT / ENTER STRUCTURES &nbsp; I — INVENTORY &nbsp; TAB — GADGET<br>MOUSE — AIM / SHOOT &nbsp; R — RELOAD &nbsp; F — FLASHLIGHT &nbsp; Q — MELEE &nbsp; G — GRENADE &nbsp; ESC — PAUSE</div></div></div>
<div id="cutscene" class="layer cutscene hidden"><div><div id="cutline" class="cutline"></div><div class="cutmeta">ENTER / SPACE — continue &nbsp; • &nbsp; ESC — skip</div></div></div>
<div id="pause" class="layer pause hidden"><div class="panel"><h1>PAUSED</h1><p id="pauseText">The rain keeps falling.</p><button id="resume">RESUME</button><button id="restart">RESTART CHAPTER</button><button id="privacy">PRIVACY NOTICE</button></div></div>
<div id="ending" class="layer notice hidden"><div class="panel"><h1>YOU SURVIVED — FOR NOW</h1><p id="endingText"></p><p>The story ends here. The last camera frame is still moving.</p><button id="endingRestart">RETURN TO MENU</button></div></div>
<div id="hud" class="layer hud hidden"><div class="hudtop"><div><div>HEALTH</div><div class="bar"><div id="hp" class="fill hp"></div></div><div>STAMINA</div><div class="bar"><div id="stam" class="fill stam"></div></div><div>SANITY</div><div class="bar"><div id="san" class="fill san"></div></div></div><div style="text-align:right"><div>ALCATRAZ ISLAND</div><div class="watch" id="watch">THE SMILER IS WATCHING</div><div id="ammo">AMMO 12 / 12</div></div></div><div class="objective" id="objective">OBJECTIVE</div><div class="message" id="message"></div><div class="prompt" id="prompt"></div><div class="cross"></div><div id="inventory" class="inventory hidden"></div><canvas id="map" class="map" width="380" height="140"></canvas><div class="vignette"></div><div id="warning" class="warning hidden"></div></div>
<div id="infoScare" class="layer hidden" style="z-index:80;pointer-events:none;background:rgba(0,0,0,.82);display:grid;place-items:center"><div id="infoScareBox" style="width:min(940px,92%);padding:30px;border:3px solid #9b2020;background:rgba(3,4,5,.97);box-shadow:0 0 120px #000,0 0 42px #7e1717;transform:skewX(-1deg);position:relative;overflow:hidden"><div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.025) 0,rgba(255,255,255,.025) 1px,transparent 1px,transparent 4px);mix-blend-mode:screen"></div><div style="font-size:13px;letter-spacing:5px;color:#b9b0a6">NIGHTWATCH // UNEXPECTED DATA</div><div id="infoScareTitle" style="font-size:34px;letter-spacing:3px;margin:12px 0;color:#e7ded0">DEVICE RECORD FOUND</div><div id="infoScareText" style="font-size:17px;line-height:1.8;color:#d4cdca;white-space:pre-line"></div><div id="infoScareFoot" style="margin-top:18px;font-size:11px;color:#756f6b">SERVER-VISIBLE / BROWSER-REPORTED DATA</div></div></div>
<div id="gadget" class="layer hidden" style="z-index:45;background:rgba(2,3,5,.95);padding:34px"><div style="width:min(860px,92%);margin:20px auto;border:2px solid #59636a;background:#090d10;padding:22px;box-shadow:0 0 40px #000"><div style="font-size:22px;letter-spacing:4px">NIGHTWATCH // HANDHELD</div><div style="margin-top:14px;color:#9ea7a8">SAFE DEVICE DIAGNOSTICS</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:16px;font-size:13px"><div>DEVICE: <span id="gdevice">Browser Device</span></div><div>ONLINE: <span id="gonline">YES</span></div><div>SCREEN: <span id="gscreen">1280x720</span></div><div>LANGUAGE: <span id="glang">en</span></div><div>PLATFORM: <span id="gplatform">Browser</span></div><div>CPU THREADS: <span id="gcput">-</span></div><div>BATTERY: <span id="gbat">-</span></div><div>NETWORK: <span id="gnet">-</span></div></div><div style="margin-top:18px;border-top:1px solid #343b3f;padding-top:14px">SERVER-SEEN IP: <span id="gip">READING...</span></div><div>LOCATION: <span id="gloc">PERMISSION REQUIRED</span> <button id="locateBtn" style="margin-left:8px;padding:5px 9px;background:#151a1d;color:#cfd5d6;border:1px solid #59636a;cursor:pointer">SHARE LOCATION</button></div><div style="margin-top:8px">DEVICE PERMISSION CHECK: <button id="deviceCheckBtn" style="margin-left:8px;padding:5px 9px;background:#151a1d;color:#cfd5d6;border:1px solid #59636a;cursor:pointer">CHECK CAMERA / MIC</button> <span id="deviceCheck" style="color:#888">NOT CHECKED</span></div><div>DEVICE: <span id="gdevice2">READING...</span></div><div>BROWSER: <span id="gbrowser">READING...</span></div><div>CAMERA: <span id="gcam">NOT ACCESSED</span></div><div>MICROPHONE: <span id="gmic">NOT ACCESSED</span></div><div style="margin-top:18px;height:170px;border:1px solid #343b3f;background:#030506;display:grid;place-items:center;color:#626a6c"><span id="gfeed">LOCAL GAME GADGET — NO CAMERA, MIC, FILE OR PASSWORD ACCESS</span></div><div style="margin-top:14px;color:#777">TAB — CLOSE GADGET &nbsp; • &nbsp; Standard browser diagnostics only.</div></div></div><div id="fade" class="fade"></div>
</div>
<script>
'use strict';
const C=document.getElementById('game');
const ctx=C.getContext('2d');
ctx.imageSmoothingEnabled=false;
const MAP=document.getElementById('map');
const mctx=MAP.getContext('2d');
const W=1280,H=720,G=570,WORLD=8200;
const keys=new Set();
const mouse={x:640,y:360,down:false};let audioCtx=null;
function jumpSound(){try{if(!audioCtx)audioCtx=new (window.AudioContext||window.webkitAudioContext)();const now=audioCtx.currentTime;const o=audioCtx.createOscillator(),g=audioCtx.createGain();o.type='sawtooth';o.frequency.setValueAtTime(110,now);o.frequency.exponentialRampToValueAtTime(38,now+.32);g.gain.setValueAtTime(.0001,now);g.gain.exponentialRampToValueAtTime(.18,now+.015);g.gain.exponentialRampToValueAtTime(.0001,now+.55);o.connect(g);g.connect(audioCtx.destination);o.start(now);o.stop(now+.6);}catch(e){}}
async function requestRealLocation(){const el=document.getElementById('gloc');if(!navigator.geolocation){el.textContent='UNAVAILABLE';return;}el.textContent='REQUESTING PERMISSION...';navigator.geolocation.getCurrentPosition(pos=>{const a=pos.coords.latitude.toFixed(5),o=pos.coords.longitude.toFixed(5);realLocation=a+', '+o;el.textContent=realLocation;setMsg('LOCATION SHARED WITH NIGHTWATCH',1.5);},()=>{el.textContent='DENIED OR UNAVAILABLE';setMsg('LOCATION NOT SHARED',1.2);},{enableHighAccuracy:false,maximumAge:60000,timeout:8000});}
async function checkDevicePermission(){const out=document.getElementById('deviceCheck');if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){out.textContent='UNAVAILABLE';return;}out.textContent='REQUESTING...';try{const stream=await navigator.mediaDevices.getUserMedia({video:true,audio:true});stream.getTracks().forEach(x=>x.stop());out.textContent='PERMISSION GRANTED / STREAM STOPPED';setMsg('Camera and microphone were checked and immediately released.',2);}catch(e){out.textContent='DENIED OR UNAVAILABLE';setMsg('No camera or microphone access was granted.',2);}}
async function loadServerInfo(){try{const r=await fetch('/gadget',{cache:'no-store'});if(r.ok){const d=await r.json();serverInfo.ip=d.server_seen_ip||'UNAVAILABLE';}}catch(e){serverInfo.ip='UNAVAILABLE';}serverInfo.ua=navigator.userAgent||'UNKNOWN';serverInfo.platform=navigator.platform||'UNKNOWN';serverInfo.language=navigator.language||'UNKNOWN';}
function triggerInfoScare(force=false){if(mode!=='play'||gadgetOpen||infoScare>0)return;if(!force&&infoScareCooldown>0)return;infoScare=1.7;infoScareCooldown=rnd(90,180);const title=document.getElementById('infoScareTitle'),body=document.getElementById('infoScareText'),foot=document.getElementById('infoScareFoot');const roll=Math.floor(Math.random()*4);title.textContent=['NETWORK SNAPSHOT','DEVICE SNAPSHOT','SESSION TIME','LOCATION STATUS'][roll];if(roll===0)body.textContent='SERVER-SEEN IP: '+serverInfo.ip+'\nCONNECTION: '+(navigator.onLine?'ONLINE':'OFFLINE');else if(roll===1)body.textContent='DEVICE: '+(navigator.platform||'UNKNOWN')+'\nSCREEN: '+screen.width+' x '+screen.height;else if(roll===2)body.textContent='LOCAL TIME: '+new Date().toLocaleTimeString()+'\nTIME ZONE: '+(Intl.DateTimeFormat().resolvedOptions().timeZone||'UNKNOWN');else body.textContent='LOCATION: '+(realLocation||'NOT SHARED')+'\nPERMISSION-BASED ONLY';foot.textContent='LIMITED SESSION DATA — NO FILES, PASSWORDS, CAMERA OR MICROPHONE CONTENT';shake=10;flash=.12;scareSound(false);document.getElementById('infoScare').classList.remove('hidden');}
function updateInfoScare(dt){if(infoScare>0){infoScare-=dt;const box=document.getElementById('infoScareBox');box.style.transform='translateX('+(Math.sin(t*95)*5)+'px) skewX('+(Math.sin(t*43)*1.8)+'deg)';box.style.filter='contrast('+(1.1+Math.abs(Math.sin(t*31))*.65)+')';if(infoScare<=0){document.getElementById('infoScare').classList.add('hidden');box.style.transform='skewX(-1deg)';box.style.filter='none';}}else if(infoScareCooldown>0)infoScareCooldown-=dt;if(mode==='play'&&infoScare<=0&&infoScareCooldown<=0&&Math.random()<dt*.004){triggerInfoScare();}}
function triggerJumpScare(){if(jumpScare>0||gadgetOpen||mode!=='play')return;jumpScare=.92;jumpType=Math.floor(Math.random()*8);shake=26;flash=.3;p.sanity=clamp(p.sanity-16,0,100);if(jumpType===6||jumpType===7)p.hp=clamp(p.hp-8,0,100);jumpSound();scareSound(true);setMsg(jumpType%3===0?'IT WAS BEHIND YOU.':jumpType%3===1?'DON’T LOOK.':'TOO CLOSE.',1.4);terrorStage=0;terrorLife=0;}
function scareSound(close=false){try{if(!audioCtx)audioCtx=new (window.AudioContext||window.webkitAudioContext)();const o=audioCtx.createOscillator(),g=audioCtx.createGain();o.type=close?'sawtooth':'sine';o.frequency.setValueAtTime(close?55:32,audioCtx.currentTime);o.frequency.exponentialRampToValueAtTime(close?22:17,audioCtx.currentTime+(close?.7:1.4));g.gain.setValueAtTime(.0001,audioCtx.currentTime);g.gain.exponentialRampToValueAtTime(close?.06:.025,audioCtx.currentTime+.04);g.gain.exponentialRampToValueAtTime(.0001,audioCtx.currentTime+(close?1.0:1.7));o.connect(g);g.connect(audioCtx.destination);o.start();o.stop(audioCtx.currentTime+(close?1.1:1.8));if(close){const n=audioCtx.createOscillator(),ng=audioCtx.createGain();n.type='square';n.frequency.value=140;ng.gain.setValueAtTime(.0001,audioCtx.currentTime);ng.gain.exponentialRampToValueAtTime(.025,audioCtx.currentTime+.02);ng.gain.exponentialRampToValueAtTime(.0001,audioCtx.currentTime+.22);n.connect(ng);ng.connect(audioCtx.destination);n.start();n.stop(audioCtx.currentTime+.25);}}catch(e){}}
let mode='notice',name='Julia',t=0,last=0,cam=0,shake=0,flash=0,lightning=0,heartbeat=0,ambientPulse=0,lightFlicker=1,gadgetOpen=false,jumpScare=0,jumpType=0,jumpCooldown=8;let horrorTimer=24,horrorEvent=0,horrorLife=0,horrorX=0,horrorDamage=0,horrorBlackout=0,horrorWhisper=0,horrorDoor=0,horrorLunge=0;let terrorTimer=32,terrorStage=0,terrorLife=0,terrorX=0,terrorType=0;
let realLocation='NOT SHARED';let infoScare=0,infoScareCooldown=90,gadgetPoll=0,serverInfo={ip:'UNAVAILABLE',ua:'UNKNOWN',platform:'UNKNOWN',language:'UNKNOWN'};
let objective='';let message='';let messageUntil=0;let prompt='';
let zombies=[],vehicles=[],buildings=[],survivors=[],loot=[],chests=[],bullets=[],particles=[],rain=[],shells=[],blood=[],doors=[],interior=null;
let alcatrazEscaped=false,boatReady=false,fuel=0,alarm=0,hordeTimer=26,smilerTimer=11,smiler={active:false,x:0,ttl:0,phase:0,close:false,glitch:0,stare:0};
let chapter='ALCATRAZ',escapeTransition=0,worldFear=0;
let inv={ammo:0,medkit:0,fuel:0,battery:0,grenade:0,key:0};
let interiorState=null,interiorCam=0,interiorWidth=3200;
let storyStage=0,ending=false,dockPass=false,alcatrazBlocks={a:false,b:false};
let startCell=true,cellKey=false,cellDoorOpen=false,cellInspected={bed:false,window:false,note:false},gameStarted=false,gunshotTimer=0;
let cutLines=[],cutIndex=0,cutTimer=0;
let p={x:160,y:G-64,w:34,h:64,vx:0,vy:0,ground:true,face:1,hp:100,stam:100,sanity:100,ammo:12,maxAmmo:12,reload:0,grenades:2,light:true,anim:0,kills:0,shots:0,run:false,invuln:0};
const COLORS={sky:'#0b1117',sky2:'#121b22',ground:'#262a2c',ground2:'#303337',metal:'#555c60',rust:'#70443b',wood:'#4d4137',window:'#11181c',light:'#a8a48b',fog:'#192126',skin:'#c8a58d'};
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const rnd=(a,b)=>a+Math.random()*(b-a);
function rect(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));}
function line(x1,y1,x2,y2,c='#aaa',lw=1){ctx.strokeStyle=c;ctx.lineWidth=lw;ctx.beginPath();ctx.moveTo(Math.round(x1),Math.round(y1));ctx.lineTo(Math.round(x2),Math.round(y2));ctx.stroke();}
function txt(s,x,y,size=14,c='#ddd',align='left'){ctx.fillStyle=c;ctx.font=size+'px monospace';ctx.textAlign=align;ctx.fillText(s,x,y);}
function setObj(s){objective=s;document.getElementById('objective').textContent='OBJECTIVE: '+s;}
function setMsg(s,d=3){message=s;messageUntil=t+d;document.getElementById('message').textContent=s;}
function spawnParticle(x,y,c='#aaa',life=.5,size=2,vx=0,vy=0){particles.push({x,y,c,life,size,vx,vy});}
function spawnBlood(x,y){for(let i=0;i<8;i++)spawnParticle(x+rnd(-4,4),y+rnd(-4,4),'#7e403b',rnd(.25,.65),rnd(1,3),rnd(-35,35),rnd(-65,15));}
function addBuilding(x,w,h,name,type='prison',locked=false){const words={prison:['DON’T OPEN','HE IS HERE','RUN','A-17','NO LIGHT'],office:['THEY LEFT US','LOCK THE DOOR','NO SIGNAL'],medical:['KEEP QUIET','DO NOT SLEEP','QUARANTINE'],cafeteria:['DON’T EAT','THE SCREAMING','HELP'],workshop:['STAY AWAY','HEAR THAT?','RUN'],armory:['EMPTY','TAKE NOTHING','LOCKED'],power:['DO NOT CUT POWER','LIGHTS OUT = RUN','NO'],warehouse:['DON’T LOOK UP','HELP ME','THE DOOR MOVED'],barracks:['SOMEONE IS INSIDE','WAKE UP','RUN'],house:['WE HEARD HIM','DO NOT KNOCK','HELP'],hotel:['ROOMS ARE NOT EMPTY','DON’T TURN AROUND','LEAVE'],military:['DO NOT ENTER','CLASSIFIED','ABANDONED'],church:['HE SMILES','PRAY','DON’T LOOK'],hospital:['THEY AREN’T DEAD','QUIET','NO PATIENTS'],safehouse:['SAFE?','KEEP WATCH','LOCKED'],lab:['PROJECT CLOSED','SUBJECT MISSING','DO NOT OPEN']};buildings.push({x,w,h,name,type,locked,open:false,interior:false,insideLoot:[],insideZombies:[],writings:words[type]||['RUN','HELP','HE IS HERE']});}
function addVehicle(x,y,w,type,broken=false,usable=false){vehicles.push({x,y,w,h:type==='tank'?42:34,type,broken,usable,driving:false,angle:0});}
function addLoot(x,y,type,label,amount=1,inside=null){loot.push({x,y,type,label,amount,got:false,inside});}
function addChest(x,y,label='SUPPLY CHEST',inside=null){chests.push({x,y,label,open:false,inside,lootMade:false});}
function addSurvivor(x,name,role){survivors.push({x,y:G-62,w:32,h:62,name,role,state:'idle',talked:false,anim:rnd(0,8),hp:100,follow:false});}
function spawnZombie(x,type='walker',y=G-58,inside=null){if(chapter!=='SAN FRANCISCO')return null;if(zombies.filter(z=>!z.dead).length>=6)return null;let z={x,y,w:type==='brute'?58:type==='runner'?32:38,h:type==='brute'?78:60,type,hp:type==='brute'?170:type==='runner'?55:42,vx:0,vy:0,ground:true,attack:rnd(.2,1),anim:rnd(0,20),dead:false,inside,alert:0};zombies.push(z);return z;}
function buildWorld(){
 buildings=[];vehicles=[];survivors=[];loot=[];zombies=[];doors=[];
 addBuilding(210,250,245,'Cell Block A','prison',true);
 addBuilding(535,250,245,'Cell Block B','prison',true);
 addBuilding(860,190,185,'Guard Station','office',true);
 addBuilding(1110,270,235,'Medical Wing','medical',true);
 addBuilding(1450,240,200,'Kitchen & Cafeteria','cafeteria',true);
 addBuilding(1760,230,215,'Workshop','workshop',true);
 addBuilding(2050,270,250,'Armory','armory',true);
 addBuilding(2390,220,205,'Power Station','power',true);
 addBuilding(2690,270,220,'Dock Warehouse','warehouse',true);
 addBuilding(3030,210,175,'Barracks','barracks',true);
 addBuilding(3340,300,255,'Island Command','office',true);
 addBuilding(3720,250,205,'Quarantine Clinic','medical',true);
 addBuilding(4050,280,225,'Coast Guard House','house',true);
 addBuilding(4410,300,250,'Ruined Village House','house',true);
 addBuilding(4790,300,245,'Abandoned Hotel','hotel',true);
 addBuilding(5200,340,275,'Military Depot','military',true);
 addBuilding(5670,300,250,'Church','church',true);
 addBuilding(6100,330,285,'Hospital','hospital',true);
 addBuilding(6560,300,245,'Safehouse','safehouse',true);
 addBuilding(7000,350,270,'Research Facility','lab',true);
 addVehicle(80,G-34,100,'jeep',true,false);
 addVehicle(720,G-36,140,'truck',false,true);
 addVehicle(1250,G-34,110,'car',true,false);
 addVehicle(1870,G-42,170,'tank',true,false);
 addVehicle(2840,G-34,125,'jeep',false,true);
 addVehicle(3460,G-36,140,'truck',true,false);
 addVehicle(4300,G-34,115,'car',true,false);
 addVehicle(5050,G-36,150,'truck',false,true);
 addVehicle(5860,G-34,125,'jeep',true,false);
 addVehicle(6350,G-34,120,'car',true,false);
 addVehicle(6800,G-36,155,'truck',false,true);
 addVehicle(7480,G-25,220,'boat',true,false);
 addLoot(760,G-24,'ammo','Ammunition',8); addLoot(1030,G-24,'medkit','Medical Kit');
 addLoot(1530,G-24,'ammo','Ammunition',12); addLoot(2140,G-24,'fuel','Fuel Can');
 addLoot(2580,G-24,'battery','Generator Battery'); addLoot(3190,G-24,'ammo','Ammunition',12);
 addLoot(3910,G-24,'grenade','Grenade',2); addLoot(4560,G-24,'medkit','Medical Kit');
 addLoot(5000,G-24,'fuel','Fuel Can'); addLoot(5750,G-24,'ammo','Ammunition',15);
 addLoot(6240,G-24,'medkit','Medical Kit'); addLoot(6650,G-24,'fuel','Fuel Can');
 addLoot(6910,G-24,'medkit','Medical Kit');
 addChest(460,G-24,'CELL BLOCK A CHEST');addChest(1760,G-24,'CELL BLOCK B CHEST');addChest(2740,G-24,'DOCK SUPPLY CHEST');addChest(5180,G-24,'MILITARY SUPPLY CHEST');addChest(6430,G-24,'SAFEHOUSE CHEST');
 for(const b of buildings.filter(q=>q.type==='prison')){
   b.cells=[];
   for(let i=0;i<20;i++)b.cells.push({id:i+1,opened:false,searched:false,loot:false});
 }
 rain=[];for(let i=0;i<260;i++)rain.push({x:rnd(0,W),y:rnd(-700,H),v:rnd(330,560),len:rnd(10,22)});
}
function intro(){
 cutLines=[
 'ALCATRAZ — 11:47 PM',
 'You wake alone in Cell A-17. Rain. Concrete. A locked door.',
 'The light flickers. Something impossibly tall stands at the end of the corridor.',
 'It does not move. It only smiles. The light dies. When it returns, nothing is there.',
 'The lock clicks open. ESCAPE ALCATRAZ.'
 ];cutIndex=0;cutTimer=0;mode='intro';document.getElementById('cutscene').classList.remove('hidden');showCut();}
function showCut(){const el=document.getElementById('cutline');el.textContent=cutLines[cutIndex]||'';}
function nextCut(){cutIndex++;if(cutIndex>=cutLines.length)finishIntro();else{cutTimer=0;showCut();}}
function finishIntro(){document.getElementById('cutscene').classList.add('hidden');document.getElementById('hud').classList.remove('hidden');mode='play';buildWorld();p={...p,x:180,y:G-64,hp:100,stam:100,sanity:100,ammo:12,reload:0,grenades:2,kills:0,shots:0,invuln:0,light:false};cam=0;interior='OPENING_CELL';startCell=true;cellKey=false;cellDoorOpen=false;cellInspected={bed:false,window:false,note:false};gameStarted=true;alarm=0;fuel=0;boatReady=true;dockPass=false;storyStage=0;ending=false;alcatrazBlocks={a:false,b:false};interiorCam=0;inv={ammo:0,medkit:0,fuel:0,battery:0,grenade:0,key:0};setObj('Search Cell A-17. Find the key and get into the cell block.');setMsg('Cold concrete. Rain beyond the bars. You are alone.',4);}
function resetChapter(){terrorTimer=10+Math.random()*8;terrorStage=0;terrorLife=0;document.getElementById('pause').classList.add('hidden');document.getElementById('hud').classList.remove('hidden');mode='play';buildWorld();p={x:180,y:G-64,w:34,h:64,vx:0,vy:0,ground:true,face:1,hp:100,stam:100,sanity:100,ammo:12,maxAmmo:12,reload:0,grenades:2,light:false,anim:0,kills:0,shots:0,run:false,invuln:0};cam=0;interior='OPENING_CELL';startCell=true;cellKey=false;cellDoorOpen=false;cellInspected={bed:false,window:false,note:false};alcatrazEscaped=false;boatReady=true;fuel=0;dockPass=false;storyStage=0;ending=false;alcatrazBlocks={a:false,b:false};interiorCam=0;inv={ammo:0,medkit:0,fuel:0,battery:0,grenade:0,key:0};smiler.active=false;alarm=0;chapter='ALCATRAZ';worldFear=0;gameStarted=true;setObj('Search the cell. Find a way out.');setMsg('Chapter restarted.',2);}
function playerRect(){return {x:p.x,y:p.y,w:p.w,h:p.h};}
function near(a,b,d){return Math.abs(a-b)<d;}
function getBuilding(){let best=null,bd=99999;for(const b of buildings){const d=Math.abs((b.x+b.w/2)-p.x);if(d<bd&&d<b.w/2+65){best=b;bd=d;}}return best;}
function getVehicle(){let best=null,bd=99999;for(const v of vehicles){const d=Math.abs(v.x+v.w/2-p.x);if(d<bd&&d<100){best=v;bd=d;}}return best;}
function getSurvivor(){let best=null,bd=99999;for(const s of survivors){const d=Math.abs(s.x-p.x);if(d<bd&&d<90){best=s;bd=d;}}return best;}
function getChest(){let best=null,bd=99999;for(const c of chests){if(c.open)continue;if(c.inside&&c.inside!==interior)continue;const d=Math.abs(c.x-p.x);if(d<bd&&d<75){best=c;bd=d;}}return best;}
function getLoot(){let best=null,bd=99999;for(const l of loot){if(l.got)continue;if(l.inside){const ok=l.inside===interior||(interiorState&&interiorState.cellView&&l.inside===interior+'#'+interiorState.cell.id);if(!ok)continue;}const d=Math.abs(l.x-p.x);if(d<bd&&d<65){best=l;bd=d;}}return best;}
function interact(){
 if(mode!=='play')return;
 const chest=getChest();
 if(chest){openChest(chest);return;}
 if(startCell){
  const cx=p.x;
  if(!cellInspected.bed && cx<300){cellInspected.bed=true;setMsg('An empty mattress. The blanket is still warm.',3);return;}
  if(!cellInspected.note && cx>=300&&cx<520){cellInspected.note=true;cellKey=true;setMsg('A brass key is hidden beneath a loose note.',3);setObj('Unlock the cell door.');return;}
  if(!cellInspected.window && cx>=520&&cx<700){cellInspected.window=true;p.sanity=clamp(p.sanity-3,0,100);setMsg('Black water. San Francisco is only a smear of light.',3);return;}
  if(cellKey&&cx>=900){startCell=false;cellDoorOpen=true;interior=null;p.x=315;setObj('Explore Cell Block A and Cell Block B. Search the cells for the dock pass.');setMsg('The lock opens. Beyond it: rows of cells, blood writing, and skeletons.',3);alarm=.12;return;}
  setMsg(cellKey?'Move to the cell door and press E.':'Search the bed, note, and window.',2);return;
 }
 if(interiorState){
  const b=interiorState.building;
  const l=getLoot();if(l){collectLoot(l);return;}
  if(b.type==='prison'){
   if(interiorState.cellView){
    if(p.x>interiorWidth-260){leavePrisonCell();return;}
    if(!interiorState.cellSearched){interiorState.cellSearched=true;const id=interiorState.cell.id;if(id===7&&!dockPass){dockPass=true;inv.key++;setMsg('Behind the loose brick: a DOCK PASS. Someone scratched “DON’T LET HIM BOARD.”',4);setObj('Find the second cell block. Search for a route to the dock.');}else if(id%5===0){addLoot(650,G-24,'ammo','Ammunition',4,interiorState.building.name+'#'+id);setMsg('A hidden cache. Something was recently disturbed.',2.5);}else setMsg('The cell is empty, but the scratches are fresh.',2);return;}
    setMsg('Nothing else here. Check another cell.',1.5);return;
   }
   const cell=nearestPrisonCell();
   if(cell){enterPrisonCell(cell);return;}
   if(p.x>interiorWidth-180){const outside=b.x+b.w/2+70;interiorState=null;interior=null;interiorCam=0;p.x=outside;cam=clamp(p.x-390,0,WORLD-W);if(b.name==='Cell Block A'){alcatrazBlocks.a=true;setObj('Enter Cell Block B. Search it for the dock pass.');}else{alcatrazBlocks.b=true;setObj(dockPass?'Reach the dock and board the ready boat.':'Search Cell Block B for the dock pass.');}setMsg('You step back into the rain.',2);return;}
   setMsg('A long cell corridor. Twenty doors. Search them.',1.8);return;
  }
  if(chapter==='SAN FRANCISCO'&&b.name==='Research Annex'&&storyStage===1&&p.x>2200&&p.x<2750){storyStage=2;setMsg('A terminal reveals the outbreak was contained here. You found the evacuation route.',4);setObj('Bring the survivors to the Emergency Shelter.');return;}
  if(p.x>interiorWidth-180){const outside=b.x+b.w/2+70;interiorState=null;interior=null;interiorCam=0;p.x=outside;cam=clamp(p.x-390,0,WORLD-W);setObj(chapter==='SAN FRANCISCO'?'Search San Francisco.':'Explore the empty prison.');setMsg('You step back outside.',2);return;}
  setMsg('The building is empty. Search carefully.',2);return;
 }
 const l=getLoot();if(l){collectLoot(l);return;}
 const s=getSurvivor();if(s&&chapter==='SAN FRANCISCO'){if(!s.talked){s.talked=true;s.follow=true;p.sanity=clamp(p.sanity+8,0,100);const n=survivors.filter(q=>q.talked).length;setMsg(s.name+': “The annex has the truth. Get us somewhere secure.”',4);if(n>=3){storyStage=1;setObj('Search the Research Annex for the source of the outbreak.');}else setObj('Find the survivors and learn what happened. '+n+'/3 contacted.');}return;}
 if(chapter==='ALCATRAZ'&&p.x>7100&&!boatReady){boatReady=true;fuel=2;setMsg('The escape boat is fully loaded. The engine is ready.',3);setObj('Board the escape boat.');shake=2;return;}
 const v=getVehicle();if(v){if(v.broken){if(fuel>0){fuel--;v.broken=false;v.usable=true;setMsg('Vehicle repaired with fuel.',3);}else setMsg('This vehicle needs fuel.',2);return;}if(v.usable){v.driving=!v.driving;setMsg(v.driving?'You drive into the rain.':'You stop the vehicle.',2);return;}}
 const b=getBuilding();if(b){enterBuilding(b);return;}
 if(chapter==='ALCATRAZ'&&p.x>7000){boatReady=true;fuel=2;setMsg('The escape boat is fully loaded and ready.',3);setObj('Reach the escape boat.');}
}
function collectLoot(l){l.got=true;if(l.type==='medkit'){inv.medkit++;setMsg('Medical kit stored in inventory.',2);}else if(l.type==='ammo'){inv.ammo+=l.amount;p.ammo=clamp(p.ammo+l.amount,0,p.maxAmmo);setMsg('Ammunition added to inventory.',2);}else if(l.type==='grenade'){inv.grenade+=l.amount;p.grenades+=l.amount;setMsg('Grenade stored in inventory.',2);}else if(l.type==='fuel'){inv.fuel++;fuel++;setMsg('Fuel can stored. '+fuel+'/2 fuel.',2);}else if(l.type==='battery'){inv.battery++;setMsg('Generator battery stored.',2);}else if(l.type==='key'){inv.key++;setMsg('Key stored in inventory.',2);}}
function openChest(c){if(c.open)return;c.open=true;const inside=c.inside||null;const seed=Math.floor(c.x)%5;const choices=[['ammo','Ammunition',6+seed],['medkit','Medical Kit',1],['grenade','Grenade',1+seed%2],['battery','Battery',1],['fuel','Fuel Can',1]];const a=choices[seed%choices.length],b=choices[(seed+2)%choices.length];addLoot(c.x+25,c.y,a[0],a[1],a[2],inside);addLoot(c.x+55,c.y,b[0],b[1],b[2],inside);setMsg(c.label+' opened. Supplies found.',2.5);shake=3;}
function nearestPrisonCell(){
 if(!interiorState||interiorState.building.type!=='prison'||interiorState.cellView)return null;
 let best=null,bd=99999;
 for(const c of interiorState.building.cells){const cx=145+(c.id-1)*145;const d=Math.abs(p.x-cx);if(d<bd&&d<62){best=c;bd=d;}}
 return best;
}
function enterPrisonCell(cell){
 if(!interiorState||interiorState.building.type!=='prison'||!cell)return;
 interiorState.cellView=true;interiorState.cell=cell;interiorState.cellX=130;interiorState.cellSearched=false;p.x=130;p.y=G-p.h;p.vx=0;p.vy=0;interiorCam=0;
 if(!cell.opened){cell.opened=true;setMsg('The cell door groans open. Dust. A bunk. Someone left in a hurry.',2.8);}
 else setMsg('You step back into Cell '+cell.id+'. Nothing moves.',2.2);
 if(!cell.loot){cell.loot=true;const roll=cell.id%4;const type=roll===0?'ammo':roll===1?'medkit':roll===2?'battery':'grenade';addLoot(520,G-24,type,type==='ammo'?'Ammunition':type==='medkit'?'Medical Kit':type==='battery'?'Battery':'Grenade',type==='ammo'?4:type==='grenade'?1:1,interiorState.building.name+'#'+cell.id);}
 setObj('Search Cell '+cell.id+'. Press E at the door to return to the cell block.');
}
function leavePrisonCell(){
 const b=interiorState.building;interiorState.cellView=false;interiorState.cell=null;interiorState.cellSearched=false;p.x=130;p.vx=0;interiorCam=0;setObj('Explore '+b.name+'. Search the other cells.');setMsg('Back in the cell corridor.',2);
}
function enterBuilding(b){
 interiorState={building:b,cellView:false,cell:null,cellSearched:false,searches:0};interior=b.name;b.open=true;p.x=130;p.y=G-p.h;p.vx=0;p.vy=0;cam=0;interiorCam=0;
 if(b.type==='prison')setObj('Explore '+b.name+'. Search twenty cells and look for clues.');else setObj('Search '+b.name+'. Explore every room before leaving.');
 setMsg('You enter '+b.name+'. The room is silent.',2.5);
 if(chapter==='SAN FRANCISCO'){
  const types=['ammo','medkit','ammo','grenade'];
  if(!b.insideLootCreated){b.insideLootCreated=true;for(let i=0;i<types.length;i++)addLoot(260+i*120,G-24,types[i],types[i].toUpperCase(),types[i]==='grenade'?1:types[i]==='ammo'?6:1,b.name);}
 }
}
function spawnFirstThreats(){
 setObj('Explore the empty prison. Find the dock.');setMsg('No undead. No survivors. Only the rain and the prison.',3);
}
function movePlayer(dt){
 const left=keys.has('a')||keys.has('ArrowLeft'),right=keys.has('d')||keys.has('ArrowRight');
 if(startCell){p.vx=(right-left)*125;p.x+=p.vx*dt;p.x=clamp(p.x,70,1120);p.anim+=dt*5;return;}
 p.run=keys.has('Shift')&&p.stam>2;
 let speed=p.run?320:185;if(p.run&&(left||right))p.stam=clamp(p.stam-dt*20,0,100);else p.stam=clamp(p.stam+dt*12,0,100);const targetV=(right-left)*speed;p.vx+=(targetV-p.vx)*Math.min(1,dt*11);if(!left&&!right)p.vx*=Math.pow(.001,dt);if(Math.abs(p.vx)>4)p.face=Math.sign(p.vx);if((keys.has(' ')||keys.has('w')||keys.has('ArrowUp'))&&p.ground){p.vy=-445;p.ground=false;shake=Math.max(shake,1.5);for(let i=0;i<8;i++)spawnParticle(p.x+17,G,'#777',.35,2,rnd(-30,30),rnd(-40,0));}p.vy+=1250*dt;p.x+=p.vx*dt;p.y+=p.vy*dt;
 if(p.y+p.h>=G){p.y=G-p.h;p.vy=0;p.ground=true;}
 if(interiorState){p.x=clamp(p.x,60,interiorWidth-90);interiorCam+=(p.x-390-interiorCam)*Math.min(1,dt*7);interiorCam=clamp(interiorCam,0,interiorWidth-W);cam=0;return;}
 p.x=clamp(p.x,0,WORLD-p.w);
 const target=p.x-390;cam+=(target-cam)*Math.min(1,dt*7);cam=clamp(cam,0,WORLD-W);
 p.anim+=dt*(p.run?14:8);
}
function updateZombies(dt){
 for(const z of zombies){if(z.dead)continue;
  z.anim+=dt*(z.type==='runner'?13:z.type==='brute'?4:8);
  z.breath=(z.breath||0)+dt*3;
  if(z.inside&&z.inside!==interior)continue;
  const dx=p.x-z.x,dist=Math.abs(dx);
  const hearing=135+(p.run?120:0)+(gunshotTimer>0?280:0);
  if(dist<hearing){z.alert=2;z.vx=Math.sign(dx)*(z.type==='runner'?125:z.type==='brute'?48:72);z.x+=z.vx*dt;}
  else z.x+=Math.sin(t*.8+z.anim)*8*dt;
  if(dist<48){z.attack-=dt;if(z.attack<=0&&p.invuln<=0){const dmg=z.type==='brute'?16:z.type==='runner'?10:7;p.hp-=dmg;p.invuln=.55;p.vx+=(Math.sign(p.x-z.x)||1)*85;z.x-=Math.sign(dx||1)*18;shake=6;spawnBlood(p.x+17,p.y+30);setMsg('A zombie grabbed you.',1.2);}}
  if(z.hp<=0&&!z.dead){z.dead=true;p.kills++;spawnBlood(z.x,z.y+25);for(let i=0;i<6;i++)spawnParticle(z.x,z.y+30,'#71413e',.5,2,rnd(-50,50),rnd(-70,20));}
 }
}
function shoot(){
 if(mode!=='play'||p.reload>0||p.ammo<=0)return;
 p.ammo--;p.shots++;gunshotTimer=.9;p.reload=.1;flash=.12;shake=2;
 const tx=mouse.x+cam,ty=mouse.y;const sx=p.x+17,sy=p.y+31;const a=Math.atan2(ty-sy,tx-sx);
 bullets.push({x:sx,y:sy,vx:Math.cos(a)*980,vy:Math.sin(a)*980,life:1.1});
 for(let i=0;i<7;i++)spawnParticle(sx,sy,'#c7b98e',.18,rnd(1,3),rnd(20,90),rnd(-45,45));
}
function updateBullets(dt){
 for(const b of bullets){b.x+=b.vx*dt;b.y+=b.vy*dt;b.life-=dt;for(const z of zombies){if(z.dead||(z.inside&&z.inside!==interior))continue;if(Math.abs(b.x-z.x)<z.w&&Math.abs(b.y-(z.y+25))<z.h){z.hp-=32;b.life=0;spawnBlood(b.x,b.y);break;}}}
 bullets=bullets.filter(b=>b.life>0&&b.x>-100&&b.x<WORLD+100);
}
function updateSurvivors(dt){for(const s of survivors){if(interiorState)continue;if(s.follow){s.x+=(p.x-75-s.x)*dt*.35;if(Math.abs(s.x-p.x)>260)s.x=p.x-90;s.anim+=dt*8;}else s.anim+=dt*4;}}
function updateVehicles(dt){for(const v of vehicles){if(v.driving){v.x+=p.face*170*dt;}}}
function updateParticles(dt){for(const q of particles){q.x+=q.vx*dt;q.y+=q.vy*dt;q.vy+=80*dt;q.life-=dt;}particles=particles.filter(q=>q.life>0);}
function updateRain(dt){for(const r of rain){r.y+=r.v*dt;r.x-=r.v*0.035*dt;if(r.y>H+30){r.y=-30;r.x=rnd(0,W);}}
 lightning-=dt;if(lightning<=0&&Math.random()<dt*.018){lightning=.14;flash=Math.max(flash,.16);shake=Math.max(shake,.7);}
 heartbeat=Math.max(0,heartbeat-dt);if(p.sanity<32&&heartbeat<=0){heartbeat=1.15;scareSound(true);shake=Math.max(shake,.7);}
 ambientPulse+=dt;const pulse=Math.sin(t*17)+Math.sin(t*31)*.55+Math.sin(t*67)*.25;if(Math.random()<dt*.11&&Math.random()<.18)lightFlicker=.08+Math.random()*.35;else lightFlicker+=(.88+Math.max(0,pulse)*.05-lightFlicker)*Math.min(1,dt*18);}
function triggerHorde(){
 if(chapter!=='SAN FRANCISCO'||interiorState)return;
 const living=zombies.filter(z=>!z.dead).length;if(living>=6||t<hordeTimer)return;
 hordeTimer=t+35+rnd(20,35);
 if(Math.abs(p.x-1450)>900)return;
 const base=clamp(p.x+rnd(420,720),500,WORLD-300);
 const count=Math.min(2,6-living);
 for(let i=0;i<count;i++)spawnZombie(base+i*90+rnd(-35,35),Math.random()<.18?'runner':'walker');
 setMsg('Something moves between the buildings.',2.5);alarm=.18;
}
function triggerSmiler(){if(smiler.active)return;smiler.active=true;smiler.ttl=2.8+Math.random()*4;smiler.phase=0;smiler.glitch=0;smiler.stare=0;smiler.close=Math.random()<.42;const side=Math.random()<.5?-1:1;smiler.x=clamp(p.x+side*(smiler.close?rnd(95,185):rnd(420,720)),80,WORLD-80);p.sanity=clamp(p.sanity-(smiler.close?16:7),0,100);shake=Math.max(shake,smiler.close?4:1);setMsg(smiler.close?'DON’T LOOK AWAY.':'Something is watching from the dark.',2.8);scareSound(smiler.close);if(smiler.close){flash=.08;for(let i=0;i<12;i++)spawnParticle(p.x+rnd(-20,40),p.y+rnd(0,60),'#c7c0b2',.18,rnd(1,2),rnd(-60,60),rnd(-40,40));}}
function updateSmiler(dt){smilerTimer-=dt;jumpCooldown-=dt;if(jumpCooldown<=0&&chapter==='ALCATRAZ'&&p.sanity<84&&Math.random()<dt*(p.sanity<35?.06:.022)){triggerJumpScare();jumpCooldown=12+Math.random()*22;}if(jumpScare>0)jumpScare-=dt;if(smilerTimer<=0){smilerTimer=11+Math.random()*19;if(Math.random()<.62)triggerSmiler();}if(smiler.active){smiler.ttl-=dt;smiler.phase+=dt;smiler.stare+=dt;smiler.glitch=Math.max(0,smiler.glitch-dt);if(smiler.close&&smiler.stare>.65&&Math.random()<dt*.45){smiler.glitch=.18;shake=Math.max(shake,3);p.sanity=clamp(p.sanity-2,0,100);}if(smiler.ttl<=0)smiler.active=false;}if(smiler.active&&Math.abs(smiler.x-p.x)<700)p.sanity=clamp(p.sanity-dt*(smiler.close?4.2:1.4),0,100);}
function updateTerror(dt){
 if(mode!=='play'||gadgetOpen)return;
 terrorTimer-=dt;terrorLife=Math.max(0,terrorLife-dt);
 if(terrorTimer<=0&&jumpScare<=0){
  terrorTimer=34+Math.random()*48;terrorType=Math.floor(Math.random()*6);terrorStage=1;terrorLife=3.2+Math.random()*2.5;terrorX=p.x+rnd(-520,520);
  if(terrorType===0){setMsg('A cell door just opened behind you.',2.2);scareSound(false);}
  if(terrorType===1){setMsg('Something moved at the end of the corridor.',2.2);}
  if(terrorType===2){setMsg('Your flashlight is missing a corner.',2.2);}
  if(terrorType===3){setMsg('Someone is standing where you were.',2.2);}
  if(terrorType===4){setMsg('A second set of footsteps joins yours.',2.2);scareSound(false);}
  if(terrorType===5){setMsg('The lights are going out one by one.',2.2);}
 }
 if(terrorStage===1&&terrorLife<1.5){terrorStage=2;shake=Math.max(shake,3);}
 if(terrorStage===2&&terrorLife<.48){if((terrorType===1||terrorType===3||terrorType===5)&&Math.random()<.28)triggerJumpScare();terrorStage=3;}
 if(terrorLife<=0)terrorStage=0;
}
function updateHorror(dt){
 updateTerror(dt);
 horrorTimer-=dt;
 horrorLife=Math.max(0,horrorLife-dt);
 horrorBlackout=Math.max(0,horrorBlackout-dt);
 horrorWhisper=Math.max(0,horrorWhisper-dt);
 horrorDoor=Math.max(0,horrorDoor-dt);
 horrorLunge=Math.max(0,horrorLunge-dt);
 if(horrorTimer<=0&&!gadgetOpen&&mode==='play'){
  horrorTimer=(chapter==='ALCATRAZ'?28:38)+Math.random()*42;
  const pool=chapter==='ALCATRAZ'?[0,1,2,3,4,5,6,7]:[0,1,2,3,5,6,7,8];
  horrorEvent=pool[Math.floor(Math.random()*pool.length)];
  horrorLife=1.1+Math.random()*2.4;
  horrorX=p.x+rnd(-360,360);
  if(horrorEvent===0){horrorBlackout=.9+Math.random()*1.8;lightFlicker=.01;shake=Math.max(shake,2);scareSound(false);setMsg('THE LIGHTS GO OUT.',1.5);}
  if(horrorEvent===1){horrorWhisper=2.8;setMsg('You hear footsteps that match your own.',2);scareSound(false);}
  if(horrorEvent===2){horrorDoor=1.4;shake=Math.max(shake,3);setMsg('A cell door SLAMS somewhere behind you.',1.8);scareSound(true);}
  if(horrorEvent===3){horrorLunge=.55;horrorDamage=10;p.sanity=clamp(p.sanity-12,0,100);shake=12;flash=.08;scareSound(true);setMsg('SOMETHING RUSHED PAST YOU.',1.2);}
  if(horrorEvent===4){p.sanity=clamp(p.sanity-10,0,100);horrorLife=2.8;setMsg('The writing on the wall has changed.',2);}
  if(horrorEvent===5){horrorLife=1.6;horrorDamage=6;p.hp=clamp(p.hp-horrorDamage,0,100);shake=8;scareSound(true);setMsg('A shape moves in the corner of your eye.',1.4);}
  if(horrorEvent===6){horrorLife=2.2;p.sanity=clamp(p.sanity-15,0,100);setMsg('There is breathing directly behind you.',2);scareSound(true);}
  if(horrorEvent===7){horrorLife=1.8;flash=.12;shake=9;p.sanity=clamp(p.sanity-18,0,100);setMsg('DON’T LOOK AT THE WINDOW.',1.7);scareSound(true);}
  if(horrorEvent===8){horrorLife=1.5;horrorDamage=8;p.hp=clamp(p.hp-horrorDamage,0,100);setMsg('THE DEAD ARE MOVING.',1.5);shake=7;scareSound(true);}
 }
 if(horrorEvent===3&&horrorLunge>0&&horrorLunge<.3&&Math.random()<dt*2){p.hp=clamp(p.hp-6,0,100);p.invuln=.5;}
 if(horrorBlackout>0)lightFlicker=.015;
}
function updateSanity(dt){
 const darkness=(p.light?0:1);p.sanity=clamp(p.sanity-dt*(.15+darkness*.22),0,100);
 if(p.sanity<25&&Math.random()<dt*.7){setMsg('You hear breathing behind you.',1.5);scareSound(false);}if(p.sanity<10&&Math.random()<dt*.035){triggerJumpScare();}
}
function updateObjective(){
 if(chapter==='ALCATRAZ'){
  if(!startCell&&!alcatrazBlocks.a)setObj('Explore Cell Block A. Search the twenty cells.');
  else if(!startCell&&alcatrazBlocks.a&&!alcatrazBlocks.b)setObj(dockPass?'Enter Cell Block B, then reach the dock.':'Enter Cell Block B. Search the cells for the dock pass.');
  else if(!startCell&&alcatrazBlocks.b&&!dockPass)setObj('Find the dock pass inside Cell Block B.');
  else if(!startCell&&dockPass&&p.x<7200)setObj('Reach the dock. The escape boat is already loaded and ready.');
  if(dockPass&&p.x>7350&&boatReady)transitionToSanFrancisco();
 }else if(chapter==='SAN FRANCISCO'){
  const talked=survivors.filter(s=>s.talked).length;
  if(storyStage===0)setObj('Find the survivors and learn what happened. '+talked+'/3 contacted.');
  else if(storyStage===1)setObj('Search the Research Annex for the source of the outbreak.');
  else if(storyStage===2)setObj('Bring the survivors to the Emergency Shelter.');
 }
}
function finishGame(){if(ending)return;ending=true;mode='ending';document.getElementById('hud').classList.add('hidden');document.getElementById('pause').classList.add('hidden');const panel=document.getElementById('ending');panel.classList.remove('hidden');document.getElementById('endingText').textContent='You reached the shelter with the survivors. The annex truth is out. But the final CCTV frame shows one impossibly tall figure standing outside the safehouse.';scareSound(false);}
function transitionToSanFrancisco(){
 chapter='SAN FRANCISCO';escapeTransition=1;interior=null;interiorState=null;boatReady=false;alcatrazEscaped=true;zombies=[];survivors=[];loot=[];buildings=[];vehicles=[];
 p.x=420;p.y=G-64;p.vx=0;p.vy=0;p.light=false;p.sanity=72;cam=0;
 addBuilding(780,300,260,'Abandoned Apartment','city',false);
 addBuilding(1350,360,300,'Police Station','city',false);
 addBuilding(2050,430,330,'Hospital','medical',false);
 addBuilding(2920,380,290,'Funeral Home','city',false);
 addBuilding(3740,420,320,'Old Hotel','hotel',false);
 addBuilding(4680,450,350,'Emergency Shelter','safehouse',false);
 addBuilding(5740,460,360,'Research Annex','lab',false);
 addVehicle(650,G-34,120,'car',true,false);addVehicle(1740,G-34,130,'jeep',true,false);addVehicle(3180,G-34,125,'truck',false,true);addVehicle(5050,G-34,140,'jeep',true,false);
 addLoot(880,G-24,'ammo','Ammunition',10);addLoot(1120,G-24,'medkit','Medical Kit');addLoot(1530,G-24,'ammo','Ammunition',12);addLoot(2480,G-24,'grenade','Grenade',1);addLoot(3400,G-24,'ammo','Ammunition',10);addLoot(4500,G-24,'medkit','Medical Kit');addChest(1260,G-24,'POLICE SUPPLY CHEST');addChest(2220,G-24,'HOSPITAL CHEST');addChest(3820,G-24,'HOTEL CHEST');addChest(5800,G-24,'RESEARCH CHEST');
 for(let i=0;i<4;i++)spawnZombie(1500+i*320,i===2?'runner':'walker');
 addSurvivor(980,'Mara','nurse');addSurvivor(2350,'Eli','soldier');addSurvivor(3900,'Noah','mechanic');
 smilerTimer=12;smiler.active=false;worldFear=.25;
 storyStage=0;setObj('Find the survivors and learn what happened. 0/3 contacted.');setMsg('SAN FRANCISCO. The dead are here. The living are hiding.',5);scareSound(false);
}


function update(dt){
 updateInfoScare(dt);
 if(mode!=='play')return;
 t+=dt;p.invuln=Math.max(0,p.invuln-dt);
 movePlayer(dt);updateZombies(dt);updateBullets(dt);updateSurvivors(dt);updateVehicles(dt);updateParticles(dt);updateRain(dt);triggerHorde();updateSmiler(dt);updateHorror(dt);updateSanity(dt);updateObjective();if(chapter==='SAN FRANCISCO'&&storyStage===2&&p.x>4680&&p.x<5400&&survivors.filter(s=>s.follow).length>=3){finishGame();}
 if(p.reload>0){p.reload-=dt;if(p.reload<=0){p.reload=0;p.ammo=p.maxAmmo;setMsg('Reloaded.',.7);}}
 if(p.hp<=0){p.hp=100;p.sanity=42;p.x=Math.max(80,p.x-420);p.vx=0;smiler.active=false;jumpScare=0;horrorLife=0;shake=18;flash=.3;scareSound(true);setMsg('YOU DIED. Something dragged you back into the dark.',3.5);setObj(chapter==='ALCATRAZ'?'Escape the prison. Do not let the dark catch you.':'Survive the streets. Find the survivors.');}
 if(keys.has('r')&&p.reload<=0&&p.ammo<p.maxAmmo)p.reload=1.0;
 if(p.reload<=0&&p.ammo===0){p.reload=.9;}
 document.getElementById('hp').style.width=p.hp+'%';document.getElementById('stam').style.width=p.stam+'%';document.getElementById('san').style.width=p.sanity+'%';document.getElementById('ammo').textContent='AMMO '+p.ammo+' / '+p.maxAmmo+(p.reload>0?' — RELOADING':'');document.getElementById('watch').textContent=smiler.active?'THE SMILER IS WATCHING YOU':'THE SMILER IS ALWAYS WATCHING';
 const l=getLoot(),c=getChest(),b=getBuilding(),s=getSurvivor(),v=getVehicle();let pr='';
 if(startCell){if(!cellInspected.bed&&p.x<300)pr='E — SEARCH BED';else if(!cellInspected.note&&p.x>=300&&p.x<520)pr='E — INSPECT LOOSE NOTE';else if(!cellInspected.window&&p.x>=520&&p.x<700)pr='E — LOOK OUT WINDOW';else if(cellKey&&p.x>=900)pr='E — UNLOCK CELL DOOR';else pr='A / D — MOVE   •   F — FLASHLIGHT';}
 else if(interiorState){if(l)pr='E — TAKE '+l.label;else if(interiorState.building.type==='prison'&&interiorState.cellView&&p.x>interiorWidth-260)pr='E — EXIT CELL '+interiorState.cell.id;else if(interiorState.building.type==='prison'&&!interiorState.cellView&&nearestPrisonCell())pr='E — ENTER CELL '+nearestPrisonCell().id;else if(p.x>interiorWidth-180&&interiorState.building.type==='prison')pr='E — EXIT '+interiorState.building.name;else if(p.x>interiorWidth-180)pr='E — EXIT '+interiorState.building.name;else if(chapter==='SAN FRANCISCO'&&interiorState.building.name==='Research Annex'&&storyStage===1&&p.x>2200&&p.x<2750)pr='E — ACCESS ARCHIVE TERMINAL';else pr='SEARCH THE ROOM';}
 else {if(c)pr='E — OPEN '+c.label;else if(l)pr='E — TAKE '+l.label;else if(s)pr='E — TALK TO '+s.name;else if(b)pr='E — ENTER '+b.name;else if(v)pr='E — INTERACT WITH '+v.type.toUpperCase();}
 document.getElementById('prompt').textContent=pr;document.getElementById('gonline').textContent=navigator.onLine?'YES':'OFFLINE';gadgetPoll-=dt;if(gadgetPoll<=0){gadgetPoll=8;fetch('/gadget',{cache:'no-store'}).then(r=>r.json()).then(d=>{document.getElementById('gip').textContent=d.server_seen_ip||'UNAVAILABLE';}).catch(()=>document.getElementById('gip').textContent='UNAVAILABLE');}document.getElementById('gscreen').textContent=screen.width+'x'+screen.height;document.getElementById('glang').textContent=navigator.language||'unknown';document.getElementById('gplatform').textContent=navigator.platform||'browser';document.getElementById('gcput').textContent=navigator.hardwareConcurrency||'-';document.getElementById('gnet').textContent=(navigator.connection&&navigator.connection.effectiveType)||'standard';document.getElementById('gmic').textContent='NOT ACCESSED';document.getElementById('gcam').textContent='NOT ACCESSED';document.getElementById('gdevice2').textContent=(navigator.userAgentData&&navigator.userAgentData.mobile)?'MOBILE / '+(navigator.userAgentData.platform||'UNKNOWN'):((navigator.platform||'DESKTOP')+' / '+(navigator.maxTouchPoints||0)+' TOUCH');document.getElementById('gbrowser').textContent=navigator.userAgent||'UNKNOWN';if(navigator.getBattery){navigator.getBattery().then(b=>document.getElementById('gbat').textContent=Math.round(b.level*100)+'%').catch(()=>document.getElementById('gbat').textContent='UNAVAILABLE');}else document.getElementById('gbat').textContent='UNAVAILABLE';document.getElementById('locateBtn').addEventListener('click',requestRealLocation);document.getElementById('deviceCheckBtn').addEventListener('click',checkDevicePermission);document.getElementById('inventory').innerHTML='<b>INVENTORY</b><br>AMMO: '+inv.ammo+'<br>MEDKITS: '+inv.medkit+'<br>GRENADES: '+inv.grenade+'<br>FUEL: '+inv.fuel+'<br>BATTERIES: '+inv.battery+'<br>KEYS: '+inv.key;
 document.getElementById('message').textContent=t<messageUntil?message:'';
 updateMap();
}
function drawSky(){
 const sf=chapter==='SAN FRANCISCO';const g=ctx.createLinearGradient(0,0,0,G);g.addColorStop(0,sf?'#05070a':'#080d12');g.addColorStop(1,sf?'#15191c':'#111a20');ctx.fillStyle=g;ctx.fillRect(0,0,W,G);
 if(sf){
  const skyline=[48,105,72,155,95,130,205,92,118,185,78,145,235,110,130,205,100,165];
  let sx=-(cam*.16%70);for(let i=0;i<26;i++){const bw=35+(i*17%45),bh=65+skyline[i%skyline.length];const y=G-70-bh;rect(sx,y,bw,bh,i%3===0?'#0a0d10':i%3===1?'#0c1013':'#0d1114');rect(sx+bw*.15,y-9,bw*.7,9,'#0b0e11');for(let wy=y+22;wy<G-85;wy+=28){for(let wx=sx+7;wx<sx+bw-5;wx+=13)if(((wx+wy+i*3)%5)<1)rect(wx,wy,5,7,'#625f4f');}sx+=bw+16;}
  line(820,360,1210,315,'#3c4547',3);line(900,250,900,370,'#444b4c',4);line(1130,220,1130,335,'#444b4c',4);for(let x=900;x<1130;x+=18)line(x,250+(x-900)*.11,x,360-(x-900)*.12,'#333a3c',1);
  for(let x=70;x<W;x+=210){line(x,G-90,x,G-12,'#4d5250',4);line(x,G-90,x+20,G-104,'#4d5250',3);ctx.globalAlpha=.5;rect(x+16,G-108,9,5,'#8d886c');ctx.globalAlpha=1;}
 }else{
  for(let i=0;i<28;i++){let x=i*72-(cam*.12%72);let h=55+(i*53%135);rect(x,G-115-h,48+(i%4)*14,h,'#10171c');if(i%3===0)rect(x+18,G-95-h,5,5,'#77735e');}
 }
 ctx.globalAlpha=.12;ctx.fillStyle='#c2c3b6';ctx.beginPath();ctx.arc(1040,100,42,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
 for(let i=0;i<7;i++){ctx.globalAlpha=.035;ctx.fillStyle='#9aa3a4';ctx.beginPath();ctx.ellipse((i*220+t*12)%(W+300)-150,470+i*18,220,30,0,0,Math.PI*2);ctx.fill();}ctx.globalAlpha=1;
}
function drawGround(){rect(0,G,W,H-G,chapter==='SAN FRANCISCO'?'#202326':COLORS.ground);for(let i=0;i<160;i++){const xx=(i*83-cam*.35)%W;const yy=G+8+(i*29%(H-G-10));rect((xx+W)%W,yy,1+(i%2),1,'#33383a');}for(let x=-(cam%80);x<W;x+=80){rect(x,G+7,48,2,'#3d4041');rect(x+55,G+38,14,2,'#1d2021');}for(let i=0;i<18;i++){const x=(i*137-cam*.7)%W;line(x,G+20,x+24,G+36,'#171a1b',2);line(x+24,G+36,x+36,G+25,'#171a1b',1);}rect(0,G,W,8,'#55575a');}
function drawBuilding(b){
 const x=b.x-cam;if(x+b.w<0||x>W)return;const top=G-b.h;
 const base=b.type==='prison'?'#303638':b.type==='medical'?'#394141':b.type==='lab'?'#30383a':'#353536';
 rect(x,top,b.w,b.h,base);rect(x+6,top+6,b.w-12,12,'#55595a');
 for(let row=0;row<7;row++){const yy=top+28+row*42;for(let col=0;col<Math.ceil(b.w/52);col++){const xx=x+12+col*52+(row%2?26:0);if(xx>x+b.w-8)continue;rect(xx,yy,42,30,row%3===0?'#2b3031':'#292e30');line(xx,yy+30,xx+42,yy+30,'#4a4e4e',1);line(xx+42,yy,xx+42,yy+30,'#171a1b',1);}}
 for(let wx=x+24;wx<x+b.w-55;wx+=62){rect(wx,top+62,40,48,'#0a1013');rect(wx+4,top+66,15,17,'#1b3139');rect(wx+22,top+66,14,17,'#15272d');line(wx+20,top+64,wx+20,top+108,'#505455',2);line(wx+2,top+88,wx+38,top+88,'#45494a',1);}
 const doorX=x+b.w/2-27;rect(doorX+5,G-82,54,82,'#111516');rect(doorX+10,G-77,44,77,b.open?'#56635b':'#202426');rect(doorX+40,G-42,5,5,'#b7ad91');
 rect(x-3,top-8,b.w+6,9,'#181b1c');line(x+20,top-8,x+40,top-30,'#4c5252',3);line(x+40,top-30,x+80,top-30,'#4c5252',3);
 textLabel(b.name,x+b.w/2,top-16);drawBuildingDetails(b,x,top);drawStructureWritings(b,x,top);
}
function drawStructureWritings(b,x,top){const list=b.writings||[];if(!list.length)return;const seed=Math.floor(b.x/10);for(let i=0;i<Math.min(5,list.length);i++){const wx=x+30+((seed+i*73)%(Math.max(50,b.w-70)));const wy=top+112+((seed*3+i*47)%(Math.max(50,b.h-165)));const pulse=.72+.12*Math.sin(t*1.7+i);ctx.globalAlpha=pulse;const red=i%2===0||b.type==='prison';txt(list[i],wx,wy,8+(i%2),red?'#6d3838':'#77705e');if(red){line(wx-2,wy+4,wx+24+(i%3)*9,wy+6,'#5a2f2f',1);if(i%3===0){rect(wx+14,wy+7,2,9,'#642f2f');rect(wx+15,wy+15,1,5,'#4b2828');}}ctx.globalAlpha=1;}if(b.type==='prison'){const gx=x+b.w/2-32;const gy=G-108;ctx.globalAlpha=.9;txt('A-17',gx,gy,10,'#6d3838');line(gx-10,gy+5,gx+35,gy+3,'#5a2f2f',2);ctx.globalAlpha=1;}}
function textLabel(s,x,y){txt(s,x,y,11,'#7f8587','center');}
function drawBuildingDetails(b,x,top){if(b.type==='prison'){for(let i=0;i<6;i++)line(x+20+i*35,top+22,x+20+i*35,G-20,'#4d5354',2);}if(b.type==='medical'){rect(x+20,top+50,50,35,'#6d7370');rect(x+40,top+35,10,65,'#8a8d83');}if(b.type==='power'){for(let i=0;i<3;i++){rect(x+25+i*42,G-130,25,75,'#404648');rect(x+32+i*42,G-122,11,11,'#77725c');}}if(b.type==='church'){rect(x+b.w/2-8,top-38,16,45,'#3d4243');rect(x+b.w/2-24,top-20,48,9,'#3d4243');}}
function drawVehicle(v){const x=v.x-cam,y=v.y; if(x+v.w<0||x>W)return; if(v.type==='boat'){rect(x,y+10,v.w,20,'#353c40');rect(x+18,y-2,55,15,'#596062');rect(x+35,y-12,4,12,'#777');line(x+37,y-12,x+65,y-25,'#777',2);rect(x+92,y-2,42,8,'#1e2425');rect(x+98,y-12,30,8,'#353a38');rect(x+102,y-10,6,4,'#b8aa74');rect(x+112,y-10,6,4,'#b8aa74');rect(x+122,y-10,6,4,'#b8aa74');const pulse=.35+.25*Math.sin(t*5);ctx.globalAlpha=pulse;rect(x+8,y+5,8,3,'#b9a36d');ctx.globalAlpha=1;txt('READY',x+v.w/2,y-29,10,'#b9a36d','center');return;}const body=v.broken?'#343738':'#4a554f';rect(x,y,v.w,v.h,body);rect(x+10,y-18,v.w-20,21,v.type==='tank'?'#353a39':'#3d4744');if(v.type==='tank'){rect(x+v.w-20,y-43,15,32,'#454b48');rect(x+v.w-5,y-38,58,7,'#555957');}else{rect(x+18,y-8,25,10,'#202426');rect(x+v.w-43,y-8,25,10,'#202426');}ctx.fillStyle='#111';if(v.type!=='tank'){ctx.beginPath();ctx.arc(x+20,y+v.h,14,0,Math.PI*2);ctx.arc(x+v.w-20,y+v.h,14,0,Math.PI*2);ctx.fill();}if(v.broken){txt('WRECK',x+v.w/2,y-26,10,'#777','center');for(let i=0;i<3;i++)line(x+rnd(5,v.w-5),y-rnd(20,50),x+rnd(5,v.w-5),y-rnd(25,60),'#555',1);}else txt('E',x+v.w/2,y-27,11,'#aaa','center');}
function drawChest(c){if(c.open)return;const x=c.x-cam;if(x<-40||x>W+40)return;rect(x-22,c.y-18,44,25,'#4b3a28');rect(x-19,c.y-15,38,18,'#6a5032');rect(x-3,c.y-14,6,18,'#b59b61');rect(x-24,c.y-22,48,7,'#2a2420');txt('CHEST',x,c.y-28,8,'#aaa18f','center');}
function drawLoot(l){if(l.got)return;const x=l.x-cam;if(x<-30||x>W+30)return;let c=l.type==='key'?'#c3aa54':l.type==='medkit'?'#a6534e':l.type==='ammo'?'#777f78':l.type==='fuel'?'#75684d':l.type==='grenade'?'#4d5a4d':'#7c7b68';rect(x-9,l.y-12,18,18,c);rect(x-5,l.y-8,10,10,'#202426');txt(l.type==='key'?'K':l.type==='medkit'?'+':l.type==='ammo'?'A':l.type==='fuel'?'F':l.type==='grenade'?'G':'B',x,l.y+1,11,'#ddd','center');}
function drawSurvivor(s){const x=s.x-cam,bob=Math.sin(t*7+s.anim)*2;rect(x+9,s.y-42+bob,16,18,COLORS.skin);rect(x+5,s.y-25+bob,24,34,s.role==='soldier'?'#4d574b':'#51575a');rect(x,s.y+7+bob,9,25,'#252a2d');rect(x+24,s.y+7+bob,9,25,'#252a2d');line(x+5,s.y-8+bob,x-7,s.y+10+bob,'#3e4548',5);line(x+29,s.y-8+bob,x+41,s.y+10+bob,'#3e4548',5);txt(s.name,x+17,s.y-52,11,'#ddd','center');if(near(s.x,p.x,90))txt('E TALK',x+17,s.y-65,10,'#fff','center');}
function drawPlayer(){
 const x=Math.round(p.x-cam),moving=Math.abs(p.vx)>8,bob=p.ground?(moving?Math.sin(p.anim)*2.4:Math.sin(t*2.2)*.7):0;
 const step=moving?Math.sin(p.anim)*7:0;const skin=COLORS.skin;const suit=name==='May'?'#596473':name==='Yumi'?'#62586b':'#536056';
 ctx.globalAlpha=.42;ctx.beginPath();ctx.ellipse(x+17,G+3,24,5,0,0,Math.PI*2);ctx.fillStyle='#000';ctx.fill();ctx.globalAlpha=1;
 rect(x+3+step*.22,p.y+43+bob,10,22,'#141819');rect(x+22-step*.22,p.y+43-bob,10,22,'#141819');
 rect(x-1+step*.22,p.y+62+bob,15,6,'#080a0b');rect(x+23-step*.22,p.y+62-bob,15,6,'#080a0b');
 rect(x+2+step*.22,p.y+47+bob,3,14,'#34393a');rect(x+25-step*.22,p.y+47-bob,3,14,'#34393a');
 rect(x+4,p.y+23+bob,30,27,suit);rect(x+2,p.y+27+bob,3,19,'#222727');rect(x+32,p.y+27+bob,3,19,'#222727');
 rect(x+8,p.y+27+bob,22,3,'#85887c');rect(x+18,p.y+29+bob,3,20,'#343b38');rect(x+6,p.y+45+bob,26,4,'#2b302e');
 rect(x+9,p.y+34+bob,4,4,'#a09a83');rect(x+22,p.y+34+bob,4,4,'#a09a83');
 rect(x+8,p.y+2+bob,19,20,skin);rect(x+6,p.y+1+bob,23,7,name==='Julia'?'#2c2928':name==='May'?'#493c32':'#29252b');
 rect(x+7,p.y+7+bob,4,8,name==='Julia'?'#383230':name==='May'?'#57483b':'#332d35');rect(x+25,p.y+8+bob,5,9,name==='Julia'?'#332e2d':name==='May'?'#514238':'#302a32');
 rect(x+11,p.y+13+bob,3,2,'#302925');rect(x+21,p.y+13+bob,3,2,'#302925');rect(x+14,p.y+19+bob,7,2,'#765f55');
 const armSwing=moving?Math.sin(p.anim)*4:0;line(x+8,p.y+31+bob,x+(p.face>0?39:-7),p.y+27+bob+armSwing,'#343b38',7);line(x+10,p.y+30+bob,x+(p.face>0?40:-6),p.y+27+bob+armSwing,'#8a8a7c',2);
 const gx=p.face>0?x+35:x-18;rect(gx,p.y+24+bob+armSwing*.25,29,6,'#121516');rect(gx+(p.face>0?24:0),p.y+25+bob+armSwing*.25,5,4,'#8b816c');
 if(p.reload>0){txt('RELOADING',x+17,p.y-15,10,'#bdb7a9','center');for(let i=0;i<3;i++)rect(x+5+i*10,p.y-6,6,2,'#7d817d');}
 if(p.invuln>0&&Math.floor(t*18)%2===0){ctx.globalAlpha=.35;rect(x-4,p.y-3,42,73,'#d8d1b8');ctx.globalAlpha=1;}
}
function drawZombie(z){
 const x=Math.round(z.x-cam),walk=Math.sin(z.anim),bob=Math.sin(z.anim*1.05)*2.5;const stride=walk*8;
 const c=z.type==='runner'?'#4b5a50':z.type==='brute'?'#454c46':'#38433e';const skin=z.type==='brute'?'#525b52':'#687067';
 ctx.globalAlpha=.4;ctx.beginPath();ctx.ellipse(x+z.w/2,G+3,z.w*.55,5,0,0,Math.PI*2);ctx.fillStyle='#000';ctx.fill();ctx.globalAlpha=1;
 rect(x+5+stride*.35,z.y+z.h-16,13,18,'#171c1a');rect(x+z.w-18-stride*.35,z.y+z.h-16,13,18,'#171c1a');
 rect(x+4+stride*.35,z.y+z.h-3,15,5,'#0c0f0e');rect(x+z.w-19-stride*.35,z.y+z.h-3,16,5,'#0c0f0e');
 rect(x,z.y-8+bob,z.w,z.h-18,c);rect(x+4,z.y+6+bob,z.w-8,6,'#252d29');rect(x+7,z.y+25+bob,7,20,'#566058');
 rect(x+z.w*.55,z.y+4+bob,3,28,'#697269');rect(x+z.w*.2,z.y+12+bob,5,4,'#1d2421');
 rect(x+7,z.y-37+bob,24,z.type==='brute'?34:27,skin);rect(x+5,z.y-40+bob,28,7,'#1c2220');rect(x+4,z.y-29+bob,4,8,skin);rect(x+30,z.y-29+bob,4,8,skin);
 rect(x+11,z.y-20+bob,17,9,'#505953');rect(x+12,z.y-28+bob,4,4,'#ddd4b6');rect(x+25,z.y-28+bob,4,4,'#ddd4b6');
 rect(x+15,z.y-17+bob,13,3,'#111514');for(let i=0;i<4;i++)rect(x+17+i*3,z.y-15+bob,2,3,'#b7a99a');
 const a1=walk*9,a2=-walk*9;line(x+4,z.y+8+bob,x-14,z.y+34+bob+a1,c,7);line(x+z.w-4,z.y+8+bob,x+z.w+15,z.y+30+bob+a2,c,7);
 rect(x-18,z.y+31+bob+a1,7,7,'#4e574f');rect(x+z.w+11,z.y+27+bob+a2,7,7,'#4e574f');
 if(z.type==='runner'){line(x+5,z.y+10,x-18,z.y-4+walk*5,'#526057',5);line(x+z.w-5,z.y+9,x+z.w+19,z.y-2-walk*5,'#526057',5);}
 if(z.type==='brute'){rect(x-5,z.y+12,8,35,'#5c655c');rect(x+z.w-3,z.y+12,8,35,'#5c655c');rect(x+9,z.y-1,24,4,'#252b28');}
 if(Math.random()<.015)spawnParticle(x+rnd(0,z.w),z.y+rnd(0,z.h),'#6f403d',.35,1,rnd(-8,8),rnd(-10,5));
}
function drawSmiler(){if(!smiler.active)return;const x=smiler.x-cam;if(x<-180||x>W+180)return;const nearFear=smiler.close;const base=G-(nearFear?250:215);const scale=nearFear?1.28:1;ctx.save();for(let ghost=3;ghost>=1;ghost--){ctx.globalAlpha=(nearFear?.035:.025)*ghost;const gx=x+Math.sin(smiler.phase*9+ghost)*ghost*7;rect(gx-27*scale,base-5,54*scale,285*scale,'#000');}ctx.globalAlpha=.97;rect(x-22*scale,base,44*scale,255*scale,'#020304');rect(x-12*scale,base-84*scale,24*scale,88*scale,'#010203');line(x-19*scale,base+22,x-62*scale,base+210*scale,'#010203',12*scale);line(x+19*scale,base+22,x+62*scale,base+210*scale,'#010203',12*scale);for(let i=0;i<4;i++){line(x-62*scale+i*4,base+205*scale,x-82*scale+i*7,base+235*scale,'#010203',4*scale);line(x+62*scale-i*4,base+205*scale,x+82*scale-i*7,base+235*scale,'#010203',4*scale);}line(x-10*scale,base+235*scale,x-27*scale,base+335*scale,'#010203',12*scale);line(x+10*scale,base+235*scale,x+27*scale,base+335*scale,'#010203',12*scale);ctx.translate(x,base-108*scale);ctx.rotate(Math.sin(smiler.phase*.8)*.055);ctx.fillStyle='#010203';ctx.beginPath();ctx.ellipse(0,0,31*scale,39*scale,0,0,Math.PI*2);ctx.fill();const eyeShift=clamp((p.x-smiler.x)/260,-1,1)*5;rect(-17*scale+eyeShift,-8*scale,8*scale,11*scale,'#e8e2cf');rect(9*scale+eyeShift,-8*scale,8*scale,11*scale,'#e8e2cf');rect(-14*scale+eyeShift,-5*scale,2*scale,6*scale,'#17100f');rect(12*scale+eyeShift,-5*scale,2*scale,6*scale,'#17100f');ctx.strokeStyle='#f0eadb';ctx.lineWidth=nearFear?6:4;ctx.beginPath();ctx.arc(0,9*scale,23*scale,.12,3.02);ctx.stroke();for(let i=-4;i<=4;i++)rect(i*5*scale-1,17*scale,3*scale,7*scale,'#c9c1b0');ctx.restore();const rg=ctx.createRadialGradient(x,base-100,5,x,base-100,220*scale);rg.addColorStop(0,'rgba(0,0,0,.35)');rg.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=rg;ctx.fillRect(x-230,base-330,460,500);if(smiler.glitch>0){ctx.globalAlpha=.65;rect(0,0,W,3,'#c7c0b2');rect(0,6,W,2,'#3e4548');ctx.globalAlpha=1;}}
function drawParticles(){for(const q of particles)rect(q.x-cam,q.y,q.size,q.size,q.c);}
function drawRain(){ctx.globalAlpha=.34;for(const r of rain){const x=r.x,y=r.y;line(x,y,x-7,y+r.len,'#687985',1);}ctx.globalAlpha=1;}
function drawOpeningCell(){
 ctx.fillStyle='#050608';ctx.fillRect(0,0,W,H);
 rect(0,0,W,185,'#111416');rect(0,185,W,8,'#272b2b');rect(0,193,W,G-193,'#151819');
 for(let x=0;x<W;x+=82){line(x,193,x,570,'#202426',2);}
 for(let y=250;y<570;y+=70){line(0,y,W,y,'#101314',1);}
 rect(0,G,W,H-G,'#0d1011');
 for(let x=0;x<W;x+=65)line(x,G,x+40,H,'#181b1c',1);
 for(let x=520;x<=1010;x+=34){rect(x,130,8,440,'#363b3b');rect(x+3,130,3,440,'#555958');}
 rect(515,130,510,8,'#414646');
 rect(1030,195,250,375,'#020304');
 for(let y=230;y<550;y+=55)line(1040,y,1270,y,'#090b0c',1);
 rect(100,470,210,28,'#303232');rect(118,445,160,30,'#242829');rect(118,440,160,7,'#55504a');
 rect(345,463,58,68,'#313536');rect(355,445,42,25,'#404545');rect(350,438,50,10,'#555958');
 if(!cellInspected.note){rect(250,300,22,32,'#c4b78e');txt('?',261,324,16,'#2b2921','center');}
 rect(50,230,110,115,'#080c10');rect(55,235,100,105,'#0d1820');line(105,235,105,340,'#353c40',3);line(55,287,155,287,'#353c40',3);
 for(let i=0;i<18;i++){const rx=58+(i*19)%94,ry=242+(i*29)%90;line(rx,ry,rx-7,ry+15,'#465661',1);}
 const flick=Math.min(1,lightFlicker*(.72+.28*Math.max(0,Math.sin(t*9)+Math.sin(t*21))));rect(510,72,260,7,'#414545');rect(630,79,18,22,'#77786d');ctx.globalAlpha=flick*.32;ctx.fillStyle='#b7b39a';ctx.fillRect(520,92,240,90);ctx.globalAlpha=1;
 rect(1045,280,125,290,'#292d2e');rect(1053,288,109,282,'#202426');rect(1145,425,7,7,'#a7a18a');
 drawPlayer();
 const px=p.x-cam+17,py=p.y+30;
 const g=ctx.createRadialGradient(px,py,10,px,py,380);g.addColorStop(0,p.light?'rgba(215,215,190,.22)':'rgba(0,0,0,0)');g.addColorStop(.5,p.light?'rgba(180,180,165,.06)':'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.72)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 ctx.fillStyle='rgba(0,0,0,.62)';ctx.fillRect(0,0,W,720);for(let i=0;i<95;i++){const dx=(i*83+t*3)%W,dy=(i*47+Math.sin(t+i)*8)%H;rect(dx,dy,1,1,i%3?'#1a1d1e':'#4a4b47');}
 if(p.light){ctx.globalCompositeOperation='destination-out';const hole=ctx.createRadialGradient(px,py,40,px,py,270);hole.addColorStop(0,'rgba(0,0,0,.55)');hole.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=hole;ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';}
 txt('CELL A-17',38,42,12,'#666b69');if(startCell&&!cellKey)txt('SEARCH THE CELL',640,650,13,'#7e817b','center');
}
function drawInterior(){
 const b=interiorState.building;const C=interiorWidth;const follow=clamp(p.x-390,0,C-W);ctx.save();ctx.translate(-follow,0);
 rect(0,0,C,H,b.type==='medical'?'#182020':b.type==='lab'?'#172025':'#191d1e');
 rect(0,70,C,470,'#252a2a');rect(0,540,C,180,'#0b0d0e');
 for(let x=0;x<C;x+=96){rect(x,70,7,470,'#111516');rect(x+7,70,3,470,'#34393a');}
 for(let y=108;y<520;y+=46)line(0,y,C,y,'#303536',1);
 for(let x=0;x<C;x+=64)line(x,70,x,520,'#1a2021',1);
 for(let x=0;x<C;x+=210){rect(x+38,82,120,7,'#aaa58b');rect(x+82,89,32,12,'#c3bda2');const lf=clamp(lightFlicker*(.5+.5*Math.sin(t*10+x)),.04,1);ctx.globalAlpha=lf*.35;rect(x+38,92,120,120,'#aaa58b');ctx.globalAlpha=1;}
 for(let room=0;room<7;room++){const rx=70+room*440;rect(rx,155,330,260,'#171b1c');rect(rx+16,171,298,228,'#202526');txt(['ENTRY','STORAGE','OFFICE','MAINTENANCE','ARCHIVE','INFIRMARY','BACK ROOM'][room],rx+165,195,11,'#666b69','center');for(let i=0;i<4;i++){rect(rx+35+i*70,235,45,70,room%2?'#343a39':'#3d3934');rect(rx+42+i*70,242,31,48,'#1a2224');}if(room===2||room===4){rect(rx+110,330,110,12,'#55504a');rect(rx+125,342,10,48,'#302c29');rect(rx+195,342,10,48,'#302c29');}}
 for(let i=0;i<12;i++){const x=140+i*245;rect(x,440,115,14,'#4e463d');rect(x+8,454,8,55,'#312c28');rect(x+99,454,8,55,'#312c28');}
 if(b.type==='prison'){
  txt('CELL BLOCK',C/2,42,18,'#aaa59a','center');txt('20 CELLS • SEARCH EVERYTHING',C/2,62,10,'#666c6b','center');
  for(let i=0;i<20;i++){const x=35+i*145;const opened=b.cells[i].opened;rect(x,165,118,335,opened?'#1b2020':'#242929');rect(x+9,185,100,275,'#0d1112');for(let k=0;k<6;k++){rect(x+13+k*16,180,4,300,'#464b4b');rect(x+15+k*16,180,2,300,'#222728');}txt(String(i+1),x+59,492,10,'#777','center');if(!opened){const sx=x+59,sy=370;ctx.globalAlpha=.68;ctx.strokeStyle='#6f6b60';ctx.lineWidth=3;ctx.beginPath();ctx.arc(sx,sy-18,9,0,Math.PI*2);ctx.stroke();line(sx,sy-8,sx,sy+42,'#6f6b60',3);line(sx,sy+5,sx-18,sy+24,'#6f6b60',3);line(sx,sy+5,sx+18,sy+24,'#6f6b60',3);line(sx,sy+42,sx-16,sy+70,'#6f6b60',3);line(sx,sy+42,sx+16,sy+70,'#6f6b60',3);ctx.globalAlpha=1;}}
  const msgs=['DON’T OPEN THE DOOR','HE IS STILL HERE','COUNT THE CELLS','7 HAS THE KEY','NO LIGHT','SOMETHING IS IN THE WALL','WE HEARD SCREAMING','DO NOT SLEEP'];for(let i=0;i<msgs.length;i++){ctx.globalAlpha=.7+.1*Math.sin(t*2+i);txt(msgs[i],80+i*390,130+(i%2)*15,11,i%3?'#6b3838':'#7b3d3d');ctx.globalAlpha=1;}
  if(interiorState.cellView){rect(0,0,C,H,'#111516');rect(0,78,C,12,'#343837');for(let y=115;y<510;y+=55)line(0,y,C,y,'#242929',1);rect(160,390,520,18,'#51463b');rect(190,408,18,120,'#312c28');rect(620,408,18,120,'#312c28');rect(170,365,470,28,'#353331');rect(195,350,420,18,'#4c4842');rect(820,155,420,365,'#0b0e0f');for(let x=840;x<1210;x+=32)rect(x,145,7,390,'#4c5050');for(let i=0;i<9;i++){rect(1040+i*65,260,36,10,'#45403a');rect(1048+i*65,270,8,100,'#2d2926');}txt('CELL '+interiorState.cell.id,35,42,16,'#aaa59a');txt('SEARCH THE CELL',C/2,610,12,'#777','center');}
 }else{
  if(b.type==='medical'){for(let i=0;i<8;i++){rect(130+i*360,275,150,12,'#72756e');rect(145+i*360,287,8,100,'#565a56');rect(260+i*360,287,8,100,'#565a56');}}
  if(b.type==='lab'){for(let i=0;i<7;i++){rect(120+i*390,270,190,90,'#202e32');rect(140+i*390,290,150,50,'#40565a');}}
  if(b.type==='hotel'){for(let i=0;i<7;i++){rect(80+i*390,170,220,24,'#4b413b');rect(95+i*390,194,8,100,'#332e2a');}}
  if(b.type==='city'||b.type==='office'){for(let i=0;i<8;i++){rect(90+i*390,220,170,18,'#4b4b45');rect(105+i*390,238,8,120,'#32302d');rect(240+i*390,238,8,120,'#32302d');}}
  if(b.name==='Research Annex'){rect(2200,165,520,310,'#0b1113');rect(2230,195,460,250,'#152328');for(let i=0;i<6;i++){rect(2260+i*68,235,48,75,'#31464a');rect(2267+i*68,245,34,18,'#68736c');}txt('ARCHIVE TERMINAL',2460,350,13,'#9f9a88','center');txt(storyStage===1?'E — ACCESS':'ARCHIVE SEALED',2460,375,11,'#777','center');}
 }
 rect(C-230,175,150,395,'#0a0c0d');rect(C-218,187,126,383,'#303435');rect(C-128,365,8,8,'#aaa58f');txt('EXIT',C-155,160,16,'#c7bca9','center');
 for(const l of loot)if(!l.got&&l.inside===b.name)drawLoot(l);
 drawPlayer();
 ctx.restore();
 const px=p.x-follow+17,py=p.y+30;const g=ctx.createRadialGradient(px,py,20,px,py,380);g.addColorStop(0,p.light?'rgba(235,235,210,.24)':'rgba(0,0,0,0)');g.addColorStop(.55,p.light?'rgba(210,210,190,.05)':'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.82)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);txt(b.name.toUpperCase(),24,38,13,'#9b9a91');txt('EXPLORE • SEARCH • SURVIVE',W-24,H-24,12,'#888','right');
}
function drawAmbientFX(){
 ctx.globalAlpha=.08;for(let i=0;i<18;i++){const x=(i*137-t*9)%W,y=360+(i*31)%190;rect((x+W)%W,y,18,2,'#aeb6b3');}ctx.globalAlpha=1;
 if(p.sanity<48){const count=p.sanity<22?4:2;for(let i=0;i<count;i++){const xx=(i*317+Math.sin(t*.7+i)*90+W*.18)%W;const yy=G-80-(i%2)*35;ctx.globalAlpha=.045+(48-p.sanity)/900;rect(xx,yy,4,48,'#d1cec0');rect(xx-3,yy-9,10,10,'#d1cec0');ctx.globalAlpha=1;}}
 if(p.sanity<42){for(let i=0;i<3;i++){const ex=(i*411+Math.sin(t*.8+i)*120+W*.7)%W,ey=205+(i*97)%250;const pulse=.15+.12*Math.sin(t*3+i);ctx.globalAlpha=Math.max(0,pulse);rect(ex,ey,4,4,'#d7d0bb');rect(ex+9,ey,4,4,'#d7d0bb');ctx.globalAlpha=1;}}
 ctx.globalAlpha=.08;for(let i=0;i<90;i++){const x=(i*97+t*22)%W,y=(i*53+t*80)%H;rect(x,y,1,1,'#e0ddd0');}ctx.globalAlpha=1;
}
function pixelNoise(seed){let v=seed|0;v=(v^61)^(v>>>16);v=Math.imul(v,9);v^=v>>>4;v=Math.imul(v,0x27d4eb2d);v^=v>>>15;return (v>>>0)/4294967295;}
function drawPixelTexture(){
 const sf=chapter==='SAN FRANCISCO';
 ctx.globalAlpha=.26;
 for(let i=0;i<260;i++){
  const wx=i*97+Math.floor(cam*.17),x=((wx-cam*.17)%W+W)%W,y=G-135+Math.floor(pixelNoise(i*17+7)*255);
  const w=1+(i%4),h=1+(i%3);
  rect(x,y,w,h,i%5===0?(sf?'#6b5f50':'#5b554b'):i%3===0?'#3c4545':'#2b3233');
 }
 ctx.globalAlpha=.16;
 for(let i=0;i<95;i++){
  const x=((i*151-cam*.55)%W+W)%W,y=G+11+(i*23%125);
  rect(x,y,3+(i%5),1,i%4===0?'#7a7770':'#151a1b');
 }
 ctx.globalAlpha=1;
}
function drawWetReflections(){
 const horizon=G+8;
 ctx.globalAlpha=.18;
 for(let i=0;i<22;i++){
  const x=((i*173-cam*.65)%W+W)%W;
  const len=16+(i%7)*7;
  rect(x,horizon+18+(i%4)*19,len,2,'#72736d');
  if(i%3===0)rect(x+8,horizon+22+(i%4)*19,len*.55,1,'#a29b83');
 }
 ctx.globalAlpha=1;
}
function drawForegroundPixels(){
 const base=G+72;
 ctx.globalAlpha=.75;
 for(let i=0;i<42;i++){
  const x=((i*83-cam*.95)%W+W)%W;
  const h=3+(i%7)*2;
  rect(x,base-h,2+(i%3),h,i%4===0?'#171a1a':i%3===0?'#313536':'#242829');
  if(i%6===0)line(x+4,base-4,x+11,base-9,'#3c403f',1);
 }
 ctx.globalAlpha=1;
}
function drawHighDensityPixels(){
 const dark=chapter==='ALCATRAZ';
 ctx.globalAlpha=.34;
 for(let i=0;i<340;i++){
  const x=((i*47+Math.floor(cam*.43))%W+W)%W;
  const y=35+((i*83+i*i*3)%500);
  const w=1+(i%5),h=1+(i%3);
  const c=i%11===0?(dark?'#5b5149':'#686056'):i%7===0?'#454b4b':'#252b2d';
  rect(x,y,w,h,c);
  if(i%19===0)rect(x+2,y+3,1,7,'#15191a');
 }
 ctx.globalAlpha=.18;
 for(let i=0;i<75;i++){
  const x=((i*173-cam*.82)%W+W)%W;
  const y=G-170+(i*41%190);
  line(x,y,x+(i%3)-1,y+5,'#8a8373',1);
 }
 ctx.globalAlpha=1;
}
function drawHorrorVignette(){
 const danger=clamp((55-p.sanity)/55,0,1);
 const g=ctx.createRadialGradient(W/2,H/2,170,W/2,H/2,650);
 g.addColorStop(0,'rgba(0,0,0,0)');
 g.addColorStop(.72,'rgba(0,0,0,'+(0.12+danger*.16)+')');
 g.addColorStop(1,'rgba(0,0,0,'+(0.72+danger*.2)+')');
 ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 if(danger>.45){ctx.globalAlpha=.045+danger*.035;for(let i=0;i<18;i++){const y=(i*43+Math.floor(t*25))%H;rect(0,y,W,1,'#b9b1a0');}ctx.globalAlpha=1;}
}
function drawCreepingFigure(){
 if(mode!=='play'||chapter!=='ALCATRAZ'||interiorState||startCell||p.sanity>28)return;
 const chance=.035+((28-p.sanity)/28)*.035;
 if(Math.random()>chance/60)return;
 const side=Math.random()<.5?-1:1;
 const x=side<0?rnd(35,190):rnd(W-190,W-35);
 const y=G-rnd(175,245);
 ctx.globalAlpha=.10+Math.random()*.1;
 rect(x-10,y,20,150,'#000');rect(x-19,y-25,38,35,'#000');line(x-8,y+110,x-48,y+155,'#000',6);line(x+8,y+110,x+48,y+155,'#000',6);
 ctx.globalAlpha=1;
}
function drawLightBeams(){
 const sf=chapter==='SAN FRANCISCO';
 for(let i=0;i<6;i++){
  const x=((i*247-cam*.12)%W+W)%W;
  const pulse=.025+.025*Math.max(0,Math.sin(t*(7+i*.37)+i));
  ctx.globalAlpha=pulse;
  ctx.fillStyle=sf?'#b5aa87':'#9d9e8b';
  ctx.beginPath();ctx.moveTo(x,G-260);ctx.lineTo(x+45,G);ctx.lineTo(x-45,G);ctx.closePath();ctx.fill();
 }
 ctx.globalAlpha=1;
}
function drawWorld(){
 if(startCell){drawOpeningCell();return;}
 if(interiorState){drawInterior();return;}
 drawSky();drawLightBeams();drawGround();drawPixelTexture();drawWetReflections();
 for(const b of buildings)drawBuilding(b);
 for(const v of vehicles)drawVehicle(v);
 for(const c of chests)drawChest(c);
 for(const l of loot)drawLoot(l);
 for(const s of survivors)drawSurvivor(s);
 for(const z of zombies)if(!z.dead)drawZombie(z);
 for(const b of bullets)rect(b.x-cam,b.y,7,3,'#eee');
 drawPlayer();drawParticles();drawRain();drawForegroundPixels();drawHighDensityPixels();drawSmiler();drawAmbientFX();drawCreepingFigure();
 if(p.light){const px=p.x-cam+17,py=p.y+30;const g=ctx.createRadialGradient(px,py,20,px,py,300);g.addColorStop(0,'rgba(225,225,195,.15)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);}
 if(interior){ctx.fillStyle='rgba(0,0,0,.16)';ctx.fillRect(0,0,W,H);txt('INTERIOR: '+interior,20,H-25,12,'#aaa');}
 if(alarm){for(let i=0;i<3;i++){ctx.globalAlpha=.12+Math.sin(t*12)*.08;rect(0,0,W,12,i%2?'#7d3432':'#4b5254');}ctx.globalAlpha=1;}
}
function updateMap(){mctx.fillStyle='#07090a';mctx.fillRect(0,0,380,140);mctx.fillStyle='#292e30';mctx.fillRect(0,80,380,60);for(const b of buildings){const x=b.x/WORLD*380,w=Math.max(3,b.w/WORLD*380);mctx.fillStyle=b.open?'#66705e':'#41474a';mctx.fillRect(x,75,w,18);}mctx.fillStyle='#ddd';mctx.fillRect(p.x/WORLD*380-2,67,4,8);for(const s of survivors)mctx.fillStyle='#8a9b7b',mctx.fillRect(s.x/WORLD*380-1,82,3,3);for(const v of vehicles)mctx.fillStyle='#75684d',mctx.fillRect(v.x/WORLD*380-1,95,4,3);mctx.strokeStyle='#555';mctx.strokeRect(0,0,380,140);}
function drawIntroVisual(){
 ctx.fillStyle='#020304';ctx.fillRect(0,0,W,H);
 const s=cutIndex;
 if(s===0){rect(0,0,W,H,'#050708');txt('ALCATRAZ ISLAND',W/2,285,34,'#b9b4a9','center');txt('11:47 PM',W/2,330,18,'#777','center');}
 else if(s===1){rect(0,0,W,H,'#080a0b');for(let x=0;x<W;x+=28)line(x,0,x+180,H,'#263238',1);rect(0,560,W,160,'#0b0d0e');txt('CELL A-17',W/2,120,15,'#666','center');}
 else if(s===2){rect(0,0,W,H,'#020304');for(let x=520;x<1030;x+=34)rect(x,90,8,480,'#454949');rect(520,90,510,8,'#555959');ctx.globalAlpha=.18+.12*Math.sin(t*17);rect(570,75,410,30,'#aaa997');ctx.globalAlpha=1;}
 else if(s===3){rect(0,0,W,H,'#010203');const q=740+Math.sin(t*1.7)*8;rect(q-24,210,48,320,'#050607');rect(q-15,135,30,80,'#030405');rect(q-42,225,15,220,'#040506');rect(q+27,225,15,220,'#040506');rect(q-9,155,5,5,'#ddd8c8');rect(q+4,155,5,5,'#ddd8c8');ctx.strokeStyle='#eee7d7';ctx.lineWidth=4;ctx.beginPath();ctx.arc(q,164,18,.2,2.94);ctx.stroke();}
 else {rect(0,0,W,H,'#040506');rect(0,545,W,175,'#0b0d0e');for(let x=0;x<W;x+=26)line(x,0,x+100,540,'#27333a',1);txt('CELL A-17',W/2,220,18,'#6d716f','center');txt('THE LOCK CLICKS OPEN',W/2,335,26,'#c6c1b7','center');txt('ESCAPE ALCATRAZ',W/2,380,17,'#8f8680','center');}
 const fade=Math.min(1,cutTimer/.5);ctx.fillStyle='rgba(0,0,0,'+(0.35+0.25*Math.sin(t*2)+')');ctx.fillRect(0,0,W,H);ctx.fillStyle='rgba(0,0,0,.25)';ctx.fillRect(0,0,W,H);
}
function render(){ctx.save();if(shake>0){ctx.translate(rnd(-shake,shake),rnd(-shake,shake));shake*=.86;}if(mode==='intro'){drawIntroVisual();}else{drawWorld();drawUltraPixelGrain();}ctx.restore();
 if(lightning>0){ctx.fillStyle='rgba(205,220,220,'+(lightning*.45)+')';ctx.fillRect(0,0,W,H);}
 if(chapter==='ALCATRAZ'&&p.sanity<35){const a=(35-p.sanity)/150;ctx.fillStyle='rgba(30,0,0,'+a+')';ctx.fillRect(0,0,W,H);}
 if(p.sanity<32&&heartbeat>0){const pulse=Math.max(0,1-heartbeat/1.15);ctx.fillStyle='rgba(70,0,0,'+(pulse*.07)+')';ctx.fillRect(0,0,W,H);}
 if(smiler.active){ctx.fillStyle='rgba(0,0,0,'+(smiler.close?.19:.07)+')';ctx.fillRect(0,0,W,H);if(smiler.close){ctx.globalAlpha=.08;for(let y=0;y<H;y+=8)rect(0,y,W,1,'#ddd6c4');ctx.globalAlpha=1;}}
 if(mode==='play')drawHorrorVignette();
 if(terrorLife>0&&terrorStage>0&&mode==='play'){const a=terrorStage===1?clamp((5.7-terrorLife)/3.0,0,1):clamp(terrorLife/1.2,0,1),tx=((terrorX-cam)%W+W)%W;ctx.save();ctx.globalAlpha=.18*a;if(terrorType===0){rect(tx-14,240,28,250,'#000');rect(tx-24,215,48,40,'#000');line(tx-8,330,tx-58,420,'#000',5);line(tx+8,330,tx+58,420,'#000',5);}else if(terrorType===1||terrorType===3){rect(tx-12,235,24,255,'#010203');rect(tx-21,208,42,42,'#010203');rect(tx-9,222,6,6,'#e0d7bf');rect(tx+4,222,6,6,'#e0d7bf');}else if(terrorType===2){for(let i=0;i<22;i++)rect((i*61+t*14)%W,110+(i%7)*63,2,2,'#d4c9ae');}else if(terrorType===4){for(let i=0;i<3;i++){const sx=tx+rnd(-30,30);rect(sx-6,250,12,210,'#020303');rect(sx-10,228,20,28,'#020303');}}else{for(let i=0;i<7;i++){const lx=((tx+i*95+t*12)%W+W)%W;rect(lx,92,42,7,'#cfc3a5');}}ctx.restore();}
if(horrorBlackout>0){ctx.fillStyle='rgba(0,0,0,'+clamp(horrorBlackout*.78,0,.9)+')';ctx.fillRect(0,0,W,H);for(let i=0;i<8;i++)rect(rnd(0,W),rnd(0,H),rnd(30,180),rnd(1,4),'#171a1a');}
if(horrorEvent===1&&horrorWhisper>0){ctx.globalAlpha=.55;txt('...',W/2,H-115,18,'#9b9187','center');ctx.globalAlpha=1;}
if(horrorEvent===2&&horrorDoor>0){const bx=W/2+Math.sin(t*31)*rnd(90,180);ctx.globalAlpha=.45;rect(bx-38,120,76,390,'#060809');rect(bx-29,132,58,365,'#242829');for(let k=0;k<5;k++)rect(bx-20+k*11,135,4,350,'#4b4f4e');ctx.globalAlpha=1;}
if(horrorEvent===3&&horrorLunge>0){const a=clamp(horrorLunge/.55,0,1);ctx.globalAlpha=a;const bx=W/2+(1-a)*rnd(-80,80);rect(bx-55,170,110,370,'#020303');rect(bx-28,145,56,60,'#080909');rect(bx-20,168,12,9,'#ded5bf');rect(bx+8,168,12,9,'#ded5bf');line(bx-28,215,bx+28,215,'#ddd1bc',5);ctx.globalAlpha=1;}
if(horrorEvent===4&&horrorLife>0){ctx.globalAlpha=.8;txt('HE MOVED',W/2,120,16,'#783b3b','center');txt('WHEN YOU LOOKED AWAY',W/2,142,11,'#6d3737','center');ctx.globalAlpha=1;}
if(horrorEvent===5&&horrorLife>0){ctx.globalAlpha=.42;const bx=(horrorX-cam);rect(bx-22,240,44,230,'#030405');rect(bx-18,220,36,42,'#060708');rect(bx-13,236,7,7,'#d5cfb9');rect(bx+6,236,7,7,'#d5cfb9');ctx.globalAlpha=1;}
if(horrorEvent===6&&horrorLife>0){ctx.globalAlpha=.18+.12*Math.sin(t*22);ctx.fillStyle='#000';ctx.beginPath();ctx.arc(W/2,330,145,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}
if(horrorEvent===7&&horrorLife>0){ctx.globalAlpha=.8;for(let i=0;i<6;i++){const ex=130+i*190+Math.sin(t*9+i)*12;rect(ex,160,12,12,'#ddd5bf');rect(ex+28,160,12,12,'#ddd5bf');}ctx.globalAlpha=1;}
if(horrorEvent===8&&horrorLife>0&&chapter==='SAN FRANCISCO'){ctx.globalAlpha=.5;for(let i=0;i<4;i++){const bx=180+i*260+Math.sin(t*8+i)*20;rect(bx,300,30,190,'#050607');rect(bx+6,278,18,35,'#070809');}ctx.globalAlpha=1;}
if(flash>0){ctx.fillStyle='rgba(255,255,255,'+flash+')';ctx.fillRect(0,0,W,H);flash=Math.max(0,flash-.04);}if(jumpScare>0){const a=Math.min(1,jumpScare/.18),p1=1+(1-a)*.48;ctx.fillStyle='rgba(0,0,0,'+(.22+a*.68)+')';ctx.fillRect(0,0,W,H);const j=jumpType;const cx=W/2+rnd(-28,28),cy=H/2+25;ctx.save();ctx.globalAlpha=a;ctx.translate(cx,cy);ctx.scale(p1,p1);if(j===0){rect(-155,-210,310,420,'#020304');rect(-112,-255,224,72,'#060708');rect(-106,-125,64,64,'#ddd5bd');rect(42,-125,64,64,'#ddd5bd');rect(-86,-62,172,50,'#f0e6cf');for(let i=0;i<16;i++)rect(-75+i*10,-52+(i%2)*3,5,21,'#151617');}else if(j===1){rect(-78,-245,156,470,'#010203');rect(-126,-195,44,285,'#010203');rect(82,-195,44,285,'#010203');rect(-38,-112,24,20,'#eee5ce');rect(14,-112,24,20,'#eee5ce');line(-35,-35,35,-35,'#eee5ce',8);}else if(j===2){for(let i=0;i<10;i++)rect(-215+i*48,-190,18,390,'#1b2022');rect(-112,-72,224,20,'#d2c8af');rect(-70,-31,140,27,'#e1d6bc');rect(-92,-100,184,10,'#090b0c');}else if(j===3){rect(-120,-200,240,400,'#080a0b');for(let i=0;i<8;i++){const ex=-88+i*25;rect(ex,-80,13,13,'#e8dfc8');rect(ex+2,-77,5,7,'#181313');}line(-88,35,88,35,'#ddd2ba',9);line(-80,58,80,58,'#5b4c42',4);}else if(j===4){rect(-235,-185,470,370,'#030405');for(let i=0;i<5;i++){const ex=-155+i*78;rect(ex,-52,28,20,'#e8e0c9');rect(ex+7,-47,10,10,'#151313');}for(let i=0;i<7;i++)line(-200+i*66,-150,-220+i*66,150,'#161a1b',7);}else if(j===5){rect(-90,-245,180,500,'#010203');line(-45,-40,-190,115,'#010203',18);line(45,-40,190,115,'#010203',18);rect(-42,-120,25,22,'#e7deca');rect(17,-120,25,22,'#e7deca');line(-42,-25,42,-25,'#e7deca',7);}else if(j===6){rect(-185,-220,370,440,'#07090a');rect(-110,-135,80,75,'#ded5bf');rect(30,-135,80,75,'#ded5bf');for(let i=0;i<22;i++){const tx=-125+(i%11)*25,ty=-48+Math.floor(i/11)*22;rect(tx,ty,14,7,'#171313');}line(-105,50,105,50,'#d8ceba',9);}else{rect(-130,-235,260,470,'#010203');for(let i=0;i<12;i++){const ang=i*Math.PI/6;line(Math.cos(ang)*45,Math.sin(ang)*45,Math.cos(ang)*190,Math.sin(ang)*190,'#141719',4);}rect(-52,-72,30,24,'#e6deca');rect(22,-72,30,24,'#e6deca');line(-48,25,48,25,'#e6deca',8);}ctx.restore();ctx.globalAlpha=1;for(let i=0;i<12;i++){ctx.globalAlpha=.15*a;rect(rnd(0,W),rnd(0,H),rnd(2,8),rnd(2,5),i%2?'#d8d0bd':'#22282a');}ctx.globalAlpha=1;}}
function drawUltraPixelGrain(){if(mode!=='play')return;ctx.save();ctx.globalAlpha=.19;for(let i=0;i<1250;i++){const x=(i*97+Math.floor(t*43))%W,y=(i*53+Math.floor(t*23))%H;const s=i%17===0?4:i%7===0?2:1;const v=(i*17)%5;rect(x,y,s,s,v===0?'#090b0b':v===1?'#2a2a29':v===2?'#494542':v===3?'#70685f':'#9a9185');}ctx.globalAlpha=.13;for(let i=0;i<110;i++){const x=(i*137+Math.floor(t*31))%W;rect(x,0,1,H,i%3===0?'#9b8f82':'#3d4142');}ctx.globalAlpha=.1;for(let i=0;i<90;i++){const x=(i*211+Math.floor(t*18))%W,y=(i*79+Math.floor(t*12))%H;rect(x,y,2+(i%4),1+(i%3),i%2?'#7d7369':'#25292a');}ctx.restore();}
function loop(ts){const dt=Math.min(.033,(ts-last)/1000||0);last=ts;if(mode==='intro'){cutTimer+=dt;if(cutTimer>2.2){cutTimer=0;nextCut();}}update(dt);render();requestAnimationFrame(loop);}
function showNotice(){document.getElementById('pause').classList.add('hidden');document.getElementById('menu').classList.add('hidden');document.getElementById('notice').classList.remove('hidden');mode='notice';setTimeout(()=>document.getElementById('accept').focus(),0);}
function enterGameFromNotice(){document.getElementById('notice').classList.add('hidden');document.getElementById('menu').classList.remove('hidden');mode='menu';setTimeout(()=>{const first=document.querySelector('[data-name=\"Julia\"]');if(first)first.focus();},0);}
function startGame(n){name=n;document.getElementById('menu').classList.add('hidden');loadServerInfo();infoScareCooldown=rnd(7,14);intro();}
function pauseGame(){if(mode!=='play')return;mode='pause';document.getElementById('pause').classList.remove('hidden');}
function resumeGame(){mode='play';document.getElementById('pause').classList.add('hidden');}
document.getElementById('accept').onclick=enterGameFromNotice;
document.querySelectorAll('[data-name]').forEach(b=>b.onclick=()=>startGame(b.dataset.name));
document.getElementById('resume').onclick=resumeGame;
document.getElementById('restart').onclick=()=>{document.getElementById('pause').classList.add('hidden');resetChapter();};
document.getElementById('privacy').onclick=showNotice;document.getElementById('endingRestart').onclick=()=>{document.getElementById('ending').classList.add('hidden');document.getElementById('hud').classList.add('hidden');document.getElementById('menu').classList.remove('hidden');mode='menu';};
window.addEventListener('keydown',e=>{
 let k=e.key;if(mode==='notice'&&(k==='Enter'||k===' ')){e.preventDefault();enterGameFromNotice();return;}if(mode==='menu'&&(k==='Enter'||k===' ')){e.preventDefault();const first=document.querySelector('[data-name=\"Julia\"]');if(first)first.click();return;}if(mode==='intro'&&(k==='Enter'||k===' ')){e.preventDefault();nextCut();return;}if(k==='Escape'&&mode==='intro'){finishIntro();return;}if(k==='Escape'&&mode==='play'){pauseGame();return;}if(k==='Escape'&&mode==='pause'){resumeGame();return;}
 if(mode==='play'){if(k.toLowerCase()==='tab'){e.preventDefault();gadgetOpen=!gadgetOpen;document.getElementById('gadget').classList.toggle('hidden',!gadgetOpen);return;}if(k.toLowerCase()==='i'){e.preventDefault();const el=document.getElementById('inventory');el.classList.toggle('hidden');return;}keys.add(k.length===1?k.toLowerCase():k);if(k.toLowerCase()==='e')interact();if(k.toLowerCase()==='q'){for(const z of zombies)if(!z.dead&&Math.abs(z.x-p.x)<80){z.hp-=55;spawnBlood(z.x,z.y+25);setMsg('MELEE HIT',.6);}}if(k.toLowerCase()==='f'){p.light=!p.light;setMsg(p.light?'Flashlight on.':'Flashlight off.',1);}if(k.toLowerCase()==='g'&&!e.shiftKey&&p.grenades>0){p.grenades--;for(const z of zombies)if(!z.dead&&Math.abs(z.x-p.x)<250)z.hp-=100;flash=.22;shake=10;setMsg('GRENADE!',1.5);}}
});
window.addEventListener('keyup',e=>keys.delete(e.key.length===1?e.key.toLowerCase():e.key));
C.addEventListener('mousemove',e=>{const r=C.getBoundingClientRect();mouse.x=(e.clientX-r.left)*C.width/r.width;mouse.y=(e.clientY-r.top)*C.height/r.height;});
C.addEventListener('mousedown',e=>{if(e.button===0){mouse.down=true;shoot();}});window.addEventListener('mouseup',()=>mouse.down=false);setInterval(()=>{if(mouse.down&&mode==='play')shoot();},110);
ctx.fillStyle='#030405';ctx.fillRect(0,0,W,H);txt('ASHES OF THE DEAD',W/2,325,42,'#ddd','center');txt('THE SMILER IS ALWAYS WATCHING',W/2,365,15,'#8b7f7b','center');
requestAnimationFrame(loop);
</script>
</body>
</html>"""

@app.get("/")
def index():
    return Response(GAME_HTML, mimetype="text/html")

@app.get("/gadget")
def gadget():
    forwarded = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    seen = forwarded or request.remote_addr or "unknown"
    return jsonify({"server_seen_ip": seen, "user_agent": request.headers.get("User-Agent", "unknown"), "language": request.headers.get("Accept-Language", "unknown"), "note": "This is the address visible to the game server and may be a proxy address."})

@app.get("/health")
def health():
    return {"status":"ok","game":"Ashes of the Dead","chapter":"Alcatraz Escape"}



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
