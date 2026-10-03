from flask import Flask, Response, request, jsonify

app = Flask(__name__)

GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ashes of the Dead</title>
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#020304;color:#ddd;font-family:Consolas,monospace;overflow:hidden}body{display:grid;place-items:center}.shell{position:relative;width:min(100vw,1280px);aspect-ratio:16/9;background:#050708;overflow:hidden;box-shadow:0 0 90px #000}canvas{width:100%;height:100%;display:block;image-rendering:pixelated;image-rendering:crisp-edges}.layer{position:absolute;inset:0}.hidden{display:none!important}.screen{display:grid;place-items:center;background:rgba(2,3,4,.96);z-index:50}.panel{width:min(900px,92%);padding:30px;border:1px solid #4f575a;background:linear-gradient(#0b0f11,#050708);box-shadow:0 0 80px #000;position:relative}.panel:after{content:"";position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(255,255,255,.02),rgba(255,255,255,.02) 1px,transparent 1px,transparent 5px)}h1{letter-spacing:7px;margin:0 0 10px;font-size:40px;text-align:center;color:#ded8cd;text-shadow:3px 3px #000,0 0 30px #777}.subtitle{text-align:center;color:#817a75;letter-spacing:4px}.intro{text-align:center;color:#aaa;margin:20px auto;line-height:1.7;max-width:760px}.choices{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}.choices button,.panel button{font:inherit;color:#ddd;background:#111619;border:1px solid #596164;padding:12px 20px;cursor:pointer}.choices button:hover,.panel button:hover{background:#202629;border-color:#aaa}.warning{text-align:center;color:#765e5a;font-size:11px;letter-spacing:2px;margin-top:18px}.controls{text-align:center;color:#707879;font-size:11px;line-height:1.8;margin-top:16px}.hud{z-index:10;pointer-events:none;text-shadow:2px 2px #000}.top{position:absolute;left:16px;right:16px;top:14px;display:flex;justify-content:space-between;font-size:12px}.bars{width:210px}.bar{height:8px;background:#101314;border:1px solid #555;margin:3px 0 7px}.fill{height:100%}.health{background:#a94b47}.stamina{background:#879477}.sanity{background:#6e688f}.objective{position:absolute;left:18px;top:108px;max-width:500px;color:#ddd}.message{position:absolute;left:50%;bottom:50px;transform:translateX(-50%);padding:9px 15px;background:rgba(3,4,5,.86);border:1px solid #444b4e;color:#ddd}.prompt{position:absolute;left:50%;bottom:20px;transform:translateX(-50%);color:#c8c4bd}.inventory{position:absolute;right:18px;top:105px;width:245px;background:rgba(3,4,5,.92);border:1px solid #50585b;padding:12px;font-size:12px}.map{position:absolute;right:18px;bottom:18px;width:190px;height:70px;background:rgba(0,0,0,.6);border:1px solid #555}.vignette{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 36%,rgba(0,0,0,.82) 100%);mix-blend-mode:multiply}.warningText{position:absolute;top:24%;left:50%;transform:translateX(-50%);color:#c5b7ad;font-size:20px;letter-spacing:5px;text-shadow:0 0 15px #000,3px 3px #000}.gadget{z-index:40;background:rgba(2,3,4,.97);padding:30px}.gadgetBox{width:min(900px,94%);margin:auto;border:2px solid #555e62;background:#080c0e;padding:22px;box-shadow:0 0 70px #000}.gadgetGrid{display:grid;grid-template-columns:1fr 1fr;gap:9px;font-size:13px;line-height:1.6}.gadgetBox button{font:inherit;color:#ddd;background:#121719;border:1px solid #596164;padding:6px 10px;cursor:pointer}.gadgetTitle{font-size:23px;letter-spacing:4px}.infoFlash{z-index:65;background:rgba(0,0,0,.88);display:grid;place-items:center}.infoFlashBox{width:min(760px,90%);padding:26px;border:2px solid #8b3434;background:linear-gradient(#120b0c,#050607);box-shadow:0 0 90px #000,0 0 35px rgba(150,30,30,.35);text-align:left}.infoFlashTitle{font-size:25px;letter-spacing:5px;color:#d6c9c0;text-align:center;margin-bottom:18px}.infoFlashGrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:14px;line-height:1.55}.infoFlashGrid div{border-bottom:1px solid #292123;padding:7px}.infoFlashGrid b{color:#a84b49}.infoFlashClose{text-align:center;margin-top:18px;color:#777;font-size:11px;letter-spacing:2px}.cutscene{z-index:60;display:grid;place-items:center;background:#000}.cutline{text-align:center;max-width:900px;padding:30px;font-size:28px;line-height:1.5;text-shadow:4px 4px #000}.ending{z-index:70}.death{z-index:70;background:#080203}.small{font-size:11px;color:#777}.center{text-align:center}.red{color:#9c4643}.blood{color:#8e3837}
#privacyGate{position:fixed;inset:0;z-index:10000;display:flex;align-items:center;justify-content:center;padding:22px;background:rgba(0,0,0,.95);backdrop-filter:blur(7px)}#privacyGate .privacyBox{width:min(900px,96vw);max-height:90vh;overflow:auto;border:2px solid #68736d;background:linear-gradient(180deg,#101512,#070908);box-shadow:0 0 0 1px #202622,0 25px 90px #000;padding:26px;color:#d9dfdb}#privacyGate h1{margin:0 0 8px;font-size:26px;letter-spacing:2px;color:#f1f3f1}#privacyGate .privacyLead{color:#aab4ae;line-height:1.5}#privacyGate .privacyGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:16px 0}#privacyGate .privacyCard{border:1px solid #303934;background:#0b0f0d;padding:12px;line-height:1.45}#privacyGate .privacyCard b{display:block;color:#e6ebe8;margin-bottom:5px}#privacyGate .privacyNotice{border-left:3px solid #9da8a2;background:#0b0f0d;padding:11px 13px;color:#9da7a1;line-height:1.5}#privacyGate button,#privacyDashboard button{font:inherit;color:#eef1ef;background:#151b18;border:1px solid #68736d;padding:10px 15px;cursor:pointer}#privacyGate button:hover,#privacyDashboard button:hover{background:#252d29}#privacyDashboard{position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;padding:22px;background:rgba(0,0,0,.8);backdrop-filter:blur(5px)}#privacyDashboard .dashBox{width:min(1080px,96vw);max-height:90vh;overflow:auto;background:#090c0b;border:2px solid #59635e;box-shadow:0 25px 90px #000;padding:22px}#privacyDashboard .dashTop{display:flex;justify-content:space-between;align-items:center;gap:15px;border-bottom:1px solid #303633;padding-bottom:12px;margin-bottom:15px}#privacyDashboard h2{margin:0;font-size:23px;letter-spacing:1.5px}#privacyDashboard .dashSub{color:#89938d;font-size:12px;margin-top:4px}#privacyDashboard .dashGrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}#privacyDashboard .dashCard{border:1px solid #2d3531;background:#0d1110;padding:12px;min-height:68px}#privacyDashboard .dashLabel{font-size:10px;letter-spacing:1px;color:#78837d;text-transform:uppercase}#privacyDashboard .dashValue{font-size:14px;color:#dce2de;margin-top:7px;word-break:break-word}#privacyDashboard .dashBar{height:6px;background:#1a211e;margin-top:8px;overflow:hidden}#privacyDashboard .dashBar i{display:block;height:100%;background:#9ba69f}@media(max-width:760px){#privacyGate .privacyGrid,#privacyDashboard .dashGrid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div id="privacyGate"><div class="privacyBox"><h1>NIGHTWATCH SECURITY TERMINAL</h1><p class="privacyLead">ASHES OF THE DEAD — DEVICE INFORMATION NOTICE</p><div class="privacyGrid"><div class="privacyCard"><b>WHAT MAY BE DISPLAYED</b>Browser and platform details, screen size, language, timezone, online state, network hints, CPU thread count, touch support, cookies state, referrer, battery information when available, and the network address seen by the game server.</div><div class="privacyCard"><b>WHAT IS NOT READ</b>The game does not read passwords, personal files, photos, contacts, saved documents, account contents, or arbitrary data from your computer.</div><div class="privacyCard"><b>PERMISSIONS</b>Location, camera, and microphone information require separate browser permission.</div><div class="privacyCard"><b>FICTIONAL SURVEILLANCE</b>CCTV alerts, tracking messages, The Smiler observations, and horror-terminal events are fictional game elements unless explicitly identified as browser/server information.</div></div><div class="privacyNotice">The server can only see the network address that reaches it. A proxy, VPN, carrier network, or hosting layer can change the address shown. This is an entertainment game, not a security or diagnostic product.</div><div style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap"><button id="privacyAccept">ENTER ASHES OF THE DEAD</button><button id="privacyDetails">VIEW DEVICE PANEL</button></div></div></div><div id="privacyDashboard"><div class="dashBox"><div class="dashTop"><div><h2>NIGHTWATCH / PERSONAL DEVICE RECORD</h2><div class="dashSub">Press P to open or close this record</div></div><button id="privacyClose">CLOSE</button></div><div id="dashGrid" class="dashGrid"></div><div style="margin-top:14px;color:#7f8983;font-size:11px;line-height:1.5">Browser-exposed values can be unavailable or approximate. Location, camera, and microphone require permission. The server-seen address may be a proxy address. No passwords, personal files, photos, contacts, or account contents are read by this game.</div></div></div>
<div class="shell">
<canvas id="game" width="1280" height="720"></canvas>
<div id="menu" class="layer screen">
<div class="panel">
<h1>ASHES OF THE DEAD</h1>
<div class="subtitle">THE ALCATRAZ ESCAPE</div>
<div class="intro">Rain hits the island. Your cell is open. The prison is empty, but the walls are covered in warnings. Search the cell blocks, survive the island, discover what happened, and escape to San Francisco.</div>
<div class="choices"><button data-char="Julia">JULIA<br><span class="small">DETECTIVE</span></button><button data-char="May">MAY<br><span class="small">DETECTIVE</span></button><button data-char="Yumi">YUMI<br><span class="small">DETECTIVE</span></button></div>
<div class="warning">HEADPHONES RECOMMENDED • THE QUIET PART IS IMPORTANT</div>
<div class="controls">A/D OR ARROWS MOVE • SHIFT RUN • W/SPACE JUMP • E INTERACT • I INVENTORY • TAB GADGET • P PERSONAL INFO<br>F FLASHLIGHT • Q MELEE • G GRENADE • R RELOAD • MOUSE SHOOT • ESC PAUSE</div>
</div>
</div>
<div id="cutscene" class="layer cutscene hidden"><div id="cutline" class="cutline"></div></div>
<div id="pause" class="layer screen hidden"><div class="panel"><h1>PAUSED</h1><p class="center">The rain is still falling outside.</p><div class="center"><button id="resume">RESUME</button><button id="restart">RESTART CHAPTER</button><button id="backMenu">MAIN MENU</button></div></div></div>
<div id="ending" class="layer screen hidden"><div class="panel"><h1>YOU SURVIVED</h1><p id="endingText" class="intro"></p><div class="center"><button id="endingMenu">RETURN TO MENU</button></div></div></div>
<div id="death" class="layer screen hidden"><div class="panel"><h1 class="red">THE DARKNESS FOUND YOU</h1><p id="deathText" class="intro"></p><div class="center"><button id="deathRestart">RESTART</button><button id="deathMenu">MAIN MENU</button></div></div></div>
<div id="hud" class="layer hud hidden">
<div class="top"><div class="bars"><div>HEALTH <span id="healthText"></span></div><div class="bar"><div id="healthFill" class="fill health"></div></div><div>STAMINA <span id="staminaText"></span></div><div class="bar"><div id="staminaFill" class="fill stamina"></div></div><div>SANITY <span id="sanityText"></span></div><div class="bar"><div id="sanityFill" class="fill sanity"></div></div></div><div class="center"><div id="locationText">ALCATRAZ</div><div id="threatText">THE PRISON IS QUIET</div><div id="ammoText">AMMO 12 / 12</div></div></div>
<div id="objective" class="objective"></div><div id="message" class="message hidden"></div><div id="prompt" class="prompt"></div><div id="inventory" class="inventory hidden"></div><canvas id="map" class="map" width="380" height="140"></canvas><div class="vignette"></div><div id="warningText" class="warningText hidden"></div>
</div>
<div id="infoFlash" class="layer infoFlash hidden"><div class="infoFlashBox"><div class="infoFlashTitle">PERSONAL DEVICE RECORD</div><div class="infoFlashGrid"><div><b>SERVER IP</b><br><span id="flashIp">READING...</span></div><div><b>DEVICE</b><br><span id="flashDevice">READING...</span></div><div><b>BROWSER</b><br><span id="flashBrowser">READING...</span></div><div><b>SCREEN</b><br><span id="flashScreen">READING...</span></div><div><b>LANGUAGE</b><br><span id="flashLanguage">READING...</span></div><div><b>TIME ZONE</b><br><span id="flashTimezone">READING...</span></div><div><b>NETWORK</b><br><span id="flashNetwork">READING...</span></div><div><b>ONLINE</b><br><span id="flashOnline">READING...</span></div><div><b>CORES</b><br><span id="flashCores">READING...</span></div><div><b>BATTERY</b><br><span id="flashBattery">READING...</span></div><div><b>LOCATION</b><br><span id="flashLocation">NOT SHARED</span></div><div><b>TOUCH</b><br><span id="flashTouch">READING...</span></div><div><b>COOKIES</b><br><span id="flashCookies">AVAILABLE TO THIS SITE</span></div><div><b>REFERRER</b><br><span id="flashReferrer">NONE</span></div></div><div class="infoFlashClose">ESC OR ENTER TO CLOSE • THIS SCREEN USES INFORMATION AVAILABLE TO THE BROWSER OR GAME SERVER</div></div></div><div id="gadget" class="layer gadget hidden"><div class="gadgetBox"><div class="gadgetTitle">NIGHTWATCH // DEVICE PANEL</div><p class="small">Real browser information is shown only when the browser exposes it. Camera and microphone are never accessed unless you deliberately press the permission button.</p><div class="gadgetGrid"><div>SERVER-SEEN IP: <span id="gip">READING...</span></div><div>PLATFORM: <span id="gplatform">-</span></div><div>BROWSER: <span id="gbrowser">-</span></div><div>SCREEN: <span id="gscreen">-</span></div><div>LANGUAGE: <span id="glang">-</span></div><div>TIME ZONE: <span id="gtz">-</span></div><div>CPU THREADS: <span id="gcpu">-</span></div><div>NETWORK: <span id="gnet">-</span></div><div>BATTERY: <span id="gbat">-</span></div><div>ONLINE: <span id="gonline">-</span></div></div><div style="margin-top:14px">LOCATION: <span id="gloc">NOT SHARED</span> <button id="locate">SHARE LOCATION</button></div><div style="margin-top:10px">CAMERA/MIC: <span id="gperm">NOT ACCESSED</span> <button id="perm">OPTIONAL CHECK</button></div><div style="margin-top:20px;border:1px solid #333;padding:18px;color:#737b7d">P — SHOW PERSONAL DEVICE INFO • TAB TO CLOSE • THIS PANEL IS PART OF THE GAME. IT DOES NOT READ FILES, PASSWORDS, CONTACTS, OR ACCOUNTS.</div></div></div>
</div>
<script>
'use strict';

const canvas=document.getElementById('game');

const ctx=canvas.getContext('2d');

ctx.imageSmoothingEnabled=false;

const mapCanvas=document.getElementById('map');

const mapCtx=mapCanvas.getContext('2d');

const W=1280;

const H=720;

const GROUND=570;

const keys=new Set();

const mouse={x:640,y:360,down:false};

const serverInfo={ip:'UNAVAILABLE'};

let realLocation='NOT SHARED';

let audioCtx=null;

let mode='menu';

let chapter='ALCATRAZ';

let selectedCharacter='Julia';

let cutIndex=0;

let cutTimer=0;

let last=performance.now();

let totalTime=0;

let camera=0;

let flash=0;

let shake=0;

let messageTimer=0;

let scareTimer=18;

let eventTimer=12;

let quietTimer=0;

let blackout=0;

let interior=null;

let floor=1;

let endingTriggered=false;

let gadgetOpen=false;

let inventoryOpen=false;

let infoFlashOpen=false;

let infoFlashTimer=18+Math.random()*14;

let infoFlashCooldown=0;

let objectiveStep=0;

let survivorsFound=0;

let boatEscaped=false;

let archiveOpened=false;

let shelterReached=false;

let zombies=[];

let survivors=[];

let buildings=[];

let cells=[];

let chests=[];

let skeletons=[];

let writings=[];

let bloodMarks=[];

let particles=[];

let loot=[];

let bullets=[];

let footprints=[];

let doors=[];

let state={startKey:false,startEscaped:false,health:100,maxHealth:100,stamina:100,maxStamina:100,sanity:100,ammo:12,maxAmmo:12,grenades:2,light:true,hunger:100,battery:100,medkits:1,bandages:2,scrap:0,ammoReserve:36,keys:0,dockPass:false,archiveKey:false,food:2,xp:0,level:1};

let smiler={active:false,timer:8,next:24,x:0,y:0,side:1,phase:0,intensity:0};

function resetSmiler(){smiler={active:false,timer:8+Math.random()*8,next:20+Math.random()*35,x:0,y:0,side:1,phase:0,intensity:0};
}
function updateSmiler(dt){if(mode!=='play')return;
smiler.next-=dt;
smiler.phase+=dt*2;
if(smiler.active){smiler.timer-=dt;
smiler.intensity=Math.min(1,smiler.intensity+dt*2);
if(smiler.timer<=0){smiler.active=false;
smiler.intensity=0;
smiler.next=18+Math.random()*38;
setMsg('The corridor is empty.',1.2);
}}else if(smiler.next<=0&&state.sanity<92){smiler.active=true;
smiler.timer=2.2+Math.random()*4;
smiler.intensity=0;
smiler.side=Math.random()<.5?-1:1;
smiler.x=clamp(player.x+smiler.side*(520+Math.random()*260),80,chapter==='ALCATRAZ'?ALCATRAZ_WIDTH-80:SF_WIDTH-80);
smiler.y=GROUND-230;
smiler.next=30+Math.random()*45;
scareSound();
setMsg('SOMETHING IS WATCHING YOU.',2);
shake=2;
}}
function drawSmiler(){if(!smiler.active||mode!=='play')return;
const sx=smiler.x-camera;
if(sx<-160||sx>W+160)return;
const a=clamp(smiler.intensity,0,1)*.92;
ctx.save();
ctx.globalAlpha=a;
ctx.fillStyle='#030303';
ctx.beginPath();
ctx.ellipse(sx,smiler.y+90,38,112,0,0,Math.PI*2);
ctx.fill();
ctx.fillRect(sx-22,smiler.y-35,44,170);
ctx.beginPath();
ctx.ellipse(sx,smiler.y-43,31,39,0,0,Math.PI*2);
ctx.fill();
ctx.fillStyle='#ddd';
ctx.beginPath();
ctx.arc(sx-11,smiler.y-48,3,0,Math.PI*2);
ctx.arc(sx+11,smiler.y-48,3,0,Math.PI*2);
ctx.fill();
ctx.strokeStyle='#b8b0aa';
ctx.lineWidth=2;
ctx.beginPath();
ctx.arc(sx,smiler.y-37,16,.15,2.99);
ctx.stroke();
ctx.fillStyle='rgba(0,0,0,.8)';
ctx.fillRect(sx-9,smiler.y+60,18,100);
ctx.restore();
}
function triggerSmilerVision(){if(!smiler.active)return;
state.sanity=Math.max(0,state.sanity-.12);
flash=Math.max(flash,.04);
}

let player={x:180,y:GROUND-72,w:34,h:72,vx:0,vy:0,facing:1,onGround:true,anim:0,shootTimer:0,hitTimer:0};

const ALCATRAZ_WIDTH=4300;

const SF_WIDTH=8200;

const names=['Julia','May','Yumi'];

const cutsceneLines=[
'ALCATRAZ ISLAND — 11:47 PM',
'You wake in Cell A-17. The rain is louder than the prison.',
'The cell door is open. You do not remember opening it.',
'Across the corridor, twenty doors wait in the dark.',
'Blood writing covers the concrete: DO NOT LET HIM SEE YOU.',
'You need a way off the island. Search the prison.',
'If something moves, make sure it is not only your imagination.'
];

function clamp(v,a,b){return Math.max(a,Math.min(b,v));
}
function lerp(a,b,t){return a+(b-a)*t;
}
function rand(a,b){return a+Math.random()*(b-a);
}
function randi(a,b){return Math.floor(rand(a,b+1));
}
function dist(a,b){return Math.abs(a-b);
}
function rectHit(a,b){return a.x<a.w+b.x&&a.x+a.w>b.x&&a.y<a.h+b.y&&a.y+a.h>b.y;
}
function audio(){try{if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();
if(audioCtx.state==='suspended')audioCtx.resume();
return audioCtx;
}catch(e){return null;
}}
function tone(freq,duration,type='sine',volume=.05,slide=0){const ac=audio();
if(!ac)return;
const t=ac.currentTime;
const o=ac.createOscillator();
const g=ac.createGain();
o.type=type;
o.frequency.setValueAtTime(freq,t);
if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(20,freq+slide),t+duration);
g.gain.setValueAtTime(.0001,t);
g.gain.exponentialRampToValueAtTime(volume,t+.015);
g.gain.exponentialRampToValueAtTime(.0001,t+duration);
o.connect(g);
g.connect(ac.destination);
o.start(t);
o.stop(t+duration+.02);
}
function scareSound(){tone(72,.6,'sawtooth',.16,-45);
setTimeout(()=>tone(41,.8,'square',.08,-10),80);
}
function setMsg(text,time=2){const el=document.getElementById('message');
el.textContent=text;
el.classList.remove('hidden');
messageTimer=time;
}
function updateMessage(dt){if(messageTimer>0){messageTimer-=dt;
if(messageTimer<=0)document.getElementById('message').classList.add('hidden');
}}
function setObjective(){let text='';
if(chapter==='ALCATRAZ'){const list=['SEARCH CELL A-17: find the key under the mattress, then unlock the door.','SEARCH CELL BLOCK A: inspect the cells and follow the blood marks.','SEARCH CELL BLOCK B: find a way toward the prison dock.','FIND THE DOCK PASS: search the upper cells and offices.','REACH THE DOCK BEACON: use the pass and signal the ferry.','ESCAPE ALCATRAZ: board the waiting ferry.'];
text=list[Math.min(objectiveStep,list.length-1)];
}else{text=archiveOpened?'RETURN TO THE EMERGENCY SHELTER.':survivorsFound>=3?'FIND THE RESEARCH ANNEX ARCHIVE.':'FIND THE SURVIVORS IN SAN FRANCISCO.';
}document.getElementById('objective').textContent='OBJECTIVE\n'+text;
}
function resetWorld(){zombies=[];
survivors=[];
buildings=[];
cells=[];
chests=[];
skeletons=[];
writings=[];
bloodMarks=[];
particles=[];
loot=[];
bullets=[];
footprints=[];
doors=[];
interior=null;
floor=1;
camera=0;
objectiveStep=0;
survivorsFound=0;
boatEscaped=false;
archiveOpened=false;
shelterReached=false;
endingTriggered=false;
resetSmiler();
state={startKey:false,startEscaped:false,health:100,maxHealth:100,stamina:100,maxStamina:100,sanity:100,ammo:12,maxAmmo:12,grenades:2,light:true,hunger:100,battery:100,medkits:1,bandages:2,scrap:0,ammoReserve:36,keys:0,dockPass:false,archiveKey:false,food:2,xp:0,level:1};
player={x:220,y:GROUND-72,w:34,h:72,vx:0,vy:0,facing:1,anim:0,shootTimer:0,hitTimer:0};
}
function addBuilding(x,w,name,type='normal',floors=2){buildings.push({x,w,name,type,floors,visited:false});
}
function addWriting(x,y,text,scale=1){writings.push({x,y,text,scale,found:false});
}
function addSkeleton(x,y=GROUND){skeletons.push({x,y,phase:rand(0,6),type:randi(0,2)});
}
function addBlood(x,y,w=50){bloodMarks.push({x,y,w,drips:randi(1,5)});
}
function addChest(x,y=GROUND-38,rare=false,inside=false){chests.push({x,y,w:58,h:38,rare,opened:false,inside});
}
function addLoot(x,y,item,count=1){loot.push({x,y,item,count,taken:false});
}
function buildAlcatraz(){chapter='ALCATRAZ';
addBuilding(320,900,'CELL BLOCK A','prison',2);
addBuilding(1320,920,'CELL BLOCK B','prison',2);
addBuilding(2350,420,'GUARD STATION','station',2);
addBuilding(2850,520,'MEDICAL WING','medical',2);
addBuilding(3470,420,'WORKSHOP','workshop',2);
addBuilding(3970,300,'DOCK OFFICE','dock',2);
for(let i=0;
i<20;
i++){const block=i<10?0:1;
const local=i%10;
const base=block===0?370:1370;
cells.push({x:base+local*82,id:block===0?`A-${local+1}`:`B-${local+1}`,open:false,searched:false,block});
}for(let i=0;
i<20;
i++){const block=i<10?0:1;
const local=i%10;
addBlood((block===0?385:1385)+local*82,GROUND-120,rand(25,55));
if(i%2===0)addSkeleton((block===0?405:1405)+local*82,GROUND-5);
if(i===4||i===13)addWriting((block===0?390:1390)+local*82,GROUND-150,i===4?'HE LEFT THE LIGHTS ON':'DO NOT OPEN B-4',.55);
if(i%3===0)addChest((block===0?410:1410)+local*82,GROUND-40,i===18);
}addWriting(430,GROUND-210,'KEEP QUIET',.7);
addWriting(870,GROUND-205,'HE IS STILL HERE',.65);
addWriting(1540,GROUND-210,'DO NOT TRUST THE LIGHT',.58);
addWriting(2050,GROUND-210,'B-4 HAS THE PASS',.65);
addWriting(2580,GROUND-150,'THEY CLOSED THE WARD',.6);
addWriting(3650,GROUND-150,'THE DOCK IS NOT EMPTY',.55);
addSkeleton(1120);
addSkeleton(2240);
addSkeleton(2720);
addSkeleton(3400);
addChest(2600,GROUND-38,true);
addChest(3530,GROUND-38,true);
setObjective();
}
function buildSanFrancisco(){chapter='SAN FRANCISCO';
buildings=[];
chests=[];
skeletons=[];
writings=[];
bloodMarks=[];
addBuilding(520,620,'ABANDONED APARTMENT','apartment',2);
addBuilding(1320,650,'POLICE STATION','police',2);
addBuilding(2150,620,'HOSPITAL','hospital',3);
addBuilding(2940,500,'FUNERAL HOME','funeral',2);
addBuilding(3600,620,'OLD HOTEL','hotel',3);
addBuilding(4420,620,'EMERGENCY SHELTER','shelter',2);
addBuilding(5250,720,'RESEARCH ANNEX','research',3);
addBuilding(6250,540,'WAREHOUSE','warehouse',2);
addBuilding(7060,600,'CITY HALL','civic',2);
addChest(700,GROUND-38);
addChest(1500,GROUND-38);
addChest(2320,GROUND-38,true);
addChest(3820,GROUND-38);
addChest(4580,GROUND-38,true);
addChest(5400,GROUND-38,true);
addWriting(600,GROUND-170,'THEY CAME FROM THE BAY',.55);
addWriting(1420,GROUND-170,'POLICE LINE FAILED',.6);
addWriting(2250,GROUND-170,'DO NOT OPEN THE LOWER WARD',.5);
addWriting(3000,GROUND-170,'THE FUNERAL WAS FOR THE WRONG MAN',.46);
addWriting(4500,GROUND-170,'KEEP THE SURVIVORS TOGETHER',.5);
addWriting(5350,GROUND-170,'PROJECT ECLIPSE',.65);
for(let i=0;
i<6;
i++)spawnZombie(1150+i*370,i%3===0?'runner':'walker');
survivors=[{name:'Mara',role:'Nurse',x:920,found:false,follow:false},{name:'Eli',role:'Soldier',x:1950,found:false,follow:false},{name:'Noah',role:'Mechanic',x:4100,found:false,follow:false}];
setObjective();
setMsg('SAN FRANCISCO. This is where the dead are.',3);
}
function spawnZombie(x,type='walker'){if(chapter!=='SAN FRANCISCO'||zombies.filter(z=>!z.dead).length>=7)return;
zombies.push({x,y:GROUND-64,w:38,h:64,type,hp:type==='brute'?150:75,speed:type==='runner'?105:type==='brute'?38:52,attack:0,dead:false,phase:rand(0,5),hit:0});
}
function startGame(name){selectedCharacter=name;
resetWorld();
buildAlcatraz();
mode='intro';
cutIndex=0;
cutTimer=0;
hide('menu');
hide('hud');
show('cutscene');
audio();
}
function hide(id){document.getElementById(id).classList.add('hidden');
}
function show(id){document.getElementById(id).classList.remove('hidden');
}
function nextCut(){if(mode!=='intro')return;
cutIndex++;
if(cutIndex>=cutsceneLines.length)finishIntro();
else document.getElementById('cutline').textContent=cutsceneLines[cutIndex];
}
function finishIntro(){mode='play';
hide('cutscene');
show('hud');
document.getElementById('cutline').textContent='';
setObjective();
setMsg('SEARCH CELL A-17. Find the key, then open the door.',3);
}
function pauseGame(){if(mode!=='play')return;
mode='pause';
show('pause');
}
function resumeGame(){if(mode!=='pause')return;
mode='play';
hide('pause');
}
function restart(){startGame(selectedCharacter);
}
function closeInfoFlash(){infoFlashOpen=false;
hide('infoFlash');
}
async function showInfoFlash(){if(mode!=='play'||infoFlashOpen||infoFlashCooldown>0)return;
infoFlashOpen=true;
infoFlashCooldown=16;
show('infoFlash');
const set=(id,v)=>document.getElementById(id).textContent=v||'UNAVAILABLE';
set('flashDevice',navigator.platform||navigator.userAgentData?.platform||'UNKNOWN');
set('flashBrowser',navigator.userAgent||'UNKNOWN');
set('flashScreen',`${screen.width} x ${screen.height}`);
set('flashLanguage',navigator.language||'UNKNOWN');
set('flashTimezone',Intl.DateTimeFormat().resolvedOptions().timeZone||'UNKNOWN');
set('flashNetwork',navigator.connection?.effectiveType||'UNAVAILABLE');
set('flashOnline',navigator.onLine?'ONLINE':'OFFLINE');
set('flashCores',navigator.hardwareConcurrency||'UNKNOWN');
set('flashTouch',navigator.maxTouchPoints||0);
set('flashCookies',navigator.cookieEnabled?'ENABLED':'DISABLED');
set('flashReferrer',document.referrer||'NONE');
set('flashBattery','UNAVAILABLE');
if(navigator.getBattery){try{const b=await navigator.getBattery();
set('flashBattery',Math.round(b.level*100)+'%');
}catch(e){}}try{const r=await fetch('/gadget',{cache:'no-store'});
const d=await r.json();
set('flashIp',d.server_seen_ip||'UNAVAILABLE');
}catch(e){set('flashIp','UNAVAILABLE');
}if(realLocation&&realLocation!=='NOT SHARED')set('flashLocation',realLocation);
else set('flashLocation','NOT SHARED');
flash=.35;
shake=10;
tone(80,.25,'square',.04,-20);
}
function die(reason){if(mode!=='play')return;
mode='death';
document.getElementById('deathText').textContent=reason;
show('death');
scareSound();
flash=.7;
shake=20;
}
function win(text){if(endingTriggered)return;
endingTriggered=true;
mode='ending';
document.getElementById('endingText').textContent=text;
show('ending');
tone(180,.8,'triangle',.08,60);
}
function enterSF(){if(chapter!=='ALCATRAZ')return;
chapter='SAN FRANCISCO';
player.x=250;
camera=0;
buildSanFrancisco();
}
function insideBuilding(b){interior={building:b,entryX:player.x};
floor=1;
player.x=120;
player.y=520;
setMsg(`${b.name} — FLOOR 1`,2);
}
function exitBuilding(){const b=interior.building;
interior=null;
player.x=b.x+b.w+30;
player.y=GROUND-player.h;
floor=1;
setMsg(`Exited ${b.name}.`,1.5);
}
function currentCell(){if(chapter!=='ALCATRAZ'||interior)return null;
for(const c of cells){if(Math.abs(player.x-c.x)<36)return c;
}return null;
}
function currentBuilding(){if(interior)return null;
for(const b of buildings){if(player.x>b.x-40&&player.x<b.x+b.w+40)return b;
}return null;
}
function currentChest(){if(interior)return null;
return chests.find(c=>!c.opened&&Math.abs(c.x-player.x)<55);
}
function currentLoot(){return loot.find(x=>!x.taken&&Math.abs(x.x-player.x)<45);
}
function interact(){if(mode!=='play')return;
if(gadgetOpen)return;
if(chapter==='ALCATRAZ'&&!interior&&!state.startEscaped&&player.x<330){if(!state.startKey){state.startKey=true;
state.keys++;
setMsg('You found a small brass key under the mattress.',2);
setObjective();
tone(260,.18,'triangle',.03,30);
}else{setMsg('The cell is empty.',1);
}return;
}if(chapter==='ALCATRAZ'&&!interior&&!state.startEscaped&&player.x>=270){if(state.startKey||state.keys>0){state.startEscaped=true;
state.keys=Math.max(0,state.keys-1);
objectiveStep=1;
setMsg('CELL A-17 OPEN. The corridor is empty.',2.5);
setObjective();
tone(90,.35,'square',.04,-25);
}else setMsg('The cell door is locked.',1.5);
return;
}const l=currentLoot();
if(l){l.taken=true;
addItem(l.item,l.count);
setMsg(`Picked up ${itemName(l.item)} x${l.count}`,1.2);
return;
}if(interior){if(player.x>1100){exitBuilding();
return;
}if(Math.abs(player.x-620)<70){floor=floor===1?2:1;
player.x=170;
setMsg(`STAIRS — FLOOR ${floor}`,1.2);
tone(130,.25,'square',.04,-20);
return;
}if(player.x>760&&player.x<900){addChest(820,480,false,true);
const c=chests[chests.length-1];
if(!c.opened){openChest(c);
return;
}}return;
}const c=currentCell();
if(c){if(!c.open){if(state.keys>0){state.keys--;
c.open=true;
setMsg(`${c.id} unlocked.`,1.2);
}else{setMsg('Locked. Search your starting cell for a key.',1.5);
}return;
}if(!c.searched){c.searched=true;
state.sanity=Math.max(0,state.sanity-2);
if(c.id==='B-4'){state.dockPass=true;
objectiveStep=4;
setMsg('You found the DOCK PASS. The writing was true.',3);
addItem('ammo',8);
}else{const roll=Math.random();
if(roll<.4)addItem('bandage',1);
else if(roll<.7)addItem('ammo',6);
else addItem('scrap',randi(1,3));
setMsg('Cell searched.',1);
}}return;
}const ch=currentChest();
if(ch){openChest(ch);
return;
}const b=currentBuilding();
if(b){if(player.x>b.x+20&&player.x<b.x+b.w-20){insideBuilding(b);
return;
}}if(chapter==='ALCATRAZ'&&player.x>3850&&state.dockPass){enterSF();
return;
}if(chapter==='SAN FRANCISCO'){for(const s of survivors){if(!s.found&&Math.abs(player.x-s.x)<65){s.found=true;
survivorsFound++;
s.follow=true;
state.sanity=Math.min(100,state.sanity+8);
setMsg(`${s.name}: "Stay close. We need the others."`,2.5);
setObjective();
return;
}}if(player.x>5250&&player.x<5970&&survivorsFound>=3){archiveOpened=true;
setMsg('ARCHIVE OPENED. The files mention a ferry route.',3);
setObjective();
return;
}if(player.x>4420&&player.x<5040&&survivorsFound>=3&&archiveOpened){shelterReached=true;
win('Mara, Eli and Noah reached the shelter. The city is still screaming beyond the doors, but you made it through the night.');
}}}
function openChest(c){if(c.opened){setMsg('Empty.',1);
return;
}c.opened=true;
const n=c.rare?2:1;
addItem('ammo',c.rare?16:8);
addItem('bandage',n);
if(c.rare)addItem('medkit',1);
addItem('scrap',c.rare?5:2);
if(Math.random()<.35)addItem('food',1);
setMsg(c.rare?'Military cache searched.':'Supply chest opened.',1.8);
tone(190,.18,'triangle',.03,30);
}
function itemName(id){return({ammo:'Ammo',bandage:'Bandage',medkit:'Medkit',food:'Food',scrap:'Scrap',battery:'Battery'})[id]||id;
}
function addItem(id,n){if(id==='ammo')state.ammoReserve+=n;
else if(id==='bandage')state.bandages+=n;
else if(id==='medkit')state.medkits+=n;
else if(id==='food')state.food+=n;
else if(id==='scrap')state.scrap+=n;
else if(id==='battery')state.battery=clamp(state.battery+n,0,100);
}
function useItem(){if(state.medkits>0&&state.health<100){state.medkits--;
state.health=clamp(state.health+55,0,100);
setMsg('MEDKIT USED',1);
tone(420,.2,'sine',.03,80);
return;
}if(state.bandages>0&&state.health<100){state.bandages--;
state.health=clamp(state.health+25,0,100);
setMsg('BANDAGE USED',1);
}}
function shoot(){if(mode!=='play'||gadgetOpen||player.shootTimer>0)return;
if(state.ammo<=0){tone(70,.1,'square',.03);
setMsg('CLICK. RELOAD.',.7);
return;
}state.ammo--;
player.shootTimer=.16;
bullets.push({x:player.x+player.facing*28,y:player.y+30,vx:player.facing*620,life:1});
tone(150,.08,'square',.04,80);
flash=.08;
shake=2;
for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<480&&Math.sign(z.x-player.x)===player.facing&&Math.random()<.72){z.hp-=34;
z.hit=.12;
if(z.hp<=0){z.dead=true;
state.xp+=20;
setMsg('The street went quiet.',.8);
}}}}
function reload(){if(state.ammo<state.maxAmmo&&state.ammoReserve>0){const n=Math.min(state.maxAmmo-state.ammo,state.ammoReserve);
state.ammo+=n;
state.ammoReserve-=n;
setMsg('RELOADED',.7);
tone(250,.15,'triangle',.03,40);
}}
function updatePlayer(dt){if(interior){player.vx=0;
if(keys.has('a')||keys.has('ArrowLeft'))player.vx=-190;
if(keys.has('d')||keys.has('ArrowRight'))player.vx=190;
const run=keys.has('Shift');
if(run)player.vx*=1.45;
player.x=clamp(player.x+player.vx*dt,40,1210);
player.anim+=dt*Math.abs(player.vx)*.08;
return;
}let dir=0;
if(keys.has('a')||keys.has('ArrowLeft'))dir--;
if(keys.has('d')||keys.has('ArrowRight'))dir++;
let speed=190;
if(keys.has('Shift')&&state.stamina>2){speed=300;
state.stamina=Math.max(0,state.stamina-25*dt);
}else state.stamina=Math.min(100,state.stamina+13*dt);
player.vx=dir*speed;
if(dir)player.facing=dir;
player.vy+=1100*dt;
if((keys.has('w')||keys.has(' '))&&player.onGround){player.vy=-430;
player.onGround=false;
tone(90,.08,'triangle',.02,30);
}player.x=clamp(player.x+player.vx*dt,0,chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH);
if(chapter==='ALCATRAZ'&&!state.startEscaped)player.x=clamp(player.x,120,300);
player.y+=player.vy*dt;
if(player.y+player.h>=GROUND){player.y=GROUND-player.h;
player.vy=0;
player.onGround=true;
}player.anim+=dt*(dir?9:2);
if(player.hitTimer>0)player.hitTimer-=dt;
}
function updateZombies(dt){for(const z of zombies){if(z.dead)continue;
z.attack=Math.max(0,z.attack-dt);
z.hit=Math.max(0,z.hit-dt);
const d=player.x-z.x;
if(Math.abs(d)<760){z.x+=Math.sign(d)*z.speed*dt;
z.phase+=dt*(z.type==='runner'?11:6);
if(Math.abs(d)<42&&z.attack<=0){z.attack=1.1;
state.health-=z.type==='brute'?18:10;
state.sanity=Math.max(0,state.sanity-4);
player.hitTimer=.25;
shake=7;
tone(55,.16,'sawtooth',.05,-15);
if(state.health<=0)die('The dead surrounded you.');
}}}}
function updateSurvivors(dt){for(const s of survivors){if(!s.found)continue;
if(s.follow){s.x=lerp(s.x,player.x-70,dt*1.8);
}}}
function updateBullets(dt){for(const b of bullets){b.x+=b.vx*dt;
b.life-=dt;
for(const z of zombies){if(!z.dead&&Math.abs(z.x-b.x)<25){z.hp-=40;
z.hit=.12;
if(z.hp<=0)z.dead=true;
b.life=0;
}}}bullets=bullets.filter(b=>b.life>0&&b.x>-100&&b.x<(chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH));
}
function updateHunger(dt){if(chapter!=='SAN FRANCISCO')return;
state.hunger=Math.max(0,state.hunger-dt*.7);
if(state.hunger<20){state.stamina=Math.max(0,state.stamina-dt*3);
state.health=Math.max(0,state.health-dt*.8);
}}
function randomHorror(dt){scareTimer-=dt;
eventTimer-=dt;
quietTimer+=dt;
if(blackout>0)blackout-=dt;
if(scareTimer<=0){scareTimer=rand(28,52);
if(Math.random()<.45){blackout=rand(1.2,2.8);
state.sanity=Math.max(0,state.sanity-rand(3,8));
setMsg('The lights failed.',1.5);
tone(42,.5,'sine',.04,-15);
}else if(Math.random()<.5){showWarning(Math.random()<.5?'DON’T LOOK BEHIND YOU':'SOMETHING MOVED');
tone(65,.3,'triangle',.03,-25);
}else{const near=chapter==='ALCATRAZ'&&Math.random()<.6;
if(near){showWarning('A CELL DOOR JUST CLOSED');
shake=3;
tone(75,.25,'square',.03,-30);
}}}if(eventTimer<=0){eventTimer=rand(18,35);
if(Math.random()<.25){addBlood(player.x+rand(-100,100),GROUND-5,rand(20,80));
}if(Math.random()<.18){state.sanity=Math.max(0,state.sanity-5);
setMsg('You hear breathing. It stops when you stop.',2);
tone(48,.8,'sine',.02,-8);
}}if(state.sanity<30&&Math.random()<dt*.025){showWarning('HE IS AT THE END OF THE HALL');
state.sanity=Math.max(0,state.sanity-1);
}}
function showWarning(t){const el=document.getElementById('warningText');
el.textContent=t;
el.classList.remove('hidden');
setTimeout(()=>el.classList.add('hidden'),900);
}
function update(dt){totalTime+=dt;
infoFlashCooldown=Math.max(0,infoFlashCooldown-dt);
if(mode==='play'&&!infoFlashOpen){infoFlashTimer-=dt;
if(infoFlashTimer<=0){infoFlashTimer=32+Math.random()*42;
showInfoFlash();
}}updateMessage(dt);
updatePlayer(dt);
updateZombies(dt);
updateSurvivors(dt);
updateBullets(dt);
updateHunger(dt);
randomHorror(dt);
updateSmiler(dt);
triggerSmilerVision();
if(state.battery>0&&state.light)state.battery=Math.max(0,state.battery-dt*.25);
if(state.sanity<=0)die('You could no longer tell what was real.');
if(chapter==='ALCATRAZ'&&player.x>4100&&state.dockPass){objectiveStep=5;
setObjective();
}if(chapter==='SAN FRANCISCO'&&survivorsFound>=3&&!archiveOpened)setObjective();
flash=Math.max(0,flash-dt*2);
shake=Math.max(0,shake-dt*10);
camera=lerp(camera,player.x-W*.42,Math.min(1,dt*5));
const maxCam=(chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH)-W;
camera=clamp(camera,0,maxCam);
drawHUD();
}
function drawHUD(){document.getElementById('healthText').textContent=Math.ceil(state.health);
document.getElementById('staminaText').textContent=Math.ceil(state.stamina);
document.getElementById('sanityText').textContent=Math.ceil(state.sanity);
document.getElementById('healthFill').style.width=state.health+'%';
document.getElementById('staminaFill').style.width=state.stamina+'%';
document.getElementById('sanityFill').style.width=state.sanity+'%';
document.getElementById('ammoText').textContent=`AMMO ${state.ammo} / ${state.ammoReserve}`;
document.getElementById('locationText').textContent=interior?`${interior.building.name} • FLOOR ${floor}`:chapter;
document.getElementById('threatText').textContent=chapter==='ALCATRAZ'?'THE PRISON IS QUIET':'THE DEAD ARE MOVING';
const p=document.getElementById('prompt');
let t='';
if(interior){if(player.x>1080)t='E — EXIT';
else if(Math.abs(player.x-620)<75)t=`E — ${floor===1?'GO UP':'GO DOWN'} STAIRS`;
else t='SEARCH THE ROOM';
}else if(currentLoot())t='E — TAKE';
else if(chapter==='ALCATRAZ'&&!state.startEscaped)t=state.startKey?'E — OPEN CELL DOOR':'E — SEARCH CELL A-17';
else if(currentCell())t='E — SEARCH / OPEN CELL';
else if(currentChest())t='E — OPEN CHEST';
else if(currentBuilding())t='E — ENTER '+currentBuilding().name;
else if(chapter==='ALCATRAZ'&&player.x>3900&&state.dockPass)t='E — SIGNAL THE FERRY';
else if(chapter==='SAN FRANCISCO'&&survivors.some(s=>!s.found&&Math.abs(s.x-player.x)<70))t='E — TALK';
p.textContent=t;
const inv=document.getElementById('inventory');
if(inventoryOpen){inv.classList.remove('hidden');
inv.innerHTML=`<b>INVENTORY</b><hr>Ammo: ${state.ammoReserve}<br>Bandages: ${state.bandages}<br>Medkits: ${state.medkits}<br>Food: ${state.food}<br>Scrap: ${state.scrap}<br>Grenades: ${state.grenades}<br>Batteries: ${Math.floor(state.battery)}<br>Keys: ${state.keys}<br>Dock Pass: ${state.dockPass?'YES':'NO'}<br><br>H — use healing item`;
}else inv.classList.add('hidden');
drawMap();
}
function drawMap(){mapCtx.fillStyle='#050708';
mapCtx.fillRect(0,0,380,140);
const width=chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH;
const scale=360/width;
mapCtx.fillStyle='#333';
mapCtx.fillRect(8,108,364,3);
for(const b of buildings){mapCtx.fillStyle=b.type==='prison'?'#756':chapter==='SAN FRANCISCO'?'#5b6364':'#454a4b';
mapCtx.fillRect(8+b.x*scale,95,Math.max(3,b.w*scale),12);
}mapCtx.fillStyle='#ddd';
mapCtx.fillRect(8+player.x*scale,100,4,18);
}
function draw(){ctx.save();
let sx=shake?(Math.random()*shake-shake/2):0;
ctx.translate(sx,0);
ctx.fillStyle='#06090b';
ctx.fillRect(0,0,W,H);
if(interior)drawInterior();
else drawWorld();
drawWeather();
drawSmiler();
if(flash>0){ctx.fillStyle=`rgba(255,245,230,${flash})`;
ctx.fillRect(0,0,W,H);
}if(blackout>0){ctx.fillStyle=`rgba(0,0,0,${clamp(blackout/2,0,.92)})`;
ctx.fillRect(0,0,W,H);
}if(state.sanity<45){ctx.fillStyle=`rgba(30,5,15,${(45-state.sanity)/180})`;
ctx.fillRect(0,0,W,H);
}ctx.restore();
}
function drawWorld(){drawSky();
drawGround();
drawStructures();
drawBloodAndWriting();
drawSkeletons();
drawChests();
drawLoot();
drawSurvivors();
drawZombies();
drawPlayer();
}
function drawSky(){const sf=chapter==='SAN FRANCISCO';
ctx.fillStyle=sf?'#0a0d13':'#080a0d';
ctx.fillRect(0,0,W,H);
for(let i=0;
i<70;
i++){const x=(i*113-camera*.15)%W;
const y=(i*47)%360;
ctx.fillStyle=i%3?'#11161b':'#20252a';
ctx.fillRect(x,y,(i%4)+1,(i%2)+1);
}if(sf){for(let i=0;
i<14;
i++){const x=i*110-(camera*.08%110);
const h=70+(i%5)*30;
ctx.fillStyle='#11161a';
ctx.fillRect(x,370-h,85,h);
for(let w=0;
w<4;
w++){for(let q=0;
q<3;
q++){if((i+w+q)%3===0){ctx.fillStyle='#514c3d';
ctx.fillRect(x+10+w*18,380-h+12+q*22,5,8);
}}}}}else{ctx.fillStyle='#161a1d';
ctx.fillRect(0,350,W,70);
for(let i=0;
i<16;
i++){ctx.fillRect(i*100-(camera*.12%100),320-(i%4)*15,70,60);
}}}
function drawGround(){ctx.fillStyle=chapter==='ALCATRAZ'?'#171a1b':'#181a1b';
ctx.fillRect(0,430,W,290);
for(let i=0;
i<420;
i++){const x=(i*71-camera)%W;
const y=440+(i*37)%250;
ctx.fillStyle=i%5===0?'#3b3d3d':i%2?'#252828':'#202323';
ctx.fillRect(x,y,1+(i%4),1+(i%3));
}ctx.fillStyle='#101213';
ctx.fillRect(0,GROUND,W,150);
for(let i=0;
i<55;
i++){const x=(i*97-camera*1.3)%W;
ctx.fillStyle='#353636';
ctx.fillRect(x,GROUND+12+(i%4)*18,20+(i%5)*9,2);
}}
function drawStructures(){for(const b of buildings){const x=b.x-camera;
if(x<-b.w||x>W)continue;
const h=b.type==='prison'?250:b.floors*105+80;
ctx.fillStyle=b.type==='prison'?'#25292b':'#202426';
ctx.fillRect(x,GROUND-h,b.w,h);
ctx.fillStyle='#34393b';
ctx.fillRect(x,GROUND-h,b.w,8);
ctx.fillStyle='#0d1011';
ctx.fillRect(x+10,GROUND-h+20,b.w-20,8);
for(let yy=GROUND-h+45;
yy<GROUND-30;
yy+=55){for(let xx=x+20;
xx<x+b.w-20;
xx+=45){ctx.fillStyle=(Math.floor(xx)+Math.floor(yy))%3?'#0c1011':'#48463d';
ctx.fillRect(xx,yy,18,24);
ctx.fillStyle='#101315';
ctx.fillRect(xx+2,yy+2,14,20);
}}ctx.fillStyle='#080a0b';
ctx.fillRect(x+b.w/2-22,GROUND-65,44,65);
ctx.fillStyle='#575b59';
ctx.fillRect(x+b.w/2-2,GROUND-35,4,4);
for(let i=0;
i<5;
i++){ctx.fillStyle='#303436';
ctx.fillRect(x+20+i*18,GROUND-h-12,12,12);
}}}
function drawBloodAndWriting(){for(const b of bloodMarks){const x=b.x-camera;
if(x<-100||x>W+100)continue;
ctx.fillStyle='#5b1e1e';
ctx.beginPath();
ctx.ellipse(x,b.y,Math.max(8,b.w/2),5,0,0,Math.PI*2);
ctx.fill();
for(let i=0;
i<b.drips;
i++){ctx.fillRect(x-b.w/3+i*7,b.y,2,7+i*4);
}}for(const w of writings){const x=w.x-camera;
if(x<-200||x>W+200)continue;
ctx.fillStyle='#8c3635';
ctx.font=`${Math.max(12,20*w.scale)}px Consolas`;
ctx.save();
ctx.translate(x,w.y);
ctx.rotate((Math.sin(w.x)*.01));
ctx.fillText(w.text,0,0);
ctx.restore();
}}
function drawSkeletons(){for(const s of skeletons){const x=s.x-camera;
if(x<-80||x>W+80)continue;
const bob=Math.sin(totalTime*1.3+s.phase)*1.5;
ctx.strokeStyle='#b2aa98';
ctx.lineWidth=4;
ctx.beginPath();
ctx.moveTo(x,GROUND-42+bob);
ctx.lineTo(x,GROUND-12+bob);
ctx.moveTo(x,GROUND-34+bob);
ctx.lineTo(x-24,GROUND-22+bob);
ctx.moveTo(x,GROUND-34+bob);
ctx.lineTo(x+24,GROUND-22+bob);
ctx.moveTo(x,GROUND-12+bob);
ctx.lineTo(x-14,GROUND+2);
ctx.moveTo(x,GROUND-12+bob);
ctx.lineTo(x+14,GROUND+2);
ctx.stroke();
ctx.fillStyle='#b2aa98';
ctx.fillRect(x-8,GROUND-62+bob,16,16);
ctx.fillStyle='#17191a';
ctx.fillRect(x-4,GROUND-58+bob,3,4);
ctx.fillRect(x+2,GROUND-58+bob,3,4);
}}
function drawChests(){for(const c of chests){if(c.inside)continue;
const x=c.x-camera;
if(x<-70||x>W+70)continue;
ctx.fillStyle=c.opened?'#2d2924':c.rare?'#54463a':'#46382d';
ctx.fillRect(x,c.y,c.w,c.h);
ctx.strokeStyle='#171413';
ctx.strokeRect(x,c.y,c.w,c.h);
ctx.fillStyle='#9b7d45';
ctx.fillRect(x+c.w/2-4,c.y+14,8,8);
}}
function drawLoot(){for(const l of loot){if(l.taken)continue;
const x=l.x-camera;
ctx.fillStyle=l.item==='ammo'?'#bca35d':l.item==='medkit'?'#c7c0b5':l.item==='food'?'#77704f':'#777';
ctx.fillRect(x,l.y,12,12);
}}
function drawPlayer(){const x=player.x-camera;
const bob=player.onGround?Math.sin(player.anim)*2:0;
ctx.fillStyle='rgba(0,0,0,.5)';
ctx.fillRect(x-12,GROUND-4,58,8);
ctx.fillStyle='#2a3032';
ctx.fillRect(x+6,player.y+30+bob,22,30);
ctx.fillStyle='#60605a';
ctx.fillRect(x+8,player.y+2+bob,20,25);
ctx.fillStyle='#17191a';
ctx.fillRect(x+8,player.y+24+bob,20,7);
ctx.fillStyle='#b1a99c';
ctx.fillRect(x+11,player.y-1+bob,15,15);
ctx.fillStyle='#121516';
ctx.fillRect(x+7,player.y-4+bob,22,8);
ctx.fillStyle='#3f4646';
ctx.fillRect(x+3,player.y+31+bob,7,28);
ctx.fillRect(x+25,player.y+31+bob,7,28);
ctx.fillStyle='#111';
ctx.fillRect(x+1,player.y+58+bob,12,10);
ctx.fillRect(x+24,player.y+58+bob,12,10);
ctx.strokeStyle='#8a8f8e';
ctx.lineWidth=4;
ctx.beginPath();
ctx.moveTo(x+27,player.y+36+bob);
ctx.lineTo(x+45*player.facing,player.y+42+bob);
ctx.stroke();
}
function drawZombies(){for(const z of zombies){if(z.dead)continue;
const x=z.x-camera;
const bob=Math.sin(z.phase)*2;
ctx.fillStyle='rgba(0,0,0,.55)';
ctx.fillRect(x-10,GROUND-5,52,8);
ctx.fillStyle=z.type==='runner'?'#343b35':z.type==='brute'?'#393431':'#343735';
ctx.fillRect(x+7,z.y+25+bob,24,z.h-25);
ctx.fillStyle='#74776c';
ctx.fillRect(x+8,z.y+2+bob,22,24);
ctx.fillStyle='#090b0b';
ctx.fillRect(x+6,z.y+18+bob,28,9);
ctx.fillStyle='#d9cfc0';
ctx.fillRect(x+12,z.y+10+bob,4,4);
ctx.fillRect(x+23,z.y+10+bob,4,4);
ctx.strokeStyle='#4b504c';
ctx.lineWidth=6;
ctx.beginPath();
ctx.moveTo(x+9,z.y+32+bob);
ctx.lineTo(x-9,z.y+52+bob);
ctx.moveTo(x+30,z.y+32+bob);
ctx.lineTo(x+48,z.y+52+bob);
ctx.stroke();
}}
function drawSurvivors(){for(const s of survivors){const x=s.x-camera;
if(x<-50||x>W+50)continue;
ctx.fillStyle='#2b3430';
ctx.fillRect(x,GROUND-58,28,50);
ctx.fillStyle='#9d9a8d';
ctx.fillRect(x+7,GROUND-75,15,15);
ctx.fillStyle='#121515';
ctx.fillRect(x+5,GROUND-61,19,7);
}}
function drawInterior(){ctx.fillStyle='#090b0c';
ctx.fillRect(0,0,W,H);
const b=interior.building;
ctx.fillStyle=b.type==='prison'?'#262a2b':'#202426';
ctx.fillRect(0,80,W,480);
ctx.fillStyle='#151819';
ctx.fillRect(0,520,W,200);
for(let i=0;
i<18;
i++){ctx.fillStyle=i%3?'#292e2f':'#363a3a';
ctx.fillRect(i*80,520,60,3);
ctx.fillRect(i*80+15,80,3,440);
}for(let i=0;
i<16;
i++){const x=i*90;
ctx.fillStyle=i%3?'#3d413e':'#5a5545';
ctx.fillRect(x+20,105,40,8);
if(i%2===0){ctx.fillStyle='#171a1b';
ctx.fillRect(x+27,125,26,65);
}}ctx.fillStyle='#080a0b';
ctx.fillRect(600,80,5,440);
ctx.fillStyle='#65635a';
ctx.fillRect(570,90,65,10);
for(let i=0;
i<25;
i++){ctx.fillStyle=i%4?'#252a2b':'#4a4038';
ctx.fillRect((i*61)%W,205+(i%5)*55,8+(i%4)*4,4);
}drawInteriorObjects(b);
drawInteriorLoot();
drawPlayerInterior();
}
function drawInteriorObjects(b){ctx.fillStyle='#141719';
ctx.fillRect(40,430,190,80);
ctx.fillStyle='#33383a';
ctx.fillRect(55,390,160,35);
ctx.fillStyle='#0d1011';
ctx.fillRect(80,330,90,60);
ctx.fillStyle='#4a4038';
ctx.fillRect(770,410,170,100);
ctx.fillStyle='#292d2e';
ctx.fillRect(800,360,110,50);
ctx.fillStyle='#121516';
ctx.fillRect(1090,130,90,390);
ctx.fillStyle='#77706a';
ctx.fillRect(1110,160,50,4);
ctx.fillStyle='#5a2423';
ctx.fillRect(300,480,80,10);
ctx.fillStyle='#8a3635';
ctx.font='18px Consolas';
ctx.fillText(b.name.toUpperCase(),280,300);
ctx.fillStyle='#777';
ctx.fillText(`FLOOR ${floor}`,560,115);
ctx.fillStyle='#090b0c';
ctx.fillRect(580,410,80,110);
ctx.fillStyle='#4a4d4c';
ctx.fillRect(585,420,70,6);
ctx.fillRect(585,450,70,6);
ctx.fillRect(585,480,70,6);
}
function drawInteriorLoot(){for(const c of chests){if(!c.inside||c.opened)continue;
ctx.fillStyle=c.rare?'#5b4b3d':'#45382e';
ctx.fillRect(c.x-30,c.y-40,60,40);
ctx.fillStyle='#9b7d45';
ctx.fillRect(c.x-4,c.y-26,8,8);
}}
function drawPlayerInterior(){const x=player.x;
const y=player.y;
ctx.fillStyle='rgba(0,0,0,.5)';
ctx.fillRect(x-12,GROUND-4,58,8);
ctx.fillStyle='#2a3032';
ctx.fillRect(x+6,y+30,22,30);
ctx.fillStyle='#60605a';
ctx.fillRect(x+8,y+2,20,25);
ctx.fillStyle='#b1a99c';
ctx.fillRect(x+11,y-1,15,15);
ctx.fillStyle='#111';
ctx.fillRect(x+1,y+58,12,10);
ctx.fillRect(x+24,y+58,12,10);
}
function drawWeather(){if(interior)return;
ctx.strokeStyle='rgba(155,170,180,.35)';
ctx.lineWidth=1;
for(let i=0;
i<150;
i++){const x=(i*47+totalTime*210)%W;
const y=(i*83+totalTime*430)%H;
ctx.beginPath();
ctx.moveTo(x,y);
ctx.lineTo(x-5,y+15);
ctx.stroke();
}for(let i=0;
i<80;
i++){const x=(i*97-camera*.7)%W;
const y=430+(i*53)%260;
ctx.fillStyle=i%3?'#292d2e':'#3c3f3f';
ctx.fillRect(x,y,2,2);
}}
function renderLoop(){requestAnimationFrame(renderLoop);
const now=performance.now();
const dt=Math.min(.035,(now-last)/1000);
last=now;
if(mode==='play')update(dt);
draw();
}
window.addEventListener('keydown',e=>{const k=e.key.length===1?e.key.toLowerCase():e.key;
if(mode==='menu')return;
if(mode==='intro'&&(k==='Enter'||k===' ')){e.preventDefault();
nextCut();
return;
}if(k==='Escape'){if(infoFlashOpen){closeInfoFlash();
return}if(mode==='intro'){finishIntro();
return}if(mode==='play'){pauseGame();
return}if(mode==='pause'){resumeGame();
return}}if(mode!=='play')return;
if(k==='Enter'&&infoFlashOpen){closeInfoFlash();
return}if(k==='p'){e.preventDefault();
openPrivacyDashboard();
return}if(k==='Tab'){e.preventDefault();
gadgetOpen=!gadgetOpen;
document.getElementById('gadget').classList.toggle('hidden',!gadgetOpen);
if(gadgetOpen)loadGadget();
return}if(k==='i'){e.preventDefault();
inventoryOpen=!inventoryOpen;
return}if(k==='e'){interact();
return}if(k==='r'){reload();
return}if(k==='h'){useItem();
return}if(k==='f'){state.light=!state.light;
setMsg(state.light?'Flashlight on.':'Flashlight off.',1);
return}if(k==='q'){for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<80){z.hp-=55;
z.hit=.15;
shake=4;
setMsg('MELEE HIT',.5);
if(z.hp<=0)z.dead=true;
}}return}if(k==='g'&&state.grenades>0){state.grenades--;
for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<250)z.hp-=110;
}flash=.18;
shake=10;
tone(70,.4,'sawtooth',.08,-30);
setMsg('GRENADE',1);
return}keys.add(k);
});

window.addEventListener('keyup',e=>{const k=e.key.length===1?e.key.toLowerCase():e.key;
keys.delete(k);
});

canvas.addEventListener('mousemove',e=>{const r=canvas.getBoundingClientRect();
mouse.x=(e.clientX-r.left)*W/r.width;
mouse.y=(e.clientY-r.top)*H/r.height;
});

canvas.addEventListener('mousedown',e=>{if(e.button===0){mouse.down=true;
shoot();
}});
window.addEventListener('mouseup',()=>mouse.down=false);
setInterval(()=>{if(mouse.down&&mode==='play')shoot();
},150);

document.querySelectorAll('[data-char]').forEach(b=>b.addEventListener('click',()=>startGame(b.dataset.char)));

document.getElementById('resume').onclick=resumeGame;

document.getElementById('restart').onclick=restart;

document.getElementById('backMenu').onclick=()=>{mode='menu';
hide('pause');
hide('hud');
show('menu');
};

document.getElementById('endingMenu').onclick=()=>{mode='menu';
hide('ending');
hide('hud');
show('menu');
};

document.getElementById('deathRestart').onclick=restart;

document.getElementById('deathMenu').onclick=()=>{mode='menu';
hide('death');
hide('hud');
show('menu');
};

async function loadGadget(){document.getElementById('gplatform').textContent=navigator.platform||'UNKNOWN';
document.getElementById('gbrowser').textContent=navigator.userAgent||'UNKNOWN';
document.getElementById('gscreen').textContent=`${screen.width} x ${screen.height}`;
document.getElementById('glang').textContent=navigator.language||'UNKNOWN';
document.getElementById('gtz').textContent=Intl.DateTimeFormat().resolvedOptions().timeZone||'UNKNOWN';
document.getElementById('gcpu').textContent=navigator.hardwareConcurrency||'UNKNOWN';
document.getElementById('gonline').textContent=navigator.onLine?'YES':'NO';
document.getElementById('gnet').textContent=navigator.connection?.effectiveType||'UNAVAILABLE';
document.getElementById('gbat').textContent='UNAVAILABLE';
if(navigator.getBattery){try{const b=await navigator.getBattery();
document.getElementById('gbat').textContent=Math.round(b.level*100)+'%';
}catch(e){}}try{const r=await fetch('/gadget',{cache:'no-store'});
const d=await r.json();
document.getElementById('gip').textContent=d.server_seen_ip||'UNAVAILABLE';
}catch(e){document.getElementById('gip').textContent='UNAVAILABLE';
}}
document.getElementById('locate').onclick=()=>{if(!navigator.geolocation){document.getElementById('gloc').textContent='UNAVAILABLE';
return}document.getElementById('gloc').textContent='REQUESTING PERMISSION';
navigator.geolocation.getCurrentPosition(p=>{realLocation=`${p.coords.latitude.toFixed(5)}, ${p.coords.longitude.toFixed(5)}`;
document.getElementById('gloc').textContent=realLocation;
},()=>document.getElementById('gloc').textContent='DENIED OR UNAVAILABLE',{enableHighAccuracy:false,maximumAge:60000,timeout:8000});
};

document.getElementById('perm').onclick=async()=>{if(!navigator.mediaDevices?.getUserMedia){document.getElementById('gperm').textContent='UNAVAILABLE';
return}try{document.getElementById('gperm').textContent='REQUESTING';
const stream=await navigator.mediaDevices.getUserMedia({video:true,audio:true});
stream.getTracks().forEach(t=>t.stop());
document.getElementById('gperm').textContent='GRANTED / RELEASED';
}catch(e){document.getElementById('gperm').textContent='DENIED OR UNAVAILABLE';
}};

function start(){document.getElementById('cutline').textContent=cutsceneLines[0];
renderLoop();
}
start();

function openPrivacyDashboard(){const p=document.getElementById('privacyDashboard');
if(!p)return;
p.style.display='flex';
buildPrivacyDashboard();
}
function closePrivacyDashboard(){const p=document.getElementById('privacyDashboard');
if(p)p.style.display='none';
}
function dashItem(label,value,bar){const e=document.createElement('div');
e.className='dashCard';
const v=value===undefined||value===null||value===''?'Unavailable':String(value);
e.innerHTML='<div class="dashLabel">'+label+'</div><div class="dashValue">'+v.replace(/</g,'&lt;').replace(/>/g,'&gt;')+'</div>'+(bar!==undefined?'<div class="dashBar"><i style="width:'+Math.max(0,Math.min(100,Number(bar)||0))+'%"></i></div>':'');
return e;
}
async function buildPrivacyDashboard(){const g=document.getElementById('dashGrid');
if(!g)return;
g.innerHTML='';
let ip='Unavailable';
try{const r=await fetch('/gadget',{cache:'no-store'});
if(r.ok){const d=await r.json();
ip=d.server_seen_ip||'Unavailable';
}}catch(e){}const n=navigator;
const c=n.connection||n.mozConnection||n.webkitConnection;
const rows=[['SERVER-SEEN IP',ip],['PLATFORM',n.platform],['BROWSER',n.userAgent],['SCREEN',screen.width+' × '+screen.height+' / '+screen.colorDepth+' bit'],['LANGUAGE',n.language],['TIMEZONE',Intl.DateTimeFormat().resolvedOptions().timeZone],['CPU THREADS',n.hardwareConcurrency],['NETWORK',c?(c.effectiveType||c.type):'Unavailable'],['ONLINE',n.onLine?'ONLINE':'OFFLINE',n.onLine?100:0],['TOUCH POINTS',n.maxTouchPoints||0],['COOKIES',n.cookieEnabled?'ENABLED':'DISABLED'],['REFERRER',document.referrer||'Direct / none'],['DEVICE TIME',new Date().toLocaleString()],['BATTERY','Unavailable'],['LOCATION','Permission required'],['CAMERA / MIC','Permission required']];
rows.forEach(r=>g.appendChild(dashItem(r[0],r[1],r[2])));
if(n.getBattery){try{const b=await n.getBattery();
const card=dashItem('BATTERY',Math.round(b.level*100)+'% '+(b.charging?'charging':'not charging'),b.level*100);
g.replaceChild(card,g.children[13]);
}catch(e){}}}
function setupPrivacyUi(){const gate=document.getElementById('privacyGate');
const accept=document.getElementById('privacyAccept');
const details=document.getElementById('privacyDetails');
const close=document.getElementById('privacyClose');
if(!gate)return;
if(localStorage.getItem('ashesofthedead_privacy_seen')==='1')gate.style.display='none';
if(accept)accept.onclick=()=>{localStorage.setItem('ashesofthedead_privacy_seen','1');
gate.style.display='none';
};
if(details)details.onclick=()=>openPrivacyDashboard();
if(close)close.onclick=()=>closePrivacyDashboard();
window.addEventListener('keydown',e=>{if(e.key.toLowerCase()==='p'&&!e.repeat){const d=document.getElementById('privacyDashboard');
if(d&&d.style.display==='flex')closePrivacyDashboard();
else openPrivacyDashboard();
}});
}
setupPrivacyUi();

</script>
</div>
</body>
</html>"""

@app.get("/")
def index():
    return Response(GAME_HTML, mimetype="text/html")

@app.get("/gadget")
def gadget():
    forwarded = request.headers.get("X-Forwarded-For", "")
    seen = forwarded.split(",")[0].strip() if forwarded else request.remote_addr
    return jsonify({"server_seen_ip": seen or "unknown", "note": "The address visible to the game server may be a proxy address."})

@app.get("/health")
def health():
    return {"status":"ok","game":"Ashes of the Dead","chapter":"Alcatraz Escape"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
