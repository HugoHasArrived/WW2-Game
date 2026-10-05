from flask import Flask, Response, request, jsonify

app = Flask(__name__)

GAME_HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>ESCAPE ALCATRAZ — NIGHTFALL</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#020304;color:#eee7d7;font-family:Consolas,monospace}
body{display:grid;place-items:center}
button{font:inherit;color:#eee7d7;background:#0b1012;border:1px solid #6e7673;cursor:pointer;touch-action:manipulation}
button:hover{background:#172022;border-color:#c7b98f}
button:focus-visible{outline:2px solid #dbc98f;outline-offset:3px}
.hidden{display:none!important}
#app{position:relative;width:min(100vw,1400px);aspect-ratio:16/9;overflow:hidden;background:#06090b;box-shadow:0 0 0 1px #1e2527,0 0 120px #000}
#world{position:absolute;inset:0;width:100%;height:100%;display:block;background:#071217;image-rendering:pixelated;image-rendering:crisp-edges}
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
</style>
</style>
</head>
<body>
<div id="app">
<canvas id="world" width="1400" height="788"></canvas>
<div id="mainMenu" class="layer menu">
<div class="menuBackdrop"><div class="menuMoon"></div><div class="menuOcean"></div><div class="menuIsland"></div><div class="menuPrison"></div><div class="menuTower"></div><div class="menuFog"></div><div class="menuFog two"></div><div class="menuRain"></div><div class="menuVignette"></div><div class="menuNoise"></div></div>
<div class="menuContent"><div class="menuKicker">NIGHTWATCH // ALCATRAZ ESCAPE PROTOCOL</div><div class="menuLogo">ESCAPE ALCATRAZ</div><div class="menuTag">NIGHTFALL • ALCATRAZ ISLAND • ESCAPE PROTOCOL</div><div class="menuLore">You wake inside Cell A-17 after the last emergency broadcast dies. The prison is dark, the sea is violent, and something is moving through the cell blocks. Reach the dock before dawn — but first restore power, find the ferry pass, and survive the island.</div><div class="menuButtons"><button id="playButton" class="menuPlay">PLAY</button><button id="creditsButton">CREDITS</button><button id="controlsButton">CONTROL MODE</button></div><div class="menuThreat">HEADPHONES RECOMMENDED • SOME SOUNDS AREN'T AMBIENCE • NIGHT MODE ACTIVE</div><div class="menuFooter">JULIA • MAY • YUMI • LARGE 2D ALCATRAZ RECONSTRUCTION • SURVIVAL HORROR</div><div class="menuSignal">SIGNAL // <b>UNSTABLE</b></div></div>
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
<div id="mobileControls" class="hidden"><div class="mobileCluster left"><button data-touch="left">◀</button><button data-touch="right">▶</button><button class="wide" data-touch="run">RUN</button></div><div class="mobileCluster right"><button data-touch="jump">JUMP</button><button data-touch="interact">USE</button><button data-touch="melee">MELEE</button><button data-touch="light">LIGHT</button><button data-touch="inventory">BAG</button><button data-touch="reload">RELOAD</button><button class="wide" data-touch="fire">FIRE</button></div></div>
<div id="privacyGate"><div class="privacyBox"><div class="privacyTitle">NIGHTWATCH SECURITY TERMINAL</div><div class="privacySub">ESCAPE ALCATRAZ • DEVICE & PRIVACY NOTICE</div><div class="privacyGrid"><div class="privacyCard"><b>WHAT MAY BE DISPLAYED</b>Browser and platform information, screen size, language, timezone, online state, network hints, CPU thread count, touch support, battery data when available, and the network address seen by the game server.</div><div class="privacyCard"><b>WHAT IS NOT READ</b>Passwords, personal files, photos, contacts, saved documents, account contents, and arbitrary private files are not read by this game.</div><div class="privacyCard"><b>PERMISSIONS</b>Location, camera, and microphone require separate browser permission. This game does not silently grant those permissions.</div><div class="privacyCard"><b>FICTIONAL SURVEILLANCE</b>CCTV warnings, The Smiler, tracking messages, fourth-wall events, and horror-terminal events are fictional game elements unless the interface specifically labels information as browser or server information.</div></div><div class="privacyNote">The server only sees the network address that reaches it. A proxy, VPN, carrier network, or hosting layer can change the address shown. This game is entertainment, not a security diagnostic.</div><div class="privacyActions"><button id="privacyEnter">ENTER ESCAPE ALCATRAZ</button><button id="privacyDevice">VIEW DEVICE RECORD</button></div></div></div>
</div>
<script>
const canvas=document.getElementById('world');
const ctx=canvas.getContext('2d');
ctx.imageSmoothingEnabled=false;
const W=1400,H=788,GROUND=612;
const WORLD={ALCATRAZ:22000,SF:11000};
const keys=new Set();
const touch={left:false,right:false,run:false,jump:false};
const mouse={x:W/2,y:H/2,down:false};
const inputState={left:false,right:false,run:false,jump:false};
const player={x:0,y:0,w:38,h:76,vx:0,vy:0,facing:1,onGround:true,coyote:0,jumpBuffer:0,jumps:2,anim:0,stepTimer:0,landTimer:0,recoil:0,flashStep:0,lean:0,air:0};
const state={health:100,maxHealth:100,stamina:100,maxStamina:100,sanity:100,ammo:12,reserveAmmo:48,grenades:3,light:true,battery:100,startKey:false,startEscaped:false,dockPass:false,powerRestored:false,radioSignal:false,beacon:false,boatEscaped:false,survivors:0,alarm:false,finalChase:false,inventory:{bandage:2,food:2,scrap:3,ammo_9mm:48,key:0,dockPass:0,fuse:0,radioPart:0}};
let scene='menu';
let chapter='ALCATRAZ';
let selectedCharacter='Julia';
let controlMode='laptop';
let last=performance.now();
let totalTime=0;
let camera=0;
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
'ALCATRAZ ISLAND — 11:47 PM',
'You wake inside Cell A-17. Concrete walls. Rusted bars. Rain beyond the block.',
'The lock is still closed. Your badge is cold against your coat.',
'You find a small brass key beneath the mattress.',
'Outside the cell is a corridor that leads through Cell Block A and down the island.',
'Your first goal is simple: find the docks. Escape the island.'
];
const objectives=[
{title:'SURVIVE CELL BLOCK A',steps:['Search Cell A-17 for the brass key.','Unlock the cell and enter the corridor.','Cross the Recreation Yard without getting cornered.','Reach the Hospital Wing.']},
{title:'RESTORE THE ESCAPE ROUTE',steps:['Find the Dock Pass inside the Hospital Wing.','Reach the Power Plant and restore emergency power.','Find the radio room and transmit the evacuation signal.','Reach the Emergency Pier.','Light the ferry beacon and survive the wait.','Board the ferry.']},
{title:'ESCAPE ALCATRAZ',steps:['Reach the emergency pier.','Use the ferry beacon.','Survive the final attack.','Escape Alcatraz.']}
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
{name:'EMERGENCY PIER',x:21700,w:340,h:165,type:'dock'}
];
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
 state.health=100;state.maxHealth=100;state.stamina=100;state.maxStamina=100;state.sanity=100;state.ammo=12;state.reserveAmmo=48;state.grenades=3;state.light=true;state.battery=100;state.startKey=false;state.startEscaped=false;state.dockPass=false;state.powerRestored=false;state.radioSignal=false;state.beacon=false;state.boatEscaped=false;state.survivors=0;state.alarm=false;state.finalChase=false;state.inventory={bandage:2,food:2,scrap:3,ammo_9mm:48,key:0,dockPass:0,fuse:0,radioPart:0};chapter='ALCATRAZ';camera=0;interior=null;interiorPhase=0;objectiveIndex=0;currentChest=null;endingTriggered=false;smiler={active:false,x:0,timer:0,cooldown:16,intensity:0};horror={shake:0,flash:0,glitch:0,warning:0,blackout:0};particles=[];footprints=[];zombies=[];survivors=[];buildAlcatrazPopulation();player.x=210;player.y=GROUND-player.h;player.vx=0;player.vy=0;player.onGround=true;player.coyote=.12;player.jumpBuffer=0;player.jumps=2;player.anim=0;player.stepTimer=0;player.landTimer=0;player.recoil=0;player.lean=0;setObjective();
}
function buildAlcatrazPopulation(){
 zombies=[];
 for(let i=0;i<52;i++){
  const x=1250+i*392+(i%5)*73;
  const type=i%13===0?'brute':i%7===0?'stalker':i%4===0?'runner':'walker';
  zombies.push({x,type,hp:type==='brute'?230:type==='stalker'?110:type==='runner'?95:70,maxHp:type==='brute'?230:type==='stalker'?110:type==='runner'?95:70,dead:false,deathTimer:0,phase:i*.61,attack:0,hit:0,alert:0,flash:0,limb:Math.random()*6.28});
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
 for(let i=0;i<28;i++)zombies.push({x:600+i*370+(i%5)*42,type:i%8===0?'brute':i%4===0?'runner':'walker',hp:i%8===0?180:i%4===0?90:65,maxHp:i%8===0?180:i%4===0?90:65,dead:false,deathTimer:0,phase:i*.51,attack:0,hit:0,flash:0,limb:Math.random()*6.28});
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
function exitStructure(){if(!interior||fadeBusy)return;const b=interior.building;if(interior.topDown){if(interior.id==='cellA17'&&!state.startEscaped){setMessage('The cell is sealed. Search the mattress and find the key.',1.7);return;}if(interior.id==='cellA17'&&player.x>1240){enterCellCorridor();return;}if(player.x<70||player.x>1330){transitionTo('exit',()=>{const side=player.x<70?-1:1;const outside=side<0?b.x-80:b.x+b.w+80;player.x=clamp(outside,80,WORLD[chapter]-80);player.y=GROUND-player.h;player.vx=0;player.vy=0;interior=null;interiorZombies=[];camera=clamp(player.x-W*.4,0,WORLD[chapter]-W);soundDoor();setMessage(`BACK OUTSIDE — ${b.name}.`,1.3);});return;}setMessage('Find an EXIT door or stairwell.',1.0);return;}const side=player.x<200?-1:player.x>980?1:0;if(interior.id==='cellA17'&&!state.startEscaped){setMessage('The cell door is closed. Search the mattress and unlock it.',1.7);return;}if(interior.id==='cellA17'&&side!==0){enterCellCorridor();return;}if(side===0){setMessage('Move closer to the EXIT door.',1.2);return;}transitionTo('exit',()=>{const outside=side<0?b.x-80:b.x+b.w+80;player.x=clamp(outside,80,WORLD[chapter]-80);player.y=GROUND-player.h;player.vx=0;player.vy=0;player.onGround=true;interior=null;camera=clamp(player.x-W*.4,0,WORLD[chapter]-W);soundDoor();setMessage(`BACK OUTSIDE — ${b.name}.`,1.3);});}
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
function useInteract(){if(scene!=='play'||fadeBusy)return;if(currentChest){openChest(currentChest);return;}if(interior&&interior.topDown){if(interior.floors>1&&((Math.abs(player.x-145)<100||Math.abs(player.x-1245)<100)&&player.y>250&&player.y<520)){const nearLeft=player.x<700;const dir=nearLeft?1:-1;const next=clamp(interior.floor+dir,1,interior.floors);if(next===interior.floor){setMessage('NO MORE FLOORS.',1);return;}interior.floor=next;player.x=nearLeft?220:1180;player.y=390;state.sanity=Math.max(0,state.sanity-5);horror.shake=8;setMessage(`STAIRS — FLOOR ${interior.floor}/${interior.floors}`,1.4);if(interior.floor===3&&Math.random()<.8)triggerJumpscare('stair');return;}if(interior.id==='cellA17'&&!state.startKey&&Math.hypot(player.x-310,player.y-390)<110){searchStartingCell();return;}if(interior.id==='cellA17'&&state.startKey&&Math.hypot(player.x-1240,player.y-390)<125){unlockCell();return;}const c=nearestChest();if(c){openChest(c);return;}if(player.x<70||player.x>1330){exitStructure();return;}return;}if(interior&&interior.floors>1&&tryUseStairs())return;if(interactAlcatrazSpecial())return;if(interior){if(player.x<170||player.x>1010){exitStructure();return;}const c=nearestChest();if(c){openChest(c);return;}return;}if(chapter==='ALCATRAZ'){if(!state.startEscaped&&player.x<1050){setMessage('The cell is still locked. Search the mattress.',1.5);return;}const b=nearestBuilding();if(b){enterStructure(b);return;}if(Math.abs(player.x-21700)<330){if(!state.dockPass){setMessage('THE PIER GATE IS LOCKED. YOU NEED THE DOCK PASS.',2);return;}if(!state.powerRestored){setMessage('NO POWER. Restore the emergency generator first.',2);return;}if(!state.radioSignal){setMessage('THE FERRY WILL NOT ANSWER. Transmit the emergency signal.',2);return;}if(!state.beacon){state.beacon=true;advanceObjective(1);setMessage('BEACON LIT. THE FERRY IS COMING. RUN.',2);tone(250,.5,'sine',.13,90);state.finalChase=true;return;}if(!state.boatEscaped){state.boatEscaped=true;transitionTo('ferry',()=>{endingTriggered=true;scene='ending';show('ending');document.getElementById('endingText').textContent='The ferry reaches the pier through the storm. Behind you, the cellhouse lights turn on one by one. The last camera feed shows a figure standing in your empty cell.';soundScare();});return;}}}else{if(talkSurvivorState())return;const b=nearestBuilding();if(b){enterStructure(b);return;}if(state.survivors>=2&&Math.abs(player.x-3200)<420){endingTriggered=true;scene='ending';show('ending');document.getElementById('endingText').textContent='Two survivors reached the shelter. Behind the rain, the island lights were still visible. On the final CCTV frame, a tall figure smiled at the empty dock.';soundScare();}}}

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

function nearestBuilding(){let best=null,d=9999;for(const b of landmarkData){if(b.name==='CELLHOUSE'||b.name==='RECREATION YARD'||b.name==='MAIN DOCK')continue;const dd=Math.abs(player.x-b.x);if(dd<d&&dd<180){d=dd;best=b;}}return best;}
function spawnInteriorThreats(){
 interiorZombies=[];
 const count=interior.type==='cellcorridor'?8:6;
 for(let i=0;i<count;i++){
  interiorZombies.push({x:170+(i*173)%1080,y:155+(i*97)%430,hp:i%4===0?120:65,type:i%5===0?'stalker':i%3===0?'runner':'walker',attack:0,phase:i*.8,dead:false,deathTimer:0});
 }
}
function updateInteriorZombies(dt){
 if(!interior)return;
 for(const z of interiorZombies){if(z.dead){z.deathTimer=Math.max(0,z.deathTimer-dt);continue;}z.attack=Math.max(0,z.attack-dt);
  const dx=player.x-z.x,dy=player.y-z.y,d=Math.hypot(dx,dy);
  if(d<650){const sp=z.type==='runner'?118:z.type==='stalker'?92:64; if(d>32){z.x+=dx/Math.max(d,1)*sp*dt;z.y+=dy/Math.max(d,1)*sp*dt;}else if(z.attack<=0){damagePlayer(z.type==='stalker'?15:z.type==='runner'?13:10);z.attack=z.type==='runner'?.55:.9;horror.shake=10;}}
  z.x=clamp(z.x,60,1340);z.y=clamp(z.y,105,650);
 }
}
function damageInteriorZombie(){
 let best=null,bd=72;
 for(const z of interiorZombies){if(z.dead)continue;const d=Math.hypot(z.x-player.x,z.y-player.y);if(d<bd){bd=d;best=z;}}
 if(!best)return false;best.hp-=34;best.hit=.16;if(best.hp<=0){best.dead=true;best.deathTimer=.65;state.sanity=Math.max(0,state.sanity-1);spawnDust();}else{state.sanity=Math.max(0,state.sanity-.4);}return true;
}

function updateInput(){inputState.left=keys.has('a')||keys.has('A')||keys.has('ArrowLeft')||touch.left;inputState.right=keys.has('d')||keys.has('D')||keys.has('ArrowRight')||touch.right;inputState.run=keys.has('Shift')||touch.run;inputState.jump=keys.has('w')||keys.has('W')||keys.has(' ')||keys.has('ArrowUp')||touch.jump;if(inputState.jump){if(player.jumpBuffer<=0)player.jumpBuffer=.14;}else player.jumpBuffer=0;}
function tryJump(){if(scene!=='play')return;if(player.onGround||player.coyote>0){player.vy=-640;player.onGround=false;player.coyote=0;player.jumps=1;player.air=0;soundJump();spawnDust();return;}if(player.jumps>0){player.vy=-580;player.jumps=0;player.air=0;soundJump();spawnDust();}}
function movementStep(dt){
 if(scene!=='play'||fadeBusy)return;
 if(interior&&interior.topDown){
  if(interior.stairCooldown>0)interior.stairCooldown=Math.max(0,interior.stairCooldown-dt);
  const dx=(inputState.right?1:0)-(inputState.left?1:0);
  const dy=(keys.has('s')||keys.has('S')||keys.has('ArrowDown')?1:0)-(keys.has('w')||keys.has('W')||keys.has('ArrowUp')?1:0);
  const mag=Math.hypot(dx,dy)||1; const base=inputState.run&&state.stamina>5?235:165;
  player.vx=lerp(player.vx,(dx/mag)*base,1-Math.exp(-14*dt)); player.vy=lerp(player.vy,(dy/mag)*base,1-Math.exp(-14*dt));
  player.x=clamp(player.x+player.vx*dt,45,1355); player.y=clamp(player.y+player.vy*dt,92,680);
  if(dx||dy)player.facing=dx<0?-1:dx>0?1:player.facing;
  if(inputState.run&&(dx||dy))state.stamina=Math.max(0,state.stamina-dt*24);else state.stamina=Math.min(100,state.stamina+dt*15);
  player.anim+=dt*(Math.hypot(player.vx,player.vy)/70+.4); player.recoil=Math.max(0,player.recoil-dt*8);
  if(Math.hypot(player.vx,player.vy)>55){footstepsTimer-=dt;if(footstepsTimer<=0){footstepsTimer=inputState.run?.22:.34;soundStep();}}
  updateInteriorZombies(dt); return;
 }
 if(interior&&interior.stairCooldown>0)interior.stairCooldown=Math.max(0,interior.stairCooldown-dt);
 const dir=(inputState.right?1:0)-(inputState.left?1:0);
 const base=selectedCharacter==='May'?290:selectedCharacter==='Yumi'?270:255;
 const target=dir*base*(inputState.run&&state.stamina>10?1.5:1);
 const accel=dir?12:16;
 player.vx=lerp(player.vx,target,1-Math.exp(-accel*dt));
 if(inputState.run&&dir&&Math.abs(player.vx)>220)state.stamina=Math.max(0,state.stamina-dt*18);else state.stamina=Math.min(100,state.stamina+dt*12);
 if(dir)player.facing=dir;
 if(inputState.jump&&player.jumpBuffer>0){if(player.onGround||player.coyote>0||player.jumps>0){tryJump();player.jumpBuffer=0;}}
 player.vy+=1750*dt;
 const oldGround=player.onGround;
 player.x+=player.vx*dt;
 player.y+=player.vy*dt;
 const max=chapter==='ALCATRAZ'?WORLD.ALCATRAZ:WORLD.SF;
 if(interior){player.x=clamp(player.x,80,1100);}else player.x=clamp(player.x,20,max-50);
 if(player.y+player.h>=GROUND){player.y=GROUND-player.h;player.vy=0;player.onGround=true;if(!oldGround){player.landTimer=.22;soundLand();spawnDust();}player.coyote=.12;player.jumps=2;}else{player.onGround=false;player.coyote=Math.max(0,player.coyote-dt);}
 player.anim+=dt*(Math.abs(player.vx)/80+.2);player.lean=lerp(player.lean,dir*.035,1-Math.exp(-8*dt));player.recoil=Math.max(0,player.recoil-dt*8);player.landTimer=Math.max(0,player.landTimer-dt);player.air+=dt;
 footstepsTimer-=dt;if(player.onGround&&Math.abs(player.vx)>45&&footstepsTimer<=0){footstepsTimer=inputState.run?.25:.37;soundStep();footprints.push({x:player.x,f:totalTime});if(footprints.length>80)footprints.shift();}
}
function damagePlayer(a){state.health-=a;horror.shake=8;state.sanity=Math.max(0,state.sanity-2);if(state.health<=0){state.health=0;scene='death';show('death');document.getElementById('deathText').textContent='The island kept you. This was not the last attempt.';soundScare();}}
function updateZombies(dt){
 for(const z of zombies){
  if(z.dead){z.deathTimer=Math.max(0,z.deathTimer-dt);continue;}
  z.attack=Math.max(0,z.attack-dt);z.hit=Math.max(0,z.hit-dt);z.flash=Math.max(0,z.flash-dt);
  const dx=player.x-z.x,d=Math.abs(dx);
  const vision=state.light?1050:720;
  if(d<vision){
   if(dx)z.facing=dx>0?1:-1;
   if(d<430 && Math.abs(player.vx)>120)z.alert=Math.min(1,z.alert+dt*.9);
   else z.alert=Math.max(0,z.alert-dt*.25);
   if(d>62){
    let sp=z.type==='runner'?145:z.type==='brute'?48:z.type==='stalker'?105:76;
    if(z.alert>.65)sp*=1.22;
    z.x+=Math.sign(dx)*sp*dt;
   }else if(z.attack<=0){
    damagePlayer(z.type==='brute'?18:z.type==='stalker'?12:z.type==='runner'?10:8);
    z.attack=z.type==='runner'?.62:z.type==='stalker'?.82:1.08;
    if(z.type==='stalker'){horror.glitch=.55;showWarning('THE STALKER IS TOO CLOSE',.45);}
   }
  }
  z.x=clamp(z.x,20,WORLD[chapter]-40);
 }
}
function killZombie(z,force=false){
 if(!z||z.dead)return;
 z.hp=0;z.dead=true;z.deathTimer=1.8;z.flash=.3;z.vx=0;z.alert=0;
 spawnBlood(z.x,GROUND-58);spawnBlood(z.x+(Math.random()-.5)*22,GROUND-45);horror.shake=Math.max(horror.shake,4);
 state.sanity=Math.min(100,state.sanity+2);
 tone(force?95:70,.12,'sawtooth',.16,-35);noiseBurst(.09,.09);
}
function shoot(){
 if(scene!=='play')return;
 if(state.ammo<=0){soundReload();setMessage('EMPTY MAGAZINE. R TO RELOAD.',1.1);return;}
 state.ammo--;player.recoil=.2;soundShot();horror.shake=3;
 const playerScreen=player.x-camera+19;
 let aimDir=(mouse.x-playerScreen)>=0?1:-1;
 if(Math.abs(mouse.x-playerScreen)<18)aimDir=player.facing||1;
 player.facing=aimDir;
 const maxRange=920;
 let hit=null,best=Infinity;
 for(const z of zombies){
  if(z.dead)continue;
  const dx=(z.x-player.x)*aimDir;
  if(dx<35||dx>maxRange)continue;
  const vertical=Math.abs((GROUND-55)-(GROUND-55));
  if(vertical>95)continue;
  if(dx<best){best=dx;hit=z;}
 }
 if(hit){
  const damage=selectedCharacter==='Yumi'?58:selectedCharacter==='May'?48:50;
  hit.hp-=damage;hit.hit=.18;hit.flash=.14;hit.alert=1;spawnBlood(hit.x,GROUND-55);horror.shake=5;
  setMessage(hit.hp>0?`HIT — ${Math.max(0,Math.ceil(hit.hp))} HP REMAINING`:'INFECTED DOWN',.45);
  if(hit.hp<=0)killZombie(hit);
 }else{spawnSpark(player.x+aimDir*420,GROUND-54);}
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
 horror.shake=struck?7:3;tone(struck?110:85,.08,'square',.12,-30);
}
function reload(){if(state.reserveAmmo<=0||state.ammo>=12)return;const take=Math.min(12-state.ammo,state.reserveAmmo);state.reserveAmmo-=take;state.ammo+=take;soundReload();}
function updateWorld(dt){
 totalTime+=dt;
 if(scene==='play'){
  movementStep(dt);updateZombies(dt);updateHorror(dt);updateSmiler(dt);updateParticles(dt);updateAlcatrazProgression();if(chapter==='ALCATRAZ'&&!interior&&player.x>7000&&state.sanity<80)state.sanity=Math.max(0,state.sanity-dt*.42);if(state.finalChase&&chapter==='ALCATRAZ')state.sanity=Math.max(0,state.sanity-dt*.32);if(interior&&interior.topDown&&scene==='play'&&Math.random()<dt*.025&&state.sanity<60)triggerJumpscare('room');
 }
 updateMessage(dt);updateIntro(dt);updateFade(dt);renderHUD();
}
function updateIntro(dt){if(scene!=='intro')return;introTimer+=dt;if(introTimer>7.2)advanceIntro();}
function updateMessage(dt){if(messageTimer<=0)return;messageTimer-=dt;if(messageTimer<=0)hide('message');}
function updateFade(){if(!fadeBusy)return;}
function updateHorror(dt){horror.shake=Math.max(0,horror.shake-dt*9);horror.flash=Math.max(0,horror.flash-dt*2.7);horror.glitch=Math.max(0,horror.glitch-dt*2.5);horror.warning=Math.max(0,horror.warning-dt);const w=document.getElementById('warningText');if(w&&horror.warning<=0)w.style.opacity='0';if(scene!=='play')return;scareTimer-=dt;const danger=1-state.sanity/100;if(scareTimer<=0){scareTimer=6+Math.random()*16;if(Math.random()<.36+danger*.28){triggerJumpscare();}else if(Math.random()<.55){showWarning(Math.random()<.5?'DID YOU HEAR THAT?':'LOOK AT THE WINDOW.');soundWhisper();}}
 if(state.sanity<50&&Math.random()<dt*.012){showWarning(Math.random()<.5?'SOMEONE IS BEHIND YOU':'THE DOOR MOVED');horror.glitch=.5;soundWhisper();}
 if(cursorMoved&&totalTime-lastCursorMove>9&&Math.random()<dt*.02){showWarning('YOU MOVED THE CURSOR. I SAW IT.');cursorMoved=false;}
 if(tabAway&&Math.random()<dt*.03){showWarning('YOU LEFT THE ISLAND. SHE DID NOT.');soundWhisper();tabAway=false;}
 if(interior&&Math.random()<dt*.035){horror.blackout=.35;soundFlicker();setTimeout(()=>horror.blackout=0,220);}
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
function drawWorld(){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.filter='none';ctx.shadowBlur=0;ctx.clearRect(0,0,W,H);if(horror.shake>0)ctx.translate((Math.random()-.5)*horror.shake,(Math.random()-.5)*horror.shake);drawSky();drawDistantTerrain();drawOcean();drawGround();drawTerrainTexture();if(chapter==='ALCATRAZ'){drawIslandRoad();drawLandmarks();drawAlcatrazDetails();drawAlcatrazInfrastructure();drawStreetProps();drawSigns();drawDock();}else{drawCityRoads();drawBuildings();drawCityDetails();drawStreetProps();drawSigns();}if(!interior){drawFootprints();drawSurvivorShadows();drawSurvivors();drawZombies();drawSmiler();drawPlayerShadow();drawPlayer();drawRain();}else{drawInterior();drawInteriorZombies();drawPlayerInterior();}drawParticles();drawPixelDetailPass();extraAnimationPass();enhanceHorrorAtmosphere();drawDynamicWeather();drawLighting();drawFlashlightCone();drawHorror();drawHudWorld();ctx.restore();}
function drawPlayerInterior(){
 const x=player.x,y=player.y;ctx.save();ctx.translate(x,y);const bob=Math.sin(player.anim*7)*1.5;ctx.translate(0,bob);
 px(-17,14,34,9,'#090b0b');px(-13,-16,26,31,'#293b3b');px(-10,-27,20,14,'#b5a58d');px(-9,-38,18,12,'#252b2a');px(-17,-5,7,20,'#354a49');px(10,-5,7,20,'#354a49');px(-13,25,10,7,'#121817');px(4,25,10,7,'#121817');
 const arm=Math.sin(player.anim*5)*4;px(-22,-2+arm,6,21,'#536361');px(16,-2-arm,6,21,'#536361');
 if(state.light){ctx.globalAlpha=.08;ctx.beginPath();ctx.moveTo(player.facing*5,-15);ctx.lineTo(player.facing*230,-95);ctx.lineTo(player.facing*230,95);ctx.closePath();ctx.fillStyle='#e8dfc0';ctx.fill();ctx.globalAlpha=1;}
 ctx.restore();
}
function drawHudWorld(){if(chapter==='ALCATRAZ'&&scene==='play'&&!interior){const near=landmarkData.reduce((a,b)=>Math.abs(b.x-player.x)<Math.abs(a.x-player.x)?b:a,landmarkData[0]);const d=Math.max(10,Math.round(Math.abs(near.x-player.x)/10)*10);const dir=near.x>=player.x?'→':'←';px(460,744,480,26,'rgba(4,7,7,.72)');text(`${dir} ${near.name} • ${d} m`,700,763,10,'#e8dfc9','center');}}

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

function renderHUD(){renderMapStrip();const hp=document.getElementById('healthFill'),st=document.getElementById('staminaFill'),sa=document.getElementById('sanityFill');if(hp)hp.style.width=`${clamp(state.health/state.maxHealth*100,0,100)}%`;if(st)st.style.width=`${state.stamina}%`;if(sa)sa.style.width=`${state.sanity}%`;const hv=document.getElementById('healthValue'),sv=document.getElementById('staminaValue'),sav=document.getElementById('sanityValue'),am=document.getElementById('ammoText'),loc=document.getElementById('locationText'),th=document.getElementById('threatText');if(hv)hv.textContent=`${Math.ceil(state.health)}/${state.maxHealth}`;if(sv)sv.textContent=`${Math.ceil(state.stamina)}/100`;if(sav)sav.textContent=`${Math.ceil(state.sanity)}/100`;if(am)am.textContent=`AMMO ${state.ammo} / ${state.reserveAmmo}`;if(loc)loc.textContent=chapter==='ALCATRAZ'?(interior?`${interior.name} • FLOOR ${interior.floor||1}/${interior.floors||1}`:'ALCATRAZ ISLAND'):'SAN FRANCISCO';if(th)th.textContent=smiler.active?'THE SMILER IS HERE':state.sanity<45?'YOU FEEL WATCHED':state.sanity<70?'SOMETHING IS WRONG':'THE PRISON IS QUIET';}
function drawPrompt(){const e=document.getElementById('prompt');if(!e)return;if(scene!=='play'){e.textContent='';return;}let t='';if(interior){if(interior.topDown){if(interior.id==='cellA17'){if(!state.startKey&&Math.hypot(player.x-310,player.y-390)<100)t='E  /  USE  — SEARCH MATTRESS';else if(state.startKey&&Math.hypot(player.x-1240,player.y-390)<115)t='E  /  USE  — UNLOCK CELL DOOR';}if((Math.abs(player.x-145)<100||Math.abs(player.x-1245)<100)&&player.y>250&&player.y<520)t=`E  /  USE  — STAIRWELL • FLOOR ${interior.floor}/${interior.floors}`;if(player.x<70||player.x>1330)t='E  /  USE  — EXIT STRUCTURE';const c=nearestChest();if(c)t=`E  /  USE  — SEARCH ${c.building}`;}else if(player.x<170||player.x>1010)t='E  /  USE  — EXIT TO STREET';else{const c=nearestChest();if(c)t='E  /  USE  — OPEN CHEST';}}else if(chapter==='ALCATRAZ'){const b=nearestBuilding();if(b)t=`E  /  USE  — ENTER ${b.name}`;else if(Math.abs(player.x-16040)<260)t=state.dockPass?(state.beacon?'E  /  USE  — BOARD FERRY':'E  /  USE  — LIGHT FERRY BEACON'):'DOCK PASS REQUIRED';}else{let got=false;for(const s of survivors){if(!s.found&&Math.abs(player.x-s.x)<125){t=`E  /  USE  — TALK TO ${s.name}`;got=true;break;}}if(!got){const b=nearestBuilding();if(b)t=`E  /  USE  — ENTER ${b.name}`;else if(state.survivors>=2&&Math.abs(player.x-3200)<420)t='E  /  USE  — ENTER EMERGENCY SHELTER';}}e.textContent=t;}

function updateCamera(){const target=interior?0:clamp(player.x-W*.42,0,WORLD[chapter]-W);camera=lerp(camera,target,1-Math.exp(-7*.016));}
function tick(now){const dt=Math.min(.032,Math.max(.001,(now-last)/1000));last=now;updateInput();updateWorld(dt);updateCamera();drawWorld();drawPrompt();requestAnimationFrame(tick);}
function keyDown(e){const k=e.key;if(['ArrowLeft','ArrowRight','ArrowUp',' ','a','A','d','D','w','W','Shift','e','E','q','Q','f','F','r','R','i','I','Tab','Escape','Enter'].includes(k))e.preventDefault();keys.add(k);if(scene==='intro'&&(k==='Enter'||k===' '||k==='ArrowRight')){advanceIntro();return;}if(scene==='menu'&&(k==='Enter'||k===' ')){showOnly('characterMenu');scene='character';return;}if(scene==='play'){if(k==='e'||k==='E')useInteract();else if(k==='q'||k==='Q')melee();else if(k==='f'||k==='F'){state.light=!state.light;soundFlicker();}else if(k==='r'||k==='R')reload();else if(k==='i'||k==='I'){scene='inventory';show('inventoryUi');}else if(k==='Escape')togglePause();else if(k==='Tab'){objectivePanelOpen=!objectivePanelOpen;document.getElementById('objectivePanel').classList.toggle('open',objectivePanelOpen);}else if(k==='p'||k==='P'){show('deviceOverlay');renderDeviceInfo();}else if(k==='g'||k==='G'){if(state.grenades>0){state.grenades--;tone(75,.18,'square',.16);setMessage('GRENADE THROWN.',.8);horror.shake=5;}}}}
function keyUp(e){keys.delete(e.key);if(e.key===' '||e.key==='w'||e.key==='W'||e.key==='ArrowUp')touch.jump=false;}
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
