from flask import Flask, Response, request, jsonify

app = Flask(__name__)

GAME_HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Ashes of the Dead</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#020304;color:#e8e4da;font-family:Consolas,monospace}
body{display:grid;place-items:center}
#app{position:relative;width:min(100vw,1280px);aspect-ratio:16/9;background:#06090b;overflow:hidden;box-shadow:0 0 0 1px #1b2224,0 0 120px rgba(0,0,0,.95)}
canvas{position:absolute;inset:0;width:100%;height:100%;display:block;image-rendering:pixelated;image-rendering:crisp-edges}
#world{z-index:1;background:#090d10}
.layer{position:absolute;inset:0}
.hidden{display:none!important}
button{font:inherit;color:#e8e4da;background:#111719;border:1px solid #68716f;cursor:pointer;touch-action:manipulation}
button:hover{background:#202827;border-color:#c4c0b1}
button:focus-visible{outline:2px solid #d5c58e;outline-offset:2px}
.screen{display:grid;place-items:center;z-index:40;background:rgba(2,3,4,.94)}
.panel{width:min(820px,92%);border:1px solid #4f595b;background:linear-gradient(180deg,#111619,#070a0c);padding:30px;box-shadow:0 20px 90px rgba(0,0,0,.9);position:relative}
.panel:before{content:"";position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(255,255,255,.018),rgba(255,255,255,.018) 1px,transparent 1px,transparent 5px)}
h1{margin:0;text-align:center;letter-spacing:7px;font-size:42px;color:#efe9db;text-shadow:3px 3px #000,0 0 22px rgba(224,216,196,.18)}
.subtitle{text-align:center;color:#88928e;letter-spacing:3px;margin-top:9px}
.lore{text-align:center;max-width:760px;margin:20px auto;color:#a9b1ad;line-height:1.7}
.center{text-align:center}
.menu{z-index:45;overflow:hidden;background:#040607}
.menuBackdrop{position:absolute;inset:0;overflow:hidden}
.menuMoon{position:absolute;right:12%;top:10%;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,#c3c0ad 0,#7f8076 42%,#2a2f31 72%,transparent 73%);box-shadow:0 0 100px rgba(195,192,173,.08)}
.menuOcean{position:absolute;left:0;right:0;bottom:0;height:42%;background:linear-gradient(180deg,#0e1c22,#071014)}
.menuIsland{position:absolute;left:-4%;right:-4%;bottom:20%;height:24%;background:#151a1d;clip-path:polygon(0 88%,9% 70%,18% 76%,30% 50%,43% 67%,57% 35%,68% 59%,80% 48%,91% 70%,100% 52%,100% 100%,0 100%)}
.menuPrison{position:absolute;left:27%;right:27%;bottom:20%;height:34%;background:#171d20;border-top:7px solid #3a4346}
.menuPrison:before{content:"";position:absolute;left:9%;right:9%;top:24%;height:50%;background:repeating-linear-gradient(90deg,#20282b 0,#20282b 22px,#3b4548 23px,#3b4548 27px);opacity:.7}
.menuTower{position:absolute;left:49%;bottom:47%;width:70px;height:170px;background:#242c2e;box-shadow:0 0 20px rgba(0,0,0,.6)}
.menuTower:before{content:"";position:absolute;left:-9px;right:-9px;top:-12px;height:13px;background:#3b4242}
.menuFog{position:absolute;left:-10%;right:-10%;bottom:26%;height:20%;background:linear-gradient(90deg,transparent,rgba(190,196,190,.08),transparent);filter:blur(16px);animation:fogMove 12s linear infinite}
.menuFog.two{bottom:36%;opacity:.65;animation-duration:19s;animation-direction:reverse}
@keyframes fogMove{from{transform:translateX(-14%)}to{transform:translateX(14%)}}
.menuRain{position:absolute;inset:0;opacity:.33;background:repeating-linear-gradient(110deg,transparent 0 19px,rgba(195,213,220,.16) 20px,transparent 21px 37px);animation:rainShift .7s linear infinite}
@keyframes rainShift{from{background-position:0 0}to{background-position:90px 140px}}
.menuVignette{position:absolute;inset:0;background:radial-gradient(circle at center,transparent 30%,rgba(0,0,0,.72) 100%)}
.menuNoise{position:absolute;inset:0;opacity:.07;background-image:radial-gradient(circle at 10% 30%,#fff 0 1px,transparent 1.5px);background-size:9px 9px;mix-blend-mode:screen}
.menuContent{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px 20px 20px;text-align:center}
.menuKicker{font-size:11px;letter-spacing:4px;color:#8b9690;margin-bottom:14px}
.menuLogo{font-size:clamp(34px,5vw,70px);font-weight:800;letter-spacing:8px;color:#eee7db;text-shadow:4px 4px #050606,0 0 34px rgba(218,212,194,.17);animation:menuFlicker 7s infinite}
@keyframes menuFlicker{0%,94%,100%{opacity:1}95%{opacity:.75}96%{opacity:1}97%{opacity:.58}98%{opacity:1}}
.menuTag{margin-top:9px;color:#8d948f;letter-spacing:3px;font-size:11px}
.menuLore{max-width:650px;margin:17px auto;color:#b8beb9;line-height:1.6;font-size:12px}
.menuButtons{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:13px}
.menuButtons button{min-width:175px;padding:14px 22px;font-weight:800;letter-spacing:3px}
.menuPlay{border-color:#938a6e;background:#161916;box-shadow:0 0 30px rgba(170,155,105,.08)}
.menuThreat{margin-top:17px;color:#7c5954;letter-spacing:3px;font-size:10px}
.menuFooter{position:absolute;bottom:12px;left:12px;right:12px;color:#565f5b;font-size:9px;letter-spacing:1.6px}
.menuSignal{position:absolute;top:13px;right:15px;color:#5d6763;font-size:9px;letter-spacing:2px}
.menuSignal b{color:#a99668}
.charSelect{z-index:43;background:linear-gradient(180deg,#070a0c,#020304)}
.charSelectBox{width:min(880px,93%);padding:34px;border:1px solid #485153;background:linear-gradient(180deg,#111619,#080a0b);box-shadow:0 30px 110px #000;text-align:center}
.charSelectTitle{font-size:25px;letter-spacing:5px;color:#eee9de}
.charSelectSub{margin:10px auto 17px;color:#87918d;font-size:11px;line-height:1.5;max-width:670px}
.charCards{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin:18px 0}
.charCard{width:220px;min-height:150px;padding:20px 12px;position:relative;overflow:hidden;background:linear-gradient(180deg,#121819,#0a0d0e);border:1px solid #5a6362}
.charCard:before{content:"";position:absolute;inset:8px;border:1px solid #252c2b;pointer-events:none}
.charCard .name{display:block;font-size:22px;letter-spacing:4px;color:#fff5df;text-shadow:2px 2px #000;margin-top:14px}
.charCard .meta{display:block;margin-top:9px;color:#c0c7c3;font-size:10px;line-height:1.5;text-shadow:2px 2px #000}
.charCard .skill{display:block;margin-top:14px;color:#878f8a;font-size:10px}
.credits{z-index:44;background:rgba(2,3,4,.96)}
.creditsBox{width:min(820px,92%);border:1px solid #5a6260;background:linear-gradient(180deg,#101416,#060809);padding:28px;box-shadow:0 30px 100px #000;text-align:center}
.creditsBox h2{margin:0 0 16px;font-size:26px;letter-spacing:5px}
.creditsName{color:#ddd2b7;font-weight:800;letter-spacing:2px}
.creditsBox p{color:#aab1ad;line-height:1.75;font-size:12px}
.controlOverlay{z-index:46;background:rgba(0,0,0,.9);display:grid;place-items:center}
.controlBox{width:min(720px,93%);border:1px solid #5a625f;background:#080b0c;padding:24px;text-align:center;box-shadow:0 30px 100px #000}
.controlGrid{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin:19px 0}
.controlGrid button{min-width:220px;padding:15px 12px}
.controlGrid button.selected{border-color:#d2c79f;box-shadow:inset 0 0 0 1px #7c7357,0 0 30px rgba(210,199,159,.08);background:#1a1f1d}
.controlGrid small{display:block;color:#7d8782;margin-top:7px;font-size:9px}
#privacyGate{z-index:100;background:rgba(0,0,0,.97);display:flex;align-items:center;justify-content:center;padding:20px}
.privacyBox{width:min(900px,94%);max-height:90%;overflow:auto;border:2px solid #626d67;background:linear-gradient(180deg,#0f1411,#060807);padding:25px;box-shadow:0 30px 120px #000}
.privacyBox h2{margin:0;letter-spacing:4px;font-size:24px}
.privacyGrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}
.privacyCard{border:1px solid #28312d;background:#0b0f0d;padding:12px;color:#aeb7b1;line-height:1.55;font-size:11px}
.privacyCard b{display:block;color:#e0e5e0;margin-bottom:5px}
.privacyNote{border-left:3px solid #9e6f6c;background:#0b0f0d;padding:11px;color:#969f99;font-size:11px;line-height:1.5}
.privacyActions{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:18px}
.privacyActions button{padding:11px 16px}
#hud{z-index:10;pointer-events:none;text-shadow:2px 2px #000}
.topHud{position:absolute;left:18px;right:18px;top:14px;display:flex;justify-content:space-between;align-items:flex-start;font-size:11px}
.hudLeft{width:240px}.barLabel{color:#aeb5b1;margin-top:4px}.bar{height:8px;background:#0d1112;border:1px solid #4e5555;margin:3px 0 7px}.fill{height:100%}.health{background:#af4e49}.stamina{background:#849278}.sanity{background:#74709a}.hudRight{text-align:right;color:#c9cec9}.hudRight .loc{color:#ece8dc;font-size:12px;letter-spacing:2px}.hudRight .threat{color:#847f76;margin-top:5px}.objective{position:absolute;left:18px;top:107px;max-width:520px;color:#e2dfd7;font-size:12px;line-height:1.45;white-space:pre-line}.objectiveTab{position:absolute;right:18px;top:92px;padding:10px 12px;pointer-events:auto;letter-spacing:2px;background:rgba(7,10,10,.88)}.objectivePanel{position:absolute;right:18px;top:138px;width:min(420px,42%);max-height:61%;overflow:auto;display:none;pointer-events:auto;background:rgba(5,7,7,.96);border:1px solid #59625f;box-shadow:0 20px 70px #000}.objectivePanel.open{display:block}.objectiveHead{padding:13px;border-bottom:1px solid #2b3230;display:flex;justify-content:space-between}.objectiveTitle{letter-spacing:3px;font-size:14px}.objectiveList{padding:10px}.objectiveItem{padding:11px;margin-bottom:8px;border:1px solid #242b29;background:#0c100f;color:#aeb6b1;font-size:11px;line-height:1.55}.objectiveItem.current{border-color:#9a9274;color:#ece9df;box-shadow:inset 3px 0 #c7ba91}.objectiveItem.done{opacity:.55}.step{display:block;color:#737e78;margin-top:5px}.objectiveClose{width:30px;height:30px}.message{position:absolute;left:50%;bottom:55px;transform:translateX(-50%);padding:9px 15px;background:rgba(3,4,4,.9);border:1px solid #535b58;color:#e4e0d5;max-width:80%;text-align:center}.prompt{position:absolute;left:50%;bottom:21px;transform:translateX(-50%);color:#d7d1c5;text-align:center}.inventoryHud{position:absolute;right:18px;top:105px;background:rgba(5,7,7,.92);border:1px solid #4b5350;padding:11px;width:240px;font-size:11px;line-height:1.6}.inventoryUi{z-index:65;background:rgba(0,0,0,.72);display:grid;place-items:center}.chestPanel{width:min(940px,94%);border:2px solid #5d5549;background:#151311;padding:17px;box-shadow:0 25px 100px #000}.chestHeader{display:flex;justify-content:space-between;align-items:center;gap:12px;border-bottom:1px solid #463f37;padding-bottom:12px}.chestTitle{font-size:18px;color:#e6d8bd;letter-spacing:3px}.chestHint{font-size:9px;color:#8d8578;margin-top:4px}.slotArea{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:14px}.slotSection{background:#0c0b0a;border:1px solid #3e3932;padding:10px}.slotTitle{color:#aaa093;font-size:10px;letter-spacing:1px;margin-bottom:8px}.slotGrid{display:grid;grid-template-columns:repeat(9,1fr);gap:4px}.slot{aspect-ratio:1;border:1px solid #4d463d;background:#1b1916;display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:0;cursor:pointer;font-size:8px;color:#d8d1c2}.slot:hover{border-color:#c4ac77;background:#27231d}.slotIcon{width:18px;height:14px;background:#766044;margin-bottom:4px}.slotCount{color:#c7b998}.chestActions{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}.chestFooter{color:#77756d;font-size:9px;margin-top:10px}.cutscene{z-index:55;display:grid;place-items:center;background:radial-gradient(circle at 50% 50%,#182124,#020304 65%,#000)}.cutscene:before,.cutscene:after{content:"";position:absolute;left:0;right:0;height:70px;background:#000}.cutscene:before{top:0}.cutscene:after{bottom:0}.cutText{position:relative;z-index:2;max-width:890px;text-align:center;font-size:27px;line-height:1.6;color:#e2ddd2;text-shadow:4px 4px #000,0 0 18px #000;padding:28px}.cutText small{display:block;margin-top:18px;color:#777e7a;font-size:10px;letter-spacing:3px}.fade{position:absolute;inset:0;background:#000;opacity:0;pointer-events:none;z-index:80;transition:opacity .65s ease}.scare{z-index:90;background:#050000;display:grid;place-items:center;opacity:0;pointer-events:none;transition:opacity .09s linear}.scare.show{opacity:1}.scareFace{position:relative;width:min(440px,64vw);height:min(500px,70vh);background:#030303;border-radius:47% 47% 43% 43%;box-shadow:0 0 80px #000}.scareFace:before{content:"";position:absolute;left:13%;right:13%;top:17%;height:8px;background:#dfd6c7;box-shadow:0 100px 0 #dfd6c7}.scareFace:after{content:"";position:absolute;left:14%;right:14%;bottom:16%;height:70px;border:7px solid #d8d0c4;border-top:0;border-radius:0 0 80px 80px}.scareText{position:absolute;bottom:9%;left:0;right:0;text-align:center;font-weight:900;letter-spacing:7px;color:#ece4d9;text-shadow:4px 4px #000}.worldWarning{position:absolute;inset:0;pointer-events:none}.worldWarningText{position:absolute;left:50%;top:27%;transform:translate(-50%,-50%);color:#d7ccc2;font-size:20px;letter-spacing:4px;text-shadow:4px 4px #000;opacity:0}.mobileControls{z-index:30;position:absolute;inset:0;pointer-events:none}.mobileControls .cluster{position:absolute;bottom:17px;display:flex;gap:8px;pointer-events:auto}.mobileControls .left{left:17px}.mobileControls .right{right:17px;max-width:48%;flex-wrap:wrap;justify-content:flex-end}.mobileControls button{width:52px;height:52px;border-radius:10px;background:rgba(20,24,23,.74);border:1px solid rgba(222,215,195,.42);color:#f0eadc;font-size:11px}.mobileControls button:active{background:#39403c}.touchAim{position:absolute;right:146px;bottom:29px;color:#747c78;font-size:9px;pointer-events:none}.soundButton{position:absolute;left:16px;top:14px;z-index:22;padding:7px 10px;font-size:9px;letter-spacing:1px;pointer-events:auto;background:rgba(8,11,11,.8)}
@media(max-width:760px){.privacyGrid,.slotArea{grid-template-columns:1fr}.menuLogo{letter-spacing:5px}.menuPrison{left:13%;right:13%}.objectivePanel{width:88%;right:6%}.objective{max-width:65%;font-size:10px}.topHud{font-size:9px}.hudLeft{width:180px}.panel{padding:22px}.charCard{width:100%;min-height:110px}.slotGrid{grid-template-columns:repeat(6,1fr)}}
</style>
</head>
<body>
<div id="app">
<canvas id="world" width="1280" height="720"></canvas>
<div id="mainMenu" class="layer menu">
<div class="menuBackdrop"><div class="menuMoon"></div><div class="menuOcean"></div><div class="menuIsland"></div><div class="menuPrison"></div><div class="menuTower"></div><div class="menuFog"></div><div class="menuFog two"></div><div class="menuRain"></div><div class="menuVignette"></div><div class="menuNoise"></div></div>
<div class="menuContent"><div class="menuKicker">NIGHTWATCH // ALCATRAZ INCIDENT 01</div><div class="menuLogo">ASHES OF THE DEAD</div><div class="menuTag">SCREAM JAM 2026 • THE ISLAND IS LISTENING</div><div class="menuLore">A female detective wakes inside Cell A-17. The prison is quiet. The rain is loud. Something else is awake. Find the docks. Escape the island. Find two survivors.</div><div class="menuButtons"><button id="playButton" class="menuPlay">PLAY</button><button id="creditsButton">CREDITS</button><button id="controlsButton">CONTROL MODE</button></div><div class="menuThreat">HEADPHONES RECOMMENDED • DO NOT TRUST EVERY SOUND</div><div class="menuFooter">JULIA • MAY • YUMI • FEMALE DETECTIVES • ALCATRAZ → SAN FRANCISCO</div><div id="menuSignal" class="menuSignal">SIGNAL: <b>UNSTABLE</b></div></div></div>
<div id="characterMenu" class="layer screen hidden"><div class="charSelectBox"><div class="charSelectTitle">CHOOSE YOUR DETECTIVE</div><div class="charSelectSub">No portraits. Choose by profile. All three are female detectives with different strengths.</div><div class="charCards"><button class="charCard" data-character="Julia"><span class="name">JULIA</span><span class="meta">FIELD DETECTIVE<br>CALM UNDER PRESSURE</span><span class="skill">BALANCED SURVIVAL</span></button><button class="charCard" data-character="May"><span class="name">MAY</span><span class="meta">CRIME SCENE DETECTIVE<br>FAST INVESTIGATION</span><span class="skill">AGILITY + SEARCH</span></button><button class="charCard" data-character="Yumi"><span class="name">YUMI</span><span class="meta">INTELLIGENCE DETECTIVE<br>OBSERVANT + TECHNICAL</span><span class="skill">STEADY AIM + SANITY</span></button></div><div class="center"><button id="characterBack">BACK</button><button id="characterControls">CONTROL MODE</button><button id="characterPrivacy">PRIVACY</button></div></div></div>
<div id="credits" class="layer credits hidden"><div class="creditsBox"><h2>CREDITS</h2><p class="creditsName">Mayumi Alingarog (Yumi, Mimi, Yumimi)</p><p>With heartfelt thanks to Mayumi Alingarog (Yumi, Mimi, Yumimi), a wonderful classmate and developer whose kindness, helpfulness, respect, creativity, and encouragement inspired me to join Scream Jam 2026. She is the kind of teammate who makes difficult things feel possible, and I am grateful for every bit of support and inspiration.</p><p>ASHES OF THE DEAD • Scream Jam 2026</p><button id="creditsBack">BACK</button></div></div>
<div id="controlsOverlay" class="layer controlOverlay hidden"><div class="controlBox"><div class="charSelectTitle">CONTROL MODE</div><div class="charSelectSub">Choose exactly how you want to play. Your choice stays active until you change it.</div><div class="controlGrid"><button data-control="laptop" id="laptopMode">LAPTOP / DESKTOP<small>A / D • W / SPACE • SHIFT • MOUSE</small></button><button data-control="mobile" id="mobileMode">MOBILE / TOUCH<small>VIRTUAL BUTTONS • TOUCH AIM</small></button></div><div class="center"><button id="autoMode">AUTO DETECT</button> <button id="controlsBack">BACK</button></div><div id="controlStatus" class="small" style="margin-top:12px;color:#777f7b"></div></div></div>
<div id="hud" class="layer hidden"><button id="soundButton" class="soundButton">SOUND: ON</button><div class="topHud"><div class="hudLeft"><div>HEALTH <span id="healthValue"></span></div><div class="bar"><div id="healthFill" class="fill health"></div></div><div>STAMINA <span id="staminaValue"></span></div><div class="bar"><div id="staminaFill" class="fill stamina"></div></div><div>SANITY <span id="sanityValue"></span></div><div class="bar"><div id="sanityFill" class="fill sanity"></div></div></div><div class="hudRight"><div id="locationText" class="loc">ALCATRAZ</div><div id="threatText" class="threat">THE PRISON IS QUIET</div><div id="ammoText">AMMO 12 / 12</div></div></div><div id="objective" class="objective"></div><button id="objectiveTab" class="objectiveTab">OBJECTIVES +</button><div id="objectivePanel" class="objectivePanel"><div class="objectiveHead"><div><div class="objectiveTitle">OBJECTIVES</div><div id="objectiveHint" class="small">CURRENT GOAL</div></div><button id="objectiveClose" class="objectiveClose">×</button></div><div class="objectiveList" id="objectiveList"></div></div><div id="message" class="message hidden"></div><div id="prompt" class="prompt"></div><div id="inventoryHud" class="inventoryHud hidden"></div></div>
<div id="cutscene" class="layer cutscene hidden"><div id="cutText" class="cutText"></div></div>
<div id="pause" class="layer screen hidden"><div class="panel"><h1>PAUSED</h1><p class="lore">The rain keeps falling. The island keeps breathing.</p><div class="center"><button id="resumeButton">RESUME</button> <button id="restartButton">RESTART CHAPTER</button> <button id="pauseMenuButton">MAIN MENU</button></div></div></div>
<div id="ending" class="layer screen hidden"><div class="panel"><h1>YOU SURVIVED</h1><p id="endingText" class="lore"></p><div class="center"><button id="endingMenuButton">MAIN MENU</button></div></div></div>
<div id="death" class="layer screen hidden"><div class="panel"><h1 style="color:#b14d4a">THE DARKNESS FOUND YOU</h1><p id="deathText" class="lore"></p><div class="center"><button id="deathRestartButton">TRY AGAIN</button><button id="deathMenuButton">MAIN MENU</button></div></div></div>
<div id="inventoryUi" class="layer inventoryUi hidden"><div class="chestPanel"><div class="chestHeader"><div><div id="chestTitle" class="chestTitle">SUPPLY CHEST</div><div class="chestHint">CLICK AN ITEM TO TAKE IT • 27 CHEST SLOTS • 27 PLAYER SLOTS</div></div><button id="chestCloseButton">CLOSE</button></div><div class="slotArea"><div class="slotSection"><div class="slotTitle">CHEST STORAGE</div><div id="chestSlots" class="slotGrid"></div></div><div class="slotSection"><div class="slotTitle">PLAYER INVENTORY</div><div id="playerSlots" class="slotGrid"></div></div></div><div class="chestActions"><button id="takeAllButton">TAKE ALL</button><button id="sortButton">SORT</button></div><div id="chestFooter" class="chestFooter"></div></div></div>
<div id="infoOverlay" class="layer screen hidden"><div class="panel"><h1 style="font-size:26px;letter-spacing:4px">NIGHTWATCH DEVICE RECORD</h1><div class="privacyGrid" id="deviceGrid"></div><div class="center"><button id="infoClose">CLOSE</button></div></div></div>
<div id="fade" class="fade"></div>
<div id="scare" class="layer scare"><div class="scareFace"><div class="scareText">DON'T LOOK AWAY</div></div></div>
<div id="worldWarning" class="worldWarning"><div id="warningText" class="worldWarningText"></div></div>
<div id="mobileControls" class="mobileControls hidden"><div class="cluster left"><button data-touch="left">◀</button><button data-touch="right">▶</button><button data-touch="run">RUN</button></div><div class="touchAim">TOUCH AIM</div><div class="cluster right"><button data-touch="jump">JUMP</button><button data-touch="interact">USE</button><button data-touch="melee">MELEE</button><button data-touch="light">LIGHT</button><button data-touch="inventory">BAG</button><button data-touch="reload">RELOAD</button><button data-touch="fire">FIRE</button></div></div>
</div>
<div id="privacyGate"><div class="privacyBox"><h2>NIGHTWATCH SECURITY TERMINAL</h2><p class="subtitle">ASHES OF THE DEAD — DEVICE INFORMATION NOTICE</p><div class="privacyGrid"><div class="privacyCard"><b>WHAT MAY BE DISPLAYED</b>Browser/platform, screen size, language, timezone, network hints, CPU thread count, online status, touch support, cookies state, battery data when available, and the address seen by the game server.</div><div class="privacyCard"><b>WHAT IS NOT READ</b>The game does not read passwords, personal files, photos, contacts, saved documents, account contents, or arbitrary files from your computer.</div><div class="privacyCard"><b>PERMISSIONS</b>Location, camera, and microphone require a separate browser permission and are never silently enabled.</div><div class="privacyCard"><b>FICTIONAL HORROR</b>The Smiler, CCTV events, surveillance messages, screams and fourth-wall moments are fictional game elements unless explicitly identified as browser/server information.</div></div><div class="privacyNote">The server can only see the network address that reaches it. Proxies, VPNs, carrier networks and hosting layers can change the address shown. This is an entertainment game.</div><div class="privacyActions"><button id="privacyEnter">ENTER ASHES OF THE DEAD</button><button id="privacyDevice">DEVICE PANEL</button></div></div></div>
<script>
'use strict';
const canvas=document.getElementById('world');
const ctx=canvas.getContext('2d');
ctx.imageSmoothingEnabled=false;
const W=1280,H=720,GROUND=570;
const worldWidth={ALCATRAZ:5200,SF:8200};
const keys=new Set();
const touch={left:false,right:false,run:false,jump:false};
const mouse={x:640,y:360,down:false};
const player={x:0,y:0,w:34,h:70,vx:0,vy:0,facing:1,onGround:true,doubleJump:true,coyote:0,jumpBuffer:0,anim:0,stepTimer:0,landTimer:0,recoil:0,hitTimer:0};
const state={health:100,maxHealth:100,stamina:100,maxStamina:100,sanity:100,hunger:100,ammo:12,reserveAmmo:36,grenades:2,light:true,battery:100,medkits:1,bandages:2,scrap:0,startKey:false,startEscaped:false,dockPass:false,beacon:false,boatEscaped:false,survivors:0,inventory:{bandage:2,food:2,scrap:2,ammo_9mm:36},level:1,xp:0};
const inputState={left:false,right:false,run:false,jump:false};
let controlMode='laptop';
let selectedCharacter='Julia';
let scene='menu';
let chapter='ALCATRAZ';
let interior=null;
let interiorFloor=1;
let camera=0;
let last=performance.now();
let totalTime=0;
let fadeBusy=false;
let fadeTimer=0;
let messageTimer=0;
let scareTimer=16;
let footstepsTimer=0;
let weatherTime=0;
let smiler={active:false,timer:0,cooldown:13,x:0,intensity:0,variant:0};
let horror={flash:0,shake:0,warning:0,heartbeat:0,glitch:0,blackout:0};
let currentChest=null;
let objectivePanelOpen=false;
let introIndex=0;
let introTimer=0;
let objectiveIndex=0;
let goalFocus='escape';
let survivors=[];
let zombies=[];
let chests=[];
let buildings=[];
let cells=[];
let particles=[];
let footprints=[];
let rainDrops=[];
let shotTracers=[];
let transitionTarget=null;
let soundEnabled=true;
let audioCtx=null;
let masterGain=null;
let musicGain=null;
let sfxGain=null;
let rainGain=null;
let musicStarted=false;
let rainStarted=false;
let cutLines=[
'ALCATRAZ ISLAND — 11:47 PM',
'You wake inside Cell A-17. Concrete. Rust. Rain.',
'The cell door is shut. Something moves beyond the bars.',
'Across the corridor, Cell Block A disappears into darkness.',
'You need the key. Then the docks. Then a way off this island.',
'Whatever is watching you wants you to believe you are alone.'
];

const loreFragments=[
 'THE RAIN HIDES FOOTSTEPS.',
 'CELL BLOCK A // KEEP YOUR LIGHT LOW.',
 'SOMEONE SCRATCHED A MAP INTO THE WALL.',
 'B-4 WAS LOCKED BEFORE THE OUTBREAK.',
 'THE MEDICAL WING LOST POWER AT 23:14.',
 'THE DOCK SIREN RANG AFTER EVERYONE LEFT.',
 'A FERRY LIGHT WAS SEEN LAST NIGHT.',
 'NO ONE SIGNED THE FINAL LOG.',
 'THE WINDOWS WERE OPEN FROM THE INSIDE.',
 'SOMETHING WAS MOVING BETWEEN THE CELLS.',
 'THE GUARD RADIO REPEATED ONE NAME.',
 'THE PRISON CAMERAS NEVER WENT DARK.',
 'A SHADOW STOOD WHERE THE CAMERA COULD NOT SEE.',
 'THE FLOODLIGHTS STILL WORK OUTSIDE.',
 'THE WATER IS COLDER NEAR THE DOCK.',
 'FOLLOW THE WHITE PAINT ON THE PIPES.',
 'DO NOT FOLLOW FOOTSTEPS THAT STOP SUDDENLY.',
 'THE ISLAND IS QUIETER AFTER MIDNIGHT.',
 'THE SMILER DOES NOT RUN.',
 'THE SMILER WAITS.',
 'YOU ARE NOT THE FIRST DETECTIVE HERE.',
 'THE LAST REPORT ENDED MID-SENTENCE.',
 'THE SURVIVORS HEARD A BELL FROM THE WATER.',
 'THE LIGHT IN THE HALLWAY WAS REAL.',
 'THE FACE IN THE WINDOW WAS NOT.',
 'THE FERRY HORN IS YOUR WAY OUT.',
 'THE CITY HAS FEWER PEOPLE THAN CARS.',
 'FIND TWO PEOPLE. DO NOT LOSE THEM.',
 'THE ARCHIVE KNOWS WHY THEY LEFT.',
 'THE SHELTER DOOR ONLY OPENS FROM INSIDE.',
 'THE WET FLOOR REMEMBERS EVERY FOOTSTEP.',
 'THE WALLS ARE THICKER THAN THEY LOOK.',
 'THE CELL DOOR WAS NEVER MEANT TO HOLD YOU.',
 'SOMETHING SCRATCHED THE LOCK.',
 'THE OCEAN IS TOO CALM.',
 'THE FOG MOVES AGAINST THE WIND.',
 'THE STREET LAMPS ARE STILL ON.',
 'THE SHADOWS ARE NOT.',
 'THE RAIN SOUNDS LIKE WHISPERS.',
 'THE WHISPERS ARE NOT RANDOM.',
 'YOU HEARD THAT.',
 'KEEP MOVING.',
 'CHECK BEHIND YOU ONLY ONCE.',
 'THE NEXT ROOM HAS A CHEST.',
 'THE NEXT CHEST HAS A COST.',
 'THE NEXT DOOR LEADS OUT.',
 'THE EXIT IS NEVER AS FAR AS IT LOOKS.',
 'THE LIGHT WILL NOT SAVE YOU.',
 'BUT IT HELPS.',
 'DO NOT WASTE YOUR BATTERY.',
 'THE MEDICAL WING HAS WHAT YOU NEED.',
 'THE DOCK PASS IS REAL.',
 'THE FERRY IS REAL.',
 'THE SMILER IS ALSO REAL.',
 'OR AT LEAST YOU THINK IT IS.',
 'JULIA WRITES EVERYTHING DOWN.',
 'MAY NOTICES WHAT OTHERS MISS.',
 'YUMI LISTENS BEFORE SHE MOVES.',
 'EACH DETECTIVE HAS A DIFFERENT WAY THROUGH.',
 'NONE OF THEM ARE IMMUNE TO FEAR.',
 'THE CITY WILL NOT WAIT FOR YOU.',
 'THE SHELTER LIGHT IS WARM.',
 'WARM LIGHT DOES NOT MEAN SAFE.',
 'THE ARCHIVE DOOR HAS A CAMERA.',
 'THE CAMERA HAS A BLIND SPOT.',
 'SOMETHING USES THE BLIND SPOT.',
 'THE FUNERAL HOME HAS A BACK DOOR.',
 'THE HOTEL HAS TOO MANY FLOORS.',
 'THE HOSPITAL ELEVATOR STILL WORKS.',
 'THE RESEARCH ANNEX SHOULD HAVE BEEN EMPTY.',
 'IT WAS NOT EMPTY.',
 'THE FIRST SURVIVOR KNOWS THE STREET.',
 'THE SECOND SURVIVOR KNOWS THE BUILDINGS.',
 'THE THIRD SURVIVOR KNOWS THE TRUTH.',
 'YOU ONLY NEED TWO.',
 'THE FERRY ONLY NEEDS ONE SIGNAL.',
 'LIGHT THE BEACON.',
 'WATCH THE WATER.',
 'BOARD QUICKLY.',
 'DO NOT LOOK INTO THE CABIN WINDOWS.',
 'THE SMILE WILL BE THERE FIRST.',
 'THE ISLAND NEVER FORGETS.',
 'NEITHER DOES YOUR CAMERA.',
 'THIS MESSAGE IS PART OF THE GAME.',
 'UNLESS IT ISN’T.',
 'YOU ARE GETTING CLOSE.',
 'THE QUIET IS A WARNING.',
 'THE LOUD NOISE IS A DISTRACTION.',
 'THE FOOTSTEPS BEHIND YOU ARE NOT YOURS.',
 'SOMETHING IS WALKING WITH YOU.',
 'YOU HAVE BEEN HERE LONGER THAN YOU THINK.',
 'THE CLOCK IS WRONG.',
 'THE MAP IS NOT COMPLETE.',
 'THE EXIT IS STILL THERE.',
 'KEEP THE LIGHT ON.',
 'THEN TURN IT OFF.',
 'LISTEN.',
 'NOW RUN.',
 'END OF FIELD NOTES.'
];
const itemDescriptions={
 key:'A small brass key for a cell door.',
 dockPass:'A laminated prison dock pass. It is clearly marked for authorized ferry access.',
 bandage:'A basic emergency dressing.',
 ammo:'A handful of 9mm ammunition.',
 medkit:'A compact medical kit.',
 food:'A sealed can of food.',
 scrap:'Useful metal and repair pieces'
};

const gameplayTips=[
 'RUNNING MAKES MORE NOISE THAN WALKING.',
 'JUMPING CAN CROSS SMALL OBSTACLES.',
 'THE SECOND JUMP IS AVAILABLE ONCE PER AIRBORNE LEAP.',
 'LET STAMINA RECOVER BEFORE A LONG RUN.',
 'KEEP THE FLASHLIGHT ON WHEN YOU NEED TO READ SIGNS.',
 'SAVE YOUR BATTERY WHEN CROSSING OPEN GROUND.',
 'CHESTS ARE LIMITED. SEARCH IMPORTANT ROOMS FIRST.',
 'THE MEDICAL WING IS THE BEST PLACE TO FIND THE DOCK PASS.',
 'THE DOCK PASS IS MARKED FOR THE FERRY.',
 'THE BEACON IS AT THE MAIN FERRY DOCK.',
 'DOORS USE A SOFT FADE INSTEAD OF INSTANT TELEPORTS.',
 'LEFT AND RIGHT INTERIOR EXITS CAN BE USED.',
 'SURVIVORS CAN BE SPOKEN TO WITH E.',
 'YOU NEED TWO SURVIVORS TO COMPLETE THE CITY GOAL.',
 'THE OBJECTIVES TAB IS IN THE TOP RIGHT.',
 'THE MINIMAP IS INTENTIONALLY ABSENT.',
 'FOLLOW SIGNS WHEN YOU ARE LOST.',
 'FOLLOW LIGHTED DOORWAYS WHEN YOU ARE INSIDE.',
 'THE SMILER PREFERS DISTANCE.',
 'A SMILER SIGHTING DOES NOT ALWAYS MEAN AN ATTACK.',
 'LOW SANITY MAKES SOUNDS AND VISUALS LESS TRUSTWORTHY.',
 'JUMPSCARES ARE RARE ON PURPOSE.',
 'NOT EVERY SHADOW IS THE SMILER.',
 'NOT EVERY SOUND IS A ZOMBIE.',
 'THE STREET LAMPS STAY ON OUTSIDE.',
 'INTERIOR LIGHTS CAN FLICKER DURING A HORROR EVENT.',
 'THE FERRY NEVER REQUIRES A VEHICLE ON ALCATRAZ.',
 'ALCATRAZ HAS NO CARS.',
 'SAN FRANCISCO HAS DAMAGED CARS.',
 'THE MEDICAL WING HAS AN INDOOR SUPPLY CHEST.',
 'WORKSHOPS CAN CONTAIN SCRAP AND AMMUNITION.',
 'SAFE ROUTES ARE OFTEN QUIETER THAN SHORT ROUTES.',
 'A QUIET HALLWAY MAY BE A GOOD SIGN.',
 'A QUIET HALLWAY MAY ALSO BE A TERRIBLE SIGN.',
 'THE RAIN MASKS SOME FOOTSTEPS.',
 'THE RAIN DOES NOT MASK THE SMILER.',
 'HEADPHONES MAKE DISTANCE CUES EASIER TO HEAR.',
 'SOUND STARTS AFTER YOUR FIRST MENU INTERACTION.',
 'MOBILE MODE USES ON-SCREEN CONTROLS.',
 'LAPTOP MODE USES KEYBOARD AND MOUSE.',
 'AUTO DETECT CHOOSES MOBILE OR LAPTOP FOR YOU.',
 'CONTROL MODE CAN BE CHANGED FROM THE MENU.',
 'CREDITS CAN BE OPENED FROM THE MAIN MENU.',
 'MAYUMI ALINGAROG INSPIRED THIS JAM PROJECT.',
 'THE DETECTIVE YOU CHOOSE CHANGES HER VISUAL IDENTITY.',
 'YUMI IS THE INTELLIGENCE-FOCUSED DETECTIVE.',
 'MAY IS THE FAST INVESTIGATION DETECTIVE.',
 'JULIA IS THE BALANCED FIELD DETECTIVE.',
 'THE STORY CAN BE COMPLETED WITH ANY DETECTIVE.',
 'THE FIRST SCENE ALWAYS STARTS INSIDE CELL A-17.',
 'CELL A-17 BELONGS TO CELL BLOCK A.',
 'THE CELL DOOR MUST BE UNLOCKED BEFORE THE ESCAPE ROUTE OPENS.',
 'THE DOCK OBJECTIVE IS MORE IMPORTANT THAN OPTIONAL LOOT.',
 'SEARCH THE MEDICAL WING BEFORE GOING TO THE DOCK.',
 'THE FERRY SIGNAL IS VISIBLE FROM THE DOCK.',
 'WAIT FOR THE BOARDING PROMPT.',
 'SAN FRANCISCO OPENS AFTER THE FERRY TRANSITION.',
 'TALK TO TWO DIFFERENT SURVIVORS.',
 'THE THIRD SURVIVOR IS OPTIONAL FOR THE SIMPLE GOAL.',
 'THE EMERGENCY SHELTER IS THE CITY SAFE ENDPOINT.',
 'THE ARCHIVE CAN REVEAL EXTRA STORY INFORMATION.',
 'THE FOURTH WALL CAN NOTICE WHEN YOU LEAVE THE TAB.',
 'THE FOURTH WALL CAN NOTICE LONG IDLE PERIODS.',
 'THE FOURTH WALL IS FICTIONAL.',
 'THE GAME DOES NOT READ PRIVATE FILES.',
 'THE GAME DOES NOT READ PASSWORDS.',
 'THE GAME DOES NOT READ CONTACTS.',
 'THE GAME DOES NOT READ ACCOUNT CONTENTS.',
 'CAMERA AND MICROPHONE REQUIRE PERMISSION.',
 'LOCATION REQUIRES PERMISSION.',
 'SERVER-SEEN IP MAY BE A PROXY ADDRESS.',
 'THE NIGHTWATCH DEVICE PANEL IS PART OF THE GAME.',
 'THE PRISON HAS ONLY A FEW SKELETONS.',
 'ENVIRONMENTAL WRITING IS USED AS NAVIGATION.',
 'BLOOD MARKS CAN LEAD TOWARD IMPORTANT AREAS.',
 'WINDOW LIGHTS HELP YOU READ THE STREET.',
 'PUDDLES ADD VISUAL DEPTH TO THE ROAD.',
 'PIXEL DETAIL IS DENSEST NEAR THE PLAYER.',
 'BACKGROUND BUILDINGS MOVE AT A DIFFERENT PARALLAX.',
 'THE CAMERA SMOOTHLY FOLLOWS THE DETECTIVE.',
 'THE PLAYER HAS ACCELERATION AND FRICTION.',
 'JUMPING USES COYOTE TIME.',
 'JUMPING USES A SMALL INPUT BUFFER.',
 'LANDING CREATES A DUST EFFECT.',
 'RUNNING CHANGES FOOTSTEP TIMING.',
 'SHOOTING CREATES RECOIL.',
 'MELEE PUSHES INFECTED BACK.',
 'THE FLASHLIGHT IS A VISUAL TOOL, NOT A WEAPON.',
 'THE HORROR SYSTEM USES SANITY TO SCALE TENSION.',
 'THE SMILER CAN APPEAR AT THE EDGE OF THE VIEW.',
 'THE SMILER DOES NOT NEED TO CHASE YOU TO BE SCARY.',
 'A JUMPSCARE SHOULD FEEL LIKE AN EVENT.',
 'QUIET MOMENTS ARE PART OF THE HORROR DESIGN.',
 'THE PLAYER SHOULD ALWAYS HAVE A CLEAR NEXT STEP.',
 'THE OBJECTIVE PANEL EXPLAINS THE STEPS.',
 'THE GAME IS DESIGNED FOR A JAM RUN, NOT A GRIND.',
 'EXPLORE FOR STORY, NOT ONLY FOR LOOT.',
 'THE DOCK IS THE ESCAPE ROUTE.',
 'THE SHELTER IS THE SURVIVOR ROUTE.',
 'THE RAIN NEVER MEANS THE POWER IS OFF OUTSIDE.',
 'THE ISLAND REMAINS VISIBLE AFTER YOU LEAVE CELL A-17.',
 'CELL BLOCK A DOES NOT DISAPPEAR.',
 'BUILDINGS HAVE CLEAR DOORS.',
 'INTERIORS HAVE CLEAR EXIT ZONES.',
 'THE WORLD IS BUILT TO BE READ AT A GLANCE.',
 'LOOK FOR SIGNS.',
 'LISTEN FOR FOOTSTEPS.',
 'WATCH THE WINDOWS.',
 'TRUST YOUR OBJECTIVE.',
 'DO NOT TRUST EVERYTHING ELSE.'
];
const objectives=[
 {title:'FIND THE DOCKS',steps:['Leave Cell A-17 and follow the prison signs.','Search the Medical Wing for the Dock Pass.','Reach the dock beacon.']},
 {title:'ESCAPE THE ISLAND',steps:['Use the Dock Pass at the ferry beacon.','Light the beacon and wait for the boat.','Board the ferry when the prompt appears.']},
 {title:'FIND 2 SURVIVORS',steps:['Explore San Francisco after the ferry arrives.','Talk to a survivor with E / USE.','Find a second survivor.']}
];
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function dist(a,b){return Math.abs(a-b);}
function px(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));}
function line(x1,y1,x2,y2,c,w=1){ctx.strokeStyle=c;ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(Math.round(x1),Math.round(y1));ctx.lineTo(Math.round(x2),Math.round(y2));ctx.stroke();}
function poly(points,c){ctx.fillStyle=c;ctx.beginPath();ctx.moveTo(points[0][0],points[0][1]);for(let i=1;i<points.length;i++)ctx.lineTo(points[i][0],points[i][1]);ctx.closePath();ctx.fill();}
function text(t,x,y,size=12,color='#ddd',align='left'){ctx.font=`${size}px Consolas`;ctx.fillStyle=color;ctx.textAlign=align;ctx.fillText(t,Math.round(x),Math.round(y));}
function seeded(n){const s=Math.sin(n*12.9898)*43758.5453;return s-Math.floor(s);}
function noise2(x,y){return seeded(x*17.13+y*91.71);}
function show(id){const e=document.getElementById(id);if(e)e.classList.remove('hidden');}
function hide(id){const e=document.getElementById(id);if(e)e.classList.add('hidden');}
function setMessage(t,time=2){const e=document.getElementById('message');if(!e)return;e.textContent=t;e.classList.remove('hidden');messageTimer=time;}
function showWarning(t){const e=document.getElementById('warningText');if(!e)return;e.textContent=t;e.style.opacity='1';horror.warning=2.4;}
function safeAudio(){try{if(!audioCtx){audioCtx=new(window.AudioContext||window.webkitAudioContext)();masterGain=audioCtx.createGain();musicGain=audioCtx.createGain();sfxGain=audioCtx.createGain();rainGain=audioCtx.createGain();masterGain.gain.value=.92;musicGain.gain.value=.28;sfxGain.gain.value=.95;rainGain.gain.value=.21;musicGain.connect(masterGain);sfxGain.connect(masterGain);rainGain.connect(masterGain);masterGain.connect(audioCtx.destination);}if(audioCtx.state==='suspended')audioCtx.resume();return audioCtx;}catch(e){return null;}}
function tone(freq,duration,type='sine',volume=.08,slide=0,group='sfx'){if(!soundEnabled)return;const ac=safeAudio();if(!ac)return;const t=ac.currentTime;const o=ac.createOscillator();const g=ac.createGain();o.type=type;o.frequency.setValueAtTime(Math.max(20,freq),t);if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(20,freq+slide),t+duration);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(volume,t+.012);g.gain.exponentialRampToValueAtTime(.0001,t+duration);o.connect(g);g.connect(group==='music'?musicGain:sfxGain);o.start(t);o.stop(t+duration+.03);}
function noiseBurst(duration=.16,volume=.08,group='sfx'){if(!soundEnabled)return;const ac=safeAudio();if(!ac)return;const buffer=ac.createBuffer(1,ac.sampleRate*duration,ac.sampleRate);const data=buffer.getChannelData(0);for(let i=0;i<data.length;i++)data[i]=(Math.random()*2-1)*Math.pow(1-i/data.length,1.8);const src=ac.createBufferSource();const g=ac.createGain();src.buffer=buffer;g.gain.value=volume;src.connect(g);g.connect(group==='rain'?rainGain:sfxGain);src.start();}
function startSoundscape(){if(musicStarted||!soundEnabled)return;safeAudio();if(!audioCtx)return;musicStarted=true;rainStarted=true;tone(46,2.4,'sine',.018,7,'music');tone(69,2.8,'triangle',.012,-8,'music');setInterval(()=>{if(!soundEnabled||!musicStarted||!audioCtx)return;tone(state.sanity<55?38:49,2.2,'sine',.014,Math.random()<.5?4:-4,'music');if(Math.random()<.45)tone(92,1.2,'triangle',.008,-7,'music');},2100);setInterval(()=>{if(scene==='play'&&!interior&&soundEnabled)noiseBurst(.045,.012,'rain');},260);}
function soundStep(){tone(player.vx>210?95:70,.065,'square',.06,-18);noiseBurst(.025,.025);}
function soundChest(){tone(125,.13,'square',.16,70);setTimeout(()=>tone(265,.18,'sine',.11,45),75);setTimeout(()=>tone(420,.22,'triangle',.07,0),145);}
function soundDoor(){tone(55,.24,'square',.08,18);noiseBurst(.09,.04);}
function soundJump(){tone(190,.16,'triangle',.09,75);}
function soundLand(){tone(54,.1,'sine',.07,-18);noiseBurst(.04,.035);}
function soundShot(){tone(420,.06,'square',.14,-240);noiseBurst(.045,.12);}
function soundReload(){tone(160,.08,'square',.08,40);setTimeout(()=>tone(110,.09,'square',.07,-25),90);}
function soundScare(){tone(67,.68,'sawtooth',.32,-46);setTimeout(()=>tone(41,.9,'square',.2,-10),90);setTimeout(()=>noiseBurst(.5,.18),120);}
function randomHorrorAudio(){if(!soundEnabled)return;tone(35,.4,'sine',.018,-4);if(Math.random()<.5)setTimeout(()=>tone(730,.16,'sine',.018,-260),130);}
function resetWorld(){state.health=100;state.maxHealth=100;state.stamina=100;state.maxStamina=100;state.sanity=100;state.hunger=100;state.ammo=12;state.reserveAmmo=36;state.grenades=2;state.light=true;state.battery=100;state.medkits=1;state.bandages=2;state.scrap=2;state.startKey=false;state.startEscaped=false;state.dockPass=false;state.beacon=false;state.boatEscaped=false;state.survivors=0;state.archiveKey=false;state.inventory={bandage:2,food:2,scrap:2,ammo_9mm:36};camera=0;objectiveIndex=0;goalFocus='escape';interior=null;interiorFloor=1;smiler={active:false,timer:0,cooldown:14,x:0,intensity:0,variant:0};horror={flash:0,shake:0,warning:0,heartbeat:0,glitch:0,blackout:0};currentChest=null;particles=[];footprints=[];shotTracers=[];survivors=[];zombies=[];chests=[];buildings=[];cells=[];buildMap();player.x=720;player.y=GROUND-player.h;player.vx=0;player.vy=0;player.onGround=true;player.doubleJump=true;player.coyote=0;player.jumpBuffer=0;player.anim=0;player.stepTimer=0;player.landTimer=0;player.recoil=0;player.hitTimer=0;chapter='ALCATRAZ';setObjective();}
function buildMap(){
 buildings=[
  {id:'cellA',x:650,w:980,name:'CELL BLOCK A',type:'prison',floors:2},
  {id:'cellB',x:1740,w:900,name:'CELL BLOCK B',type:'prison',floors:2},
  {id:'guard',x:2720,w:420,name:'GUARD STATION',type:'station',floors:2},
  {id:'medical',x:3260,w:620,name:'MEDICAL WING',type:'medical',floors:2},
  {id:'workshop',x:4040,w:420,name:'WORKSHOP',type:'workshop',floors:1},
  {id:'dock',x:4570,w:400,name:'DOCK OFFICE',type:'dock',floors:2},
  {id:'police',x:600,w:620,name:'POLICE STATION',type:'police',floors:2},
  {id:'hospital',x:1520,w:680,name:'SAN FRANCISCO HOSPITAL',type:'hospital',floors:3},
  {id:'funeral',x:2480,w:520,name:'MERCY FUNERAL HOME',type:'funeral',floors:2},
  {id:'hotel',x:3350,w:620,name:'OLD HOTEL',type:'hotel',floors:4},
  {id:'shelter',x:4400,w:650,name:'EMERGENCY SHELTER',type:'shelter',floors:2},
  {id:'research',x:5350,w:760,name:'ECLIPSE RESEARCH ANNEX',type:'research',floors:3}
 ];
 cells=[];for(let i=0;i<20;i++){const block=i<10?'A':'B';const index=i%10;cells.push({id:`${block}-${index+1}`,x:(block==='A'?735:1825)+index*82,y:GROUND-110,w:66,h:110});}
 chests=[
  {id:'a17',x:720,y:GROUND-40,inside:false,building:'cellA',items:[{id:'key',name:'BRASS KEY',count:1}],opened:false},
  {id:'medicalPass',x:690,y:455,inside:true,building:'medical',items:[{id:'dockPass',name:'DOCK PASS',count:1},{id:'bandage',name:'BANDAGE',count:1},{id:'ammo',name:'9MM AMMO',count:8}],opened:false,important:true},
  {id:'medicalInside',x:120,y:430,inside:true,building:'medical',items:[{id:'medkit',name:'MEDKIT',count:1},{id:'ammo',name:'9MM AMMO',count:10}],opened:false},
  {id:'workshopInside',x:900,y:430,inside:true,building:'workshop',items:[{id:'ammo',name:'9MM AMMO',count:8},{id:'scrap',name:'SCRAP',count:3}],opened:false},
  {id:'shelterInside',x:500,y:430,inside:true,building:'shelter',items:[{id:'bandage',name:'BANDAGE',count:2},{id:'food',name:'CANNED FOOD',count:2}],opened:false},
  {id:'researchInside',x:650,y:430,inside:true,building:'research',items:[{id:'medkit',name:'MEDKIT',count:1},{id:'ammo',name:'9MM AMMO',count:12}],opened:false}
 ];
 survivors=[{id:'mara',name:'MARA',x:4780,found:false,talked:false},{id:'eli',name:'ELI',x:5660,found:false,talked:false},{id:'noah',name:'NOAH',x:6520,found:false,talked:false}];
 zombies=[];for(let i=0;i<16;i++){zombies.push({x:800+i*300+(i%3)*70,type:i%5===0?'brute':i%4===0?'runner':'walker',hp:i%5===0?150:70,dead:false,phase:i*.63,attack:0});}
}
function startGame(name){selectedCharacter=name;resetWorld();positionInsideCell();scene='intro';introIndex=0;introTimer=0;hide('characterMenu');hide('mainMenu');hide('controlsOverlay');hide('hud');hide('cutscene');startSoundscape();updateIntroText();}
function positionInsideCell(){interior={id:'cellA',name:'CELL A-17',type:'cell',building:{id:'cellA',name:'CELL BLOCK A',type:'prison',floors:2}};player.x=310;player.y=GROUND-70;state.startEscaped=false;}
function updateControlUI(){document.querySelectorAll('[data-control]').forEach(b=>b.classList.toggle('selected',b.dataset.control===controlMode));const s=document.getElementById('controlStatus');if(s)s.textContent=`ACTIVE: ${controlMode==='laptop'?'LAPTOP / DESKTOP':controlMode==='mobile'?'MOBILE / TOUCH':'AUTO DETECT'}`;document.getElementById('mobileControls').classList.toggle('hidden',controlMode!=='mobile');}
function setControlMode(v){if(v==='auto')v=/Android|iPhone|iPad|iPod|Mobi/i.test(navigator.userAgent)?'mobile':'laptop';controlMode=v;updateControlUI();}
function setObjective(){let idx=objectiveIndex;if(chapter==='SAN FRANCISCO')idx=2;const o=objectives[idx];const currentStep=chapter==='ALCATRAZ'?getAlcatrazStep():getSFStep();const next=o.steps[Math.min(currentStep,o.steps.length-1)];const e=document.getElementById('objective');if(e)e.textContent=`OBJECTIVE  ${o.title}\nNEXT STEP  ${next}`;renderObjectives();}
function getAlcatrazStep(){if(!state.startEscaped)return 0;if(!state.dockPass)return 1;if(!state.beacon)return 2;return 2;}
function getSFStep(){return state.survivors>=2?2:1;}
function renderObjectives(){const list=document.getElementById('objectiveList');if(!list)return;list.innerHTML='';objectives.forEach((o,i)=>{const item=document.createElement('div');item.className='objectiveItem '+(i<objectiveIndex?'done ':'')+(i===objectiveIndex?'current':'');let stateText=i<objectiveIndex?'✓ COMPLETE':i===objectiveIndex?'› CURRENT':'○ FUTURE';let steps=o.steps.map((s,k)=>`<span class="step">${k+1}. ${s}</span>`).join('');item.innerHTML=`<b>${stateText}</b><div style="margin-top:6px">${o.title}</div>${steps}`;list.appendChild(item);});}
function advanceObjective(i){if(i>objectiveIndex)objectiveIndex=Math.min(2,i);setObjective();}
function transitionTo(target,callback){if(fadeBusy)return;fadeBusy=true;fadeTimer=0;const f=document.getElementById('fade');f.style.opacity='1';transitionTarget=target;setTimeout(()=>{callback();f.style.opacity='0';setTimeout(()=>{fadeBusy=false;},650);},620);}
function enterBuilding(b){if(chapter==='ALCATRAZ'&&b.id==='cellA'&&!state.startEscaped){setMessage('The cell is already inside Cell Block A.');return;}transitionTo('enter',()=>{interior={id:b.id,name:b.name,type:b.type,building:b};interiorFloor=1;player.x=640;player.y=GROUND-120;player.vx=0;player.vy=0;scene='play';soundDoor();setMessage(`Entered ${b.name}.`,1.5);});}
function exitBuilding(){if(!interior)return;const b=interior.building;transitionTo('exit',()=>{const exitX=b.x+b.w+35;player.x=chapter==='ALCATRAZ'?clamp(exitX,80,worldWidth.ALCATRAZ-80):clamp(exitX,80,worldWidth.SF-80);player.y=GROUND-player.h;player.vx=0;player.vy=0;interior=null;scene='play';soundDoor();setMessage(`Back outside — ${b.name}.`,1.5);});}
function searchStartingCell(){if(state.startKey){setMessage('The mattress is empty.',1);return;}state.startKey=true;state.inventory.key=1;chests[0].opened=true;setMessage('You found a brass key under the mattress.');soundChest();setObjective();}
function unlockCell(){if(!state.startKey){setMessage('The door is locked. Search beneath the mattress.',1.7);return;}if(state.startEscaped){setMessage('Cell A-17 is open.',1);return;}state.startEscaped=true;interior=null;player.x=830;player.y=GROUND-player.h;objectiveIndex=0;setMessage('CELL A-17 UNLOCKED. Leave Cell Block A and find the docks.');soundDoor();soundScare();horror.flash=.45;setObjective();}
function interact(){if(scene!=='play'||fadeBusy)return;if(currentChest){openChest(currentChest);return;}if(interior){if(Math.abs(player.x-640)<95&&Math.abs(player.y-(GROUND-120))<100){exitBuilding();return;}for(const c of chests){if(!c.inside||c.building!==interior.id)continue;if(Math.abs(player.x-c.x)<90){openChest(c);return;}}if(interior.id==='cellA'&&!state.startKey&&Math.abs(player.x-310)<80){searchStartingCell();return;}if(interior.id==='cellA'&&!state.startEscaped&&Math.abs(player.x-610)<110){unlockCell();return;}return;}if(chapter==='ALCATRAZ'){if(!state.startEscaped&&player.x>270&&player.x<870){setMessage('You are still inside Cell Block A.',1);return;}for(const b of buildings.filter(x=>x.x<worldWidth.ALCATRAZ)){const door=b.x+b.w*.5;if(Math.abs(player.x-door)<130){if(b.id==='medical'){setMessage('MEDICAL WING — SUPPLY DESK AHEAD.');}enterBuilding(b);return;}}if(!state.dockPass&&player.x>3240&&player.x<3880){setMessage('The Medical Wing is this building. Find the Dock Pass.');return;}if(Math.abs(player.x-4850)<180){if(!state.dockPass){setMessage('The ferry will not accept you without the Dock Pass.');return;}if(!state.beacon){state.beacon=true;advanceObjective(1);setMessage('BEACON LIT. The ferry is coming.');tone(260,.6,'sine',.12,100);return;}if(state.beacon&&!state.boatEscaped){state.boatEscaped=true;transitionTo('ferry',()=>{chapter='SAN FRANCISCO';player.x=120;player.y=GROUND-player.h;interior=null;advanceObjective(2);setMessage('You made it to San Francisco. Find 2 survivors.',2);spawnSFZombies();});return;}}}else{for(const b of buildings){const door=b.x+b.w*.5;if(Math.abs(player.x-door)<135){enterBuilding(b);return;}}for(const s of survivors){if(s.found)continue;if(Math.abs(player.x-s.x)<90){s.found=true;s.talked=true;state.survivors++;setMessage(`${s.name}: You found me. Stay close.`,2);tone(320,.18,'sine',.09,80);if(state.survivors>=2){advanceObjective(2);setMessage('TWO SURVIVORS FOUND. GET TO THE EMERGENCY SHELTER.',2);}return;}}if(state.survivors>=2&&Math.abs(player.x-4720)<180){endingTriggered=true;scene='ending';show('ending');document.getElementById('endingText').textContent='Two survivors made it into the shelter. The ferry vanished behind the rain. But on the last CCTV frame, a tall figure was still standing on the island.';}}
}
function spawnSFZombies(){zombies=[];for(let i=0;i<20;i++)zombies.push({x:380+i*340,type:i%6===0?'brute':i%4===0?'runner':'walker',hp:i%6===0?180:70,dead:false,phase:i*.43,attack:0});}
function nearestChest(){if(interior){let best=null,d=99999;for(const c of chests){if(!c.inside||c.building!==interior.id)continue;const dd=dist(player.x,c.x);if(dd<d){d=dd;best=c;}}return d<100?best:null;}let best=null,d=99999;for(const c of chests){if(c.inside)continue;const dd=dist(player.x,c.x);if(dd<d){d=dd;best=c;}}return d<100?best:null;}
function openChest(c){if(!c)return;currentChest=c;scene='inventory';show('inventoryUi');renderChest();soundChest();if(c.id==='medicalPass'&&!c.opened){setMessage('DOCK PASS FOUND. The dock should be easier to reach now.');}c.opened=true;}
function renderChest(){if(!currentChest)return;const cg=document.getElementById('chestSlots'),pg=document.getElementById('playerSlots');cg.innerHTML='';pg.innerHTML='';for(let i=0;i<27;i++){const item=currentChest.items[i];cg.appendChild(makeSlot(item,currentChest,i));}const inv=Object.entries(state.inventory);for(let i=0;i<27;i++){const item=inv[i];pg.appendChild(makeSlot(item,null,i));}document.getElementById('chestFooter').textContent=currentChest.items.length?`${currentChest.items.length} item type(s) remain.`:'CHEST EMPTY';}
function makeSlot(item,owner,index){const b=document.createElement('button');b.className='slot';if(item){const div=document.createElement('div');div.className='slotIcon';div.style.background=itemColor(item.id||item[0]);b.appendChild(div);const label=document.createElement('div');label.textContent=item.name||item[0].replaceAll('_',' ').toUpperCase();b.appendChild(label);const count=document.createElement('div');count.className='slotCount';count.textContent=item.count??item[1];b.appendChild(count);b.onclick=()=>{if(owner){takeItem(owner,index);}};}return b;}
function itemColor(id){return({key:'#c9a85c',dockPass:'#c0a06b',bandage:'#8a4644',ammo:'#bda75b',medkit:'#c8c6bc',food:'#6f6c57',scrap:'#858989'})[id]||'#746b5b';}
function takeItem(chest,index){const item=chest.items[index];if(!item)return;const id=item.id;state.inventory[id]=Number(state.inventory[id]||0)+Number(item.count||1);if(id==='key')state.startKey=true;if(id==='dockPass')state.dockPass=true;chest.items.splice(index,1);if(id==='dockPass'){advanceObjective(0);setMessage('DOCK PASS ADDED TO INVENTORY.',1.4);soundChest();}renderChest();}
function takeAll(){if(!currentChest)return;const snapshot=currentChest.items.slice();for(const item of snapshot){takeItem(currentChest,currentChest.items.indexOf(item));}renderChest();}
function sortChest(){if(!currentChest)return;currentChest.items.sort((a,b)=>a.name.localeCompare(b.name));renderChest();tone(210,.08,'triangle',.06,40);}
function closeChest(){if(scene==='inventory'){scene='play';hide('inventoryUi');currentChest=null;}}
function tryJump(){player.jumpBuffer=.13;}
function physics(dt){if(scene!=='play'||fadeBusy)return;const left=inputState.left||keys.has('a')||keys.has('ArrowLeft');const right=inputState.right||keys.has('d')||keys.has('ArrowRight');const run=inputState.run||keys.has('Shift');const dir=(right?1:0)-(left?1:0);let maxSpeed=run?290:205;if(interior)maxSpeed*=.92;if(state.stamina<18)maxSpeed*=.78;const accel=dir?1450:1850;if(dir){player.vx=lerp(player.vx,dir*maxSpeed,Math.min(1,accel*dt/Math.max(1,maxSpeed)));player.facing=dir;}else player.vx=lerp(player.vx,0,Math.min(1,1650*dt/Math.max(1,maxSpeed)));player.coyote=player.onGround?.12:Math.max(0,player.coyote-dt);player.jumpBuffer=Math.max(0,player.jumpBuffer-dt);if((inputState.jump||keys.has('w')||keys.has(' ')||keys.has('ArrowUp'))&&!player.jumpBuffer)player.jumpBuffer=.1;if(player.jumpBuffer>0&&(player.onGround||player.coyote>0||player.doubleJump)){const second=!player.onGround;if(second&&player.doubleJump)player.doubleJump=false;player.vy=second?-390:-480;player.onGround=false;player.coyote=0;player.jumpBuffer=0;inputState.jump=false;keys.delete('w');keys.delete(' ');keys.delete('ArrowUp');soundJump();spawnDust(player.x+player.w/2,GROUND-2,7);}player.vy+=1320*dt;const wasGround=player.onGround;player.x+=player.vx*dt;player.y+=player.vy*dt;if(player.y+player.h>=GROUND){player.y=GROUND-player.h;player.vy=0;player.onGround=true;if(!wasGround){player.landTimer=.2;soundLand();spawnDust(player.x+player.w/2,GROUND-2,9);}}else player.onGround=false;if(!dir&&player.onGround)player.stamina=Math.min(state.maxStamina,state.stamina+12*dt);else if(run&&dir)state.stamina=Math.max(0,state.stamina-22*dt);else state.stamina=Math.min(state.maxStamina,state.stamina+4*dt);state.hunger=Math.max(0,state.hunger-.035*dt);if(state.hunger<=0)state.health=Math.max(0,state.health-.4*dt);player.anim+=dt*(Math.abs(player.vx)>15?Math.abs(player.vx)/34:1.2);player.stepTimer-=dt;if(player.onGround&&Math.abs(player.vx)>70&&player.stepTimer<=0){player.stepTimer=player.vx>210?.23:.34;soundStep();footprints.push({x:player.x+player.w/2,y:GROUND-3,t:2.2,side:player.facing});if(footprints.length>40)footprints.shift();spawnDust(player.x+player.w/2,GROUND-3,3);}player.recoil=Math.max(0,player.recoil-dt*4);if(player.hitTimer>0)player.hitTimer-=dt;const maxW=worldWidth[chapter];if(interior)player.x=clamp(player.x,55,W-90);else player.x=clamp(player.x,40,maxW-70);const desired=interior?0:clamp(player.x-W*.42,0,maxW-W);camera=lerp(camera,desired,Math.min(1,dt*5));}
function updateInteractables(dt){currentChest=nearestChest();if(chapter==='ALCATRAZ'&&!interior&&state.startEscaped&&player.x>3200&&player.x<3920&&!state.dockPass)setObjective();if(chapter==='ALCATRAZ'&&state.startEscaped&&state.dockPass&&!state.beacon)objectiveIndex=1;if(chapter==='SAN FRANCISCO')objectiveIndex=2;setObjective();}
function updateZombies(dt){for(const z of zombies){if(z.dead)continue;z.attack=Math.max(0,z.attack-dt);const dx=player.x-z.x;if(Math.abs(dx)<740&&!interior){z.x+=Math.sign(dx)*(z.type==='runner'?66:z.type==='brute'?25:42)*dt;const d=dist(player.x,z.x);if(d<54&&z.attack<=0){state.health=Math.max(0,state.health-(z.type==='brute'?18:8));player.hitTimer=.3;horror.shake=7;z.attack=1.15;soundHit();spawnBlood(player.x,GROUND-38,8);if(state.health<=0)die('The infected finally caught you.');}}}}
function soundHit(){tone(90,.1,'sawtooth',.08,-40);}
function updateSurvivors(dt){for(const s of survivors){if(s.found)s.x=lerp(s.x,player.x+(-80+Math.sin(totalTime+s.x)*18),dt*.8);}}
function updateSmiler(dt){if(scene!=='play'||interior)return;smiler.cooldown-=dt;if(smiler.active){smiler.timer-=dt;smiler.intensity=Math.min(1,smiler.intensity+dt*2);state.sanity=Math.max(0,state.sanity-.22*dt);if(smiler.timer<=0){smiler.active=false;smiler.intensity=0;smiler.cooldown=20+Math.random()*35;}}else if(smiler.cooldown<=0){const threshold=state.sanity<65?.0018:state.sanity<85?.0008:.00025;if(Math.random()<dt*threshold){smiler.active=true;smiler.timer=2+Math.random()*3.5;smiler.x=clamp(player.x+(Math.random()<.5?-1:1)*(450+Math.random()*280),80,worldWidth[chapter]-90);smiler.intensity=0;soundScare();showWarning('SOMETHING IS WATCHING YOU');horror.shake=5;horror.flash=.4;}}}
function updateHorror(dt){horror.flash=Math.max(0,horror.flash-dt*2.5);horror.shake=Math.max(0,horror.shake-dt*8);horror.warning=Math.max(0,horror.warning-dt);horror.heartbeat=Math.max(0,horror.heartbeat-dt*2);horror.glitch=Math.max(0,horror.glitch-dt*1.8);if(horror.warning<=0){const e=document.getElementById('warningText');if(e)e.style.opacity='0';}if(scene==='play'){scareTimer-=dt;if(scareTimer<=0&&state.sanity<92){scareTimer=18+Math.random()*32;const chance=state.sanity<45?.15:.055;if(Math.random()<chance)triggerJumpscare();}if(state.sanity<55&&Math.random()<dt*.0012){horror.glitch=.8;showWarning(Math.random()<.5?'DO NOT LOOK AT THE WINDOWS':'YOU HEARD THAT TOO');randomHorrorAudio();}}}
function triggerJumpscare(){if(scene!=='play')return;horror.flash=.9;horror.shake=18;showWarning('RUN');soundScare();const e=document.getElementById('scare');e.classList.add('show');setTimeout(()=>e.classList.remove('show'),520);}
function update(dt){if(scene==='intro'){introTimer+=dt;if(introTimer>4.4)advanceIntro();return;}if(scene==='menu'){return;}if(scene==='pause'||scene==='inventory'||scene==='ending'||scene==='death')return;if(scene==='play'){physics(dt);updateInteractables(dt);updateZombies(dt);updateSurvivors(dt);updateSmiler(dt);updateHorror(dt);if(state.battery>0&&state.light)state.battery=Math.max(0,state.battery-.15*dt);if(state.sanity<=0)die('You could no longer tell what was real.');}}
function drawSky(){const sf=chapter==='SAN FRANCISCO';const g=ctx.createLinearGradient(0,0,0,430);g.addColorStop(0,sf?'#061018':'#071015');g.addColorStop(.55,sf?'#122029':'#14252a');g.addColorStop(1,sf?'#263538':'#263738');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);for(let i=0;i<90;i++){const x=((i*127-camera*.1)%W+W)%W;const y=35+(i*49)%300;px(x,y,1+(i%3),1+(i%2),i%11===0?'#79858b':'#29353a');}for(let i=0;i<9;i++){const x=((i*185-camera*.05)%W+W)%W;const h=60+(i%5)*25;px(x,352-h,110,h,sf?'#141b20':'#182428');for(let q=0;q<4;q++){if((i+q)%3===0)px(x+15+q*22,370-h,8,12,'#6b654c');}}if(sf){drawGoldenGate();}}
function drawGoldenGate(){const x=720-camera*.05;line(x,355,x+780,355,'#3b4548',6);line(x+130,355,x+130,192,'#3f4a4d',12);line(x+660,355,x+660,208,'#3f4a4d',12);for(let i=0;i<16;i++){const t=i/15;const xx=x+144+t*500;const yy=202+Math.sin(t*Math.PI)*105;line(xx,yy,xx,350,'#2a3235',1);}}
function drawOcean(){if(chapter!=='ALCATRAZ')return;ctx.fillStyle='#0d1d23';ctx.fillRect(0,365,W,74);for(let i=0;i<50;i++){const x=((i*71-camera*.2)%W+W)%W;const y=375+(i%6)*9;line(x,y,x+16,y,'#2a4048',1);line(x+25,y+4,x+39,y+4,'#1d3036',1);}}
function drawGround(){ctx.fillStyle=chapter==='ALCATRAZ'?'#414948':'#474a49';ctx.fillRect(0,430,W,290);ctx.fillStyle='#303837';ctx.fillRect(0,568,W,152);for(let i=0;i<320;i++){const x=((i*67-camera*.9)%W+W)%W;const y=445+(i*41)%250;px(x,y,1+(i%4),1+(i%2),i%6===0?'#656863':i%3===0?'#505653':'#2d3333');}for(let i=0;i<16;i++){const x=(i*181-camera*.7)%W;px(x,620,74,5,'#80817a');px(x+9,627,42,3,'#282d2d');}}
function drawBuildings(){for(const b of buildings){if(chapter==='ALCATRAZ'&&b.id.startsWith('sf'))continue;if(chapter==='SAN FRANCISCO'&&['cellA','cellB','guard','medical','workshop','dock'].includes(b.id))continue;const x=b.x-camera;if(x<-b.w-100||x>W+100)continue;const h=b.type==='prison'?260:b.floors*102+80;const palette={prison:'#454d4e',station:'#424b50',medical:'#526063',workshop:'#4b4e4d',dock:'#4a4d49',police:'#48545a',hospital:'#526064',funeral:'#48474a',hotel:'#505252',shelter:'#4d5450',research:'#4e555a'};const body=palette[b.type]||'#4b5150';px(x,GROUND-h,b.w,h,body);px(x,GROUND-h,b.w,8,'#6e7572');px(x+9,GROUND-h+15,b.w-18,5,'#2e3435');for(let f=0;f<b.floors;f++){const fy=GROUND-78-f*102;for(let q=0;q<Math.max(2,Math.floor((b.w-50)/46));q++){const wx=x+25+q*46;const lit=(q+f+Math.floor(b.x/90))%5===0;px(wx,fy-34,26,26,lit?'#746d55':'#192124');if(lit){px(wx+5,fy-29,5,8,'#b7a06a');px(wx+15,fy-29,5,8,'#947d54');}}}px(x+b.w/2-28,GROUND-72,56,72,'#111718');px(x+b.w/2+17,GROUND-43,5,5,'#c5aa69');if(b.type==='medical'){px(x+b.w/2-76,GROUND-h+17,152,32,'#5f6e70');px(x+b.w/2-8,GROUND-h+21,16,22,'#e6e8df');px(x+b.w/2-22,GROUND-h+28,44,8,'#e6e8df');text('MEDICAL WING',x+b.w/2,GROUND-h+62,10,'#e4ded1','center');}if(b.type==='police'){text('POLICE',x+25,GROUND-h+34,13,'#ece5d8');}if(b.type==='funeral'){text('MERCY FUNERAL',x+35,GROUND-h+34,11,'#ddd4c5');}if(b.type==='research'){text('ECLIPSE RESEARCH ANNEX',x+b.w/2,GROUND-h+35,10,'#ded9ce','center');}}
}
function drawAlcatrazStructures(){if(chapter!=='ALCATRAZ')return;const x=650-camera;px(x,GROUND-255,980,255,'#3f4849');px(x,GROUND-255,980,10,'#777e7b');for(let i=0;i<13;i++){const xx=x+20+i*75;px(xx,GROUND-225,7,220,'#1d2425');}text('CELL BLOCK A',x+30,GROUND-275,12,'#e3ded2');if(state.startEscaped){px(x+160,GROUND-90,105,90,'#121718');text('A-17',x+175,GROUND-105,9,'#c8c1af');}const bx=1740-camera;px(bx,GROUND-255,900,255,'#41494b');px(bx,GROUND-255,900,10,'#707876');text('CELL BLOCK B',bx+25,GROUND-274,12,'#ddd7ca');}
function drawStreetProps(){const lamps=[380,1120,1980,2860,3770,4660,5560,6520,7480];for(const wx of lamps){const x=wx-camera;if(x<-80||x>W+80)continue;px(x,GROUND-155,6,155,'#171d1e');px(x-10,GROUND-157,26,6,'#343a3b');px(x-7,GROUND-170,20,13,'#1b1f20');px(x-3,GROUND-171,12,4,'#cfbb77');}if(chapter==='SAN FRANCISCO'){for(let i=0;i<9;i++){const x=350+i*510-camera;if(x<-120||x>W+120)continue;const broken=i%4===0;px(x,GROUND-55,72,30,'#202526');px(x+8,GROUND-47,55,12,'#394043');px(x+13,GROUND-17,12,5,'#101314');px(x+48,GROUND-17,12,5,'#101314');if(!broken){px(x+15,GROUND-42,17,8,'#74736d');px(x+38,GROUND-42,17,8,'#74736d');}}}else{for(let i=0;i<13;i++){const x=190+i*380-camera;if(x<-100||x>W+100)continue;px(x,GROUND-21,66,10,'#1f2323');px(x+9,GROUND-32,48,11,'#393b37');}}
}
function drawSigns(){if(chapter!=='ALCATRAZ')return;const signs=[{x:2960,t:'MEDICAL WING →',c:'#d6d1be'},{x:3280,t:'MEDICAL WING',c:'#e8dfcd'},{x:4330,t:'DOCKS →',c:'#d3c8ad'}];for(const s of signs){const x=s.x-camera;if(x<-160||x>W+160)continue;px(x,GROUND-170,132,31,'#202625');px(x+5,GROUND-165,122,20,'#384340');text(s.t,x+66,GROUND-151,10,s.c,'center');}}
function drawDock(){if(chapter!=='ALCATRAZ'||interior)return;const x=4470-camera;px(x,GROUND-28,430,28,'#2b302e');for(let i=0;i<15;i++){px(x+i*28,GROUND-36,18,8,'#4b4942');px(x+i*28+5,GROUND-7,6,26,'#363936');}ctx.fillStyle='#0b161b';ctx.beginPath();ctx.moveTo(x+70,GROUND-40);ctx.lineTo(x+280,GROUND-40);ctx.lineTo(x+330,GROUND-10);ctx.lineTo(x+20,GROUND-10);ctx.closePath();ctx.fill();px(x+112,GROUND-96,148,7,'#3b4343');px(x+133,GROUND-91,8,51,'#353b3b');px(x+208,GROUND-91,8,51,'#353b3b');px(x+108,GROUND-101,165,5,'#555d5a');if(state.beacon){px(x+217,GROUND-172,9,73,'#d2bd78');px(x+209,GROUND-164,25,5,'#d2bd78');}text('FERRY',x+194,GROUND-111,11,'#d8cfbd','center');if(!state.dockPass)text('DOCK PASS REQUIRED',x+208,GROUND-145,9,'#9a8177','center');else if(!state.beacon)text('E USE: LIGHT BEACON',x+208,GROUND-145,9,'#e0d8c9','center');else text('E USE: BOARD FERRY',x+208,GROUND-145,9,'#e0d8c9','center');}
function drawMedicalMarker(){if(chapter!=='ALCATRAZ'||interior||state.dockPass)return;const x=3550-camera;px(x-10,GROUND-195,20,20,'#d4c79d');text('DOCK PASS',x,GROUND-170,11,'#efe5d2','center');text('MEDICAL SUPPLY DESK',x,GROUND-154,9,'#b4a996','center');}
function drawInterior(){if(!interior)return;ctx.fillStyle=interior.type==='cell'?'#2a3132':'#394445';ctx.fillRect(0,0,W,H);ctx.fillStyle='#4e5959';ctx.fillRect(0,70,W,8);for(let row=0;row<8;row++){const y=102+row*49;for(let col=0;col<18;col++){const x=col*74+(row%2)*37;line(x,y,x+50,y,'#606a67',1);line(x+50,y,x+50,y+28,'#1f2627',1);}}ctx.fillStyle='#262c2d';ctx.fillRect(0,520,W,200);for(let i=0;i<16;i++){px(i*82,534,53,5,'#48514e');}if(interior.type==='cell'){drawCellInterior();}else{drawRoomInterior();}}
function drawCellInterior(){px(0,500,W,20,'#505a56');px(78,355,250,145,'#3a4241');px(95,337,214,20,'#626762');px(105,315,160,24,'#181d1f');px(86,393,226,8,'#121718');px(470,260,92,240,'#101718');px(483,276,64,212,'#353d3d');for(let i=0;i<7;i++)px(495+i*7,285,4,195,'#6d7673');px(880,372,190,128,'#45403a');px(900,340,140,30,'#353e40');px(1130,350,90,150,'#404a4a');for(let i=0;i<6;i++)px(1140,372+i*21,67,5,'#67716e');text('CELL A-17',640,108,19,'#e4ddd0','center');text('SEARCH UNDER THE MATTRESS',640,132,10,'#a6aaa4','center');text('E  INTERACT WITH KEY / DOOR',640,155,9,'#b8b5ab','center');if(!state.startKey){const x=205,y=319;px(x,y,74,5,'#746f63');px(x+4,y-5,66,4,'#5a554d');}}
function drawRoomInterior(){px(105,360,220,145,'#4c504c');px(122,331,186,29,'#666a65');px(190,315,80,16,'#242927');px(830,392,180,113,'#4a4035');px(855,366,130,26,'#343d3f');px(1060,345,120,160,'#3b4545');for(let i=0;i<6;i++)px(1070,370+i*23,99,5,'#69736f');const b=interior.building;if(b&&b.type==='medical'){px(545,260,190,16,'#394244');px(567,230,145,30,'#4b5455');px(630,235,18,19,'#deded3');px(611,242,56,8,'#deded3');text('SUPPLY DESK',640,216,10,'#ded8cb','center');text('DOCK PASS IS HERE',640,199,12,'#eee3cc','center');}if(b&&b.type==='workshop'){px(410,392,300,18,'#4f4639');for(let i=0;i<7;i++)px(432+i*38,347,18,44,'#3c403c');}if(b&&b.type==='research'){px(390,290,470,34,'#21292a');for(let i=0;i<8;i++)px(420+i*53,337,32,74,i%3===0?'#647169':'#33403f');}text(b?b.name.toUpperCase():'INTERIOR',640,108,17,'#e6ddd0','center');text(`FLOOR ${interiorFloor} • E TO EXIT`,640,132,10,'#b3b9b4','center');text('E  EXIT',42,342,10,'#ddd6c6');text('E  EXIT',1150,342,10,'#ddd6c6');for(const c of chests){if(c.inside&&c.building===interior.id){px(c.x-28,c.y-28,56,28,c.opened?'#604b36':'#7d5b37');px(c.x-28,c.y-32,56,7,'#a37b4b');px(c.x-5,c.y-22,10,9,'#dbc06b');text('CHEST',c.x,c.y-40,9,'#d5ccb9','center');}}if(interior.id==='cellA'&&player.x<440&&!state.startKey)text('MATTRESS',205,290,9,'#cfc7b9','center');}
function drawFootprints(){for(const f of footprints){f.t-=.016;const a=clamp(f.t/2.2,0,1)*.35;ctx.save();ctx.globalAlpha=a;px(f.x-camera-5,f.y,10,3,'#1a1d1d');ctx.restore();}footprints=footprints.filter(f=>f.t>0);}
function drawParticles(){for(const p of particles){p.life-=.016;p.x+=p.vx*.016;p.y+=p.vy*.016;p.vy+=700*.016;ctx.globalAlpha=clamp(p.life/p.max,0,1);px(p.x-camera,p.y,p.s,p.s,p.c);}ctx.globalAlpha=1;particles=particles.filter(p=>p.life>0);}
function spawnDust(x,y,n=4){for(let i=0;i<n;i++)particles.push({x,y,vx:(Math.random()-.5)*55,vy:-Math.random()*65,s:1+Math.random()*3,life:.4+Math.random()*.3,max:.7,c:Math.random()<.5?'#77756e':'#4c514e'});}
function spawnBlood(x,y,n=5){for(let i=0;i<n;i++)particles.push({x,y,vx:(Math.random()-.5)*110,vy:-Math.random()*120,s:2+Math.random()*3,life:.5+Math.random()*.4,max:.9,c:'#8e3032'});}
function drawPlayer(){let x=player.x-camera,y=player.y;const t=player.anim;const speed=Math.abs(player.vx);const walking=player.onGround&&speed>15;const bob=player.onGround?Math.sin(t*2)*1.1:0;const stride=walking?Math.sin(t)*5:0;const skin='#d9b69e';const shoes='#111719';const coat=selectedCharacter==='Yumi'?'#38665a':selectedCharacter==='May'?'#555e79':'#3f6269';const hair=selectedCharacter==='Yumi'?'#121618':selectedCharacter==='May'?'#3e2925':'#2f2224';ctx.save();ctx.translate(0,bob);px(x-11+stride,y+44,10,25,'#252d2e');px(x+6-stride,y+44,10,25,'#252d2e');px(x-14+stride,y+66,17,7,shoes);px(x+4-stride,y+66,17,7,shoes);px(x-20,y+20,40,30,coat);px(x-14,y+16,28,10,'#ece4d5');px(x-11,y-8,29,30,skin);if(selectedCharacter==='Yumi'){px(x-17,y-17,37,14,hair);px(x-23,y-10,11,45,hair);px(x+19,y-10,11,45,hair);px(x-19,y+4,8,25,hair);px(x+22,y+4,8,25,hair);}else{px(x-16,y-14,38,14,hair);px(x-18,y-8,8,37,hair);px(x+17,y-8,8,35,hair);}px(x-7,y+1,4,3,'#161616');px(x+7,y+1,4,3,'#161616');px(x+1,y+11,8,3,'#9b5f58');const armSwing=walking?Math.sin(t+.8)*7:0;px(x-27-armSwing,y+26,9,25,coat);px(x+27+armSwing,y+26,9,25,coat);px(x-6,y+26,13,5,'#cfb36c');if(player.recoil>0)px(x+(player.facing>0?35:-45),y+33,12,5,'#ecd98d');if(player.hitTimer>0){ctx.globalAlpha=.35+Math.sin(totalTime*40)*.25;px(x-23,y-14,48,88,'#fff');ctx.globalAlpha=1;}ctx.restore();}
function drawSurvivor(s){if(s.found)return;const x=s.x-camera,y=GROUND-70;ctx.save();ctx.translate(0,Math.sin(totalTime*2+s.x)*.8);const type=s.name==='MARA'?'#695849':s.name==='ELI'?'#4c5d66':'#5c554a';px(x-12,y+43,10,25,'#22282a');px(x+6,y+43,10,25,'#22282a');px(x-19,y+21,39,29,type);px(x-10,y-7,26,30,'#d4b39e');px(x-16,y-13,38,14,'#2a2524');px(x-24,y+27,8,24,type);px(x+23,y+27,8,24,type);text(s.name,x+2,y-25,11,'#f0e5d2','center');if(Math.abs(player.x-s.x)<100)text('E  TALK',x+2,y-44,9,'#d6c79e','center');ctx.restore();}
function drawZombie(z){if(z.dead)return;const x=z.x-camera,y=GROUND-64;const bob=Math.sin(totalTime*3+z.phase)*2;const body=z.type==='brute'?'#534543':z.type==='runner'?'#63514f':'#515a58';px(x-14,y+10+bob,29,45,body);px(x-11,y-14+bob,23,27,body);px(x-24,y+24+bob,9,29,body);px(x+16,y+24+bob,9,29,body);px(x-14,y+53+bob,10,15,'#1a1d1e');px(x+5,y+53+bob,10,15,'#1a1d1e');px(x-7,y-5+bob,4,4,'#d56557');px(x+5,y-5+bob,4,4,'#d56557');if(z.type==='brute')px(x-20,y-20+bob,40,7,'#343b39');}
function drawSmiler(){if(!smiler.active||interior)return;const x=smiler.x-camera;if(x<-150||x>W+150)return;ctx.save();ctx.globalAlpha=smiler.intensity*.9;const h=250;px(x-22,GROUND-h,44,h,'#040405');px(x-31,GROUND-h-33,62,42,'#040405');px(x-18,GROUND-h-18,7,5,'#f0e8dc');px(x+10,GROUND-h-18,7,5,'#f0e8dc');ctx.strokeStyle='#ddd4c7';ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,GROUND-h+2,22,.12,3.02);ctx.stroke();ctx.restore();}
function drawInteriorCharacter(){const savedX=player.x,savedC=camera;const x=player.x;camera=0;drawPlayer();camera=savedC;}
function drawRain(){if(interior)return;for(let i=0;i<130;i++){const x=((i*47+totalTime*220-camera*.35)%W+W)%W;const y=(i*79+totalTime*340)%430;line(x,y,x-5,y+15,'rgba(175,196,205,.35)',1);}for(let i=0;i<24;i++){const x=(i*71+totalTime*280)%W;const y=GROUND-2+(i%3)*3;line(x,y,x-4,y+4,'rgba(205,214,208,.36)',1);line(x,y,x+5,y+3,'rgba(205,214,208,.28)',1);}}
function drawInteriorLight(){if(!interior)return;const cx=640,cy=310;const g=ctx.createRadialGradient(cx,cy,20,cx,cy,320);g.addColorStop(0,'rgba(228,220,190,.12)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);if(horror.blackout>0){ctx.fillStyle=`rgba(0,0,0,${horror.blackout*.55})`;ctx.fillRect(0,0,W,H);}}
function drawWorld(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.shadowBlur=0;ctx.clearRect(0,0,W,H);drawSky();drawOcean();drawGround();if(chapter==='ALCATRAZ')drawAlcatrazStructures();drawBuildings();drawStreetProps();drawSigns();drawDock();drawMedicalMarker();if(!interior){drawFootprints();for(const s of survivors)drawSurvivor(s);for(const z of zombies){if(Math.abs(z.x-player.x)<950)drawZombie(z);}drawSmiler();drawPlayer();drawRain();}else{drawInterior();for(const z of zombies){if(z.x>player.x-400&&z.x<player.x+400&&interior.type!=='cell')drawZombie({...z,x:z.x-player.x+640});}drawInteriorLight();drawInteriorCharacter();}drawParticles();drawPrompt();drawLighting();drawHorrorOverlay();ctx.restore();}
function drawPrompt(){const p=document.getElementById('prompt');if(!p)return;let s='';if(scene!=='play'){p.textContent='';return;}if(interior){if(interior.id==='cellA'&&!state.startKey&&Math.abs(player.x-310)<90)s='E — SEARCH THE MATTRESS';else if(interior.id==='cellA'&&!state.startEscaped&&Math.abs(player.x-610)<120)s='E — UNLOCK CELL A-17';else if(currentChest)s='E — OPEN CHEST';else if(player.x<155||player.x>1125)s='E — EXIT TO STREET';else s='';}else if(chapter==='ALCATRAZ'){if(currentChest)s='E — OPEN CHEST';else if(Math.abs(player.x-3550)<115&&!state.dockPass)s='E — OPEN MEDICAL SUPPLY CHEST';else if(Math.abs(player.x-4850)<190)s=state.dockPass?(state.beacon?'E — BOARD FERRY':'E — LIGHT FERRY BEACON'):'DOCK PASS REQUIRED';else{for(const b of buildings){if(b.x>worldWidth.ALCATRAZ)continue;const door=b.x+b.w/2;if(Math.abs(player.x-door)<130){s=`E — ENTER ${b.name}`;break;}}}}else{if(currentChest)s='E — OPEN CHEST';else{for(const b of buildings){if(Math.abs(player.x-(b.x+b.w/2))<135){s=`E — ENTER ${b.name}`;break;}}if(!s){for(const sv of survivors){if(!sv.found&&Math.abs(player.x-sv.x)<100){s=`E — TALK TO ${sv.name}`;break;}}}if(state.survivors>=2&&Math.abs(player.x-4720)<180)s='E — ENTER EMERGENCY SHELTER';}}p.textContent=s;}
function drawLighting(){if(scene!=='play')return;if(!state.light)return;const x=player.x-camera+player.facing*45,y=player.y+35;const g=ctx.createRadialGradient(x,y,5,x+player.facing*120,y,210);g.addColorStop(0,'rgba(248,240,214,.16)');g.addColorStop(.35,'rgba(220,220,204,.065)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(x-30,y-100,360,220);}
function drawHorrorOverlay(){if(scene!=='play')return;if(horror.flash>0){ctx.fillStyle=`rgba(238,230,216,${horror.flash*.18})`;ctx.fillRect(0,0,W,H);}if(horror.glitch>0){ctx.save();ctx.globalAlpha=.12;for(let i=0;i<22;i++){const y=(i*41+totalTime*210)%H;ctx.fillStyle=i%2?'#d4d0c5':'#5d6562';ctx.fillRect((i*71+totalTime*80)%W,y,80,1+(i%2));}ctx.restore();}if(state.sanity<52){const g=ctx.createRadialGradient(W/2,H/2,120,W/2,H/2,620);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(10,0,0,.28)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);}}
function drawHUD(){const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};set('healthValue',`${Math.ceil(state.health)}/${state.maxHealth}`);set('staminaValue',`${Math.ceil(state.stamina)}/${state.maxStamina}`);set('sanityValue',`${Math.ceil(state.sanity)}/100`);document.getElementById('healthFill').style.width=state.health/state.maxHealth*100+'%';document.getElementById('staminaFill').style.width=state.stamina/state.maxStamina*100+'%';document.getElementById('sanityFill').style.width=state.sanity+'%';set('locationText',chapter==='ALCATRAZ'?(interior?'CELL BLOCK A • INTERIOR':'ALCATRAZ ISLAND'):(interior?'SAN FRANCISCO • INTERIOR':'SAN FRANCISCO'));set('threatText',smiler.active?'DO NOT LOOK BEHIND YOU':state.sanity<55?'THE QUIET IS GETTING LOUDER':'THE PRISON IS QUIET');set('ammoText',`AMMO ${state.ammo} / ${state.reserveAmmo}`);}
function drawMenuSignal(){const e=document.getElementById('menuSignal');if(!e||document.getElementById('mainMenu').classList.contains('hidden'))return;if(Math.random()<.01)e.innerHTML='SIGNAL: <b>'+(['UNSTABLE','LOST','WATCHED','UNKNOWN'][Math.floor(Math.random()*4)])+'</b>';}
function loop(){requestAnimationFrame(loop);const now=performance.now();const dt=Math.min(.035,Math.max(.001,(now-last)/1000));last=now;totalTime+=dt;try{update(dt);}catch(err){console.error(err);setMessage('SYSTEM RECOVERED',1.2);}try{if(scene==='intro'){introDraw();hide('hud');}else if(scene==='play'||scene==='pause'||scene==='inventory'||scene==='ending'||scene==='death'){drawWorld();}if(scene==='play')drawHUD();if(scene==='menu')drawMenuSignal();}catch(err){console.error(err);safeVisualFallback();}}
function safeVisualFallback(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.clearRect(0,0,W,H);ctx.fillStyle='#18262a';ctx.fillRect(0,0,W,H);ctx.fillStyle='#3e4746';ctx.fillRect(0,430,W,290);px(80,330,280,240,'#45504f');px(105,355,230,18,'#65706c');for(let i=0;i<8;i++)px(120+i*25,380,5,145,'#181e20');drawPlayer();ctx.restore();}
function die(reason){if(scene==='death'||scene==='ending')return;scene='death';hide('hud');hide('inventoryUi');document.getElementById('deathText').textContent=reason;show('death');soundScare();}
function resetChapter(){hide('death');hide('ending');hide('pause');resetWorld();positionInsideCell();scene='intro';introIndex=0;introTimer=0;hide('hud');hide('cutscene');updateIntroText();}
function openInfo(){const grid=document.getElementById('deviceGrid');const nav=navigator;const rows=[['PLATFORM',nav.platform||'UNKNOWN'],['BROWSER',nav.userAgent||'UNKNOWN'],['SCREEN',`${screen.width} × ${screen.height}`],['LANGUAGE',nav.language||'UNKNOWN'],['TIMEZONE',Intl.DateTimeFormat().resolvedOptions().timeZone||'UNKNOWN'],['CPU THREADS',nav.hardwareConcurrency||'UNKNOWN'],['ONLINE',nav.onLine?'YES':'NO'],['TOUCH POINTS',nav.maxTouchPoints||0],['COOKIES',nav.cookieEnabled?'ENABLED':'DISABLED'],['DEVICE TIME',new Date().toLocaleString()]];grid.innerHTML='';rows.forEach(([a,b])=>{const d=document.createElement('div');d.className='privacyCard';d.innerHTML=`<b>${a}</b>${String(b).replaceAll('<','&lt;').replaceAll('>','&gt;')}`;grid.appendChild(d);});show('infoOverlay');}
function fire(){if(scene!=='play'||interior)return;if(state.ammo<=0){setMessage('EMPTY. PRESS R TO RELOAD.');soundReload();return;}state.ammo--;player.recoil=.16;shotTracers.push({x:player.x+player.facing*35,y:player.y+33,life:.08,dir:player.facing});soundShot();horror.shake=Math.max(horror.shake,3);for(const z of zombies){if(z.dead)continue;if((z.x-player.x)*player.facing>0&&Math.abs(z.x-player.x)<360){z.hp-=selectedCharacter==='Yumi'?34:30;spawnBlood(z.x,GROUND-35,5);if(z.hp<=0)z.dead=true;break;}}}
function reload(){if(scene!=='play')return;if(state.ammo>=12||state.reserveAmmo<=0)return;const need=12-state.ammo;const take=Math.min(need,state.reserveAmmo);state.ammo+=take;state.reserveAmmo-=take;soundReload();setMessage('RELOADING...',1);}
function melee(){if(scene!=='play')return;for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<85){z.hp-=52;z.x+=player.facing*25;spawnBlood(z.x,GROUND-36,8);if(z.hp<=0)z.dead=true;horror.shake=3;}}tone(82,.09,'square',.1,40);}
function toggleLight(){state.light=!state.light;tone(state.light?500:180,.07,'square',.06,0);}
function setupInput(){window.addEventListener('keydown',e=>{const k=e.key;if(['ArrowLeft','ArrowRight','ArrowUp',' ','a','A','d','D','w','W','Shift','Enter'].includes(k))e.preventDefault();keys.add(k);if(scene==='intro'&&(k==='Enter'||k===' ')){advanceIntro();return;}if(k==='e'||k==='E')interact();if(k==='q'||k==='Q')melee();if(k==='f'||k==='F')toggleLight();if(k==='r'||k==='R')reload();if(k==='g'||k==='G'){if(state.grenades>0){state.grenades--;tone(90,.2,'sawtooth',.12,120);setMessage('GRENADE THROWN',.8);}}if(k==='i'||k==='I'){if(scene==='play'){document.getElementById('inventoryHud').classList.toggle('hidden');}}if(k==='p'||k==='P'){openInfo();}if(k==='Tab'){e.preventDefault();document.getElementById('objectivePanel').classList.toggle('open');}if(k==='Escape'){if(document.getElementById('infoOverlay').classList.contains('hidden')===false){hide('infoOverlay');return;}if(scene==='play'){scene='pause';show('pause');hide('hud');}else if(scene==='pause'){scene='play';hide('pause');show('hud');}else if(scene==='inventory')closeChest();}});window.addEventListener('keyup',e=>keys.delete(e.key));window.addEventListener('blur',()=>{keys.clear();});window.addEventListener('mousedown',e=>{mouse.down=true;mouse.x=e.offsetX;mouse.y=e.offsetY;safeAudio();if(scene==='play'&&controlMode==='laptop')fire();});window.addEventListener('mouseup',()=>mouse.down=false);window.addEventListener('mousemove',e=>{const r=canvas.getBoundingClientRect();mouse.x=(e.clientX-r.left)*W/r.width;mouse.y=(e.clientY-r.top)*H/r.height;});document.querySelectorAll('[data-touch]').forEach(b=>{const key=b.dataset.touch;const down=ev=>{ev.preventDefault();safeAudio();if(key==='interact'){interact();return;}if(key==='melee'){melee();return;}if(key==='light'){toggleLight();return;}if(key==='inventory'){if(scene==='play'){document.getElementById('inventoryHud').classList.toggle('hidden');}return;}if(key==='reload'){reload();return;}if(key==='fire'){fire();return;}if(key==='jump'){touch.jump=true;setTimeout(()=>touch.jump=false,90);tryJump();return;}touch[key]=true;};const up=ev=>{ev.preventDefault();if(key in touch)touch[key]=false;};b.addEventListener('pointerdown',down);b.addEventListener('pointerup',up);b.addEventListener('pointercancel',up);b.addEventListener('pointerout',up);});canvas.addEventListener('touchstart',e=>{if(controlMode==='mobile'){safeAudio();const t=e.touches[0];const r=canvas.getBoundingClientRect();mouse.x=(t.clientX-r.left)*W/r.width;mouse.y=(t.clientY-r.top)*H/r.height;fire();}}, {passive:false});}
function syncTouch(){inputState.left=touch.left;inputState.right=touch.right;inputState.run=touch.run;}
function tickInput(){syncTouch();}
function updateInputTick(){tickInput();requestAnimationFrame(updateInputTick);}
function fourthWall(){let idle=0,lastVisibility=performance.now();window.addEventListener('pointermove',()=>idle=0);window.addEventListener('keydown',()=>idle=0);setInterval(()=>{if(scene!=='play')return;idle+=1;if(document.hidden){return;}if(idle>75){idle=0;showWarning('YOU ARE STILL THERE');tone(44,.3,'sine',.018,-5);}if(Math.random()<.004&&state.sanity<70)showWarning('THE GAME KNOWS YOU ARE LISTENING');},1000);document.addEventListener('visibilitychange',()=>{if(scene==='play'&&!document.hidden){showWarning('YOU CAME BACK.');horror.flash=.3;}});}
function initButtons(){document.getElementById('privacyEnter').onclick=()=>{safeAudio();document.getElementById('privacyGate').remove();show('mainMenu');};document.getElementById('privacyDevice').onclick=openInfo;document.getElementById('infoClose').onclick=()=>hide('infoOverlay');document.getElementById('playButton').onclick=()=>{safeAudio();hide('mainMenu');show('characterMenu');};document.getElementById('creditsButton').onclick=()=>{hide('mainMenu');show('credits');};document.getElementById('controlsButton').onclick=()=>{show('controlsOverlay');};document.getElementById('creditsBack').onclick=()=>{hide('credits');show('mainMenu');};document.getElementById('characterBack').onclick=()=>{hide('characterMenu');show('mainMenu');};document.getElementById('characterControls').onclick=()=>show('controlsOverlay');document.getElementById('characterPrivacy').onclick=openInfo;document.querySelectorAll('.charCard').forEach(b=>b.onclick=()=>startGame(b.dataset.character));document.querySelectorAll('[data-control]').forEach(b=>b.onclick=()=>setControlMode(b.dataset.control));document.getElementById('autoMode').onclick=()=>setControlMode('auto');document.getElementById('controlsBack').onclick=()=>hide('controlsOverlay');document.getElementById('objectiveTab').onclick=()=>{objectivePanelOpen=!objectivePanelOpen;document.getElementById('objectivePanel').classList.toggle('open',objectivePanelOpen);};document.getElementById('objectiveClose').onclick=()=>{objectivePanelOpen=false;document.getElementById('objectivePanel').classList.remove('open');};document.getElementById('resumeButton').onclick=()=>{scene='play';hide('pause');show('hud');};document.getElementById('restartButton').onclick=resetChapter;document.getElementById('pauseMenuButton').onclick=()=>{scene='menu';hide('pause');hide('hud');show('mainMenu');};document.getElementById('endingMenuButton').onclick=()=>{scene='menu';hide('ending');show('mainMenu');};document.getElementById('deathRestartButton').onclick=resetChapter;document.getElementById('deathMenuButton').onclick=()=>{scene='menu';hide('death');show('mainMenu');};document.getElementById('chestCloseButton').onclick=closeChest;document.getElementById('takeAllButton').onclick=takeAll;document.getElementById('sortButton').onclick=sortChest;document.getElementById('soundButton').onclick=()=>{soundEnabled=!soundEnabled;document.getElementById('soundButton').textContent=`SOUND: ${soundEnabled?'ON':'OFF'}`;if(soundEnabled)safeAudio();};}
function updateIntroText(){const e=document.getElementById('cutText');if(e)e.innerHTML=`<b>${cutLines[introIndex]||cutLines[0]}</b><small>ENTER / SPACE TO CONTINUE • AUTO-ADVANCE</small>`;}
function advanceIntro(){if(scene!=='intro')return;introTimer=0;introIndex++;if(introIndex>=cutLines.length){scene='play';hide('cutscene');show('hud');player.x=315;player.y=GROUND-player.h;player.vx=0;player.vy=0;interior={id:'cellA',name:'CELL A-17',type:'cell',building:{id:'cellA',name:'CELL BLOCK A',type:'prison',floors:2}};setObjective();setMessage('CELL A-17. Search under the mattress.');soundDoor();}else{updateIntroText();tone(180,.08,'sine',.045,35);}}
function introDraw(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.clearRect(0,0,W,H);const sky=ctx.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#071018');sky.addColorStop(.55,'#101b20');sky.addColorStop(1,'#040708');ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);ctx.fillStyle='#0a1113';ctx.fillRect(0,475,W,245);ctx.fillStyle='#151d20';ctx.fillRect(0,390,W,115);ctx.fillStyle='#1c2528';ctx.fillRect(90,305,1100,95);for(let i=0;i<12;i++){const x=120+i*92;ctx.fillStyle=i%3===0?'#b9ad7c':'#20292b';ctx.fillRect(x,328,42,36);if(i%3===0){ctx.fillStyle='rgba(230,215,166,.25)';ctx.fillRect(x+5,333,32,26);}}ctx.fillStyle='#252e30';ctx.fillRect(535,215,210,185);ctx.fillStyle='#141a1c';ctx.fillRect(610,185,60,215);ctx.fillStyle='#303a3c';ctx.fillRect(596,200,88,18);for(let i=0;i<18;i++){const x=((i*83-totalTime*35)%W+W)%W;const y=100+(i*37)%340;ctx.fillStyle='rgba(170,198,210,.32)';ctx.fillRect(x,y,2,12);}const fog=.05+.025*Math.sin(totalTime*1.3);ctx.fillStyle=`rgba(190,200,197,${fog})`;ctx.fillRect(0,360,W,110);ctx.fillStyle='rgba(0,0,0,.38)';ctx.fillRect(0,0,W,54);ctx.fillRect(0,H-54,W,54);text('ASHES OF THE DEAD',W/2,100,34,'#ded8ca','center');text(cutLines[introIndex]||cutLines[0],W/2,520,20,'#e7e1d7','center');text('ALCATRAZ ISLAND • 11:47 PM',W/2,552,11,'#929a96','center');ctx.restore();}
function renderScene(){if(scene==='menu')return;drawWorld();if(scene==='intro')introDraw();}
function mainLoop(){requestAnimationFrame(mainLoop);const now=performance.now();const dt=Math.min(.033,Math.max(.001,(now-last)/1000));last=now;totalTime+=dt;try{if(scene==='play'||scene==='intro')tickInput();update(dt);if(scene==='menu'){}if(scene==='play')drawHUD();if(messageTimer>0){messageTimer-=dt;if(messageTimer<=0)hide('message');}renderScene();}catch(e){console.error(e);safeVisualFallback();}}
let booted=false;let loopStarted=false;function bootstrap(){if(booted)return;try{setControlMode('laptop');initButtons();setupInput();fourthWall();resetWorld();hide('mainMenu');hide('hud');hide('cutscene');show('privacyGate');booted=true;if(!loopStarted){loopStarted=true;loop();}}catch(err){console.error('BOOT FAILURE',err);booted=false;setTimeout(bootstrap,80);}}
bootstrap();setTimeout(()=>{if(!booted||!document.getElementById('privacyEnter')?.onclick)bootstrap();},120);
</script>
</body>
</html>'''

@app.get('/')
def index():
    return Response(GAME_HTML, mimetype='text/html')

@app.get('/gadget')
def gadget():
    forwarded=request.headers.get('X-Forwarded-For','')
    seen=forwarded.split(',')[0].strip() if forwarded else request.remote_addr
    return jsonify({'server_seen_ip':seen or 'unknown','note':'The address visible to the game server may be a proxy address.'})

@app.get('/health')
def health():
    return {'status':'ok','game':'Ashes of the Dead','chapter':'Alcatraz Escape'}

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
