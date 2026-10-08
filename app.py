from flask import Flask, Response, request, jsonify

app = Flask(__name__)

GAME_HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>CASE 17 — CRIME SCENE</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#020304;color:#eee7d7;font-family:Consolas,monospace}
body{display:grid;place-items:center}
button{font:inherit;color:#eee7d7;background:#0b1012;border:1px solid #6e7673;cursor:pointer;touch-action:manipulation}
button:hover{background:#172022;border-color:#c7b98f}
button:focus-visible{outline:2px solid #dbc98f;outline-offset:3px}
.hidden{display:none!important}
#app{position:relative;width:min(100vw,1400px);aspect-ratio:16/9;overflow:hidden;background:#06090b;box-shadow:0 0 0 1px #1e2527,0 0 120px #000}
#world{position:absolute;inset:0;width:100%;height:100%;display:block;background:#071217;image-rendering:auto;image-rendering:auto;filter:saturate(.88) contrast(1.08) brightness(.92)}
.layer{position:absolute;inset:0}
.screen{display:grid;place-items:center;background:rgba(2,3,4,.76);z-index:50}
.menu{z-index:60;overflow:hidden;background:#030607}
.menuBackdrop{position:absolute;inset:0;background:linear-gradient(180deg,#03070b 0,#07151a 48%,#0d1a1c 49%,#040708 100%)}
.menuBackdrop:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 72% 20%,rgba(224,218,190,.2) 0 2%,transparent 7%),linear-gradient(180deg,transparent 45%,rgba(0,0,0,.4) 75%,rgba(0,0,0,.85))}
.menuMoon{position:absolute;right:13%;top:12%;width:130px;height:130px;border-radius:50%;background:#d0cbb9;box-shadow:0 0 100px rgba(222,214,190,.16)}
.menuMoon:after{content:"";position:absolute;inset:16px 30px 42px 18px;border-radius:50%;background:rgba(75,78,75,.25)}
.menuOcean{position:absolute;left:0;right:0;bottom:0;height:52%;background:repeating-linear-gradient(175deg,rgba(82,118,126,.08) 0 2px,transparent 2px 15px),linear-gradient(180deg,#0d2026,#04080a)}
.menuIsland{position:absolute;left:-5%;right:-5%;bottom:30%;height:31%;background:#111a1c;clip-path:polygon(0 88%,10% 72%,19% 76%,28% 55%,38% 66%,50% 40%,60% 55%,70% 35%,82% 58%,93% 70%,100% 50%,100% 100%,0 100%);filter:drop-shadow(0 12px 20px #000)}
.menuPrison{position:absolute;left:33%;bottom:30%;width:34%;height:28%;background:#1a2427;border-top:5px solid #4a5557;box-shadow:inset 0 -18px 0 rgba(0,0,0,.28)}
.menuPrison:before{content:"";position:absolute;left:4%;right:4%;top:25%;height:52%;background:repeating-linear-gradient(90deg,#2c3a3b 0 24px,#172224 24px 32px)}
.menuTower{position:absolute;left:50%;bottom:52%;width:8%;height:27%;background:#253134;border-top:8px solid #56605f;box-shadow:inset 0 -30px 0 rgba(0,0,0,.25)}
.menuTower:before{content:"";position:absolute;left:-8px;right:-8px;top:-13px;height:8px;background:#6d736e}
.menuFog{position:absolute;left:-10%;width:120%;height:18%;bottom:29%;background:linear-gradient(90deg,transparent,rgba(187,199,196,.1),transparent);filter:blur(10px);animation:fog 14s linear infinite}
.menuFog.two{bottom:39%;opacity:.55;animation-duration:21s;animation-direction:reverse}
@keyframes fog{from{transform:translateX(-12%)}to{transform:translateX(12%)}}
.menuRain{position:absolute;inset:0;opacity:.35;background:repeating-linear-gradient(106deg,transparent 0 8px,rgba(166,198,204,.13) 9px,transparent 10px 21px);background-size:20px 34px;animation:rain 1.2s linear infinite}
@keyframes rain{from{background-position:0 0}to{background-position:-20px 34px}}
.menuNoise{position:absolute;inset:0;opacity:.08;background:repeating-linear-gradient(0deg,transparent 0 3px,#fff 4px,#fff 5px,transparent 6px)}
.menuVignette{position:absolute;inset:0;background:radial-gradient(circle,transparent 28%,rgba(0,0,0,.17) 58%,rgba(0,0,0,.82) 100%)}
.menuContent{position:relative;z-index:2;max-width:780px;margin-left:9%;margin-top:-2%;text-shadow:0 2px 5px #000}
.menuKicker{font-size:12px;letter-spacing:3px;color:#8f9b98;margin-bottom:12px}
.menuLogo{font-weight:900;font-size:clamp(40px,6vw,76px);letter-spacing:7px;color:#f4ecdb;line-height:.95;text-shadow:4px 4px 0 #080b0c,0 0 28px rgba(232,221,192,.18)}
.menuTag{margin-top:14px;letter-spacing:2px;color:#aa9b77;font-size:12px}
.menuLore{max-width:680px;margin:22px 0;color:#c1c4be;line-height:1.75;font-size:14px}
.menuButtons{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.menuButtons button{min-width:190px;padding:14px 24px;letter-spacing:2px;font-weight:800}
.menuPlay{border-color:#b8aa7f;background:#15191a;color:#f5edda;box-shadow:0 0 28px rgba(214,195,138,.08)}
.menuPlay:hover{background:#232727}
.menuThreat{margin-top:21px;font-size:10px;letter-spacing:1.6px;color:#777f7b}
.menuFooter{margin-top:30px;font-size:10px;color:#646d69;letter-spacing:1px;max-width:780px}
.menuSignal{position:absolute;right:-30%;bottom:-13%;font-size:10px;color:#727c77;letter-spacing:2px}
.panel{width:min(880px,92%);max-height:92%;overflow:auto;border:1px solid #596262;background:linear-gradient(180deg,#111819,#06090a);padding:30px;box-shadow:0 25px 90px #000;position:relative}
.panel:after{content:"";position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(255,255,255,.012) 0 1px,transparent 1px 5px)}
h1{margin:0;text-align:center;letter-spacing:6px;font-size:40px;color:#efe9db;text-shadow:3px 3px #000}
.subtitle{text-align:center;color:#9ba49f;letter-spacing:2px;margin:12px auto;line-height:1.6}
.center{text-align:center}
#privacyGate{z-index:90;position:absolute;inset:0;background:rgba(0,0,0,.95);display:grid;place-items:center;padding:24px}
.privacyBox{width:min(1050px,96%);max-height:92%;overflow:auto;border:2px solid #818984;background:linear-gradient(180deg,#121817,#060908);padding:34px;box-shadow:0 0 80px #000}
.privacyTitle{font-size:clamp(26px,4vw,48px);letter-spacing:4px;font-weight:900;text-align:center;color:#f1ebdd;text-shadow:3px 3px #000}
.privacySub{text-align:center;color:#b3b8b3;letter-spacing:2px;margin:8px 0 25px}
.privacyGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.privacyCard{border:1px solid #303836;background:#0b0f0d;padding:15px;color:#c8ceca;line-height:1.5}
.privacyCard b{display:block;color:#eee9dc;letter-spacing:1px;margin-bottom:6px}
.privacyNote{margin-top:15px;border-left:4px solid #9c8d67;background:#0b100e;padding:13px;color:#a9b0aa;line-height:1.55}
.privacyActions{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:20px}
.privacyActions button{padding:13px 19px;min-width:210px}
.charSelectBox,.controlBox,.creditsBox{width:min(1000px,94%);max-height:92%;overflow:auto;border:1px solid #596363;background:linear-gradient(180deg,#111819,#070a0b);padding:28px;box-shadow:0 25px 90px #000}
.charSelectTitle{text-align:center;font-size:29px;letter-spacing:4px;color:#eee7d8}
.charSelectSub{text-align:center;color:#929c97;max-width:820px;margin:9px auto 23px;line-height:1.55}
.charCards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.charCard{min-height:220px;text-align:left;padding:22px;background:linear-gradient(160deg,#12191a,#080c0d);position:relative;overflow:hidden}
.charCard:before{content:"";position:absolute;inset:0;background:linear-gradient(140deg,transparent 40%,rgba(255,255,255,.025));pointer-events:none}
.charCard .name{display:block;font-size:26px;letter-spacing:4px;color:#f0e6cf;text-shadow:2px 2px #000}
.charCard .meta{display:block;color:#9ba49f;margin-top:14px;line-height:1.7;font-size:11px}
.charCard .skill{display:inline-block;margin-top:30px;padding:7px 10px;border:1px solid #5c6660;color:#d9ceae;font-size:10px;letter-spacing:1px}
.charCard:hover{transform:translateY(-2px);border-color:#b7aa86}
.controlGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:22px 0}
.controlGrid button{padding:25px;text-align:left;font-weight:900;letter-spacing:2px}
.controlGrid button small{display:block;font-weight:400;color:#8d9893;letter-spacing:0;margin-top:9px;line-height:1.45}
.controlGrid button.selected{border-color:#dbc68f;background:#1a1d1a;box-shadow:inset 0 0 0 1px #dbc68f,0 0 22px rgba(218,198,143,.08)}
.creditsBox{text-align:center;line-height:1.7;color:#b3bbb6}
.creditsBox .creditsName{font-size:24px;color:#efe5cd;letter-spacing:2px}
.creditsBox .creditsQuote{font-size:18px;color:#d4c9aa;max-width:760px;margin:22px auto}
.topHud{position:absolute;left:0;right:0;top:0;display:flex;justify-content:space-between;padding:14px 18px;z-index:12;background:linear-gradient(180deg,rgba(2,4,4,.74),transparent)}
.hudGroup{min-width:260px}.hudGroup.right{text-align:right}.hudLabel{font-size:10px;letter-spacing:2px;color:#7f8883}.hudVal{font-size:12px;color:#ebe5d7}.bar{height:7px;width:210px;background:#131a1a;border:1px solid #283130;margin:4px 0 8px}.fill{height:100%}.hp{background:#9d4e4e}.st{background:#9c8b55}.san{background:#667e72}
#objectiveTab{position:absolute;right:18px;top:97px;z-index:16;padding:11px 14px;font-size:10px;letter-spacing:1px}
#objectivePanel{position:absolute;right:18px;top:144px;width:min(470px,calc(100% - 36px));max-height:65%;overflow:auto;z-index:18;background:rgba(6,9,9,.96);border:1px solid #6c7470;box-shadow:0 24px 70px #000;padding:15px;display:none}
#objectivePanel.open{display:block}
.objectiveHead{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid #2b3331;padding-bottom:9px;margin-bottom:10px}.objectiveTitle{letter-spacing:3px;font-weight:900}.objectiveClose{width:38px;height:38px}.objectiveItem{padding:11px;border:1px solid #27302f;background:#0c1211;margin-bottom:8px}.objectiveItem.current{border-color:#a79569}.objectiveItem.done{opacity:.62}.step{display:block;color:#919b95;font-size:11px;line-height:1.6;margin-top:4px}.step.active{color:#efe2c4}
#message{position:absolute;left:50%;bottom:68px;transform:translateX(-50%);max-width:75%;z-index:30;padding:10px 16px;background:rgba(5,8,8,.92);border:1px solid #7b827d;color:#ece4cf;text-align:center;line-height:1.45;box-shadow:0 15px 35px #000}
#prompt{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);z-index:31;padding:10px 15px;background:rgba(7,10,10,.94);border:1px solid #b4a173;color:#f1e4c5;font-weight:900;letter-spacing:1px;white-space:nowrap}
#warningText{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:34;color:#f0e7d3;font-size:28px;letter-spacing:5px;text-shadow:4px 4px #000,0 0 20px rgba(255,255,255,.3);opacity:0;transition:opacity .15s;text-align:center}
#scare{position:absolute;inset:0;z-index:80;pointer-events:none;display:none;background:rgba(145,0,0,.16)}
#scare.show{display:block}.scareFace{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:320px;height:390px;background:#050606;clip-path:polygon(50% 0,82% 13%,100% 44%,88% 100%,12% 100%,0 44%,18% 13%);animation:scarePop .62s steps(3,end)}
.scareFace:before,.scareFace:after{content:"";position:absolute;top:125px;width:56px;height:20px;background:#f5f0dc;box-shadow:0 0 18px #fff}.scareFace:before{left:66px}.scareFace:after{right:66px}.scareMouth{position:absolute;left:80px;right:80px;bottom:80px;height:72px;background:#efe6d4;clip-path:polygon(0 0,100% 0,82% 60%,50% 100%,18% 60%)}
@keyframes scarePop{0%{transform:translate(-50%,-50%) scale(.2);opacity:0}20%{transform:translate(-50%,-50%) scale(1.1);opacity:1}45%{transform:translate(-50%,-50%) scale(.94)}100%{transform:translate(-50%,-50%) scale(1);opacity:1}}
#fade{position:absolute;inset:0;background:#000;z-index:70;opacity:0;pointer-events:none;transition:opacity .55s}
#mobileControls{position:absolute;inset:0;z-index:35;pointer-events:none}
.mobileCluster{position:absolute;bottom:20px;display:grid;grid-template-columns:repeat(3,56px);gap:8px;pointer-events:auto}.mobileCluster.left{left:18px}.mobileCluster.right{right:18px;grid-template-columns:repeat(3,56px)}
.mobileCluster button{width:56px;height:56px;background:rgba(8,12,12,.72);border-color:#8e938c;font-size:11px}.mobileCluster .wide{grid-column:span 2}
#deviceOverlay{z-index:75}.deviceGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.deviceCard{border:1px solid #303735;background:#0c1010;padding:12px}.deviceCard b{display:block;color:#8d9892;font-size:10px;letter-spacing:1px}.deviceCard span{display:block;margin-top:6px;color:#e4e7e2;word-break:break-word;font-size:13px}
#cutscene{z-index:65;background:#020303;display:grid;place-items:center;padding:45px;text-align:center}.cutWrap{max-width:900px}.cutKicker{font-size:11px;color:#7d8782;letter-spacing:3px}.cutMain{font-size:clamp(22px,3vw,38px);line-height:1.55;color:#eae3d5;margin:22px 0}.cutHint{font-size:10px;color:#747e78;letter-spacing:1px}
#hud{z-index:20;pointer-events:none}#hud button,#hud .objectivePanel{pointer-events:auto}
.pixelOverlay{position:absolute;inset:0;pointer-events:none;z-index:19;background:repeating-linear-gradient(0deg,rgba(255,255,255,.014) 0 1px,transparent 1px 4px);mix-blend-mode:screen;opacity:.78;mix-blend-mode:overlay}

#scare.show{animation:screenPanic .08s steps(2,end) infinite;background:rgba(120,0,0,.28)}
#scare[data-variant="1"] .scareFace{filter:contrast(1.8) invert(.05);transform:translate(-50%,-50%) scale(1.18)}
#scare[data-variant="2"] .scareFace{width:430px;height:470px;filter:contrast(1.6)}
#scare[data-variant="3"] .scareFace{width:520px;height:520px;filter:blur(.3px) contrast(2)}
@keyframes screenPanic{0%{filter:none}50%{filter:contrast(1.5) brightness(.65)}100%{filter:none}}

@media(max-width:760px){#app{width:100vw;aspect-ratio:auto;height:100%}.charCards,.privacyGrid,.deviceGrid,.controlGrid{grid-template-columns:1fr}.menuContent{margin:0 auto;width:92%;}.menuLogo{font-size:41px;letter-spacing:4px}.menuButtons button{width:100%}.panel{padding:20px}.privacyBox{padding:22px}.menuLore{font-size:12px}.hudGroup{min-width:0}.bar{width:130px}.mobileCluster{bottom:13px}.mobileCluster.left{left:10px}.mobileCluster.right{right:10px}.mobileCluster button{width:52px;height:52px}}

.menuContent:before{content:"";position:absolute;left:-28px;top:-18px;width:4px;height:230px;background:#b8aa7f;box-shadow:0 0 22px rgba(218,199,145,.2)}
.menuLogo:after{content:"";display:block;width:230px;height:2px;background:#927e57;margin-top:14px;box-shadow:0 0 15px rgba(194,166,107,.25)}
.charCard:after{content:"";position:absolute;left:0;bottom:0;width:100%;height:4px;background:linear-gradient(90deg,transparent,#b2a67f,transparent);opacity:.4}
.controlGrid button:after{content:"";position:absolute;right:10px;top:10px;width:6px;height:6px;background:#75694f;box-shadow:0 0 10px #b5a16d}
.panel button{min-height:42px;padding:10px 15px}
#message{font-size:12px;letter-spacing:.4px}
#warningText:before{content:"// NIGHTWATCH //";display:block;font-size:9px;letter-spacing:3px;color:#8f8f84;margin-bottom:8px}

#mapStrip{position:absolute;left:50%;top:58px;transform:translateX(-50%);width:min(560px,42vw);height:24px;background:rgba(4,7,7,.78);border:1px solid #3c4542;z-index:15;overflow:hidden}
#mapStrip .mapLine{position:absolute;left:10px;right:10px;top:11px;height:2px;background:#59625d}
#mapStrip .mapPlayer{position:absolute;top:6px;width:9px;height:12px;background:#eee5cf;box-shadow:0 0 8px rgba(238,229,207,.5)}
#mapStrip .mapPoint{position:absolute;top:8px;width:5px;height:8px;background:#81785e}
#mapStrip .mapDanger{position:absolute;top:7px;width:6px;height:10px;background:#9d4e4e}

/* POLISHED NIGHTFALL UI */
#app{border:1px solid #303938;box-shadow:0 0 0 1px #070a0a,0 0 80px #000,0 0 160px rgba(80,95,91,.12)}
.menuBackdrop{background:linear-gradient(180deg,#020507 0,#071116 38%,#101c1e 57%,#030607 100%)}
.menuBackdrop:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.018) 0 1px,transparent 1px 5px),radial-gradient(circle at 50% 50%,transparent 35%,rgba(0,0,0,.5) 100%);pointer-events:none}
.menuMoon{width:150px;height:150px;right:12%;top:10%;background:#d6d0b8;box-shadow:0 0 20px rgba(220,215,194,.28),0 0 100px rgba(218,208,178,.12)}
.menuMoon:before{content:"";position:absolute;inset:22px 30px 28px 45px;border-radius:50%;background:rgba(76,79,75,.22);box-shadow:-22px 34px 0 -8px rgba(76,79,75,.15),15px -14px 0 -10px rgba(76,79,75,.16)}
.menuIsland{filter:drop-shadow(0 20px 28px #000);background:#0a1214;clip-path:polygon(0 88%,8% 79%,15% 81%,24% 65%,31% 70%,39% 49%,47% 61%,54% 42%,63% 54%,71% 35%,80% 55%,89% 63%,100% 45%,100% 100%,0 100%)}
.menuPrison{background:#151f21;border-top:5px solid #65706e;box-shadow:inset 0 -22px 0 rgba(0,0,0,.35),0 -8px 30px rgba(93,105,102,.08)}
.menuPrison:after{content:"";position:absolute;left:48%;top:-34%;width:5%;height:42%;background:#263234;box-shadow:0 0 0 4px #3e4a4b}
.menuTower{background:#202c2f;box-shadow:inset 0 -30px 0 rgba(0,0,0,.35),0 0 30px rgba(87,103,102,.08)}
.menuFog{opacity:.8;filter:blur(12px)}
.menuContent{max-width:900px;width:min(900px,88%);margin:0 auto;padding:34px 42px 34px;border-left:1px solid rgba(164,154,119,.28);background:linear-gradient(90deg,rgba(2,5,6,.72),rgba(2,5,6,.25),transparent);backdrop-filter:blur(1px)}
.menuKicker{color:#a29d88;font-weight:700}
.menuLogo{font-size:clamp(44px,6.8vw,88px);letter-spacing:8px;line-height:.88;color:#f3ead6;text-shadow:4px 4px 0 #050708,0 0 32px rgba(236,223,190,.16)}
.menuTag{font-size:11px;color:#c1b28d;letter-spacing:3px}
.menuLore{max-width:720px;color:#c8cbc5;border-left:3px solid #70634a;padding-left:16px;line-height:1.8}
.menuButtons{gap:12px}
.menuButtons button{position:relative;min-width:205px;padding:15px 26px;background:rgba(10,15,16,.82);border-color:#46504e;letter-spacing:2.5px;transition:.16s transform,.16s border-color,.16s background}
.menuButtons button:hover{transform:translateY(-2px);border-color:#c0b38c;background:#151c1d}
.menuPlay{border-color:#a99b74!important;background:linear-gradient(180deg,#242a29,#111615)!important;box-shadow:inset 0 0 0 1px rgba(215,199,151,.18),0 8px 25px rgba(0,0,0,.35)}
.menuPlay:before{content:"▶";margin-right:10px;color:#c9bb91}
.menuThreat{color:#a9a596;margin-top:24px}
.menuFooter{color:#7d8781}
.menuSignal{color:#8f958d}
.charSelectBox,.controlBox,.creditsBox,.panel{border-color:#4d5855;background:linear-gradient(180deg,rgba(19,26,26,.98),rgba(5,8,9,.99));box-shadow:0 30px 100px #000,inset 0 1px 0 rgba(255,255,255,.035)}
.charSelectTitle{font-weight:900;text-shadow:3px 3px #000}
.charCard{border-color:#303a39;background:linear-gradient(145deg,#131b1c,#080c0d);min-height:245px;transition:.16s transform,.16s border-color,.16s box-shadow}
.charCard:hover{transform:translateY(-4px);border-color:#aaa07c;box-shadow:0 12px 30px rgba(0,0,0,.45)}
.charCard .name{font-size:28px}
.charCard .skill{border-color:#6e705f;background:#111615}
#hud .topHud{background:linear-gradient(180deg,rgba(1,3,4,.92),rgba(1,3,4,.25),transparent);border-bottom:1px solid rgba(117,126,120,.08)}
#mapStrip{position:absolute;left:50%;top:12px;transform:translateX(-50%);width:min(520px,42vw);height:35px;background:rgba(5,8,8,.82);border:1px solid #303a38;box-shadow:0 8px 24px #000;z-index:15}
#mapStrip .mapLine{position:absolute;left:12px;right:12px;top:17px;height:2px;background:#47514e}
#mapStrip .mapPlayer{position:absolute;top:12px;width:8px;height:8px;background:#e2d3a9;box-shadow:0 0 9px #e2d3a9;transform:translateX(-50%)}
#mapPoints{position:absolute;inset:0}
.mapPoint{position:absolute;top:13px;width:6px;height:6px;background:#727b76;border:1px solid #a4aa9e;transform:translateX(-50%)}
.mapPoint.active{background:#d1bd86;box-shadow:0 0 8px rgba(215,190,130,.7)}
#objectiveTab,#soundButton{border-color:#59615d!important;background:rgba(6,10,10,.88)!important;box-shadow:0 8px 20px #000}
#message,#prompt{box-shadow:0 12px 35px #000,inset 0 1px rgba(255,255,255,.04)}
.pixelOverlay{opacity:.32;background:repeating-linear-gradient(0deg,rgba(255,255,255,.02) 0 1px,transparent 1px 3px)}
@media(max-width:760px){#mapStrip{width:52vw}.menuContent{padding:18px 20px;margin:0 auto;width:92%}.menuLogo{font-size:42px;letter-spacing:4px}}

<style>
.menuContent{align-self:center;justify-self:center;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);max-height:86%;overflow:auto;text-align:center;border:1px solid rgba(154,145,112,.24);background:linear-gradient(180deg,rgba(2,5,6,.68),rgba(2,5,6,.38));box-shadow:0 25px 80px rgba(0,0,0,.45)}
.menuContent:before{left:0;top:0;height:100%;width:3px}.menuLore{margin-left:auto;margin-right:auto;text-align:left}.menuButtons{justify-content:center}.menuFooter,.menuSignal{position:static}.menuSignal{margin-top:12px}.menuLogo:after{margin-left:auto;margin-right:auto}

/* NIGHTFALL 2.0 — cinematic presentation overhaul */
#app{border-radius:10px;box-shadow:0 0 0 1px rgba(170,183,170,.18),0 25px 100px rgba(0,0,0,.92),0 0 180px rgba(65,95,100,.12);isolation:isolate}
#world{image-rendering:auto;image-rendering:crisp-edges}
#app:after{content:"";position:absolute;inset:0;pointer-events:none;z-index:18;background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.18) 72%,rgba(0,0,0,.72) 100%),linear-gradient(180deg,rgba(120,150,150,.035),transparent 35%,rgba(0,0,0,.16));mix-blend-mode:multiply}
.menu{background:#020506!important}
.menuBackdrop{filter:saturate(.82) contrast(1.12);transform:scale(1.03);animation:menuDrift 18s ease-in-out infinite alternate}
.menuMoon{box-shadow:0 0 40px rgba(220,220,196,.2),0 0 180px rgba(150,180,180,.08);filter:contrast(1.1)}
.menuContent{backdrop-filter:blur(2px);background:linear-gradient(180deg,rgba(3,6,7,.5),rgba(3,6,7,.18));border:1px solid rgba(160,169,159,.14);padding:30px 34px;box-shadow:0 25px 80px rgba(0,0,0,.35)}
.menuLogo{text-shadow:0 3px 0 #050707,0 0 25px rgba(205,197,165,.16);font-weight:900}
.menuLore{max-width:610px;text-shadow:0 1px 5px #000}
.menuButtons button{position:relative;overflow:hidden;background:linear-gradient(180deg,rgba(24,31,31,.94),rgba(8,12,13,.98));border-color:#58615c;box-shadow:inset 0 1px rgba(255,255,255,.06),0 7px 20px rgba(0,0,0,.22);transition:.18s transform,.18s border-color,.18s background}
.menuButtons button:hover{transform:translateY(-2px);background:linear-gradient(180deg,#27302f,#0a0e0f);border-color:#c5b98f}
.menuButtons button:active{transform:translateY(1px)}
.menuButtons button:before{content:"";position:absolute;left:-30%;top:0;width:30%;height:100%;background:linear-gradient(90deg,transparent,rgba(230,224,198,.16),transparent);transform:skewX(-20deg);transition:.5s}
.menuButtons button:hover:before{left:110%}
#hud{filter:drop-shadow(0 2px 5px rgba(0,0,0,.75))}
#message,#warningText,#prompt{backdrop-filter:blur(5px);text-shadow:0 2px 5px #000}
#message{border-color:rgba(175,184,174,.34)!important;background:rgba(4,7,7,.78)!important}
#warningText{background:linear-gradient(90deg,rgba(70,8,8,.78),rgba(18,5,5,.45))!important;border-left:2px solid #b76558!important;letter-spacing:1.5px}
#prompt{background:rgba(4,7,7,.76)!important;border:1px solid rgba(180,184,170,.25);padding:8px 12px!important}
#mapStrip{box-shadow:0 5px 18px rgba(0,0,0,.35),inset 0 0 20px rgba(130,155,150,.05);backdrop-filter:blur(4px)}
#mobileControls button{border-radius:12px!important;box-shadow:0 8px 24px rgba(0,0,0,.35),inset 0 1px rgba(255,255,255,.08);backdrop-filter:blur(6px)}
@keyframes menuDrift{from{transform:scale(1.03) translate3d(-8px,0,0)}to{transform:scale(1.06) translate3d(8px,-5px,0)}}
@media(max-width:760px){.menuContent{padding:24px 20px;max-height:88vh;overflow:auto}.menuLogo{font-size:clamp(30px,10vw,48px)}#app:after{background:radial-gradient(ellipse at center,transparent 40%,rgba(0,0,0,.68) 100%)}}
</style>
</style>

<style>
/* CASE 17 crime-noir visual treatment */
#app:after{content:"";position:absolute;inset:0;pointer-events:none;z-index:11;background:linear-gradient(180deg,rgba(12,20,22,.08),transparent 22%,transparent 78%,rgba(0,0,0,.3)),repeating-linear-gradient(0deg,rgba(255,255,255,.018) 0 1px,transparent 1px 4px);mix-blend-mode:screen;opacity:.5}
.menuLogo{letter-spacing:9px}.menuTag{color:#c1a86c}.menuThreat:before{content:"CASE FILE 17  •  MURDER / EXTORTION / MISSING PERSON";display:block;color:#9d4b45;margin-bottom:7px}
</style>
</head>
<body>
<div id="app">
<canvas id="world" width="1400" height="788"></canvas>
<div id="mainMenu" class="layer menu">
<div class="menuBackdrop"><div class="menuMoon"></div><div class="menuOcean"></div><div class="menuIsland"></div><div class="menuPrison"></div><div class="menuTower"></div><div class="menuFog"></div><div class="menuFog two"></div><div class="menuRain"></div><div class="menuVignette"></div><div class="menuNoise"></div></div>
<div class="menuContent"><div class="menuKicker">NIGHTWATCH // ALCATRAZ ESCAPE PROTOCOL</div><div class="menuLogo">ESCAPE ALCATRAZ</div><div class="menuTag">NIGHTFALL • ALCATRAZ ISLAND • ESCAPE PROTOCOL</div><div class="menuLore">You wake inside Cell A-17 after the last emergency broadcast dies. The prison is dark, the sea is violent, and something is moving through the cell blocks. Reach the dock before dawn — but first restore power, find the ferry pass, and survive the island.</div><div class="menuButtons"><button id="playButton" class="menuPlay">PLAY</button><button id="creditsButton">CREDITS</button><button id="controlsButton">CONTROL MODE</button></div><div class="menuThreat">HEADPHONES RECOMMENDED • SOME SOUNDS AREN'T AMBIENCE • NIGHT MODE ACTIVE</div><div class="menuThreat" style="color:#b9a77b">DYNAMIC THREAT DIRECTOR • LIMITED LIGHT • NO SAFE ROOM • 3 FLOORS OF HELL</div><div class="menuFooter">JULIA • MAY • YUMI • LARGE 2D ALCATRAZ RECONSTRUCTION • SURVIVAL HORROR</div><div class="menuSignal">SIGNAL // <b>UNSTABLE</b></div></div>
</div>
<div id="characterMenu" class="layer screen hidden"><div class="charSelectBox"><div class="charSelectTitle">CHOOSE YOUR DETECTIVE</div><div class="charSelectSub">No portraits. Choose by profile. Your detective changes visual styling and small gameplay bonuses.</div><div class="charCards"><button class="charCard" data-character="Julia"><span class="name">JULIA</span><span class="meta">FIELD DETECTIVE<br>Balanced health and stamina<br>Calm under pressure</span><span class="skill">BALANCED</span></button><button class="charCard" data-character="May"><span class="name">MAY</span><span class="meta">CRIME SCENE DETECTIVE<br>Faster movement and searching<br>Quick investigation</span><span class="skill">AGILITY</span></button><button class="charCard" data-character="Yumi"><span class="name">YUMI</span><span class="meta">INTELLIGENCE DETECTIVE<br>Steady aim and stronger sanity<br>Technical problem solver</span><span class="skill">TECHNICAL</span></button></div><div class="center" style="margin-top:18px"><button id="characterBack">BACK</button><button id="characterControls">CONTROL MODE</button></div></div></div>
<div id="credits" class="layer screen hidden"><div class="creditsBox"><h1>CREDITS</h1><p class="creditsName">Mayumi Alingarog (Yumi, Mimi, Yumimi)</p><p class="creditsQuote">“A wonderful classmate and developer who is very helpful, kind, respectful, creative, and encouraging.”</p><p>Thank you, Mayumi, for inspiring me to join Scream Jam 2026 and for showing me that making a game can be scary, stressful, funny, and genuinely fun.</p><p>This game is inspired by the spirit of small side-scrolling horror jam games, including the feeling of getting trapped somewhere and slowly learning how to escape.</p><button id="creditsBack">BACK</button></div></div>
<div id="controlsOverlay" class="layer screen hidden"><div class="controlBox"><div class="charSelectTitle">CONTROL MODE</div><div class="charSelectSub">Pick one. The selected mode stays active during gameplay.</div><div class="controlGrid"><button data-control="laptop" id="laptopMode">LAPTOP / DESKTOP<small>OUTSIDE: A / D + W / SPACE • INSIDE: W A S D / arrows move • E interact • mouse aim/fire • F flashlight • R reload • Q melee</small></button><button data-control="mobile" id="mobileMode">MOBILE / TOUCH<small>Virtual movement and action buttons • touch aim • FIRE / USE / JUMP / LIGHT / BAG</small></button></div><div class="center"><button id="autoMode">AUTO DETECT</button> <button id="controlsBack">BACK</button><div id="controlStatus" class="subtitle"></div></div></div></div>
<div id="hud" class="layer hidden"><div id="mapStrip"><div class="mapLine"></div><div id="mapPlayer" class="mapPlayer"></div><div id="mapPoints"></div></div><div class="topHud"><div class="hudGroup"><div class="hudLabel">HEALTH <span id="healthValue"></span></div><div class="bar"><div id="healthFill" class="fill hp"></div></div><div class="hudLabel">STAMINA <span id="staminaValue"></span></div><div class="bar"><div id="staminaFill" class="fill st"></div></div><div class="hudLabel">SANITY <span id="sanityValue"></span></div><div class="bar"><div id="sanityFill" class="fill san"></div></div></div><div class="hudGroup right"><div class="hudLabel">LOCATION</div><div id="locationText" class="hudVal">ALCATRAZ ISLAND</div><div id="threatText" class="hudVal">THE PRISON IS QUIET</div><div id="ammoText" class="hudVal">AMMO 12 / 12</div></div></div><button id="objectiveTab">OBJECTIVES +</button><div id="objectivePanel"><div class="objectiveHead"><div><div class="objectiveTitle">OBJECTIVES</div><div id="objectiveHint" class="step active">CURRENT GOAL</div></div><button id="objectiveClose" class="objectiveClose">×</button></div><div id="objectiveList"></div></div><button id="soundButton" style="position:absolute;right:18px;top:58px;z-index:16;padding:9px 12px;font-size:10px">SOUND: ON</button><div id="message" class="hidden"></div><div id="prompt"></div></div>
<div id="cutscene" class="layer hidden"><div class="cutWrap"><div class="cutKicker">CASE FILE 07 // ALCATRAZ ISLAND</div><div id="cutMain" class="cutMain"></div><div class="cutHint">ENTER / SPACE / RIGHT ARROW TO CONTINUE</div></div></div>
<div id="pause" class="layer screen hidden"><div class="panel"><h1>PAUSED</h1><p class="subtitle">The island is still there when you stop looking.</p><div class="center"><button id="resumeButton">RESUME</button> <button id="restartButton">RESTART</button> <button id="pauseMenuButton">MAIN MENU</button></div></div></div>
<div id="ending" class="layer screen hidden"><div class="panel"><h1>ESCAPE</h1><p id="endingText" class="subtitle"></p><div class="center"><button id="endingMenuButton">MAIN MENU</button></div></div></div>
<div id="death" class="layer screen hidden"><div class="panel"><h1 style="color:#bc5955">THE DARKNESS FOUND YOU</h1><p id="deathText" class="subtitle"></p><div class="center"><button id="deathRestartButton">TRY AGAIN</button><button id="deathMenuButton">MAIN MENU</button></div></div></div>
<div id="inventoryUi" class="layer screen hidden"><div class="panel"><h1 style="font-size:30px">CHEST INVENTORY</h1><div class="subtitle">TAKE ITEMS • SORT • CLOSE</div><div id="chestSlots" class="privacyGrid"></div><div class="center" style="margin-top:18px"><button id="takeAllButton">TAKE ALL</button><button id="sortButton">SORT</button><button id="chestCloseButton">CLOSE</button></div></div></div>
<div id="deviceOverlay" class="layer screen hidden"><div class="panel"><h1 style="font-size:26px">NIGHTWATCH DEVICE RECORD</h1><div id="deviceGrid" class="deviceGrid" style="margin-top:18px"></div><div class="center" style="margin-top:18px"><button id="infoClose">CLOSE</button></div></div></div>
<div id="fade"></div><div id="warningText"></div><div id="scare"><div class="scareFace"><div class="scareMouth"></div></div></div><div class="pixelOverlay"></div>
<div id="mobileControls" class="hidden"><div class="mobileCluster left"><button data-touch="left">◀</button><button data-touch="right">▶</button><button class="wide" data-touch="run">RUN</button></div><div class="mobileCluster right"><button data-touch="up">▲</button><button data-touch="down">▼</button><button data-touch="jump">JUMP</button><button data-touch="interact">USE</button><button data-touch="melee">MELEE</button><button data-touch="light">LIGHT</button><button data-touch="inventory">BAG</button><button data-touch="reload">RELOAD</button><button class="wide" data-touch="fire">FIRE</button></div></div>
<div id="privacyGate"><div class="privacyBox"><div class="privacyTitle">NIGHTWATCH SECURITY TERMINAL</div><div class="privacySub">ESCAPE ALCATRAZ • DEVICE & PRIVACY NOTICE</div><div class="privacyGrid"><div class="privacyCard"><b>WHAT MAY BE DISPLAYED</b>Browser and platform information, screen size, language, timezone, online state, network hints, CPU thread count, touch support, battery data when available, and the network address seen by the game server.</div><div class="privacyCard"><b>WHAT IS NOT READ</b>Passwords, personal files, photos, contacts, saved documents, account contents, and arbitrary private files are not read by this game.</div><div class="privacyCard"><b>PERMISSIONS</b>Location, camera, and microphone require separate browser permission. This game does not silently grant those permissions.</div><div class="privacyCard"><b>FICTIONAL SURVEILLANCE</b>CCTV warnings, The Smiler, tracking messages, fourth-wall events, and horror-terminal events are fictional game elements unless the interface specifically labels information as browser or server information.</div></div><div class="privacyNote">The server only sees the network address that reaches it. A proxy, VPN, carrier network, or hosting layer can change the address shown. This game is entertainment, not a security diagnostic.</div><div class="privacyActions"><button id="privacyEnter">ENTER ESCAPE ALCATRAZ</button><button id="privacyDevice">VIEW DEVICE RECORD</button></div></div></div>
</div>
<script>
const canvas=document.getElementById('world');
const ctx=canvas.getContext('2d');
ctx.imageSmoothingEnabled=false;
const W=1400,H=788,GROUND=612;
const WORLD={ALCATRAZ:52000,SF:30000};
const WORLD_HEIGHT={ALCATRAZ:28000,SF:19000};
const keys=new Set();
const touch={left:false,right:false,up:false,down:false,run:false,jump:false,interact:false,fire:false,melee:false,light:false,inventory:false,reload:false};
const mouse={x:W/2,y:H/2,down:false};
const inputState={left:false,right:false,run:false,jump:false};
const player={x:0,y:0,w:38,h:76,vx:0,vy:0,facing:1,onGround:true,coyote:0,jumpBuffer:0,jumps:2,anim:0,stepTimer:0,landTimer:0,recoil:0,flashStep:0,lean:0,air:0};
const state={health:100,maxHealth:100,stamina:100,maxStamina:100,sanity:100,ammo:10,reserveAmmo:36,grenades:2,light:true,battery:100,startKey:false,startEscaped:false,dockPass:false,powerRestored:false,radioSignal:false,beacon:false,boatEscaped:false,survivors:0,alarm:false,finalChase:false,inventory:{bandage:2,food:2,scrap:3,ammo_9mm:48,key:0,dockPass:0,fuse:0,radioPart:0}};
const crime={heat:0,evidence:0,cash:0,weaponFound:false,radioFound:false,caseSolved:false,policeTimer:0,sceneTimer:0,witness:false,deadBodySeen:false,clueFlash:0,suspect:null};

let scene='menu';
let chapter='ALCATRAZ';
let selectedCharacter='Julia';
let controlMode='laptop';
let last=performance.now();
let totalTime=0;
let camera=0;
let cameraY=0;
let interior=null;
let interiorPhase=0;
let floorTransitionLock=0;
let jumpscareVariant=0;
let fadeBusy=false;
let messageTimer=0;
let introIndex=0;
let introTimer=0;
let objectiveIndex=0;
let objectivePanelOpen=false;
let currentChest=null;
let chestData=[];
let survivors=[];
let zombies=[];
let interiorZombies=[];
let difficulty=1;let threatLevel=0;let encounterTimer=11;let totalKills=0;let lastDamageTime=0;let lowHealthWarned=false;
let dread={eventTimer:5,phantomTimer:0,phantomX:0,phantomY:0,phantomAlpha:0,heartbeat:0,ambushCooldown:0,roomEnteredAt:0};
let horrorDirector={timer:7,phase:'quiet',intensity:0,noise:0,lockdown:0,stalker:null,eventId:0,warningTimer:0,doorSlam:0,hunt:0,huntMessage:0};
let hiding=false;let wardenSpawned=false;
let particles=[];
let footprints=[];
let rainDrops=[];
let transitionKind='';
let soundEnabled=true;
let audioCtx=null;
let masterGain=null;
let musicGain=null;
let sfxGain=null;
let rainGain=null;
let musicTimer=null;
let rainTimer=null;
let footstepsTimer=0;
let scareTimer=14;
let tabAway=false;
let lastCursorMove=0;
let cursorMoved=false;
let smiler={active:false,x:0,timer:0,cooldown:18,intensity:0};
let horror={shake:0,flash:0,glitch:0,warning:0,blackout:0};
let endingTriggered=false;
const introLines=[
'CASE 17 — 11:47 PM',
'You wake inside a locked evidence room after a violent prison murder. Rain hits the bars. A body is missing.',
'Your detective badge is scratched. Your radio is dead. Someone has taken the murder weapon.',
'Under a stained mattress you find a brass key — and a blood-covered photograph.',
'Outside is a crime scene sealed by a failed security system. Whoever did this is still inside.',
'Find the evidence. Identify the killer. Stay alive long enough to get the truth out.'
];
const objectives=[
{title:'CASE 17 — THE MISSING BODY',steps:['Search Cell A-17 for the brass key and photograph.','Collect the blood trail evidence.','Find the missing murder weapon.','Identify the masked suspect.']},
{title:'BREAK THE LOCKDOWN',steps:['Search the police evidence room.','Recover the stolen radio.','Reach the communications room.','Transmit the case file before the police lockdown closes.']},
{title:'THE KILLER IS STILL HERE',steps:['Reach the emergency exit.','Survive the suspect encounter.','Get the evidence off the island.']}
];
const landmarkData=[
{name:'CELLHOUSE',x:950,w:1180,h:320,type:'cellhouse'},
{name:'RECREATION YARD',x:2450,w:980,h:155,type:'yard'},
{name:'DINING HALL',x:3800,w:540,h:225,type:'dining'},
{name:'GUARDHOUSE / SALLY PORT',x:4930,w:430,h:250,type:'guard'},
{name:'HOSPITAL WING',x:6200,w:720,h:270,type:'medical'},
{name:'CHAPEL / MORGUE',x:7440,w:520,h:230,type:'chapel'},
{name:'MODEL INDUSTRIES',x:8550,w:680,h:250,type:'industry'},
{name:'NEW INDUSTRIES',x:10020,w:700,h:260,type:'industry'},
{name:'POWER PLANT',x:11550,w:620,h:295,type:'power'},
{name:'UNDERGROUND ACCESS',x:12700,w:500,h:180,type:'tunnel'},
{name:'STOREHOUSE',x:13700,w:520,h:205,type:'store'},
{name:'POST EXCHANGE / OFFICERS CLUB',x:14850,w:600,h:240,type:'club'},
{name:'WATER TOWER',x:16000,w:290,h:350,type:'tower'},
{name:"WARDEN'S HOUSE",x:17150,w:620,h:260,type:'warden'},
{name:'CITADEL / WEST GATE',x:18300,w:760,h:280,type:'citadel'},
{name:'ROCKY SHORE',x:19450,w:520,h:170,type:'shore'},
{name:'LIGHTHOUSE',x:20700,w:260,h:380,type:'lighthouse'},
{name:'EMERGENCY PIER',x:21700,w:340,h:165,type:'dock'},
{name:'NORTH BATTERY',x:23800,w:760,h:300,type:'citadel'},
{name:'OLD QUARRY',x:25200,w:920,h:210,type:'industry'},
{name:'SIGNAL STATION',x:26800,w:560,h:260,type:'tower'},
{name:'EAST BOATHOUSE',x:28300,w:720,h:240,type:'store'},
{name:'CLIFF TUNNEL',x:30000,w:620,h:200,type:'tunnel'},
{name:'ABANDONED WARD',x:31800,w:780,h:280,type:'medical'},
{name:'BLACKWATER DOCK',x:33900,w:520,h:190,type:'dock'}
];
landmarkData.push(
{name:'NORTH CLIFF VILLAS',x:36500,w:900,h:300,type:'club'},
{name:'OLD PRISON FARM',x:39200,w:1100,h:340,type:'store'},
{name:'SOUTH SERVICE YARD',x:41500,w:1200,h:280,type:'industry'},
{name:'FORGOTTEN CEMETERY',x:43800,w:850,h:260,type:'chapel'},
{name:'WATCHMAN CABINS',x:46200,w:760,h:280,type:'guard'},
{name:'BLACK ROCK ESTATE',x:49000,w:1100,h:360,type:'warden'},
{name:'COASTAL WAREHOUSE',x:34500,w:1000,h:320,type:'store'},
{name:'TIDAL PUMP STATION',x:37800,w:780,h:250,type:'power'},
{name:'DERELICT CLINIC',x:40500,w:850,h:310,type:'medical'},
{name:'OLD ARMORY',x:43000,w:900,h:300,type:'industry'},
{name:'SOUTH LIGHTHOUSE',x:45500,w:300,h:420,type:'lighthouse'},
{name:'SMUGGLER COVE',x:48200,w:1000,h:240,type:'dock'});
const mapRows=[2600,5400,8200,11100,14000,16900,19800,22700,25400];
landmarkData.forEach((l,i)=>{if(l.y==null)l.y=mapRows[i%mapRows.length]+((i*733)%900);});
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function px(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));}
function line(x1,y1,x2,y2,c,w=1){ctx.strokeStyle=c;ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(Math.round(x1),Math.round(y1));ctx.lineTo(Math.round(x2),Math.round(y2));ctx.stroke();}
function poly(p,c){ctx.fillStyle=c;ctx.beginPath();ctx.moveTo(p[0][0],p[0][1]);for(let i=1;i<p.length;i++)ctx.lineTo(p[i][0],p[i][1]);ctx.closePath();ctx.fill();}
function text(t,x,y,size=12,c='#ddd',a='left'){ctx.font=`${size}px Consolas`;ctx.fillStyle=c;ctx.textAlign=a;ctx.textBaseline='alphabetic';ctx.fillText(t,Math.round(x),Math.round(y));}
function strokeRect(x,y,w,h,c,l=1){ctx.strokeStyle=c;ctx.lineWidth=l;ctx.strokeRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));}
function glow(x,y,r,inner,outer){const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,inner);g.addColorStop(1,outer);ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2);}
function hide(id){const e=document.getElementById(id);if(e)e.classList.add('hidden');}
function show(id){const e=document.getElementById(id);if(e)e.classList.remove('hidden');}
function showOnly(id){['mainMenu','characterMenu','credits','controlsOverlay','hud','cutscene','pause','ending','death','inventoryUi','deviceOverlay'].forEach(x=>hide(x));if(id)show(id);}
function setMessage(t,d=2){const e=document.getElementById('message');if(!e)return;e.textContent=t;e.classList.remove('hidden');messageTimer=d;}
function showWarning(t,d=2.3){const e=document.getElementById('warningText');if(!e)return;e.textContent=t;e.style.opacity='1';horror.warning=d;}
function resetWorld(){
 dread={eventTimer:4,phantomTimer:0,phantomX:0,phantomY:0,phantomAlpha:0,heartbeat:0,ambushCooldown:0,roomEnteredAt:0};
 horrorDirector={timer:5+Math.random()*5,phase:'quiet',intensity:0,noise:0,lockdown:0,stalker:null,eventId:0,warningTimer:0,doorSlam:0};
 state.health=100;state.maxHealth=100;state.stamina=100;state.maxStamina=100;state.sanity=100;state.ammo=10;state.reserveAmmo=36;state.grenades=2;state.light=true;state.battery=100;state.startKey=false;state.startEscaped=false;state.dockPass=false;state.powerRestored=false;state.radioSignal=false;state.beacon=false;state.boatEscaped=false;state.survivors=0;state.alarm=false;state.finalChase=false;hiding=false;wardenSpawned=false;state.inventory={bandage:1,food:1,scrap:2,ammo_9mm:36,key:0,dockPass:0,fuse:0,radioPart:0};Object.assign(crime,{heat:0,evidence:0,cash:0,weaponFound:false,radioFound:false,caseSolved:false,policeTimer:0,sceneTimer:0,witness:false,deadBodySeen:false,clueFlash:0,suspect:null});chapter='ALCATRAZ';camera=0;interior=null;interiorPhase=0;objectiveIndex=0;currentChest=null;endingTriggered=false;difficulty=1;threatLevel=0;encounterTimer=14;totalKills=0;lastDamageTime=0;lowHealthWarned=false;smiler={active:false,x:0,timer:0,cooldown:16,intensity:0};horror={shake:0,flash:0,glitch:0,warning:0,blackout:0};particles=[];footprints=[];zombies=[];survivors=[];buildAlcatrazPopulation();player.x=1250;player.y=5400;player.vx=0;player.vy=0;player.onGround=true;player.coyote=.12;player.jumpBuffer=0;player.jumps=2;player.anim=0;player.stepTimer=0;player.landTimer=0;player.recoil=0;player.lean=0;setObjective();
}
function buildAlcatrazPopulation(){
 zombies=[];
 for(let i=0;i<68;i++){
  const x=1250+i*392+(i%5)*73;
  const type=i%13===0?'brute':i%7===0?'stalker':i%4===0?'runner':'walker';
  zombies.push({x,type,hp:type==='brute'?230:type==='stalker'?110:type==='runner'?95:70,maxHp:type==='brute'?230:type==='stalker'?110:type==='runner'?95:70,dead:false,deathTimer:0,phase:i*.61,attack:0,hit:0,alert:0,flash:0,limb:Math.random()*6.28,crimeRole:i%9===0?'detective':i%5===0?'enforcer':i%3===0?'masked':'thug'});
 }
 chestData=[
  {id:'cellKey',world:'ALCATRAZ',inside:true,building:'CELLHOUSE',x:310,y:390,items:[{id:'key',name:'BRASS KEY',count:1}],opened:false},
  {id:'medicalPass',world:'ALCATRAZ',inside:true,building:'HOSPITAL WING',x:1040,y:390,items:[{id:'dockPass',name:'DOCK PASS',count:1},{id:'fuse',name:'FUSE',count:1},{id:'bandage',name:'BANDAGE',count:2},{id:'ammo_9mm',name:'9MM AMMO',count:12}],opened:false},
  {id:'workshop',world:'ALCATRAZ',inside:true,building:'MODEL INDUSTRIES',x:520,y:420,items:[{id:'scrap',name:'SCRAP',count:4},{id:'radioPart',name:'RADIO PART',count:1},{id:'ammo_9mm',name:'9MM AMMO',count:10}],opened:false},
  {id:'dockCrate',world:'ALCATRAZ',inside:false,building:'MAIN DOCK',x:15780,y:0,items:[{id:'food',name:'CANNED FOOD',count:1}],opened:false}
 ];
}
function buildSFPopulation(){
 survivors=[
  {id:'mara',name:'MARA',x:3200,found:false,talked:false,building:'EMERGENCY SHELTER'},
  {id:'eli',name:'ELI',x:6200,found:false,talked:false,building:'OLD POLICE STATION'},
  {id:'noah',name:'NOAH',x:8600,found:false,talked:false,building:'HARBOR WAREHOUSE'}
 ];
 zombies=[];
 for(let i=0;i<38;i++)zombies.push({x:600+i*370+(i%5)*42,type:i%8===0?'brute':i%4===0?'runner':'walker',hp:i%8===0?180:i%4===0?90:65,maxHp:i%8===0?180:i%4===0?90:65,dead:false,deathTimer:0,phase:i*.51,attack:0,hit:0,flash:0,limb:Math.random()*6.28});
}
function beginGame(name){selectedCharacter=name;resetWorld();startSoundscape();introIndex=0;introTimer=0;scene='intro';show('cutscene');hide('characterMenu');hide('mainMenu');updateIntroText();}
function positionInsideCell(){interior={id:'cellA17',name:'CELL A-17',type:'cell',building:{name:'CELLHOUSE',w:1060,x:370,floors:3},floor:1,floors:3,stairCooldown:0,topDown:true};interiorPhase=0;player.x=310;player.y=400;player.vx=0;player.vy=0;player.onGround=true;interiorZombies=[];}
function updateIntroText(){const e=document.getElementById('cutMain');if(e)e.textContent=introLines[introIndex]||'';}
function advanceIntro(){if(scene!=='intro')return;introIndex++;introTimer=0;if(introIndex>=introLines.length){scene='play';show('hud');hide('cutscene');setObjective();setMessage('CELL A-17 • SEARCH THE MATTRESS FOR THE KEY.',2.5);}else updateIntroText();}
function getObjectiveStep(){if(chapter==='ALCATRAZ'){if(!state.startKey)return 0;if(!state.startEscaped)return 1;if(!state.dockPass)return 2;if(!state.powerRestored)return 1;if(!state.radioSignal)return 2;if(!state.beacon)return 4;return 5;}return state.survivors>=2?3:1;}
function setObjective(){const idx=chapter==='ALCATRAZ'?Math.min(objectiveIndex,1):2;const o=objectives[idx];const step=chapter==='ALCATRAZ'?getObjectiveStep():getObjectiveStep();const s=o.steps[Math.min(step,o.steps.length-1)];const e=document.getElementById('objective');if(e)e.textContent=`${o.title}\n${s}`;renderObjectives();}
function renderObjectives(){const list=document.getElementById('objectiveList');if(!list)return;list.innerHTML='';objectives.forEach((o,i)=>{const item=document.createElement('div');item.className='objectiveItem '+(i<objectiveIndex?'done ':'')+(i===objectiveIndex?'current':'');const status=i<objectiveIndex?'✓ COMPLETE':i===objectiveIndex?'› CURRENT':'○ FUTURE';const activeStep=i===0&&chapter==='ALCATRAZ'?getObjectiveStep():i===2&&chapter==='SAN FRANCISCO'?getObjectiveStep():0;item.innerHTML=`<b>${status}</b><div style="margin-top:6px;letter-spacing:1px">${o.title}</div>`;o.steps.forEach((s,k)=>{const sp=document.createElement('span');sp.className='step'+(k===activeStep&&i===objectiveIndex?' active':'');sp.textContent=`${k+1}. ${s}`;item.appendChild(sp);});list.appendChild(item);});}
function transitionTo(kind,fn){if(fadeBusy)return;fadeBusy=true;transitionKind=kind;const f=document.getElementById('fade');f.style.opacity='1';setTimeout(()=>{fn();setTimeout(()=>{f.style.opacity='0';setTimeout(()=>fadeBusy=false,520);},60)},440);}
function enterStructure(b){if(fadeBusy)return;transitionTo('enter',()=>{interior={id:b.type+'_'+b.x,name:b.name,type:b.type,building:b,roomWidth:1400,roomHeight:788,floor:1,floors:Math.max(1,b.floors||3),stairCooldown:0,topDown:true};interiorPhase=0;player.x=700;player.y=430;player.vx=0;player.vy=0;player.onGround=true;spawnInteriorThreats();soundDoor();setMessage(`ENTERED ${b.name} — SEARCH EVERY ROOM.`,1.4);});}
function enterCellCorridor(){if(fadeBusy)return;transitionTo('cellcorridor',()=>{interior={id:'cellCorridor',name:'CELL BLOCK A',type:'cellcorridor',building:{name:'CELLHOUSE',x:370,w:1060,floors:3},roomWidth:1400,roomHeight:788,floor:1,floors:3,stairCooldown:0,topDown:true};interiorPhase=1;player.x=700;player.y=430;player.vx=0;player.vy=0;player.onGround=true;spawnInteriorThreats();soundDoor();setMessage('CELL BLOCK A — SOMETHING IS MOVING ABOVE YOU.',2);setObjective();});}
function exitStructure(){if(!interior||fadeBusy)return;const b=interior.building;if(interior.topDown){if(interior.id==='cellA17'&&!state.startEscaped){setMessage('The cell is sealed. Search the mattress and find the key.',1.7);return;}if(interior.id==='cellA17'&&player.x>1240){enterCellCorridor();return;}if(player.x<70||player.x>1330){transitionTo('exit',()=>{const side=player.x<70?-1:1;const outside=side<0?b.x-80:b.x+b.w+80;player.x=clamp(outside,180,WORLD[chapter]-180);player.y=clamp((b.y||4200),900,WORLD_HEIGHT[chapter]-700);player.vx=0;player.vy=0;interior=null;interiorZombies=[];camera=clamp(player.x-W*.4,0,WORLD[chapter]-W);soundDoor();setMessage(`BACK OUTSIDE — ${b.name}.`,1.3);});return;}setMessage('Find an EXIT door or stairwell.',1.0);return;}const side=player.x<200?-1:player.x>980?1:0;if(interior.id==='cellA17'&&!state.startEscaped){setMessage('The cell door is closed. Search the mattress and unlock it.',1.7);return;}if(interior.id==='cellA17'&&side!==0){enterCellCorridor();return;}if(side===0){setMessage('Move closer to the EXIT door.',1.2);return;}transitionTo('exit',()=>{const outside=side<0?b.x-80:b.x+b.w+80;player.x=clamp(outside,180,WORLD[chapter]-180);player.y=clamp((b.y||4200),900,WORLD_HEIGHT[chapter]-700);player.vx=0;player.vy=0;player.onGround=true;interior=null;camera=clamp(player.x-W*.4,0,WORLD[chapter]-W);soundDoor();setMessage(`BACK OUTSIDE — ${b.name}.`,1.3);});}
function searchStartingCell(){if(state.startKey){setMessage('The mattress is empty.',1);return;}state.startKey=true;state.inventory.key=1;const c=chestData.find(x=>x.id==='cellKey');if(c)c.opened=true;soundChest();setMessage('BRASS KEY FOUND. The lock is within reach.',2);setObjective();}
function unlockCell(){if(!state.startKey){setMessage('Search under the mattress first.',1.5);return;}if(state.startEscaped){enterCellCorridor();return;}state.startEscaped=true;objectiveIndex=0;soundDoor();soundScare();horror.flash=.28;setObjective();enterCellCorridor();}
function openChest(c){if(!c)return;currentChest=c;scene='inventory';show('inventoryUi');renderChest();soundChest();}
function renderChest(){const root=document.getElementById('chestSlots');if(!root||!currentChest)return;root.innerHTML='';for(let i=0;i<27;i++){const slot=document.createElement('button');slot.style.minHeight='74px';slot.style.textAlign='left';slot.style.padding='8px';slot.style.background='#0b100f';const item=currentChest.items[i];if(item){slot.innerHTML=`<b style="color:#eee5cf">${item.name}</b><br><span style="color:#8f9993">× ${item.count}</span>`;slot.onclick=()=>takeChestItem(i);}else{slot.textContent='EMPTY';slot.style.color='#4e5853';slot.disabled=true;}root.appendChild(slot);} }
function takeChestItem(i){if(!currentChest||!currentChest.items[i])return;const item=currentChest.items[i];state.inventory[item.id]=(state.inventory[item.id]||0)+item.count;if(item.id==='key')state.startKey=true;if(item.id==='dockPass'){state.dockPass=true;advanceObjective(0);setMessage('DOCK PASS FOUND. The ferry route is open.',2.2);}else{setMessage(`TAKEN: ${item.name} × ${item.count}`,1.2);}currentChest.items.splice(i,1);currentChest.opened=true;soundPickup();renderChest();setObjective();}
function takeAll(){if(!currentChest)return;for(const item of currentChest.items){state.inventory[item.id]=(state.inventory[item.id]||0)+item.count;if(item.id==='key')state.startKey=true;if(item.id==='dockPass')state.dockPass=true;}if(currentChest.items.some(x=>x.id==='dockPass'))setMessage('DOCK PASS FOUND. Follow the signs to the ferry.',2);else setMessage('CHEST CLEARED.',1);currentChest.items=[];currentChest.opened=true;soundPickup();renderChest();setObjective();}
function sortChest(){if(!currentChest)return;currentChest.items.sort((a,b)=>a.name.localeCompare(b.name));renderChest();tone(260,.1,'sine',.1,80);}
function closeChest(){hide('inventoryUi');scene='play';currentChest=null;}
function nearestChest(){if(interior){let best=null,d=9999;for(const c of chestData){if(!c.inside||c.building!==interior.building.name||c.opened&&c.items.length===0)continue;const dd=interior.topDown?Math.hypot(player.x-c.x,player.y-(c.y||390)):Math.abs(player.x-c.x);if(dd<d){d=dd;best=c;}}return d<120?best:null;}let best=null,d=9999;for(const c of chestData){if(c.inside||c.opened&&c.items.length===0||c.world!==chapter)continue;const dd=Math.abs(player.x-c.x);if(dd<d){d=dd;best=c;}}return d<110?best:null;}
function talkSurvivor(){if(chapter!=='SAN FRANCISCO')return;let best=null,d=130;for(const s of survivors){if(s.found)continue;const dd=Math.abs(player.x-s.x);if(dd<d){d=dd;best=s;}}if(!best)return;best.found=true;best.talked=true;state.survivors++;soundPickup();setMessage(`${best.name}: I thought nobody else was alive.`,2.2);if(state.survivors===1)showWarning('ONE SURVIVOR FOUND');if(state.survivors>=2){objectiveIndex=2;setObjective();setMessage('TWO SURVIVORS FOUND. REACH THE EMERGENCY SHELTER.',2.3);}}
function tryUseStairs(){
 if(!interior||interior.floors<=1)return false;
 const nearLeft=Math.abs(player.x-245)<105;
 const nearRight=Math.abs(player.x-935)<105;
 if(!nearLeft&&!nearRight)return false;
 if(interior.stairCooldown>0)return true;
 const dir=nearLeft?1:-1;
 const next=clamp(interior.floor+dir,1,interior.floors);
 if(next===interior.floor){setMessage(next===interior.floors?'NO HIGHER FLOOR.':'NO LOWER FLOOR.',1);return true;}
 interior.floor=next;interior.stairCooldown=.55;player.x=nearLeft?300:880;player.vx=0;player.vy=0;player.onGround=true;
 horror.flash=.18;horror.shake=5;state.sanity=Math.max(0,state.sanity-3);soundDoor();
 setMessage(`STAIRWELL — FLOOR ${interior.floor} / ${interior.floors}`,1.4);
 if(interior.floor===3&&Math.random()<.65){setTimeout(()=>{if(scene==='play'&&interior){triggerJumpscare('stair');}},500);}
 return true;
}
function useInteract(){if(scene!=='play'||fadeBusy)return;if(crimeCollect())return;if(interior&&interior.topDown&&nearestHideSpot()){toggleHide();return;}if(currentChest){openChest(currentChest);return;}if(interior&&interior.topDown){if(interior.floors>1&&((Math.abs(player.x-145)<100||Math.abs(player.x-1245)<100)&&player.y>250&&player.y<520)){const nearLeft=player.x<700;const dir=nearLeft?1:-1;const next=clamp(interior.floor+dir,1,interior.floors);if(next===interior.floor){setMessage('NO MORE FLOORS.',1);return;}interior.floor=next;player.x=nearLeft?220:1180;player.y=390;state.sanity=Math.max(0,state.sanity-5);horror.shake=8;setMessage(`STAIRS — FLOOR ${interior.floor}/${interior.floors}`,1.4);if(interior.floor===3&&Math.random()<.8)triggerJumpscare('stair');return;}if(interior.id==='cellA17'&&!state.startKey&&Math.hypot(player.x-310,player.y-390)<110){searchStartingCell();return;}if(interior.id==='cellA17'&&state.startKey&&Math.hypot(player.x-1240,player.y-390)<125){unlockCell();return;}const c=nearestChest();if(c){openChest(c);return;}if(player.x<70||player.x>1330){exitStructure();return;}return;}if(interior&&interior.floors>1&&tryUseStairs())return;if(interactAlcatrazSpecial())return;if(interior){if(player.x<170||player.x>1010){exitStructure();return;}const c=nearestChest();if(c){openChest(c);return;}return;}if(chapter==='ALCATRAZ'){if(!state.startEscaped&&player.x<1050){setMessage('The cell is still locked. Search the mattress.',1.5);return;}const b=nearestBuilding();if(b){enterStructure(b);return;}if(Math.abs(player.x-21700)<330){if(!state.dockPass){setMessage('THE PIER GATE IS LOCKED. YOU NEED THE DOCK PASS.',2);return;}if(!state.powerRestored){setMessage('NO POWER. Restore the emergency generator first.',2);return;}if(!state.radioSignal){setMessage('THE FERRY WILL NOT ANSWER. Transmit the emergency signal.',2);return;}if(!state.beacon){state.beacon=true;advanceObjective(1);setMessage('BEACON LIT. THE FERRY IS COMING. RUN.',2);tone(250,.5,'sine',.13,90);state.finalChase=true;return;}if(!state.boatEscaped){state.boatEscaped=true;transitionTo('ferry',()=>{endingTriggered=true;scene='ending';show('ending');document.getElementById('endingText').textContent='The ferry reaches the pier through the storm. Behind you, the cellhouse lights turn on one by one. The last camera feed shows a figure standing in your empty cell.';soundScare();});return;}}}else{if(talkSurvivorState())return;const b=nearestBuilding();if(b){enterStructure(b);return;}if(state.survivors>=2&&Math.abs(player.x-3200)<420){endingTriggered=true;scene='ending';show('ending');document.getElementById('endingText').textContent='Two survivors reached the shelter. Behind the rain, the island lights were still visible. On the final CCTV frame, a tall figure smiled at the empty dock.';soundScare();}}}

function talkSurvivorState(){if(chapter!=='SAN FRANCISCO')return false;for(const s of survivors){if(!s.found&&Math.abs(player.x-s.x)<125){talkSurvivor();return true;}}return false;}
function advanceObjective(i){if(i>objectiveIndex)objectiveIndex=Math.min(i,2);setObjective();}
function updateAlcatrazProgression(){
 if(chapter!=='ALCATRAZ'||interior)return;
 if(state.dockPass && !state.powerRestored && player.x>10800 && player.x<12350){
  setMessage('THE POWER PLANT IS DEAD. THE FUSE BOX MAY STILL WORK.',1.8);
 }
 if(state.powerRestored && !state.radioSignal && player.x>14500 && player.x<15500){
  setMessage('THE RADIO ROOM IS NEARBY. SOMETHING IS FOLLOWING YOU.',1.8);
 }
 if(state.radioSignal && !state.finalChase && player.x>18500){
  state.finalChase=true;state.alarm=true;horror.glitch=1;horror.shake=12;
  showWarning('THE ISLAND LOCKDOWN HAS BEGUN',2.4);soundScare();
  for(let i=0;i<7;i++){
   zombies.push({x:player.x+650+i*125,type:i%3===0?'runner':'stalker',hp:i%3===0?95:110,dead:false,phase:i*.7,attack:0,hit:0,alert:1});
  }
 }
 if(state.finalChase && player.x>21500){
  state.beacon=true;
  if(!state.boatEscaped)setMessage('THE FERRY IS HERE. KEEP RUNNING.',1.6);
 }
}
function interactAlcatrazSpecial(){
 if(chapter!=='ALCATRAZ'||interior)return false;
 if(state.dockPass && !state.powerRestored && Math.abs(player.x-11550)<330){
   state.powerRestored=true;state.inventory.fuse=Math.max(0,state.inventory.fuse-1);
   if(state.inventory.fuse<0)state.inventory.fuse=0;
   state.alarm=false;advanceObjective(1);soundDoor();horror.flash=.35;
   setMessage('EMERGENCY POWER RESTORED. THE PRISON JUST WOKE UP.',2.5);
   return true;
 }
 if(state.powerRestored && !state.radioSignal && Math.abs(player.x-15100)<260){
   state.radioSignal=true;advanceObjective(1);state.sanity=Math.max(0,state.sanity-12);
   showWarning('SIGNAL TRANSMITTED — SOMETHING ANSWERED',2.5);soundWhisper();
   return true;
 }
 return false;
}

function nearestBuilding(){let best=null,d=99999;for(const b of landmarkData){if(b.name==='CELLHOUSE'||b.name==='RECREATION YARD'||b.name==='MAIN DOCK')continue;const dd=Math.hypot(player.x-b.x,player.y-(b.y||4000));if(dd<d&&dd<720){d=dd;best=b;}}return best;}
function nearestHideSpot(){
 if(!interior)return null;
 const spots=[{x:105,y:170},{x:1290,y:180},{x:260,y:570},{x:720,y:610},{x:1160,y:520}];
 let best=null,bd=999;for(const h of spots){const d=Math.hypot(player.x-h.x,player.y-h.y);if(d<bd){bd=d;best=h;}}
 return bd<105?best:null;
}
function toggleHide(){
 if(!interior||scene!=='play')return;
 const h=nearestHideSpot();
 if(h){hiding=!hiding;player.x=h.x;player.y=h.y;player.vx=0;player.vy=0;showWarning(hiding?'HIDDEN — HOLD STILL':'YOU LEFT COVER',1.1);if(hiding)soundWhisper();return;}
 setMessage('Find a locker, cabinet, or dark corner to hide in.',1.2);
}

function spawnInteriorThreats(){
 interiorZombies=[];dread.roomEnteredAt=totalTime;dread.eventTimer=3+Math.random()*5;dread.ambushCooldown=9;
 const count=interior.type==='cellcorridor'?15:12;
 for(let i=0;i<count;i++){
  interiorZombies.push({x:170+(i*173)%1080,y:155+(i*97)%430,hp:i%4===0?155:i%3===0?95:72,type:i%4===0?'stalker':i%3===0?'runner':'walker',attack:Math.random()*.6,phase:i*.8,dead:false,deathTimer:0,hit:0,alert:0});
 }
}
function updateInteriorZombies(dt){
 if(!interior)return;
 for(const z of interiorZombies){if(z.dead){z.deathTimer=Math.max(0,z.deathTimer-dt);continue;}z.attack=Math.max(0,z.attack-dt);
  const dx=player.x-z.x,dy=player.y-z.y,d=Math.hypot(dx,dy);
  if(hiding){ if(d<95){z.alert=1; z.x+=(Math.sign(dx)||1)*22*dt; z.y+=(Math.sign(dy)||1)*16*dt; if(d<48&&z.attack<=0){hiding=false;damagePlayer(z.type==='stalker'?32:22);showWarning('IT FOUND YOUR HIDING PLACE',1.2);}} continue; }
  const alertRadius=state.light?920:520;
  if(d<alertRadius || (z.alert||0)>0){z.alert=Math.max(0,(z.alert||0)-dt*.08);const sp=(z.type==='runner'?176:z.type==='stalker'?142:92)*(1+Math.min(.28,(difficulty-1)*.09));if(d>34){const flank=z.type==='stalker'?Math.sin(totalTime*1.8+z.phase)*.34:0;z.x+=(dx/Math.max(d,1)+flank)*sp*dt;z.y+=dy/Math.max(d,1)*sp*dt;}else if(z.attack<=0){damagePlayer(z.type==='stalker'?21:z.type==='runner'?18:14);z.attack=z.type==='runner'?.42:z.type==='stalker'?.58:.78;horror.shake=12;showWarning(z.type==='stalker'?'IT GOT THROUGH THE DARK':'THEY ARE ON YOU',.8);}}
  z.x=clamp(z.x,60,1340);z.y=clamp(z.y,105,650);
 }
}
function damageInteriorZombie(){
 let best=null,bd=72;
 for(const z of interiorZombies){if(z.dead)continue;const d=Math.hypot(z.x-player.x,z.y-player.y);if(d<bd){bd=d;best=z;}}
 if(!best)return false;best.hp-=34;best.hit=.16;if(best.hp<=0){best.dead=true;best.deathTimer=.65;state.sanity=Math.max(0,state.sanity-1);spawnDust();}else{state.sanity=Math.max(0,state.sanity-.4);}return true;
}

function updateInput(){inputState.left=keys.has('a')||keys.has('A')||keys.has('ArrowLeft')||touch.left;inputState.right=keys.has('d')||keys.has('D')||keys.has('ArrowRight')||touch.right;inputState.run=keys.has('Shift')||touch.run;inputState.jump=keys.has(' ')||touch.jump;if(inputState.jump){if(player.jumpBuffer<=0)player.jumpBuffer=.14;}else player.jumpBuffer=0;}
function tryJump(){if(scene!=='play')return;if(player.onGround||player.coyote>0){player.vy=-640;player.onGround=false;player.coyote=0;player.jumps=1;player.air=0;soundJump();spawnDust();return;}if(player.jumps>0){player.vy=-580;player.jumps=0;player.air=0;soundJump();spawnDust();}}
function movementStep(dt){
 if(scene!=='play'||fadeBusy)return;
 if(interior&&interior.topDown){
  if(hiding){player.vx=0;player.vy=0;state.stamina=Math.min(100,state.stamina+dt*18);updateInteriorZombies(dt);return;}
  const dx=(inputState.right?1:0)-(inputState.left?1:0);
  const dy=((keys.has('s')||keys.has('S')||keys.has('ArrowDown')||touch.down)?1:0)-((keys.has('w')||keys.has('W')||keys.has('ArrowUp')||touch.up)?1:0);
  const mag=Math.hypot(dx,dy)||1,base=inputState.run&&state.stamina>5?245:175;
  player.vx=lerp(player.vx,(dx/mag)*base,1-Math.exp(-16*dt));player.vy=lerp(player.vy,(dy/mag)*base,1-Math.exp(-16*dt));
  player.x=clamp(player.x+player.vx*dt,42,1358);player.y=clamp(player.y+player.vy*dt,88,682);
  if(dx)player.facing=dx<0?-1:1;if(inputState.run&&(dx||dy))state.stamina=Math.max(0,state.stamina-dt*31);else state.stamina=Math.min(100,state.stamina+dt*14);
  player.anim+=dt*(Math.hypot(player.vx,player.vy)/70+.4);player.recoil=Math.max(0,player.recoil-dt*8);
  if(Math.hypot(player.vx,player.vy)>55){footstepsTimer-=dt;if(footstepsTimer<=0){footstepsTimer=inputState.run?.22:.34;soundStep();horrorDirector.noise=Math.min(100,horrorDirector.noise+(inputState.run?13:5));}}
  if((keys.has('ArrowUp')||keys.has('w')||keys.has('W')||touch.up||touch.interact)&&Math.abs(player.x-1240)<145&&interior.id==='cellA17'&&state.startKey&&!state.startEscaped){unlockCell();return;}
  updateInteriorZombies(dt);return;
 }
 // TRUE TOP-DOWN EXTERIOR MOVEMENT: north / south / east / west.
 const dx=(inputState.right?1:0)-(inputState.left?1:0);
 const dy=((keys.has('s')||keys.has('S')||keys.has('ArrowDown')||touch.down)?1:0)-((keys.has('w')||keys.has('W')||keys.has('ArrowUp')||touch.up)?1:0);
 const mag=Math.hypot(dx,dy)||1,base=inputState.run&&state.stamina>5?360:245;
 player.vx=lerp(player.vx,(dx/mag)*base,1-Math.exp(-14*dt));player.vy=lerp(player.vy,(dy/mag)*base,1-Math.exp(-14*dt));
 const maxX=WORLD[chapter],maxY=WORLD_HEIGHT[chapter];player.x=clamp(player.x+player.vx*dt,180,maxX-180);player.y=clamp(player.y+player.vy*dt,900,maxY-700);
 if(dx)player.facing=dx<0?-1:1;const moving=Math.hypot(player.vx,player.vy)>35;
 if(inputState.run&&moving)state.stamina=Math.max(0,state.stamina-dt*23);else state.stamina=Math.min(100,state.stamina+dt*16);
 horrorDirector.noise=Math.max(0,horrorDirector.noise-dt*5);if(inputState.run&&moving)horrorDirector.noise=Math.min(100,horrorDirector.noise+dt*16);
 player.anim+=dt*(Math.hypot(player.vx,player.vy)/80+.25);player.recoil=Math.max(0,player.recoil-dt*8);
 if(moving){footstepsTimer-=dt;if(footstepsTimer<=0){footstepsTimer=inputState.run?.20:.34;soundStep();footprints.push({x:player.x,y:player.y,f:totalTime});if(footprints.length>140)footprints.shift();}}
 const near=nearestBuilding();if(near&&(keys.has('ArrowUp')||keys.has('w')||keys.has('W')||touch.up||touch.interact||keys.has('e')||keys.has('E'))){enterStructure(near);return;}
}

function damagePlayer(a){if(totalTime-lastDamageTime<0.38)return;lastDamageTime=totalTime;state.health-=a;horror.shake=10;horror.flash=.18;state.sanity=Math.max(0,state.sanity-3.5);if(state.health<=0){state.health=0;scene='death';show('death');document.getElementById('deathText').textContent='The island kept you. This was not the last attempt.';soundScare();}}
function updateHorrorDirector(dt){
 if(scene!=='play')return;
 const inside=!!interior;
 horrorDirector.intensity=clamp((100-state.sanity)/70+(difficulty-1)*.22+(state.finalChase?.35:0),0,1.9);
 horrorDirector.timer-=dt; horrorDirector.noise=Math.max(0,horrorDirector.noise-dt*(inside?5:3));
 if(horrorDirector.lockdown>0){horrorDirector.lockdown-=dt;if(horrorDirector.lockdown<=0){state.alarm=false;showWarning('THE LOCKS RELEASED. FOR NOW.',1);}}
 if(horrorDirector.doorSlam>0)horrorDirector.doorSlam-=dt;
 if(horrorDirector.stalker){
  const q=horrorDirector.stalker;
  q.life-=dt;
  const dx=player.x-q.x,dy=(inside?player.y-q.y:0),d=Math.hypot(dx,dy);
  q.x+=Math.sign(dx)*dt*(inside?72:52);
  if(inside)q.y+=Math.sign(dy)*dt*48;
  q.alpha=clamp(1-d/720,.05,.9);
  if(d<75&&q.life<7){damagePlayer(17);horrorDirector.stalker=null;horrorDirector.timer=14+Math.random()*12;}
  if(q.life<=0)horrorDirector.stalker=null;
 }
 if(horrorDirector.timer>0)return;
 horrorDirector.timer=(inside?4:7)+Math.random()*9;
 const I=horrorDirector.intensity;
 const roll=Math.random();
 if(roll<.22+I*.10){
   // A fake safe moment followed by a sudden blackout.
   horror.blackout=.65+Math.random()*.7;horror.glitch=.35;horror.shake=5;soundFlicker();
   showWarning(inside?'THE LIGHTS WENT OUT. DO NOT MOVE.':'THE FLOODLIGHTS JUST DIED.',1.8);
   setTimeout(()=>{if(scene==='play'){horror.blackout=0;horror.glitch=.9;triggerJumpscare('random');}},700+Math.random()*1300);
 }else if(roll<.43+I*.13){
   // Spawn a hunter behind the player rather than in front.
   const side=Math.random()<.5?-1:1;
   horrorDirector.stalker={x:clamp(player.x+side*(520+Math.random()*280),80,(interior?1340:WORLD[chapter]-80)),y:inside?clamp(player.y+(Math.random()-.5)*280,110,650):GROUND-55,life:5.5+Math.random()*5,alpha:.1};
   showWarning(Math.random()<.5?'SOMETHING IS WALKING BEHIND YOU.':'DO NOT LOOK BACK.',1.5);soundWhisper();
 }else if(roll<.62+I*.12){
   // Noise consequence: an ambush wave materializes from the edges.
   const n=inside?2+Math.floor(Math.random()*3):2+Math.floor(Math.random()*4);
   for(let i=0;i<n;i++){
    const side=Math.random()<.5?-1:1;
    if(inside)interiorZombies.push({x:side<0?80:1320,y:130+Math.random()*500,hp:95,type:Math.random()<.45?'runner':'stalker',attack:.3,phase:Math.random()*6,dead:false,deathTimer:0,hit:0,alert:1});
    else zombies.push({x:clamp(player.x+side*(650+i*100),80,WORLD[chapter]-80),type:i%2?'runner':'stalker',hp:i%2?95:110,maxHp:i%2?95:110,dead:false,deathTimer:0,phase:Math.random()*6,attack:0,hit:0,alert:1,flash:0});
   }
   horror.shake=8;showWarning('THEY HEARD THAT.',1.5);tone(55,.25,'sawtooth',.12,-45);
 }else if(roll<.80){
   // Environmental scare: a door slam / distant movement.
   horrorDirector.doorSlam=1.2;horror.shake=3;showWarning(Math.random()<.5?'A DOOR SLAMMED SOMEWHERE.':'FOOTSTEPS ABOVE YOU.',1.3);soundWhisper();
 }else if(I>.65 && !state.finalChase){
   // Rare lockdown: changes the objective from exploring to surviving.
   horrorDirector.lockdown=9+Math.random()*7;state.alarm=true;horror.glitch=.8;horror.shake=10;
   showWarning(inside?'THE BUILDING JUST LOCKED ITSELF.':'THE ISLAND LOCKDOWN HAS BEGUN.',2.2);tone(48,.5,'square',.15,-30);
   for(let i=0;i<4;i++){
    if(inside)interiorZombies.push({x:Math.random()<.5?70:1330,y:130+Math.random()*500,hp:130,type:'stalker',attack:.2,phase:i,dead:false,deathTimer:0,hit:0,alert:1});
   }
 }
}

function drawHorrorDirector(){
 if(scene!=='play')return;
 const q=horrorDirector.stalker;
 if(q){const x=q.x-(interior?0:camera),y=q.y;ctx.save();ctx.globalAlpha=.72*q.alpha;px(x-17,y-48,34,62,'#030505');px(x-24,y-68,48,25,'#020303');px(x-14,y-60,7,5,'#d9d2bb');px(x+7,y-60,7,5,'#d9d2bb');ctx.restore();}
 if(horrorDirector.doorSlam>0){ctx.save();ctx.globalAlpha=horrorDirector.doorSlam*.18;px(0,0,W,3,'#ddd5c0');ctx.restore();}
}

function updateZombies(dt){
 for(const z of zombies){if(z.dead){z.deathTimer=Math.max(0,z.deathTimer-dt);continue;}if(z.y==null)z.y=4000+((z.phase*137)%9000);z.attack=Math.max(0,z.attack-dt);z.hit=Math.max(0,z.hit-dt);z.flash=Math.max(0,z.flash-dt);const dx=player.x-z.x,dy=player.y-z.y,d=Math.hypot(dx,dy),vision=state.light?1250:760;
  if(d<vision){z.facing=dx>=0?1:-1;if(d<500&&Math.hypot(player.vx,player.vy)>160)z.alert=Math.min(1,(z.alert||0)+dt*.9);else z.alert=Math.max(0,(z.alert||0)-dt*.18);if(d>58){let sp=z.type==='warden'?118:z.type==='runner'?205:z.type==='brute'?72:z.type==='stalker'?150:98;if(z.alert>.55)sp*=1.18;z.x+=dx/Math.max(d,1)*sp*dt;z.y+=dy/Math.max(d,1)*sp*dt;}else if(z.attack<=0){damagePlayer(z.type==='brute'?30:z.type==='stalker'?23:z.type==='runner'?19:14);z.attack=z.type==='runner'?.42:z.type==='stalker'?.58:.78;horror.shake=9;}}
  z.x=clamp(z.x,160,WORLD[chapter]-160);z.y=clamp(z.y,800,WORLD_HEIGHT[chapter]-650);
 }
}

function killZombie(z,force=false){
 if(!z||z.dead)return;
 z.hp=0;z.dead=true;z.deathTimer=1.8;z.flash=.3;z.vx=0;z.alert=0;
 spawnBlood(z.x,GROUND-58);spawnBlood(z.x+(Math.random()-.5)*22,GROUND-45);horror.shake=Math.max(horror.shake,4);
 state.sanity=Math.min(100,state.sanity+1.5);totalKills++;
 tone(force?95:70,.12,'sawtooth',.16,-35);noiseBurst(.09,.09);
}
function shoot(){
 if(scene!=='play')return;if(state.ammo<=0){soundReload();setMessage('EMPTY MAGAZINE. R TO RELOAD.',1.1);return;}state.ammo--;player.recoil=.2;soundShot();horror.shake=3;horrorDirector.noise=100;
 let wx=camera+mouse.x,wy=cameraY+mouse.y,dx=wx-player.x,dy=wy-player.y,len=Math.hypot(dx,dy)||1,ax=dx/len,ay=dy/len;player.facing=ax<0?-1:1;let hit=null,best=920;
 for(const z of zombies){if(z.dead)continue;const zx=z.x-player.x,zy=z.y-player.y,along=zx*ax+zy*ay,perp=Math.abs(zx*ay-zy*ax);if(along>35&&along<best&&perp<48){best=along;hit=z;}}
 if(hit){const damage=selectedCharacter==='Yumi'?58:selectedCharacter==='May'?48:50;if(hit.type==='warden')hit.hp-=Math.round(damage*.72);else hit.hp-=damage;hit.hit=.18;hit.flash=.14;hit.alert=1;spawnBlood(hit.x,hit.y);horror.shake=5;setMessage(hit.hp>0?`HIT — ${Math.max(0,Math.ceil(hit.hp))} HP REMAINING`:'TARGET DOWN',.45);if(hit.hp<=0)killZombie(hit);}else spawnSpark(player.x+ax*420,player.y+ay*420);
}

function melee(){
 if(scene!=='play')return;
 if(interior&&interior.topDown){const struck=damageInteriorZombie();horror.shake=struck?8:3;tone(struck?110:85,.08,'square',.12,-30);return;}
 let struck=false;
 for(const z of zombies){
  if(z.dead)continue;
  const dx=(z.x-player.x)*player.facing;
  if(dx>=-15&&dx<105){
   const damage=selectedCharacter==='May'?78:selectedCharacter==='Yumi'?62:68;
   z.hp-=damage;z.hit=.22;z.flash=.18;z.alert=1;z.x+=player.facing*48;spawnBlood(z.x,GROUND-54);struck=true;
   if(z.hp<=0)killZombie(z,true);
  }
 }
 horror.shake=struck?7:3;tone(struck?110:85,.08,'square',.12,-30);horrorDirector.noise=Math.min(100,horrorDirector.noise+45);
}
function reload(){if(state.reserveAmmo<=0||state.ammo>=12)return;const take=Math.min(12-state.ammo,state.reserveAmmo);state.reserveAmmo-=take;state.ammo+=take;soundReload();}
function updateDifficultyDirector(dt){
 if(scene!=='play')return;
 const progress=chapter==='ALCATRAZ'?clamp(player.x/WORLD.ALCATRAZ,0,1):clamp(player.x/WORLD.SF,0,1);
 const survivalPressure=(100-state.health)/100;
 difficulty=1+progress*.9+(state.alarm?0.45:0)+(state.finalChase?0.85:0)+survivalPressure*.35;
 threatLevel=clamp((difficulty-1)*100,0,100);
 encounterTimer-=dt;
 if(state.light&&state.battery>0){state.battery=Math.max(0,state.battery-dt*(interior?0.8:0.34));}
 if(state.battery<=0&&state.light){state.light=false;showWarning('FLASHLIGHT BATTERY DEAD',2);soundFlicker();}if(state.powerRestored&&!wardenSpawned&&!interior&&player.x>11800){
  wardenSpawned=true;
  zombies.push({x:clamp(player.x+1100,100,WORLD[chapter]-100),type:'warden',hp:420,maxHp:420,dead:false,deathTimer:0,phase:Math.random()*6.28,attack:2,hit:0,alert:1,flash:0,limb:0});
  showWarning('THE WARDEN HAS LEFT THE CELLHOUSE',2.4);soundScare();state.sanity=Math.max(0,state.sanity-10);
}

 if(state.health<28&&!lowHealthWarned){lowHealthWarned=true;showWarning('CRITICAL CONDITION — FIND COVER',2.2);}
 if(state.health>45)lowHealthWarned=false;
 if(encounterTimer<=0&&!interior&&!state.boatEscaped){
   encounterTimer=Math.max(3.2,10.5-difficulty*3)+Math.random()*4.5;
   const active=zombies.filter(z=>!z.dead).length;
   if(active<95){
    const side=player.x>WORLD[chapter]/2?-1:1;
    const spawnX=clamp(player.x+side*(520+Math.random()*500),140,WORLD[chapter]-140);
    const roll=Math.random();
    const type=roll<.16?'brute':roll<.38?'stalker':roll<.68?'runner':'walker';
    const hp=type==='brute'?290:type==='stalker'?155:type==='runner'?125:88;
    zombies.push({x:spawnX,type,hp,maxHp:hp,dead:false,deathTimer:0,phase:Math.random()*6.28,attack:0,hit:0,alert:1,flash:0,limb:Math.random()*6.28});
    showWarning(type==='stalker'?'A SHADOW MOVED BEHIND YOU':type==='runner'?'FOOTSTEPS — FAST':'MORE INFECTED ARE COMING',1.2);
   }
 }
 if(state.sanity<35 && Math.random()<dt*.025){triggerJumpscare('whisper');}
}
function updateDreadDirector(dt){
 if(scene!=='play')return;
 dread.eventTimer-=dt;dread.ambushCooldown=Math.max(0,dread.ambushCooldown-dt);
 const low=1-state.sanity/100;
 // The prison reacts to noise and time spent lingering. Quiet is never safety.
 if(dread.eventTimer<=0){
  dread.eventTimer=Math.max(3.2,10.5-low*4)+Math.random()*5;
  const roll=Math.random();
  if(interior){
   if(roll<.28){horror.blackout=.65+Math.random()*.6;horror.glitch=.8;soundFlicker();showWarning('LIGHTS OUT. DO NOT MOVE.',1.15);}
   else if(roll<.54){showWarning(Math.random()<.5?'SOMETHING IS BREATHING IN THIS ROOM':'THE LOCK JUST TURNED',1.5);soundWhisper();horror.shake=5;}
   else if(roll<.76 && dread.ambushCooldown<=0 && interiorZombies.filter(z=>!z.dead).length<24){
    const side=Math.random()<.5?-1:1;const z={x:clamp(player.x+side*(380+Math.random()*280),75,1325),y:clamp(player.y+(Math.random()-.5)*280,115,660),hp:115,type:'stalker',attack:.4,phase:Math.random()*7,dead:false,deathTimer:0,hit:0,alert:1};interiorZombies.push(z);dread.ambushCooldown=13;showWarning('IT WAS WAITING IN THE ROOM WITH YOU',1.4);soundScare();horror.glitch=1.1;
   } else if(roll<.9){dread.phantomX=clamp(player.x+(Math.random()<.5?-1:1)*(240+Math.random()*220),50,1350);dread.phantomY=clamp(player.y+(Math.random()-.5)*160,120,650);dread.phantomTimer=1.1+Math.random()*.8;dread.phantomAlpha=.7;}
  }else if(roll<.38){showWarning('THE RADIO IS USING YOUR VOICE',1.7);soundWhisper();state.sanity=Math.max(0,state.sanity-2);}
  else if(roll<.65){horror.glitch=.9;horror.blackout=.24;soundFlicker();showWarning('MOVEMENT DETECTED BEHIND YOU',1.2);}
  else if(roll<.83){dread.phantomX=clamp(player.x+(Math.random()<.5?-1:1)*(500+Math.random()*250),80,WORLD[chapter]-80);dread.phantomTimer=1.25;dread.phantomAlpha=.65;showWarning('DO NOT FOLLOW THE FIGURE',1.2);}
  else {triggerJumpscare('random');}
 }
 if(dread.phantomTimer>0){dread.phantomTimer-=dt;dread.phantomAlpha=Math.max(0,dread.phantomAlpha-dt*.55);}
 // Low sanity causes false silhouettes, distorted perception, and faster threat escalation.
 if(state.sanity<32 && Math.random()<dt*.045){horror.glitch=.55;state.sanity=Math.max(0,state.sanity-.12);}
 if(state.sanity<18 && Math.random()<dt*.012){triggerJumpscare('random');}
}
function drawDreadPhantom(){
 if(scene!=='play'||dread.phantomTimer<=0||dread.phantomAlpha<=0)return;
 ctx.save();ctx.globalAlpha=dread.phantomAlpha*(.5+Math.sin(totalTime*19)*.22);
 if(interior){const x=dread.phantomX,y=dread.phantomY;px(x-18,y-54,36,58,'#050807');px(x-14,y-76,28,25,'#030504');px(x-10,y-67,5,3,'#b8b8a1');px(x+5,y-67,5,3,'#b8b8a1');px(x-26,y-25,9,39,'#080b0a');px(x+17,y-25,9,39,'#080b0a');}
 else{const sx=dread.phantomX-camera;px(sx-15,GROUND-103,30,70,'#050706');px(sx-12,GROUND-124,24,23,'#020403');px(sx-8,GROUND-115,4,3,'#b4b19a');px(sx+4,GROUND-115,4,3,'#b4b19a');}
 ctx.restore();
}
function crimeEvent(text,heat=0){crime.heat=clamp(crime.heat+heat,0,100);crime.clueFlash=1.4;showWarning(text,1.5);tone(58,.18,'square',.12,-35);}
function crimeCollect(){
 if(scene!=='play')return false;
 const spots=[{x:1260,y:GROUND-22,id:'blood',label:'BLOOD-SOAKED GLOVE'},{x:4930,y:GROUND-22,id:'shells',label:'9MM CASINGS'},{x:7440,y:GROUND-22,id:'photo',label:'DAMAGED SURVEILLANCE PHOTO'},{x:10020,y:GROUND-22,id:'weapon',label:'STOLEN MURDER WEAPON'},{x:14850,y:GROUND-22,id:'radio',label:'STOLEN POLICE RADIO'}];
 if(interior)return false;
 for(const q of spots){if(Math.abs(player.x-q.x)<115 && Math.abs(player.y-q.y)<120){
   if(q.id==='blood'&&!crime.evidence){crime.evidence=1;crime.deadBodySeen=true;crimeCollectMessage('EVIDENCE 01/05 — BLOOD PATTERN PHOTOGRAPHED',6);return true;}
   if(q.id==='shells'&&crime.evidence>=1){crime.evidence=Math.max(crime.evidence,2);crimeCollectMessage('EVIDENCE 02/05 — BALLISTICS CASINGS BAGGED',8);return true;}
   if(q.id==='photo'&&crime.evidence>=2){crime.evidence=Math.max(crime.evidence,3);crimeCollectMessage('EVIDENCE 03/05 — FACE MATCH FOUND',10);return true;}
   if(q.id==='weapon'&&crime.evidence>=3&&!crime.weaponFound){crime.weaponFound=true;crime.evidence=4;crime.heat=clamp(crime.heat+18,0,100);crimeCollectMessage('EVIDENCE 04/05 — MURDER WEAPON RECOVERED',18);return true;}
   if(q.id==='radio'&&crime.weaponFound&&!crime.radioFound){crime.radioFound=true;crime.evidence=5;crime.caseSolved=true;crime.witness=true;crimeCollectMessage('EVIDENCE 05/05 — RADIO LOG IDENTIFIES THE KILLER',22);return true;}
 }}
 return false;
}
function crimeCollectMessage(t,heat){crime.heat=clamp(crime.heat+heat*.18,0,100);setMessage(t,2.2);tone(320,.09,'triangle',.12,50);}
function updateCrime(dt){
 if(scene!=='play')return;
 crime.clueFlash=Math.max(0,crime.clueFlash-dt);
 crime.heat=Math.max(0,crime.heat-dt*.7);
 if(state.alarm)crime.heat=clamp(crime.heat+dt*2.8,0,100);
 if(inputState.run&&Math.abs(player.vx)>120)crime.heat=clamp(crime.heat+dt*.9,0,100);
 if(crime.heat>35)crime.policeTimer-=dt;
 if(crime.heat>35&&crime.policeTimer<=0&&!interior){
   crime.policeTimer=9+Math.random()*8;
   const side=Math.random()<.5?-1:1;const x=clamp(player.x+side*(600+Math.random()*450),120,WORLD[chapter]-120);
   const z={x,type:'runner',hp:135,maxHp:135,dead:false,deathTimer:0,phase:Math.random()*6,attack:0,hit:0,alert:1,flash:0,limb:0,crimeRole:'police'};zombies.push(z);
   crimeEvent('POLICE RESPONSE — DO NOT GET SPOTTED',4);
 }
 if(crime.caseSolved&&!crime.suspect){crime.suspect={x:clamp(player.x+Math.random()*800+500,200,WORLD[chapter]-200),hp:260,maxHp:260,phase:Math.random()*6};crimeEvent('THE SUSPECT KNOWS YOU HAVE THE EVIDENCE',15);}
 if(crime.suspect){const q=crime.suspect;const dx=player.x-q.x;if(Math.abs(dx)>65)q.x+=Math.sign(dx)*105*dt;if(Math.abs(dx)<105&&Math.random()<dt*.65){damagePlayer(27);horror.shake=9;crime.heat=100;showWarning('THE KILLER FOUND YOU.',.8);}if(q.hp<=0){crime.suspect=null;crime.heat=clamp(crime.heat-30,0,100);crimeEvent('SUSPECT DOWN — GET TO THE EXTRACTION POINT',0);}}
}
function drawCrimePixelLayer(){
 if(scene!=='play')return;
 ctx.save();
 if(!interior){
   const marks=[{x:1260,c:'#7b2c2c',n:'01'},{x:4930,c:'#b8a25e',n:'02'},{x:7440,c:'#657f91',n:'03'},{x:10020,c:'#8a3d36',n:'04'},{x:14850,c:'#6f8291',n:'05'}];
   for(const m of marks){const x=m.x-camera;if(x<-80||x>W+80)continue;for(let i=0;i<9;i++){px(x-22+i*6,GROUND-15-(i%3)*3,4,3,m.c);}text('E'+m.n,x,GROUND-31,8,'#d5cdb6','center');}
   // crime-scene tape
   const tapeY=GROUND-116;for(let i=-2;i<7;i++){const x=(((i*110-camera*.9)%W)+W)%W;line(x,tapeY,x+75,tapeY-18,'#a68f52',4);line(x,tapeY-3,x+75,tapeY-21,'#111515',2);}
   // pixel cars / police lights
   for(let i=0;i<6;i++){const x=((i*430-camera*.55)%W+W)%W,y=GROUND-48;px(x,y,92,30,'#151b1c');px(x+8,y-12,58,16,'#273233');px(x+15,y+25,18,8,'#090c0d');px(x+61,y+25,18,8,'#090c0d');if(i%3===0){px(x+32,y-18,8,4,'#a84646');px(x+41,y-18,8,4,'#58768b');}}
 }
 // high-density pixel grain gives the world a deliberate 16-bit/32-bit texture
 ctx.globalAlpha=.12;for(let i=0;i<180;i++){const x=(i*83+Math.floor(totalTime*12))%W,y=(i*47)%H;px(x,y,1+(i%3),1+(i%2),i%4?'#c8c2ad':'#6e7773');}ctx.globalAlpha=1;
 if(crime.clueFlash>0){ctx.globalAlpha=crime.clueFlash/1.4*.25;px(0,0,W,H,'#c5a55c');ctx.globalAlpha=1;}
 ctx.restore();
}
function drawCrimeHUD(){
 if(scene!=='play')return;
 const x=18,y=92;px(x,y,235,78,'rgba(4,6,6,.78)');strokeRect(x,y,235,78,'#4b514d');text('CASE 17 // CRIME SCENE',x+12,y+17,10,'#d9cba9');text(`EVIDENCE  ${crime.evidence}/5`,x+12,y+37,11,'#eee4cc');text(`HEAT      ${Math.round(crime.heat)}%`,x+12,y+55,11,crime.heat>60?'#d26b5d':'#a9b2aa');text(crime.caseSolved?'CASE FILE: SOLVED':'CASE FILE: ACTIVE',x+12,y+70,8,crime.caseSolved?'#d2b86d':'#8e9791');
 if(crime.heat>70){ctx.globalAlpha=.12+.08*Math.sin(totalTime*10);px(0,0,W,H,'#8d2525');ctx.globalAlpha=1;}
}
function updateWorldBase(dt){
 totalTime+=dt;
 if(scene==='play'){
  movementStep(dt);updateDifficultyDirector(dt);updateCrime(dt);updateHorrorDirector(dt);updateZombies(dt);updateHorror(dt);updateSmiler(dt);updateDreadDirector(dt);updateParticles(dt);updateAlcatrazProgression();if(chapter==='ALCATRAZ'&&!interior&&player.x>7000&&state.sanity<80)state.sanity=Math.max(0,state.sanity-dt*.42);if(state.finalChase&&chapter==='ALCATRAZ')state.sanity=Math.max(0,state.sanity-dt*.32);if(interior&&interior.topDown&&scene==='play'&&Math.random()<dt*.025&&state.sanity<60)triggerJumpscare('room');
 }
 updateMessage(dt);updateIntro(dt);updateFade(dt);renderHUD();
}
function updateIntro(dt){if(scene!=='intro')return;introTimer+=dt;if(introTimer>7.2)advanceIntro();}
function updateMessage(dt){if(messageTimer<=0)return;messageTimer-=dt;if(messageTimer<=0)hide('message');}
function updateFade(){if(!fadeBusy)return;}
function updateHorror(dt){horror.shake=Math.max(0,horror.shake-dt*9);horror.flash=Math.max(0,horror.flash-dt*2.7);horror.glitch=Math.max(0,horror.glitch-dt*2.5);horror.warning=Math.max(0,horror.warning-dt);const w=document.getElementById('warningText');if(w&&horror.warning<=0)w.style.opacity='0';if(scene!=='play')return;scareTimer-=dt;const danger=1-state.sanity/100;if(scareTimer<=0){scareTimer=(interior?3.5:5.5)+Math.random()*(interior?7:10);if(Math.random()<.48+danger*.32){triggerJumpscare();}else if(Math.random()<.55){showWarning(Math.random()<.5?'DID YOU HEAR THAT?':'LOOK AT THE WINDOW.');soundWhisper();}}
 if(state.sanity<50&&Math.random()<dt*.012){showWarning(Math.random()<.5?'SOMEONE IS BEHIND YOU':'THE DOOR MOVED');horror.glitch=.5;soundWhisper();}
 if(cursorMoved&&totalTime-lastCursorMove>9&&Math.random()<dt*.02){showWarning('YOU MOVED THE CURSOR. I SAW IT.');cursorMoved=false;}
 if(tabAway&&Math.random()<dt*.03){showWarning('YOU LEFT THE ISLAND. SHE DID NOT.');soundWhisper();tabAway=false;}
 if(interior&&Math.random()<dt*.055){horror.blackout=.42+Math.random()*.3;soundFlicker();setTimeout(()=>{if(horror.blackout<.8)horror.blackout=0;},320);}
}
function triggerJumpscare(kind='random'){
 jumpscareVariant=kind==='stair'?3:Math.floor(Math.random()*4);
 horror.flash=1.15;horror.shake=28;horror.glitch=1.25;state.sanity=Math.max(0,state.sanity-7);showWarning(jumpscareVariant===0?'DON’T TURN AROUND':jumpscareVariant===1?'HE IS IN THE CELL':jumpscareVariant===2?'RUN. RUN. RUN.':'THE STAIRS ARE NOT EMPTY',1.2);soundScare();
 const e=document.getElementById('scare');
 if(e){e.dataset.variant=String(jumpscareVariant);e.classList.add('show');setTimeout(()=>e.classList.remove('show'),850);}
 setTimeout(()=>{if(scene==='play'&&Math.random()<.45){horror.blackout=.45;soundFlicker();}},300);
}
function updateSmiler(dt){if(scene!=='play'||interior)return;smiler.cooldown-=dt;if(smiler.active){smiler.timer-=dt;smiler.intensity=Math.min(1,smiler.intensity+dt*1.4);state.sanity=Math.max(0,state.sanity-dt*.2);if(smiler.timer<=0){smiler.active=false;smiler.intensity=0;smiler.cooldown=20+Math.random()*35;}}else if(smiler.cooldown<=0){const chance=.0025+(1-state.sanity/100)*.0035;if(Math.random()<dt*chance){smiler.active=true;smiler.timer=2.7+Math.random()*3.2;smiler.x=clamp(player.x+(Math.random()<.5?-1:1)*(430+Math.random()*520),100,WORLD[chapter]-100);soundScare();showWarning('THE SMILER IS WATCHING');}}}
function updateParticles(dt){for(const p of particles){p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.g*dt;p.life-=dt;}particles=particles.filter(p=>p.life>0);}
function spawnDust(x=player.x,y=GROUND){for(let i=0;i<8;i++)particles.push({x:x+(Math.random()-.5)*22,y:y-3,vx:(Math.random()-.5)*60,vy:-30-Math.random()*60,g:120,life:.25+Math.random()*.2,c:'#aaa89c',s:2+Math.random()*3});}
function spawnBlood(x,y){for(let i=0;i<10;i++)particles.push({x,y,vx:(Math.random()-.5)*120,vy:-20-Math.random()*110,g:230,life:.25+Math.random()*.25,c:'#9a4747',s:2+Math.random()*3});}
function spawnSpark(x,y){for(let i=0;i<7;i++)particles.push({x,y,vx:(Math.random()-.5)*90,vy:-30-Math.random()*80,g:160,life:.2+Math.random()*.25,c:'#ddbf77',s:2});}
function safeAudio(){try{if(!audioCtx){audioCtx=new(window.AudioContext||window.webkitAudioContext)();masterGain=audioCtx.createGain();musicGain=audioCtx.createGain();sfxGain=audioCtx.createGain();rainGain=audioCtx.createGain();masterGain.gain.value=1.0;musicGain.gain.value=.55;sfxGain.gain.value=1.45;rainGain.gain.value=.24;musicGain.connect(masterGain);sfxGain.connect(masterGain);rainGain.connect(masterGain);masterGain.connect(audioCtx.destination);}if(audioCtx.state==='suspended')audioCtx.resume();return true;}catch(e){return false;}}
function tone(freq,dur,type='sine',vol=.08,slide=0,group='sfx'){if(!soundEnabled)return;if(!safeAudio())return;const now=audioCtx.currentTime,o=audioCtx.createOscillator(),g=audioCtx.createGain();o.type=type;o.frequency.setValueAtTime(Math.max(20,freq),now);if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(20,freq+slide),now+dur);g.gain.setValueAtTime(.0001,now);g.gain.exponentialRampToValueAtTime(vol,now+.012);g.gain.exponentialRampToValueAtTime(.0001,now+dur);o.connect(g);g.connect(group==='music'?musicGain:group==='rain'?rainGain:sfxGain);o.start(now);o.stop(now+dur+.03);}
function noiseBurst(dur=.12,vol=.06,group='sfx'){if(!soundEnabled||!safeAudio())return;const b=audioCtx.createBuffer(1,audioCtx.sampleRate*dur,audioCtx.sampleRate),d=b.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*(1-i/d.length);const s=audioCtx.createBufferSource(),g=audioCtx.createGain();s.buffer=b;g.gain.value=vol;s.connect(g);g.connect(group==='rain'?rainGain:sfxGain);s.start();}
function startSoundscape(){safeAudio();if(!audioCtx||musicTimer)return;tone(39,2.8,'sine',.025,5,'music');tone(58,2.2,'triangle',.018,-9,'music');musicTimer=setInterval(()=>{if(!soundEnabled)return;tone(state.sanity<55?36:46,2.4,'sine',.024,4,'music');if(Math.random()<.6)tone(91,1.1,'triangle',.012,-8,'music');},2300);rainTimer=setInterval(()=>{if(scene==='play'&&!interior&&soundEnabled){noiseBurst(.05,.018,'rain');if(Math.random()<.18)tone(150,.035,'sine',.02,-70,'rain');}},240);}
function soundStep(){tone(inputState.run?105:78,.055,'square',.13,-18);noiseBurst(.018,.03);}
function soundJump(){tone(175,.11,'triangle',.11,80);}
function soundLand(){tone(55,.09,'sine',.11,-20);noiseBurst(.035,.05);}
function soundChest(){tone(120,.12,'square',.23,75);setTimeout(()=>tone(260,.15,'sine',.17,55),70);setTimeout(()=>tone(410,.18,'triangle',.12,0),145);}
function soundPickup(){tone(560,.1,'sine',.18,130);setTimeout(()=>tone(790,.08,'sine',.12,0),70);}
function soundDoor(){tone(48,.26,'square',.18,20);noiseBurst(.11,.08);}
function soundReload(){tone(160,.09,'square',.12,45);setTimeout(()=>tone(108,.11,'square',.11,-30),100);setTimeout(()=>tone(220,.12,'square',.1,0),210);}
function soundShot(){tone(420,.055,'square',.26,-230);noiseBurst(.06,.18);}
function soundScare(){tone(65,.8,'sawtooth',.42,-48);setTimeout(()=>tone(37,.9,'square',.3,-5),100);setTimeout(()=>noiseBurst(.62,.28),120);setTimeout(()=>tone(680,.21,'sawtooth',.32,-500),150);}
function soundWhisper(){tone(38,.35,'sine',.025,-2);setTimeout(()=>tone(480,.08,'triangle',.025,-200),100);}
function soundFlicker(){tone(95,.05,'square',.08,-45);setTimeout(()=>tone(71,.05,'square',.07,-40),80);}
function drawSky(){
 const sf=chapter==='SAN FRANCISCO';const g=ctx.createLinearGradient(0,0,0,500);g.addColorStop(0,sf?'#061019':'#071219');g.addColorStop(.48,sf?'#162a34':'#12272d');g.addColorStop(1,sf?'#314447':'#2d4548');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 const moonX=1040,moonY=104;glow(moonX,moonY,135,'rgba(225,219,194,.14)','rgba(225,219,194,0)');ctx.fillStyle='rgba(223,217,196,.75)';ctx.beginPath();ctx.arc(moonX,moonY,43,0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(75,77,72,.28)';ctx.beginPath();ctx.arc(moonX-12,moonY-10,23,0,Math.PI*2);ctx.fill();
 for(let i=0;i<140;i++){const x=((i*131-camera*.07)%W+W)%W;const y=24+(i*53)%325;ctx.globalAlpha=.14+.3*((i%7)/7);px(x,y,1+(i%2),1+(i%2),i%11===0?'#9caeae':'#53666a');}ctx.globalAlpha=1;
 for(let layer=0;layer<5;layer++){const par=camera*(.035+layer*.032);for(let i=-4;i<20;i++){const x=i*150-(par%150)+layer*31;const h=78+((i*37+layer*29)%150);const w=104+((i*23+layer*17)%68);const c=['#102127','#13282d','#183036','#20383c','#294144'][layer];px(x,428-h,w,h,c);px(x,428-h,w,5,'#385055');for(let q=0;q<4;q++){const wx=x+16+q*23,yy=448-h+((q+layer)%3)*31;if((q+i+layer)%3===0){px(wx,yy,11,17,'#46544f');if((q+layer)%2===0)px(wx+2,yy+3,7,11,'#8e7953');}}}}
 const haze=ctx.createLinearGradient(0,320,0,480);haze.addColorStop(0,'rgba(168,193,188,.02)');haze.addColorStop(.6,'rgba(167,190,186,.09)');haze.addColorStop(1,'rgba(4,8,9,.17)');ctx.fillStyle=haze;ctx.fillRect(0,300,W,190);
 if(sf)drawGoldenGate();
}
function drawGoldenGate(){const base=390-camera*.07;ctx.save();ctx.globalAlpha=.26;line(base,390,base+180,240,'#687978',3);line(base+360,390,base+180,240,'#687978',3);px(base+160,225,22,170,'#596866');px(base+200,225,22,170,'#596866');for(let i=0;i<7;i++){line(base+172+i*8,240,base+360-i*17,385,'#596866',1);line(base+210-i*8,240,base+20+i*20,385,'#596866',1);}ctx.restore();}
function drawOcean(){if(chapter!=='ALCATRAZ')return;ctx.fillStyle='#0b2028';ctx.fillRect(0,365,W,70);for(let i=0;i<75;i++){const x=((i*73-camera*.18)%W+W)%W;const y=375+(i%7)*8;line(x,y,x+22,y,'#2b4c57',1);line(x+29,y+3,x+48,y+3,'#1a343d',1);} }
function drawGround(){const base=chapter==='ALCATRAZ'?'#46514f':'#444c4f';ctx.fillStyle=base;ctx.fillRect(0,430,W,H-430);const road=chapter==='ALCATRAZ'?'#2f3938':'#31383a';ctx.fillStyle=road;ctx.fillRect(0,555,W,233);px(0,430,W,4,'#738078');for(let i=0;i<500;i++){const x=((i*71-camera*.91)%W+W)%W;const y=442+(i*43)%260;const c=i%17===0?'#92978b':i%5===0?'#67706b':'#394240';px(x,y,1+(i%3),1+(i%2),c);}for(let i=0;i<46;i++){const x=((i*241-camera*.71)%W+W)%W;const y=585+(i%5)*24;line(x,y,x+16+(i%4)*9,y+(i%3)-1,'#1d2525',1);}for(let i=0;i<13;i++){const x=((i*317-camera*.55)%W+W)%W;ctx.fillStyle=`rgba(198,215,210,${.025+(i%4)*.013})`;ctx.beginPath();ctx.ellipse(x,538+(i%5)*8,35+(i%4)*12,5+(i%2),0,0,Math.PI*2);ctx.fill();}}
function drawIslandRoad(){if(chapter!=='ALCATRAZ')return;for(let i=0;i<22;i++){const x=((i*780-camera*.76)%W+W)%W;poly([[x,555],[x+180,555],[x+240,540],[x+60,540]],i%2?'#3a4543':'#36403f');}}
function drawLandmarks(){if(chapter!=='ALCATRAZ')return;for(const l of landmarkData){const x=l.x-camera;if(x<-l.w-200||x>W+200)continue;const h=l.h;const top=GROUND-h;const body=l.type==='cellhouse'?'#4d5a5c':l.type==='medical'?'#5c6d6f':l.type==='power'?'#4c595a':l.type==='tower'?'#3f4b4d':l.type==='lighthouse'?'#64706c':'#4f5d5e';px(x-l.w/2,top,l.w,h,body);px(x-l.w/2,top,l.w,9,'#87908b');px(x-l.w/2+10,top+18,l.w-20,6,'#2f3a3b');if(l.type==='cellhouse'){for(let j=0;j<16;j++){const wx=x-l.w/2+18+j*65;px(wx,top+47,42,34,'#263335');px(wx+4,top+52,34,24,j%4===0?'#857453':'#3d4b4c');}for(let j=0;j<18;j++){const gx=x-l.w/2+19+j*56;px(gx,top+95,5,h-108,'#1a2425');px(gx+2,top+104,2,h-124,'#79827d');}}
 else if(l.type==='yard'){for(let j=0;j<12;j++){const gx=x-l.w/2+j*(l.w/11);px(gx,top-18,5,h+18,'#68716c');}for(let j=0;j<5;j++)line(x-l.w/2+j*180,top,x-l.w/2+j*180,GROUND-10,'#64706c',2);}
 else if(l.type==='tower'){px(x-44,top+34,88,h-35,'#495658');px(x-58,top+18,116,14,'#737c77');px(x-10,top-5,20,24,'#252c2d');glow(x,top+8,58,'rgba(224,197,126,.08)','rgba(0,0,0,0)');}
 else if(l.type==='lighthouse'){px(x-42,top+70,84,h-70,'#5f6b68');px(x-55,top+56,110,14,'#7b827b');px(x-25,top+8,50,56,'#273233');glow(x,top+35,80,'rgba(229,204,133,.09)','rgba(0,0,0,0)');}
 else {const count=Math.max(3,Math.floor((l.w-60)/52));for(let j=0;j<count;j++){const wx=x-l.w/2+30+j*52;const lit=(j+Math.floor(l.x/200))%5===0;px(wx,top+43,34,34,lit?'#7c7253':'#273537');px(wx+4,top+47,26,26,lit?'#b2965c':'#3c4b4c');if(lit)glow(wx+17,top+61,30,'rgba(227,197,123,.055)','rgba(0,0,0,0)');}}
 text(l.name,x,top-16,11,'#ebe2cc','center');}
}
function drawBuildings(){if(chapter!=='SAN FRANCISCO')return;const bs=[{x:850,w:580,h:250,n:'OLD POLICE STATION',t:'police'},{x:2700,w:520,h:280,n:'HOSPITAL',t:'hospital'},{x:4700,w:510,h:240,n:'FUNERAL HOME',t:'funeral'},{x:6500,w:620,h:330,n:'OLD HOTEL',t:'hotel'},{x:8600,w:580,h:260,n:'EMERGENCY SHELTER',t:'shelter'},{x:9900,w:620,h:310,n:'RESEARCH ANNEX',t:'research'}];for(const b of bs){const x=b.x-camera;if(x<-b.w||x>W+b.w)continue;const col={police:'#596b70',hospital:'#65797a',funeral:'#635b63',hotel:'#6b726f',shelter:'#5d716b',research:'#5e6f79'}[b.t];px(x-b.w/2,GROUND-b.h,b.w,b.h,col);px(x-b.w/2,GROUND-b.h,b.w,10,'#8b948f');for(let f=0;f<Math.max(2,Math.round(b.h/96));f++){const yy=GROUND-58-f*96;const count=Math.floor((b.w-60)/50);for(let j=0;j<count;j++){const wx=x-b.w/2+30+j*50;const lit=(j+f)%6===0;px(wx,yy-32,34,32,lit?'#857656':'#283638');px(wx+4,yy-28,26,24,lit?'#b69b60':'#3f4d4e');}}const door=x-34;px(door,GROUND-82,68,82,'#1b2425');px(door+6,GROUND-76,56,70,'#465251');px(door+45,GROUND-43,5,5,'#d9c27e');text(b.n,x,GROUND-b.h-16,11,'#efe5cf','center');}}
function drawStreetProps(){const lamps=chapter==='ALCATRAZ'?[1200,3300,4750,5900,7600,9300,10700,12100,13900,15350,16000]:[700,2100,3600,5200,6800,8400,9800];for(const wx of lamps){const x=wx-camera;if(x<-100||x>W+100)continue;px(x,GROUND-170,7,170,'#1b2324');px(x-12,GROUND-178,31,9,'#4b5452');const unstable=chapter==='ALCATRAZ'&&Math.abs(player.x-wx)<300&&state.sanity<65;const flick=unstable?Math.random():.9+.1*Math.sin(totalTime*2.2+wx);px(x-8,GROUND-190,22,12,'#252e2f');px(x-4,GROUND-191,14,5,flick>.52?'#ddc77f':'#675a44');if(flick>.28)glow(x+2,GROUND-182,86,'rgba(224,198,124,.08)','rgba(0,0,0,0)');}}
function drawSigns(){if(chapter==='ALCATRAZ'){const s=[{x:3400,t:'DINING HALL →'},{x:5450,t:'HOSPITAL WING →'},{x:7250,t:'MODEL INDUSTRIES →'},{x:8950,t:'NEW INDUSTRIES →'},{x:15440,t:'LIGHTHOUSE / DOCK →'}];for(const a of s){const x=a.x-camera;if(x<-160||x>W+160)continue;px(x-95,GROUND-250,190,48,'#303a3b');px(x-89,GROUND-244,178,34,'#727c77');text(a.t,x,GROUND-219,10,'#f2e8cf','center');}}else{const s=[{x:2300,t:'HOSPITAL →'},{x:4400,t:'FUNERAL HOME →'},{x:6400,t:'OLD HOTEL →'},{x:8500,t:'SHELTER →'}];for(const a of s){const x=a.x-camera;if(x<-160||x>W+160)continue;px(x-85,GROUND-235,170,42,'#303a3b');px(x-79,GROUND-229,158,30,'#717a75');text(a.t,x,GROUND-209,10,'#f2e8cf','center');}}}
function drawDock(){if(chapter!=='ALCATRAZ')return;const x=21700-camera;px(x-170,GROUND-31,340,31,'#4f5b58');for(let i=0;i<7;i++)px(x-148+i*48,GROUND-37,32,7,'#7a7f76');px(x-33,GROUND-158,66,126,'#252d2f');px(x-43,GROUND-171,86,13,'#707771');const bc=state.beacon?'#f3d27e':'#5d513a';px(x-20,GROUND-196,40,22,bc);glow(x,GROUND-188,125,state.beacon?'rgba(239,204,121,.2)':'rgba(150,130,82,.05)','rgba(0,0,0,0)');px(x-123,GROUND-69,246,7,'#1d2324');px(x-117,GROUND-90,234,24,'#455252');px(x-94,GROUND-116,188,22,'#5a6666');px(x-54,GROUND-139,108,20,'#657171');text('FERRY',x,GROUND-153,13,'#eee4c6','center');text(state.beacon?'BOARD':state.radioSignal?'SIGNAL READY':'BEACON',x,GROUND-214,10,'#d8ca9e','center');}
function drawInterior(){
 if(!interior)return;
 ctx.save();
 const type=interior.type;const floor=interior.floor||1;
 const walls={cell:'#3b4140',cellcorridor:'#30383a',medical:'#465b5d',industry:'#3f4540',dining:'#514c43',guard:'#3c4b4d',power:'#3c4545',police:'#3e5559',hospital:'#4d6365',funeral:'#4d444d',hotel:'#555b56',shelter:'#4d625b'};
 px(0,0,W,H,walls[type]||'#3c4542');
 // tiled floor
 for(let y=82;y<H;y+=42)for(let x=0;x<W;x+=42){const alt=((x/42+y/42+floor)%2)?'#202827':'#252d2c';px(x,y,40,40,alt);if((x+y)%126===0)px(x+5,y+7,3,2,'#56615d');}
 // perimeter walls and doors
 px(0,0,W,78,'#171d1e');px(0,0,28,H,'#14191a');px(W-28,0,28,H,'#14191a');px(0,H-55,W,55,'#14191a');
 px(42,86,1316,5,'#66706c');px(42,682,1316,5,'#5a625f');
 // deep perspective bands and floor stains
 for(let y=170;y<680;y+=86){ctx.globalAlpha=.16;px(30,y,1340,2,'#0b1010');ctx.globalAlpha=1;}
 for(let i=0;i<32;i++){const sx=50+(i*173)%1280, sy=110+(i*97)%540;px(sx,sy,3+(i%4),1+(i%3),i%5===0?'#714f48':'#303b39');}
 // ceiling lamps, flicker
 for(let x=120;x<1320;x+=220){px(x,54,72,9,'#56605b');const f=.55+.45*Math.sin(totalTime*7+x);glow(x+36,75,100,`rgba(224,210,166,${.045*f})`,'rgba(0,0,0,0)');}
 // room dividers, pipes, grime
 for(let x=190;x<1300;x+=220){px(x,100,9,540,'#1a2222');px(x+3,100,3,540,'#59635f');}
 for(let i=0;i<35;i++){const x=(i*83)%1320+40,y=100+(i*47)%540;px(x,y,2+(i%4),2,'#737269');}
 // stairwells as real floor transitions
 if(interior.floors>1){for(const sx of [145,1245]){px(sx-55,245,110,250,'#171e1f');px(sx-45,255,90,230,'#394443');for(let i=0;i<9;i++){px(sx-34+i*7,450-i*20,68,8,'#6b726d');px(sx-34+i*7,458-i*20,68,4,'#202726');}text(sx<700?'UP / DOWN':'UP / DOWN',sx,490,9,'#ded4ba','center');}}
 // interactive furniture / search zones
 const props= type==='medical'?[['MEDICAL DESK',1030,380],['OPERATING TABLE',480,220],['SUPPLY CABINET',820,530]]:
 type==='industry'?[['WORKBENCH',470,420],['PRESS',860,250],['SCRAP PILE',1120,530]]:
 type==='cellcorridor'?[['CELL BANK',330,220],['CELL BANK',650,520],['WATCH DESK',1090,330]]:
 [['TABLE',470,350],['CABINET',820,250],['LOCKERS',1080,520]];
 for(const [label,x,y] of props){px(x-55,y-25,110,50,'#171f1f');px(x-48,y-19,96,8,'#59625e');px(x-43,y-9,86,28,'#2d3735');text(label,x,y+48,7,'#aaa58f','center');}
 ctx.restore();
}
function drawInteriorZombies(){
 if(!interior)return;
 for(const z of interiorZombies){if(z.deathTimer<=0&&z.dead)continue;const x=z.x,y=z.y;ctx.save();ctx.translate(x,y);const bob=Math.sin(totalTime*7+z.phase)*2;ctx.translate(0,bob);ctx.globalAlpha=z.dead?clamp(z.deathTimer/.65,0,1):1;
  const scale=z.type==='runner'?1.05:z.type==='stalker'?1.12:1;ctx.scale(scale,scale);
  px(-13,-18,26,28,'#26302f');px(-9,-31,18,15,'#5b5047');px(-6,-27,4,3,'#d6d1bd');px(3,-27,4,3,'#d6d1bd');px(-15,8,8,20,'#202827');px(7,8,8,20,'#202827');px(-22,-5,8,20,'#303a38');px(14,-5,8,20,'#303a38');
  if(z.hit>0){px(-18,-34,36,48,'rgba(235,235,220,.45)');}if(!z.dead){px(-18,-43,36,4,'#171d1c');px(-18,-43,36*clamp(z.hp/(z.type==='stalker'?115:z.type==='runner'?90:65),0,1),4,'#a65a52');}
  ctx.restore();
 }
}
function drawInteriorDecor(){
 if(!interior)return;
 if(interior.floors>1){drawStairwell();}
 for(let i=0;i<14;i++){
  const x=32+i*101;
  const y=362+(i%3)*30;
  px(x,y,48,4,'#222c2c');
  px(x+8,y-18,30,16,i%4===0?'#7e6c4c':'#48534f');
 }
 for(let i=0;i<9;i++){
  const x=180+i*127;
  px(x,524,60,5,'#252d2c');
  px(x+10,516,42,5,'#58615c');
 }
 if(interior.type==='medical'){
  for(let i=0;i<5;i++){
   const x=260+i*170;
   px(x,120,44,8,'#d8ddd7');
   px(x+17,100,9,28,'#b3bab3');
  }
 }
 if(interior.type==='industry'){
  for(let i=0;i<7;i++){
   const x=180+i*145;
   px(x,300,70,72,'#293333');
   px(x+8,312,54,48,'#4c5c58');
  }
 }
 if(interior.type==='cellcorridor'){
  for(let i=0;i<12;i++){
   const x=205+i*82;
   px(x,120,5,300,'#1b2525');
   px(x+2,130,2,282,'#747c76');
  }
 }
}
function drawDynamicWeather(){
 if(scene!=='play')return;
 if(interior)return;
 if(Math.random()<.05){
  const x=Math.random()*W;
  const y=430+Math.random()*120;
  px(x,y,2,2,'#c4d2cd');
 }
 if(chapter==='ALCATRAZ'){
  for(let i=0;i<8;i++){
   const x=((i*211-camera*.25)%W+W)%W;
   const y=425+(i%3)*8;
   line(x,y,x+38,y-3,'rgba(185,204,201,.22)',1);
  }
 }
}
function extraAnimationPass(){
 if(scene!=='play')return;
 const phase=Math.sin(totalTime*3.2);
 if(!interior&&Math.abs(player.vx)>30){
  ctx.save();ctx.globalAlpha=.16;
  const x=player.x-camera+19;
  for(let i=0;i<3;i++){
   px(x-player.facing*(18+i*11),GROUND-48+i*3,4,3,'#9a9a8d');
  }
  ctx.restore();
 }
 if(interior&&interior.type!=='cell'){
  const x=700+Math.sin(totalTime*.7)*220;
  glow(x,85,42,'rgba(235,217,170,.055)','rgba(0,0,0,0)');
 }
 if(phase>.94&&Math.random()<.04)spawnSpark(player.x-camera+19,GROUND-120);
}
function enhanceHorrorAtmosphere(){
 if(scene!=='play')return;
 ctx.save();
 if(state.sanity<65){
  ctx.globalAlpha=.05+(65-state.sanity)*.0012;
  for(let i=0;i<7;i++){const y=90+((i*113+totalTime*31)%530);px(0,y,W,1,'#d4d0bf');}
 }
 if(smiler.active&&!interior){ctx.globalAlpha=.08;const edge=smiler.x<player.x?0:W-10;px(edge,0,10,H,'#e7e0d1');}
 ctx.restore();
}


function drawAlcatrazInfrastructure(){
 if(chapter!=='ALCATRAZ'||interior)return;
 const pipes=[5200,6800,9100,11200,13400,15600,17700,19900];
 for(const wx of pipes){
  const x=wx-camera;if(x<-200||x>W+200)continue;
  line(x,GROUND-175,x+180,GROUND-175,'#596562',6);
  line(x+180,GROUND-175,x+180,GROUND-90,'#596562',6);
  for(let k=0;k<4;k++)px(x+k*58,GROUND-183,18,8,'#303b3a');
 }
 const flood=[2600,5100,8000,11600,14600,18200,20500];
 for(const wx of flood){
  const x=wx-camera;if(x<-100||x>W+100)continue;
  px(x-3,GROUND-260,6,160,'#202929');
  px(x-14,GROUND-270,28,14,'#77786b');
  const hot=state.alarm||Math.sin(totalTime*3+wx)>-.15;
  glow(x,GROUND-260,105,hot?'rgba(224,192,116,.10)':'rgba(224,192,116,.045)','rgba(0,0,0,0)');
 }
 for(let i=0;i<26;i++){
  const x=((i*401-camera*.92)%W+W)%W;
  const y=520+(i%5)*15;
  px(x,y,28,5,'#1d2525');
  px(x+5,y-8,18,8,i%6===0?'#6c5747':'#394543');
 }
 if(state.alarm){
  const sweep=((totalTime*190)%W);
  ctx.globalAlpha=.055;
  ctx.fillStyle='#a83d3d';
  ctx.beginPath();ctx.moveTo(sweep,GROUND-320);ctx.lineTo(sweep+220,GROUND);ctx.lineTo(sweep+340,GROUND);ctx.lineTo(sweep+120,GROUND-320);ctx.closePath();ctx.fill();
  ctx.globalAlpha=1;
 }
}

function drawPixelDetailPass(){
 if(scene!=='play')return;
 ctx.save();
 // Dense foreground pixels give the scene a higher-resolution hand-pixeled feel.
 const base=interior?GROUND-42:GROUND;
 for(let i=0;i<95;i++){
  const wx=((i*137-camera*.92)%W+W)%W;
  const yy=base-((i*29)%115);
  const s=1+(i%3);
  const col=i%9===0?'#8b8878':i%4===0?'#4e5b57':'#2a3332';
  px(wx,yy,s,Math.max(1,s-1),col);
 }
 // animated dust/embers inside dark buildings
 if(interior){for(let i=0;i<22;i++){const xx=(i*71+totalTime*(8+i%3)*2)%W;const yy=145+(i*43)%350;px(xx,yy,1+(i%2),1,'#a89b79');}}
 // wet pavement glints
 if(!interior){for(let i=0;i<18;i++){const xx=((i*181-camera*.7)%W+W)%W;const yy=560+(i%5)*23;line(xx,yy,xx+16+(i%4)*5,yy,'#566966',1);}}
 ctx.restore();
}
function drawDistantTerrain(){
 const par=camera*.12;
 if(chapter==='ALCATRAZ'){
  for(let i=0;i<9;i++){
   const x=i*220-par%220;
   const h=38+(i%4)*16;
   poly([[x-90,438],[x-28,438-h],[x+28,438-h-16],[x+90,438]],'#1b2b2e');
  }
 }else{
  for(let i=0;i<12;i++){
   const x=i*190-par%190;
   const h=50+(i%5)*19;
   px(x,430-h,140,h,'#15272d');
   px(x+18,430-h+18,22,26,i%3?'#2e454a':'#776b4f');
   px(x+72,430-h+46,25,32,i%2?'#30464a':'#75694e');
  }
 }
}
function drawTerrainTexture(){
 const bands=[{y:462,c:'#56615d'},{y:492,c:'#4f5b58'},{y:528,c:'#3f4a48'}];
 for(const b of bands){
  for(let i=0;i<55;i++){
   const x=((i*149-camera*(.65+(b.y%3)*.05))%W+W)%W;
   px(x,b.y+(i%4)*3,20+(i%5)*5,2,b.c);
  }
 }
 for(let i=0;i<24;i++){
  const x=((i*251-camera*.82)%W+W)%W;
  const y=548+(i%7)*8;
  px(x,y,8+(i%4)*4,2,'#71807a');
  px(x+7,y+5,3,2,'#252e2d');
 }
}
function drawAlcatrazDetails(){
 const fenceXs=[420,1810,2920,5050,6850,8450,10150,11350,12800,14380,15280,15820];
 for(const wx of fenceXs){
  const x=wx-camera;if(x<-100||x>W+100)continue;
  for(let i=0;i<7;i++){
   const xx=x+i*34;
   px(xx,GROUND-92,4,92,'#1c2728');
   px(xx+1,GROUND-87,2,86,'#717b76');
  }
  line(x,GROUND-92,x+204,GROUND-92,'#56625f',2);
  line(x,GROUND-72,x+204,GROUND-72,'#3d4847',1);
 }
 const guardLights=[1050,4700,10820,13900,15580];
 for(const wx of guardLights){const x=wx-camera;if(x>-100&&x<W+100){glow(x,GROUND-245,72,'rgba(229,203,133,.08)','rgba(0,0,0,0)');px(x-3,GROUND-250,6,16,'#a79566');}}
 for(let i=0;i<16;i++){
  const x=((i*317-camera*.48)%W+W)%W;
  const y=500+(i%4)*16;
  px(x,y,18,4,i%3?'#35413f':'#81765e');
 }
}
function drawCityRoads(){
 for(let i=0;i<8;i++){
  const x=((i*610-camera*.8)%W+W)%W;
  px(x,GROUND-6,260,6,'#454d4d');
  px(x+20,GROUND+12,78,4,'#565d58');
  px(x+125,GROUND+12,78,4,'#565d58');
 }
 for(let i=0;i<18;i++){
  const x=((i*319-camera*.56)%W+W)%W;
  px(x,GROUND+26,58,4,'#5c6260');
 }
}
function drawCityDetails(){
 for(let i=0;i<17;i++){
  const x=((i*405-camera*.36)%W+W)%W;
  const y=545+(i%5)*10;
  px(x,y,28,3,i%4?'#4e5855':'#8d7c5a');
  if(i%3===0)px(x+20,y-8,3,11,'#252e2d');
 }
 for(let i=0;i<7;i++){
  const x=((i*950-camera*.42)%W+W)%W;
  line(x,340,x+165,320,'#39484d',1);
  line(x+30,334,x+196,345,'#39484d',1);
 }
}
function drawFootprints(){if(interior)return;for(const f of footprints){const x=f.x-camera;if(x>-20&&x<W+20){ctx.globalAlpha=clamp(1-(totalTime-f.f)*.035,.05,.45);px(x,GROUND-7,10,3,'#a7adaa');px(x+14,GROUND-8,8,2,'#8e9892');}}ctx.globalAlpha=1;}
function drawSurvivorShadows(){
 if(chapter!=='SAN FRANCISCO')return;
 for(const s of survivors){if(s.found)continue;const x=s.x-camera;if(x>-120&&x<W+120){ctx.globalAlpha=.18;ctx.beginPath();ctx.ellipse(x,GROUND-3,23,6,0,0,Math.PI*2);ctx.fillStyle='#050707';ctx.fill();ctx.globalAlpha=1;}}
}
function drawSurvivors(){if(chapter!=='SAN FRANCISCO')return;for(const s of survivors){if(s.found)continue;const x=s.x-camera;if(x<-100||x>W+100)continue;const phase=totalTime*3+s.x*.01;const sw=Math.sin(phase)*5;px(x-13,GROUND-30,10,30,'#252b2b');px(x+4,GROUND-30,10,30,'#252b2b');px(x-18,GROUND-59,37,31,s.name==='MARA'?'#76594c':s.name==='ELI'?'#536f7c':'#6a6b60');px(x-11,GROUND-80,24,25,'#cda890');px(x-15,GROUND-91,31,13,s.name==='NOAH'?'#403b35':'#2d2826');px(x-23-sw,GROUND-50,8,24,'#5d675f');px(x+17+sw,GROUND-50,8,24,'#5d675f');text(s.name,x,GROUND-105,11,'#f5e4c3','center');if(Math.abs(player.x-s.x)<125)text('E • TALK',x,GROUND-122,10,'#f0d59e','center');}}
function drawZombies(){for(const z of zombies){if(z.dead)continue;const x=z.x-camera;if(x<-130||x>W+130)continue;const phase=totalTime*(z.type==='runner'?7:z.type==='brute'?2.5:3.7)+z.phase;const a=Math.sin(phase),b=Math.sin(phase+1.5);const bob=Math.sin(phase*.8)*2;const body=z.type==='warden'?'#171b1d':z.type==='brute'?'#60474d':z.type==='runner'?'#76524d':'#53615f';const skin='#7b635a';ctx.save();ctx.translate(0,bob);const sc=z.type==='warden'?1.48:z.type==='brute'?1.15:1;ctx.scale(sc,1);px(x-16+a*2,GROUND-67,32,50,body);px(x-13,GROUND-94,26,29,skin);px(x-10,GROUND-89,20,20,body);px(x-28-b*5,GROUND-55,9,30,body);px(x+19+a*5,GROUND-55,9,30,body);px(x-15-b*3,GROUND-17,11,17,'#1b1f20');px(x+5+a*3,GROUND-17,11,17,'#1b1f20');px(x-8,GROUND-84,4,4,'#e96a59');px(x+5,GROUND-84,4,4,'#e96a59');px(x-5,GROUND-72,12,3,'#251b1b');if(z.type==='warden'){px(x-24,GROUND-108,48,10,'#252a2c');px(x-31,GROUND-53,12,18,'#111517');px(x+20,GROUND-53,12,18,'#111517');px(x-5,GROUND-91,10,4,'#b83f3f');}if(z.type==='brute'){px(x-24,GROUND-103,48,7,'#394340');px(x-33,GROUND-50,9,14,'#715052');px(x+24,GROUND-50,9,14,'#715052');}ctx.restore();if(Math.abs(player.x-z.x)<95&&Math.abs(player.x-z.x)>45)showWarning('THE INFECTED HEARD YOU',.55);}}
function drawSmiler(){if(!smiler.active||interior)return;const x=smiler.x-camera;if(x<-250||x>W+250)return;const alpha=clamp(smiler.intensity,0,1);const h=338+Math.sin(totalTime)*8;ctx.save();ctx.globalAlpha=.98*alpha;px(x-30,GROUND-h,60,h,'#020303');px(x-45,GROUND-h-55,90,66,'#010202');px(x-22,GROUND-h-33,12,8,'#f2ead9');px(x+10,GROUND-h-33,12,8,'#f2ead9');px(x-13,GROUND-h-9,26,4,'#f3e8da');for(let i=0;i<8;i++)px(x-16+i*4,GROUND-h+1,3,4,'#cfc6b7');px(x-49,GROUND-h+34,12,160,'#010202');px(x+37,GROUND-h+34,12,160,'#010202');ctx.restore();}
function drawPlayerShadow(){
 if(interior)return;
 const x=player.x-camera+19;
 const y=GROUND+1;
 ctx.save();ctx.globalAlpha=.28;ctx.fillStyle='#050708';ctx.beginPath();ctx.ellipse(x,y,28+Math.min(10,Math.abs(player.vx)*.03),7,0,0,Math.PI*2);ctx.fill();ctx.restore();
}
function drawRain(){if(interior)return;ctx.save();ctx.globalAlpha=.46;for(let i=0;i<230;i++){const x=(i*83+totalTime*420)%W;const y=(i*47+totalTime*660)%H;line(x,y,x-6,y+18,'#9cb7bf',1);}ctx.restore();}
function drawParticles(){for(const p of particles){const x=p.x-camera;if(x<-20||x>W+20)continue;ctx.globalAlpha=clamp(p.life/.5,0,1);px(x,p.y,p.s,p.s,p.c);}ctx.globalAlpha=1;}
function drawLighting(){if(scene!=='play')return;ctx.save();if(interior){if(state.light){const flick=.86+.14*Math.sin(totalTime*7);glow(700,105,450,`rgba(240,226,192,${.08*flick})`,'rgba(0,0,0,0)');}}else{ctx.fillStyle='rgba(0,0,0,.09)';ctx.fillRect(0,0,W,H);}ctx.restore();}
function drawHorror(){if(scene!=='play')return;ctx.save();if(horror.shake>0)ctx.translate((Math.random()-.5)*horror.shake,(Math.random()-.5)*horror.shake);if(horror.flash>0){ctx.globalAlpha=Math.min(.28,horror.flash*.35);ctx.fillStyle='#fff4dc';ctx.fillRect(0,0,W,H);}if(horror.glitch>0){ctx.globalAlpha=.12;for(let i=0;i<13;i++)px(0,Math.random()*H,W,2,i%2?'#c1ceca':'#293834');}if(state.sanity<42){ctx.globalAlpha=.07;ctx.fillStyle='#cfc7b2';ctx.fillRect(0,0,W,H);}ctx.restore();}
function drawPlayer(){const x=player.x-camera,y=player.y;const moving=player.onGround&&Math.abs(player.vx)>15;const run=inputState.run&&moving;const step=Math.sin(player.anim*(run?1.45:1.08));const bob=player.onGround?(moving?Math.abs(step)*2:Math.sin(totalTime*2)*.7):0;const colors={Julia:{coat:'#536f77',trim:'#8eaaa9',hair:'#3a292b',hi:'#76565a',scarf:'#e8e0cf'},May:{coat:'#606b84',trim:'#9aa5b9',hair:'#5a3c30',hi:'#95604c',scarf:'#e6dfd2'},Yumi:{coat:'#3a7a69',trim:'#79ad97',hair:'#1a1d21',hi:'#66767d',scarf:'#ece4d0'}};const q=colors[selectedCharacter]||colors.Julia;ctx.save();ctx.translate(x+19,y+43+bob);ctx.rotate(player.lean);const swing=moving?step*10:Math.sin(totalTime*2.1)*1.2;const jumpPose=!player.onGround;
 px(-14+swing,8,10,30,'#292f32');px(4-swing,8,10,30,'#292f32');px(-20+swing,35,21,7,'#171c1d');px(-1-swing,35,21,7,'#171c1d');
 px(-24,-8,48,40,q.coat);px(-30,-2,7,31,q.trim);px(23,-2,7,31,q.trim);px(-10,-17,20,8,q.scarf);px(-12,-41,25,29,'#d9ae94');px(-9,-35,19,20,'#f0c7a9');
 if(selectedCharacter==='Yumi'){px(-20,-51,40,12,q.hair);px(-23,-45,9,46,q.hair);px(19,-45,10,48,q.hair);px(-16,-57,29,7,q.hi);px(-25,-24,10,24,q.hair);px(19,-24,10,24,q.hair);px(-12,-44,4,3,q.hi);px(5,-44,4,3,q.hi);}else{px(-19,-50,38,12,q.hair);px(-22,-44,9,39,q.hair);px(18,-44,9,36,q.hair);px(-15,-56,28,6,q.hi);}
 px(-8,-29,3,3,'#201b18');px(6,-29,3,3,'#201b18');px(-2,-18,9,2,'#9d7466');
 const arm= moving?step*7:Math.sin(totalTime*2.1)*1.3;px(-29-arm,-4,9,28,q.coat);px(21+arm,-4,9,28,q.coat);px(-34-arm,18,9,9,'#d6aa91');px(27+arm,18,9,9,'#d6aa91');px(-6,-7,13,5,'#d7bb70');px(-2,-5,5,2,'#fff0a4');
 const gun=player.facing>0?28:-48;px(gun,-1,22,6,'#202a2c');px(player.facing>0?44:-44,2,8,3,'#68746f');if(player.recoil>0)px(player.facing>0?48:-60,-3,11,5,'#ffe08b');if(jumpPose){px(-20,42,13,5,'#6b736e');px(7,40,13,5,'#6b736e');}
 ctx.restore();}
function drawStairwell(){
 if(!interior||interior.floors<=1)return;
 const left=145,right=1245;
 for(const sx of [left,right]){
  const active=(Math.abs(player.x-sx)<120 && player.y>220 && player.y<550);
  px(sx-58,230,116,280,'#121819');
  px(sx-48,240,96,258,active?'#46504d':'#343d3b');
  for(let i=0;i<10;i++){
   const yy=465-i*21;
   px(sx-38+i*7,yy,76,8,'#7b8178');
   px(sx-38+i*7,yy+8,76,4,'#202625');
  }
  px(sx-48,490,96,5,'#111716');
  text('STAIRS',sx,520,9,active?'#e5d9bd':'#8f968e','center');
 }
}
function drawFlashlightCone(){
 if(scene!=='play'||!state.light)return;
 ctx.save();
 if(interior){
  const x=player.x,y=player.y-18;
  const dir=player.facing||1;
  const g=ctx.createRadialGradient(x+dir*40,y,8,x+dir*150,y,230);
  g.addColorStop(0,'rgba(238,231,201,.14)');
  g.addColorStop(.35,'rgba(218,214,190,.055)');
  g.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=g;
  ctx.beginPath();
  ctx.moveTo(x,y);ctx.lineTo(x+dir*270,y-120);ctx.lineTo(x+dir*270,y+120);ctx.closePath();ctx.fill();
 }else{
  const x=player.x-camera+18,y=player.y-38,dir=player.facing||1;
  const g=ctx.createLinearGradient(x,y,x+dir*260,y);
  g.addColorStop(0,'rgba(235,228,198,.08)');g.addColorStop(1,'rgba(235,228,198,0)');
  ctx.fillStyle=g;
  ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+dir*250,y-70);ctx.lineTo(x+dir*250,y+70);ctx.closePath();ctx.fill();
 }
 ctx.restore();
}
function drawWorldBase(){
 ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.shadowBlur=0;ctx.clearRect(0,0,W,H);if(horror.shake>0)ctx.translate((Math.random()-.5)*horror.shake,(Math.random()-.5)*horror.shake);
 if(!interior){drawTopDownExterior();drawTopDownThreats();drawTopDownPlayer();drawRainTopDown();}else{drawInterior();drawInteriorDecor();drawInteriorZombies();drawPlayerInterior();if(hiding){ctx.save();ctx.globalAlpha=.18;px(0,0,W,H,'#000');ctx.globalAlpha=1;text('HIDDEN',W/2,72,13,'#c8c1a9','center');text('STAY STILL',W/2,92,9,'#8d948c','center');ctx.restore();}}
 drawDreadPhantom();drawHorrorDirector();drawParticles();drawPixelDetailPass();extraAnimationPass();enhanceHorrorAtmosphere();if(interior)drawDynamicWeather();drawLighting();drawFlashlightCone();drawHorror();drawHudWorld();ctx.restore();
}
function drawTopDownExterior(){
 const maxX=WORLD[chapter], maxY=WORLD_HEIGHT[chapter];
 ctx.save();
 const sky=ctx.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#0a171d');sky.addColorStop(.48,'#173238');sky.addColorStop(1,'#0b181a');ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
 ctx.translate(-camera,-cameraY);
 // large island / coastal terrain
 const coast=ctx.createLinearGradient(0,0,0,maxY);coast.addColorStop(0,'#30483d');coast.addColorStop(.45,'#263f35');coast.addColorStop(1,'#1d332e');ctx.fillStyle=coast;
 ctx.beginPath();ctx.moveTo(500,1300);ctx.bezierCurveTo(8000,600,15000,900,21500,1500);ctx.bezierCurveTo(30000,650,41000,1300,50500,3200);ctx.bezierCurveTo(51500,9000,51000,16000,48500,23200);ctx.bezierCurveTo(39000,27000,27000,26300,17000,27200);ctx.bezierCurveTo(8000,27000,1900,24400,700,18200);ctx.closePath();ctx.fill();
 // water bands
 ctx.fillStyle='#102a34';ctx.fillRect(0,0,maxX,900);ctx.fillRect(0,maxY-850,maxX,850);ctx.fillStyle='rgba(74,125,133,.24)';
 for(let y=900;y<maxY;y+=420){ctx.beginPath();ctx.moveTo(0,y);for(let x=0;x<maxX;x+=520)ctx.quadraticCurveTo(x+130,y-22,x+260,y);ctx.strokeStyle='rgba(102,153,157,.13)';ctx.lineWidth=5;ctx.stroke();}
 // major road network: smooth, not pixel blocks
 const roadYs=[3600,6900,10300,13800,17300,20800,24200];
 ctx.lineCap='round';for(const y of roadYs){ctx.strokeStyle='#343c3a';ctx.lineWidth=190;ctx.beginPath();ctx.moveTo(900,y);ctx.lineTo(maxX-1300,y+(y%700)-300);ctx.stroke();ctx.strokeStyle='#62655b';ctx.lineWidth=7;ctx.setLineDash([90,70]);ctx.beginPath();ctx.moveTo(900,y);ctx.lineTo(maxX-1300,y+(y%700)-300);ctx.stroke();ctx.setLineDash([]);}
 const roadXs=[5200,11200,17800,24600,31400,38200,45000];
 for(const x of roadXs){ctx.strokeStyle='#303937';ctx.lineWidth=165;ctx.beginPath();ctx.moveTo(x,1500);ctx.lineTo(x+(x%500)-250,maxY-1400);ctx.stroke();ctx.strokeStyle='#595f57';ctx.lineWidth=6;ctx.setLineDash([80,75]);ctx.beginPath();ctx.moveTo(x,1500);ctx.lineTo(x+(x%500)-250,maxY-1400);ctx.stroke();ctx.setLineDash([]);}
 // parks / fields
 for(let i=0;i<26;i++){const x=1700+((i*1733)%47000),y=1700+((i*2471)%24500),r=180+(i%5)*70;ctx.fillStyle=i%2?'rgba(67,100,69,.38)':'rgba(83,108,67,.28)';ctx.beginPath();ctx.ellipse(x,y,r,r*.58,(i%7)*.18,0,Math.PI*2);ctx.fill();}
 drawTopDownLandmarks();drawTopDownProps();
 // subtle coordinate grid for exploration readability
 ctx.strokeStyle='rgba(170,186,171,.035)';ctx.lineWidth=1;for(let x=1000;x<maxX;x+=1000){ctx.beginPath();ctx.moveTo(x,900);ctx.lineTo(x,maxY-850);ctx.stroke();}for(let y=1500;y<maxY;y+=1000){ctx.beginPath();ctx.moveTo(600,y);ctx.lineTo(maxX-700,y);ctx.stroke();}
 ctx.restore();
 // navigation card
 ctx.save();ctx.fillStyle='rgba(4,8,9,.78)';roundRect(18,88,154,112,14);ctx.fill();strokeRoundRect(18,88,154,112,14,'rgba(184,195,177,.34)',1);
 text('N',95,109,13,'#e9e3cf','center');text('W',38,153,11,'#9da9a0','center');text('E',152,153,11,'#9da9a0','center');text('S',95,190,11,'#9da9a0','center');
 line(95,118,95,178,'#d6c99e',2);line(62,151,128,151,'#d6c99e',2);ctx.restore();
}
function roundRect(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r);}
function strokeRoundRect(x,y,w,h,r,c,l=1){ctx.strokeStyle=c;ctx.lineWidth=l;roundRect(x,y,w,h,r);ctx.stroke();}
function drawTopDownLandmarks(){for(const l of landmarkData){const x=l.x,y=l.y||4000;if(x<camera-900||x>camera+W+900||y<cameraY-700||y>cameraY+H+700)continue;const bw=clamp(l.w*.62,180,760),bh=clamp(l.h*.64,130,430),bx=x-bw/2,by=y-bh/2;
  // shadow and foundation
  ctx.fillStyle='rgba(0,0,0,.34)';roundRect(bx+20,by+24,bw,bh,16);ctx.fill();
  const g=ctx.createLinearGradient(bx,by,bx,by+bh);g.addColorStop(0,l.type==='medical'?'#82968f':l.type==='power'?'#68756f':l.type==='cellhouse'?'#727c79':'#7b847d');g.addColorStop(1,'#3e4946');ctx.fillStyle=g;roundRect(bx,by,bw,bh,12);ctx.fill();
  // roof
  ctx.fillStyle='#252e2d';roundRect(bx-10,by-12,bw+20,24,8);ctx.fill();
  // windows with glow
  const cols=Math.max(3,Math.floor(bw/68));for(let j=0;j<cols;j++){const wx=bx+24+j*((bw-48)/Math.max(1,cols-1));const lit=(j*7+Math.floor(y/300))%5===0;ctx.fillStyle=lit?'#d8b86c':'#1b2929';roundRect(wx-16,by+34,32,34,5);ctx.fill();if(lit){const gg=ctx.createRadialGradient(wx,by+51,2,wx,by+51,70);gg.addColorStop(0,'rgba(232,190,99,.20)');gg.addColorStop(1,'rgba(232,190,99,0)');ctx.fillStyle=gg;ctx.fillRect(wx-70,by-20,140,140);}}
  // doors / signs
  ctx.fillStyle='#202827';roundRect(x-25,by+bh-58,50,58,6);ctx.fill();ctx.fillStyle='#a9a28c';ctx.fillRect(x-2,by+bh-31,4,4);
  ctx.strokeStyle='rgba(220,225,209,.42)';ctx.lineWidth=2;roundRect(bx,by,bw,bh,12);ctx.stroke();
  text(l.name,x,by-22,12,'#eee8d8','center');
  if(Math.hypot(player.x-x,player.y-y)<900){text('ENTER',x,by+bh+24,9,'#b8c5b7','center');}
 }}
function drawTopDownProps(){
 // trees
 for(let i=0;i<420;i++){const x=900+((i*941)%50000),y=1500+((i*617)%25500);if(x<camera-100||x>camera+W+100||y<cameraY-100||y>cameraY+H+100)continue;const r=10+(i%8)*2;ctx.fillStyle='rgba(0,0,0,.22)';ctx.beginPath();ctx.ellipse(x+8,y+15,r*1.2,r*.55,0,0,Math.PI*2);ctx.fill();ctx.fillStyle=i%3?'#2f5b43':'#41684a';ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.fillStyle='#557b57';ctx.beginPath();ctx.arc(x-r*.25,y-r*.35,r*.58,0,Math.PI*2);ctx.fill();ctx.fillStyle='#344b38';ctx.fillRect(x-2,y+r*.55,4,14);}
 // cars / wrecks / crates
 for(let i=0;i<100;i++){const x=1200+((i*1377)%49000),y=1800+((i*877)%24500);if(x<camera-120||x>camera+W+120||y<cameraY-120||y>cameraY+H+120)continue;ctx.save();ctx.translate(x,y);ctx.rotate((i%6-3)*.12);ctx.fillStyle='rgba(0,0,0,.3)';roundRect(-38,12,76,28,8);ctx.fill();ctx.fillStyle=i%3?'#3f4b4a':'#5b4643';roundRect(-42,-12,84,32,7);ctx.fill();ctx.fillStyle='#182222';roundRect(-28,-22,56,17,5);ctx.fill();ctx.fillStyle='#8a8e82';ctx.beginPath();ctx.arc(-25,18,8,0,Math.PI*2);ctx.arc(25,18,8,0,Math.PI*2);ctx.fill();ctx.restore();}
}
function drawTopDownThreats(){for(const z of zombies){if(z.dead)continue;const x=z.x-camera,y=(z.y||4200)-cameraY;if(x<-100||x>W+100||y<-100||y>H+100)continue;const s=z.type==='warden'?1.55:z.type==='brute'?1.3:z.type==='runner'?1.05:1;ctx.save();ctx.translate(x,y);const a=Math.atan2(player.y-(z.y||4200),player.x-z.x);ctx.rotate(a+Math.PI/2);ctx.fillStyle='rgba(0,0,0,.38)';ctx.beginPath();ctx.ellipse(0,26,28*s,11*s,0,0,Math.PI*2);ctx.fill();const g=ctx.createLinearGradient(-18,-35,18,32);g.addColorStop(0,z.type==='warden'?'#111517':z.type==='brute'?'#674d50':z.type==='runner'?'#7c514c':'#56645f');g.addColorStop(1,'#202726');ctx.fillStyle=g;ctx.beginPath();ctx.roundRect(-18*s,-25*s,36*s,52*s,9*s);ctx.fill();ctx.fillStyle='#9b806e';ctx.beginPath();ctx.arc(0,-38*s,15*s,0,Math.PI*2);ctx.fill();ctx.fillStyle='#1b2020';ctx.beginPath();ctx.arc(0,-43*s,15*s,Math.PI,Math.PI*2);ctx.fill();ctx.fillStyle='#d96457';ctx.beginPath();ctx.arc(-6*s,-38*s,2.8*s,0,Math.PI*2);ctx.arc(6*s,-38*s,2.8*s,0,Math.PI*2);ctx.fill();ctx.strokeStyle='rgba(226,228,210,.25)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-19*s,-4*s);ctx.lineTo(-29*s,19*s);ctx.moveTo(19*s,-4*s);ctx.lineTo(29*s,19*s);ctx.stroke();ctx.restore();}}
function drawTopDownPlayer(){const x=player.x-camera,y=player.y-cameraY;ctx.save();ctx.translate(x,y);const bob=Math.sin(player.anim*8)*2;ctx.translate(0,bob);ctx.fillStyle='rgba(0,0,0,.42)';ctx.beginPath();ctx.ellipse(0,28,28,12,0,0,Math.PI*2);ctx.fill();const body=ctx.createLinearGradient(-20,-22,20,30);body.addColorStop(0,'#4f6c70');body.addColorStop(1,'#1d3032');ctx.fillStyle=body;ctx.beginPath();ctx.roundRect(-19,-22,38,50,10);ctx.fill();ctx.fillStyle='#bfae96';ctx.beginPath();ctx.arc(0,-38,15,0,Math.PI*2);ctx.fill();ctx.fillStyle='#202625';ctx.beginPath();ctx.arc(0,-43,16,Math.PI,Math.PI*2);ctx.fill();ctx.fillStyle='#657a78';ctx.beginPath();ctx.roundRect(-28,-14,9,27,5);ctx.roundRect(19,-14,9,27,5);ctx.fill();ctx.fillStyle='#151b1b';ctx.beginPath();ctx.roundRect(-15,27,11,10,4);ctx.roundRect(4,27,11,10,4);ctx.fill();ctx.strokeStyle='rgba(233,227,207,.35)';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(0,-38,16,0,Math.PI*2);ctx.stroke();if(state.light){const g=ctx.createRadialGradient(player.facing*90,0,8,player.facing*90,0,300);g.addColorStop(0,'rgba(255,244,198,.15)');g.addColorStop(1,'rgba(255,244,198,0)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(0,-5);ctx.lineTo(player.facing*280,-125);ctx.lineTo(player.facing*280,125);ctx.closePath();ctx.fill();}ctx.restore();}
function drawRainTopDown(){ctx.save();ctx.globalAlpha=.23;for(let i=0;i<150;i++){const x=(i*83+totalTime*430)%W,y=(i*47+totalTime*600)%H;line(x,y,x-7,y+17,'#91aeb4',1);}ctx.restore();}

function drawPlayerInterior(){
 const x=player.x,y=player.y;ctx.save();ctx.translate(x,y);const bob=Math.sin(player.anim*7)*1.5;ctx.translate(0,bob);
 px(-17,14,34,9,'#090b0b');px(-13,-16,26,31,'#293b3b');px(-10,-27,20,14,'#b5a58d');px(-9,-38,18,12,'#252b2a');px(-17,-5,7,20,'#354a49');px(10,-5,7,20,'#354a49');px(-13,25,10,7,'#121817');px(4,25,10,7,'#121817');
 const arm=Math.sin(player.anim*5)*4;px(-22,-2+arm,6,21,'#536361');px(16,-2-arm,6,21,'#536361');
 if(state.light){ctx.globalAlpha=.08;ctx.beginPath();ctx.moveTo(player.facing*5,-15);ctx.lineTo(player.facing*230,-95);ctx.lineTo(player.facing*230,95);ctx.closePath();ctx.fillStyle='#e8dfc0';ctx.fill();ctx.globalAlpha=1;}
 ctx.restore();
}
function drawHudWorld(){if(scene==='play'&&!interior){const near=landmarkData.reduce((a,b)=>Math.hypot(b.x-player.x,(b.y||4000)-player.y)<Math.hypot(a.x-player.x,(a.y||4000)-player.y)?b:a,landmarkData[0]);const d=Math.max(10,Math.round(Math.hypot(near.x-player.x,(near.y||4000)-player.y)/10)*10);const ang=Math.atan2((near.y||4000)-player.y,near.x-player.x);const dirs=['→','↘','↓','↙','←','↖','↑','↗'];const di=((Math.round(ang/(Math.PI/4))+8)%8);px(430,744,540,28,'rgba(4,7,7,.78)');text(`${dirs[di]} ${near.name} • ${d} m`,700,764,10,'#e8dfc9','center');}}
function renderMapStrip(){
 const strip=document.getElementById('mapStrip'),p=document.getElementById('mapPlayer'),pts=document.getElementById('mapPoints');
 if(!strip||!p||!pts)return;
 if(chapter!=='ALCATRAZ'){strip.style.display='none';return;}
 strip.style.display='block';
 const max=WORLD.ALCATRAZ-80;
 p.style.left=`calc(10px + ${clamp(player.x/max,0,1)*100}% - 4px)`;
 pts.innerHTML='';
 const marks=[900,3800,6200,8550,10020,11550,14850,17150,18300,20700,21700];
 marks.forEach((x,i)=>{
  const d=document.createElement('i');d.className=(state.finalChase&&x>player.x?'mapDanger':'mapPoint');
  d.style.position='absolute';d.style.left=`calc(10px + ${x/max*100}% - 2px)`;d.title=String(i+1);pts.appendChild(d);
 });
}

function renderHUDBase(){renderMapStrip();const hp=document.getElementById('healthFill'),st=document.getElementById('staminaFill'),sa=document.getElementById('sanityFill');if(hp)hp.style.width=`${clamp(state.health/state.maxHealth*100,0,100)}%`;if(st)st.style.width=`${state.stamina}%`;if(sa)sa.style.width=`${state.sanity}%`;const hv=document.getElementById('healthValue'),sv=document.getElementById('staminaValue'),sav=document.getElementById('sanityValue'),am=document.getElementById('ammoText'),loc=document.getElementById('locationText'),th=document.getElementById('threatText');if(hv)hv.textContent=`${Math.ceil(state.health)}/${state.maxHealth}`;if(sv)sv.textContent=`${Math.ceil(state.stamina)}/100`;if(sav)sav.textContent=`${Math.ceil(state.sanity)}/100`;if(am)am.textContent=`AMMO ${state.ammo} / ${state.reserveAmmo}  •  EVIDENCE ${crime.evidence}/5  •  BAT ${Math.ceil(state.battery)}%`;if(loc)loc.textContent=chapter==='ALCATRAZ'?(interior?`${interior.name} • FLOOR ${interior.floor||1}/${interior.floors||1}`:'ALCATRAZ ISLAND'):'SAN FRANCISCO';if(th)th.textContent=crime.heat>75?'POLICE + KILLER ARE HUNTING YOU':crime.caseSolved?'CASE SOLVED — EXTRACT NOW':crime.heat>45?'WANTED — DO NOT GET SPOTTED':state.health<28?'CRITICAL — BLEEDING':state.sanity<35?'YOU ARE LOSING YOUR MIND':state.sanity<55?'SOMEONE IS WATCHING':'CRIME SCENE ACTIVE';}
function drawPrompt(){const e=document.getElementById('prompt');if(!e)return;if(scene!=='play'){e.textContent='';return;}let t='';if(interior){if(interior.topDown){if(interior.id==='cellA17'){if(!state.startKey&&Math.hypot(player.x-310,player.y-390)<100)t='E  /  USE  — SEARCH MATTRESS';else if(state.startKey&&Math.hypot(player.x-1240,player.y-390)<115)t='E  /  USE  — UNLOCK CELL DOOR';}if(nearestHideSpot())t=hiding?'E  /  USE — LEAVE COVER':'E  /  USE — HIDE';if((Math.abs(player.x-145)<100||Math.abs(player.x-1245)<100)&&player.y>250&&player.y<520)t=`E  /  USE  — STAIRWELL • FLOOR ${interior.floor}/${interior.floors}`;if(player.x<70||player.x>1330)t='E  /  USE  — EXIT STRUCTURE';const c=nearestChest();if(c)t=`E  /  USE  — SEARCH ${c.building}`;}else if(player.x<170||player.x>1010)t='E  /  USE  — EXIT TO STREET';else{const c=nearestChest();if(c)t='E  /  USE  — OPEN CHEST';}}else if(chapter==='ALCATRAZ'){const b=nearestBuilding();if(b)t=`E  /  USE  — ENTER ${b.name}`;else if(Math.abs(player.x-16040)<260)t=state.dockPass?(state.beacon?'E  /  USE  — BOARD FERRY':'E  /  USE  — LIGHT FERRY BEACON'):'DOCK PASS REQUIRED';}else{let got=false;for(const s of survivors){if(!s.found&&Math.abs(player.x-s.x)<125){t=`E  /  USE  — TALK TO ${s.name}`;got=true;break;}}if(!got){const b=nearestBuilding();if(b)t=`E  /  USE  — ENTER ${b.name}`;else if(state.survivors>=2&&Math.abs(player.x-3200)<420)t='E  /  USE  — ENTER EMERGENCY SHELTER';}}e.textContent=t;}

function updateCamera(){if(interior){camera=0;cameraY=0;return;}const maxX=Math.max(0,WORLD[chapter]-W),maxY=Math.max(0,WORLD_HEIGHT[chapter]-H);const tx=clamp(player.x-W*.5,0,maxX),ty=clamp(player.y-H*.5,0,maxY);camera=lerp(camera,tx,1-Math.exp(-7*.016));cameraY=lerp(cameraY,ty,1-Math.exp(-7*.016));}
function tick(now){const dt=Math.min(.032,Math.max(.001,(now-last)/1000));last=now;updateInput();updateWorld(dt);updateCamera();drawWorld();drawPrompt();requestAnimationFrame(tick);}
function keyDown(e){const k=e.key;if(['ArrowLeft','ArrowRight','ArrowUp',' ','a','A','d','D','w','W','Shift','e','E','q','Q','f','F','r','R','i','I','Tab','Escape','Enter'].includes(k))e.preventDefault();keys.add(k);if(scene==='intro'&&(k==='Enter'||k===' '||k==='ArrowRight')){advanceIntro();return;}if(scene==='menu'&&(k==='Enter'||k===' ')){showOnly('characterMenu');scene='character';return;}if(scene==='play'){if(k==='e'||k==='E')useInteract();else if(k==='q'||k==='Q')melee();else if(k==='f'||k==='F'){state.light=!state.light;soundFlicker();}else if(k==='r'||k==='R')reload();else if(k==='i'||k==='I'){scene='inventory';show('inventoryUi');}else if(k==='Escape')togglePause();else if(k==='Tab'){objectivePanelOpen=!objectivePanelOpen;document.getElementById('objectivePanel').classList.toggle('open',objectivePanelOpen);}else if(k==='p'||k==='P'){show('deviceOverlay');renderDeviceInfo();}else if(k==='g'||k==='G'){if(state.grenades>0){state.grenades--;tone(75,.18,'square',.16);setMessage('GRENADE THROWN.',.8);horror.shake=5;}}}}
function keyUp(e){keys.delete(e.key);if(e.key===' ')touch.jump=false;}
function onMove(e){const r=canvas.getBoundingClientRect();mouse.x=(e.clientX-r.left)*W/r.width;mouse.y=(e.clientY-r.top)*H/r.height;cursorMoved=true;lastCursorMove=totalTime;}
function onPointerDown(e){onMove(e);mouse.down=true;if(scene==='play'){safeAudio();shoot();}}
function onPointerUp(){mouse.down=false;}
function updateMouseFire(dt){if(mouse.down&&controlMode==='laptop'&&scene==='play'){if(!updateMouseFire.timer||totalTime-updateMouseFire.timer>.22){updateMouseFire.timer=totalTime;shoot();}}}
function togglePause(){if(scene==='play'){scene='pause';show('pause');}else if(scene==='pause')resumeGame();}
function resumeGame(){scene='play';hide('pause');safeAudio();}
function restartChapter(){hide('pause');hide('death');hide('ending');resetWorld();positionInsideCell();scene='intro';introIndex=0;introTimer=0;show('cutscene');updateIntroText();startSoundscape();}
function mainMenu(){hide('pause');hide('death');hide('ending');hide('cutscene');showOnly('mainMenu');scene='menu';}
function saveControlMode(){try{sessionStorage.setItem('aotd_control',controlMode);}catch(e){}}
function loadControlMode(){try{const v=sessionStorage.getItem('aotd_control');if(v)setControlMode(v);else setControlMode('auto');}catch(e){setControlMode('auto');}}
function setControlMode(v){if(v==='auto')v=/Android|iPhone|iPad|iPod|Mobi/i.test(navigator.userAgent)?'mobile':'laptop';controlMode=v==='mobile'?'mobile':'laptop';updateControlUI();saveControlMode();}
function updateControlUI(){document.querySelectorAll('[data-control]').forEach(b=>b.classList.toggle('selected',b.dataset.control===controlMode));const e=document.getElementById('controlStatus');if(e)e.textContent=`ACTIVE: ${controlMode==='mobile'?'MOBILE / TOUCH':'LAPTOP / DESKTOP'}`;const m=document.getElementById('mobileControls');if(m)m.classList.toggle('hidden',controlMode!=='mobile');}
function renderDeviceInfo(){const g=document.getElementById('deviceGrid');if(!g)return;g.innerHTML='';const n=navigator,c=n.connection||n.mozConnection||n.webkitConnection;const rows=[['SERVER-SEEN IP','Loading...'],['PLATFORM',n.platform||'Unavailable'],['BROWSER',n.userAgent||'Unavailable'],['SCREEN',`${screen.width} × ${screen.height}`],['LANGUAGE',n.language||'Unavailable'],['TIMEZONE',Intl.DateTimeFormat().resolvedOptions().timeZone||'Unavailable'],['CPU THREADS',n.hardwareConcurrency||'Unavailable'],['NETWORK',c?(c.effectiveType||c.type):'Unavailable'],['ONLINE',n.onLine?'ONLINE':'OFFLINE'],['TOUCH POINTS',n.maxTouchPoints||0],['COOKIES',n.cookieEnabled?'ENABLED':'DISABLED'],['REFERRER',document.referrer||'Direct / none']];rows.forEach(r=>{const d=document.createElement('div');d.className='deviceCard';d.innerHTML=`<b>${r[0]}</b><span>${String(r[1]).replace(/</g,'&lt;')}</span>`;g.appendChild(d);});fetch('/gadget',{cache:'no-store'}).then(r=>r.json()).then(d=>{if(g.firstChild)g.firstChild.querySelector('span').textContent=d.server_seen_ip||'Unavailable';}).catch(()=>{});}
function setupInterface(){
 const bind=(id,fn)=>{const e=document.getElementById(id);if(e)e.onclick=ev=>{ev.preventDefault();ev.stopPropagation();safeAudio();fn();};};
 bind('privacyEnter',()=>{hide('privacyGate');showOnly('mainMenu');scene='menu';safeAudio();});
 bind('privacyDevice',()=>{hide('privacyGate');show('deviceOverlay');renderDeviceInfo();});
 bind('privacyGate',()=>{});
 bind('playButton',()=>{showOnly('characterMenu');scene='character';});
 bind('creditsButton',()=>{showOnly('credits');scene='credits';});
 bind('controlsButton',()=>{showOnly('controlsOverlay');scene='controls';updateControlUI();});
 bind('creditsBack',()=>{showOnly('mainMenu');scene='menu';});
 bind('characterBack',()=>{showOnly('mainMenu');scene='menu';});
 bind('characterControls',()=>{showOnly('controlsOverlay');scene='controls';updateControlUI();});
 bind('controlsBack',()=>{showOnly('mainMenu');scene='menu';});
 bind('autoMode',()=>setControlMode('auto'));
 bind('objectiveTab',()=>{objectivePanelOpen=!objectivePanelOpen;document.getElementById('objectivePanel').classList.toggle('open',objectivePanelOpen);});
 bind('objectiveClose',()=>{objectivePanelOpen=false;document.getElementById('objectivePanel').classList.remove('open');});
 bind('soundButton',()=>{soundEnabled=!soundEnabled;document.getElementById('soundButton').textContent=`SOUND: ${soundEnabled?'ON':'OFF'}`;if(soundEnabled)startSoundscape();});
 bind('resumeButton',resumeGame);bind('restartButton',restartChapter);bind('pauseMenuButton',mainMenu);bind('endingMenuButton',mainMenu);bind('deathRestartButton',restartChapter);bind('deathMenuButton',mainMenu);bind('infoClose',()=>hide('deviceOverlay'));bind('chestCloseButton',closeChest);bind('takeAllButton',takeAll);bind('sortButton',sortChest);
 document.querySelectorAll('[data-character]').forEach(b=>b.onclick=e=>{e.preventDefault();e.stopPropagation();safeAudio();beginGame(b.dataset.character);});
 document.querySelectorAll('[data-control]').forEach(b=>b.onclick=e=>{e.preventDefault();e.stopPropagation();safeAudio();setControlMode(b.dataset.control);});
 document.querySelectorAll('[data-touch]').forEach(b=>{const a=b.dataset.touch;b.onpointerdown=e=>{e.preventDefault();e.stopPropagation();safeAudio();touch[a]=true;if(a==='jump')tryJump();if(a==='interact')useInteract();if(a==='melee')melee();if(a==='fire')shoot();if(a==='light'){state.light=!state.light;soundFlicker();}if(a==='inventory'){scene='inventory';show('inventoryUi');}if(a==='reload')reload();};b.onpointerup=e=>{e.preventDefault();touch[a]=false;};b.onpointercancel=()=>touch[a]=false;});
 window.addEventListener('keydown',keyDown,{passive:false});window.addEventListener('keyup',keyUp,{passive:false});canvas.addEventListener('pointermove',onMove);canvas.addEventListener('pointerdown',onPointerDown);window.addEventListener('pointerup',onPointerUp);window.addEventListener('blur',()=>{keys.clear();Object.keys(touch).forEach(k=>touch[k]=false);});document.addEventListener('visibilitychange',()=>{tabAway=document.hidden;});loadControlMode();updateControlUI();
 window.addEventListener('resize',()=>{});
}
setInterval(()=>updateMouseFire(.016),40);
function boot(){try{setupInterface();resetWorld();positionInsideCell();scene='menu';drawWorld();renderHUD();show('privacyGate');requestAnimationFrame(tick);}catch(err){const e=document.getElementById('warningText');if(e){e.textContent='BOOT ERROR: '+err.message;e.style.opacity='1';}show('privacyGate');}}

/* ================= NIGHTFALL 2.0 GAMEPLAY / VISUAL DIRECTOR ================= */
const NF={
 fear:0, noise:0, pulse:0, event:null, eventTimer:24, eventCooldown:9, eventSeed:0,
 hunter:null, hunterTimer:0, bloodTrail:[], sparks:[], fog:[], objective:'SURVIVE',
 introShown:false, lastMilestone:0, cameraBob:0
};
for(let i=0;i<42;i++) NF.fog.push({x:Math.random()*W,y:360+Math.random()*260,s:18+Math.random()*55,a:.015+Math.random()*.035,sp:4+Math.random()*10});
function nfClamp(v,a,b){return Math.max(a,Math.min(b,v));}
function nfEventName(){return ['THE HUNT','POWER FAILURE','LOCKDOWN','SILENT HOUSE','BLOOD TRAIL','THE WHISTLE'][Math.floor(Math.random()*6)];}
function nfStartEvent(){
 if(scene!=='play'||NF.eventCooldown>0)return;
 const inside=!!interior, e=nfEventName(); NF.event=e; NF.eventTimer=inside?15+Math.random()*15:18+Math.random()*22; NF.eventCooldown=30+Math.random()*28; NF.eventSeed++;
 if(e==='THE HUNT'){
   horrorDirector.noise=100; state.sanity=Math.max(0,state.sanity-4); showWarning('THE HUNT HAS STARTED — KEEP MOVING.',2.1); soundScare();
   const side=Math.random()<.5?-1:1; NF.hunter={x:clamp(player.x+side*(inside?480:900),70,(inside?1330:WORLD[chapter]-70)),y:inside?clamp(player.y+(Math.random()-.5)*260,110,650):GROUND-55,hp:280,phase:0};
 } else if(e==='POWER FAILURE'){
   state.light=false; horror.blackout=2.5; state.battery=Math.max(0,state.battery-10); showWarning('TOTAL BLACKOUT. FIND A LIGHT SOURCE.',2.1); soundFlicker();
 } else if(e==='LOCKDOWN'){
   state.alarm=true; horrorDirector.lockdown=NF.eventTimer; showWarning('LOCKDOWN — THE EXITS ARE NOT SAFE.',2.1); tone(48,.8,'square',.16,-25);
   for(let i=0;i<(inside?3:5);i++){const side=i%2?-1:1;if(inside)interiorZombies.push({x:side<0?65:1335,y:120+Math.random()*510,hp:130,maxHp:130,type:i%2?'runner':'stalker',attack:.3,phase:Math.random()*6,dead:false,deathTimer:0,hit:0,alert:1});}
 } else if(e==='SILENT HOUSE'){
   NF.objective='DO NOT MAKE NOISE'; state.sanity=Math.max(0,state.sanity-2); showWarning('SILENT HOUSE — RUNNING WILL DRAW SOMETHING.',2.2); horror.glitch=.4;
 } else if(e==='BLOOD TRAIL'){
   NF.objective='FOLLOW THE BLOOD'; state.sanity=Math.max(0,state.sanity-2); showWarning('A FRESH BLOOD TRAIL LEADS DEEPER.',2.2); soundWhisper();
   for(let i=0;i<12;i++)NF.bloodTrail.push({x:player.x+(i+1)*70,y:inside?player.y+(Math.random()-.5)*120:GROUND-4,life:22});
 } else {
   NF.objective='FIND THE SOURCE'; showWarning('A WHISTLE CAME FROM SOMEWHERE NEARBY.',2.2); soundWhisper();
   NF.hunter={x:clamp(player.x+(Math.random()<.5?-1:1)*650,70,(inside?1330:WORLD[chapter]-70)),y:inside?player.y:GROUND-55,hp:190,phase:0};
 }
}
function nfUpdateEvent(dt){
 if(scene!=='play')return;
 NF.eventCooldown=Math.max(0,NF.eventCooldown-dt); NF.eventTimer-=dt; NF.noise=Math.max(0,NF.noise-dt*7);
 const movementNoise=Math.hypot(player.vx,player.vy); if(movementNoise>80)NF.noise+=dt*(inputState.run?18:5); if(horrorDirector.noise>65)NF.noise+=dt*2;
 NF.fear=nfClamp((100-state.health)/100*.35+(100-state.sanity)/100*.45+threatLevel/220+(state.alarm?.18:0)+(state.finalChase?.28:0),0,1.35);
 if(!NF.event && NF.eventCooldown<=0 && (NF.noise>72 || Math.random()<dt*(.006+NF.fear*.012)))nfStartEvent();
 if(NF.event && NF.eventTimer<=0){if(NF.event==='POWER FAILURE'&&state.health>0)state.light=true;NF.event=null;NF.objective='SURVIVE';}
 if(NF.hunter){
   const h=NF.hunter; h.phase+=dt; const dx=player.x-h.x,dy=interior?player.y-h.y:0,d=Math.hypot(dx,dy);
   const speed=interior?72:62;
   if(d>55){h.x+=Math.sign(dx)*speed*dt+Math.sin(h.phase*2.1)*18*dt;if(interior)h.y+=Math.sign(dy)*speed*.62*dt;}
   if(d<95&&Math.random()<dt*.7){damagePlayer(24);horror.shake=14;showWarning('THE HUNTER FOUND YOU.',.8);}
   if(h.hp<=0||d>1450){if(h.hp<=0)showWarning('IT LEFT A BODY. BUT NOT AN ANSWER.',1);NF.hunter=null;}
 }
 for(const b of NF.bloodTrail)b.life-=dt; NF.bloodTrail=NF.bloodTrail.filter(b=>b.life>0);
}
function nfDrawDepth(){
 if(scene!=='play')return;
 ctx.save();
 // Deep atmospheric haze and moving volumetric bands.
 if(!interior){
   const g=ctx.createLinearGradient(0,330,0,H);g.addColorStop(0,'rgba(100,130,132,.015)');g.addColorStop(.58,'rgba(40,55,56,.035)');g.addColorStop(1,'rgba(0,0,0,.16)');ctx.fillStyle=g;ctx.fillRect(0,300,W,H-300);
   for(const f of NF.fog){const x=((f.x-totalTime*f.sp-camera*.06)% (W+160)+W+160)%(W+160)-80;ctx.globalAlpha=f.a*(.5+.5*Math.sin(totalTime*.4+f.x));ctx.fillStyle='#9eaaa2';ctx.beginPath();ctx.ellipse(x,f.y,f.s,3+f.s*.08,0,0,Math.PI*2);ctx.fill();}
   ctx.globalAlpha=.22;for(let i=0;i<7;i++){const x=((i*257-camera*.18)%W+W)%W;line(x,430,x+90,420,'#9aaba5',1);}ctx.globalAlpha=1;
 }
 // Cinematic letterbox at the edges, keeping the playable center clear.
 ctx.fillStyle='rgba(0,0,0,.18)';ctx.fillRect(0,0,W,22);ctx.fillRect(0,H-20,W,20);
 // Event indicator.
 if(NF.event){ctx.globalAlpha=.88;text(`EVENT // ${NF.event}`,W/2,36,11,'#d6c8a4','center');ctx.globalAlpha=1;}
 // Hunter silhouette with readable eyes.
 if(NF.hunter){const h=NF.hunter;const x=h.x-(interior?0:camera),y=interior?h.y:GROUND-55;const d=Math.hypot(player.x-h.x,interior?player.y-h.y:0);const a=nfClamp(1-d/1000,.08,.72);ctx.globalAlpha=a;px(x-18,y-58,36,58,'#050708');px(x-13,y-80,26,25,'#020303');px(x-10,y-70,5,3,'#d6caa4');px(x+5,y-70,5,3,'#d6caa4');ctx.globalAlpha=a*.45;line(x-27,y-25,x-45,y+18,'#0b0e0e',7);line(x+27,y-25,x+45,y+18,'#0b0e0e',7);ctx.globalAlpha=1;}
 for(const b of NF.bloodTrail){const x=b.x-(interior?0:camera);if(x>-10&&x<W+10){ctx.globalAlpha=nfClamp(b.life/8,0,.55);px(x,b.y,7,3,'#5f2d2c');px(x+8,b.y+2,3,2,'#35191a');}}ctx.globalAlpha=1;
 ctx.restore();
}
function nfDrawVignette(){
 if(scene!=='play')return;ctx.save();
 const fear=nfClamp(NF.fear,0,1);const g=ctx.createRadialGradient(W/2,H*.5,Math.min(W,H)*.18,W/2,H*.5,Math.max(W,H)*.72);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(.55,`rgba(0,0,0,${.035+fear*.05})`);g.addColorStop(1,`rgba(0,0,0,${.38+fear*.28})`);ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 if(fear>.72){ctx.globalAlpha=.035+(.18*Math.sin(totalTime*7)**2);ctx.fillStyle='#b66c61';ctx.fillRect(0,0,W,H);}
 ctx.restore();
}
function nfDrawCrosshair(){
 if(scene!=='play')return;ctx.save();const x=mouse.x,y=mouse.y;const near=interior?interiorZombies.some(z=>!z.dead&&Math.hypot(z.x-player.x,z.y-player.y)<120):zombies.some(z=>!z.dead&&Math.abs(z.x-player.x)<120);ctx.globalAlpha=.72;ctx.strokeStyle=near?'#d88972':'#d7d7c8';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x-8,y);ctx.lineTo(x-2,y);ctx.moveTo(x+2,y);ctx.lineTo(x+8,y);ctx.moveTo(x,y-8);ctx.lineTo(x,y-2);ctx.moveTo(x,y+2);ctx.lineTo(x,y+8);ctx.stroke();ctx.restore();
}
function cinSky(){
 const sf=chapter==='SAN FRANCISCO';
 const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,sf?'#050a12':'#04090d');g.addColorStop(.48,sf?'#12222b':'#10232b');g.addColorStop(.72,sf?'#293b3e':'#233b3d');g.addColorStop(1,'#0b1112');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 const mx=1060,my=105;const mg=ctx.createRadialGradient(mx,my,4,mx,my,180);mg.addColorStop(0,'rgba(235,231,210,.25)');mg.addColorStop(1,'rgba(235,231,210,0)');ctx.fillStyle=mg;ctx.fillRect(mx-180,my-180,360,360);ctx.fillStyle='#d9d4be';ctx.globalAlpha=.82;ctx.beginPath();ctx.arc(mx,my,34,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
 for(let i=0;i<120;i++){const x=(i*137)%W,y=18+(i*47)%300;ctx.fillStyle=`rgba(205,216,212,${.12+(i%5)*.035})`;ctx.fillRect(x,y,1,1);}
 for(let l=0;l<5;l++){const par=camera*(.025+l*.025);ctx.fillStyle=`rgba(${18+l*5},${35+l*5},${39+l*5},${.75-l*.08})`;ctx.beginPath();ctx.moveTo(-50,435);for(let i=-1;i<13;i++){const x=i*150-(par%150);const y=390-((i*43+l*67)%95);ctx.lineTo(x,y);ctx.lineTo(x+95,y+((i+l)%3)*18);}ctx.lineTo(W+50,435);ctx.closePath();ctx.fill();}
}
function cinGround(){
 const g=ctx.createLinearGradient(0,430,0,H);g.addColorStop(0,'#465451');g.addColorStop(.16,'#343f3e');g.addColorStop(.17,'#252f2f');g.addColorStop(1,'#151c1d');ctx.fillStyle=g;ctx.fillRect(0,430,W,H-430);
 ctx.fillStyle='#303938';ctx.fillRect(0,548,W,240);ctx.fillStyle='#1d2525';ctx.fillRect(0,552,W,4);
 for(let i=0;i<70;i++){const x=((i*173-camera*.65)%W+W)%W,y=448+(i*71)%300;ctx.fillStyle=i%7===0?'rgba(146,154,145,.28)':'rgba(10,14,14,.22)';ctx.beginPath();ctx.ellipse(x,y,2+(i%4),1+(i%3),0,0,Math.PI*2);ctx.fill();}
 for(let i=0;i<12;i++){const x=((i*260-camera*.4)%W+W)%W;ctx.fillStyle='rgba(120,140,135,.055)';ctx.beginPath();ctx.ellipse(x,535,80,10,0,0,Math.PI*2);ctx.fill();}
}
function cinBuilding(x,w,h,name,type){const left=x-w/2,top=GROUND-h;const body=ctx.createLinearGradient(0,top,0,GROUND);body.addColorStop(0,type==='cell'?'#596568':'#526062');body.addColorStop(.55,'#394648');body.addColorStop(1,'#202a2b');ctx.fillStyle=body;ctx.fillRect(left,top,w,h);ctx.fillStyle='rgba(220,225,211,.18)';ctx.fillRect(left,top,w,5);ctx.fillStyle='rgba(0,0,0,.32)';ctx.fillRect(left,top+h-16,w,16);
 const cols=Math.max(4,Math.floor(w/62)),rows=Math.max(2,Math.floor(h/68));for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const wx=left+24+c*(w-48)/(cols-1)-16,wy=top+32+r*58;const lit=((c*7+r*3+Math.floor(x/500))%9===0);ctx.fillStyle=lit?'#a9905b':'#172123';ctx.fillRect(wx,wy,32,25);ctx.fillStyle=lit?'rgba(255,210,128,.28)':'rgba(95,115,116,.18)';ctx.fillRect(wx+4,wy+4,24,17);}
 ctx.fillStyle='#12191a';ctx.fillRect(x-36,GROUND-86,72,86);ctx.fillStyle='#425051';ctx.fillRect(x-29,GROUND-79,58,72);ctx.fillStyle='#b6a36e';ctx.beginPath();ctx.arc(x+21,GROUND-42,3,0,Math.PI*2);ctx.fill();
 ctx.font='600 11px Consolas';ctx.textAlign='center';ctx.fillStyle='#d7d2c0';ctx.fillText(name,x,top-13);}
function cinWorldLandmarks(){
 if(chapter==='ALCATRAZ'){const ls=[{x:1200,w:820,h:250,n:'CELLHOUSE',t:'cell'},{x:3800,w:600,h:190,n:'RECREATION YARD',t:'yard'},{x:6200,w:650,h:210,n:'DINING HALL',t:'hall'},{x:8500,w:560,h:225,n:'HOSPITAL WING',t:'medical'},{x:10800,w:620,h:250,n:'MODEL INDUSTRIES',t:'industry'},{x:13200,w:520,h:290,n:'POWER PLANT',t:'power'},{x:15800,w:440,h:340,n:'WATER TOWER',t:'tower'},{x:18100,w:520,h:250,n:'WARDEN HOUSE',t:'house'},{x:23800,w:760,h:300,n:'NORTH BATTERY',t:'citadel'},{x:25200,w:920,h:210,n:'OLD QUARRY',t:'industry'},{x:26800,w:560,h:260,n:'SIGNAL STATION',t:'tower'},{x:28300,w:720,h:240,n:'EAST BOATHOUSE',t:'store'},{x:30000,w:620,h:200,n:'CLIFF TUNNEL',t:'tunnel'},{x:31800,w:780,h:280,n:'ABANDONED WARD',t:'medical'},{x:33900,w:520,h:190,n:'BLACKWATER DOCK',t:'dock' }];for(const b of ls){const x=b.x-camera;if(x>-b.w&&x<W+b.w)cinBuilding(x,b.w,b.h,b.n,b.t);}
  const dx=21700-camera;ctx.fillStyle='#354242';ctx.fillRect(dx-180,GROUND-20,360,20);ctx.fillStyle='#68746f';for(let i=0;i<7;i++)ctx.fillRect(dx-150+i*48,GROUND-27,30,7);ctx.fillStyle='#263333';ctx.fillRect(dx-38,GROUND-160,76,140);ctx.fillStyle='#73786f';ctx.fillRect(dx-48,GROUND-173,96,13);ctx.fillStyle=state.beacon?'#e8c879':'#65583f';ctx.beginPath();ctx.arc(dx,GROUND-194,15,0,Math.PI*2);ctx.fill();glow(dx,GROUND-194,110,state.beacon?'rgba(236,205,121,.22)':'rgba(0,0,0,0)','rgba(0,0,0,0)');
 } else {const ls=[{x:850,w:580,h:250,n:'OLD POLICE STATION',t:'police'},{x:2700,w:520,h:280,n:'HOSPITAL',t:'medical'},{x:4700,w:510,h:240,n:'FUNERAL HOME',t:'funeral'},{x:6500,w:620,h:330,n:'OLD HOTEL',t:'hotel'},{x:8600,w:580,h:260,n:'EMERGENCY SHELTER',t:'shelter'},{x:9900,w:620,h:310,n:'RESEARCH ANNEX',t:'research'}];for(const b of ls){const x=b.x-camera;if(x>-b.w&&x<W+b.w)cinBuilding(x,b.w,b.h,b.n,b.t);}}
}
function cinZombie(z){const x=z.x-camera;if(x<-80||x>W+80)return;const ground=GROUND;const scale=z.type==='warden'?1.25:z.type==='brute'?1.12:z.type==='runner'?1.03:1;const bob=Math.sin(totalTime*(z.type==='runner'?9:4)+z.phase)*2;ctx.save();ctx.translate(x,ground+bob);ctx.scale(scale,scale);const shadow=ctx.createRadialGradient(0,0,4,0,0,35);shadow.addColorStop(0,'rgba(0,0,0,.5)');shadow.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=shadow;ctx.beginPath();ctx.ellipse(0,0,38,10,0,0,Math.PI*2);ctx.fill();
 const coat=z.type==='warden'?'#121718':z.type==='brute'?'#554346':'#344241';ctx.fillStyle=coat;ctx.beginPath();ctx.roundRect(-17,-62,34,58,8);ctx.fill();ctx.fillStyle='#0d1213';ctx.beginPath();ctx.ellipse(0,-76,17,18,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#6f5d55';ctx.beginPath();ctx.ellipse(0,-75,13,14,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#d66b5d';ctx.beginPath();ctx.arc(-5,-77,2.5,0,Math.PI*2);ctx.arc(6,-77,2.5,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#261c1d';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,-71,7,.15,Math.PI-.15);ctx.stroke();ctx.strokeStyle='#1a2221';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(-13,-47);ctx.lineTo(-28,-17);ctx.moveTo(13,-47);ctx.lineTo(28,-17);ctx.moveTo(-8,-5);ctx.lineTo(-13,25);ctx.moveTo(8,-5);ctx.lineTo(13,25);ctx.stroke();if(z.type==='warden'){ctx.strokeStyle='#705e54';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(-22,-42);ctx.lineTo(22,-42);ctx.stroke();ctx.fillStyle='#d3b46b';ctx.fillRect(-20,-100,40,5);}if(z.hit>0){ctx.fillStyle='rgba(255,245,220,.35)';ctx.beginPath();ctx.arc(0,-55,35,0,Math.PI*2);ctx.fill();}ctx.restore();
}
function cinPlayer(){const x=player.x-camera,y=GROUND;const moving=Math.abs(player.vx)>15;const step=Math.sin(player.anim*(inputState.run?1.5:1.1));const bob=player.onGround?(moving?Math.abs(step)*2:0):0;ctx.save();ctx.translate(x+19,y-36+bob);ctx.scale(player.facing||1,1);const sh=ctx.createRadialGradient(0,34,3,0,34,38);sh.addColorStop(0,'rgba(0,0,0,.5)');sh.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=sh;ctx.beginPath();ctx.ellipse(0,34,34,9,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#182322';ctx.lineWidth=10;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-8,13);ctx.lineTo(-11,38);ctx.moveTo(8,13);ctx.lineTo(11,38);ctx.stroke();ctx.fillStyle=selectedCharacter==='Yumi'?'#2d7567':selectedCharacter==='May'?'#4e5d79':'#496873';ctx.beginPath();ctx.roundRect(-17,-30,34,48,9);ctx.fill();ctx.fillStyle='#c0a48e';ctx.beginPath();ctx.arc(0,-43,15,0,Math.PI*2);ctx.fill();ctx.fillStyle=selectedCharacter==='Yumi'?'#161b1d':selectedCharacter==='May'?'#4a3028':'#332527';ctx.beginPath();ctx.arc(0,-47,15,Math.PI,Math.PI*2);ctx.fill();ctx.strokeStyle='#536968';ctx.lineWidth=7;ctx.beginPath();ctx.moveTo(-14,-12);ctx.lineTo(-28,5);ctx.moveTo(14,-12);ctx.lineTo(29,2);ctx.stroke();ctx.fillStyle='#d6d0bd';ctx.fillRect(17,-1,26,4);if(!player.onGround){ctx.rotate(-.08*player.vy/180);}ctx.restore();}
function cinInterior(){
 const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#11191b');g.addColorStop(.42,'#293535');g.addColorStop(1,'#0d1213');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.fillStyle='#1b2425';ctx.fillRect(0,0,W,70);ctx.fillStyle='#171f20';ctx.fillRect(0,690,W,98);
 for(let i=0;i<8;i++){const x=i*190+35;ctx.fillStyle='rgba(210,202,168,.12)';ctx.fillRect(x,78,120,3);glow(x+60,90,95,'rgba(231,214,169,.07)','rgba(0,0,0,0)');}
 for(let i=0;i<12;i++){const x=i*125+(Math.sin(i)*18);ctx.strokeStyle='rgba(6,9,9,.5)';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x,90);ctx.lineTo(x+((i%2)*35-18),680);ctx.stroke();}
 for(let i=0;i<9;i++){const x=100+i*145;const y=390+(i%2)*90;ctx.fillStyle='#242f2f';ctx.fillRect(x,y,92,52);ctx.fillStyle='#53605b';ctx.fillRect(x+6,y+6,80,8);ctx.fillStyle='#171d1d';ctx.fillRect(x+10,y+18,72,28);}
 const depth=ctx.createRadialGradient(W/2,420,40,W/2,420,620);depth.addColorStop(0,'rgba(0,0,0,0)');depth.addColorStop(1,'rgba(0,0,0,.55)');ctx.fillStyle=depth;ctx.fillRect(0,0,W,H);
 for(const z of interiorZombies){if(!z.dead||z.deathTimer>0){const xx=z.x,yy=z.y;ctx.save();ctx.translate(xx,yy);ctx.fillStyle='#172020';ctx.beginPath();ctx.ellipse(0,0,20,30,0,0,Math.PI*2);ctx.fill();ctx.fillStyle='#765f57';ctx.beginPath();ctx.arc(0,-31,13,0,Math.PI*2);ctx.fill();ctx.fillStyle='#e06d5d';ctx.fillRect(-6,-33,4,3);ctx.fillRect(3,-33,4,3);ctx.strokeStyle='#26312f';ctx.lineWidth=7;ctx.beginPath();ctx.moveTo(-12,-8);ctx.lineTo(-20,18);ctx.moveTo(12,-8);ctx.lineTo(20,18);ctx.stroke();ctx.restore();}}
 const x=player.x,y=player.y;ctx.save();ctx.translate(x,y);ctx.fillStyle='#1d2928';ctx.beginPath();ctx.roundRect(-17,-22,34,48,9);ctx.fill();ctx.fillStyle='#c0a48e';ctx.beginPath();ctx.arc(0,-36,14,0,Math.PI*2);ctx.fill();ctx.fillStyle='#332527';ctx.beginPath();ctx.arc(0,-40,15,Math.PI,Math.PI*2);ctx.fill();ctx.strokeStyle='#1b2524';ctx.lineWidth=9;ctx.beginPath();ctx.moveTo(-8,18);ctx.lineTo(-12,43);ctx.moveTo(8,18);ctx.lineTo(12,43);ctx.stroke();ctx.restore();
 if(state.light){const lx=player.x+player.facing*15,ly=player.y-25;const beam=ctx.createRadialGradient(lx,ly,10,lx+player.facing*240,ly,270);beam.addColorStop(0,'rgba(241,232,195,.18)');beam.addColorStop(.45,'rgba(226,219,184,.06)');beam.addColorStop(1,'rgba(226,219,184,0)');ctx.fillStyle=beam;ctx.fillRect(0,0,W,H);}
}
function drawCinematicWorldBase(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,W,H);if(horror.shake>0)ctx.translate((Math.random()-.5)*horror.shake,(Math.random()-.5)*horror.shake);if(interior){cinInterior();}else{cinSky();cinGround();cinWorldLandmarks();for(const z of zombies){if(!z.dead)cinZombie(z);}cinPlayer();if(chapter==='ALCATRAZ'){const fog=ctx.createLinearGradient(0,380,0,520);fog.addColorStop(0,'rgba(170,190,184,0)');fog.addColorStop(1,'rgba(170,190,184,.10)');ctx.fillStyle=fog;ctx.fillRect(0,360,W,180);}}
drawDreadPhantom();drawHorrorDirector();drawParticles();drawCrimePixelLayer();drawCrimeHUD();drawDynamicWeather();drawLighting();drawFlashlightCone();drawHorror();drawHudWorld();ctx.restore();}
function drawWorld(){drawCinematicWorldBase();nfDrawDepth();nfDrawCrosshair();nfDrawVignette();}
function updateWorld(dt){updateWorldBase(dt);nfUpdateEvent(dt);if(scene==='play'){NF.cameraBob=lerp(NF.cameraBob,Math.sin(totalTime*8)*Math.min(2.2,Math.abs(player.vx)/110),1-Math.exp(-9*dt));if(!interior)camera+=NF.cameraBob*.08;}renderHUD();}
function renderHUD(){renderHUDBase();const h=document.getElementById('hud');if(!h)return;let el=document.getElementById('nfEventHud');if(!el){el=document.createElement('div');el.id='nfEventHud';el.style.cssText='position:absolute;left:50%;top:88px;transform:translateX(-50%);padding:7px 12px;border:1px solid rgba(190,181,145,.25);background:rgba(3,6,7,.58);backdrop-filter:blur(5px);font:10px Consolas,monospace;letter-spacing:1.5px;color:#bdb8a1;opacity:.0;transition:opacity .2s;pointer-events:none;z-index:22';h.appendChild(el);}if(NF.event){el.textContent=`ACTIVE EVENT  //  ${NF.event}  //  ${Math.ceil(Math.max(0,NF.eventTimer))}s`;el.style.opacity='1';}else{el.style.opacity='0';}}

/* ============================================================================
   ASHES OF THE DEAD // CRIME-HORROR OVERHAUL 3.0
   High-detail top-down exploration layer.
   ============================================================================ */
const A3={
 version:'3.0',
 seed:71337,
 nav:{x:0,y:0,angle:0},
 district:'NORTH SHORE',
 weather:'FOG',
 weatherTimer:0,
 sirenTimer:0,
 rainTimer:0,
 streetPulse:0,
 dustTimer:0,
 ambience:0,
 mapOpen:false,
 mapZoom:.18,
 collisionRadius:34,
 footprints:[],
 shellCasings:[],
 glass:[],
 lights:[],
 doors:[],
 props:[],
 roads:[],
 fences:[],
 buildings:[],
 patrols:[],
 clues:[],
 initialized:false
};

function a3Hash(n){
 let x=(n|0)^0x9e3779b9;
 x=Math.imul(x^(x>>>16),0x85ebca6b);
 x=Math.imul(x^(x>>>13),0xc2b2ae35);
 return ((x^(x>>>16))>>>0)/4294967296;
}
function a3Rand(i=0){
 return a3Hash(Math.floor(i*374761393+A3.seed));
}
function a3Noise(x,y){
 const xi=Math.floor(x/80);
 const yi=Math.floor(y/80);
 const fx=(x%80)/80;
 const fy=(y%80)/80;
 const a=a3Hash(xi*928371+yi*1237);
 const b=a3Hash((xi+1)*928371+yi*1237);
 const c=a3Hash(xi*928371+(yi+1)*1237);
 const d=a3Hash((xi+1)*928371+(yi+1)*1237);
 const ux=fx*fx*(3-2*fx);
 const uy=fy*fy*(3-2*fy);
 return lerp(lerp(a,b,ux),lerp(c,d,ux),uy);
}
function a3DistrictAt(x,y){
 if(chapter==='SF'){
  if(y<4200)return 'NORTH BEACH';
  if(y<7600)return 'MISSION EDGE';
  if(y<10800)return 'DOWNTOWN';
  if(y<14500)return 'SOUTH INDUSTRIAL';
  return 'WATERFRONT';
 }
 if(y<4300)return 'NORTH CLIFF';
 if(y<7600)return 'CELL BLOCK';
 if(y<10800)return 'CENTRAL YARD';
 if(y<14500)return 'SERVICE DISTRICT';
 if(y<18500)return 'SOUTH BATTERY';
 if(y<22500)return 'QUARRY ROAD';
 return 'COVE DISTRICT';
}
function a3WorldX(){return interior?player.x:player.x;}
function a3WorldY(){return interior?player.y:player.y;}
function a3ScreenX(x){return interior?x:x-camera;}
function a3ScreenY(y){return interior?y:y-cameraY;}
function a3Visible(x,y,pad=120){
 const sx=a3ScreenX(x);
 const sy=a3ScreenY(y);
 return sx>-pad&&sx<W+pad&&sy>-pad&&sy<H+pad;
}
function a3RoundRect(x,y,w,h,r,fill,stroke=null,lw=1){
 ctx.beginPath();
 if(ctx.roundRect)ctx.roundRect(x,y,w,h,r);
 else{
  ctx.moveTo(x+r,y);
  ctx.lineTo(x+w-r,y);
  ctx.quadraticCurveTo(x+w,y,x+w,y+r);
  ctx.lineTo(x+w,y+h-r);
  ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);
  ctx.lineTo(x+r,y+h);
  ctx.quadraticCurveTo(x,y+h,x,y+h-r);
  ctx.lineTo(x,y+r);
  ctx.quadraticCurveTo(x,y,x+r,y);
 }
 if(fill){ctx.fillStyle=fill;ctx.fill();}
 if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=lw;ctx.stroke();}
}
function a3Line(x1,y1,x2,y2,c,w=1){
 ctx.strokeStyle=c;
 ctx.lineWidth=w;
 ctx.beginPath();
 ctx.moveTo(x1,y1);
 ctx.lineTo(x2,y2);
 ctx.stroke();
}
function a3Circle(x,y,r,c){
 ctx.fillStyle=c;
 ctx.beginPath();
 ctx.arc(x,y,r,0,Math.PI*2);
 ctx.fill();
}
function a3Text(t,x,y,s,c='#d8d2bf',align='left'){
 ctx.font=`${s}px Consolas,monospace`;
 ctx.textAlign=align;
 ctx.textBaseline='middle';
 ctx.fillStyle=c;
 ctx.fillText(t,x,y);
}
function a3SeedWorld(){
 if(a3.initialized)return;
 a3.initialized=true;
 a3.buildings=[];
 a3.doors=[];
 a3.roads=[];
 a3.fences=[];
 a3.props=[];
 a3.lights=[];
 a3.clues=[];
 for(let i=0;i<landmarkData.length;i++){
  const l=landmarkData[i];
  const bw=clamp(l.w*.68,220,880);
  const bh=clamp(l.h*.72,150,460);
  a3.buildings.push({
   x:l.x,
   y:l.y||4200,
   w:bw,
   h:bh,
   name:l.name,
   type:l.type,
   floors:Math.max(1,l.floors||1),
   locked:(i%7===0),
   crime:i%4===0,
   id:`landmark_${i}`
  });
 }
 for(let i=0;i<42;i++){
  const y=1700+i*640+(i%4)*58;
  a3.roads.push({x1:500,x2:WORLD.ALCATRAZ-500,y,w:70+(i%3)*16});
 }
 for(let i=0;i<38;i++){
  const x=900+i*1320+(i%3)*80;
  a3.roads.push({x,y1:1100,y2:WORLD_HEIGHT.ALCATRAZ-900,w:58+(i%4)*12});
 }
 for(let i=0;i<210;i++){
  const x=500+a3Rand(i*3)*Math.max(1000,WORLD[chapter]-1000);
  const y=1200+a3Rand(i*3+1)*Math.max(2000,WORLD_HEIGHT[chapter]-2500);
  a3.props.push({x,y,type:['tree','lamp','crate','barrel','bench','sign'][i%6],s:.65+a3Rand(i*3+2)*.8});
 }
 for(let i=0;i<90;i++){
  const x=600+a3Rand(900+i)*Math.max(1000,WORLD[chapter]-1200);
  const y=1300+a3Rand(1000+i)*Math.max(2000,WORLD_HEIGHT[chapter]-2600);
  a3.lights.push({x,y,r:45+a3Rand(i)*45,phase:a3Rand(i+33)*6.28,dead:i%9===0});
 }
 for(let i=0;i<18;i++){
  const x=1200+a3Rand(i+200)*Math.max(1000,WORLD[chapter]-2400);
  const y=1800+a3Rand(i+300)*Math.max(1800,WORLD_HEIGHT[chapter]-3600);
  a3.clues.push({x,y,type:i%3===0?'shell':i%3===1?'footprint':'paper',found:false,id:`clue_${i}`});
 }
}
function a3BuildDoorData(){
 a3.doors=[];
 for(const b of a3.buildings){
  a3.doors.push({x:b.x,y:b.y+b.h*.5,w:34,h:92,building:b,side:'west'});
  a3.doors.push({x:b.x+b.w,y:b.y+b.h*.5,w:34,h:92,building:b,side:'east'});
  a3.doors.push({x:b.x+b.w*.5,y:b.y+b.h,w:92,h:34,building:b,side:'south'});
 }
}
function a3FindBuilding(name){
 a3SeedWorld();
 return a3.buildings.find(b=>b.name===name)||null;
}
function a3FindDoor(b){
 if(!a3.doors.length)a3BuildDoorData();
 let best=null,bd=Infinity;
 for(const d of a3.doors){
  if(d.building!==b)continue;
  const dist=Math.hypot(player.x-d.x,player.y-d.y);
  if(dist<bd){bd=dist;best=d;}
 }
 return best;
}
function a3BlockedByBuilding(x,y,r=28){
 if(interior)return false;
 a3SeedWorld();
 for(const b of a3.buildings){
  const left=b.x-b.w*.5;
  const right=b.x+b.w*.5;
  const top=b.y-b.h*.5;
  const bottom=b.y+b.h*.5;
  const cx=clamp(x,left,right);
  const cy=clamp(y,top,bottom);
  const d=Math.hypot(x-cx,y-cy);
  if(d<r){
   const doorY=b.y+b.h*.5;
   const nearDoor=Math.abs(y-doorY)<90&&(Math.abs(x-left)<100||Math.abs(x-right)<100);
   if(!nearDoor)return true;
  }
 }
 return false;
}
function a3MovePlayer(dt,dx,dy,speed){
 const oldX=player.x;
 const oldY=player.y;
 const len=Math.hypot(dx,dy)||1;
 const nx=clamp(player.x+dx/len*speed*dt,180,WORLD[chapter]-180);
 const ny=clamp(player.y+dy/len*speed*dt,900,WORLD_HEIGHT[chapter]-700);
 if(!a3BlockedByBuilding(nx,player.y,32))player.x=nx;
 if(!a3BlockedByBuilding(player.x,ny,32))player.y=ny;
 if(player.x!==oldX||player.y!==oldY){
  if(Math.hypot(player.vx,player.vy)>70)A3.noise=Math.min(100,A3.noise+dt*4);
 }
}
function a3PopulateEnemies(){
 if(chapter==='SF')return;
 const old=zombies||[];
 const count=Math.max(68,old.length);
 zombies=[];
 for(let i=0;i<count;i++){
  const type=i%17===0?'brute':i%11===0?'stalker':i%5===0?'runner':'walker';
  const lane=i%7;
  const x=800+a3Rand(i*9+1)*(WORLD.ALCATRAZ-1600);
  const y=1300+a3Rand(i*9+2)*(WORLD_HEIGHT.ALCATRAZ-2500);
  zombies.push({
   x,y,type,
   hp:type==='brute'?240:type==='stalker'?120:type==='runner'?98:72,
   maxHp:type==='brute'?240:type==='stalker'?120:type==='runner'?98:72,
   dead:false,deathTimer:0,phase:a3Rand(i+40)*6.28,
   attack:0,hit:0,alert:0,flash:0,limb:a3Rand(i+70)*6.28,
   state:'roam',targetX:x,targetY:y,roamTimer:2+a3Rand(i+90)*6,
   lane,hearing:260+(i%4)*80,vision:540+(i%5)*130,
   crimeRole:i%9===0?'detective':i%5===0?'enforcer':i%3===0?'masked':'thug'
  });
 }
}
function a3ChooseRoam(z){
 const district=a3DistrictAt(player.x,player.y);
 const bias=a3Hash(Math.floor(z.phase*1000)+Math.floor(totalTime/4));
 const radius=district==='COVE DISTRICT'?1200:850;
 z.targetX=clamp(z.x+(bias-.5)*radius*2,250,WORLD[chapter]-250);
 z.targetY=clamp(z.y+(a3Hash(Math.floor(z.phase*2000)+3)-.5)*radius*2,1000,WORLD_HEIGHT[chapter]-850);
 z.roamTimer=2.5+bias*5.5;
}
function a3HasLineOfSight(z){
 const dx=player.x-z.x;
 const dy=player.y-z.y;
 const d=Math.hypot(dx,dy);
 if(d>z.vision)return false;
 const steps=Math.max(2,Math.ceil(d/90));
 for(let i=1;i<steps;i++){
  const t=i/steps;
  if(a3BlockedByBuilding(z.x+dx*t,z.y+dy*t,4))return false;
 }
 return true;
}
function a3UpdateEnemy(z,dt){
 if(z.dead){z.deathTimer=Math.max(0,z.deathTimer-dt);return;}
 z.attack=Math.max(0,z.attack-dt);
 z.hit=Math.max(0,z.hit-dt);
 z.flash=Math.max(0,z.flash-dt);
 z.roamTimer-=dt;
 const dx=player.x-z.x;
 const dy=player.y-z.y;
 const d=Math.hypot(dx,dy);
 const visible=a3HasLineOfSight(z);
 const hearing=Math.hypot(player.vx,player.vy)>120&&d<z.hearing;
 if(visible||hearing||horrorDirector.noise>80&&d<850){
  z.alert=clamp((z.alert||0)+dt*(visible?.9:1.4),0,1);
  z.state=z.alert>.3?'hunt':'investigate';
 }else{
  z.alert=Math.max(0,(z.alert||0)-dt*.12);
  if(z.alert<.1)z.state='roam';
 }
 let tx=z.targetX;
 let ty=z.targetY;
 if(z.state==='hunt'){
  tx=player.x;
  ty=player.y;
 }else if(z.state==='investigate'){
  tx=player.x;
  ty=player.y;
 }
 if(z.roamTimer<=0||Math.hypot(tx-z.x,ty-z.y)<70){
  if(z.state==='roam')a3ChooseRoam(z);
  z.roamTimer=Math.max(z.roamTimer,1);
 }
 const vx=tx-z.x;
 const vy=ty-z.y;
 const vlen=Math.hypot(vx,vy)||1;
 let speed=z.type==='warden'?145:z.type==='brute'?70:z.type==='runner'?195:z.type==='stalker'?132:92;
 if(z.state==='hunt')speed*=1.18;
 if(z.state==='investigate')speed*=.72;
 if(z.type==='stalker'&&state.light===false)speed*=1.08;
 const nx=z.x+vx/vlen*speed*dt;
 const ny=z.y+vy/vlen*speed*dt;
 if(!a3BlockedByBuilding(nx,z.y,26))z.x=nx;
 if(!a3BlockedByBuilding(z.x,ny,26))z.y=ny;
 z.x=clamp(z.x,160,WORLD[chapter]-160);
 z.y=clamp(z.y,800,WORLD_HEIGHT[chapter]-650);
 if(d<64&&z.attack<=0){
  const damage=z.type==='brute'?30:z.type==='stalker'?24:z.type==='runner'?19:14;
  damagePlayer(damage);
  z.attack=z.type==='runner'?.42:z.type==='stalker'?.58:.82;
  horror.shake=Math.max(horror.shake,7);
  A3.noise=Math.min(100,A3.noise+22);
 }
}
function updateZombies(dt){
 if(scene!=='play')return;
 if(!a3.initialized)a3SeedWorld();
 if(!interior){
  for(const z of zombies)a3UpdateEnemy(z,dt);
 }
}
function a3UpdatePatrols(dt){
 if(interior||scene!=='play')return;
 if(a3.patrols.length<7&&Math.random()<dt*.12){
  const side=Math.random()<.5?-1:1;
  a3.patrols.push({
   x:clamp(player.x+side*(900+Math.random()*800),300,WORLD[chapter]-300),
   y:clamp(player.y+(Math.random()-.5)*1600,1100,WORLD_HEIGHT[chapter]-1000),
   life:22+Math.random()*20,
   speed:110+Math.random()*45,
   siren:Math.random()<.45,
   phase:Math.random()*6.28
  });
 }
 for(const p of a3.patrols){
  p.life-=dt;
  const dx=player.x-p.x;
  const dy=player.y-p.y;
  const d=Math.hypot(dx,dy);
  const target=d<1200?player:{x:p.x+Math.cos(p.phase)*500,y:p.y+Math.sin(p.phase)*500};
  const tx=target.x-p.x;
  const ty=target.y-p.y;
  const n=Math.hypot(tx,ty)||1;
  p.x+=tx/n*p.speed*dt;
  p.y+=ty/n*p.speed*dt;
  if(p.siren&&d<900){crime.heat=clamp(crime.heat+dt*1.8,0,100);A3.sirenTimer=.4;}
 }
 a3.patrols=a3.patrols.filter(p=>p.life>0);
}
function a3UpdateClues(dt){
 if(interior||scene!=='play')return;
 for(const c of a3.clues){
  if(c.found)continue;
  if(Math.hypot(player.x-c.x,player.y-c.y)<58){
   c.found=true;
   crime.evidence=clamp(crime.evidence+1,0,5);
   crime.clueFlash=1.2;
   state.sanity=Math.max(0,state.sanity-1);
   setMessage(c.type==='shell'?'BALLISTIC EVIDENCE RECOVERED':c.type==='footprint'?'FOOTPRINT PATTERN RECORDED':'HANDWRITTEN NOTE RECOVERED',1.5);
   tone(520,.08,'sine',.16,130);
  }
 }
}
function a3UpdateAtmosphere(dt){
 A3.weatherTimer-=dt;
 A3.sirenTimer=Math.max(0,A3.sirenTimer-dt);
 A3.streetPulse+=dt;
 A3.dustTimer-=dt;
 if(A3.weatherTimer<=0){
  const r=Math.random();
  A3.weather=r<.45?'FOG':r<.7?'DRIZZLE':r<.86?'CLEAR':'HEAVY RAIN';
  A3.weatherTimer=25+Math.random()*45;
 }
 if(A3.dustTimer<=0&&!interior){
  A3.dustTimer=.12;
  const count=A3.weather==='HEAVY RAIN'?2:1;
  for(let i=0;i<count;i++){
   A3.footprints.push({x:player.x+(Math.random()-.5)*16,y:player.y+(Math.random()-.5)*16,life:3.5,type:'player'});
  }
 }
 for(const f of A3.footprints)f.life-=dt;
 A3.footprints=A3.footprints.filter(f=>f.life>0);
}
function a3DrawTerrainTexture(){
 if(interior)return;
 const startX=Math.floor(camera/120)*120;
 const endX=startX+W+240;
 const startY=Math.floor(cameraY/120)*120;
 const endY=startY+H+240;
 for(let wx=startX;wx<endX;wx+=120){
  for(let wy=startY;wy<endY;wy+=120){
   const n=a3Noise(wx,wy);
   const sx=wx-camera;
   const sy=wy-cameraY;
   const alpha=.035+n*.035;
   ctx.fillStyle=`rgba(${50+Math.floor(n*20)},${63+Math.floor(n*22)},${57+Math.floor(n*18)},${alpha})`;
   ctx.fillRect(sx,sy,120,120);
   if(n>.64){
    ctx.strokeStyle='rgba(143,151,130,.12)';
    ctx.lineWidth=1;
    ctx.beginPath();
    ctx.moveTo(sx+20+n*40,sy+80);
    ctx.lineTo(sx+35+n*50,sy+52);
    ctx.stroke();
   }
  }
 }
}
function a3DrawRoads(){
 if(interior)return;
 for(const r of a3.roads){
  if(r.x1!==undefined){
   const y=r.y-cameraY;
   if(y<-r.w||y>H+r.w)continue;
   ctx.fillStyle='rgba(28,34,34,.82)';
   ctx.fillRect(0,y-r.w/2,W,r.w);
   ctx.strokeStyle='rgba(122,127,116,.16)';
   ctx.lineWidth=2;
   ctx.setLineDash([34,28]);
   ctx.beginPath();
   ctx.moveTo(0,y);
   ctx.lineTo(W,y);
   ctx.stroke();
   ctx.setLineDash([]);
   for(let i=0;i<7;i++){
    const xx=((i*220-camera*.25)%W+W)%W;
    a3Line(xx,y-r.w*.4,xx+55,y-r.w*.15,'rgba(9,12,12,.4)',2);
   }
  }else{
   const x=r.x-camera;
   if(x<-r.w||x>W+r.w)continue;
   ctx.fillStyle='rgba(28,34,34,.78)';
   ctx.fillRect(x-r.w/2,0,r.w,H);
   ctx.strokeStyle='rgba(122,127,116,.13)';
   ctx.lineWidth=2;
   ctx.setLineDash([34,28]);
   ctx.beginPath();
   ctx.moveTo(x,0);
   ctx.lineTo(x,H);
   ctx.stroke();
   ctx.setLineDash([]);
  }
 }
}
function a3DrawWater(){
 if(interior)return;
 const top=0;
 const g=ctx.createLinearGradient(0,0,0,H);
 g.addColorStop(0,'#081820');
 g.addColorStop(.45,'#0d252c');
 g.addColorStop(1,'#102f35');
 ctx.fillStyle=g;
 ctx.fillRect(0,0,W,H);
 ctx.globalAlpha=.18;
 for(let i=0;i<22;i++){
  const y=(i*71+totalTime*12)%H;
  ctx.strokeStyle=i%2?'#5c7778':'#263f43';
  ctx.lineWidth=1;
  ctx.beginPath();
  for(let x=0;x<W+30;x+=30){
   const yy=y+Math.sin(x*.03+totalTime+i)*2;
   if(x===0)ctx.moveTo(x,yy);else ctx.lineTo(x,yy);
  }
  ctx.stroke();
 }
 ctx.globalAlpha=1;
}
function a3DrawIslandMass(){
 if(interior)return;
 const cx=W*.52;
 const cy=H*.54;
 ctx.save();
 ctx.translate(-camera*.02,-cameraY*.02);
 const grd=ctx.createLinearGradient(0,cy-500,0,cy+600);
 grd.addColorStop(0,'#314b46');
 grd.addColorStop(.5,'#263c39');
 grd.addColorStop(1,'#1c2e2d');
 ctx.fillStyle=grd;
 ctx.beginPath();
 ctx.moveTo(-120,cy-360);
 ctx.quadraticCurveTo(W*.15,cy-520,W*.38,cy-420);
 ctx.quadraticCurveTo(W*.72,cy-550,W+120,cy-260);
 ctx.lineTo(W+120,H+80);
 ctx.quadraticCurveTo(W*.7,H+160,W*.42,H+70);
 ctx.quadraticCurveTo(W*.12,H+130,-120,H-80);
 ctx.closePath();
 ctx.fill();
 ctx.strokeStyle='rgba(154,167,151,.18)';
 ctx.lineWidth=18;
 ctx.stroke();
 ctx.strokeStyle='rgba(10,18,17,.6)';
 ctx.lineWidth=6;
 ctx.stroke();
 ctx.restore();
}
function a3DrawProps(){
 if(interior)return;
 a3SeedWorld();
 for(const p of a3.props){
  if(!a3Visible(p.x,p.y,90))continue;
  const x=p.x-camera;
  const y=p.y-cameraY;
  const s=p.s;
  if(p.type==='tree'){
   ctx.fillStyle='rgba(0,0,0,.3)';
   ctx.beginPath();ctx.ellipse(x,y+20*s,28*s,9*s,0,0,Math.PI*2);ctx.fill();
   ctx.fillStyle='#253a31';ctx.fillRect(x-5*s,y-2*s,10*s,25*s);
   const g=ctx.createRadialGradient(x-7*s,y-25*s,3,x,y-15*s,42*s);
   g.addColorStop(0,'#506d56');g.addColorStop(.65,'#304b3c');g.addColorStop(1,'#182923');
   ctx.fillStyle=g;
   ctx.beginPath();ctx.arc(x,y-20*s,28*s,0,Math.PI*2);ctx.fill();
   ctx.beginPath();ctx.arc(x-18*s,y-9*s,20*s,0,Math.PI*2);ctx.fill();
   ctx.beginPath();ctx.arc(x+18*s,y-8*s,20*s,0,Math.PI*2);ctx.fill();
  }else if(p.type==='lamp'){
   a3Line(x,y+24*s,x,y-38*s,'#101617',5*s);
   a3Circle(x,y-43*s,6*s,'#2d3430');
   if(Math.sin(totalTime*2+p.x)>.1){
    const g=ctx.createRadialGradient(x,y-42*s,2,x,y-42*s,45*s);
    g.addColorStop(0,'rgba(233,209,146,.22)');g.addColorStop(1,'rgba(233,209,146,0)');
    ctx.fillStyle=g;ctx.fillRect(x-50*s,y-92*s,100*s,100*s);
   }
  }else if(p.type==='crate'){
   a3RoundRect(x-18*s,y-16*s,36*s,32*s,3,'#594937','#8a7050',1);
   a3Line(x-15*s,y-13*s,x+15*s,y+13*s,'rgba(18,19,16,.45)',2);
   a3Line(x+15*s,y-13*s,x-15*s,y+13*s,'rgba(18,19,16,.45)',2);
  }else if(p.type==='barrel'){
   ctx.fillStyle='#3a4140';ctx.beginPath();ctx.ellipse(x,y-12*s,15*s,5*s,0,0,Math.PI*2);ctx.fill();ctx.fillRect(x-15*s,y-12*s,30*s,25*s);ctx.beginPath();ctx.ellipse(x,y+13*s,15*s,5*s,0,0,Math.PI*2);ctx.fill();
   a3Line(x-15*s,y-2*s,x+15*s,y-2*s,'#101617',2);
   a3Line(x-15*s,y+6*s,x+15*s,y+6*s,'#101617',2);
  }else if(p.type==='bench'){
   a3RoundRect(x-30*s,y-14*s,60*s,10*s,3,'#56493d');
   a3Line(x-22*s,y-3*s,x-18*s,y+19*s,'#252625',5);
   a3Line(x+22*s,y-3*s,x+18*s,y+19*s,'#252625',5);
  }else{
   a3RoundRect(x-22*s,y-10*s,44*s,20*s,2,'#3a4544','#111716',1);
   a3Text('KEEP',x,y,6,'#b5aa8c','center');
  }
 }
}
function a3DrawBuildings(){
 if(interior)return;
 a3SeedWorld();
 for(const b of a3.buildings){
  if(!a3Visible(b.x,b.y,Math.max(b.w,b.h)))continue;
  const x=b.x-b.w*.5-camera;
  const y=b.y-b.h*.5-cameraY;
  const w=b.w;
  const h=b.h;
  const roof=b.type==='medical'?'#51676a':b.type==='industry'?'#4b4f4a':b.type==='power'?'#3f4b4d':b.type==='dock'?'#5a4c40':'#5a5a51';
  ctx.fillStyle='rgba(0,0,0,.35)';
  a3RoundRect(x+14,y+18,w,h,16,ctx.fillStyle);
  const wall=ctx.createLinearGradient(x,y,x,y+h);
  wall.addColorStop(0,'#69706a');
  wall.addColorStop(.48,'#4f5955');
  wall.addColorStop(1,'#303a39');
  a3RoundRect(x,y,w,h,14,wall,'rgba(194,193,169,.15)',2);
  ctx.fillStyle=roof;
  ctx.beginPath();
  ctx.moveTo(x+18,y+6);
  ctx.lineTo(x+w*.5,y-22);
  ctx.lineTo(x+w-18,y+6);
  ctx.lineTo(x+w-25,y+20);
  ctx.lineTo(x+25,y+20);
  ctx.closePath();
  ctx.fill();
  for(let c=0;c<Math.max(2,Math.floor(w/110));c++){
   const wx=x+38+c*(w-76)/Math.max(1,Math.floor(w/110)-1);
   for(let r=0;r<Math.max(1,Math.floor(h/90));r++){
    const wy=y+52+r*68;
    const lit=((c*13+r*7+Math.floor(b.x/500))%8===0);
    a3RoundRect(wx-13,wy-9,26,18,3,lit?'#b9a86c':'#1e2828');
    if(lit){ctx.fillStyle='rgba(240,215,146,.14)';ctx.fillRect(wx-9,wy-5,18,10);}
   }
  }
  const door=a3FindDoor(b);
  if(door){
   const dx=door.x-camera;
   const dy=door.y-cameraY;
   a3RoundRect(dx-17,dy-40,34,80,4,'#172020','#6d725e',1);
   a3RoundRect(dx-10,dy-33,20,67,2,'#283434');
   if(Math.hypot(player.x-door.x,player.y-door.y)<220){
    ctx.globalAlpha=.75+.2*Math.sin(totalTime*5);
    a3RoundRect(dx-29,dy-66,58,16,5,'rgba(8,11,11,.82)','#a99a6e',1);
    a3Text(door.building.locked?'LOCKED':'ENTER',dx,dy-58,7,door.building.locked?'#bd7269':'#e0d4b4','center');
    ctx.globalAlpha=1;
   }
  }
  if(b.crime){
   a3Line(x+12,y+h-18,x+w-12,y+h-18,'rgba(175,142,69,.32)',3);
   a3Text('CASE SITE',x+w*.5,y+h+17,7,'#a9996c','center');
  }
  a3Text(b.name,x+w*.5,y-33,8,'#d1ccb9','center');
 }
}
function a3DrawClues(){
 if(interior)return;
 for(const c of a3.clues){
  if(c.found||!a3Visible(c.x,c.y,70))continue;
  const x=c.x-camera;
  const y=c.y-cameraY;
  const pulse=.65+.35*Math.sin(totalTime*5+c.x);
  ctx.globalAlpha=.35*pulse;
  a3Circle(x,y,18,'#b7a66d');
  ctx.globalAlpha=1;
  a3Circle(x,y,4,'#e4d9b0');
 }
}
function a3DrawLighting(){
 if(interior)return;
 for(const l of a3.lights){
  if(l.dead||!a3Visible(l.x,l.y,100))continue;
  const x=l.x-camera;
  const y=l.y-cameraY;
  const pulse=.8+.2*Math.sin(totalTime*2+l.phase);
  const g=ctx.createRadialGradient(x,y,2,x,y,l.r*pulse);
  g.addColorStop(0,'rgba(229,203,139,.18)');
  g.addColorStop(.35,'rgba(229,203,139,.05)');
  g.addColorStop(1,'rgba(229,203,139,0)');
  ctx.fillStyle=g;
  ctx.fillRect(x-l.r,y-l.r,x+l.r,y+l.r);
 }
}
function a3DrawWeather(){
 if(interior)return;
 if(A3.weather==='FOG'){
  const g=ctx.createLinearGradient(0,0,0,H);
  g.addColorStop(0,'rgba(160,174,166,.03)');
  g.addColorStop(.5,'rgba(155,171,164,.10)');
  g.addColorStop(1,'rgba(125,143,140,.14)');
  ctx.fillStyle=g;
  ctx.fillRect(0,0,W,H);
 }
 if(A3.weather==='DRIZZLE'||A3.weather==='HEAVY RAIN'){
  const count=A3.weather==='HEAVY RAIN'?180:75;
  ctx.globalAlpha=A3.weather==='HEAVY RAIN'?.18:.1;
  for(let i=0;i<count;i++){
   const x=(i*83+totalTime*220)%W;
   const y=(i*47+totalTime*360)%H;
   a3Line(x,y,x-5,y+16,'#aab9b4',1);
  }
  ctx.globalAlpha=1;
 }
 if(A3.sirenTimer>0){
  const phase=Math.sin(totalTime*13)>.0;
  ctx.globalAlpha=.07;
  ctx.fillStyle=phase?'#8e2f38':'#496a82';
  ctx.fillRect(0,0,W,H);
  ctx.globalAlpha=1;
 }
}
function drawTopDownExterior(){
 a3SeedWorld();
 ctx.save();
 a3DrawWater();
 a3DrawIslandMass();
 a3DrawTerrainTexture();
 a3DrawRoads();
 a3DrawBuildings();
 a3DrawProps();
 a3DrawClues();
 a3DrawLighting();
 a3DrawWeather();
 ctx.restore();
}
function a3DrawEnemy(z){
 if(z.dead)return;
 const x=z.x-camera;
 const y=z.y-cameraY;
 if(x<-80||x>W+80||y<-80||y>H+80)return;
 const s=z.type==='warden'?1.55:z.type==='brute'?1.35:z.type==='runner'?1.05:1;
 const angle=Math.atan2(player.y-z.y,player.x-z.x);
 const walk=Math.sin(totalTime*(z.type==='runner'?10:5)+z.phase);
 ctx.save();
 ctx.translate(x,y);
 ctx.rotate(angle+Math.PI/2);
 ctx.fillStyle='rgba(0,0,0,.36)';
 ctx.beginPath();ctx.ellipse(0,25*s,24*s,9*s,0,0,Math.PI*2);ctx.fill();
 const coat=z.type==='warden'?'#121618':z.type==='brute'?'#5a4747':z.type==='runner'?'#684b49':'#40504c';
 const g=ctx.createLinearGradient(-20,-35,20,35);
 g.addColorStop(0,coat);
 g.addColorStop(1,'#182221');
 a3RoundRect(-18*s,-22*s,36*s,48*s,9*s,g,'rgba(216,209,187,.1)',1);
 ctx.fillStyle='#a98b78';ctx.beginPath();ctx.arc(0,-37*s,15*s,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#1a2020';ctx.beginPath();ctx.arc(0,-43*s,15*s,Math.PI,Math.PI*2);ctx.fill();
 ctx.fillStyle=z.alert>.45?'#e27462':'#b94d4d';
 a3Circle(-6*s,-38*s,2.8*s,ctx.fillStyle);
 a3Circle(6*s,-38*s,2.8*s,ctx.fillStyle);
 ctx.strokeStyle='#1c2523';ctx.lineWidth=7*s;ctx.lineCap='round';
 ctx.beginPath();
 ctx.moveTo(-13*s,-2*s);ctx.lineTo(-26*s,17*s+walk*3);
 ctx.moveTo(13*s,-2*s);ctx.lineTo(26*s,17*s-walk*3);
 ctx.moveTo(-8*s,25*s);ctx.lineTo(-12*s,43*s+walk*4);
 ctx.moveTo(8*s,25*s);ctx.lineTo(12*s,43*s-walk*4);
 ctx.stroke();
 if(z.crimeRole==='detective'){
  ctx.strokeStyle='#8d6d4f';ctx.lineWidth=3*s;ctx.beginPath();ctx.moveTo(-20*s,-12*s);ctx.lineTo(20*s,-12*s);ctx.stroke();
 }
 if(z.type==='warden'){
  a3RoundRect(-20*s,-61*s,40*s,7*s,2,'#b29a61');
 }
 if(z.hit>0){ctx.globalAlpha=.45;ctx.fillStyle='#f2e5c7';ctx.beginPath();ctx.arc(0,-15*s,35*s,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;}
 if(z.alert>.7){ctx.strokeStyle='rgba(207,116,98,.45)';ctx.lineWidth=1;ctx.beginPath();ctx.arc(0,-20*s,48*s,0,Math.PI*2);ctx.stroke();}
 ctx.restore();
}
function drawTopDownThreats(){
 for(const z of zombies)a3DrawEnemy(z);
 if(A3.patrols.length){
  for(const p of A3.patrols){
   const x=p.x-camera,y=p.y-cameraY;
   if(x<-60||x>W+60||y<-60||y>H+60)continue;
   ctx.save();ctx.translate(x,y);
   a3RoundRect(-20,-12,40,24,6,'#1a2324','#5c6864',1);
   a3RoundRect(-13,-25,26,15,4,'#273333');
   a3Circle(-12,14,6,'#080b0b');a3Circle(12,14,6,'#080b0b');
   const flash=Math.sin(totalTime*10)>0;
   a3Circle(0,-29,4,flash?'#b84e52':'#526d84');
   ctx.restore();
  }
 }
}
function drawTopDownPlayer(){
 const x=player.x-camera;
 const y=player.y-cameraY;
 ctx.save();
 ctx.translate(x,y);
 const moving=Math.hypot(player.vx,player.vy)>25;
 const bob=moving?Math.sin(totalTime*11)*1.7:0;
 ctx.translate(0,bob);
 ctx.fillStyle='rgba(0,0,0,.42)';
 ctx.beginPath();ctx.ellipse(0,29,28,11,0,0,Math.PI*2);ctx.fill();
 const body=ctx.createLinearGradient(-20,-20,20,30);
 body.addColorStop(0,'#66858a');body.addColorStop(.45,'#3f6166');body.addColorStop(1,'#1a2b2e');
 a3RoundRect(-19,-23,38,52,10,body,'rgba(227,221,203,.2)',1);
 ctx.fillStyle='#c4ad96';ctx.beginPath();ctx.arc(0,-39,15,0,Math.PI*2);ctx.fill();
 ctx.fillStyle=selectedCharacter==='Yumi'?'#17221e':selectedCharacter==='May'?'#45312b':'#252a2a';
 ctx.beginPath();ctx.arc(0,-44,16,Math.PI,Math.PI*2);ctx.fill();
 ctx.fillStyle='#566e70';
 a3RoundRect(-29,-15,10,29,5,ctx.fillStyle);
 a3RoundRect(19,-15,10,29,5,ctx.fillStyle);
 ctx.fillStyle='#141b1b';
 a3RoundRect(-15,28,11,10,4,ctx.fillStyle);
 a3RoundRect(4,28,11,10,4,ctx.fillStyle);
 ctx.strokeStyle='rgba(236,229,209,.35)';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(0,-39,16,0,Math.PI*2);ctx.stroke();
 const aimX=mouse.x+camera;
 const aimY=mouse.y+cameraY;
 const angle=Math.atan2(aimY-player.y,aimX-player.x);
 ctx.rotate(angle);
 ctx.strokeStyle='#b7b6a5';ctx.lineWidth=5;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(15,-4);ctx.lineTo(42,-4);ctx.stroke();
 ctx.restore();
 if(state.light){
  const a=Math.atan2(mouse.y-H*.5,mouse.x-W*.5);
  const sx=x,sy=y-8;
  ctx.save();
  ctx.globalAlpha=.12;
  const g=ctx.createRadialGradient(sx,sy,12,sx+Math.cos(a)*180,sy+Math.sin(a)*180,300);
  g.addColorStop(0,'rgba(255,246,204,.3)');
  g.addColorStop(1,'rgba(255,246,204,0)');
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.restore();
 }
}
function a3DrawFootprints(){
 if(interior)return;
 for(const f of A3.footprints){
  const x=f.x-camera,y=f.y-cameraY;
  ctx.globalAlpha=clamp(f.life/3.5,0,.35);
  a3RoundRect(x-3,y-7,6,14,3,'#69706b');
 }
 ctx.globalAlpha=1;
}
function a3DrawWorldOverlay(){
 if(interior)return;
 a3DrawFootprints();
 if(a3Visible(player.x,player.y,0)){
  const sx=player.x-camera;
  const sy=player.y-cameraY;
  ctx.globalAlpha=.25;
  ctx.strokeStyle='#d5c9a4';
  ctx.lineWidth=1;
  ctx.beginPath();ctx.arc(sx,sy,54+Math.sin(totalTime*3)*5,0,Math.PI*2);ctx.stroke();
  ctx.globalAlpha=1;
 }
}
function a3BuildMinimap(){
 let el=document.getElementById('a3Minimap');
 if(el)return el;
 el=document.createElement('canvas');
 el.id='a3Minimap';
 el.width=280;el.height=190;
 el.style.cssText='position:absolute;right:18px;top:112px;width:280px;height:190px;border:1px solid rgba(193,184,151,.38);background:rgba(4,7,7,.78);box-shadow:0 10px 40px rgba(0,0,0,.38);z-index:30;pointer-events:none;border-radius:8px;';
 const hud=document.getElementById('hud');
 if(hud)hud.appendChild(el);else document.body.appendChild(el);
 return el;
}
function a3RenderMinimap(){
 if(scene!=='play'||interior){const e=document.getElementById('a3Minimap');if(e)e.style.display='none';return;}
 const e=a3BuildMinimap();e.style.display='block';
 const m=e.getContext('2d');
 const mw=e.width,mh=e.height;
 m.clearRect(0,0,mw,mh);
 const grad=m.createLinearGradient(0,0,0,mh);grad.addColorStop(0,'#12242a');grad.addColorStop(1,'#1d302f');m.fillStyle=grad;m.fillRect(0,0,mw,mh);
 const sx=mw/WORLD[chapter];
 const sy=mh/WORLD_HEIGHT[chapter];
 for(const r of a3.roads){
  m.strokeStyle='rgba(150,150,130,.18)';m.lineWidth=Math.max(1,r.w*sx*.35);
  m.beginPath();
  if(r.x1!==undefined){m.moveTo(r.x1*sx,r.y*sy);m.lineTo(r.x2*sx,r.y*sy);}else{m.moveTo(r.x*sx,r.y1*sy);m.lineTo(r.x*sx,r.y2*sy);}
  m.stroke();
 }
 for(const b of a3.buildings){
  m.fillStyle=b.crime?'#78524b':'#59625d';
  m.fillRect((b.x-b.w/2)*sx,(b.y-b.h/2)*sy,Math.max(2,b.w*sx),Math.max(2,b.h*sy));
 }
 for(const c of a3.clues){if(!c.found){m.fillStyle='#c2a765';m.fillRect(c.x*sx-1,c.y*sy-1,3,3);}}
 for(const z of zombies){if(z.dead)continue;if(Math.hypot(z.x-player.x,z.y-player.y)<1500){m.fillStyle=z.type==='brute'?'#9d5c56':'#81514e';m.fillRect(z.x*sx-1,z.y*sy-1,2,2);}}
 m.fillStyle='#e1d3a8';m.beginPath();m.arc(player.x*sx,player.y*sy,4,0,Math.PI*2);m.fill();
 m.strokeStyle='rgba(225,211,168,.35)';m.lineWidth=1;m.beginPath();m.arc(player.x*sx,player.y*sy,8,0,Math.PI*2);m.stroke();
 m.fillStyle='#d7cfb8';m.font='10px Consolas';m.textAlign='left';m.fillText(a3DistrictAt(player.x,player.y),8,14);
 m.fillStyle='rgba(4,7,7,.55)';m.fillRect(0,mh-22,mw,22);
 m.fillStyle='#bfb79f';m.fillText('N',mw-16, mh-8);
}
function a3DrawCompass(){
 if(scene!=='play'||interior)return;
 const x=W/2,y=52;
 ctx.save();
 ctx.globalAlpha=.8;
 a3RoundRect(x-92,y-12,184,24,8,'rgba(5,8,8,.72)','rgba(184,176,145,.22)',1);
 const px=WORLD[chapter]?player.x/WORLD[chapter]:0;
 const py=WORLD_HEIGHT[chapter]?player.y/WORLD_HEIGHT[chapter]:0;
 a3Text(`N ${Math.round(py*100)}%`,x-66,y,8,'#bcb49c','center');
 a3Text(`E ${Math.round(px*100)}%`,x,y,8,'#bcb49c','center');
 a3Text(a3DistrictAt(player.x,player.y),x+57,y,7,'#d2c7a8','center');
 ctx.restore();
}
function a3DrawCrimeMarkers(){
 if(interior)return;
 for(const c of a3.clues){
  if(c.found)continue;
  const d=Math.hypot(c.x-player.x,c.y-player.y);
  if(d<520){
   const angle=Math.atan2(c.y-player.y,c.x-player.x);
   const x=W/2+Math.cos(angle)*145;
   const y=H/2+Math.sin(angle)*100;
   ctx.save();ctx.globalAlpha=clamp(1-d/520,.15,.8);ctx.translate(x,y);ctx.rotate(angle);a3Text('◆',0,0,11,'#c2a765','center');ctx.restore();
  }
 }
}
function a3DrawLocationCard(){
 if(scene!=='play')return;
 const district=a3DistrictAt(player.x,player.y);
 if(district===A3.district)return;
 A3.district=district;
 A3.ambience=1;
 setMessage(district,1.1);
}
function a3UpdateLocationCard(dt){
 A3.ambience=Math.max(0,A3.ambience-dt*.45);
}
function a3DrawFineGrain(){
 if(scene!=='play')return;
 ctx.save();
 ctx.globalAlpha=.06;
 for(let i=0;i<260;i++){
  const x=(i*97+Math.floor(totalTime*8))%W;
  const y=(i*53+Math.floor(totalTime*5))%H;
  ctx.fillStyle=i%3?'#d1c9b1':'#6d7772';
  ctx.fillRect(x,y,1,1);
 }
 ctx.restore();
}
function a3DrawCinematicFrame(){
 if(scene!=='play')return;
 ctx.save();
 ctx.fillStyle='rgba(0,0,0,.22)';
 ctx.fillRect(0,0,W,18);
 ctx.fillRect(0,H-18,W,18);
 const g=ctx.createRadialGradient(W/2,H/2,Math.min(W,H)*.22,W/2,H/2,Math.max(W,H)*.76);
 g.addColorStop(0,'rgba(0,0,0,0)');
 g.addColorStop(.65,'rgba(0,0,0,.02)');
 g.addColorStop(1,'rgba(0,0,0,.36)');
 ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 ctx.restore();
}
function a3DrawStatusPanel(){
 if(scene!=='play')return;
 const x=18,y=180;
 const wanted=crime.heat>50;
 ctx.save();
 a3RoundRect(x,y,238,58,7,'rgba(5,8,8,.68)','rgba(181,171,139,.18)',1);
 a3Text(`DISTRICT  ${a3DistrictAt(player.x,player.y)}`,x+10,y+15,8,'#c7c0a7');
 a3Text(`WEATHER   ${A3.weather}`,x+10,y+31,8,'#aeb7af');
 a3Text(wanted?'POLICE SEARCH ACTIVE':'POLICE SEARCH: LOW',x+10,y+47,8,wanted?'#c97c6f':'#8d9a91');
 ctx.restore();
}
function a3RenderHUD(){
 a3RenderMinimap();
 a3DrawCompass();
 a3DrawCrimeMarkers();
 a3DrawStatusPanel();
}
function a3Update(dt){
 if(scene!=='play')return;
 if(!a3.initialized)a3SeedWorld();
 a3UpdateAtmosphere(dt);
 a3UpdatePatrols(dt);
 a3UpdateClues(dt);
 a3UpdateLocationCard(dt);
}
function a3PatchMovement(){
 if(scene!=='play'||interior)return false;
 const dx=(inputState.right?1:0)-(inputState.left?1:0);
 const dy=((keys.has('s')||keys.has('S')||keys.has('ArrowDown')||touch.down)?1:0)-((keys.has('w')||keys.has('W')||keys.has('ArrowUp')||touch.up)?1:0);
 if(!dx&&!dy)return false;
 const base=inputState.run&&state.stamina>5?360:245;
 a3MovePlayer(.016,dx,dy,base);
 return true;
}
const a3OriginalMovementStep=movementStep;
function movementStep(dt){
 if(scene!=='play')return;
 if(interior){
  const dx=(inputState.right?1:0)-(inputState.left?1:0);
  const dy=((keys.has('s')||keys.has('S')||keys.has('ArrowDown')||touch.down)?1:0)-((keys.has('w')||keys.has('W')||keys.has('ArrowUp')||touch.up)?1:0);
  const mag=Math.hypot(dx,dy)||1;
  const base=inputState.run&&state.stamina>5?300:205;
  player.vx=lerp(player.vx,(dx/mag)*base,1-Math.exp(-15*dt));
  player.vy=lerp(player.vy,(dy/mag)*base,1-Math.exp(-15*dt));
  if(dx||dy)player.facing=dx<0?-1:dx>0?1:player.facing;
  if(inputState.run&&state.stamina>0&&mag>0)state.stamina=Math.max(0,state.stamina-dt*24);else state.stamina=Math.min(100,state.stamina+dt*17);
  const nx=clamp(player.x+player.vx*dt,42,1358);
  const ny=clamp(player.y+player.vy*dt,88,682);
  player.x=nx;player.y=ny;
  if(Math.abs(player.vx)+Math.abs(player.vy)>18)player.anim+=dt*8;
  const near=nearestBuilding();
  if(near&&(keys.has('ArrowUp')||keys.has('w')||keys.has('W')||touch.up||touch.interact||keys.has('e')||keys.has('E')))enterStructure(near);
  return;
 }
 const dx=(inputState.right?1:0)-(inputState.left?1:0);
 const dy=((keys.has('s')||keys.has('S')||keys.has('ArrowDown')||touch.down)?1:0)-((keys.has('w')||keys.has('W')||keys.has('ArrowUp')||touch.up)?1:0);
 const mag=Math.hypot(dx,dy);
 if(mag>0){
  const base=inputState.run&&state.stamina>5?360:245;
  player.vx=lerp(player.vx,(dx/mag)*base,1-Math.exp(-18*dt));
  player.vy=lerp(player.vy,(dy/mag)*base,1-Math.exp(-18*dt));
  player.facing=dx<0?-1:dx>0?1:player.facing;
  a3MovePlayer(dt,dx,dy,base);
  player.anim+=dt*(inputState.run?13:9);
  if(inputState.run&&state.stamina>0)state.stamina=Math.max(0,state.stamina-dt*22);else state.stamina=Math.min(100,state.stamina+dt*14);
 }else{
  player.vx=lerp(player.vx,0,1-Math.exp(-22*dt));
  player.vy=lerp(player.vy,0,1-Math.exp(-22*dt));
  state.stamina=Math.min(100,state.stamina+dt*16);
 }
 const near=nearestBuilding();
 if(near&&(keys.has('e')||keys.has('E')||keys.has('ArrowUp')||keys.has('w')||keys.has('W')||touch.interact||touch.up))enterStructure(near);
}
function nearestBuilding(){
 if(interior||!a3.initialized)return null;
 let best=null,bd=Infinity;
 for(const b of a3.buildings){
  const d=Math.hypot(player.x-b.x,player.y-b.y);
  const doorDist=Math.min(d,Math.abs(player.x-(b.x-b.w/2))+Math.abs(player.y-b.y),Math.abs(player.x-(b.x+b.w/2))+Math.abs(player.y-b.y));
  if(doorDist<720&&doorDist<bd){bd=doorDist;best=b;}
 }
 return best;
}
function enterStructure(b){
 if(!b||fadeBusy)return;
 if(b.locked&&!state.startKey&&b.name!=='CELLHOUSE'){
  setMessage(`${b.name} IS LOCKED. FIND ANOTHER WAY IN.`,1.4);
  crime.heat=clamp(crime.heat+2,0,100);
  return;
 }
 transitionTo('enter',()=>{
  interior={id:b.id||b.type+'_'+b.x,name:b.name,type:b.type,building:b,roomWidth:1400,roomHeight:788,floor:1,floors:Math.max(1,b.floors||3),stairCooldown:0,topDown:true};
  interiorPhase=0;
  player.x=700;
  player.y=430;
  player.vx=0;
  player.vy=0;
  player.onGround=true;
  spawnInteriorThreats();
  soundDoor();
  setMessage(`ENTERED ${b.name} — SEARCH EVERY ROOM.`,1.4);
 });
}
function a3EnterNearest(){
 const b=nearestBuilding();
 if(!b)return false;
 enterStructure(b);
 return true;
}
function a3DoorPrompt(){
 if(scene!=='play'||interior)return;
 const b=nearestBuilding();
 if(!b)return;
 const d=Math.hypot(player.x-b.x,player.y-b.y);
 if(d<500){
  const e=document.getElementById('prompt');
  if(e)e.textContent=`E / ↑  ${b.locked?'LOCKED — FIND ACCESS':'ENTER '+b.name}`;
 }
}
function a3PatchUseInteract(){
 const b=nearestBuilding();
 if(b){enterStructure(b);return true;}
 return false;
}
const a3OldUseInteract=useInteract;
function useInteract(){
 if(scene!=='play')return;
 if(!interior&&a3PatchUseInteract())return;
 a3OldUseInteract();
}
function a3PatchReset(){
 a3OldReset();
 a3SeedWorld();
 a3BuildDoorData();
 a3PopulateEnemies();
 player.x=1250;
 player.y=5400;
 camera=0;
 cameraY=0;
 A3.patrols=[];
 A3.clues.forEach(c=>c.found=false);
 A3.weather='FOG';
 A3.weatherTimer=22;
}
const a3OldReset=resetWorld;
resetWorld=a3PatchReset;
function a3PatchWorldBase(dt){
 const old=updateWorldBase;
 return old(dt);
}
const a3OldUpdateWorldBase=updateWorldBase;
function updateWorldBase(dt){
 a3OldUpdateWorldBase(dt);
 a3Update(dt);
}
function a3PatchDraw(){
 if(scene!=='play')return;
 a3DrawWorldOverlay();
 a3DrawFineGrain();
 a3DrawCinematicFrame();
 a3RenderHUD();
 a3DoorPrompt();
}
const a3OldDrawWorld=drawWorld;
function drawWorld(){
 a3OldDrawWorld();
 a3PatchDraw();
}
function a3ToggleMap(){
 A3.mapOpen=!A3.mapOpen;
 let e=document.getElementById('a3MapOverlay');
 if(!e){
  e=document.createElement('div');
  e.id='a3MapOverlay';
  e.style.cssText='position:fixed;inset:0;background:rgba(2,5,5,.82);z-index:120;display:none;align-items:center;justify-content:center;backdrop-filter:blur(5px);';
  e.innerHTML='<canvas id="a3BigMap" width="1100" height="720" style="width:min(92vw,1100px);height:auto;border:1px solid rgba(205,194,160,.35);background:#13262a;border-radius:12px;box-shadow:0 30px 100px #000"></canvas><div style="position:fixed;top:24px;left:50%;transform:translateX(-50%);font:12px Consolas;color:#d8cfb3;letter-spacing:3px">FIELD MAP // M TO CLOSE</div>';
  document.body.appendChild(e);
 }
 e.style.display=A3.mapOpen?'flex':'none';
 if(A3.mapOpen)a3RenderBigMap();
}
function a3RenderBigMap(){
 const e=document.getElementById('a3BigMap');
 if(!e)return;
 const m=e.getContext('2d');
 const mw=e.width,mh=e.height;
 m.clearRect(0,0,mw,mh);
 const grad=m.createLinearGradient(0,0,0,mh);grad.addColorStop(0,'#10242b');grad.addColorStop(1,'#1b302f');m.fillStyle=grad;m.fillRect(0,0,mw,mh);
 const sx=mw/WORLD[chapter],sy=mh/WORLD_HEIGHT[chapter];
 m.fillStyle='rgba(52,73,66,.78)';m.beginPath();m.ellipse(mw*.5,mh*.5,mw*.42,mh*.47,0,0,Math.PI*2);m.fill();
 for(const r of a3.roads){m.strokeStyle='rgba(171,169,143,.16)';m.lineWidth=Math.max(2,r.w*sx*.5);m.beginPath();if(r.x1!==undefined){m.moveTo(r.x1*sx,r.y*sy);m.lineTo(r.x2*sx,r.y*sy);}else{m.moveTo(r.x*sx,r.y1*sy);m.lineTo(r.x*sx,r.y2*sy);}m.stroke();}
 for(const b of a3.buildings){m.fillStyle=b.crime?'#82554d':'#66716a';m.fillRect((b.x-b.w/2)*sx,(b.y-b.h/2)*sy,b.w*sx,b.h*sy);m.strokeStyle='rgba(222,214,186,.16)';m.strokeRect((b.x-b.w/2)*sx,(b.y-b.h/2)*sy,b.w*sx,b.h*sy);}
 for(const c of a3.clues){if(!c.found){m.fillStyle='#d0b76e';m.beginPath();m.arc(c.x*sx,c.y*sy,4,0,Math.PI*2);m.fill();}}
 m.fillStyle='#d9d0ae';m.beginPath();m.arc(player.x*sx,player.y*sy,7,0,Math.PI*2);m.fill();
 m.strokeStyle='#d9d0ae';m.lineWidth=2;m.beginPath();m.arc(player.x*sx,player.y*sy,14,0,Math.PI*2);m.stroke();
 m.fillStyle='#d7cfb8';m.font='16px Consolas';m.fillText(a3DistrictAt(player.x,player.y),24,30);
}
function a3KeyMap(e){
 if(e.key==='m'||e.key==='M'){
  if(scene==='play'){e.preventDefault();a3ToggleMap();}
 }
 if(e.key==='Escape'&&A3.mapOpen){e.preventDefault();a3ToggleMap();}
}
window.addEventListener('keydown',a3KeyMap,{passive:false});
function a3InstallHUD(){
 if(document.getElementById('a3Legend'))return;
 const e=document.createElement('div');
 e.id='a3Legend';
 e.style.cssText='position:absolute;right:18px;top:310px;width:280px;padding:9px 11px;border:1px solid rgba(190,181,145,.18);border-radius:8px;background:rgba(4,7,7,.6);font:8px Consolas;color:#aaa894;letter-spacing:1px;z-index:30;pointer-events:none;';
 e.innerHTML='M MAP  •  E ENTER  •  WASD / ARROWS MOVE  •  SHIFT RUN  •  F LIGHT  •  Q MELEE  •  R RELOAD';
 const hud=document.getElementById('hud');if(hud)hud.appendChild(e);else document.body.appendChild(e);
}
const a3OldSetup=setupInterface;
function setupInterface(){
 a3OldSetup();
 a3InstallHUD();
}
/* ---------------------------- EXTRA VISUAL PASS ---------------------------- */
function a3DrawRoadDetails(){
 if(interior)return;
 for(let i=0;i<55;i++){
  const x=((i*317-camera*.55)%W+W)%W;
  const y=((i*181-cameraY*.35)%H+H)%H;
  ctx.globalAlpha=.08;
  ctx.strokeStyle=i%2?'#151b1b':'#9a9c88';
  ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+18+(i%5)*7,y+(i%3-1)*2);ctx.stroke();
 }
 ctx.globalAlpha=1;
}
function a3DrawFences(){
 if(interior)return;
 for(let i=0;i<28;i++){
  const x=((i*487-camera*.9)%W+W)%W;
  const y=((i*291-cameraY*.8)%H+H)%H;
  ctx.globalAlpha=.3;
  for(let k=0;k<5;k++){a3Line(x+k*14,y,x+k*14,y+18,'#222b29',2);if(k<4)a3Line(x+k*14,y,x+(k+1)*14,y,'#3e4843',1);}
 }
 ctx.globalAlpha=1;
}
function a3DrawParkDetails(){
 if(interior)return;
 for(let i=0;i<40;i++){
  const x=((i*211-camera*.22)%W+W)%W;
  const y=((i*151-cameraY*.18)%H+H)%H;
  ctx.globalAlpha=.18;
  a3Circle(x,y,2+(i%3),'#81916f');
  ctx.globalAlpha=1;
 }
}
function a3DrawWorldMicrodetail(){
 a3DrawRoadDetails();
 a3DrawFences();
 a3DrawParkDetails();
}
const a3OldDrawTopDownExterior=drawTopDownExterior;
function drawTopDownExterior(){
 a3OldDrawTopDownExterior();
 a3DrawWorldMicrodetail();
}
/* ------------------------------ CRIME PATROLS ------------------------------ */
function a3SpawnCrimeScene(){
 if(interior||scene!=='play')return;
 if(crime.evidence>=5||crime.heat<25)return;
 if(Math.random()<.0015){
  const x=clamp(player.x+(Math.random()<.5?-1:1)*(400+Math.random()*700),400,WORLD[chapter]-400);
  const y=clamp(player.y+(Math.random()-.5)*1200,1200,WORLD_HEIGHT[chapter]-1200);
  a3.clues.push({x,y,type:'paper',found:false,id:`scene_${Math.floor(totalTime)}`});
  showWarning('A FRESH CRIME SCENE WAS DISCOVERED.',1.5);
 }
}
function a3PolicePressure(dt){
 if(scene!=='play'||interior)return;
 if(crime.heat>70){crime.policeTimer=Math.max(0,crime.policeTimer-dt);if(crime.policeTimer<=0){crime.policeTimer=8+Math.random()*8;a3.sirenTimer=3;crime.heat=clamp(crime.heat-2,0,100);showWarning('PATROL SEARCHING THE DISTRICT.',1.2);}}
}
function a3CrimeUpdate(dt){
 a3SpawnCrimeScene();
 a3PolicePressure(dt);
}
const a3OldUpdateCrime=updateCrime;
function updateCrime(dt){
 a3OldUpdateCrime(dt);
 a3CrimeUpdate(dt);
}
/* ------------------------------ SOUND DIRECTOR ----------------------------- */
function a3AmbientSound(dt){
 if(scene!=='play'||!soundEnabled)return;
 A3.ambience+=dt;
 if(A3.ambience>9+Math.random()*8){
  A3.ambience=0;
  const r=Math.random();
  if(r<.3)tone(42,.6,'sine',.02,-3,'music');
  else if(r<.6)noiseBurst(.08,.015,'rain');
  else if(r<.8)tone(160,.06,'triangle',.018,-80,'sfx');
 }
}
const a3OldUpdateWorldBase2=updateWorldBase;
function updateWorldBase(dt){
 a3OldUpdateWorldBase2(dt);
 a3AmbientSound(dt);
}
/* ------------------------------ FINAL RENDER ------------------------------- */
const a3OldDrawWorld2=drawWorld;
function drawWorld(){
 a3OldDrawWorld2();
 if(scene==='play'){
  a3DrawWorldOverlay();
  a3DrawFineGrain();
  a3DrawCinematicFrame();
  a3RenderHUD();
 }
}
/* ---------------------------- STARTUP SAFETY ------------------------------- */
function a3Startup(){
 try{
  a3SeedWorld();
  a3BuildDoorData();
  a3PopulateEnemies();
  a3InstallHUD();
 }catch(err){
  console.warn('A3 startup:',err);
 }
}
a3Startup();

boot();
</script>
</body>
</html>'''

@app.get('/')
def index():
    return Response(GAME_HTML, mimetype='text/html')

@app.get('/gadget')
def gadget():
    forwarded = request.headers.get('X-Forwarded-For', '')
    seen = forwarded.split(',')[0].strip() if forwarded else request.remote_addr
    return jsonify({'server_seen_ip': seen or 'unknown', 'note': 'The address visible to the game server may be a proxy address.'})

@app.get('/health')
def health():
    return {'status': 'ok', 'game': 'Ashes of the Dead', 'chapter': 'Alcatraz Escape'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
