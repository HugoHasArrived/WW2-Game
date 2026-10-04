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

#app{border:1px solid #242d2f;background:#10191c}#world{background:#152126;box-shadow:inset 0 0 0 1px rgba(221,221,210,.03)}.appPixelGlow{position:absolute;inset:0;z-index:3;pointer-events:none;background:radial-gradient(circle at 50% 42%,rgba(220,216,194,.075),transparent 42%),linear-gradient(180deg,rgba(255,255,255,.018),transparent 27%,rgba(0,0,0,.10));mix-blend-mode:screen}.menu{background:#05090b}.menuBackdrop:after{content:"";position:absolute;left:0;right:0;bottom:0;height:23%;background:linear-gradient(180deg,transparent,rgba(0,0,0,.44));pointer-events:none}.menuPrison{filter:drop-shadow(0 0 14px rgba(187,177,145,.06));background:linear-gradient(180deg,#1b2326,#12181a)}.menuTower{box-shadow:0 0 36px rgba(170,177,163,.09),0 0 10px rgba(0,0,0,.8)}.menuLogo{letter-spacing:10px;text-shadow:4px 4px #030506,0 0 10px rgba(238,231,211,.10),0 0 36px rgba(197,184,144,.10)}.menuLore{background:rgba(5,8,9,.27);border:1px solid rgba(96,105,104,.25);padding:12px 16px}.menuTip{margin-top:10px;color:#707a75;letter-spacing:2px;font-size:9px}.menuButtons button{min-width:186px}.charSelectBox{background:linear-gradient(180deg,rgba(17,23,25,.97),rgba(7,10,11,.97));border-color:#596260;box-shadow:0 30px 120px #000,0 0 60px rgba(166,154,114,.04)}.charCard{background:linear-gradient(180deg,#151c1d,#0a0e0f);border-color:#5e6765;min-height:162px}.charCard .name{font-size:24px;color:#f5e7ca;text-shadow:0 2px #090b0c,0 0 12px rgba(213,195,150,.15)}.charCard .meta{color:#d1d6d2}.charCard .skill{color:#b9ae8c}.hudLeft,.hudRight{backdrop-filter:blur(2px)}.objectiveTab{background:linear-gradient(180deg,#1a1e1a,#0b0f0e);color:#efe7d4}.prompt{background:rgba(5,8,8,.72);border-color:#85795e!important;padding:8px 14px!important}.soundButton{background:rgba(6,9,9,.84)!important;border-color:#596360!important}.worldWarningText{letter-spacing:3px;text-shadow:0 0 18px rgba(232,210,177,.28)}.mobileControls{backdrop-filter:blur(2px)}

.visualEnhance{position:absolute;inset:0;z-index:4;pointer-events:none;overflow:hidden}.visualEnhance:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,.025),transparent 20%,rgba(0,0,0,.12) 100%),repeating-linear-gradient(0deg,rgba(255,255,255,.018) 0 1px,transparent 1px 4px);mix-blend-mode:screen;opacity:.36}.visualEnhance:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 52%,rgba(0,0,0,.38) 100%);opacity:.72}.pixelTag{position:absolute;left:50%;top:16px;transform:translateX(-50%);padding:5px 10px;border:1px solid rgba(201,190,157,.25);background:rgba(4,7,7,.55);color:#b8ad8f;font-size:9px;letter-spacing:3px;white-space:nowrap}.menuDepth{position:absolute;inset:0;pointer-events:none}.menuDepth:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(9,16,19,0) 0 56%,rgba(5,9,10,.52) 80%,rgba(3,5,6,.9) 100%)}.menuDepth:after{content:"";position:absolute;left:0;right:0;bottom:18%;height:22%;background:linear-gradient(90deg,transparent,rgba(158,169,168,.04),transparent);filter:blur(11px);animation:depthSweep 9s linear infinite}@keyframes depthSweep{0%{transform:translateX(-25%)}50%{transform:translateX(8%)}100%{transform:translateX(25%)}}.menuButtonPulse{animation:buttonPulse 3.7s ease-in-out infinite}@keyframes buttonPulse{0%,100%{box-shadow:0 0 0 rgba(210,195,151,0)}50%{box-shadow:0 0 34px rgba(210,195,151,.10)}}
</style>
</head>
<body>
<div id="app">
<canvas id="world" width="1280" height="720"></canvas><div class="appPixelGlow"></div><div id="visualEnhance" class="visualEnhance"><div class="pixelTag">NIGHTWATCH FIELD RENDER • PIXEL BUILD</div></div>
<div id="mainMenu" class="layer menu">
<div class="menuDepth"></div><div class="menuBackdrop"><div class="menuMoon"></div><div class="menuOcean"></div><div class="menuIsland"></div><div class="menuPrison"></div><div class="menuTower"></div><div class="menuFog"></div><div class="menuFog two"></div><div class="menuRain"></div><div class="menuVignette"></div><div class="menuNoise"></div></div>
<div class="menuContent"><div class="menuKicker">NIGHTWATCH // ALCATRAZ INCIDENT 01</div><div class="menuLogo">ASHES OF THE DEAD</div><div class="menuTag">SCREAM JAM 2026 • THE ISLAND IS LISTENING</div><div class="menuLore">A female detective wakes inside Cell A-17. The prison is quiet. The rain is loud. Something else is awake. Find the docks. Escape the island. Find two survivors.</div><div class="menuButtons"><button id="playButton" class="menuPlay menuButtonPulse">PLAY</button><button id="creditsButton">CREDITS</button><button id="controlsButton">CONTROL MODE</button></div><div class="menuThreat">HEADPHONES RECOMMENDED • DO NOT TRUST EVERY SOUND</div><div class="menuFooter">JULIA • MAY • YUMI • FEMALE DETECTIVES • ALCATRAZ → SAN FRANCISCO</div><div id="menuSignal" class="menuSignal">SIGNAL: <b>UNSTABLE</b></div></div></div>
<div id="characterMenu" class="layer screen hidden"><div class="charSelectBox"><div class="charSelectTitle">CHOOSE YOUR DETECTIVE</div><div class="charSelectSub">Choose your detective by profile. All three are female field investigators with distinct strengths. Your choice changes her visual identity, animation style, and small gameplay bonuses.</div><div class="charCards"><button class="charCard" data-character="Julia"><span class="name">JULIA</span><span class="meta">FIELD DETECTIVE<br>CALM UNDER PRESSURE</span><span class="skill">BALANCED SURVIVAL</span></button><button class="charCard" data-character="May"><span class="name">MAY</span><span class="meta">CRIME SCENE DETECTIVE<br>FAST INVESTIGATION</span><span class="skill">AGILITY + SEARCH</span></button><button class="charCard" data-character="Yumi"><span class="name">YUMI</span><span class="meta">INTELLIGENCE DETECTIVE<br>OBSERVANT + TECHNICAL</span><span class="skill">STEADY AIM + SANITY</span></button></div><div class="center"><button id="characterBack">BACK</button><button id="characterControls">CONTROL MODE</button><button id="characterPrivacy">PRIVACY</button></div></div></div>
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
const player={x:0,y:0,w:34,h:70,vx:0,vy:0,facing:1,onGround:true,doubleJump:true,coyote:0,jumpBuffer:0,anim:0,stepTimer:0,landTimer:0,recoil:0,hitTimer:0,lean:0,squash:0,airTime:0};
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
let visualFX={mist:0,water:0,lightPulse:0,worldBeat:0};
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
function strokeRect(x,y,w,h,c,l=1){ctx.strokeStyle=c;ctx.lineWidth=l;ctx.strokeRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));}
function pixelDiamond(cx,cy,r,c){poly([[cx,cy-r],[cx+r,cy],[cx,cy+r],[cx-r,cy]],c);}
function glow(cx,cy,r,inner,outer){const g=ctx.createRadialGradient(cx,cy,0,cx,cy,r);g.addColorStop(0,inner);g.addColorStop(1,outer);ctx.fillStyle=g;ctx.fillRect(cx-r,cy-r,r*2,r*2);}
function drawPixelCloud(x,y,w,h,c,a=.12){ctx.save();ctx.globalAlpha=a;for(let i=0;i<8;i++){const bx=x+i*w*.12;const by=y+Math.sin(i*1.7+totalTime*.15)*h*.25;px(bx,by,w*.22,h*.4,c);px(bx+w*.1,by-h*.18,w*.25,h*.55,c);}ctx.restore();}
function spawnSparks(x,y,n=5){for(let i=0;i<n;i++)particles.push({x,y,vx:(Math.random()-.5)*120,vy:-20-Math.random()*140,s:1+Math.random()*2,life:.25+Math.random()*.35,max:.55,c:Math.random()<.55?'#d6c17b':'#aab8b6'});}
function drawLampGlow(x,y,r=92,p=.85){const pulse=.84+.16*Math.sin(totalTime*2.2+x*.001);glow(x,y,r,`rgba(231,208,135,${.15*p*pulse})`,'rgba(231,208,135,0)');}

function show(id){const e=document.getElementById(id);if(e)e.classList.remove('hidden');}
function hide(id){const e=document.getElementById(id);if(e)e.classList.add('hidden');}
function setMessage(t,time=2){const e=document.getElementById('message');if(!e)return;e.textContent=t;e.classList.remove('hidden');messageTimer=time;}
function showWarning(t){const e=document.getElementById('warningText');if(!e)return;e.textContent=t;e.style.opacity='1';horror.warning=2.4;}
function safeAudio(){try{if(!audioCtx){audioCtx=new(window.AudioContext||window.webkitAudioContext)();masterGain=audioCtx.createGain();musicGain=audioCtx.createGain();sfxGain=audioCtx.createGain();rainGain=audioCtx.createGain();masterGain.gain.value=.98;musicGain.gain.value=.34;sfxGain.gain.value=1.12;rainGain.gain.value=.27;musicGain.connect(masterGain);sfxGain.connect(masterGain);rainGain.connect(masterGain);masterGain.connect(audioCtx.destination);}if(audioCtx.state==='suspended')audioCtx.resume();return audioCtx;}catch(e){return null;}}
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
function physics(dt){if(scene!=='play'||fadeBusy)return;const left=inputState.left||keys.has('a')||keys.has('ArrowLeft');const right=inputState.right||keys.has('d')||keys.has('ArrowRight');const run=inputState.run||keys.has('Shift');const dir=(right?1:0)-(left?1:0);let maxSpeed=run?300:210;if(interior)maxSpeed*=.94;if(state.stamina<18)maxSpeed*=.78;const accel=dir?1550:1900;if(dir){player.vx=lerp(player.vx,dir*maxSpeed,Math.min(1,accel*dt/Math.max(1,maxSpeed)));player.facing=dir;}else player.vx=lerp(player.vx,0,Math.min(1,1750*dt/Math.max(1,maxSpeed)));player.coyote=player.onGround?.13:Math.max(0,player.coyote-dt);player.jumpBuffer=Math.max(0,player.jumpBuffer-dt);if((inputState.jump||keys.has('w')||keys.has(' ')||keys.has('ArrowUp'))&&!player.jumpBuffer)player.jumpBuffer=.11;if(player.jumpBuffer>0&&(player.onGround||player.coyote>0||player.doubleJump)){const second=!player.onGround;if(second&&player.doubleJump)player.doubleJump=false;player.vy=second?-400:-505;player.onGround=false;player.coyote=0;player.jumpBuffer=0;player.airTime=0;soundJump();spawnDust(player.x+player.w/2,GROUND-2,8);}player.vy+=1350*dt;const wasGround=player.onGround;player.x+=player.vx*dt;player.y+=player.vy*dt;if(player.y+player.h>=GROUND){player.y=GROUND-player.h;player.vy=0;player.onGround=true;if(!wasGround){player.landTimer=.24;player.squash=.16;soundLand();spawnDust(player.x+player.w/2,GROUND-2,10);spawnSparks(player.x+player.w/2,GROUND-2,2);}}else{player.onGround=false;player.airTime+=dt;}if(!dir&&player.onGround)state.stamina=Math.min(state.maxStamina,state.stamina+12*dt);else if(run&&dir)state.stamina=Math.max(0,state.stamina-22*dt);else state.stamina=Math.min(state.maxStamina,state.stamina+4*dt);state.hunger=Math.max(0,state.hunger-.035*dt);if(state.hunger<=0)state.health=Math.max(0,state.health-.4*dt);player.anim+=dt*(Math.abs(player.vx)>15?Math.abs(player.vx)/31:1.2);player.stepTimer-=dt;if(player.onGround&&Math.abs(player.vx)>70&&player.stepTimer<=0){player.stepTimer=player.vx>215?.23:.34;soundStep();footprints.push({x:player.x+player.w/2,y:GROUND-3,t:2.2,side:player.facing});if(footprints.length>40)footprints.shift();spawnDust(player.x+player.w/2,GROUND-3,3);}player.recoil=Math.max(0,player.recoil-dt*4);player.landTimer=Math.max(0,player.landTimer-dt);player.squash=Math.max(0,player.squash-dt);player.hitTimer=Math.max(0,player.hitTimer-dt);player.lean=lerp(player.lean,dir*.045,Math.min(1,dt*10));const maxW=worldWidth[chapter];if(interior)player.x=clamp(player.x,55,W-90);else player.x=clamp(player.x,40,maxW-70);const desired=interior?0:clamp(player.x-W*.42,0,maxW-W);camera=lerp(camera,desired,Math.min(1,dt*5.5));}
function updateInteractables(dt){currentChest=nearestChest();if(chapter==='ALCATRAZ'&&!interior&&state.startEscaped&&player.x>3200&&player.x<3920&&!state.dockPass)setObjective();if(chapter==='ALCATRAZ'&&state.startEscaped&&state.dockPass&&!state.beacon)objectiveIndex=1;if(chapter==='SAN FRANCISCO')objectiveIndex=2;setObjective();}
function updateZombies(dt){for(const z of zombies){if(z.dead)continue;z.attack=Math.max(0,z.attack-dt);const dx=player.x-z.x;if(Math.abs(dx)<740&&!interior){z.x+=Math.sign(dx)*(z.type==='runner'?66:z.type==='brute'?25:42)*dt;const d=dist(player.x,z.x);if(d<54&&z.attack<=0){state.health=Math.max(0,state.health-(z.type==='brute'?18:8));player.hitTimer=.3;horror.shake=7;z.attack=1.15;soundHit();spawnBlood(player.x,GROUND-38,8);if(state.health<=0)die('The infected finally caught you.');}}}}
function soundHit(){tone(90,.1,'sawtooth',.08,-40);}
function updateSurvivors(dt){for(const s of survivors){if(s.found)s.x=lerp(s.x,player.x+(-80+Math.sin(totalTime+s.x)*18),dt*.8);}}
function updateSmiler(dt){if(scene!=='play'||interior)return;smiler.cooldown-=dt;if(smiler.active){smiler.timer-=dt;smiler.intensity=Math.min(1,smiler.intensity+dt*2);state.sanity=Math.max(0,state.sanity-.22*dt);if(smiler.timer<=0){smiler.active=false;smiler.intensity=0;smiler.cooldown=20+Math.random()*35;}}else if(smiler.cooldown<=0){const threshold=state.sanity<65?.0018:state.sanity<85?.0008:.00025;if(Math.random()<dt*threshold){smiler.active=true;smiler.timer=2+Math.random()*3.5;smiler.x=clamp(player.x+(Math.random()<.5?-1:1)*(450+Math.random()*280),80,worldWidth[chapter]-90);smiler.intensity=0;soundScare();showWarning('SOMETHING IS WATCHING YOU');horror.shake=5;horror.flash=.4;}}}
function updateHorror(dt){horror.flash=Math.max(0,horror.flash-dt*2.5);horror.shake=Math.max(0,horror.shake-dt*8);horror.warning=Math.max(0,horror.warning-dt);horror.heartbeat=Math.max(0,horror.heartbeat-dt*2);horror.glitch=Math.max(0,horror.glitch-dt*1.8);if(horror.warning<=0){const e=document.getElementById('warningText');if(e)e.style.opacity='0';}if(scene==='play'){scareTimer-=dt;if(scareTimer<=0&&state.sanity<92){scareTimer=18+Math.random()*32;const chance=state.sanity<45?.15:.055;if(Math.random()<chance)triggerJumpscare();}if(state.sanity<55&&Math.random()<dt*.0012){horror.glitch=.8;showWarning(Math.random()<.5?'DO NOT LOOK AT THE WINDOWS':'YOU HEARD THAT TOO');randomHorrorAudio();}}}
function triggerJumpscare(){if(scene!=='play')return;horror.flash=.9;horror.shake=18;showWarning('RUN');soundScare();const e=document.getElementById('scare');e.classList.add('show');setTimeout(()=>e.classList.remove('show'),520);}
function update(dt){if(scene==='intro'){introTimer+=dt;if(introTimer>4.4)advanceIntro();return;}if(scene==='menu'){return;}if(scene==='pause'||scene==='inventory'||scene==='ending'||scene==='death')return;if(scene==='play'){physics(dt);updateInteractables(dt);updateZombies(dt);updateSurvivors(dt);updateSmiler(dt);updateHorror(dt);if(state.battery>0&&state.light)state.battery=Math.max(0,state.battery-.15*dt);if(state.sanity<=0)die('You could no longer tell what was real.');}}
function drawSky(){const sf=chapter==='SAN FRANCISCO';const g=ctx.createLinearGradient(0,0,0,430);g.addColorStop(0,sf?'#07131c':'#061118');g.addColorStop(.42,sf?'#13262f':'#102329');g.addColorStop(.78,sf?'#294047':'#284045');g.addColorStop(1,'#3a4d4d');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);const moonX=sf?1035:1018;const moonY=96;glow(moonX,moonY,110,'rgba(223,216,189,.16)','rgba(223,216,189,0)');ctx.fillStyle='rgba(224,217,193,.68)';ctx.beginPath();ctx.arc(moonX,moonY,42,0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(92,92,85,.25)';ctx.beginPath();ctx.arc(moonX-12,moonY-9,23,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(moonX+12,moonY+12,13,0,Math.PI*2);ctx.fill();for(let i=0;i<120;i++){const x=((i*127-camera*.10)%W+W)%W;const y=28+(i*49)%294;const a=.16+.35*(.5+.5*Math.sin(totalTime*1.4+i));ctx.globalAlpha=a;px(x,y,1+(i%2),1+(i%2),i%13===0?'#aab5b5':'#506168');}ctx.globalAlpha=1;for(let layer=0;layer<4;layer++){const par=camera*(.045+layer*.05);for(let i=-3;i<18;i++){const x=i*145-(par%145)+layer*23;const h=72+((i*37+layer*17)%130);const w=92+((i*23+layer*13)%80);const c=layer===0?'#14242a':layer===1?'#18292e':layer===2?'#1e3034':'#273b3e';px(x,404-h,w,h,c);px(x,404-h,w,5,'#33474a');for(let q=0;q<4;q++){const ww=x+12+q*22;const yy=423-h+((q+layer)%3)*29;if((q+i+layer)%3===0){px(ww,yy,10,17,'#4b5149');px(ww+2,yy+3,6,11,(q+layer)%2?'#8b7953':'#5d725f');}}}}drawPixelCloud((W*0.1+Math.sin(totalTime*.13)*25)%W,306,210,70,'#aab8b4',.08);drawPixelCloud((W*0.62+Math.sin(totalTime*.09)*35)%W,330,260,85,'#aab8b4',.07);const haze=ctx.createLinearGradient(0,315,0,470);haze.addColorStop(0,'rgba(181,198,194,.02)');haze.addColorStop(.58,'rgba(185,198,193,.08)');haze.addColorStop(1,'rgba(4,8,9,.18)');ctx.fillStyle=haze;ctx.fillRect(0,315,W,155);if(sf)drawGoldenGate();}
function drawGoldenGate(){const x=720-camera*.05;line(x,355,x+780,355,'#3b4548',6);line(x+130,355,x+130,192,'#3f4a4d',12);line(x+660,355,x+660,208,'#3f4a4d',12);for(let i=0;i<16;i++){const t=i/15;const xx=x+144+t*500;const yy=202+Math.sin(t*Math.PI)*105;line(xx,yy,xx,350,'#2a3235',1);}}
function drawOcean(){if(chapter!=='ALCATRAZ')return;ctx.fillStyle='#0d1d23';ctx.fillRect(0,365,W,74);for(let i=0;i<50;i++){const x=((i*71-camera*.2)%W+W)%W;const y=375+(i%6)*9;line(x,y,x+16,y,'#2a4048',1);line(x+25,y+4,x+39,y+4,'#1d3036',1);}}
function drawGround(){const base=chapter==='ALCATRAZ'?'#3f4846':'#474c4b';const road=chapter==='ALCATRAZ'?'#303938':'#383e3e';ctx.fillStyle=base;ctx.fillRect(0,430,W,290);ctx.fillStyle=road;ctx.fillRect(0,566,W,154);px(0,430,W,3,'#64706c');for(let i=0;i<380;i++){const x=((i*67-camera*.9)%W+W)%W;const y=441+(i*41)%225;const c=i%11===0?'#858780':i%4===0?'#626965':'#363d3c';px(x,y,1+(i%4),1+(i%3),c);}for(let i=0;i<34;i++){const x=((i*173-camera*.75)%W+W)%W;const y=590+(i%6)*19;line(x,y,x+12+(i%4)*6,y+((i%3)-1),'#242b2a',1);}for(let i=0;i<10;i++){const x=((i*251-camera*.5)%W+W)%W;ctx.fillStyle=`rgba(174,196,193,${.055+.02*(i%3)})`;ctx.beginPath();ctx.ellipse(x,546+(i%3)*9,35+(i%4)*15,5+(i%2)*2,0,0,Math.PI*2);ctx.fill();}if(chapter==='SAN FRANCISCO'){for(let i=0;i<10;i++){const x=((i*307-camera*.74)%W+W)%W;px(x,638,78,5,'#252c2b');px(x+22,631,34,3,'#636864');}}}
function drawAlcatrazStructures(){if(chapter!=='ALCATRAZ')return;const ax=650-camera;px(ax,GROUND-255,980,255,'#465153');px(ax,GROUND-255,980,10,'#818986');px(ax+9,GROUND-244,962,6,'#263032');for(let i=0;i<14;i++){const xx=ax+20+i*72;px(xx,GROUND-227,7,222,'#1c2526');px(xx+2,GROUND-220,3,212,'#707a76');}for(let i=0;i<11;i++){const xx=ax+42+i*78;px(xx,GROUND-214,47,34,'#2a3234');px(xx+4,GROUND-209,39,25,i%4===0?'#827759':'#3a484a');if(i%4===0)glow(xx+23,GROUND-195,40,'rgba(215,194,133,.06)','rgba(215,194,133,0)');}text('CELL BLOCK A',ax+34,GROUND-278,13,'#f1ead9');px(ax+10,GROUND-195,16,16,'#333c3d');px(ax+14,GROUND-191,8,8,'#b8a76f');const bx=1740-camera;px(bx,GROUND-255,900,255,'#465153');px(bx,GROUND-255,900,10,'#7d8784');for(let i=0;i<12;i++){const xx=bx+34+i*74;px(xx,GROUND-228,6,223,'#1c2426');px(xx+2,GROUND-220,3,214,'#69736f');}text('CELL BLOCK B',bx+30,GROUND-278,13,'#ece6d9');const tower=3020-camera;px(tower,GROUND-345,130,345,'#3b4547');px(tower-10,GROUND-357,150,15,'#68716f');px(tower+17,GROUND-328,95,37,'#1b2426');px(tower+35,GROUND-315,20,13,'#c0a967');glow(tower+45,GROUND-309,50,'rgba(214,191,119,.08)','rgba(214,191,119,0)');text('GUARD',tower+65,GROUND-286,10,'#ddd4c0','center');}
function drawBuildings(){const skip=['cellA','cellB','guard','medical','workshop','dock'];for(const b of buildings){if(chapter==='ALCATRAZ'&&b.id.startsWith('sf'))continue;if(chapter==='SAN FRANCISCO'&&skip.includes(b.id))continue;const x=b.x-camera;if(x<-b.w-160||x>W+160)continue;const h=b.type==='prison'?260:b.floors*102+86;const palette={prison:'#4c585a',station:'#515f64',medical:'#5e7072',workshop:'#5e625e',dock:'#5d625d',police:'#566871',hospital:'#65787b',funeral:'#5e5961',hotel:'#68706c',shelter:'#627069',research:'#64707a'};const body=palette[b.type]||'#5a6462';ctx.fillStyle='rgba(0,0,0,.16)';ctx.fillRect(x+18,GROUND-h+16,b.w,h);px(x,GROUND-h,b.w,h,body);px(x,GROUND-h,b.w,10,'#89918c');px(x+10,GROUND-h+16,b.w-20,7,'#2e393b');for(let f=0;f<b.floors;f++){const fy=GROUND-78-f*102;const count=Math.max(2,Math.floor((b.w-48)/45));for(let q=0;q<count;q++){const wx=x+24+q*45;const lit=(q+f+Math.floor(b.x/90))%5===0;px(wx,fy-37,29,32,lit?'#756e54':'#273437');px(wx+3,fy-34,23,25,lit?'#a28c59':'#344246');if(lit){px(wx+7,fy-30,6,8,'#dfc981');px(wx+17,fy-30,5,8,'#a8915b');glow(wx+15,fy-19,22,'rgba(224,198,121,.045)','rgba(224,198,121,0)');}}}for(let i=0;i<Math.min(9,Math.floor(b.w/90));i++){const bx=x+26+i*90;px(bx,GROUND-h+70,50,5,'#465052');px(bx+5,GROUND-h+76,40,4,'#707775');}const door=x+b.w/2-31;px(door,GROUND-79,62,79,'#171f21');px(door+5,GROUND-74,52,69,'#394446');px(door+43,GROUND-43,5,5,'#ddc47a');glow(door+30,GROUND-40,45,'rgba(225,205,145,.045)','rgba(225,205,145,0)');if(b.type==='medical'){px(x+b.w/2-98,GROUND-h+18,196,39,'#6e7c7d');px(x+b.w/2-12,GROUND-h+23,24,26,'#f1eee4');px(x+b.w/2-35,GROUND-h+31,70,10,'#f1eee4');text('MEDICAL WING',x+b.w/2,GROUND-h+67,11,'#f4ead6','center');}if(b.type==='police'){text('POLICE',x+25,GROUND-h+39,14,'#eee9dc');px(x+23,GROUND-h+52,82,3,'#aca58b');}if(b.type==='funeral'){text('MERCY FUNERAL',x+38,GROUND-h+39,11,'#e1d7ca');}if(b.type==='research'){text('ECLIPSE RESEARCH ANNEX',x+b.w/2,GROUND-h+39,10,'#e4dfd4','center');}}}
function drawStreetProps(){const lamps=[380,1120,1980,2860,3770,4660,5560,6520,7480];for(const wx of lamps){const x=wx-camera;if(x<-120||x>W+120)continue;px(x,GROUND-156,7,156,'#1a2223');px(x-12,GROUND-161,29,7,'#454e4d');px(x-9,GROUND-173,23,12,'#252c2d');px(x-4,GROUND-174,13,5,'#dfc97d');drawLampGlow(x+2,GROUND-166,84,.95);}if(chapter==='SAN FRANCISCO'){for(let i=0;i<14;i++){const x=260+i*500-camera;if(x<-120||x>W+120)continue;px(x,GROUND-59,84,33,'#2b3233');px(x+8,GROUND-51,68,13,'#4d5555');px(x+12,GROUND-16,15,6,'#14191a');px(x+57,GROUND-16,15,6,'#14191a');if(i%4!==0){px(x+17,GROUND-45,20,9,'#77786f');px(x+45,GROUND-45,20,9,'#696b67');}}}else{for(let i=0;i<15;i++){const x=130+i*370-camera;if(x<-120||x>W+120)continue;px(x,GROUND-22,78,12,'#252b2a');px(x+7,GROUND-34,62,12,'#4b504a');px(x+19,GROUND-29,34,3,'#818279');if(i%3===0)pixelDiamond(x+48,GROUND-42,5,'#5e6a65');}}}
function drawPlayer(){const x=player.x-camera,y=player.y;const moving=player.onGround&&Math.abs(player.vx)>15;const run=Math.abs(player.vx)>225;const p=Math.sin(player.anim*(run?1.7:1.35));const idle=Math.sin(totalTime*2.15)*.35;const bob=player.onGround?(moving?Math.abs(p)*1.5:idle*.45):0;const skin='#d7b39a',skinHi='#efc8ab',skinShadow='#9e7565',shoe='#14191b';const profiles={Julia:{coat:'#456f78',coat2:'#79a1a6',hair:'#302327',hi:'#65474f',accent:'#d4bd79',scarf:'#ded7c5'},May:{coat:'#596684',coat2:'#8791ad',hair:'#513329',hi:'#845648',accent:'#d6c17e',scarf:'#e3ddd0'},Yumi:{coat:'#3c7866',coat2:'#72aa96',hair:'#151a1b',hi:'#58666b',accent:'#ddc17b',scarf:'#e5ded0'}};const q=profiles[selectedCharacter]||profiles.Julia;const stride=moving?p*7:0;const arm=moving?p*5:idle*1.5;const lean=moving?p*.045:0;const stretch=player.onGround?1:clamp(1+Math.abs(player.vy)*.00045,.92,1.10);ctx.save();ctx.translate(x+1,y+36+bob);ctx.rotate(player.lean||lean);ctx.scale(1,stretch);const legA=8+stride,legB=8-stride;px(-13+legA,8,10,28,'#263133');px(5-legB,8,10,28,'#263133');px(-17+legA,34,19,7,shoe);px(2-legB,34,19,7,shoe);px(-23,-10,46,39,q.coat);px(-27,-5,7,30,q.coat2);px(20,-5,7,30,q.coat2);px(-14,-13,28,10,'#eee6d8');px(-8,-4,16,5,q.scarf);px(-12,-39,28,29,skin);px(-8,-35,20,20,skinHi);if(selectedCharacter==='Yumi'){px(-18,-48,36,12,q.hair);px(-22,-42,10,41,q.hair);px(18,-43,11,45,q.hair);px(-15,-51,26,6,q.hi);px(21,-22,7,19,q.hi);px(-20,-20,7,19,q.hi);px(-10,-43,5,3,q.hi);px(5,-43,5,3,q.hi);px(-15,-7,8,14,q.hi);px(17,-9,8,16,q.hi);}else{px(-17,-47,36,12,q.hair);px(-21,-41,10,35,q.hair);px(18,-41,9,31,q.hair);px(-14,-51,26,6,q.hi);}px(-7,-29,3,3,'#191817');px(6,-29,3,3,'#191817');px(-1,-19,8,2,skinShadow);px(-7,-7,14,3,q.scarf);px(-29-arm,-5,9,28,q.coat);px(21+arm,-5,9,28,q.coat);px(-33-arm,19,9,8,skin);px(25+arm,19,9,8,skin);px(-6,-6,13,5,q.accent);px(-3,-4,6,2,'#f2dda8');if(player.facing>0){px(28,-1,20,5,'#1f292b');px(34,4,12,3,'#66706d');}else{px(-48,-1,20,5,'#1f292b');px(-45,4,12,3,'#66706d');}if(player.recoil>0){px(player.facing>0?47:-60,-2,13,5,'#f5d988');}if(!player.onGround){px(-21,41,11,5,'#5f6864');px(9,39,11,5,'#5f6864');}if(player.landTimer>0){ctx.globalAlpha=.08*clamp(player.landTimer/.2,0,1);px(-32,45,64,5,'#d2c8af');ctx.globalAlpha=1;}if(player.hitTimer>0){ctx.globalAlpha=.28+.12*Math.sin(totalTime*38);px(-29,-51,58,94,'#fff');ctx.globalAlpha=1;}ctx.restore();}
function drawSurvivor(s){if(s.found)return;const x=s.x-camera,y=GROUND-70;const walk=Math.sin(totalTime*2.7+s.x*.01)*4;const breath=Math.sin(totalTime*1.6+s.x*.002);const profiles={MARA:{body:'#795946',coat:'#8e6a50',hair:'#2e2725'},ELI:{body:'#4f6775',coat:'#667f8e',hair:'#302a29'},NOAH:{body:'#686057',coat:'#81776c',hair:'#413a34'}};const q=profiles[s.name]||profiles.NOAH;const skin='#d1ad95';ctx.save();ctx.translate(0,Math.sin(totalTime*1.9+s.x)*.7+breath*.6);const swing=walk;px(x-12+swing,y+43,10,25,'#252b2c');px(x+6-swing,y+43,10,25,'#252b2c');px(x-20,y+21,40,30,q.body);px(x-15,y+7,30,17,q.coat);px(x-10,y-7,26,30,skin);px(x-16,y-14,38,14,q.hair);px(x-23,y+27+swing,8,24,q.coat);px(x+22,y+27-swing,8,24,q.coat);px(x-9,y+3,3,3,'#21201d');px(x+4,y+3,3,3,'#21201d');px(x-7,y-1,17,2,'#8a6052');text(s.name,x+2,y-27,12,'#fff1d4','center');if(Math.abs(player.x-s.x)<110)text('E  TALK',x+2,y-48,10,'#ecd69e','center');ctx.restore();}
function drawZombie(z){if(z.dead)return;const x=z.x-camera,y=GROUND-64;const t=totalTime*(z.type==='runner'?6.5:z.type==='brute'?2.4:3.8)+z.phase;const f=Math.sin(t);const f2=Math.sin(t+1.4);const bob=Math.sin(t*.83)*2.5;const body=z.type==='brute'?'#654b4d':z.type==='runner'?'#70524f':'#566560';const skin=z.type==='brute'?'#715253':'#816b5f';ctx.save();ctx.translate(0,bob);const sx=z.type==='brute'?1.14:1;ctx.scale(sx,1);px(x-15+f*2,y+10,30,46,body);px(x-12,y-15,24,28,skin);px(x-9,y-11,18,18,body);px(x-27-f*3,y+24,9,29,body);px(x+18+f2*3,y+24,9,29,body);px(x-15-f2*3,y+53,11,15,'#1b1e1f');px(x+5+f*3,y+53,11,15,'#1b1e1f');px(x-8,y-6,4,4,'#e06b5a');px(x+5,y-6,4,4,'#e06b5a');px(x-3,y+5,10,3,'#2b2022');px(x-18,y+14,5,13,'#785b54');px(x+13,y+13,5,13,'#765852');if(z.type==='brute'){px(x-22,y-22,44,7,'#3a4440');px(x-29,y+32,8,12,'#765454');px(x+21,y+33,8,12,'#765454');}if(z.type==='runner'){px(x-18,y+2,36,4,'#9b7060');}ctx.restore();}
function drawSmiler(){if(!smiler.active||interior)return;const x=smiler.x-camera;if(x<-190||x>W+190)return;const a=clamp(smiler.intensity,0,1);const h=292+18*Math.sin(totalTime*1.15);ctx.save();ctx.globalAlpha=.96*a;px(x-28,GROUND-h,56,h,'#050506');px(x-38,GROUND-h-44,76,54,'#050506');px(x-20,GROUND-h-24,9,6,'#f1eadc');px(x+11,GROUND-h-24,9,6,'#f1eadc');px(x-10,GROUND-h-5,20,4,'#efe7dc');for(let i=0;i<6;i++)px(x-14+i*6,GROUND-h+3,4,4,'#bdb5ad');px(x-42,GROUND-h+34,11,128,'#050506');px(x+31,GROUND-h+34,11,128,'#050506');px(x-20,GROUND-5,13,5,'#050506');px(x+8,GROUND-5,13,5,'#050506');ctx.globalAlpha=.14*a;const g=ctx.createRadialGradient(x,GROUND-h*.5,20,x,GROUND-h*.5,220);g.addColorStop(0,'rgba(237,231,215,.16)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(x-240,GROUND-h-130,480,380);ctx.restore();}
function drawInteriorLight(){if(!interior)return;const g=ctx.createRadialGradient(640,300,20,640,300,390);g.addColorStop(0,'rgba(242,233,202,.18)');g.addColorStop(.42,'rgba(214,211,194,.07)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);if(interior.type==='cell'){const l=ctx.createRadialGradient(642,176,2,642,176,160);l.addColorStop(0,'rgba(235,213,161,.20)');l.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=l;ctx.fillRect(480,80,320,260);}if(horror.blackout>0){ctx.fillStyle=`rgba(0,0,0,${horror.blackout*.2})`;ctx.fillRect(0,0,W,H);}}

function drawWorldDepthFX(){ctx.save();if(!interior){const horizon=430;for(let i=0;i<18;i++){const x=((i*91-camera*.32)%W+W)%W;const y=horizon+20+(i%6)*13;px(x,y,18+(i%4)*7,2,'#4b5753');}for(let i=0;i<8;i++){const x=((i*177-camera*.58)%W+W)%W;px(x,GROUND-4,16,4,'#202625');px(x+5,GROUND-8,7,4,'#676b65');}}else{for(let i=0;i<7;i++){const x=35+i*196;px(x,508,110,6,'#333a39');px(x+14,502,64,4,'#68706c');}}ctx.restore();}
function drawDynamicLight(){if(scene!=='play')return;ctx.save();if(interior){glow(640,125,185,'rgba(226,208,163,.065)','rgba(0,0,0,0)');}else{for(const wx of [380,1120,1980,2860,3770,4660,5560,6520,7480]){const sx=wx-camera;if(sx>-120&&sx<W+120)drawLampGlow(sx+2,GROUND-166,82,.78);}}ctx.restore();}
function drawScaryDepth(){if(scene!=='play')return;ctx.save();const danger=clamp((100-state.sanity)/100,0,1);if(danger>.18){const pulse=.5+.5*Math.sin(totalTime*(2.2+danger*3));ctx.globalAlpha=.05+danger*.07+pulse*.015;ctx.fillStyle='#2b161b';ctx.fillRect(0,0,W,H);}if(smiler.active&&!interior){const x=smiler.x-camera;const dir=x<W/2?1:-1;ctx.globalAlpha=.12*smiler.intensity;ctx.fillStyle=dir>0?'#000':'#000';ctx.fillRect(dir>0?W-180:0,0,180,H);}ctx.restore();}
function drawWorld(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.shadowBlur=0;ctx.clearRect(0,0,W,H);drawSky();drawOcean();drawGround();if(chapter==='ALCATRAZ')drawAlcatrazStructures();drawBuildings();drawStreetProps();drawSigns();drawDock();drawMedicalMarker();if(!interior){drawFootprints();for(const s of survivors)drawSurvivor(s);for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<1100)drawZombie(z);}drawSmiler();drawPlayer();drawRain();}else{drawInterior();drawInteriorLight();drawInteriorCharacter();}drawParticles();drawPrompt();drawLighting();drawHorrorOverlay();ctx.restore();}

function saveControlMode(v){try{localStorage.setItem('ashesofthedead_control_mode',v);}catch(e){}}
function loadControlMode(){try{const v=localStorage.getItem('ashesofthedead_control_mode');if(v==='mobile'||v==='laptop')controlMode=v;}catch(e){}updateControlUI();}
function showOnly(id){['mainMenu','characterMenu','credits','controlsOverlay','hud','cutscene','pause','ending','death','inventoryUi','infoOverlay'].forEach(x=>{if(document.getElementById(x))hide(x);});if(id)show(id);}
function beginExperience(){safeAudio();hide('privacyGate');showOnly('mainMenu');scene='menu';}
function updateIntroText(){const e=document.getElementById('cutText');if(!e)return;e.innerHTML=`${cutLines[introIndex]||cutLines[cutLines.length-1]}<small>CLICK • ENTER • SPACE TO CONTINUE</small>`;}
function advanceIntro(){if(scene!=='intro')return;introIndex++;introTimer=0;if(introIndex>=cutLines.length){scene='play';showOnly('hud');hide('cutscene');setObjective();setMessage(`Welcome, ${selectedCharacter}. You are inside Cell A-17.`,2.2);startSoundscape();return;}updateIntroText();}
function renderHUD(){const hp=document.getElementById('healthFill'),st=document.getElementById('staminaFill'),sa=document.getElementById('sanityFill');if(hp)hp.style.width=`${clamp(state.health/state.maxHealth*100,0,100)}%`;if(st)st.style.width=`${clamp(state.stamina/state.maxStamina*100,0,100)}%`;if(sa)sa.style.width=`${clamp(state.sanity/100*100,0,100)}%`;const hv=document.getElementById('healthValue'),sv=document.getElementById('staminaValue'),sav=document.getElementById('sanityValue'),av=document.getElementById('ammoText'),loc=document.getElementById('locationText'),th=document.getElementById('threatText');if(hv)hv.textContent=`${Math.ceil(state.health)}/${state.maxHealth}`;if(sv)sv.textContent=`${Math.ceil(state.stamina)}/${state.maxStamina}`;if(sav)sav.textContent=`${Math.ceil(state.sanity)}/100`;if(av)av.textContent=`AMMO ${state.ammo} / ${state.reserveAmmo}`;if(loc)loc.textContent=chapter==='ALCATRAZ'?'ALCATRAZ ISLAND':'SAN FRANCISCO';if(th)th.textContent=smiler.active?'THE SMILER IS HERE':state.sanity<45?'YOU FEEL WATCHED':state.sanity<70?'SOMETHING IS WRONG':'THE PRISON IS QUIET';}
function setObjectiveHint(){const e=document.getElementById('objectiveHint');if(!e)return;e.textContent=chapter==='ALCATRAZ'?(state.startEscaped?(state.dockPass?'GET TO THE DOCK BEACON':'SEARCH THE MEDICAL WING'):'ESCAPE CELL A-17'):'FIND TWO SURVIVORS';}
function setObjectiveFixed(){let idx=chapter==='SAN FRANCISCO'?2:(state.startEscaped?(state.dockPass?1:0):0);if(chapter==='ALCATRAZ'&&state.startEscaped&&state.dockPass&&state.beacon)idx=1;objectiveIndex=idx;const o=objectives[idx];let step=0;if(chapter==='ALCATRAZ'){if(!state.startEscaped)step=0;else if(!state.dockPass)step=1;else if(!state.beacon)step=2;else step=1;}else step=state.survivors>=2?2:1;const next=o.steps[Math.min(step,o.steps.length-1)];const e=document.getElementById('objective');if(e)e.textContent=`OBJECTIVE  ${o.title}\nNEXT STEP  ${next}`;setObjectiveHint();renderObjectives();}
function setObjective(){setObjectiveFixed();}
function spawnDust(x,y,n=5){for(let i=0;i<n;i++)particles.push({x:x+(Math.random()-.5)*20,y:y-(Math.random()*3),vx:(Math.random()-.5)*70,vy:-20-Math.random()*65,s:1+Math.random()*2,life:.22+Math.random()*.3,max:.5,c:i%3===0?'#d6c6a3':'#7c8581'});}
function spawnBlood(x,y,n=8){for(let i=0;i<n;i++)particles.push({x:x+(Math.random()-.5)*16,y:y+(Math.random()-.5)*12,vx:(Math.random()-.5)*100,vy:-20-Math.random()*100,s:1+Math.random()*2.4,life:.35+Math.random()*.45,max:.8,c:i%3===0?'#b8443d':'#6f2526'});}
function die(reason){if(scene==='death')return;scene='death';hide('hud');show('death');const e=document.getElementById('deathText');if(e)e.textContent=reason||'The darkness found you.';soundScare();}
function updateMessage(dt){if(messageTimer>0){messageTimer-=dt;if(messageTimer<=0)hide('message');}}
function updateFade(dt){if(fadeTimer>0)fadeTimer-=dt;}
function drawInterior(){const b=interior?.building||{type:'cell',name:'CELL A-17'};const wall={cell:'#4b4e4a',prison:'#50585a',station:'#566064',medical:'#6b7777',workshop:'#655d52',dock:'#66615a',police:'#596874',hospital:'#65777b',funeral:'#5a555d',hotel:'#686866',shelter:'#5e6d67',research:'#667581'}[b.type]||'#555d5a';ctx.fillStyle='#101516';ctx.fillRect(0,0,W,H);px(0,0,W,380,wall);px(0,0,W,7,'#89918b');px(0,376,W,8,'#282e2e');px(0,384,W,186,'#3a3935');for(let i=0;i<26;i++){const x=i*52+(i%2)*7;px(x,402,34,2,'#5d625d');px(x+8,430+(i%3)*26,2,2,'#70756d');if(i%4===0)px(x+18,468,3,3,'#292b29');}if(b.type==='cell'){px(70,115,330,190,'#3f4543');px(82,126,306,8,'#747b75');for(let i=0;i<8;i++){const x=96+i*36;px(x,135,6,160,'#20292a');px(x+2,138,2,154,'#707873');}px(485,130,270,125,'#4a4a43');px(510,145,190,45,'#6c6659');px(512,198,220,17,'#262826');px(520,215,180,12,'#93806a');px(546,224,15,22,'#b39b7d');px(55,335,310,10,'#272b29');px(45,330,330,5,'#646a65');px(934,108,250,192,'#464b48');px(948,120,224,165,'#353b3a');for(let i=0;i<5;i++){px(970+i*40,132,25,5,'#707771');px(975+i*40,139,15,11,'#343b39');}text('CELL A-17',640,84,18,'#eee5d0','center');text('CONCRETE • RUST • RAIN',640,104,9,'#989d98','center');px(598,382,84,188,'#1d2526');px(606,390,68,178,'#394344');px(654,448,5,5,'#ddc47a');}
else{px(55,105,330,205,'#3c4748');px(75,120,290,170,'#556265');for(let i=0;i<5;i++){px(90+i*55,136,38,58,'#263235');px(94+i*55,140,30,50,(i+b.floors||0)%3===0?'#8d825f':'#3d4a4c');}px(430,112,370,6,'#77807a');for(let i=0;i<7;i++){px(450+i*47,138,34,5,'#2f3736');px(454+i*47,145,26,16,'#59615d');}px(862,108,320,194,'#424846');px(885,125,260,150,'#2a302f');for(let i=0;i<8;i++){px(905+i*29,142,18,18,i%3===0?'#7f7050':'#424a49');}px(570,388,140,182,'#1d2425');px(577,395,126,173,'#3d4645');px(670,448,5,5,'#ddc47a');text(b.name,640,72,17,'#f0eadc','center');text('INTERIOR',640,94,9,'#9ba39d','center');}
const exitTint='rgba(188,200,190,.08)';px(34,431,180,76,'#252b2b');px(45,444,155,48,'#303837');text('EXIT',122,473,13,'#ece4d3','center');px(1066,431,180,76,'#252b2b');px(1080,444,155,48,'#303837');text('EXIT',1140,473,13,'#ece4d3','center');ctx.fillStyle=exitTint;ctx.fillRect(0,431,214,78);ctx.fillRect(1066,431,214,78);if(interior.type==='medical'){px(905,320,290,70,'#5f6a68');px(935,334,92,42,'#ece9df');px(956,340,48,30,'#a6aaa3');px(1045,338,118,35,'#303737');text('SUPPLY DESK',1055,359,10,'#f0e7d4');if(!state.dockPass){px(1050,312,112,16,'#8b7055');text('DOCK PASS',1106,324,9,'#f3dfb2','center');}}
}
function drawInteriorCharacter(){drawPlayer();if(currentChest){}for(const s of survivors){if(interior&&s.found)drawInteriorNPC(s);}}
function drawInteriorNPC(s){const x=s.x,y=GROUND-90;px(x-13,y+16,10,36,'#273031');px(x+3,y+16,10,36,'#273031');px(x-21,y+48,18,7,'#14191a');px(x+5,y+48,18,7,'#14191a');px(x-19,y-8,38,42,'#5f6e6c');px(x-11,y-26,22,21,'#d4b09a');px(x-16,y-33,32,10,'#2f2928');text(s.name,x,y-42,12,'#fff1d4','center');}
function drawSigns(){if(chapter!=='ALCATRAZ'||interior)return;const signs=[{x:3240,t:'MEDICAL WING →'},{x:4320,t:'DOCKS →'},{x:2380,t:'CELL BLOCK B'},{x:1470,t:'BLOCK A'}];for(const a of signs){const x=a.x-camera;if(x<-200||x>W+200)continue;px(x-78,GROUND-250,156,44,'#30393a');px(x-72,GROUND-244,144,32,'#69726d');text(a.t,x,GROUND-223,10,'#f2e7cf','center');}}
function drawDock(){if(chapter!=='ALCATRAZ'||interior)return;const x=4850-camera;px(x-170,GROUND-35,340,35,'#4b514e');for(let i=0;i<7;i++)px(x-150+i*48,GROUND-39,31,8,'#71746d');px(x-22,GROUND-160,45,125,'#252c2d');px(x-30,GROUND-172,61,14,'#6b726d');px(x-20,GROUND-191,41,19,'#d9c57e');glow(x,GROUND-182,105,'rgba(224,199,126,.12)','rgba(224,199,126,0)');px(x-125,GROUND-25,250,5,'#25292a');px(x-98,GROUND-9,196,8,'#171b1c');px(x-98,GROUND-9,196,3,'#7e827d');px(x-62,GROUND-74,124,30,'#4a5556');px(x-44,GROUND-102,88,30,'#5c6767');px(x-27,GROUND-126,54,26,'#65706f');px(x-9,GROUND-136,18,10,'#343b3b');text('FERRY',x,GROUND-154,13,'#eee3c7','center');if(state.dockPass&&!state.beacon){text('E  LIGHT BEACON',x,GROUND-218,12,'#ecd89f','center');}else if(state.beacon&&!state.boatEscaped){text('E  BOARD FERRY',x,GROUND-218,12,'#ecd89f','center');}}
function drawMedicalMarker(){if(chapter!=='ALCATRAZ'||interior||state.dockPass)return;const x=3570-camera;glow(x,GROUND-205,80,'rgba(230,219,172,.08)','rgba(230,219,172,0)');px(x-115,GROUND-245,230,48,'#414a49');text('DOCK PASS →',x,GROUND-222,15,'#f6e5b8','center');}
function drawFootprints(){for(const f of footprints){f.t-=1/60;const x=f.x-camera;if(f.t>0&&x>-20&&x<W+20){ctx.globalAlpha=Math.min(.38,f.t/2);px(x,f.y,8,3,'#99a09b');ctx.globalAlpha=1;}}}
function drawRain(){if(interior)return;ctx.save();ctx.globalAlpha=.4;for(let i=0;i<150;i++){const x=(i*83+totalTime*370)%W;const y=(i*47+totalTime*540)%H;line(x,y,x-6,y+16,'#9fb6bb',1);}ctx.restore();}
function drawPrompt(){const p=document.getElementById('prompt');if(!p||scene!=='play'){if(p)p.textContent='';return;}let t='';if(interior){if(Math.abs(player.x-640)<120)t='E / USE  — EXIT TO STREET';else if(currentChest)t='E / USE  — OPEN CHEST';else if(interior.id==='cellA'&&!state.startKey&&Math.abs(player.x-310)<95)t='E / USE  — SEARCH MATTRESS';else if(interior.id==='cellA'&&!state.startEscaped&&Math.abs(player.x-610)<120)t='E / USE  — UNLOCK CELL A-17';else{for(const c of chests){if(c.inside&&c.building===interior.id&&Math.abs(player.x-c.x)<105){t='E / USE  — OPEN CHEST';break;}}}}else{if(currentChest)t='E / USE  — OPEN CHEST';else if(chapter==='ALCATRAZ'&&Math.abs(player.x-4850)<200)t=state.dockPass?(state.beacon?'E / USE  — BOARD FERRY':'E / USE  — LIGHT FERRY BEACON'):'DOCK PASS REQUIRED';else if(chapter==='ALCATRAZ'&&Math.abs(player.x-3570)<260&&!state.dockPass)t='E / USE  — ENTER MEDICAL WING';else{for(const b of buildings){if(chapter==='ALCATRAZ'&&!['cellA','cellB','guard','medical','workshop','dock'].includes(b.id))continue;if(chapter==='SAN FRANCISCO'&&['cellA','cellB','guard','medical','workshop','dock'].includes(b.id))continue;const door=b.x+b.w/2;if(Math.abs(player.x-door)<120){t='E / USE  — ENTER '+b.name;break;}}for(const s of survivors){if(!s.found&&Math.abs(player.x-s.x)<100){t='E / USE  — TALK TO '+s.name;break;}}}}p.textContent=t;}
function drawLighting(){if(scene!=='play')return;ctx.save();if(!state.light){ctx.fillStyle='rgba(0,0,0,.64)';ctx.fillRect(0,0,W,H);}else{const x=player.x-camera+player.w/2,y=player.y+24;const g=ctx.createRadialGradient(x,y,10,x,y,255);g.addColorStop(0,'rgba(245,231,190,.12)');g.addColorStop(.5,'rgba(245,231,190,.035)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(x-270,y-270,540,540);}ctx.restore();}
function drawHorrorOverlay(){if(scene!=='play')return;ctx.save();if(horror.shake>0){ctx.translate((Math.random()-.5)*horror.shake,(Math.random()-.5)*horror.shake);}if(horror.flash>0){ctx.globalAlpha=Math.min(.34,horror.flash*.42);ctx.fillStyle='#efe5d3';ctx.fillRect(0,0,W,H);}if(horror.glitch>0){ctx.globalAlpha=.2;for(let i=0;i<10;i++){const y=Math.random()*H;px(0,y,W,2,i%2?'#b7c2bd':'#4d5c59');}}ctx.restore();}
function renderParticles(){for(let i=particles.length-1;i>=0;i--){const q=particles[i];q.x+=q.vx/60;q.y+=q.vy/60;q.vy+=180/60;q.life-=1/60;if(q.life<=0){particles.splice(i,1);continue;}ctx.globalAlpha=clamp(q.life/q.max,0,1);px(q.x-camera,q.y,q.s,q.s,q.c);}ctx.globalAlpha=1;}
function drawParticles(){renderParticles();}
function updateParticles(){for(let i=particles.length-1;i>=0;i--){const q=particles[i];q.x+=q.vx/60;q.y+=q.vy/60;q.vy+=160/60;q.life-=1/60;if(q.life<=0)particles.splice(i,1);}}
function damageNearestZombie(amount){let best=null,bd=120;for(const z of zombies){if(z.dead)continue;const d=Math.abs(z.x-player.x);if(d<bd){bd=d;best=z;}}if(best){best.hp-=amount;best.x+=player.facing*18;spawnBlood(best.x,GROUND-40,6);soundHit();if(best.hp<=0){best.dead=true;setMessage('INFECTED DOWN.');}}}
function useMelee(){damageNearestZombie(55);horror.shake=Math.max(horror.shake,4);}
function updateInput(){inputState.left=touch.left||keys.has('a')||keys.has('ArrowLeft');inputState.right=touch.right||keys.has('d')||keys.has('ArrowRight');inputState.run=touch.run||keys.has('Shift');inputState.jump=touch.jump;}
function keyDown(e){if(['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName))return;const k=e.key;if(['ArrowLeft','ArrowRight','ArrowUp',' ','a','d','w','A','D','W','Shift','e','E','q','Q','f','F','r','R','g','G','i','I','Tab','Escape','Enter','c','C','p','P'].includes(k))e.preventDefault();keys.add(k);if(scene==='intro'&&(k==='Enter'||k===' '||k==='ArrowRight')){advanceIntro();return;}if(scene==='play'){if(k==='e'||k==='E')interact();else if(k==='q'||k==='Q')useMelee();else if(k==='f'||k==='F'){state.light=!state.light;tone(state.light?440:140,.08,'square',.11); }else if(k==='r'||k==='R')soundReload();else if(k==='g'||k==='G'){state.grenades=Math.max(0,state.grenades-1);tone(75,.25,'square',.18);horror.shake=5;}else if(k==='i'||k==='I'){if(scene==='play'){scene='inventory';show('inventoryUi');}}else if(k==='Escape')togglePause();else if(k==='Tab'){objectivePanelOpen=!objectivePanelOpen;document.getElementById('objectivePanel').classList.toggle('open',objectivePanelOpen);}else if(k==='p'||k==='P'){showOnly('infoOverlay');renderDeviceInfo();}}
else if(k==='Escape'){if(scene==='pause')resumeGame();else if(scene==='controlsOverlay'){showOnly(scene==='controlsOverlay'?'mainMenu':'mainMenu');}else if(scene==='credits'){showOnly('mainMenu');}}
}
function keyUp(e){keys.delete(e.key);}
function onPointerMove(e){const r=canvas.getBoundingClientRect();mouse.x=(e.clientX-r.left)*W/r.width;mouse.y=(e.clientY-r.top)*H/r.height;}
function onPointerDown(e){onPointerMove(e);mouse.down=true;safeAudio();if(scene==='play'){tone(430,.035,'square',.03);if(interior===null)shootRay();}}
function onPointerUp(){mouse.down=false;}
function shootRay(){const wx=mouse.x+camera;let best=null,bd=99999;for(const z of zombies){if(z.dead)continue;const d=Math.abs(z.x-wx);if(d<bd&&d<360){bd=d;best=z;}}soundShot();player.recoil=.16;if(best){best.hp-=25;best.x+=player.facing*10;spawnBlood(best.x,GROUND-40,4);if(best.hp<=0)best.dead=true;}}
function togglePause(){if(scene==='play'){scene='pause';show('pause');}else if(scene==='pause'){resumeGame();}}
function resumeGame(){if(scene!=='pause')return;scene='play';hide('pause');show('hud');}
function restartChapter(){resetWorld();positionInsideCell();scene='intro';introIndex=0;introTimer=0;hide('pause');hide('death');hide('ending');hide('hud');show('cutscene');updateIntroText();}
function mainMenu(){scene='menu';hide('pause');hide('death');hide('ending');hide('credits');hide('characterMenu');hide('controlsOverlay');hide('hud');hide('cutscene');hide('inventoryUi');hide('infoOverlay');show('mainMenu');}
function renderDeviceInfo(){const g=document.getElementById('deviceGrid');if(!g)return;const n=navigator;g.innerHTML='';const rows=[['PLATFORM',n.platform||'Unavailable'],['BROWSER',n.userAgent],['SCREEN',`${screen.width} × ${screen.height}`],['LANGUAGE',n.language||'Unavailable'],['TIMEZONE',Intl.DateTimeFormat().resolvedOptions().timeZone||'Unavailable'],['CPU THREADS',n.hardwareConcurrency||'Unavailable'],['ONLINE',n.onLine?'ONLINE':'OFFLINE'],['TOUCH',n.maxTouchPoints||0]];rows.forEach(a=>{const d=document.createElement('div');d.className='privacyCard';d.innerHTML=`<b>${a[0]}</b>${String(a[1]).replace(/</g,'&lt;').replace(/>/g,'&gt;')}`;g.appendChild(d);});}
function bindButton(id,fn){const e=document.getElementById(id);if(e)e.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();safeAudio();fn(e);});}
function initInterface(){loadControlMode();bindButton('privacyEnter',beginExperience);bindButton('privacyDevice',()=>{beginExperience();showOnly('infoOverlay');renderDeviceInfo();});bindButton('playButton',()=>{showOnly('characterMenu');scene='menu';});bindButton('creditsButton',()=>{showOnly('credits');scene='credits';});bindButton('controlsButton',()=>{showOnly('controlsOverlay');scene='controls';updateControlUI();});bindButton('creditsBack',mainMenu);bindButton('characterBack',mainMenu);bindButton('characterControls',()=>{showOnly('controlsOverlay');scene='controls';updateControlUI();});bindButton('characterPrivacy',()=>{show('privacyGate');});document.querySelectorAll('[data-character]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();startGame(b.dataset.character);}));document.querySelectorAll('[data-control]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();setControlMode(b.dataset.control);saveControlMode(controlMode);}));bindButton('autoMode',()=>{setControlMode('auto');saveControlMode(controlMode);});bindButton('controlsBack',()=>{showOnly('mainMenu');scene='menu';});bindButton('objectiveTab',()=>{objectivePanelOpen=!objectivePanelOpen;document.getElementById('objectivePanel').classList.toggle('open',objectivePanelOpen);});bindButton('objectiveClose',()=>{objectivePanelOpen=false;document.getElementById('objectivePanel').classList.remove('open');});bindButton('resumeButton',resumeGame);bindButton('restartButton',restartChapter);bindButton('pauseMenuButton',mainMenu);bindButton('endingMenuButton',mainMenu);bindButton('deathRestartButton',restartChapter);bindButton('deathMenuButton',mainMenu);bindButton('infoClose',()=>{hide('infoOverlay');if(scene==='info')scene='menu';});bindButton('chestCloseButton',closeChest);bindButton('takeAllButton',takeAll);bindButton('sortButton',sortChest);bindButton('soundButton',()=>{soundEnabled=!soundEnabled;document.getElementById('soundButton').textContent=`SOUND: ${soundEnabled?'ON':'OFF'}`;if(soundEnabled)startSoundscape();});document.querySelectorAll('[data-touch]').forEach(b=>{const action=b.dataset.touch;b.addEventListener('pointerdown',e=>{e.preventDefault();touch[action]=true;safeAudio();if(action==='jump')tryJump();if(action==='interact')interact();if(action==='melee')useMelee();if(action==='light'){state.light=!state.light;tone(state.light?440:140,.08,'square',.1);}if(action==='inventory'){scene='inventory';show('inventoryUi');}if(action==='reload')soundReload();if(action==='fire')shootRay();});b.addEventListener('pointerup',e=>{e.preventDefault();touch[action]=false;});b.addEventListener('pointercancel',e=>{touch[action]=false;});});window.addEventListener('keydown',keyDown);window.addEventListener('keyup',keyUp);canvas.addEventListener('pointermove',onPointerMove);canvas.addEventListener('pointerdown',onPointerDown);window.addEventListener('pointerup',onPointerUp);canvas.addEventListener('contextmenu',e=>e.preventDefault());window.addEventListener('blur',()=>{keys.clear();Object.keys(touch).forEach(k=>touch[k]=false);});setControlMode(controlMode);show('privacyGate');scene='menu';}
function tick(now){const dt=Math.min(.033,Math.max(.001,(now-last)/1000));last=now;totalTime+=dt;updateInput();if(scene==='play')update(dt);else if(scene==='intro'){introTimer+=dt;if(introTimer>7.5)advanceIntro();}updateMessage(dt);updateFade(dt);updateParticles();if(scene==='play')renderHUD();drawWorld();requestAnimationFrame(tick);}
function boot(){try{initInterface();resetWorld();positionInsideCell();drawWorld();renderHUD();requestAnimationFrame(tick);}catch(err){document.body.dataset.bootError=String(err);const gate=document.getElementById('privacyGate');if(gate)gate.style.display='none';show('mainMenu');}}
boot();

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
