from flask import Flask, Response

app = Flask(__name__)

GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ashes of the Dead — Alcatraz Escape</title>
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#030506;color:#eee;font-family:Consolas,monospace;overflow:hidden}body{display:grid;place-items:center}.shell{position:relative;width:min(100vw,1280px);aspect-ratio:16/9;background:#080b0e;overflow:hidden;box-shadow:0 0 70px #000}canvas{display:block;width:100%;height:100%;image-rendering:pixelated;image-rendering:crisp-edges;background:#080b0e}.layer{position:absolute;inset:0}.hidden{display:none!important}.notice,.menu,.pause{display:grid;place-items:center;background:rgba(2,3,4,.96);z-index:50}.cutscene{display:grid;place-items:center;background:rgba(0,0,0,.12);z-index:50}.panel{max-width:820px;padding:30px;border:2px solid #656a6d;background:#0b0f12;box-shadow:0 0 50px #000}.panel h1{letter-spacing:5px;margin:0 0 15px;font-size:28px}.panel p{color:#bbb;line-height:1.65}.panel button{font:inherit;color:#eee;background:#151a1e;border:1px solid #73787b;padding:12px 22px;margin:7px;cursor:pointer}.panel button:hover{background:#242b30}.name{display:flex;flex-wrap:wrap;justify-content:center}.title{text-align:center;letter-spacing:7px;font-size:36px}.subtitle{text-align:center;color:#888;letter-spacing:4px;margin-bottom:28px}.controls{font-size:12px;color:#888;text-align:center;line-height:1.8;margin-top:18px}.cutscene{padding:35px;text-align:center}.cutline{max-width:930px;font-size:clamp(18px,2.6vw,32px);line-height:1.55;text-shadow:3px 3px #000;margin-top:250px}.cutmeta{position:absolute;bottom:20px;right:20px;color:#666;font-size:12px}.hud{pointer-events:none;z-index:10}.hudtop{position:absolute;left:18px;right:18px;top:14px;display:flex;justify-content:space-between;text-shadow:2px 2px #000;font-size:12px}.bar{width:190px;height:9px;border:1px solid #777;background:#111;margin:3px 0 8px}.fill{height:100%;width:100%}.hp{background:#a84a46}.stam{background:#8b8f76}.san{background:#716b91}.objective{position:absolute;left:18px;top:105px;max-width:440px;color:#ddd;text-shadow:2px 2px #000}.message{position:absolute;left:50%;bottom:55px;transform:translateX(-50%);padding:9px 16px;background:rgba(5,7,8,.82);border:1px solid #454b4f;color:#ddd}.prompt{position:absolute;left:50%;bottom:24px;transform:translateX(-50%);color:#bbb;text-shadow:2px 2px #000}.cross{position:absolute;left:50%;top:50%;width:12px;height:12px;transform:translate(-50%,-50%);opacity:.7}.cross:before,.cross:after{content:"";position:absolute;background:#ddd}.cross:before{width:12px;height:1px;top:5px}.cross:after{height:12px;width:1px;left:5px}.watch{color:#b7aaa4}.inventory{position:absolute;right:18px;top:95px;background:rgba(4,5,6,.84);border:1px solid #3e4447;padding:10px;min-width:210px;font-size:12px}.map{position:absolute;right:18px;bottom:18px;width:190px;height:70px;border:1px solid #555;background:rgba(0,0,0,.55)}.fade{position:absolute;inset:0;background:#000;opacity:0;pointer-events:none;z-index:40}.vignette{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.72) 100%);opacity:.8}.warning{position:absolute;left:50%;top:22%;transform:translateX(-50%);font-size:22px;letter-spacing:4px;color:#c9b9b0;text-shadow:0 0 12px #000,3px 3px #000}.privacy-small{font-size:11px;color:#777;margin-top:18px}
</style>
</head>
<body>
<div class="shell">
<canvas id="game" width="1280" height="720"></canvas>
<div id="notice" class="layer notice"><div class="panel"><h1>PRIVACY & SAFETY NOTICE</h1><p>This is a fictional horror game. It does <b>not</b> access, collect, store, or reveal your real IP address, exact location, camera, microphone, files, passwords, contacts, browser history, accounts, or personal identity.</p><p>Any surveillance screens, names, locations, network messages, or similar information shown during gameplay are <b>fictional game effects</b>. <b>The Smiler is fictional and cannot actually watch you.</b></p><button id="accept">I UNDERSTAND — ENTER THE GAME</button><div class="privacy-small">You can open this notice again from the pause menu.</div></div></div>
<div id="menu" class="layer menu hidden"><div class="panel"><div class="title">ASHES OF THE DEAD</div><div class="subtitle">THE ALCATRAZ ESCAPE</div><p style="text-align:center">Choose the detective who will try to survive the night.</p><div class="name"><button data-name="Julia">JULIA</button><button data-name="May">MAY</button><button data-name="Yumi">YUMI</button></div><div class="controls">A / D or ARROWS — MOVE &nbsp; SHIFT — RUN &nbsp; SPACE / W — JUMP<br>E — INTERACT / ENTER STRUCTURES &nbsp; MOUSE — AIM / SHOOT<br>R — RELOAD &nbsp; F — FLASHLIGHT &nbsp; Q — MELEE &nbsp; G — GRENADE &nbsp; ESC — PAUSE</div></div></div>
<div id="cutscene" class="layer cutscene hidden"><div><div id="cutline" class="cutline"></div><div class="cutmeta">ENTER / SPACE — continue &nbsp; • &nbsp; ESC — skip</div></div></div>
<div id="pause" class="layer pause hidden"><div class="panel"><h1>PAUSED</h1><p id="pauseText">The rain keeps falling.</p><button id="resume">RESUME</button><button id="restart">RESTART CHAPTER</button><button id="privacy">PRIVACY NOTICE</button></div></div>
<div id="hud" class="layer hud hidden"><div class="hudtop"><div><div>HEALTH</div><div class="bar"><div id="hp" class="fill hp"></div></div><div>STAMINA</div><div class="bar"><div id="stam" class="fill stam"></div></div><div>SANITY</div><div class="bar"><div id="san" class="fill san"></div></div></div><div style="text-align:right"><div>ALCATRAZ ISLAND</div><div class="watch" id="watch">THE SMILER IS WATCHING</div><div id="ammo">AMMO 12 / 12</div></div></div><div class="objective" id="objective">OBJECTIVE</div><div class="message" id="message"></div><div class="prompt" id="prompt"></div><div class="cross"></div><div id="inventory" class="inventory hidden"></div><canvas id="map" class="map" width="380" height="140"></canvas><div class="vignette"></div><div id="warning" class="warning hidden"></div></div>
<div id="fade" class="fade"></div>
</div>
<script>
'use strict';
const C=document.getElementById('game');
const ctx=C.getContext('2d');
ctx.imageSmoothingEnabled=false;
const MAP=document.getElementById('map');
const mctx=MAP.getContext('2d');
const W=1280,H=720,G=570,WORLD=12800;
const keys=new Set();
const mouse={x:640,y:360,down:false};
let mode='notice',name='Julia',t=0,last=0,cam=0,shake=0,flash=0;
let objective='';let message='';let messageUntil=0;let prompt='';
let zombies=[],vehicles=[],buildings=[],survivors=[],loot=[],bullets=[],particles=[],rain=[],shells=[],blood=[],doors=[],interior=null;
let alcatrazEscaped=false,boatReady=false,fuel=0,alarm=0,hordeTimer=18,smilerTimer=7,smiler={active:false,x:0,ttl:0,phase:0};
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
function addBuilding(x,w,h,name,type='prison',locked=false){buildings.push({x,w,h,name,type,locked,open:false,interior:false,insideLoot:[],insideZombies:[]});}
function addVehicle(x,y,w,type,broken=false,usable=false){vehicles.push({x,y,w,h:type==='tank'?42:34,type,broken,usable,driving:false,angle:0});}
function addLoot(x,y,type,label,amount=1,inside=null){loot.push({x,y,type,label,amount,got:false,inside});}
function addSurvivor(x,name,role){survivors.push({x,y:G-62,w:32,h:62,name,role,state:'idle',talked:false,anim:rnd(0,8),hp:100,follow:false});}
function spawnZombie(x,type='walker',y=G-58,inside=null){if(zombies.filter(z=>!z.dead).length>=12)return null;let z={x,y,w:type==='brute'?58:type==='runner'?32:38,h:type==='brute'?78:60,type,hp:type==='brute'?170:type==='runner'?55:42,vx:0,vy:0,ground:true,attack:rnd(.2,1),anim:rnd(0,20),dead:false,inside,alert:0};zombies.push(z);return z;}
function buildWorld(){
 buildings=[];vehicles=[];survivors=[];loot=[];zombies=[];doors=[];
 // Alcatraz prison complex and island structures.
 addBuilding(260,280,250,'Cell Block A','prison',true);
 addBuilding(620,250,230,'Cell Block B','prison',true);
 addBuilding(970,220,190,'Guard Station','office',true);
 addBuilding(1280,310,250,'Medical Wing','medical',true);
 addBuilding(1710,260,205,'Kitchen & Cafeteria','cafeteria',true);
 addBuilding(2050,250,225,'Workshop','workshop',true);
 addBuilding(2390,300,260,'Armory','armory',true);
 addBuilding(2810,240,210,'Power Station','power',true);
 addBuilding(3230,310,235,'Dock Warehouse','warehouse',true);
 addBuilding(3720,220,180,'Barracks','barracks',true);
 addBuilding(4200,350,270,'Island Command','office',true);
 addBuilding(4900,290,210,'Quarantine Clinic','medical',true);
 addBuilding(5480,330,240,'Coast Guard House','house',true);
 addBuilding(6120,390,290,'Ruined Village House','house',true);
 addBuilding(6840,360,250,'Abandoned Hotel','hotel',true);
 addBuilding(7650,440,300,'Military Depot','military',true);
 addBuilding(8580,390,260,'Church','church',true);
 addBuilding(9510,430,310,'Hospital','hospital',true);
 addBuilding(10600,360,260,'Safehouse','safehouse',true);
 addBuilding(11600,420,280,'Research Facility','lab',true);
 // vehicles
 addVehicle(112,G-34,105,'jeep',true,false);
 addVehicle(760,G-36,145,'truck',false,true);
 addVehicle(1480,G-34,110,'car',true,false);
 addVehicle(2170,G-36,145,'truck',true,false);
 addVehicle(2560,G-42,180,'tank',true,false);
 addVehicle(3350,G-34,130,'jeep',false,true);
 addVehicle(3880,G-34,115,'car',true,false);
 addVehicle(4520,G-36,145,'truck',true,false);
 addVehicle(5630,G-34,115,'jeep',true,false);
 addVehicle(7040,G-34,125,'car',true,false);
 addVehicle(7760,G-36,160,'truck',false,true);
 addVehicle(8670,G-34,130,'jeep',true,false);
 addVehicle(9720,G-34,120,'car',true,false);
 addVehicle(10800,G-36,155,'truck',false,true);
 addVehicle(12120,G-25,220,'boat',true,false);
 // No survivors or zombies are present at the opening. The prison feels abandoned.
 // They are introduced only after the player leaves the opening cell.
 // exterior loot
 addLoot(870,G-24,'ammo','Ammunition',8); addLoot(1190,G-24,'medkit','Medical Kit'); addLoot(1540,G-24,'ammo','Ammunition',12); addLoot(2290,G-24,'fuel','Fuel Can'); addLoot(2990,G-24,'battery','Generator Battery'); addLoot(3480,G-24,'ammo','Ammunition',12); addLoot(4380,G-24,'grenade','Grenade',2); addLoot(5230,G-24,'medkit','Medical Kit'); addLoot(5800,G-24,'fuel','Fuel Can'); addLoot(7200,G-24,'ammo','Ammunition',15); addLoot(8020,G-24,'medkit','Medical Kit'); addLoot(9000,G-24,'ammo','Ammunition',20); addLoot(10040,G-24,'fuel','Fuel Can'); addLoot(11080,G-24,'medkit','Medical Kit');
 // Interior zombie pockets are created when entering structures.
 rain=[];for(let i=0;i<260;i++)rain.push({x:rnd(0,W),y:rnd(-700,H),v:rnd(330,560),len:rnd(10,22)});
}
function intro(){
 cutLines=[
 'ALCATRAZ ISLAND — 11:47 PM',
 'Rain claws at the prison windows. You wake alone inside a locked cell.',
 'The emergency lights die. For a moment, the corridor beyond the bars is completely black.',
 'A tall shape appears at the far end. Two pale eyes. One impossible smile. Then it is gone.',
 'The lock clicks. No voices. No footsteps. Just rain. ESCAPE ALCATRAZ.'
 ];cutIndex=0;cutTimer=0;mode='intro';document.getElementById('cutscene').classList.remove('hidden');showCut();}
function showCut(){const el=document.getElementById('cutline');el.textContent=cutLines[cutIndex]||'';}
function nextCut(){cutIndex++;if(cutIndex>=cutLines.length)finishIntro();else{cutTimer=0;showCut();}}
function finishIntro(){document.getElementById('cutscene').classList.add('hidden');document.getElementById('hud').classList.remove('hidden');mode='play';buildWorld();p={...p,x:180,y:G-64,hp:100,stam:100,sanity:100,ammo:12,reload:0,grenades:2,kills:0,shots:0,invuln:0,light:false};cam=0;interior='OPENING_CELL';startCell=true;cellKey=false;cellDoorOpen=false;cellInspected={bed:false,window:false,note:false};gameStarted=true;alarm=0;setObj('Search the cell. Find a way out.');setMsg('Cold concrete. Rain beyond the bars. You are alone.',4);}
function resetChapter(){document.getElementById('pause').classList.add('hidden');document.getElementById('hud').classList.remove('hidden');mode='play';buildWorld();p={x:180,y:G-64,w:34,h:64,vx:0,vy:0,ground:true,face:1,hp:100,stam:100,sanity:100,ammo:12,maxAmmo:12,reload:0,grenades:2,light:false,anim:0,kills:0,shots:0,run:false,invuln:0};cam=0;interior='OPENING_CELL';startCell=true;cellKey=false;cellDoorOpen=false;cellInspected={bed:false,window:false,note:false};alcatrazEscaped=false;boatReady=false;fuel=0;smiler.active=false;alarm=0;gameStarted=true;setObj('Search the cell. Find a way out.');setMsg('Chapter restarted.',2);}
function playerRect(){return {x:p.x,y:p.y,w:p.w,h:p.h};}
function near(a,b,d){return Math.abs(a-b)<d;}
function getBuilding(){let best=null,bd=99999;for(const b of buildings){const d=Math.abs((b.x+b.w/2)-p.x);if(d<bd&&d<b.w/2+65){best=b;bd=d;}}return best;}
function getVehicle(){let best=null,bd=99999;for(const v of vehicles){const d=Math.abs(v.x+v.w/2-p.x);if(d<bd&&d<100){best=v;bd=d;}}return best;}
function getSurvivor(){let best=null,bd=99999;for(const s of survivors){const d=Math.abs(s.x-p.x);if(d<bd&&d<90){best=s;bd=d;}}return best;}
function getLoot(){let best=null,bd=99999;for(const l of loot){if(l.got||l.inside&&l.inside!==interior)continue;const d=Math.abs(l.x-p.x);if(d<bd&&d<65){best=l;bd=d;}}return best;}
function interact(){
 if(mode!=='play')return;
 if(startCell){
  const cx=p.x;
  if(!cellInspected.bed && cx<300){cellInspected.bed=true;setMsg('An empty mattress. Someone left in a hurry.',3);return;}
  if(!cellInspected.note && cx>=300&&cx<520){cellInspected.note=true;cellKey=true;setMsg('You find a small brass key hidden beneath a loose note.',3);setObj('Unlock the cell door.');return;}
  if(!cellInspected.window && cx>=520&&cx<700){cellInspected.window=true;p.sanity=clamp(p.sanity-3,0,100);setMsg('A black ocean. San Francisco lights are barely visible.',3);return;}
  if(cellKey && cx>=900){startCell=false;cellDoorOpen=true;interior=null;p.x=315;setObj('Leave the cell block. Find the prison exit.');setMsg('The cell door opens. The corridor is empty.',3);alarm=.15;spawnFirstThreats();return;}
  setMsg(cellKey?'Move to the cell door and press E.':'Search the bed, note, and window.',2);return;
 }
 const l=getLoot();if(l){l.got=true;if(l.type==='medkit'){p.hp=clamp(p.hp+40,0,100);setMsg('Medical supplies restored health.',2);}else if(l.type==='ammo'){p.ammo=clamp(p.ammo+l.amount,0,p.maxAmmo);setMsg('Ammunition collected.',2);}else if(l.type==='grenade'){p.grenades+=l.amount;setMsg('Grenades collected.',2);}else if(l.type==='fuel'){fuel++;setMsg('Fuel can collected. '+fuel+'/2 fuel.',2);}else if(l.type==='battery'){setMsg('Generator battery collected.',2);}return;}
 const s=getSurvivor();if(s){s.talked=true;s.follow=true;p.sanity=clamp(p.sanity+8,0,100);setMsg(s.name+': “Stay close. The Smiler is watching.”',4);setObj('Help the survivors reach the dock.');return;}
 const v=getVehicle();if(v){if(v.broken){if(fuel>0){fuel--;v.broken=false;v.usable=true;setMsg('Vehicle repaired with fuel.',3);}else setMsg('This vehicle needs fuel.',2);return;}if(v.usable){p.x=v.x+v.w/2;setMsg('Vehicle ready. Press E to drive / leave.',2);setObj('Reach the dock.');return;}}
 const b=getBuilding();if(b){if(!b.open){b.open=true;interior=b.name;enterBuilding(b);return;}b.open=false;interior=null;setMsg('Exited '+b.name+'.',2);setObj('Search the island and find a route to the dock.');return;}
 if(p.x>11650&&fuel>=2){boatReady=true;setMsg('The boat is fueled. Escape Alcatraz!',3);setObj('Reach the escape boat.');}
}
function spawnFirstThreats(){
 const spots=[560,760,1080,1420,1880,2240,2780,3300];
 for(let i=0;i<spots.length;i++){const type=i===2||i===6?'runner':'walker';spawnZombie(spots[i],type);}
 addSurvivor(1190,'Eli','former guard');
 addSurvivor(1900,'Mara','nurse');
 setObj('Reach the prison exit. Stay alert.');
}
function enterBuilding(b){
 setObj('Search '+b.name+' for supplies and survivors.');setMsg('Entered '+b.name+'. The outside world is quiet.',2);
 for(let i=0;i<Math.min(2+(b.w>320?1:0),3);i++){const z=spawnZombie(b.x+60+rnd(0,b.w-120),'walker',G-58,b.name);if(z)z.x=b.x+60+rnd(0,b.w-120);}
 const types=['ammo','medkit','ammo','grenade'];for(let i=0;i<types.length;i++)addLoot(b.x+70+i*55,G-24,types[i],types[i].toUpperCase(),types[i]==='grenade'?1:types[i]==='ammo'?6:1,b.name);
}
function movePlayer(dt){
 const left=keys.has('a')||keys.has('ArrowLeft'),right=keys.has('d')||keys.has('ArrowRight');
 if(startCell){p.vx=(right-left)*125;p.x+=p.vx*dt;p.x=clamp(p.x,70,1120);p.anim+=dt*5;return;}
 p.run=keys.has('Shift')&&p.stam>2;
 let speed=p.run?310:185;
 if(p.run&&(left||right))p.stam=clamp(p.stam-dt*20,0,100);else p.stam=clamp(p.stam+dt*12,0,100);
 p.vx=(right-left)*speed;if(p.vx)p.face=Math.sign(p.vx);
 if((keys.has(' ')||keys.has('w')||keys.has('ArrowUp'))&&p.ground){p.vy=-445;p.ground=false;for(let i=0;i<5;i++)spawnParticle(p.x+17,G,'#777',.35,2,rnd(-30,30),rnd(-40,0));}
 p.vy+=1120*dt;p.x+=p.vx*dt;p.y+=p.vy*dt;
 if(p.y+p.h>=G){p.y=G-p.h;p.vy=0;p.ground=true;}
 p.x=clamp(p.x,0,WORLD-p.w);
 const target=p.x-390;cam+=(target-cam)*Math.min(1,dt*7);cam=clamp(cam,0,WORLD-W);
 p.anim+=dt*(p.run?14:8);
}
function updateZombies(dt){
 for(const z of zombies){if(z.dead)continue;
  if(z.inside&&z.inside!==interior)continue;
  const dx=p.x-z.x,dist=Math.abs(dx);
  const hearing=135+(p.run?120:0)+(gunshotTimer>0?280:0);
  if(dist<hearing){z.alert=2;z.vx=Math.sign(dx)*(z.type==='runner'?125:z.type==='brute'?48:72);z.x+=z.vx*dt;}
  else z.x+=Math.sin(t*.8+z.anim)*8*dt;
  if(dist<48){z.attack-=dt;if(z.attack<=0&&p.invuln<=0){const dmg=z.type==='brute'?16:z.type==='runner'?10:7;p.hp-=dmg;p.invuln=.55;shake=6;spawnBlood(p.x+17,p.y+30);setMsg('A zombie grabbed you.',1.2);}}
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
function updateSurvivors(dt){for(const s of survivors){if(s.follow){s.x+=(p.x-75-s.x)*dt*.35;if(Math.abs(s.x-p.x)>260)s.x=p.x-90;}}}
function updateVehicles(dt){for(const v of vehicles){if(v.driving){v.x+=p.face*170*dt;}}}
function updateParticles(dt){for(const q of particles){q.x+=q.vx*dt;q.y+=q.vy*dt;q.vy+=80*dt;q.life-=dt;}particles=particles.filter(q=>q.life>0);}
function updateRain(dt){for(const r of rain){r.y+=r.v*dt;if(r.y>H+30){r.y=-30;r.x=rnd(0,W);}}}
function triggerHorde(){
 if(startCell||zombies.filter(z=>!z.dead).length>=12)return;if(t<hordeTimer)return;hordeTimer=t+40+rnd(10,20);const base=clamp(p.x-600,50,WORLD-600);const count=Math.min(4,12-zombies.filter(z=>!z.dead).length);for(let i=0;i<count;i++){const r=Math.random();spawnZombie(base+i*75+rnd(-40,40),r<.15?'runner':'walker');}setMsg('More movement in the dark...',3);alarm=.35;}
function triggerSmiler(){
 if(smiler.active)return;
 smiler.active=true;smiler.ttl=3.8+Math.random()*3;smiler.phase=0;const side=Math.random()<.5?-1:1;smiler.x=clamp(p.x+side*rnd(300,520),80,WORLD-80);p.sanity=clamp(p.sanity-8,0,100);setMsg('THE SMILER IS WATCHING.',2.5);
}
function updateSmiler(dt){
 smilerTimer-=dt;if(smilerTimer<=0){smilerTimer=10+Math.random()*15;if(Math.random()<.7)triggerSmiler();}
 if(smiler.active){smiler.ttl-=dt;smiler.phase+=dt;if(smiler.ttl<=0)smiler.active=false;}
 // Persistent observation: sanity drains subtly when the player is close to its sight line.
 if(smiler.active&&Math.abs(smiler.x-p.x)<650)p.sanity=clamp(p.sanity-dt*1.8,0,100);
}
function updateSanity(dt){
 const darkness=(p.light?0:1);p.sanity=clamp(p.sanity-dt*(.15+darkness*.22),0,100);
 if(p.sanity<25&&Math.random()<dt*.7){setMsg('You hear breathing behind you.',1.5);}
}
function updateObjective(){
 if(!alcatrazEscaped&&p.x>3850){alcatrazEscaped=true;setObj('The mainland route is blocked. Reach the dock and find a boat.');setMsg('You made it through the prison complex.',4);}
 if(alcatrazEscaped&&p.x>11300&&fuel<2)setObj('Find 2 fuel cans and reach the escape boat.');
 if(alcatrazEscaped&&p.x>11300&&fuel>=2&&!boatReady)setObj('Fuel the escape boat with E.');
 if(boatReady&&p.x>11900){setMsg('YOU ESCAPED ALCATRAZ.',8);setObj('Chapter complete — San Francisco awaits.');}
}
function update(dt){
 if(mode!=='play')return;
 t+=dt;p.invuln=Math.max(0,p.invuln-dt);
 movePlayer(dt);updateZombies(dt);updateBullets(dt);updateSurvivors(dt);updateVehicles(dt);updateParticles(dt);updateRain(dt);triggerHorde();updateSmiler(dt);updateSanity(dt);updateObjective();
 if(p.reload>0)p.reload-=dt;
 if(p.hp<=0){p.hp=100;p.sanity=55;p.x=Math.max(80,p.x-250);setMsg('You collapsed. You wake up again in the rain.',4);shake=10;}
 if(keys.has('r')&&p.reload<=0&&p.ammo<p.maxAmmo)p.reload=1.0;
 if(p.reload<=0&&p.ammo===0){p.reload=.9;}
 document.getElementById('hp').style.width=p.hp+'%';document.getElementById('stam').style.width=p.stam+'%';document.getElementById('san').style.width=p.sanity+'%';document.getElementById('ammo').textContent='AMMO '+p.ammo+' / '+p.maxAmmo+(p.reload>0?' — RELOADING':'');document.getElementById('watch').textContent=smiler.active?'THE SMILER IS WATCHING YOU':'THE SMILER IS ALWAYS WATCHING';
 const l=getLoot(),b=getBuilding(),s=getSurvivor(),v=getVehicle();let pr='';
 if(startCell){if(!cellInspected.bed&&p.x<300)pr='E — SEARCH BED';else if(!cellInspected.note&&p.x>=300&&p.x<520)pr='E — INSPECT LOOSE NOTE';else if(!cellInspected.window&&p.x>=520&&p.x<700)pr='E — LOOK OUT WINDOW';else if(cellKey&&p.x>=900)pr='E — UNLOCK CELL DOOR';else pr='A / D — MOVE   •   F — FLASHLIGHT';}
 else {if(l)pr='E — TAKE '+l.label;if(s)pr='E — TALK TO '+s.name;if(b)pr='E — ENTER / EXIT '+b.name;if(v)pr='E — INTERACT WITH '+v.type.toUpperCase();}
 document.getElementById('prompt').textContent=pr;
 document.getElementById('message').textContent=t<messageUntil?message:'';
 updateMap();
}
function drawSky(){
 const g=ctx.createLinearGradient(0,0,0,G);g.addColorStop(0,COLORS.sky);g.addColorStop(1,COLORS.sky2);ctx.fillStyle=g;ctx.fillRect(0,0,W,G);
 // distant San Francisco silhouette
 for(let i=0;i<18;i++){let x=i*110-(cam*.12%110);let h=70+(i*37%100);rect(x,G-115-h,70,h,'#10171c');rect(x+12,G-100-h,9,10,'#252b2d');rect(x+40,G-82-h,8,9,'#252b2d');}
 // moon behind clouds
 ctx.globalAlpha=.18;ctx.fillStyle='#c2c3b6';ctx.beginPath();ctx.arc(1040,100,42,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
}
function drawGround(){rect(0,G,W,H-G,COLORS.ground);for(let x=-(cam%80);x<W;x+=80){rect(x,G+7,48,2,'#3d4041');rect(x+55,G+38,14,2,'#1d2021');}rect(0,G,W,8,'#55575a');}
function drawBuilding(b){const x=b.x-cam;if(x+b.w<0||x>W)return;const top=G-b.h;const dark=b.open?'#32383a':'#292e31';rect(x,top,b.w,b.h,dark);rect(x+8,top+8,b.w-16,9,'#4d5354');
 for(let yy=top+34;yy<G-45;yy+=42){for(let xx=x+22;xx<x+b.w-20;xx+=47){rect(xx,yy,20,24,'#111619');if(((xx+yy+Math.floor(t*4))%11)<2)rect(xx+5,yy+5,8,8,'#6b6c57');}}
 const doorX=x+b.w/2-25;rect(doorX,G-78,50,78,b.open?'#59665d':'#15191b');if(b.open){rect(doorX+20,G-50,3,3,'#b9b28d');}else{rect(doorX+18,G-43,13,13,'#2c3031');}
 textLabel(b.name,x+b.w/2,top-8);drawBuildingDetails(b,x,top);
}
function textLabel(s,x,y){txt(s,x,y,11,'#7f8587','center');}
function drawBuildingDetails(b,x,top){if(b.type==='prison'){for(let i=0;i<6;i++)line(x+20+i*35,top+22,x+20+i*35,G-20,'#4d5354',2);}if(b.type==='medical'){rect(x+20,top+50,50,35,'#6d7370');rect(x+40,top+35,10,65,'#8a8d83');}if(b.type==='power'){for(let i=0;i<3;i++){rect(x+25+i*42,G-130,25,75,'#404648');rect(x+32+i*42,G-122,11,11,'#77725c');}}if(b.type==='church'){rect(x+b.w/2-8,top-38,16,45,'#3d4243');rect(x+b.w/2-24,top-20,48,9,'#3d4243');}}
function drawVehicle(v){const x=v.x-cam,y=v.y; if(x+v.w<0||x>W)return; if(v.type==='boat'){rect(x,y+10,v.w,20,'#353c40');rect(x+18,y-2,55,15,'#596062');rect(x+35,y-12,4,12,'#777');line(x+37,y-12,x+65,y-25,'#777',2);return;}const body=v.broken?'#343738':'#4a554f';rect(x,y,v.w,v.h,body);rect(x+10,y-18,v.w-20,21,v.type==='tank'?'#353a39':'#3d4744');if(v.type==='tank'){rect(x+v.w-20,y-43,15,32,'#454b48');rect(x+v.w-5,y-38,58,7,'#555957');}else{rect(x+18,y-8,25,10,'#202426');rect(x+v.w-43,y-8,25,10,'#202426');}ctx.fillStyle='#111';if(v.type!=='tank'){ctx.beginPath();ctx.arc(x+20,y+v.h,14,0,Math.PI*2);ctx.arc(x+v.w-20,y+v.h,14,0,Math.PI*2);ctx.fill();}if(v.broken){txt('WRECK',x+v.w/2,y-26,10,'#777','center');for(let i=0;i<3;i++)line(x+rnd(5,v.w-5),y-rnd(20,50),x+rnd(5,v.w-5),y-rnd(25,60),'#555',1);}else txt('E',x+v.w/2,y-27,11,'#aaa','center');}
function drawLoot(l){if(l.got)return;const x=l.x-cam;if(x<-30||x>W+30)return;let c=l.type==='key'?'#c3aa54':l.type==='medkit'?'#a6534e':l.type==='ammo'?'#777f78':l.type==='fuel'?'#75684d':l.type==='grenade'?'#4d5a4d':'#7c7b68';rect(x-9,l.y-12,18,18,c);rect(x-5,l.y-8,10,10,'#202426');txt(l.type==='key'?'K':l.type==='medkit'?'+':l.type==='ammo'?'A':l.type==='fuel'?'F':l.type==='grenade'?'G':'B',x,l.y+1,11,'#ddd','center');}
function drawSurvivor(s){const x=s.x-cam,bob=Math.sin(t*7+s.anim)*2;rect(x+9,s.y-42+bob,16,18,COLORS.skin);rect(x+5,s.y-25+bob,24,34,s.role==='soldier'?'#4d574b':'#51575a');rect(x,s.y+7+bob,9,25,'#252a2d');rect(x+24,s.y+7+bob,9,25,'#252a2d');line(x+5,s.y-8+bob,x-7,s.y+10+bob,'#3e4548',5);line(x+29,s.y-8+bob,x+41,s.y+10+bob,'#3e4548',5);txt(s.name,x+17,s.y-52,11,'#ddd','center');if(near(s.x,p.x,90))txt('E TALK',x+17,s.y-65,10,'#fff','center');}
function drawPlayer(){const x=p.x-cam,bob=p.ground?Math.sin(p.anim)*1.5:0;const walk=Math.sin(p.anim)*3;rect(x+7,p.y+2+bob,21,25,COLORS.skin);rect(x+5,p.y+26+bob,25,37,name==='May'?'#4b5560':name==='Yumi'?'#55505e':'#4b5550');rect(x,p.y+39+bob,9,25,'#202529');rect(x+25,p.y+39+bob,9,25,'#202529');line(x+8,p.y+34+bob,x+(p.face>0?40:-8),p.y+28+bob,'#303438',6);const gx=p.face>0?x+34:x-17;rect(gx,p.y+27,28,6,'#202224');if(p.reload>0)txt('RELOADING',x+17,p.y-15,10,'#aaa','center');}
function drawZombie(z){const x=z.x-cam,bob=Math.sin(t*8+z.anim)*3;const c=z.type==='brute'?'#303936':z.type==='runner'?'#46574b':'#39483f';const skin=z.type==='brute'?'#4c5750':'#536055';rect(x+7,z.y-38+bob,24,z.type==='brute'?34:27,skin);rect(x,z.y-10+bob,z.w,z.h-25,c);line(x+4,z.y+8+bob,x-12,z.y+32+bob,c,7);line(x+z.w-4,z.y+8+bob,x+z.w+12,z.y+32+bob,c,7);rect(x+4,z.y+z.h-13,13,20,'#242a27');rect(x+z.w-17,z.y+z.h-13,13,20,'#242a27');rect(x+13,z.y-29+bob,4,4,'#c6c19b');rect(x+26,z.y-29+bob,4,4,'#c6c19b');if(z.type==='runner'){line(x+5,z.y+10,x-16,z.y-3,'#536055',6);}}
function drawSmiler(){if(!smiler.active)return;const x=smiler.x-cam;if(x<-100||x>W+100)return;const base=G-260;ctx.save();ctx.globalAlpha=.92; // tall silhouette
 rect(x-25,base,50,260,'#050607');rect(x-15,base-80,30,82,'#030405');rect(x-39,base+5,14,190,'#040506');rect(x+25,base+5,14,190,'#040506');rect(x-16,base+230,14,42,'#030405');rect(x+2,base+230,14,42,'#030405');
 // long neck and impossible head
 rect(x-12,base-36,24,35,'#030405');ctx.strokeStyle='#d7d1c3';ctx.lineWidth=3;ctx.beginPath();ctx.arc(x,base-58,18,0,Math.PI*2);ctx.stroke();rect(x-9,base-62,5,5,'#e4e0cf');rect(x+4,base-62,5,5,'#e4e0cf');ctx.strokeStyle='#eee7d7';ctx.lineWidth=4;ctx.beginPath();ctx.arc(x,base-56,13,.18,2.96);ctx.stroke();ctx.globalAlpha=.18+.1*Math.sin(smiler.phase*8);rect(x-55,base-100,110,360,'#000');ctx.restore();}
function drawParticles(){for(const q of particles)rect(q.x-cam,q.y,q.size,q.size,q.c);}
function drawRain(){ctx.globalAlpha=.34;for(const r of rain){const x=r.x,y=r.y;line(x,y,x-7,y+r.len,'#687985',1);}ctx.globalAlpha=1;}
function drawOpeningCell(){
 // Claustrophobic first-person-ish side-view cell. No zombies, no survivors.
 ctx.fillStyle='#050608';ctx.fillRect(0,0,W,H);
 // concrete walls
 rect(0,0,W,185,'#111416');rect(0,185,W,8,'#272b2b');rect(0,193,W,G-193,'#151819');
 // rear wall blocks
 for(let x=0;x<W;x+=82){line(x,193,x,570,'#202426',2);}
 for(let y=250;y<570;y+=70){line(0,y,W,y,'#101314',1);}
 // floor
 rect(0,G,W,H-G,'#0d1011');
 for(let x=0;x<W;x+=65)line(x,G,x+40,H,'#181b1c',1);
 // bars / cell front
 for(let x=520;x<=1010;x+=34){rect(x,130,8,440,'#363b3b');rect(x+3,130,3,440,'#555958');}
 rect(515,130,510,8,'#414646');
 // corridor beyond bars
 rect(1030,195,250,375,'#020304');
 for(let y=230;y<550;y+=55)line(1040,y,1270,y,'#090b0c',1);
 // mattress / bed
 rect(100,470,210,28,'#303232');rect(118,445,160,30,'#242829');rect(118,440,160,7,'#55504a');
 // tiny toilet
 rect(345,463,58,68,'#313536');rect(355,445,42,25,'#404545');rect(350,438,50,10,'#555958');
 // wall note
 if(!cellInspected.note){rect(250,300,22,32,'#c4b78e');txt('?',261,324,16,'#2b2921','center');}
 // window
 rect(50,230,110,115,'#080c10');rect(55,235,100,105,'#0d1820');line(105,235,105,340,'#353c40',3);line(55,287,155,287,'#353c40',3);
 // rain outside window
 for(let i=0;i<18;i++){const rx=58+(i*19)%94,ry=242+(i*29)%90;line(rx,ry,rx-7,ry+15,'#465661',1);}
 // ceiling lamp, flickering
 const flick=(Math.sin(t*9)+Math.sin(t*21)>.6)?1:.35;rect(510,72,260,7,'#414545');rect(630,79,18,22,'#77786d');ctx.globalAlpha=flick*.32;ctx.fillStyle='#b7b39a';ctx.fillRect(520,92,240,90);ctx.globalAlpha=1;
 // door
 rect(1045,280,125,290,'#292d2e');rect(1053,288,109,282,'#202426');rect(1145,425,7,7,'#a7a18a');
 // player
 drawPlayer();
 // darkness / flashlight cone
 const px=p.x-cam+17,py=p.y+30;
 const g=ctx.createRadialGradient(px,py,10,px,py,380);g.addColorStop(0,p.light?'rgba(215,215,190,.22)':'rgba(0,0,0,0)');g.addColorStop(.5,p.light?'rgba(180,180,165,.06)':'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.72)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 // heavy darkness around edges
 ctx.fillStyle='rgba(0,0,0,.42)';ctx.fillRect(0,0,W,720);
 if(p.light){ctx.globalCompositeOperation='destination-out';const hole=ctx.createRadialGradient(px,py,40,px,py,270);hole.addColorStop(0,'rgba(0,0,0,.55)');hole.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=hole;ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='source-over';}
 txt('CELL A-17',38,42,12,'#666b69');if(startCell&&!cellKey)txt('SEARCH THE CELL',640,650,13,'#7e817b','center');
}
function drawWorld(){
 if(startCell){drawOpeningCell();return;}
 drawSky();drawGround();
 for(const b of buildings)drawBuilding(b);
 for(const v of vehicles)drawVehicle(v);
 for(const l of loot)drawLoot(l);
 for(const s of survivors)drawSurvivor(s);
 for(const z of zombies)if(!z.dead)drawZombie(z);
 for(const b of bullets)rect(b.x-cam,b.y,7,3,'#eee');
 drawPlayer();drawParticles();drawRain();drawSmiler();
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
function render(){ctx.save();if(shake>0){ctx.translate(rnd(-shake,shake),rnd(-shake,shake));shake*=.86;}if(mode==='intro'){drawIntroVisual();}else{drawWorld();}ctx.restore();if(flash>0){ctx.fillStyle='rgba(255,255,255,'+flash+')';ctx.fillRect(0,0,W,H);flash=Math.max(0,flash-.04);}}
function loop(ts){const dt=Math.min(.033,(ts-last)/1000||0);last=ts;if(mode==='intro'){cutTimer+=dt;if(cutTimer>2.2){cutTimer=0;nextCut();}}update(dt);render();requestAnimationFrame(loop);}
function showNotice(){document.getElementById('pause').classList.add('hidden');document.getElementById('menu').classList.add('hidden');document.getElementById('notice').classList.remove('hidden');mode='notice';setTimeout(()=>document.getElementById('accept').focus(),0);}
function enterGameFromNotice(){document.getElementById('notice').classList.add('hidden');document.getElementById('menu').classList.remove('hidden');mode='menu';setTimeout(()=>{const first=document.querySelector('[data-name=\"Julia\"]');if(first)first.focus();},0);}
function startGame(n){name=n;document.getElementById('menu').classList.add('hidden');intro();}
function pauseGame(){if(mode!=='play')return;mode='pause';document.getElementById('pause').classList.remove('hidden');}
function resumeGame(){mode='play';document.getElementById('pause').classList.add('hidden');}
document.getElementById('accept').onclick=enterGameFromNotice;
document.querySelectorAll('[data-name]').forEach(b=>b.onclick=()=>startGame(b.dataset.name));
document.getElementById('resume').onclick=resumeGame;
document.getElementById('restart').onclick=()=>{document.getElementById('pause').classList.add('hidden');resetChapter();};
document.getElementById('privacy').onclick=showNotice;
window.addEventListener('keydown',e=>{
 let k=e.key;if(mode==='notice'&&(k==='Enter'||k===' ')){e.preventDefault();enterGameFromNotice();return;}if(mode==='menu'&&(k==='Enter'||k===' ')){e.preventDefault();const first=document.querySelector('[data-name=\"Julia\"]');if(first)first.click();return;}if(mode==='intro'&&(k==='Enter'||k===' ')){e.preventDefault();nextCut();return;}if(k==='Escape'&&mode==='intro'){finishIntro();return;}if(k==='Escape'&&mode==='play'){pauseGame();return;}if(k==='Escape'&&mode==='pause'){resumeGame();return;}
 if(mode==='play'){keys.add(k.length===1?k.toLowerCase():k);if(k.toLowerCase()==='e')interact();if(k.toLowerCase()==='q'){for(const z of zombies)if(!z.dead&&Math.abs(z.x-p.x)<80){z.hp-=55;spawnBlood(z.x,z.y+25);setMsg('MELEE HIT',.6);}}if(k.toLowerCase()==='f'){p.light=!p.light;setMsg(p.light?'Flashlight on.':'Flashlight off.',1);}if(k.toLowerCase()==='g'&&p.grenades>0){p.grenades--;for(const z of zombies)if(!z.dead&&Math.abs(z.x-p.x)<250)z.hp-=100;flash=.22;shake=10;setMsg('GRENADE!',1.5);}}
});
window.addEventListener('keyup',e=>keys.delete(e.key.length===1?e.key.toLowerCase():e.key));
C.addEventListener('mousemove',e=>{const r=C.getBoundingClientRect();mouse.x=(e.clientX-r.left)*C.width/r.width;mouse.y=(e.clientY-r.top)*C.height/r.height;});
C.addEventListener('mousedown',e=>{if(e.button===0){mouse.down=true;shoot();}});window.addEventListener('mouseup',()=>mouse.down=false);setInterval(()=>{if(mouse.down&&mode==='play')shoot();},110);
// Initial title frame.
ctx.fillStyle='#030405';ctx.fillRect(0,0,W,H);txt('ASHES OF THE DEAD',W/2,325,42,'#ddd','center');txt('THE SMILER IS ALWAYS WATCHING',W/2,365,15,'#8b7f7b','center');
requestAnimationFrame(loop);
</script>
</body>
</html>"""

@app.get("/")
def index():
    return Response(GAME_HTML, mimetype="text/html")

@app.get("/health")
def health():
    return {"status":"ok","game":"Ashes of the Dead","chapter":"Alcatraz Escape"}


# ============================================================================
# ASHES OF THE DEAD — DESIGN / CONTENT REFERENCE
# ============================================================================
# The browser game above intentionally remains self-contained: Flask serves a
# single HTML document containing the Canvas renderer and gameplay systems.
# No Pygame, camera, microphone, geolocation, IP lookup, or external API is
# required. The privacy notice is part of the actual game UI.
#
# STORY PRINCIPLES
# 1. The game begins at Alcatraz, not in a generic open world.
# 2. The player escapes the prison before the wider island opens up.
# 3. The Smiler is a tall, dark, frightening creature that watches rather than
#    behaving like an ordinary zombie.
# 4. The player can encounter survivors and enter structures.
# 5. Vehicles are part of the world rather than background-only decorations.
# 6. The first launch includes a privacy disclaimer.
# 7. Surveillance-style horror text is fictional and never uses personal data.
# 8. Pixel art is intentionally rendered with imageSmoothingEnabled=false.
# 9. The game is designed to run in a browser on Render through Flask/Gunicorn.
# 10. The game does not require a native display server.
#
# NOTE FOR FUTURE ART PASSES
# The renderer uses procedural pixel primitives now. A later asset pass can
# replace individual drawing functions with sprite sheets without changing
# the gameplay state model. Recommended sprite sheets include:
#   Julia/May/Yumi idle, walk, run, jump, shoot, reload, hurt, death
#   Walker idle/walk/attack/hurt/death
#   Runner idle/run/attack/death
#   Brute idle/walk/attack/hurt/death
#   Smiler standing/watch/disappear/close-up
#   Jeep/truck/tank/boat damaged and repaired states
#   Prison doors, ladders, lockers, beds, desks, medical props, generators
#   Rain, muzzle flash, shell casings, smoke, sparks, blood particles
## CONTENT SLOT 0001: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0002: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0003: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0004: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0005: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0006: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0007: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0008: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0009: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0010: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0011: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0012: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0013: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0014: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0015: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0016: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0017: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0018: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0019: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0020: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0021: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0022: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0023: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0024: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0025: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0026: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0027: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0028: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0029: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0030: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0031: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0032: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0033: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0034: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0035: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0036: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0037: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0038: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0039: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0040: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0041: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0042: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0043: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0044: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0045: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0046: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0047: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0048: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0049: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0050: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0051: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0052: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0053: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0054: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0055: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0056: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0057: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0058: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0059: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0060: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0061: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0062: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0063: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0064: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0065: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0066: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0067: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0068: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0069: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0070: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0071: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0072: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0073: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0074: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0075: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0076: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0077: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0078: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0079: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0080: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0081: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0082: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0083: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0084: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0085: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0086: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0087: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0088: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0089: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0090: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0091: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0092: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0093: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0094: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0095: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0096: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0097: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0098: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0099: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0100: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0101: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0102: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0103: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0104: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0105: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0106: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0107: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0108: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0109: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0110: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0111: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0112: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0113: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0114: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0115: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0116: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0117: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0118: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0119: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0120: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0121: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0122: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0123: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0124: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0125: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0126: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0127: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0128: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0129: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0130: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0131: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0132: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0133: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0134: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0135: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0136: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0137: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0138: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0139: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0140: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0141: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0142: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0143: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0144: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0145: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0146: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0147: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0148: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0149: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0150: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0151: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0152: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0153: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0154: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0155: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0156: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0157: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0158: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0159: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0160: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0161: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0162: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0163: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0164: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0165: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0166: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0167: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0168: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0169: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0170: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0171: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0172: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0173: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0174: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0175: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0176: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0177: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0178: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0179: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0180: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0181: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0182: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0183: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0184: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0185: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0186: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0187: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0188: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0189: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0190: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0191: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0192: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0193: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0194: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0195: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0196: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0197: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0198: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0199: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0200: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0201: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0202: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0203: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0204: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0205: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0206: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0207: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0208: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0209: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0210: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0211: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0212: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0213: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0214: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0215: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0216: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0217: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0218: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0219: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0220: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0221: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0222: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0223: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0224: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0225: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0226: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0227: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0228: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0229: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0230: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0231: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0232: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0233: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0234: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0235: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0236: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0237: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0238: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0239: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0240: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0241: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0242: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0243: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0244: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0245: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0246: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0247: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0248: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0249: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0250: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0251: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0252: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0253: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0254: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0255: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0256: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0257: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0258: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0259: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0260: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0261: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0262: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0263: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0264: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0265: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0266: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0267: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0268: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0269: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0270: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0271: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0272: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0273: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0274: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0275: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0276: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0277: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0278: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0279: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0280: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0281: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0282: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0283: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0284: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0285: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0286: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0287: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0288: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0289: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0290: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0291: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0292: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0293: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0294: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0295: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0296: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0297: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0298: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0299: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0300: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0301: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0302: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0303: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0304: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0305: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0306: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0307: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0308: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0309: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0310: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0311: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0312: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0313: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0314: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0315: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0316: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0317: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0318: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0319: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0320: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0321: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0322: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0323: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0324: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0325: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0326: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0327: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0328: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0329: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0330: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0331: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0332: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0333: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0334: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0335: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0336: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0337: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0338: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0339: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0340: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0341: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0342: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0343: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0344: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0345: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0346: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0347: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0348: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0349: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0350: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0351: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0352: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0353: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0354: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0355: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0356: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0357: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0358: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0359: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0360: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0361: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0362: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0363: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0364: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0365: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0366: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0367: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0368: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0369: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0370: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0371: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0372: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0373: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0374: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0375: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0376: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0377: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0378: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0379: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0380: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0381: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0382: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0383: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0384: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0385: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0386: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0387: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0388: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0389: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0390: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0391: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0392: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0393: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0394: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0395: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0396: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0397: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0398: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0399: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0400: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0401: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0402: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0403: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0404: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0405: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0406: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0407: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0408: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0409: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0410: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0411: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0412: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0413: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0414: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0415: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0416: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0417: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0418: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0419: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0420: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0421: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0422: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0423: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0424: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0425: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0426: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0427: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0428: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0429: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0430: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0431: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0432: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0433: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0434: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0435: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0436: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0437: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0438: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0439: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0440: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0441: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0442: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0443: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0444: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0445: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0446: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0447: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0448: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0449: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0450: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0451: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0452: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0453: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0454: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0455: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0456: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0457: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0458: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0459: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0460: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0461: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0462: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0463: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0464: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0465: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0466: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0467: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0468: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0469: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0470: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0471: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0472: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0473: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0474: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0475: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0476: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0477: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0478: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0479: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0480: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0481: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0482: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0483: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0484: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0485: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0486: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0487: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0488: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0489: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0490: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0491: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0492: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0493: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0494: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0495: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0496: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0497: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0498: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0499: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0500: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0501: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0502: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0503: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0504: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0505: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0506: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0507: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0508: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0509: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0510: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0511: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0512: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0513: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0514: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0515: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0516: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0517: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0518: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0519: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0520: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0521: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0522: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0523: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0524: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0525: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0526: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0527: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0528: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0529: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0530: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0531: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0532: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0533: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0534: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0535: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0536: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0537: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0538: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0539: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0540: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0541: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0542: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0543: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0544: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0545: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0546: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0547: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0548: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0549: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0550: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0551: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0552: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0553: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0554: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0555: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0556: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0557: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0558: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0559: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0560: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0561: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0562: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0563: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0564: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0565: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0566: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0567: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0568: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0569: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0570: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0571: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0572: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0573: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0574: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0575: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0576: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0577: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0578: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0579: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0580: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0581: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0582: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0583: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0584: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0585: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0586: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0587: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0588: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0589: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0590: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0591: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0592: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0593: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0594: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0595: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0596: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0597: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0598: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0599: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0600: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0601: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0602: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0603: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0604: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0605: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0606: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0607: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0608: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0609: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0610: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0611: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0612: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0613: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0614: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0615: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0616: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0617: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0618: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0619: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0620: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0621: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0622: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0623: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0624: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0625: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0626: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0627: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0628: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0629: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0630: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0631: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0632: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0633: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0634: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0635: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0636: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0637: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0638: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0639: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0640: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0641: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0642: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0643: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0644: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0645: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0646: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0647: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0648: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0649: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0650: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0651: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0652: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0653: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0654: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0655: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0656: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0657: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0658: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0659: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0660: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0661: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0662: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0663: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0664: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0665: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0666: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0667: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0668: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0669: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0670: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0671: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0672: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0673: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0674: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0675: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0676: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0677: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0678: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0679: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0680: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0681: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0682: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0683: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0684: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0685: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0686: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0687: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0688: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0689: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0690: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0691: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0692: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0693: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0694: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0695: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0696: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0697: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0698: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0699: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0700: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0701: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0702: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0703: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0704: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0705: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0706: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0707: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0708: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0709: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0710: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0711: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0712: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0713: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0714: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0715: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0716: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0717: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0718: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0719: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0720: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0721: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0722: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0723: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0724: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0725: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0726: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0727: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0728: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0729: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0730: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0731: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0732: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0733: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0734: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0735: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0736: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0737: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0738: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0739: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0740: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0741: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0742: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0743: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0744: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0745: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0746: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0747: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0748: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0749: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0750: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0751: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0752: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0753: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0754: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0755: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0756: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0757: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0758: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0759: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0760: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0761: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0762: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0763: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0764: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0765: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0766: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0767: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0768: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0769: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0770: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0771: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0772: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0773: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0774: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0775: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0776: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0777: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0778: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0779: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0780: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0781: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0782: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0783: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0784: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0785: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0786: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0787: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0788: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0789: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0790: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0791: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0792: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0793: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0794: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0795: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0796: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0797: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0798: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0799: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0800: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0801: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0802: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0803: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0804: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0805: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0806: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0807: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0808: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0809: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0810: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0811: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0812: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0813: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0814: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0815: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0816: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0817: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0818: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0819: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0820: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0821: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0822: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0823: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0824: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0825: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0826: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0827: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0828: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0829: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0830: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0831: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0832: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0833: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0834: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0835: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0836: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0837: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0838: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0839: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0840: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0841: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0842: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0843: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0844: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0845: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0846: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0847: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0848: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0849: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0850: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0851: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0852: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0853: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0854: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0855: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0856: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0857: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0858: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0859: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0860: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0861: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0862: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0863: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0864: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0865: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0866: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0867: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0868: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0869: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0870: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0871: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0872: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0873: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0874: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0875: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0876: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0877: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0878: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0879: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0880: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0881: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0882: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0883: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0884: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0885: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0886: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0887: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0888: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0889: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0890: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0891: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0892: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0893: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0894: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0895: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0896: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0897: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0898: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0899: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0900: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0901: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0902: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0903: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0904: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0905: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0906: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0907: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0908: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0909: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0910: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0911: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0912: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0913: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0914: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0915: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0916: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0917: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0918: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0919: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0920: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0921: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0922: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0923: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0924: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0925: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0926: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0927: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0928: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0929: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0930: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0931: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0932: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0933: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0934: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0935: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0936: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0937: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0938: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0939: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0940: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0941: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0942: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0943: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0944: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0945: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0946: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0947: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0948: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0949: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0950: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0951: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0952: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0953: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0954: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0955: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0956: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0957: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0958: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0959: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0960: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0961: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0962: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0963: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0964: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0965: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0966: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0967: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0968: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0969: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0970: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0971: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0972: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0973: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0974: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0975: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0976: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0977: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0978: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0979: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0980: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0981: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0982: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0983: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0984: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0985: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0986: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0987: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0988: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0989: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0990: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0991: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0992: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0993: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0994: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0995: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0996: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0997: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0998: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 0999: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1000: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1001: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1002: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1003: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1004: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1005: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1006: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1007: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1008: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1009: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1010: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1011: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1012: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1013: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1014: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1015: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1016: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1017: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1018: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1019: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1020: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1021: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1022: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1023: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1024: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1025: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1026: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1027: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1028: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1029: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1030: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1031: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1032: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1033: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1034: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1035: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1036: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1037: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1038: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1039: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1040: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1041: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1042: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1043: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1044: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1045: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1046: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1047: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1048: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1049: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1050: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1051: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1052: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1053: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1054: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1055: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1056: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1057: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1058: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1059: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1060: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1061: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1062: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1063: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1064: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1065: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1066: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1067: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1068: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1069: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1070: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1071: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1072: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1073: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1074: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1075: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1076: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1077: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1078: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1079: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1080: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1081: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1082: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1083: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1084: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1085: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1086: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1087: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1088: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1089: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1090: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1091: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1092: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1093: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1094: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1095: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1096: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1097: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1098: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1099: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1100: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1101: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1102: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1103: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1104: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1105: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1106: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1107: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1108: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1109: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1110: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1111: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1112: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1113: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1114: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1115: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1116: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1117: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1118: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1119: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1120: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1121: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1122: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1123: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1124: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1125: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1126: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1127: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1128: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1129: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1130: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1131: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1132: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1133: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1134: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1135: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1136: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1137: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1138: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1139: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1140: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1141: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1142: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1143: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1144: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1145: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1146: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1147: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1148: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1149: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1150: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1151: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1152: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1153: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1154: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1155: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1156: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1157: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1158: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1159: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1160: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1161: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1162: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1163: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1164: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1165: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1166: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1167: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1168: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1169: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1170: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1171: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1172: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1173: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1174: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1175: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1176: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1177: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1178: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1179: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1180: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1181: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1182: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1183: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1184: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1185: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1186: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1187: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1188: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1189: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1190: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1191: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1192: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1193: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1194: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1195: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1196: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1197: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1198: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1199: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1200: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1201: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1202: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1203: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1204: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1205: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1206: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1207: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1208: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1209: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1210: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1211: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1212: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1213: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1214: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1215: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1216: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1217: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1218: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1219: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1220: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1221: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1222: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1223: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1224: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1225: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1226: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1227: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1228: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1229: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1230: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1231: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1232: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1233: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1234: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1235: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1236: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1237: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1238: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1239: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1240: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1241: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1242: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1243: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1244: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1245: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1246: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1247: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1248: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1249: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1250: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1251: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1252: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1253: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1254: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1255: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1256: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1257: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1258: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1259: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1260: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1261: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1262: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1263: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1264: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1265: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1266: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1267: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1268: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1269: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1270: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1271: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1272: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1273: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1274: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1275: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1276: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1277: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1278: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1279: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1280: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1281: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1282: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1283: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1284: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1285: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1286: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1287: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1288: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1289: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1290: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1291: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1292: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1293: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1294: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1295: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1296: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1297: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1298: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1299: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1300: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1301: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1302: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1303: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1304: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1305: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1306: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1307: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1308: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1309: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1310: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1311: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1312: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1313: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1314: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1315: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1316: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1317: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1318: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1319: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1320: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1321: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1322: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1323: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1324: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1325: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1326: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1327: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1328: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1329: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1330: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1331: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1332: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1333: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1334: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1335: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1336: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1337: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1338: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1339: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1340: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1341: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1342: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1343: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1344: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1345: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1346: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1347: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1348: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1349: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1350: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1351: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1352: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1353: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1354: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1355: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1356: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1357: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1358: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1359: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1360: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1361: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1362: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1363: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1364: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1365: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1366: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1367: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1368: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1369: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1370: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1371: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1372: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1373: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1374: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1375: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1376: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1377: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1378: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1379: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1380: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1381: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1382: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1383: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1384: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1385: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1386: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1387: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1388: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1389: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1390: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1391: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1392: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1393: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1394: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1395: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1396: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1397: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1398: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1399: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1400: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1401: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1402: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1403: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1404: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1405: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1406: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1407: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1408: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1409: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1410: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1411: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1412: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1413: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1414: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1415: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1416: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1417: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1418: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1419: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1420: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1421: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1422: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1423: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1424: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1425: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1426: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1427: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1428: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1429: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1430: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1431: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1432: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1433: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1434: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1435: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1436: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1437: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1438: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1439: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1440: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1441: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1442: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1443: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1444: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1445: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1446: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1447: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1448: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1449: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1450: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1451: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1452: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1453: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1454: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1455: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1456: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1457: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1458: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1459: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1460: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1461: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1462: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1463: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1464: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1465: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1466: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1467: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1468: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1469: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1470: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1471: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1472: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1473: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1474: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1475: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1476: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1477: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1478: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1479: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1480: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1481: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1482: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1483: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1484: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1485: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1486: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1487: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1488: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1489: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1490: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1491: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1492: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1493: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1494: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1495: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1496: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1497: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1498: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1499: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1500: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1501: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1502: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1503: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1504: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1505: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1506: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1507: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1508: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1509: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1510: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1511: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1512: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1513: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1514: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1515: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1516: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1517: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1518: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1519: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1520: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1521: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1522: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1523: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1524: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1525: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1526: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1527: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1528: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1529: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1530: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1531: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1532: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1533: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1534: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1535: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1536: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1537: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1538: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1539: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1540: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1541: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1542: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1543: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1544: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1545: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1546: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1547: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1548: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1549: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1550: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1551: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1552: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1553: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1554: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1555: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1556: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1557: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1558: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1559: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1560: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1561: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1562: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1563: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1564: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1565: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1566: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1567: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1568: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1569: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1570: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1571: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1572: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1573: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1574: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1575: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1576: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1577: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1578: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1579: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1580: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1581: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1582: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1583: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1584: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1585: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1586: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1587: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1588: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1589: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1590: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1591: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1592: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1593: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1594: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1595: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1596: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1597: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1598: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1599: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1600: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1601: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1602: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1603: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1604: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1605: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1606: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1607: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1608: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1609: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1610: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1611: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1612: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1613: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1614: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1615: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1616: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1617: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1618: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1619: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1620: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1621: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1622: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1623: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1624: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1625: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1626: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1627: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1628: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1629: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1630: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1631: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1632: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1633: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1634: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1635: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1636: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1637: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1638: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1639: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1640: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1641: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1642: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1643: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1644: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1645: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1646: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1647: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1648: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1649: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1650: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1651: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1652: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1653: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1654: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1655: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1656: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1657: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1658: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1659: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1660: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1661: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1662: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1663: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1664: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1665: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1666: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1667: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1668: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1669: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1670: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1671: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1672: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1673: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1674: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1675: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1676: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1677: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1678: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1679: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1680: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1681: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1682: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1683: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1684: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1685: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1686: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1687: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1688: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1689: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1690: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1691: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1692: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1693: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1694: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1695: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1696: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1697: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1698: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1699: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1700: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1701: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1702: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1703: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1704: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1705: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1706: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1707: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1708: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1709: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1710: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1711: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1712: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1713: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1714: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1715: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1716: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1717: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1718: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1719: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1720: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1721: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1722: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1723: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1724: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1725: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1726: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1727: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1728: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1729: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1730: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1731: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1732: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1733: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1734: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1735: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1736: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1737: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1738: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1739: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1740: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1741: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1742: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1743: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1744: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1745: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1746: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1747: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1748: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1749: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1750: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1751: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1752: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1753: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1754: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1755: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1756: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1757: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1758: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1759: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1760: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1761: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1762: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1763: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1764: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1765: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1766: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1767: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1768: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1769: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1770: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1771: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1772: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1773: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1774: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1775: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1776: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1777: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1778: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1779: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1780: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1781: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1782: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1783: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1784: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1785: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1786: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1787: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1788: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1789: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1790: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1791: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1792: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1793: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1794: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1795: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1796: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1797: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1798: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1799: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.
# CONTENT SLOT 1800: reserved for future pixel-art asset, animation frame, level prop, dialogue beat, or encounter tuning.

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
