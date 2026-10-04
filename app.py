from flask import Flask, Response, request, jsonify

app = Flask(__name__)

GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ashes of the Dead</title>
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#020304;color:#ddd;font-family:Consolas,monospace;overflow:hidden}body{display:grid;place-items:center}.shell{position:relative;width:min(100vw,1280px);aspect-ratio:16/9;background:#050708;overflow:hidden;box-shadow:0 0 90px #000,0 0 0 1px #161c1c}canvas{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:1;image-rendering:pixelated;image-rendering:crisp-edges}.layer{position:absolute;inset:0}.hidden{display:none!important}.screen{display:grid;place-items:center;background:rgba(2,3,4,.96);z-index:50}.panel{width:min(900px,92%);padding:30px;border:1px solid #4f575a;background:linear-gradient(#0b0f11,#050708);box-shadow:0 0 80px #000;position:relative}.panel:after{content:"";position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(255,255,255,.02),rgba(255,255,255,.02) 1px,transparent 1px,transparent 5px)}h1{letter-spacing:7px;margin:0 0 10px;font-size:40px;text-align:center;color:#e5e0d6;text-shadow:3px 3px #000,0 0 30px #777,0 0 2px #fff}.subtitle{text-align:center;color:#817a75;letter-spacing:4px}.intro{text-align:center;color:#aaa;margin:20px auto;line-height:1.7;max-width:760px}.choices{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}.choices button,.panel button{font:inherit;color:#ddd;background:#111619;border:1px solid #596164;padding:12px 20px;cursor:pointer}.choices button:hover,.panel button:hover{background:#252d2d;border-color:#d7d3c8;transform:translateY(-1px)}.choices button{min-width:160px;box-shadow:inset 0 0 0 1px #1d2425,0 7px 20px rgba(0,0,0,.28)}.choices button .small{color:#7f898a}.choices button:first-child{border-color:#6e7770}.choices button:nth-child(2){border-color:#676f79}.choices button:nth-child(3){border-color:#626f69}.warning{text-align:center;color:#765e5a;font-size:11px;letter-spacing:2px;margin-top:18px}.controls{text-align:center;color:#707879;font-size:11px;line-height:1.8;margin-top:16px}.hud{z-index:10;pointer-events:none;text-shadow:2px 2px #000}.top{position:absolute;left:16px;right:16px;top:14px;display:flex;justify-content:space-between;font-size:12px}.bars{width:210px}.bar{height:8px;background:#101314;border:1px solid #555;margin:3px 0 7px}.fill{height:100%}.health{background:#a94b47}.stamina{background:#879477}.sanity{background:#6e688f}.objective{position:absolute;left:18px;top:108px;max-width:500px;color:#ddd;font-size:12px;text-shadow:2px 2px #000}.objectiveTab{position:absolute;right:18px;top:96px;z-index:24;pointer-events:auto;font:700 11px Consolas,monospace;letter-spacing:2px;color:#e4e1d8;background:rgba(9,12,12,.9);border:1px solid #69716e;padding:9px 11px;cursor:pointer;box-shadow:0 4px 16px #000}.objectiveTab:hover{background:#202623;border-color:#a7afaa}.objectiveTab span{display:inline-block;margin-left:5px;color:#8c9791;font-size:14px}.objectivePanel{position:absolute;right:18px;top:136px;z-index:26;width:min(420px,44%);max-height:58%;display:none;overflow:auto;pointer-events:auto;background:rgba(5,7,7,.96);border:1px solid #646c68;box-shadow:0 18px 45px #000,0 0 0 1px #171c1a}.objectivePanel.open{display:block}.objectivePanelHead{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:13px 14px;border-bottom:1px solid #2a302e}.objectivePanelTitle{font-size:15px;letter-spacing:3px;color:#eee9df}.objectivePanelSub{font-size:9px;letter-spacing:1px;color:#717b76;margin-top:4px}.objectiveClose{font:inherit;color:#cfcfc8;background:#131816;border:1px solid #535b57;width:30px;height:30px;cursor:pointer}.objectiveList{padding:10px}.objectiveItem{display:grid;grid-template-columns:22px 1fr;gap:8px;padding:10px;border:1px solid #222927;background:#0b0f0e;margin-bottom:7px;color:#9ba39e;font-size:11px;line-height:1.45}.objectiveItem.current{border-color:#78827c;color:#e4e6e2;box-shadow:inset 3px 0 #9ba69f}.objectiveItem.done{color:#68716c;background:#090c0b}.objectiveMark{font-size:13px;text-align:center;color:#7d8781}.objectiveItem.current .objectiveMark{color:#ddd5c7}.objectiveItem.done .objectiveMark{color:#6f8a75}.message{position:absolute;left:50%;bottom:50px;transform:translateX(-50%);padding:9px 15px;background:rgba(3,4,5,.86);border:1px solid #444b4e;color:#ddd}.prompt{position:absolute;left:50%;bottom:20px;transform:translateX(-50%);color:#c8c4bd}.inventory{position:absolute;right:18px;top:105px;width:245px;background:rgba(3,4,5,.92);border:1px solid #50585b;padding:12px;font-size:12px}.vignette{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 36%,rgba(0,0,0,.82) 100%);mix-blend-mode:multiply}.warningText{position:absolute;top:24%;left:50%;transform:translateX(-50%);color:#c5b7ad;font-size:20px;letter-spacing:5px;text-shadow:0 0 15px #000,3px 3px #000}.gadget{z-index:40;background:rgba(2,3,4,.97);padding:30px}.gadgetBox{width:min(900px,94%);margin:auto;border:2px solid #555e62;background:#080c0e;padding:22px;box-shadow:0 0 70px #000}.gadgetGrid{display:grid;grid-template-columns:1fr 1fr;gap:9px;font-size:13px;line-height:1.6}.gadgetBox button{font:inherit;color:#ddd;background:#121719;border:1px solid #596164;padding:6px 10px;cursor:pointer}.gadgetTitle{font-size:23px;letter-spacing:4px}.infoFlash{z-index:65;background:rgba(0,0,0,.88);display:grid;place-items:center}.infoFlashBox{width:min(760px,90%);padding:26px;border:2px solid #8b3434;background:linear-gradient(#120b0c,#050607);box-shadow:0 0 90px #000,0 0 35px rgba(150,30,30,.35);text-align:left}.infoFlashTitle{font-size:25px;letter-spacing:5px;color:#d6c9c0;text-align:center;margin-bottom:18px}.infoFlashGrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:14px;line-height:1.55}.infoFlashGrid div{border-bottom:1px solid #292123;padding:7px}.infoFlashGrid b{color:#a84b49}.infoFlashClose{text-align:center;margin-top:18px;color:#777;font-size:11px;letter-spacing:2px}.cutscene{z-index:60;display:grid;place-items:center;background:radial-gradient(circle at 50% 55%,#121719 0,#020304 62%,#000 100%);overflow:hidden}.cutscene:before,.cutscene:after{content:'';position:absolute;left:0;right:0;height:74px;background:#000;z-index:1}.cutscene:before{top:0}.cutscene:after{bottom:0}.cutline{position:relative;z-index:2;text-align:center;max-width:930px;padding:30px;font-size:28px;line-height:1.5;text-shadow:4px 4px #000,0 0 18px #000;color:#ddd8ce}.cutline:after{content:'ENTER / SPACE';display:block;margin-top:22px;font-size:10px;letter-spacing:3px;color:#666d6c}.ending{z-index:70}.death{z-index:70;background:#080203}.small{font-size:11px;color:#777}.center{text-align:center}.red{color:#9c4643}.blood{color:#8e3837}
#privacyGate{position:fixed;inset:0;z-index:10000;display:flex;align-items:center;justify-content:center;padding:22px;background:rgba(0,0,0,.96);backdrop-filter:blur(8px)}#privacyGate .privacyBox{width:min(900px,96vw);max-height:90vh;overflow:auto;border:2px solid #68736d;background:linear-gradient(180deg,#101512,#070908);box-shadow:0 0 0 1px #202622,0 25px 90px #000;padding:26px;color:#d9dfdb}#privacyGate h1{margin:0 0 8px;font-size:26px;letter-spacing:2px;color:#f1f3f1}#privacyGate .privacyLead{color:#aab4ae;line-height:1.5}#privacyGate .privacyGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:16px 0}#privacyGate .privacyCard{border:1px solid #303934;background:#0b0f0d;padding:12px;line-height:1.45}#privacyGate .privacyCard b{display:block;color:#e6ebe8;margin-bottom:5px}#privacyGate .privacyNotice{border-left:3px solid #9da8a2;background:#0b0f0d;padding:11px 13px;color:#9da7a1;line-height:1.5}#privacyGate button,#privacyDashboard button{font:inherit;color:#eef1ef;background:#151b18;border:1px solid #68736d;padding:10px 15px;cursor:pointer}#privacyGate button:hover,#privacyDashboard button:hover{background:#252d29}#privacyDashboard{position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;padding:22px;background:rgba(0,0,0,.8);backdrop-filter:blur(5px)}#privacyDashboard .dashBox{width:min(1080px,96vw);max-height:90vh;overflow:auto;background:#090c0b;border:2px solid #59635e;box-shadow:0 25px 90px #000;padding:22px}#privacyDashboard .dashTop{display:flex;justify-content:space-between;align-items:center;gap:15px;border-bottom:1px solid #303633;padding-bottom:12px;margin-bottom:15px}#privacyDashboard h2{margin:0;font-size:23px;letter-spacing:1.5px}#privacyDashboard .dashSub{color:#89938d;font-size:12px;margin-top:4px}#privacyDashboard .dashGrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}#privacyDashboard .dashCard{border:1px solid #2d3531;background:#0d1110;padding:12px;min-height:68px}#privacyDashboard .dashLabel{font-size:10px;letter-spacing:1px;color:#78837d;text-transform:uppercase}#privacyDashboard .dashValue{font-size:14px;color:#dce2de;margin-top:7px;word-break:break-word}#privacyDashboard .dashBar{height:6px;background:#1a211e;margin-top:8px;overflow:hidden}#privacyDashboard .dashBar i{display:block;height:100%;background:#9ba69f}@media(max-width:760px){#privacyGate .privacyGrid,#privacyDashboard .dashGrid{grid-template-columns:1fr}}

.modePicker{z-index:55;display:grid;place-items:center;background:rgba(0,0,0,.86);backdrop-filter:blur(5px)}.modeBox{width:min(680px,92%);border:2px solid #525b58;background:#080b0d;padding:25px;text-align:center;box-shadow:0 0 80px #000}.modeTitle{font-size:23px;letter-spacing:4px;color:#e6e2da}.modeSub{color:#818a87;margin:10px 0 20px}.modeBtns{display:flex;justify-content:center;flex-wrap:wrap;gap:10px}.modeBtns button{font:inherit;color:#ddd;background:#121719;border:1px solid #606969;padding:13px 18px;cursor:pointer;min-width:180px}.modeBtns button:hover{background:#27302f;border-color:#ddd}.modeHint{font-size:11px;color:#707a77;margin-top:15px;line-height:1.6}.mobileControls{position:absolute;inset:auto 0 0 0;height:210px;z-index:25;pointer-events:none;display:flex;justify-content:space-between;align-items:flex-end;padding:14px;gap:12px;background:linear-gradient(transparent,rgba(0,0,0,.45))}.mobileMove,.mobileActions{display:flex;flex-wrap:wrap;gap:8px;pointer-events:auto}.mobileMove{width:45%;align-items:flex-end}.mobileActions{width:50%;justify-content:flex-end}.mobileControls button{font:700 11px Consolas,monospace;min-width:58px;height:50px;color:#e7e5de;background:rgba(10,13,14,.72);border:1px solid #68706d;box-shadow:0 3px 12px #000}.mobileControls button:active{transform:scale(.96);background:#343b38}.mobileMove button{min-width:72px;height:62px;font-size:18px}.mobileMove button[data-key="shift"]{font-size:10px}@media(max-width:760px){.shell{width:100vw;aspect-ratio:auto;height:100vh}.mobileControls{height:195px}.hud .top{font-size:10px}.bars{width:150px}.objective{top:90px;max-width:55%;font-size:10px}.prompt{bottom:205px}.message{bottom:185px;max-width:88%;font-size:11px}.inventory{right:8px;top:86px;width:190px;font-size:11px}.warningText{font-size:14px}}


.chestUI{position:absolute;inset:0;z-index:95;display:none;place-items:center;background:rgba(0,0,0,.72);backdrop-filter:blur(4px)}
.chestPanel{width:min(980px,94%);max-height:92%;overflow:auto;border:2px solid #6b716d;background:linear-gradient(#111512,#090b0a);box-shadow:0 20px 80px #000;padding:18px;color:#e4e3dc}
.chestHeader{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #343a36;padding-bottom:10px;margin-bottom:14px;gap:12px}.chestTitle{font-size:22px;letter-spacing:3px}.chestHint{font-size:10px;color:#737b76}.chestSections{display:grid;grid-template-columns:1fr 1fr;gap:16px}.chestSection{border:1px solid #343a36;background:#0b0e0d;padding:12px}.slotGrid{display:grid;grid-template-columns:repeat(9,1fr);gap:5px}.slot{aspect-ratio:1;border:1px solid #4a504d;background:#171b19;display:flex;align-items:center;justify-content:center;position:relative;cursor:pointer;min-width:0;box-shadow:inset 0 0 0 1px #090b0a}.slot:hover{background:#29302c;border-color:#8d958f}.slot.empty{opacity:.72}.slotIcon{font-size:16px;line-height:1}.slotCount{position:absolute;right:3px;bottom:1px;font-size:10px;color:#f0eee6;text-shadow:2px 2px #000}.slotName{position:absolute;left:4px;bottom:3px;font-size:7px;color:#a9b0ab;pointer-events:none}.chestActions{display:flex;gap:8px;margin-top:12px}.chestActions button{font:inherit;color:#e4e5e1;background:#171c19;border:1px solid #606963;padding:8px 12px;cursor:pointer}.chestActions button:hover{background:#27302b}.chestFooter{margin-top:12px;color:#747d78;font-size:10px;line-height:1.5}.slot.rare{box-shadow:inset 0 0 0 1px #756343,0 0 8px rgba(157,128,67,.1)}
.pixelPulse{animation:pixelPulse .28s steps(3,end)}@keyframes pixelPulse{0%{transform:scale(1)}40%{transform:scale(1.03)}100%{transform:scale(1)}}
@media(max-width:760px){.chestSections{grid-template-columns:1fr}.chestPanel{padding:12px}.slotGrid{gap:4px}.slotIcon{font-size:13px}}


.objectiveSteps{margin-top:9px;padding-top:8px;border-top:1px solid #242b28;color:#858f89;font-size:10px;line-height:1.55}.objectiveSteps div{padding:3px 0}.objectiveSteps .stepNow{color:#ded9ca}.objectiveSteps .stepDone{color:#66716b;text-decoration:line-through}.objectiveHelp{margin-top:8px;color:#69736e;font-size:9px;letter-spacing:.5px}.objectiveItem.current .objectiveHelp{color:#b1b6ad} .goalFocus{display:flex;gap:6px;align-items:center;flex-wrap:wrap;padding:9px 10px;border-bottom:1px solid #252b28;background:#080b0a}.goalFocus span{font-size:9px;color:#656e69;letter-spacing:1px;margin-right:auto}.goalFocus button{font:inherit;font-size:9px;letter-spacing:1px;color:#9ca49f;background:#111615;border:1px solid #39413d;padding:6px 8px;cursor:pointer}.goalFocus button.active{color:#e8e2d5;border-color:#818b85;background:#222925}.goalFocus button:hover{background:#1a201d}.goalNote{padding:8px 10px;color:#747d78;font-size:9px;border-bottom:1px solid #1f2522}

.mainMenu{z-index:58;background:radial-gradient(circle at 50% 42%,rgba(43,47,43,.32),rgba(0,0,0,.96) 72%),linear-gradient(180deg,#060909,#020303)}
.mainMenuBox{width:min(860px,92%);padding:38px 36px 30px;border:1px solid #68716d;background:linear-gradient(180deg,rgba(12,16,15,.96),rgba(3,5,5,.98));box-shadow:0 0 110px #000,0 0 0 1px #161b19;position:relative;overflow:hidden}
.mainMenuBox:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 4px,rgba(255,255,255,.018) 5px),linear-gradient(90deg,rgba(255,255,255,.02),transparent 18%,transparent 82%,rgba(255,255,255,.02));pointer-events:none}
.menuLogo{position:relative;font-size:52px;letter-spacing:9px;text-align:center;color:#e7e1d7;text-shadow:4px 4px #000,0 0 22px rgba(190,186,174,.22);margin-bottom:6px}
.menuTag{position:relative;text-align:center;color:#8a928e;letter-spacing:5px;font-size:11px;margin-bottom:24px}
.menuLore{position:relative;max-width:700px;margin:0 auto 25px;text-align:center;color:#a2a8a4;font-size:12px;line-height:1.7}
.menuButtons{position:relative;display:flex;justify-content:center;flex-wrap:wrap;gap:11px}
.menuPlay{min-width:260px!important;min-height:54px;font-size:19px!important;letter-spacing:4px;padding:15px 28px!important;background:#18201d!important;border-color:#a6afa7!important;box-shadow:0 0 20px rgba(180,180,170,.08),inset 0 0 0 1px #28302c!important}
.menuButton{min-width:185px!important;min-height:48px}
.menuFooter{position:relative;text-align:center;margin-top:20px;color:#646d68;font-size:9px;letter-spacing:2px}
.menuThreat{position:relative;text-align:center;margin:15px auto 0;color:#6f4949;font-size:10px;letter-spacing:2px;min-height:14px}
.charSelectBox{width:min(920px,94%);padding:30px;border:1px solid #5d6661;background:linear-gradient(180deg,#0d1210,#050706);box-shadow:0 0 90px #000}
.charSelectTitle{font-size:25px;letter-spacing:5px;text-align:center;color:#e3dfd6}
.charSelectSub{text-align:center;color:#737c77;font-size:11px;letter-spacing:2px;margin:8px 0 22px}
.charCards{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.charCard{min-width:210px;min-height:135px!important;position:relative;overflow:hidden}
.charCard:after{content:'';position:absolute;right:9px;top:8px;width:38px;height:58px;background:linear-gradient(180deg,#c9bfa8 0 18%,#544b43 18% 46%,#25282a 46% 100%);opacity:.18;image-rendering:pixelated;pointer-events:none}
.charBack{margin-top:19px!important}
.credits{z-index:59;background:rgba(0,0,0,.94);backdrop-filter:blur(5px)}
.creditsBox{width:min(700px,92%);padding:32px;border:1px solid #606863;background:#080b0a;box-shadow:0 0 100px #000;text-align:center}
.creditsBox h2{margin:0 0 14px;font-size:29px;letter-spacing:5px;color:#e4e0d8}
.creditsBox p{color:#9ca39f;line-height:1.75;font-size:12px}
.creditsName{font-size:17px!important;color:#d5d0c4!important;letter-spacing:2px}


.competitionMenu{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.menuMoon{position:absolute;width:92px;height:92px;border-radius:50%;right:9%;top:11%;background:radial-gradient(circle at 35% 35%,#d9d8cf 0 7%,#9b9b95 9%,#545957 43%,#15191a 72%);box-shadow:0 0 48px rgba(198,200,192,.13);opacity:.48;animation:moonBreath 6s ease-in-out infinite}
.menuFog{position:absolute;left:-15%;right:-15%;height:120px;bottom:9%;background:linear-gradient(90deg,transparent,rgba(129,137,132,.06),rgba(216,220,212,.08),rgba(110,120,116,.04),transparent);filter:blur(7px);animation:fogDrift 13s linear infinite}
.menuFog.two{bottom:24%;opacity:.55;animation-duration:18s;animation-delay:-7s}
.menuScan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0 6px,rgba(255,255,255,.018) 7px,transparent 8px);mix-blend-mode:screen;opacity:.45;animation:scanShift 8s linear infinite}
.menuEyes{position:absolute;left:50%;top:23%;width:160px;height:64px;transform:translateX(-50%);opacity:.25;filter:blur(.2px);animation:eyeWatch 9s ease-in-out infinite}
.menuEyes i{position:absolute;width:5px;height:5px;background:#c9cbc4;box-shadow:0 0 9px #c9cbc4}
.menuEyes i:first-child{left:47px;top:27px}.menuEyes i:last-child{right:47px;top:27px}
.menuThreatPulse{animation:threatPulse 2.4s steps(2,end) infinite}
.menuBadge{position:absolute;left:30px;top:24px;color:#707a75;font-size:9px;letter-spacing:2px;border:1px solid #313834;background:rgba(4,6,6,.52);padding:7px 9px;opacity:.8}
.menuSignal{position:absolute;right:30px;bottom:24px;color:#555f5a;font-size:8px;letter-spacing:2px;opacity:.85}
.menuSignal b{color:#8e4b4b;font-weight:700}
.menuGlitch{animation:menuGlitch .12s steps(2,end)}
@keyframes moonBreath{0%,100%{transform:scale(1);opacity:.42}50%{transform:scale(1.04);opacity:.58}}
@keyframes fogDrift{0%{transform:translateX(-10%)}50%{transform:translateX(8%)}100%{transform:translateX(-10%)}}
@keyframes scanShift{0%{transform:translateY(0)}100%{transform:translateY(14px)}}
@keyframes eyeWatch{0%,37%,100%{opacity:.05;transform:translateX(-50%) scale(.9)}41%,45%{opacity:.75;transform:translateX(-50%) scale(1)}47%,50%{opacity:.1}53%,55%{opacity:.72}60%,92%{opacity:.05}}
@keyframes threatPulse{0%,100%{opacity:.65}50%{opacity:.2}}
@keyframes menuGlitch{0%{transform:translate(0)}33%{transform:translate(2px,-1px)}66%{transform:translate(-2px,1px)}100%{transform:translate(0)}}
.pixelHudChip{position:absolute;right:18px;top:58px;z-index:23;pointer-events:none;font:700 9px Consolas,monospace;letter-spacing:1.5px;color:#767f7a;background:rgba(4,6,6,.58);border:1px solid #2a302e;padding:5px 7px;opacity:.8}
.horrorLetterbox{position:absolute;left:0;right:0;top:0;height:0;background:#000;z-index:37;pointer-events:none;opacity:0;transition:height .18s,opacity .18s}
.horrorLetterbox.on{height:34px;opacity:.96}.horrorLetterbox.bottom{top:auto;bottom:0}
@media(max-width:760px){.menuBadge{left:12px;top:12px}.menuSignal{right:12px;bottom:12px}.menuMoon{right:5%;top:9%;width:66px;height:66px}.pixelHudChip{right:12px;top:82px}}

#aotdSoundPanel{position:absolute;left:18px;top:62px;z-index:28;pointer-events:auto;font:700 9px Consolas,monospace;letter-spacing:1.5px;color:#aeb6b1;background:rgba(6,9,9,.76);border:1px solid #3d4542;padding:6px 8px;cursor:pointer;box-shadow:0 3px 12px #000}#aotdSoundPanel b{color:#d6d0c5}#aotdSoundPanel.off{color:#7d8581}#modePicker .modeBtns button.active{background:#27302d;border-color:#b8c0bb;box-shadow:0 0 0 1px #4f5853,inset 0 0 14px rgba(200,200,190,.06)}#modePicker .soundChoice{margin-top:12px;border-top:1px solid #252b29;padding-top:12px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap}.soundChoice button{font:inherit;color:#d7dbd8;background:#101514;border:1px solid #4e5753;padding:8px 12px;cursor:pointer;min-width:120px}.soundChoice button.active{border-color:#b3bbb5;background:#242c29}


.mainMenu{background:radial-gradient(circle at 50% 34%,rgba(70,74,71,.18),transparent 28%),radial-gradient(circle at 82% 18%,rgba(126,132,126,.07),transparent 16%),linear-gradient(180deg,#030507 0%,#05080a 47%,#080b0d 100%);overflow:hidden}
.mainMenu:before{content:"";position:absolute;inset:0;background:linear-gradient(rgba(210,210,200,.025) 50%,transparent 50%),repeating-linear-gradient(90deg,rgba(255,255,255,.018) 0 1px,transparent 1px 7px);background-size:100% 6px,7px 100%;opacity:.35;mix-blend-mode:screen;pointer-events:none;animation:menuScan 7s linear infinite}
.mainMenu:after{content:"";position:absolute;inset:auto 0 0;height:46%;background:linear-gradient(180deg,transparent,rgba(0,0,0,.18) 18%,rgba(0,0,0,.82) 100%),linear-gradient(90deg,transparent 0 8%,rgba(24,30,31,.7) 8% 12%,transparent 12% 23%,rgba(19,25,27,.68) 23% 31%,transparent 31% 43%,rgba(24,29,30,.8) 43% 49%,transparent 49% 62%,rgba(17,23,25,.78) 62% 72%,transparent 72% 84%,rgba(22,27,28,.82) 84% 90%,transparent 90%);clip-path:polygon(0 45%,8% 37%,15% 49%,24% 30%,31% 48%,40% 41%,49% 20%,59% 48%,68% 34%,77% 45%,86% 26%,94% 44%,100% 33%,100% 100%,0 100%);opacity:.72;pointer-events:none}
.mainMenuBox{position:relative;z-index:3;width:min(880px,92%);padding:40px 42px 34px;border:1px solid #58605f;background:linear-gradient(180deg,rgba(9,13,15,.95),rgba(5,8,9,.91));box-shadow:0 30px 100px rgba(0,0,0,.86),0 0 0 1px rgba(255,255,255,.025);backdrop-filter:blur(4px)}
.mainMenuBox:before{content:"";position:absolute;left:18px;right:18px;top:16px;height:2px;background:linear-gradient(90deg,transparent,#6c756f 25%,#c7c2b4 50%,#6c756f 75%,transparent);opacity:.42}
.mainMenuBox:after{content:"ALCATRAZ ISLAND • 1968 • CASE FILE 17";position:absolute;right:18px;bottom:10px;color:#59615d;font:9px Consolas,monospace;letter-spacing:2px}
.menuLogo{font-size:clamp(34px,5vw,64px)!important;letter-spacing:8px!important;line-height:1!important;color:#e6e2d9!important;text-shadow:4px 4px #000,0 0 18px rgba(216,213,203,.2)!important;position:relative;display:inline-block;animation:menuFlicker 5.5s infinite}
.menuTag{margin-top:13px!important;font-size:10px!important;letter-spacing:3px!important;color:#858d89!important}
.menuLore{max-width:680px!important;margin:24px auto 26px!important;padding:16px 20px;border-top:1px solid #252b2a;border-bottom:1px solid #252b2a;color:#aeb5b1!important;line-height:1.65!important;background:rgba(0,0,0,.18)}
.menuButtons{display:grid!important;grid-template-columns:1.5fr 1fr 1fr;gap:10px!important;max-width:700px;margin:0 auto}
.menuButtons button{min-height:50px!important;letter-spacing:2px;border:1px solid #48514f!important;background:linear-gradient(180deg,#171d1c,#0d1211)!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.025),0 9px 25px rgba(0,0,0,.35)!important;transition:background .16s,border-color .16s,transform .16s,box-shadow .16s}
.menuButtons button:hover{background:linear-gradient(180deg,#242b28,#121816)!important;border-color:#9aa39d!important;transform:translateY(-2px)!important;box-shadow:0 12px 30px rgba(0,0,0,.55),inset 0 0 0 1px rgba(255,255,255,.04)!important}
.menuPlay{font-size:16px!important;color:#e9e6dc!important;border-color:#737b75!important;position:relative;overflow:hidden}
.menuPlay:after{content:"";position:absolute;left:-35%;top:0;width:30%;height:100%;background:linear-gradient(90deg,transparent,rgba(235,235,224,.12),transparent);animation:menuSweep 4.5s ease-in-out infinite}
.menuThreat{margin-top:24px!important;color:#8d4142!important;font-size:10px!important;letter-spacing:3px!important;animation:threatPulse 2.4s ease-in-out infinite}
.menuFooter{margin-top:15px!important;color:#5f6763!important;font-size:9px!important;letter-spacing:2px!important}
@media(max-width:780px){.menuButtons{grid-template-columns:1fr}.mainMenuBox{padding:28px 20px 30px}.menuLogo{letter-spacing:5px!important}.menuLore{font-size:12px}}
@keyframes menuScan{0%{background-position:0 0,0 0}100%{background-position:0 100%,140px 0}}
@keyframes menuFlicker{0%,93%,100%{opacity:1}94%{opacity:.72}95%{opacity:1}97%{opacity:.86}98%{opacity:1}}
@keyframes menuSweep{0%,70%{left:-35%}92%,100%{left:115%}}
@keyframes threatPulse{0%,100%{opacity:.5}50%{opacity:1}}


<style id="competitionUpgradeStyle">
.roomTransitionScreen{position:absolute;inset:0;z-index:75;pointer-events:none;background:#000;opacity:0;display:block;transition:opacity .42s ease}
.roomTransitionScreen.on{opacity:1}
.controlChoiceFix{position:absolute;inset:0;z-index:90;display:grid;place-items:center;background:rgba(0,0,0,.92);backdrop-filter:blur(8px)}
.controlChoiceBox{width:min(720px,92%);padding:30px;border:1px solid #66716c;background:linear-gradient(180deg,#0b100f,#030506);box-shadow:0 25px 100px #000;text-align:center}
.controlChoiceBox h2{margin:0 0 10px;color:#e9e6dd;letter-spacing:4px;font-size:25px}
.controlChoiceBox p{color:#8b958f;font-size:11px;line-height:1.7;margin:0 auto 20px;max-width:560px}
.controlChoiceGrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.controlChoiceGrid button{min-height:105px;font:700 13px Consolas,monospace;letter-spacing:2px;color:#e8e5dc;background:#111716;border:1px solid #4f5955;cursor:pointer;box-shadow:inset 0 0 0 1px rgba(255,255,255,.025),0 12px 25px rgba(0,0,0,.3)}
.controlChoiceGrid button:hover,.controlChoiceGrid button.selected{background:#222925;border-color:#c2c7c0;box-shadow:inset 0 0 22px rgba(205,205,195,.08),0 12px 28px rgba(0,0,0,.45)}
.controlChoiceGrid small{display:block;margin-top:9px;color:#7f8984;font-size:9px;letter-spacing:1px;font-weight:400}
.controlChoiceFoot{margin-top:15px;color:#666f6a;font-size:10px;letter-spacing:1px}
.medicalPassMarker{position:absolute;z-index:27;display:none;pointer-events:none;color:#e0d2a0;font:700 10px Consolas,monospace;letter-spacing:2px;text-shadow:2px 2px #000;background:rgba(8,10,10,.72);border:1px solid #575349;padding:7px 9px}
.roomTransitionLabel{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:76;color:#ded9cf;font:700 12px Consolas,monospace;letter-spacing:4px;text-shadow:0 0 18px #fff}
@media(max-width:760px){.controlChoiceGrid{grid-template-columns:1fr}.controlChoiceBox{padding:20px}}

#aotdExitPrompt{position:absolute;left:50%;bottom:78px;transform:translateX(-50%);z-index:29;display:none;pointer-events:none;padding:9px 14px;border:1px solid #777f7b;background:rgba(5,7,7,.92);color:#e7e3d8;font:700 11px Consolas,monospace;letter-spacing:1.5px;text-shadow:2px 2px #000;box-shadow:0 8px 22px #000}#aotdExitPrompt.show{display:block}

.charCard{color:#f4efe2!important;text-align:left!important;text-shadow:2px 2px #000,0 0 5px rgba(0,0,0,.9);background:linear-gradient(160deg,#17201f,#09100f)!important;border:1px solid #69746e!important;min-height:178px!important;padding:18px 16px!important;display:flex!important;flex-direction:column!important;justify-content:flex-end!important;align-items:flex-start!important;position:relative!important;overflow:hidden!important}
.charCard:before{content:'';position:absolute;left:50%;top:12px;transform:translateX(-50%);width:78px;height:108px;background:linear-gradient(180deg,#d7bca3 0 22%,#111516 22% 45%,#314943 45% 74%,#202527 74% 100%);border:1px solid #84908a;box-shadow:0 0 0 1px #0a0d0c,0 10px 24px rgba(0,0,0,.45);opacity:.88;image-rendering:pixelated}
.charCard[data-char="Yumi"]:before{background:linear-gradient(180deg,#d7bda5 0 20%,#17191a 20% 42%,#345047 42% 72%,#20292a 72% 100%);box-shadow:inset 18px 0 #222627,inset -18px 0 #222627,0 0 0 1px #88938e,0 10px 28px rgba(0,0,0,.5)}
.charCard[data-char="Julia"]:before{background:linear-gradient(180deg,#d7b7a0 0 20%,#3a2928 20% 43%,#3b5659 43% 72%,#222a2b 72% 100%)}
.charCard[data-char="May"]:before{background:linear-gradient(180deg,#d8baa1 0 20%,#5c4032 20% 43%,#4d5061 43% 72%,#272a31 72% 100%)}
.charCard br{display:none}
.charCard::after{display:none!important}
.charCard .small{display:block!important;color:#d4cec0!important;text-shadow:2px 2px #000,0 0 4px #000!important;font-size:10px!important;letter-spacing:1px;margin-top:4px}
.charCard[data-char="Yumi"]{border-color:#80998e!important}
.charCard[data-char="Yumi"]::marker{display:none}
.charSelectBox{background:radial-gradient(circle at 50% 12%,rgba(80,94,88,.16),transparent 32%),linear-gradient(180deg,#0b110f,#030706)!important;border-color:#69746e!important;box-shadow:0 20px 90px rgba(0,0,0,.82),inset 0 0 90px rgba(170,184,174,.035)!important}


#aotdVisibilityFix{display:none}
.vignette{background:radial-gradient(ellipse at center,transparent 64%,rgba(0,0,0,.10) 100%)!important}
.charCard:after{display:none!important}
.charCard{background:linear-gradient(180deg,#141c1e,#0b1113)!important}
.mainMenuBox{z-index:20!important}
</style>
</style>
<style id="visualUpgradeStyle">
.charCard{background:linear-gradient(180deg,#101719,#070a0b)!important;border-color:#56605e!important;transition:transform .2s ease,box-shadow .2s ease,background .2s ease}.charCard:hover{transform:translateY(-4px)!important;box-shadow:0 12px 28px rgba(0,0,0,.48),inset 0 0 0 1px #8b938d}.charCard.selected{background:linear-gradient(180deg,#1a2222,#0b1010)!important;box-shadow:0 0 0 1px #a7afa8,0 0 24px rgba(180,190,181,.12)}.mainMenuBox{background:linear-gradient(180deg,rgba(7,10,11,.96),rgba(2,4,5,.98))!important;border:1px solid #4f5958!important;box-shadow:0 22px 80px rgba(0,0,0,.75),inset 0 0 70px rgba(130,140,135,.025)!important}.menuLogo{letter-spacing:10px!important;text-shadow:4px 4px #000,0 0 22px rgba(220,220,210,.18)!important}.menuThreat{animation:aotdThreatPulse 2.8s ease-in-out infinite}.menuLore{max-width:760px!important}.controlChoiceGrid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:12px!important}.controlChoiceGrid button{min-height:86px!important}.controlChoiceGrid button.selected{border-color:#d0c8b4!important;background:#222926!important;box-shadow:inset 0 0 0 2px #777d77,0 0 22px rgba(205,200,185,.08)!important}.roomTransitionLabel{letter-spacing:5px!important}.objectivePanel{backdrop-filter:blur(7px)}
@keyframes aotdThreatPulse{0%,100%{opacity:.58}50%{opacity:1;text-shadow:0 0 12px rgba(190,30,34,.32)}}
#aotdWorldLabel{position:absolute;left:18px;top:152px;z-index:14;pointer-events:none;color:#b8b3a7;font:700 10px Consolas,monospace;letter-spacing:2px;text-shadow:2px 2px #000;opacity:.7}
#aotdSceneFX{position:absolute;inset:0;pointer-events:none;z-index:13}
</style><style id="finalCharacterSelectionFix">
.charCards .charCard::before,.charCards .charCard:before{display:none!important;content:none!important;background:none!important;box-shadow:none!important}
.charCards .charCard{min-height:154px!important;padding:22px!important;display:flex!important;justify-content:center!important;align-items:center!important;text-align:center!important;background:linear-gradient(160deg,#141b1b,#080b0c)!important;border:1px solid #69736d!important;box-shadow:inset 0 0 24px rgba(180,190,180,.035),0 10px 28px rgba(0,0,0,.45)!important}
.charCards .charCard:hover{transform:translateY(-3px)!important;border-color:#c7c1af!important}
.charCards .charCard .charName{color:#fff7e6!important;font:900 25px Consolas,monospace!important;letter-spacing:5px!important;text-shadow:3px 3px #000,0 0 9px #000!important}
.charCards .charCard .charMeta{color:#cfd5d0!important;font:700 10px Consolas,monospace!important;letter-spacing:1px!important;line-height:1.5!important;text-shadow:2px 2px #000!important}
.charCards .charCard[data-char="Yumi"]{border-color:#87a095!important;background:linear-gradient(160deg,#17211e,#080c0b)!important}
.charCards .charCard[data-char="Yumi"] .charName{color:#eef8ee!important}
</style>
</head>
<body>
<div id="privacyGate"><div class="privacyBox"><h1>NIGHTWATCH SECURITY TERMINAL</h1><p class="privacyLead">ASHES OF THE DEAD — DEVICE INFORMATION NOTICE</p><div class="privacyGrid"><div class="privacyCard"><b>WHAT MAY BE DISPLAYED</b>Browser and platform details, screen size, language, timezone, online state, network hints, CPU thread count, touch support, cookies state, referrer, battery information when available, and the network address seen by the game server.</div><div class="privacyCard"><b>WHAT IS NOT READ</b>The game does not read passwords, personal files, photos, contacts, saved documents, account contents, or arbitrary data from your computer.</div><div class="privacyCard"><b>PERMISSIONS</b>Location, camera, and microphone information require separate browser permission.</div><div class="privacyCard"><b>FICTIONAL SURVEILLANCE</b>CCTV alerts, tracking messages, The Smiler observations, and horror-terminal events are fictional game elements unless explicitly identified as browser/server information.</div></div><div class="privacyNotice">The server can only see the network address that reaches it. A proxy, VPN, carrier network, or hosting layer can change the address shown. This is an entertainment game, not a security or diagnostic product.</div><div style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap"><button id="privacyAccept">ENTER ASHES OF THE DEAD</button><button id="privacyDetails">VIEW DEVICE PANEL</button></div></div></div><div id="privacyDashboard"><div class="dashBox"><div class="dashTop"><div><h2>NIGHTWATCH / PERSONAL DEVICE RECORD</h2><div class="dashSub">Press P to open or close this record</div></div><button id="privacyClose">CLOSE</button></div><div id="dashGrid" class="dashGrid"></div><div style="margin-top:14px;color:#7f8983;font-size:11px;line-height:1.5">Browser-exposed values can be unavailable or approximate. Location, camera, and microphone require permission. The server-seen address may be a proxy address. No passwords, personal files, photos, contacts, or account contents are read by this game.</div></div></div>

<div id="mainMenu" class="layer screen mainMenu"><div class="mainMenuBox"><div class="menuLogo">ASHES OF THE DEAD</div><div class="menuTag">SCREAM JAM 2026 • THE ALCATRAZ ESCAPE</div><div class="menuLore">A detective wakes alone inside Cell A-17. The island is quiet. The rain is not. Find the docks. Escape the island. Then find the people who are still alive.</div><div class="menuButtons"><button id="mainMenuPlay" class="menuPlay">PLAY</button><button id="mainMenuCredits" class="menuButton">CREDITS</button><button id="mainMenuControls" class="menuButton">CONTROL MODE</button></div><div class="menuThreat">DO NOT STAY IN ONE PLACE TOO LONG.</div><div class="menuFooter">JULIA • MAY • YUMI • FEMALE DETECTIVES • ALCATRAZ → SAN FRANCISCO • MADE WITH GRATITUDE</div></div></div><div id="credits" class="layer credits hidden"><div class="creditsBox"><h2>CREDITS</h2><p class="creditsName">Mayumi Alingarog (Yumi, Mimi, Yumimi)</p><p>With heartfelt thanks to Mayumi Alingarog (Yumi, Mimi, Yumimi), a wonderful classmate and fellow developer whose kindness, patience, creativity, helpful nature, and respectful spirit made a lasting difference and inspired me to take the leap into <b>Scream Jam 2026</b>. Her encouragement and love for building things helped turn this little idea into a game I could proudly share.</p><p>Ashes of the Dead is an original horror game experience built for the jam.</p><button id="creditsBack">BACK</button></div></div>
<div id="modePicker" class="modePicker layer hidden">
<div class="modeBox">
<div class="modeTitle">CONTROL PROFILE</div>
<div class="modeSub">Choose the way you want to survive.</div>
<div class="modeBtns"><button data-mode="laptop">LAPTOP / DESKTOP</button><button data-mode="mobile">MOBILE / TOUCH</button><button id="modeAuto">AUTO DETECT</button></div>
<div class="modeHint">Laptop: keyboard + mouse. Mobile: virtual controls + touch shooting.</div>
<div class="soundChoice"><button id="soundOn" type="button">SOUND ON</button><button id="soundOff" type="button">SOUND OFF</button></div>

</div>
</div>

<button id="aotdSoundPanel" type="button" aria-pressed="true">SOUND: <b>ON</b></button>

<div id="aotdExitPrompt">E — EXIT TO STREET</div><div id="mobileControls" class="mobileControls hidden">
<div class="mobileMove"><button data-key="a">◀</button><button data-key="d">▶</button><button data-key="shift">RUN</button></div>
<div class="mobileActions"><button data-key="w">JUMP</button><button data-action="e">USE</button><button data-action="q">MELEE</button><button data-action="f">LIGHT</button><button data-action="g">GRENADE</button><button data-action="h">HEAL</button><button data-action="i">BAG</button><button data-action="r">RELOAD</button><button data-action="shoot">FIRE</button></div>
</div>
<div id="aotdWorldLabel"></div><div id="aotdSceneFX"></div><div class="shell">
<canvas id="game" width="1280" height="720"></canvas>
<div id="menu" class="layer screen hidden">
<div class="charSelectBox">
<div class="charSelectTitle">CHOOSE YOUR DETECTIVE</div><div class="charSelectSub">All three are female detectives. Their skills and look differ, but the story can be completed with any of them.</div>
<div class="intro">Rain hits the island. Your cell is open. The prison is empty, but the walls are covered in warnings. Search the cell blocks, survive the island, discover what happened, and escape to San Francisco.</div>
<div class="charCards"><button class="charCard" data-char="Julia">JULIA<br><span class="small">FEMALE DETECTIVE • FIELD FILES</span></button><button class="charCard" data-char="May">MAY<br><span class="small">FEMALE DETECTIVE • CRIME SCENE</span></button><button class="charCard" data-char="Yumi">YUMI<br><span class="small">FEMALE DETECTIVE • INTELLIGENCE</span></button></div><div class="center"><button id="charBack">BACK TO MAIN MENU</button></div>
<div class="warning">HEADPHONES RECOMMENDED • THE QUIET PART IS IMPORTANT</div><div class="center" style="margin-top:12px"><button id="privacyReopen">PRIVACY / DEVICE NOTICE</button><button id="controlModeOpen">CONTROL MODE</button></div>
<div class="controls">A/D OR ARROWS MOVE • SHIFT RUN • W/SPACE JUMP • E INTERACT • I INVENTORY • TAB GADGET • P PERSONAL INFO<br>F FLASHLIGHT • Q MELEE • G GRENADE • R RELOAD • MOUSE SHOOT • ESC PAUSE</div>
</div>
</div>
<div id="cutscene" class="layer cutscene hidden"><div id="cutline" class="cutline"></div></div>
<div id="pause" class="layer screen hidden"><div class="panel"><h1>PAUSED</h1><p class="center">The rain is still falling outside.</p><div class="center"><button id="resume">RESUME</button><button id="restart">RESTART CHAPTER</button><button id="backMenu">MAIN MENU</button></div></div></div>
<div id="ending" class="layer screen hidden"><div class="panel"><h1>YOU SURVIVED</h1><p id="endingText" class="intro"></p><div class="center"><button id="endingMenu">RETURN TO MENU</button></div></div></div>
<div id="death" class="layer screen hidden"><div class="panel"><h1 class="red">THE DARKNESS FOUND YOU</h1><p id="deathText" class="intro"></p><div class="center"><button id="deathRestart">RESTART</button><button id="deathMenu">MAIN MENU</button></div></div></div>

<div id="chestUI" class="chestUI">
 <div id="chestPanel" class="chestPanel">
  <div class="chestHeader"><div><div id="chestTitle" class="chestTitle">SUPPLY CHEST</div><div class="chestHint">CLICK AN ITEM TO TAKE IT • TAKE ALL TRANSFERS EVERYTHING</div></div><button id="chestClose">CLOSE</button></div>
  <div class="chestSections">
   <div class="chestSection"><div class="small" style="margin-bottom:8px">CHEST STORAGE</div><div id="chestSlots" class="slotGrid"></div></div>
   <div class="chestSection"><div class="small" style="margin-bottom:8px">PLAYER INVENTORY</div><div id="playerSlots" class="slotGrid"></div></div>
  </div>
  <div class="chestActions"><button id="takeAllChest">TAKE ALL</button><button id="sortChest">SORT</button></div>
  <div id="chestFooter" class="chestFooter"></div>
 </div>
</div>

<div id="hud" class="layer hud hidden">
<div class="top"><div class="bars"><div>HEALTH <span id="healthText"></span></div><div class="bar"><div id="healthFill" class="fill health"></div></div><div>STAMINA <span id="staminaText"></span></div><div class="bar"><div id="staminaFill" class="fill stamina"></div></div><div>SANITY <span id="sanityText"></span></div><div class="bar"><div id="sanityFill" class="fill sanity"></div></div></div><div class="center"><div id="locationText">ALCATRAZ</div><div id="threatText">THE PRISON IS QUIET</div><div id="ammoText">AMMO 12 / 12</div></div></div>
<button id="objectiveTab" class="objectiveTab">OBJECTIVES <span>+</span></button><div id="objectivePanel" class="objectivePanel" aria-hidden="true"><div class="objectivePanelHead"><div><div class="objectivePanelTitle">OBJECTIVES</div><div id="objectivePanelSub" class="objectivePanelSub">CURRENT MISSION</div></div><button id="objectiveClose" class="objectiveClose">×</button></div><div id="goalFocus" class="goalFocus"><span>GOAL FOCUS</span><button data-goal="escape">ESCAPE</button><button data-goal="search">SEARCH</button><button data-goal="survivors">SURVIVORS</button></div><div id="objectiveList" class="objectiveList"></div></div><div id="objective" class="objective"></div><div id="message" class="message hidden"></div><div id="prompt" class="prompt"></div><div id="inventory" class="inventory hidden"></div><div class="vignette"></div><div id="warningText" class="warningText hidden"></div>
</div>
<div id="infoFlash" class="layer infoFlash hidden"><div class="infoFlashBox"><div class="infoFlashTitle">PERSONAL DEVICE RECORD</div><div class="infoFlashGrid"><div><b>SERVER IP</b><br><span id="flashIp">READING...</span></div><div><b>DEVICE</b><br><span id="flashDevice">READING...</span></div><div><b>BROWSER</b><br><span id="flashBrowser">READING...</span></div><div><b>SCREEN</b><br><span id="flashScreen">READING...</span></div><div><b>LANGUAGE</b><br><span id="flashLanguage">READING...</span></div><div><b>TIME ZONE</b><br><span id="flashTimezone">READING...</span></div><div><b>NETWORK</b><br><span id="flashNetwork">READING...</span></div><div><b>ONLINE</b><br><span id="flashOnline">READING...</span></div><div><b>CORES</b><br><span id="flashCores">READING...</span></div><div><b>BATTERY</b><br><span id="flashBattery">READING...</span></div><div><b>LOCATION</b><br><span id="flashLocation">NOT SHARED</span></div><div><b>TOUCH</b><br><span id="flashTouch">READING...</span></div><div><b>COOKIES</b><br><span id="flashCookies">AVAILABLE TO THIS SITE</span></div><div><b>REFERRER</b><br><span id="flashReferrer">NONE</span></div></div><div class="infoFlashClose">ESC OR ENTER TO CLOSE • THIS SCREEN USES INFORMATION AVAILABLE TO THE BROWSER OR GAME SERVER</div></div></div><div id="gadget" class="layer gadget hidden"><div class="gadgetBox"><div class="gadgetTitle">NIGHTWATCH // DEVICE PANEL</div><p class="small">Real browser information is shown only when the browser exposes it. Camera and microphone are never accessed unless you deliberately press the permission button.</p><div class="gadgetGrid"><div>SERVER-SEEN IP: <span id="gip">READING...</span></div><div>PLATFORM: <span id="gplatform">-</span></div><div>BROWSER: <span id="gbrowser">-</span></div><div>SCREEN: <span id="gscreen">-</span></div><div>LANGUAGE: <span id="glang">-</span></div><div>TIME ZONE: <span id="gtz">-</span></div><div>CPU THREADS: <span id="gcpu">-</span></div><div>NETWORK: <span id="gnet">-</span></div><div>BATTERY: <span id="gbat">-</span></div><div>ONLINE: <span id="gonline">-</span></div></div><div style="margin-top:14px">LOCATION: <span id="gloc">NOT SHARED</span> <button id="locate">SHARE LOCATION</button></div><div style="margin-top:10px">CAMERA/MIC: <span id="gperm">NOT ACCESSED</span> <button id="perm">OPTIONAL CHECK</button></div><div style="margin-top:20px;border:1px solid #333;padding:18px;color:#737b7d">P — SHOW PERSONAL DEVICE INFO • TAB TO CLOSE • THIS PANEL IS PART OF THE GAME. IT DOES NOT READ FILES, PASSWORDS, CONTACTS, OR ACCOUNTS.</div></div></div>
</div>
<script>
'use strict';

const canvas=document.getElementById('game');

const ctx=canvas.getContext('2d');

ctx.imageSmoothingEnabled=false;

const W=1280;

const H=720;

const GROUND=570;

const keys=new Set();

const inputState={left:false,right:false,down:false,run:false,jump:false};

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
'You wake inside Cell A-17. The rain is louder than the prison.',
'The cell door is shut. Something is breathing on the other side.',
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
function scareSound(){tone(72,.6,'sawtooth',.22,-45);
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
function getObjectiveData(){if(chapter==='ALCATRAZ'){return[{t:'SEARCH CELL A-17: find the key under the mattress, then unlock the door.',d:0},{t:'SEARCH CELL BLOCK A: inspect the cells and follow the blood marks.',d:1},{t:'SEARCH CELL BLOCK B: find a way toward the prison dock.',d:2},{t:'FIND THE DOCK PASS: enter the Medical Wing and search the marked supply desk.',d:3},{t:'REACH THE DOCK BEACON: use the pass and signal the ferry.',d:4},{t:'ESCAPE ALCATRAZ: board the waiting ferry.',d:5}];}return[{t:'FIND THE SURVIVORS IN SAN FRANCISCO.',d:0},{t:'FIND THE RESEARCH ANNEX ARCHIVE.',d:1},{t:'RETURN TO THE EMERGENCY SHELTER.',d:2}];}
function getCurrentObjectiveIndex(){if(chapter==='ALCATRAZ')return Math.min(objectiveStep,5);if(archiveOpened)return 2;if(survivorsFound>=3)return 1;return 0;}
function renderObjectivePanel(){const list=document.getElementById('objectiveList');const sub=document.getElementById('objectivePanelSub');if(!list||!sub)return;const data=getObjectiveData();const current=getCurrentObjectiveIndex();sub.textContent=chapter==='ALCATRAZ'?'ALCATRAZ ISLAND • CELL BLOCK A / ESCAPE ROUTE':'SAN FRANCISCO • SURVIVOR / ARCHIVE ROUTE';list.innerHTML='';data.forEach((o,i)=>{const item=document.createElement('div');item.className='objectiveItem '+(i<current?'done ':'')+(i===current?'current':'');const mark=i<current?'✓':i===current?'›':'○';item.innerHTML='<div class="objectiveMark">'+mark+'</div><div>'+o.t+'</div>';list.appendChild(item);});}
function setObjective(){const data=getObjectiveData();const current=getCurrentObjectiveIndex();const el=document.getElementById('objective');if(el)el.textContent='OBJECTIVE\n'+data[current].t;renderObjectivePanel();}
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
addWriting(2860,GROUND-205,'MEDICAL WING HAS THE DOCK PASS',.68);
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
setMsg('The Medical Wing should have the Dock Pass.',2.4);
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
function updatePlayer(dt){
if(interior){
 let dir=0;
 if(keys.has('a')||keys.has('ArrowLeft'))dir--;
 if(keys.has('d')||keys.has('ArrowRight'))dir++;
 const running=keys.has('Shift')&&state.stamina>1&&dir!==0;
 const speed=running?305:195;
 player.vx=dir*speed;
 if(dir)player.facing=dir;
 player.x=clamp(player.x+player.vx*dt,40,1210);
 player.anim+=dt*(dir?10:2.2);
 state.stamina=clamp(state.stamina+(running?-22:15)*dt,0,100);
 return;
}
let dir=0;
if(keys.has('a')||keys.has('ArrowLeft'))dir--;
if(keys.has('d')||keys.has('ArrowRight'))dir++;
const running=keys.has('Shift')&&state.stamina>1&&dir!==0;
const speed=running?315:205;
player.vx=dir*speed;
if(dir)player.facing=dir;
if(running)state.stamina=Math.max(0,state.stamina-27*dt);else state.stamina=Math.min(100,state.stamina+15*dt);
player.vy+=1150*dt;
if((keys.has('w')||keys.has(' ')||keys.has('ArrowUp'))&&player.onGround){player.vy=-455;player.onGround=false;tone(105,.08,'triangle',.025,35);}
player.x+=player.vx*dt;
player.x=clamp(player.x,0,chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH);
if(chapter==='ALCATRAZ'&&!state.startEscaped)player.x=clamp(player.x,120,300);
player.y+=player.vy*dt;
if(player.y+player.h>=GROUND){player.y=GROUND-player.h;player.vy=0;player.onGround=true;}
if(player.x<20)player.x=20;
if(player.hitTimer>0)player.hitTimer-=dt;
if(player.shootTimer>0)player.shootTimer-=dt;
player.anim+=dt*(dir?10:2.2);
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
if(interior&&Math.random()<.45){blackout=rand(1.2,2.8);
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
}
function draw(){ctx.save();
let sx=shake?(Math.random()*shake-shake/2):0;
ctx.translate(sx,0);
ctx.fillStyle='#06090b';
ctx.fillRect(0,0,W,H);
if(interior)drawInterior();
else drawWorld();
drawWeather();
if(flash>0){ctx.fillStyle=`rgba(255,245,230,${flash})`;
ctx.fillRect(0,0,W,H);
}if(interior&&blackout>0){ctx.fillStyle=`rgba(0,0,0,${clamp(blackout/2,0,.92)})`;
ctx.fillRect(0,0,W,H);
}if(state.sanity<45){ctx.fillStyle=`rgba(30,5,15,${(45-state.sanity)/180})`;
ctx.fillRect(0,0,W,H);
}ctx.restore();
}
function drawWorld(){
drawEnhancedSky();
drawEnhancedGround();
chapter==='SAN FRANCISCO'?drawSFStreetProps():drawAlcatrazProps();
drawEnhancedStructures();
drawEnhancedBloodWriting();
drawEnhancedSkeletons();
drawEnhancedChests();
drawEnhancedLoot();
drawEnhancedSurvivors();
drawEnhancedZombies();
for(const b of bullets){const x=b.x-camera;if(x>-30&&x<W+30){px(x-4,b.y-2,8,4,'#e7d48c');px(x+2,b.y-1,5,2,'#fff1bb');}}
drawEnhancedPlayer();
drawEnhancedSmiler();
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
window.addEventListener('keydown',e=>{
const k=e.key.length===1?e.key.toLowerCase():e.key;
const code=e.code||'';
const mapped=code==='KeyA'?'a':code==='KeyD'?'d':code==='KeyW'?'w':code==='KeyS'?'s':code==='ArrowLeft'?'ArrowLeft':code==='ArrowRight'?'ArrowRight':code==='ArrowUp'?'ArrowUp':code==='ArrowDown'?'ArrowDown':code==='ShiftLeft'||code==='ShiftRight'?'Shift':k;
const movement=['a','d','w','s','ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' ','Shift'];
if(movement.includes(mapped))e.preventDefault();
if(mode==='menu')return;
if(mode==='intro'&&(k==='Enter'||k===' ')){nextCut();return;}
if(k==='Escape'){
 if(infoFlashOpen){closeInfoFlash();return}
 if(mode==='intro'){finishIntro();return}
 if(mode==='play'){pauseGame();return}
 if(mode==='pause'){resumeGame();return}
}
if(mode!=='play')return;
if(k==='Enter'&&infoFlashOpen){closeInfoFlash();return}
if(k==='p'){openPrivacyDashboard();return}
if(k==='Tab'){e.preventDefault();gadgetOpen=!gadgetOpen;document.getElementById('gadget').classList.toggle('hidden',!gadgetOpen);if(gadgetOpen)loadGadget();return}
if(k==='i'){inventoryOpen=!inventoryOpen;return}
if(k==='e'){interact();return}
if(k==='r'){reload();return}
if(k==='h'){useItem();return}
if(k==='f'){state.light=!state.light;setMsg(state.light?'Flashlight on.':'Flashlight off.',1);return}
if(k==='q'){for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<82){z.hp-=55;z.hit=.15;shake=4;if(z.hp<=0)z.dead=true;setMsg('MELEE HIT',.5);}}return}
if(k==='g'&&state.grenades>0){state.grenades--;for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<250)z.hp-=110;}flash=.18;shake=10;tone(70,.4,'sawtooth',.08,-30);setMsg('GRENADE',1);return}
keys.add(mapped);
if(mapped==='a'||mapped==='ArrowLeft')inputState.left=true;
if(mapped==='d'||mapped==='ArrowRight')inputState.right=true;
if(mapped==='s'||mapped==='ArrowDown')inputState.down=true;
if(mapped==='Shift')inputState.run=true;
if(mapped==='w'||mapped==='ArrowUp'||mapped===' ')inputState.jump=true;
});
window.addEventListener('keyup',e=>{const k=e.key.length===1?e.key.toLowerCase():e.key;const code=e.code||'';const mapped=code==='KeyA'?'a':code==='KeyD'?'d':code==='KeyW'?'w':code==='KeyS'?'s':code==='ArrowLeft'?'ArrowLeft':code==='ArrowRight'?'ArrowRight':code==='ArrowUp'?'ArrowUp':code==='ArrowDown'?'ArrowDown':code==='ShiftLeft'||code==='ShiftRight'?'Shift':k;keys.delete(mapped);if(mapped==='a'||mapped==='ArrowLeft')inputState.left=false;if(mapped==='d'||mapped==='ArrowRight')inputState.right=false;if(mapped==='s'||mapped==='ArrowDown')inputState.down=false;if(mapped==='Shift')inputState.run=false;if(mapped==='w'||mapped==='ArrowUp'||mapped===' ')inputState.jump=false;});
window.addEventListener('blur',()=>{keys.clear();mouse.down=false;inputState.left=false;inputState.right=false;inputState.down=false;inputState.run=false;inputState.jump=false;});
window.addEventListener('visibilitychange',()=>{if(document.hidden)keys.clear();});
canvas.setAttribute('tabindex','0');
canvas.addEventListener('click',()=>canvas.focus());
window.addEventListener('pointerdown',()=>{if(mode==='play')canvas.focus();});
window.addEventListener('pointerup',()=>{if(mode==='play'){keys.delete('a');keys.delete('d');keys.delete('s');keys.delete('ArrowLeft');keys.delete('ArrowRight');keys.delete('ArrowDown');}});
document.querySelectorAll('[data-char]').forEach(b=>b.addEventListener('click',()=>{closeModePicker();audio();startGame(b.dataset.char);}));
document.getElementById('cutscene').addEventListener('click',()=>{if(mode==='intro')nextCut();});
document.getElementById('objectiveTab').onclick=()=>{const panel=document.getElementById('objectivePanel');if(!panel)return;const open=panel.classList.toggle('open');panel.setAttribute('aria-hidden',open?'false':'true');if(open)renderObjectivePanel();};document.getElementById('objectiveClose').onclick=()=>{const panel=document.getElementById('objectivePanel');if(panel){panel.classList.remove('open');panel.setAttribute('aria-hidden','true');}};
document.getElementById('resume').onclick=resumeGame;
document.getElementById('restart').onclick=restart;
document.getElementById('backMenu').onclick=()=>{mode='menu';hide('pause');hide('hud');show('menu');};
document.getElementById('endingMenu').onclick=()=>{mode='menu';hide('ending');hide('hud');show('menu');};
document.getElementById('deathRestart').onclick=restart;
document.getElementById('deathMenu').onclick=()=>{mode='menu';hide('death');hide('hud');show('menu');};
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


function px(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));}
function poly(points,c){ctx.fillStyle=c;ctx.beginPath();ctx.moveTo(points[0][0],points[0][1]);for(let i=1;i<points.length;i++)ctx.lineTo(points[i][0],points[i][1]);ctx.closePath();ctx.fill();}
function line(x1,y1,x2,y2,c,w=2){ctx.strokeStyle=c;ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();}
function glowRect(x,y,w,h,c,a){ctx.save();ctx.globalAlpha=a;ctx.fillStyle=c;ctx.fillRect(x,y,w,h);ctx.restore();}
function drawPixelClouds(){const drift=(totalTime*9)%1700;for(let i=0;i<9;i++){const x=i*190-(camera*.035+drift)%1900;const y=55+(i%4)*38;ctx.globalAlpha=.16+(i%3)*.03;px(x,y,110,9,'#30363b');px(x+20,y-6,64,6,'#252a2e');px(x+44,y-11,35,7,'#1d2226');}ctx.globalAlpha=1;}
function drawDistantOcean(){if(chapter!=='ALCATRAZ')return;px(0,365,W,74,'#10191e');for(let i=0;i<44;i++){const x=(i*73-camera*.21)%W;const y=376+(i%6)*9;line(x,y,x+18,y,'#26363c',1);line(x+29,y+4,x+42,y+4,'#1b2a2f',1);}for(let i=0;i<7;i++){const x=70+i*190-(camera*.08%250);poly([[x,382],[x+30,354-(i%2)*12],[x+72,382]],'#11171a');}}
function drawGoldenGate(){if(chapter!=='SAN FRANCISCO')return;const base=360;const x=60-camera*.055;line(x,base-38,x+1070,base-38,'#2a3033',7);line(x+180,base-38,x+180,210,'#30383c',12);line(x+800,base-38,x+800,235,'#30383c',12);line(x+174,214,x+804,240,'#40484b',3);line(x+174,237,x+804,262,'#252b2e',2);for(let i=0;i<13;i++){const t=i/12;const xx=x+188+t*604;const yy=218+24*t;line(xx,yy,xx,base-10,'#232a2d',1);}}
function drawSFStreetProps(){if(chapter!=='SAN FRANCISCO')return;const viewLeft=camera-40,viewRight=camera+W+40;for(let i=0;i<20;i++){const wx=260+i*430;const x=wx-camera;if(wx<viewLeft||wx>viewRight)continue;const broken=i%5===0;const poleH=110+(i%4)*22;px(x,GROUND-poleH,6,poleH,'#171b1c');px(x-8,GROUND-poleH,22,5,'#222627');if(i%3===0){px(x+8,GROUND-poleH+10,23,5,'#4a4338');px(x+17,GROUND-poleH+8,7,9,'#625540');}if(i%4===0){px(x-55,GROUND-34,70,22,'#202426');px(x-62,GROUND-12,84,9,'#101214');if(!broken){ctx.strokeStyle='#4a4f50';ctx.lineWidth=3;ctx.strokeRect(x-50,GROUND-30,14,10);ctx.strokeRect(x+8,GROUND-30,14,10);px(x-45,GROUND-5,14,5,'#050607');px(x+14,GROUND-5,14,5,'#050607');}}}}
function drawAlcatrazProps(){if(chapter!=='ALCATRAZ')return;for(let i=0;i<15;i++){const x=(250+i*315-camera)% (ALCATRAZ_WIDTH+600);const pxv=x<0?x+ALCATRAZ_WIDTH+600:x;if(pxv>W+50)continue;px(pxv,GROUND-82,6,82,'#181b1c');for(let j=0;j<5;j++)line(pxv+6+j*8,GROUND-82,pxv+2+j*8,GROUND-42,'#3c4140',2);px(pxv-12,GROUND-118,34,4,'#424746');}for(let i=0;i<7;i++){const x=330+i*620-camera*.7;px(x,GROUND-160,88,8,'#16191a');px(x+8,GROUND-152,7,90,'#252a2b');px(x+70,GROUND-152,7,90,'#252a2b');line(x+10,GROUND-150,x+42,GROUND-178,'#353a3b',2);}}
function drawEnhancedSky(){const sf=chapter==='SAN FRANCISCO';const top=sf?'#070b11':'#06090d';const bottom=sf?'#161b23':'#11171b';const g=ctx.createLinearGradient(0,0,0,440);g.addColorStop(0,top);g.addColorStop(1,bottom);ctx.fillStyle=g;ctx.fillRect(0,0,W,H);for(let i=0;i<110;i++){const x=(i*137-camera*.12)%W;const y=(i*43)%330;px(x,y,(i%3)+1,(i%2)+1,i%7===0?'#5b5d5c':'#1c252a');}drawPixelClouds();if(sf){for(let i=0;i<18;i++){const x=i*105-(camera*.09%105);const h=80+(i%6)*31;px(x,375-h,82,h,'#11161a');for(let q=0;q<4;q++){for(let w=0;w<3;w++){if((i+q+w)%3===0)px(x+10+w*20,390-h+18+q*28,6,10,'#544f41');}}}drawGoldenGate();}else{drawDistantOcean();for(let i=0;i<5;i++){const x=120+i*270-camera*.06;px(x,275-(i%2)*18,130,85,'#171d20');px(x+18,260-(i%2)*18,95,14,'#22282b');}}
}
function drawEnhancedGround(){const sf=chapter==='SAN FRANCISCO';const g=ctx.createLinearGradient(0,430,0,H);g.addColorStop(0,sf?'#1b1d1f':'#171a1b');g.addColorStop(1,sf?'#0e1112':'#0e1112');ctx.fillStyle=g;ctx.fillRect(0,430,W,290);for(let i=0;i<520;i++){const x=(i*83-camera*1.05)%W;const y=438+(i*47)%260;px(x,y,1+(i%4),1+(i%3),i%9===0?'#484949':i%2?'#242829':'#1a1e1f');}px(0,GROUND,W,150,'#0c0f10');for(let i=0;i<95;i++){const x=(i*67-camera*1.2)%W;const y=GROUND+10+(i%8)*17;px(x,y,11+(i%8)*7,2,i%4===0?'#3f4140':'#262a2b');}for(let i=0;i<18;i++){const x=(i*171-camera*0.8)%W;px(x,GROUND+70,36,4,'#16191a');px(x+12,GROUND+74,13,2,'#303333');}}
function drawEnhancedStructures(){for(const b of buildings){const x=b.x-camera;if(x<-b.w-80||x>W+80)continue;const h=b.type==='prison'?265:b.floors*112+88;const main=b.type==='prison'?'#24292b':'#202527';const dark=b.type==='prison'?'#171b1c':'#15191a';const edge=b.type==='hospital'?'#3b4041':b.type==='police'?'#30383a':'#34393a';px(x,GROUND-h,b.w,h,main);px(x,GROUND-h,b.w,8,edge);px(x+12,GROUND-h+10,b.w-24,6,dark);if(b.type==='prison'){for(let k=0;k<6;k++)px(x+25+k*62,GROUND-h-13,36,12,'#34393a');}else{for(let f=0;f<b.floors;f++){const fy=GROUND-78-f*112;px(x+18,fy,b.w-36,5,'#32383a');for(let q=0;q<Math.floor((b.w-50)/44);q++){const wx=x+25+q*44;const lit=((q+f+Math.floor(b.x/100))%7===0);px(wx,fy-35,23,27,lit?'#655f4e':'#0b0f10');if(lit)px(wx+4,fy-30,4,5,'#897856');}}}px(x+b.w/2-29,GROUND-71,58,71,'#080a0b');px(x+b.w/2+15,GROUND-37,6,6,'#605a4b');px(x+b.w/2-28,GROUND-4,56,5,'#101212');if(b.type==='police'){px(x+18,GROUND-h+18,b.w-36,22,'#171b1c');ctx.font='bold 13px Consolas';ctx.fillStyle='#c4c0b3';ctx.fillText('POLICE',x+28,GROUND-h+34);}if(b.type==='hospital'){px(x+b.w/2-62,GROUND-h+18,124,33,'#394245');px(x+b.w/2-8,GROUND-h+23,16,22,'#b5b9b4');px(x+b.w/2-20,GROUND-h+31,40,8,'#b5b9b4');}if(b.type==='funeral'){px(x+24,GROUND-h+18,b.w-48,25,'#191d1e');ctx.font='12px Consolas';ctx.fillStyle='#8d918e';ctx.fillText('MERCY FUNERAL',x+35,GROUND-h+35);}if(b.type==='research'){px(x+b.w/2-90,GROUND-h+16,180,25,'#13191a');ctx.font='12px Consolas';ctx.fillStyle='#909794';ctx.fillText('ECLIPSE RESEARCH ANNEX',x+b.w/2-78,GROUND-h+33);}}}
function drawEnhancedBloodWriting(){for(const b of bloodMarks){const x=b.x-camera;if(x<-120||x>W+120)continue;ctx.save();ctx.globalAlpha=.85;ctx.fillStyle='#591c1e';ctx.beginPath();ctx.ellipse(x,b.y,Math.max(9,b.w/2),6,0,0,Math.PI*2);ctx.fill();for(let i=0;i<b.drips+2;i++){px(x-b.w/3+i*9,b.y,2,8+i*5,'#651f20');}ctx.restore();}for(const w of writings){const x=w.x-camera;if(x<-230||x>W+230)continue;ctx.save();ctx.translate(x,w.y);ctx.rotate(Math.sin(w.x*.014)*.02);ctx.font=`bold ${Math.max(12,20*w.scale)}px Consolas`;ctx.fillStyle='#813131';ctx.shadowColor='#160708';ctx.shadowBlur=4;ctx.fillText(w.text,0,0);ctx.restore();}}
function drawEnhancedSkeletons(){for(const s of skeletons){const x=s.x-camera;if(x<-80||x>W+80)continue;const bob=Math.sin(totalTime*1.8+s.phase)*1.3;ctx.strokeStyle='#b4aa98';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x,GROUND-47+bob);ctx.lineTo(x,GROUND-15+bob);ctx.moveTo(x,GROUND-37+bob);ctx.lineTo(x-28,GROUND-23+bob);ctx.moveTo(x,GROUND-37+bob);ctx.lineTo(x+28,GROUND-20+bob);ctx.moveTo(x,GROUND-15+bob);ctx.lineTo(x-18,GROUND+2);ctx.moveTo(x,GROUND-15+bob);ctx.lineTo(x+17,GROUND+3);ctx.stroke();px(x-9,GROUND-70+bob,18,18,'#aaa28f');px(x-6,GROUND-65+bob,4,5,'#151719');px(x+2,GROUND-65+bob,4,5,'#151719');px(x-13,GROUND-48+bob,26,5,'#8b8475');}}
function drawEnhancedChests(){for(const c of chests){if(c.inside)continue;const x=c.x-camera;if(x<-80||x>W+80)continue;const body=c.opened?'#2c2924':c.rare?'#574535':'#45372d';px(x,c.y,c.w,c.h,body);px(x,c.y,c.w,6,'#6c5440');ctx.strokeStyle='#171313';ctx.strokeRect(x,c.y,c.w,c.h);px(x+c.w/2-4,c.y+13,8,9,'#c09a50');if(c.rare){px(x+8,c.y+8,7,4,'#80694a');px(x+c.w-15,c.y+8,7,4,'#80694a');}}}
function drawEnhancedLoot(){for(const l of loot){if(l.taken)continue;const x=l.x-camera;const bob=Math.sin(totalTime*3+l.x)*2;const colors={ammo:'#c0a85b',medkit:'#ddd8ca',food:'#797052',scrap:'#888b88',battery:'#6a8b78',key:'#c09d59',pass:'#b99e69'};px(x,l.y+bob,15,11,colors[l.item]||'#777b79');px(x+3,l.y+bob-4,9,4,colors[l.item]||'#777b79');if(l.item==='ammo')px(x+5,l.y+bob-7,4,4,'#dfc477');if(l.item==='medkit')px(x+6,l.y+bob-5,3,14,'#914545');}}
function drawCharacterSprite(x,y,who,dir,anim,role){
const stride=Math.sin(anim)*4;
const bounce=Math.sin(totalTime*2.1+x*.008)*1.1;
const p=(who==='May'?{coat:'#343845',coat2:'#54596a',shirt:'#c9c3b6',skin:'#d1b49b',hair:'#56382b',hair2:'#7a4f3b',pants:'#22262b',boot:'#101214',badge:'#cfb872',tie:'#414b56'}:who==='Yumi'?{coat:'#2b3935',coat2:'#44514a',shirt:'#c8c3b7',skin:'#d2b99f',hair:'#121718',hair2:'#2c3030',pants:'#202526',boot:'#0c1011',badge:'#d0b66d',tie:'#394940'}:{coat:'#29383a',coat2:'#405153',shirt:'#c9c1b0',skin:'#ccaf97',hair:'#302322',hair2:'#533d34',pants:'#1e2426',boot:'#0e1214',badge:'#cfb56e',tie:'#3e4a46'});
const by=y+bounce;
px(x-20,by+70,58,8,'rgba(0,0,0,.52)');
px(x-7+stride*.12,by+48,13,23,p.pants);
px(x+11-stride*.12,by+48,13,23,p.pants);
px(x-10-stride*.12,by+68,17,7,p.boot);
px(x+9+stride*.12,by+68,17,7,p.boot);
px(x-11,by+24,40,29,p.coat);
px(x-6,by+22,31,17,p.shirt);
px(x-1,by+25,8,12,p.tie);
px(x-17+stride*.18,by+27,10,27,p.coat2);
px(x+30+stride*.18,by+27,10,27,p.coat2);
px(x-20+stride*.18,by+48,14,9,p.coat);
px(x+29+stride*.18,by+48,14,9,p.coat);
px(x-7,by+1,33,29,p.skin);
px(x-11,by-6,41,12,p.hair);
px(x-8,by-13,35,10,p.hair2);
if(who==='Julia'){px(x+20,by-9,11,7,p.hair2);px(x+25,by-2,9,21,p.hair2);px(x+29,by+4,6,12,p.hair2);}
if(who==='May'){px(x-13,by-5,8,28,p.hair2);px(x+25,by-3,10,20,p.hair2);px(x+29,by+5,7,18,p.hair2);}
if(who==='Yumi'){px(x-13,by-1,8,26,p.hair2);px(x+27,by-1,9,30,p.hair2);px(x-10,by-14,29,6,p.hair);}
px(x-1,by+9,4,4,'#151719');
px(x+18,by+9,4,4,'#151719');
px(x+3,by+17,18,3,'#8a5b54');
px(x-5,by+30,9,13,p.coat2);
px(x+18,by+30,9,13,p.coat2);
px(x-10,by+24,5,6,p.badge);
px(x-8,by+25,3,3,'#fff0a4');
px(x+27,by+29,6,20,'#161b1c');
px(x+29,by+32,3,7,'#4c5553');
if(role==='Soldier'){px(x-15,by-5,40,9,'#3f4c43');px(x-5,by-10,25,5,'#2a342f');}
if(role==='Nurse'){px(x-8,by+30,34,7,'#768078');px(x+2,by+31,5,18,'#e7e3d8');px(x,by+37,10,5,'#e7e3d8');}
if(role==='Mechanic'){px(x-9,by+20,35,7,'#654f3e');px(x+28,by+35,8,14,'#94775c');}
}

function drawSFStreetProps(){
if(chapter!=='SAN FRANCISCO')return;
for(let i=0;i<24;i++){
 const wx=180+i*360;
 const x=wx-camera;
 if(x<-100||x>W+100)continue;
 const poleH=115+(i%5)*18;
 px(x,GROUND-poleH,7,poleH,'#15191c');
 px(x-10,GROUND-poleH,27,6,'#202629');
 px(x+12,GROUND-poleH+10,30,6,'#393e3e');
 if(i%4===0){px(x-52,GROUND-38,79,23,'#222728');px(x-60,GROUND-15,95,8,'#101214');px(x-44,GROUND-34,18,10,'#40464a');px(x+7,GROUND-34,18,10,'#40464a');px(x-44,GROUND-4,14,5,'#060708');px(x+16,GROUND-4,14,5,'#060708');}
 if(i%5===0){px(x-72,GROUND-88,24,55,'#2f3835');px(x-79,GROUND-95,38,9,'#39433d');px(x-69,GROUND-107,18,12,'#171b1c');}
}
for(let i=0;i<10;i++){
 const x=(i*167-camera*.18)%W;
 const y=GROUND-20-(i%3)*26;
 px(x,y,48,8,'#25292a');
 px(x+7,y-5,30,5,'#3a3d3e');
 px(x+2,y+8,8,4,'#a06c4d');
}
}
function drawAlcatrazProps(){
if(chapter!=='ALCATRAZ')return;
for(let i=0;i<18;i++){
 const wx=240+i*300;
 const x=wx-camera;
 if(x<-70||x>W+70)continue;
 px(x,GROUND-92,7,92,'#171b1c');
 for(let j=0;j<6;j++)line(x+8+j*10,GROUND-92,x+3+j*10,GROUND-45,'#454b49',2);
 px(x-14,GROUND-125,38,5,'#4a504d');
}
for(let i=0;i<8;i++){
 const x=350+i*590-camera*.66;
 px(x,GROUND-165,96,8,'#111415');
 px(x+8,GROUND-157,8,90,'#2e3434');
 px(x+78,GROUND-157,8,90,'#2e3434');
 line(x+9,GROUND-153,x+47,GROUND-183,'#4c514f',2);
}
for(let i=0;i<5;i++){
 const x=690+i*740-camera*.1;
 px(x,GROUND-235,12,235,'#252b2c');
 px(x-17,GROUND-246,47,12,'#303738');
 px(x-8,GROUND-258,29,13,'#15191a');
 px(x-2,GROUND-278,17,20,'#303738');
}
}
function drawEnhancedSky(){
const sf=chapter==='SAN FRANCISCO';
const top=sf?'#070c13':'#05090d';
const bottom=sf?'#171e25':'#12191d';
const g=ctx.createLinearGradient(0,0,0,430);
g.addColorStop(0,top);g.addColorStop(.7,bottom);g.addColorStop(1,'#1b2022');
ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
for(let i=0;i<120;i++){
 const x=(i*137-camera*.09)%W;
 const y=(i*43)%330;
 px(x,y,(i%3)+1,(i%2)+1,i%11===0?'#74736a':i%5===0?'#3a4145':'#1c252a');
}
drawPixelClouds();
if(sf){
 for(let i=0;i<18;i++){
  const x=i*105-(camera*.055%105);
  const h=80+(i%6)*31;
  px(x,375-h,82,h,'#10161b');
  px(x+7,382-h,68,5,'#242b30');
  for(let q=0;q<4;q++)for(let w=0;w<3;w++)if((i+q+w)%3===0)px(x+10+w*20,390-h+18+q*28,6,10,'#5a5444');
 }
 drawGoldenGate();
}else{
 drawDistantOcean();
 for(let i=0;i<7;i++){
  const x=80+i*245-camera*.045;
  px(x,270-(i%2)*17,145,92,'#151b1f');
  px(x+17,257-(i%2)*17,107,14,'#242a2d');
  px(x+69,242-(i%2)*17,44,20,'#1d2326');
 }
}
}
function drawEnhancedGround(){
const sf=chapter==='SAN FRANCISCO';
const g=ctx.createLinearGradient(0,430,0,H);
g.addColorStop(0,sf?'#24282a':'#1c2021');g.addColorStop(.45,sf?'#141718':'#15191a');g.addColorStop(1,'#0b0e0f');ctx.fillStyle=g;ctx.fillRect(0,430,W,290);
for(let i=0;i<560;i++){
 const x=(i*83-camera*1.05)%W;
 const y=438+(i*47)%260;
 px(x,y,1+(i%4),1+(i%3),i%13===0?'#575956':i%3===0?'#313535':'#1d2223');
}
px(0,GROUND,W,150,'#0b0e0f');
for(let i=0;i<112;i++){
 const x=(i*67-camera*1.2)%W;
 const y=GROUND+9+(i%8)*17;
 px(x,y,11+(i%8)*7,2,i%7===0?'#4a4b48':'#24292a');
}
if(sf){for(let i=0;i<12;i++){const x=(i*124-camera*.8)%W;px(x,GROUND-3,62,5,'#202526');px(x+8,GROUND+5,34,3,'#343738');}}
}
function drawEnhancedStructures(){
for(const b of buildings){
 const x=b.x-camera;
 if(x<-b.w-100||x>W+100)continue;
 const h=b.type==='prison'?290:b.floors*116+94;
 const main=b.type==='prison'?'#252b2d':b.type==='hospital'?'#323638':b.type==='police'?'#2b3134':b.type==='funeral'?'#2d292b':'#23282a';
 const trim=b.type==='prison'?'#42494a':'#3a4040';
 px(x,GROUND-h,b.w,h,main);px(x,GROUND-h,b.w,9,trim);px(x+12,GROUND-h+12,b.w-24,6,'#111516');
 if(b.type==='prison'){
  for(let f=0;f<3;f++)for(let q=0;q<Math.floor(b.w/62);q++){const wx=x+24+q*62;const wy=GROUND-60-f*72;px(wx,wy,38,24,'#0b0f10');for(let j=0;j<5;j++)px(wx+5+j*7,wy+3,2,18,'#666a66');}
  for(let k=0;k<6;k++)px(x+28+k*62,GROUND-h-16,38,12,'#353b3c');
 }else{
  for(let f=0;f<b.floors;f++){
   const fy=GROUND-82-f*116;px(x+18,fy,b.w-36,5,'#3d4242');
   for(let q=0;q<Math.floor((b.w-48)/43);q++){
    const wx=x+25+q*43;const lit=((q+f+Math.floor(b.x/100))%6===0);
    px(wx,fy-37,23,28,lit?'#655f4d':'#0a0e0f');
    px(wx+3,fy-34,17,3,lit?'#8a7a59':'#171c1d');
    if(f>0)px(wx+2,fy-6,18,3,'#292e2e');
   }
  }
 }
 px(x+b.w/2-31,GROUND-73,62,73,'#080a0b');px(x+b.w/2+18,GROUND-39,6,6,'#6c6452');
 if(b.type==='police'){px(x+18,GROUND-h+19,b.w-36,23,'#121718');ctx.font='bold 13px Consolas';ctx.fillStyle='#d1c9b5';ctx.fillText('POLICE',x+30,GROUND-h+35);}
 if(b.type==='hospital'){px(x+b.w/2-63,GROUND-h+19,126,35,'#3c494a');px(x+b.w/2-8,GROUND-h+24,16,25,'#d2d6ce');px(x+b.w/2-21,GROUND-h+33,42,8,'#d2d6ce');}
 if(b.type==='funeral'){px(x+23,GROUND-h+18,b.w-46,27,'#171b1d');ctx.font='12px Consolas';ctx.fillStyle='#a7a097';ctx.fillText('MERCY FUNERAL',x+34,GROUND-h+36);}
 if(b.type==='research'){px(x+b.w/2-96,GROUND-h+16,192,27,'#111719');ctx.font='11px Consolas';ctx.fillStyle='#a5ada8';ctx.fillText('ECLIPSE RESEARCH ANNEX',x+b.w/2-84,GROUND-h+34);}
 }
}
function drawEnhancedBloodWriting(){
for(const b of bloodMarks){const x=b.x-camera;if(x<-140||x>W+140)continue;ctx.save();ctx.globalAlpha=.92;ctx.fillStyle='#561c20';ctx.beginPath();ctx.ellipse(x,b.y,b.w/2,6,0,0,Math.PI*2);ctx.fill();for(let i=0;i<b.drips+3;i++)px(x-b.w/3+i*8,b.y,2,8+i*5,'#682126');ctx.restore();}
for(const w of writings){const x=w.x-camera;if(x<-260||x>W+260)continue;ctx.save();ctx.translate(x,w.y);ctx.rotate(Math.sin(w.x*.014)*.02);ctx.font=`bold ${Math.max(12,20*w.scale)}px Consolas`;ctx.fillStyle='#8b3437';ctx.shadowColor='#160708';ctx.shadowBlur=5;ctx.fillText(w.text,0,0);ctx.restore();}
}
function drawEnhancedSkeletons(){
for(const s of skeletons){const x=s.x-camera;if(x<-90||x>W+90)continue;const bob=Math.sin(totalTime*1.8+s.phase)*1.4;ctx.strokeStyle='#bdb39e';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x,GROUND-47+bob);ctx.lineTo(x,GROUND-15+bob);ctx.moveTo(x,GROUND-38+bob);ctx.lineTo(x-30,GROUND-22+bob);ctx.moveTo(x,GROUND-38+bob);ctx.lineTo(x+29,GROUND-20+bob);ctx.moveTo(x,GROUND-15+bob);ctx.lineTo(x-19,GROUND+2);ctx.moveTo(x,GROUND-15+bob);ctx.lineTo(x+18,GROUND+3);ctx.stroke();px(x-10,GROUND-70+bob,20,20,'#afa690');px(x-6,GROUND-65+bob,4,5,'#151718');px(x+3,GROUND-65+bob,4,5,'#151718');px(x-13,GROUND-49+bob,27,5,'#81796d');}
}
function drawEnhancedChests(){for(const c of chests){if(c.inside)continue;const x=c.x-camera;if(x<-90||x>W+90)continue;const body=c.opened?'#2f2b27':c.rare?'#654b35':'#4a392d';px(x,c.y,c.w,c.h,body);px(x,c.y,c.w,7,'#76583f');px(x+5,c.y+8,c.w-10,4,'#2c2926');px(x+c.w/2-5,c.y+13,10,11,'#d0a85d');ctx.strokeStyle='#161313';ctx.lineWidth=2;ctx.strokeRect(x,c.y,c.w,c.h);if(c.rare){px(x+8,c.y+8,9,5,'#9b7d4d');px(x+c.w-17,c.y+8,9,5,'#9b7d4d');}}}
function drawEnhancedLoot(){for(const l of loot){if(l.taken)continue;const x=l.x-camera;const bob=Math.sin(totalTime*3+l.x)*2;const colors={ammo:'#cdb15d',medkit:'#e1ddd0',food:'#77705a',scrap:'#929794',battery:'#739985',key:'#d1af62',pass:'#c5aa72'};px(x,l.y+bob,17,12,colors[l.item]||'#8b8e8a');px(x+3,l.y+bob-5,11,5,colors[l.item]||'#8b8e8a');if(l.item==='ammo')px(x+6,l.y+bob-9,5,4,'#f2d47b');if(l.item==='medkit'){px(x+7,l.y+bob-6,4,14,'#984649');px(x+2,l.y+bob-1,14,4,'#984649');}}
}
function drawEnhancedZombies(){
 for(const z of zombies){
  if(z.dead)continue;
  const x=z.x-camera;if(x<-90||x>W+90)continue;
  const bob=Math.sin(totalTime*2.2+z.phase)*2.2;
  const swing=Math.sin(totalTime*3.1+z.phase)*8;
  const shirt=z.type==='runner'?'#455347':z.type==='brute'?'#493836':'#3d4540';
  const skin=z.type==='brute'?'#655c52':'#767970';
  ctx.save();
  if(z.hit>0&&Math.floor(totalTime*30)%2===0)ctx.globalAlpha=.52;
  px(x-14,GROUND+2,58,7,'rgba(0,0,0,.45)');
  px(x-2,z.y+31+bob,38,z.h-31,shirt);
  px(x-1,z.y+1+bob,35,30,skin);
  px(x-4,z.y+19+bob,42,10,'#171b1b');
  px(x+5,z.y+8+bob,6,5,'#e5dcc0');px(x+23,z.y+8+bob,6,5,'#d0d7cc');
  line(x+2,z.y+42+bob,x-12,z.y+61+bob+swing,'#555b56',6);
  line(x+33,z.y+42+bob,x+49,z.y+61+bob-swing,'#555b56',6);
  const leg=Math.sin(totalTime*3.1+z.phase)*5;
  px(x-3+leg,GROUND-2,14,7,'#141819');px(x+23-leg,GROUND-2,14,7,'#141819');
  if(z.type==='runner'){px(x+6,z.y-8+bob,22,6,'#594a40');px(x+12,z.y-13+bob,9,5,'#6e5d4f');}
  if(z.type==='brute'){px(x-7,z.y+25+bob,46,33,'#382e2d');px(x-14,z.y+49+bob,12,23,'#443835');px(x+41,z.y+49+bob,12,23,'#443835');}
  ctx.restore();
 }
}
function drawEnhancedSurvivors(){for(const s of survivors){const x=s.x-camera;if(x<-90||x>W+90)continue;const who=s.name==='Mara'?'May':s.name==='Eli'?'Julia':'Yumi';drawCharacterSprite(x+7,GROUND-72,who,s.x<player.x?-1:1,totalTime*2.2,s.role);if(s.follow){ctx.fillStyle='#d0c9ba';ctx.font='11px Consolas';ctx.fillText('FOLLOWING',x-30,GROUND-90);}}}
function drawEnhancedSmiler(){if(!smiler.active||mode!=='play')return;const sx=smiler.x-camera;if(sx<-210||sx>W+210)return;const a=clamp(smiler.intensity,0,1)*.96;ctx.save();ctx.globalAlpha=a;ctx.shadowColor='rgba(0,0,0,.9)';ctx.shadowBlur=24;px(sx-34,GROUND-222,68,144,'#020203');px(sx-47,GROUND-143,94,70,'#020203');px(sx-28,GROUND-280,56,65,'#010102');px(sx-20,GROUND-270,40,16,'#050506');px(sx-11,GROUND-257,8,6,'#d5d1c8');px(sx+4,GROUND-257,8,6,'#d5d1c8');ctx.strokeStyle='#ded7ce';ctx.lineWidth=4;ctx.beginPath();ctx.arc(sx,GROUND-233,23,.12,3.02);ctx.stroke();for(let i=0;i<5;i++){line(sx-21+i*10,GROUND-202,sx-30+i*14,GROUND-101,'#050506',6);}line(sx-13,GROUND-256,sx-33,GROUND-223,'#080809',4);line(sx+13,GROUND-256,sx+34,GROUND-223,'#080809',4);ctx.restore();}
function drawEnhancedInterior(){
const b=interior.building;const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#090c0d');g.addColorStop(.6,'#1b2021');g.addColorStop(1,'#0b0e0f');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);px(0,520,W,200,'#0b0e0f');for(let i=0;i<20;i++){px(i*70,76,48,5,i%4?'#303636':'#4a4e4b');px(i*70+17,81,4,439,'#202526');}px(560,80,6,440,'#0b0d0e');px(70,420,220,95,'#171b1c');px(55,388,250,36,'#383d3e');px(88,337,94,48,'#0c1011');px(770,422,184,93,'#37312b');px(792,378,138,44,'#262a2b');px(808,389,18,10,'#535750');px(1088,410,64,110,'#202526');for(let i=0;i<3;i++){px(1095,424+i*27,50,6,'#565b58');}ctx.font='bold 17px Consolas';ctx.fillStyle='#8e3b3a';ctx.fillText(b.name.toUpperCase(),255,300);ctx.font='12px Consolas';ctx.fillStyle='#7d8582';ctx.fillText(`FLOOR ${floor}`,590,112);px(575,405,92,115,'#101415');for(let i=0;i<3;i++)px(585,421+i*29,70,7,'#585c59');if(floor>=2){px(412,110,55,250,'#171b1c');px(820,110,55,250,'#171b1c');px(412,110,463,6,'#353a3b');}if(floor>=3){for(let i=0;i<4;i++){px(320+i*170,150,108,80,'#111515');px(337+i*170,168,74,10,'#4d514d');px(347+i*170,185,52,34,'#202426');}}
}
function drawEnhancedInteriorPlayer(){drawCharacterSprite(player.x,player.y,selectedCharacter,player.facing,player.anim,'');const gunX=player.x+26*player.facing;line(gunX,player.y+39,gunX+30*player.facing,player.y+36,'#101315',5);}
function enhancedFootsteps(){if(mode!=='play'||interior)return;if(Math.abs(player.vx)>25&&player.onGround&&Math.random()<.2)particles.push({x:player.x+rand(-7,7),y:GROUND-4,life:.65,vx:rand(-20,20),vy:rand(-35,-10),size:rand(2,4),c:'#747673'});if(particles.length>140)particles.splice(0,particles.length-140);}
function drawEnhancedPlayer(){
const x=player.x-camera;const bob=player.onGround?Math.sin(player.anim)*1.2:0;ctx.save();if(player.hitTimer>0&&Math.floor(totalTime*20)%2===0)ctx.globalAlpha=.45;drawCharacterSprite(x+8,player.y+bob,selectedCharacter,player.facing,player.anim,'');const gunX=x+26*player.facing;const gunY=player.y+39+bob;line(gunX,gunY,gunX+31*player.facing,gunY-2,'#101416',6);line(gunX+1,gunY-3,gunX+25*player.facing,gunY-3,'#747773',2);px(gunX+6*player.facing,gunY-6,8,4,'#2d3130');if(player.shootTimer>0){poly([[gunX+30*player.facing,gunY-6],[gunX+52*player.facing,gunY-12],[gunX+44*player.facing,gunY],[gunX+52*player.facing,gunY+6],[gunX+30*player.facing,gunY+3]],'#f0db8e');}ctx.restore();}
function drawWorld(){drawEnhancedSky();drawEnhancedGround();chapter==='SAN FRANCISCO'?drawSFStreetProps():drawAlcatrazProps();drawEnhancedStructures();drawEnhancedBloodWriting();drawEnhancedSkeletons();drawEnhancedChests();drawEnhancedLoot();drawEnhancedSurvivors();drawEnhancedZombies();for(const b of bullets){const x=b.x-camera;if(x>-30&&x<W+30){px(x-4,b.y-2,8,4,'#e6d48f');px(x+2,b.y-1,5,2,'#fff2be');}}drawEnhancedPlayer();drawEnhancedSmiler();}
function drawInterior(){drawEnhancedInterior();drawInteriorLoot();drawEnhancedInteriorPlayer();}
function drawWeather(){if(interior)return;for(let i=0;i<240;i++){const x=(i*43+totalTime*270-camera*.65)%W;const y=(i*71+totalTime*430)%H;line(x,y,x-6,y+17,'rgba(174,188,195,.35)',1);}for(let i=0;i<60;i++){const x=(i*91-camera*.8)%W;const y=430+(i*57)%250;px(x,y,2,2,i%3?'#2e3333':'#555956');}}
function drawSmiler(){drawEnhancedSmiler();}

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
gate.style.display='flex';
if(accept)accept.onclick=()=>{gate.style.setProperty('display','none','important');gate.style.pointerEvents='none';closeModePicker();hide('cutscene');hide('hud');hide('pause');hide('ending');hide('death');show('menu');mode='menu';};
if(details)details.onclick=()=>openPrivacyDashboard();
if(close)close.onclick=()=>closePrivacyDashboard();
 const reopen=document.getElementById('privacyReopen');
 if(reopen)reopen.onclick=()=>{gate.style.setProperty('display','flex','important');gate.style.pointerEvents='auto';};
}
setupPrivacyUi();


let physicsState={coyote:0,jumpBuffer:0,fallSpeed:0,landKick:0,stepClock:0,impact:0};
function makeBuildingDoor(b){const inset=Math.min(95,Math.max(58,b.w*.08));return {left:b.x+b.w*.5-inset,right:b.x+b.w*.5+inset};}
function buildingBlocksPoint(b,x){const d=makeBuildingDoor(b);return x>b.x+18&&x<b.x+b.w-18&&(x<d.left||x>d.right);}
function resolveBuildingX(oldX,newX,half){let x=newX;for(const b of buildings){if(interior)break;if(b.type==='prison')continue;if(chapter==='ALCATRAZ'&&!state.startEscaped&&b.x>300)continue;const left=b.x+8-half;const right=b.x+b.w-8+half;if(x>left&&x<right&&buildingBlocksPoint(b,x)){const door=makeBuildingDoor(b);if(oldX<=left&&x>left&&x<door.left)x=left;if(oldX>=right&&x<right&&x>door.right)x=right;if(oldX<door.left&&x>=door.left&&x<=door.right)x=door.left;if(oldX>door.right&&x<=door.right&&x>=door.left)x=door.right;}}
return x;}
function resolveWorldX(oldX,newX){const half=player.w*.42;let x=clamp(newX,22,(chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH)-22);if(chapter==='ALCATRAZ'&&startingCell&&!state.startEscaped){return clamp(x,120,350);}if(!interior)x=resolveBuildingX(oldX,x,half);return x;}
function stepParticles(x,y,count,type='dust'){for(let i=0;i<count;i++){if(particles.length>190)particles.shift();if(type==='rain'){particles.push({x:x+rand(-8,8),y:y,life:rand(.35,.8),vx:rand(-25,25),vy:rand(80,160),size:randi(1,3),c:'#7d8788'});}else if(type==='spark'){particles.push({x:x+rand(-4,4),y:y+rand(-4,4),life:rand(.18,.42),vx:rand(-90,90),vy:rand(-120,-20),size:randi(1,3),c:'#d1a95c'});}else{particles.push({x:x+rand(-8,8),y:y+rand(-2,2),life:rand(.25,.6),vx:rand(-25,25),vy:rand(-60,-10),size:randi(1,3),c:type==='debris'?'#5e625f':'#777a76'});}}}
function updatePlayer(dt){
if(!physicsState)physicsState={coyote:0,jumpBuffer:0,fallSpeed:0,landKick:0,stepClock:0,impact:0};
const left=inputState.left||keys.has('a')||keys.has('ArrowLeft');
const right=inputState.right||keys.has('d')||keys.has('ArrowRight');
const down=inputState.down||keys.has('s')||keys.has('ArrowDown');
let dir=(right?1:0)-(left?1:0);
if(dir)player.facing=dir;
const moving=Math.abs(player.vx)>18&&dir!==0;
const running=inputState.run&&state.stamina>1&&dir!==0&&!down || keys.has('Shift')&&state.stamina>1&&dir!==0&&!down;
const target=running?360:235;
const accel=running?1550:1240;
player.vx+=(dir*target-player.vx)*Math.min(1,accel*dt/Math.max(1,target));
if(dir===0)player.vx*=Math.pow(.001,dt);
if(Math.abs(player.vx)<3)player.vx=0;
if(running)state.stamina=Math.max(0,state.stamina-30*dt);else state.stamina=Math.min(100,state.stamina+19*dt);
if(interior){
 player.vy+=1450*dt;
 physicsState.coyote=player.onGround?.09:Math.max(0,physicsState.coyote-dt);
 if(inputState.jump||keys.has('w')||keys.has('ArrowUp')||keys.has(' '))physicsState.jumpBuffer=.12;else physicsState.jumpBuffer=Math.max(0,physicsState.jumpBuffer-dt);
 if(physicsState.jumpBuffer>0&&(player.onGround||physicsState.coyote>0)){player.vy=-500;player.onGround=false;physicsState.jumpBuffer=0;physicsState.coyote=0;tone(115,.07,'triangle',.022,40);stepParticles(player.x,player.y+player.h-2,5,'dust');}
 if(!(inputState.jump||keys.has('w')||keys.has('ArrowUp')||keys.has(' '))&&player.vy<-170)player.vy+=1250*dt;
 const oldX=player.x;player.x=clamp(player.x+player.vx*dt,40,1200);if(player.x<=40&&player.vx<0){player.vx=0;}if(player.x>=1200&&player.vx>0){player.vx=0;}
 const oldY=player.y;player.y+=player.vy*dt;
 if(player.y+player.h>=GROUND){const falling=player.vy;player.y=GROUND-player.h;player.vy=0;if(!player.onGround&&falling>430){physicsState.impact=Math.min(1,(falling-430)/700);stepParticles(player.x,GROUND-3,8,'dust');shake=Math.max(shake,physicsState.impact*4);}player.onGround=true;}else{player.onGround=false;}
 if(physicsState.impact>0){physicsState.impact=Math.max(0,physicsState.impact-dt*4);}
 if(player.hitTimer>0)player.hitTimer-=dt;
 if(player.shootTimer>0)player.shootTimer-=dt;
 player.anim+=dt*(moving?10:2.2);
 if(moving){physicsState.stepClock-=dt;if(physicsState.stepClock<=0){physicsState.stepClock=running?.21:.32;stepParticles(player.x,GROUND-2,running?2:1,'dust');tone(running?72:58,.025,'square',.006,running?5:0);}}
 return;
}
player.vy+=1500*dt;
if(player.onGround)physicsState.coyote=.1;else physicsState.coyote=Math.max(0,physicsState.coyote-dt);
if(inputState.jump||keys.has('w')||keys.has('ArrowUp')||keys.has(' '))physicsState.jumpBuffer=.12;else physicsState.jumpBuffer=Math.max(0,physicsState.jumpBuffer-dt);
if(physicsState.jumpBuffer>0&&(player.onGround||physicsState.coyote>0)){player.vy=running?-535:-505;player.onGround=false;physicsState.jumpBuffer=0;physicsState.coyote=0;tone(108,.07,'triangle',.023,42);stepParticles(player.x,GROUND-3,6,'dust');}
if(!(inputState.jump||keys.has('w')||keys.has('ArrowUp')||keys.has(' '))&&player.vy<-190)player.vy+=1400*dt;
const oldX=player.x;
let proposed=player.x+player.vx*dt;
player.x=resolveWorldX(oldX,proposed);
if(player.x!==proposed){player.vx=0;if(Math.abs(proposed-player.x)>5)stepParticles(player.x,GROUND-3,2,'debris');}
const oldY=player.y;
player.y+=player.vy*dt;
if(player.y<110){player.y=110;player.vy=Math.max(0,player.vy);}
if(player.y+player.h>=GROUND){const falling=player.vy;player.y=GROUND-player.h;player.vy=0;if(!player.onGround&&falling>430){physicsState.impact=Math.min(1,(falling-430)/650);stepParticles(player.x,GROUND-3,9,'dust');shake=Math.max(shake,physicsState.impact*5);tone(42,.05,'square',.012,-5);}player.onGround=true;}else player.onGround=false;
if(physicsState.impact>0)physicsState.impact=Math.max(0,physicsState.impact-dt*4);
if(player.hitTimer>0)player.hitTimer-=dt;
if(player.shootTimer>0)player.shootTimer-=dt;
player.anim+=dt*(moving?10:2.2);
if(moving&&player.onGround){physicsState.stepClock-=dt;if(physicsState.stepClock<=0){physicsState.stepClock=running?.19:.3;stepParticles(player.x,GROUND-2,running?3:1,'dust');tone(running?68:54,.025,'square',.006,running?3:0);}}
}
function updateZombies(dt){for(const z of zombies){if(z.dead)continue;z.attack=Math.max(0,z.attack-dt);z.hit=Math.max(0,z.hit-dt);const d=player.x-z.x;if(interior){z.x=lerp(z.x,player.x+Math.sin(z.phase)*230,dt*.18);continue;}if(Math.abs(d)<820){const direction=Math.sign(d);const chase=z.type==='runner'?z.speed*1.12:z.type==='brute'?z.speed*.78:z.speed;z.x+=direction*chase*dt;z.phase+=dt*(z.type==='runner'?12:6);if(Math.abs(d)<44&&z.attack<=0){z.attack=1.1;state.health-=z.type==='brute'?19:11;state.sanity=Math.max(0,state.sanity-4.5);player.hitTimer=.28;player.vx=-direction*(z.type==='brute'?210:150);shake=8;tone(52,.16,'sawtooth',.06,-16);stepParticles(player.x,GROUND-35,8,'debris');if(state.health<=0)die('The dead surrounded you.');}}}}
function drawGroundReflection(){if(interior)return;for(let i=0;i<20;i++){const wx=70+i*145;const x=wx-camera;if(x<-150||x>W+150)continue;const y=GROUND-5-(i%3)*4;ctx.save();ctx.globalAlpha=.14;ctx.fillStyle=chapter==='SAN FRANCISCO'?'#78838a':'#68757a';ctx.fillRect(x,y,70,2);ctx.fillRect(x+10,y+5,45,1);ctx.restore();}}
function drawEnhancedGround(){const sf=chapter==='SAN FRANCISCO';const g=ctx.createLinearGradient(0,425,0,H);g.addColorStop(0,sf?'#232529':'#1b1e20');g.addColorStop(.52,sf?'#15191c':'#161a1c');g.addColorStop(1,'#080a0b');ctx.fillStyle=g;ctx.fillRect(0,410,W,310);for(let i=0;i<620;i++){const x=(i*83-camera*1.05)%W;const y=420+(i*47)%290;px(x,y,1+(i%4),1+(i%3),i%11===0?'#555759':i%3===0?'#303435':i%2?'#202526':'#171b1c');}px(0,GROUND,W,150,'#0b0e10');for(let i=0;i<115;i++){const x=(i*67-camera*1.18)%W;const y=GROUND+8+(i%9)*16;px(x,y,8+(i%10)*8,2,i%5===0?'#4b4e4d':'#292d2e');}for(let i=0;i<20;i++){const x=(i*191-camera*.76)%W;px(x,GROUND+58,42,4,'#171a1b');px(x+9,GROUND+64,22,2,'#333737');}drawGroundReflection();}
function drawEnhancedStructures(){for(const b of buildings){const x=b.x-camera;if(x<-b.w-120||x>W+120)continue;const h=b.type==='prison'?270:b.floors*116+94;const main=b.type==='prison'?'#272c2e':b.type==='hospital'?'#262d31':b.type==='police'?'#252c30':'#222728';const shadow=b.type==='prison'?'#171b1d':'#15191b';const trim=b.type==='hospital'?'#4a5152':b.type==='police'?'#3d474a':'#3b4140';px(x,GROUND-h,b.w,h,main);px(x,GROUND-h,b.w,9,trim);px(x+10,GROUND-h+9,b.w-20,7,shadow);px(x+8,GROUND-8,b.w-16,8,'#0a0c0d');for(let f=0;f<b.floors;f++){const fy=GROUND-82-f*116;px(x+18,fy,b.w-36,6,trim);const cols=Math.max(2,Math.floor((b.w-58)/48));for(let q=0;q<cols;q++){const wx=x+27+q*48;const lit=((q+f+Math.floor(b.x/90))%8===0)||((q+2*f)%13===0);px(wx,fy-37,26,29,lit?'#5c5748':'#0a0e10');px(wx+3,fy-33,20,22,lit?'#806f4f':'#171c1e');if(lit){px(wx+6,fy-29,5,8,'#b09b67');px(wx+14,fy-29,5,8,'#8c7a55');}}}const door=makeBuildingDoor(b);const dx=door.left-camera;px(dx,GROUND-73,door.right-door.left,73,'#07090a');px(dx+5,GROUND-67,door.right-door.left-10,67,'#121718');px(dx+8,GROUND-52,3,3,'#777052');px(dx+door.right-door.left-11,GROUND-52,3,3,'#777052');for(let q=0;q<Math.floor(b.w/120);q++){const ax=x+22+q*120;px(ax,GROUND-h+20,46,11,'#1b2021');px(ax+8,GROUND-h+8,31,12,'#15191a');if(q%2===0)px(ax+9,GROUND-h+31,18,4,'#4a4037');}if(b.type==='police'){px(x+18,GROUND-h+17,b.w-36,25,'#182023');ctx.font='bold 13px Consolas';ctx.fillStyle='#c6c4ba';ctx.fillText('POLICE',x+30,GROUND-h+35);px(x+b.w-62,GROUND-h+23,28,10,'#4a5558');}if(b.type==='hospital'){px(x+b.w/2-66,GROUND-h+16,132,35,'#3a4648');px(x+b.w/2-8,GROUND-h+21,16,24,'#d1d4cf');px(x+b.w/2-24,GROUND-h+29,48,8,'#d1d4cf');}if(b.type==='funeral'){px(x+22,GROUND-h+18,b.w-44,26,'#181d1e');ctx.font='12px Consolas';ctx.fillStyle='#929892';ctx.fillText('MERCY FUNERAL',x+34,GROUND-h+36);}if(b.type==='research'){px(x+b.w/2-100,GROUND-h+15,200,28,'#101719');ctx.font='11px Consolas';ctx.fillStyle='#aab1ac';ctx.fillText('ECLIPSE RESEARCH ANNEX',x+b.w/2-85,GROUND-h+33);}if(b.type==='apartment'){for(let q=0;q<4;q++){px(x+40+q*110,GROUND-h+65,52,7,'#33393a');px(x+57+q*110,GROUND-h+53,18,8,'#4d4c45');}}}}
function drawStreetDebris(){if(interior)return;for(let i=0;i<45;i++){const wx=95+i*173;const x=wx-camera;if(x<-60||x>W+60)continue;const y=GROUND-4-(i%4)*2;if(i%4===0){px(x,y,18,7,'#343735');px(x+4,y-5,8,5,'#4b4b43');}else if(i%4===1){px(x,y,27,4,'#4f514c');px(x+7,y-5,10,5,'#262a29');}else if(i%4===2){px(x,y,9,11,'#55524c');px(x+9,y+3,12,5,'#343634');}else{px(x,y,5,5,'#6e6b62');px(x+6,y-1,3,3,'#575650');}}}
function drawSFStreetProps(){if(chapter!=='SAN FRANCISCO')return;for(let i=0;i<28;i++){const wx=150+i*315;const x=wx-camera;if(x<-140||x>W+140)continue;const poleH=118+(i%5)*20;px(x,GROUND-poleH,7,poleH,'#15191b');px(x-13,GROUND-poleH,32,6,'#252b2d');if(i%3===0){px(x+8,GROUND-poleH+9,27,6,'#4b4438');px(x+17,GROUND-poleH+4,8,12,'#62543d');}if(i%4===0){px(x-61,GROUND-35,78,24,'#202527');px(x-68,GROUND-12,91,9,'#0b0e10');px(x-50,GROUND-32,15,9,'#3e4648');px(x+5,GROUND-32,15,9,'#3e4648');px(x-48,GROUND-5,14,5,'#050607');px(x+16,GROUND-5,14,5,'#050607');}if(i%6===0){px(x+27,GROUND-86,25,52,'#303735');px(x+20,GROUND-94,40,9,'#3a4540');px(x+32,GROUND-106,15,12,'#111516');}if(i%7===0){px(x-90,GROUND-10,58,8,'#2b2e2e');px(x-82,GROUND-18,12,8,'#56524b');px(x-68,GROUND-20,8,6,'#4b4944');}}
for(let i=0;i<18;i++){const x=(i*227-camera*.18)%W;const y=GROUND-10-(i%3)*20;px(x,y,70,7,'#202526');px(x+10,y-4,47,4,'#343837');if(i%2===0)px(x+25,y-10,12,5,'#49473f');}}
function drawAlcatrazProps(){if(chapter!=='ALCATRAZ')return;for(let i=0;i<18;i++){const wx=220+i*280;const x=wx-camera;if(x<-80||x>W+80)continue;px(x,GROUND-93,7,93,'#15191a');for(let j=0;j<5;j++)line(x+7+j*9,GROUND-93,x+3+j*9,GROUND-46,'#424747',2);px(x-13,GROUND-129,36,5,'#4a4d4b');if(i%4===0){px(x-27,GROUND-30,74,7,'#3a3a35');px(x-19,GROUND-38,56,8,'#202424');}}for(let i=0;i<9;i++){const x=290+i*510-camera*.72;px(x,GROUND-160,96,8,'#171a1b');px(x+7,GROUND-152,7,92,'#292e2e');px(x+76,GROUND-152,7,92,'#292e2e');line(x+8,GROUND-149,x+47,GROUND-180,'#454a48',2);line(x+74,GROUND-149,x+47,GROUND-180,'#454a48',2);}}
function drawEnhancedSky(){const sf=chapter==='SAN FRANCISCO';const g=ctx.createLinearGradient(0,0,0,440);g.addColorStop(0,sf?'#05070d':'#05080d');g.addColorStop(.55,sf?'#0b1117':'#0b1216');g.addColorStop(1,sf?'#1a2027':'#161d21');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);for(let i=0;i<140;i++){const x=(i*139-camera*.14)%W;const y=(i*47)%360;px(x,y,1+(i%3),1+(i%2),i%17===0?'#788087':i%5===0?'#303a40':'#182126');}drawPixelClouds();if(sf){for(let i=0;i<22;i++){const x=i*98-(camera*.085%130);const h=88+(i%7)*29;px(x,382-h,72,h,'#10161b');for(let q=0;q<5;q++)for(let w=0;w<3;w++)if((i+q+w)%4===0){px(x+9+w*20,394-h+14+q*29,6,10,'#514d42');px(x+10+w*20,395-h+14+q*29,3,5,'#6a5d45');}}drawGoldenGate();}else{drawDistantOcean();for(let i=0;i<8;i++){const x=40+i*185-camera*.06;px(x,270-(i%2)*16,120,110,'#141b1f');px(x+16,252-(i%2)*16,90,16,'#222a2d');px(x+35,236-(i%3)*13,50,15,'#101618');}}}
function drawEnhancedWeather(){if(interior)return;for(let i=0;i<280;i++){const x=(i*41+totalTime*310-camera*.72)%W;const y=(i*73+totalTime*455)%440;line(x,y,x-7,y+20,'rgba(169,187,195,.34)',1);}if(chapter==='SAN FRANCISCO'){for(let i=0;i<50;i++){const x=(i*87-camera*.8)%W;const y=GROUND-6+(i%4)*4;px(x,y,3,2,'#4b5050');}}else{for(let i=0;i<32;i++){const x=(i*97-camera*.6)%W;const y=GROUND-6+(i%5)*3;px(x,y,4,2,'#495052');}}}
function drawEnhancedInterior(){const b=interior.building;const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#080b0d');g.addColorStop(.45,'#1b2021');g.addColorStop(1,'#090c0d');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);px(0,510,W,210,'#090c0d');for(let i=0;i<22;i++){px(i*62,74,45,5,i%4?'#323737':'#4d514e');px(i*62+14,79,4,431,'#202526');}for(let i=0;i<12;i++){const x=45+i*107;px(x,130,68,6,'#111516');px(x+7,138,54,27,'#262b2c');if(i%3===0){px(x+17,151,38,6,'#5c513f');px(x+33,159,6,5,'#7b6547');}}px(574,78,8,438,'#0a0d0e');px(566,84,24,6,'#3c403e');const doorX=590;px(doorX-52,390,104,122,'#101415');px(doorX-44,402,88,110,'#222728');px(doorX-3,433,5,5,'#6c6556');px(60,410,225,103,'#171b1c');px(45,378,255,35,'#3e4444');px(88,333,90,45,'#0c1012');px(760,419,202,94,'#332f2b');px(780,374,154,43,'#292d2e');px(807,386,20,9,'#56584e');px(1085,404,74,110,'#1f2526');for(let i=0;i<4;i++){px(1092,419+i*25,58,6,'#5b605c');}ctx.font='bold 17px Consolas';ctx.fillStyle='#8e3a3c';ctx.fillText(b.name.toUpperCase(),250,300);ctx.font='12px Consolas';ctx.fillStyle='#7f8884';ctx.fillText(`FLOOR ${floor}`,588,110);for(let i=0;i<8;i++){const x=335+i*120;px(x,218,48,5,'#494c48');px(x+11,226,26,14,'#272b2b');if(i%3===0)px(x+18,210,9,8,'#58544b');}if(floor>=2){px(400,108,62,252,'#171b1c');px(813,108,62,252,'#171b1c');px(400,108,475,6,'#363a3a');for(let i=0;i<5;i++){px(428+i*82,150,48,6,'#4a4d49');px(440+i*82,165,24,32,'#1c2222');}}if(floor>=3){for(let i=0;i<4;i++){px(280+i*190,145,112,85,'#111516');px(294+i*190,162,86,10,'#4f534f');px(310+i*190,184,54,34,'#242829');}}}
function drawEnhancedPlayer(){const x=player.x-camera;const bounce=player.onGround?Math.sin(player.anim)*1.25:-physicsState.impact*3;ctx.save();if(player.hitTimer>0&&Math.floor(totalTime*28)%2===0)ctx.globalAlpha=.45;drawCharacterSprite(x+8,player.y+bounce,selectedCharacter,player.facing,player.anim,'');const gunX=x+27*player.facing;const gunY=player.y+39+bounce;line(gunX,gunY,gunX+33*player.facing,gunY-3,'#0e1214',7);line(gunX+2*player.facing,gunY-4,gunX+27*player.facing,gunY-4,'#7b7e77',2);px(gunX+7*player.facing,gunY-7,9,4,'#353938');if(player.shootTimer>0)poly([[gunX+29*player.facing,gunY-7],[gunX+57*player.facing,gunY-14],[gunX+47*player.facing,gunY],[gunX+57*player.facing,gunY+7],[gunX+29*player.facing,gunY+3]],'#f0d27c');ctx.restore();}
function drawEnhancedInteriorPlayer(){drawCharacterSprite(player.x,player.y,selectedCharacter,player.facing,player.anim,'');const gunX=player.x+27*player.facing;}
function updateParticles(dt){for(const p of particles){p.life-=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;if(p.vy<380)p.vy+=420*dt;}particles=particles.filter(p=>p.life>0);}
function drawParticles(){for(const p of particles){const x=p.x-camera;ctx.save();ctx.globalAlpha=clamp(p.life*2,0,1);px(x,p.y,p.size,p.size,p.c);ctx.restore();}}
function drawLighting(){if(interior)return;if(state.light){const pxs=player.x-camera;const cone=ctx.createRadialGradient(pxs+player.facing*90,player.y+26,12,pxs+player.facing*90,player.y+26,260);cone.addColorStop(0,'rgba(255,239,185,.16)');cone.addColorStop(.36,'rgba(255,226,162,.07)');cone.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=cone;ctx.fillRect(0,0,W,H);}const fog=ctx.createLinearGradient(0,320,0,520);fog.addColorStop(0,'rgba(170,178,178,0)');fog.addColorStop(1,'rgba(120,130,132,.055)');ctx.fillStyle=fog;ctx.fillRect(0,250,W,300);}
function drawWorld(){drawEnhancedSky();drawEnhancedGround();chapter==='SAN FRANCISCO'?drawSFStreetProps():drawAlcatrazProps();drawStreetDebris();drawEnhancedStructures();drawCellBlockAExterior();drawStartingCell();drawCellBlockAHint();drawEnhancedBloodWriting();drawEnhancedSkeletons();drawEnhancedChests();drawEnhancedLoot();drawEnhancedSurvivors();drawEnhancedZombies();for(const b of bullets){const x=b.x-camera;if(x>-30&&x<W+30){px(x-5,b.y-2,10,4,'#e6d28b');px(x+2,b.y-1,6,2,'#fff4c0');}}drawEnhancedPlayer();drawParticles();drawLighting();drawEnhancedSmiler();}
function drawInterior(){drawEnhancedInterior();drawInteriorLoot();drawEnhancedInteriorPlayer();drawParticles();}
function drawWeather(){drawEnhancedWeather();}
function update(dt){totalTime+=dt;infoFlashCooldown=Math.max(0,infoFlashCooldown-dt);if(mode==='play'&&!infoFlashOpen){infoFlashTimer-=dt;if(infoFlashTimer<=0){infoFlashTimer=32+Math.random()*42;showInfoFlash();}}updateMessage(dt);updatePlayer(dt);updateZombies(dt);updateSurvivors(dt);updateBullets(dt);updateHunger(dt);randomHorror(dt);updateSmiler(dt);triggerSmilerVision();updateParticles(dt);if(state.battery>0&&state.light)state.battery=Math.max(0,state.battery-dt*.25);if(state.sanity<=0)die('You could no longer tell what was real.');if(chapter==='ALCATRAZ'&&player.x>4100&&state.dockPass){objectiveStep=5;setObjective();}if(chapter==='SAN FRANCISCO'&&survivorsFound>=3&&!archiveOpened)setObjective();flash=Math.max(0,flash-dt*2);shake=Math.max(0,shake-dt*10);camera=lerp(camera,player.x-W*.42,Math.min(1,dt*5));const maxCam=(chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH)-W;camera=clamp(camera,0,maxCam);drawHUD();}


let controlMode=window.matchMedia&&window.matchMedia('(pointer:coarse)').matches?'mobile':'laptop';
let startingCell=true;
let horrorPulse=0;
let horrorEyes=0;
let horrorMessageTimer=0;
let lastDoorBang=0;
function setControlMode(next){
 controlMode=next==='mobile'?'mobile':'laptop';
 document.body.dataset.controlMode=controlMode;
 const mob=document.getElementById('mobileControls');
 if(mob)mob.classList.toggle('hidden',controlMode!=='mobile'||mode!=='play');
}
function openModePicker(){
 const p=document.getElementById('modePicker');
 if(p)p.classList.remove('hidden');
}
function closeModePicker(){
 const p=document.getElementById('modePicker');
 if(p)p.classList.add('hidden');
 setControlMode(controlMode);
}
const savedControlMode=null;
function addMobileKey(key,pressed){
 const k=key==='shift'?'Shift':key==='space'?' ':key;
 if(pressed)keys.add(k);else keys.delete(k);
}
function triggerMobileAction(a){
 if(mode!=='play'||gadgetOpen)return;
 if(a==='shoot')shoot();
 else if(a==='e')interact();
 else if(a==='q'){for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<86){z.hp-=55;z.hit=.15;shake=5;if(z.hp<=0)z.dead=true;setMsg('MELEE HIT',.5);}}}
 else if(a==='f'){state.light=!state.light;setMsg(state.light?'Flashlight on.':'Flashlight off.',1);}
 else if(a==='g'&&state.grenades>0){state.grenades--;for(const z of zombies){if(!z.dead&&Math.abs(z.x-player.x)<280)z.hp-=120;}flash=.2;shake=11;scareSound();setMsg('GRENADE',1);}
 else if(a==='h')useItem();
 else if(a==='i')inventoryOpen=!inventoryOpen;
 else if(a==='r')reload();
}
function setupMobileControls(){
 document.querySelectorAll('#mobileControls [data-key]').forEach(btn=>{
  const k=btn.dataset.key;
  const down=e=>{e.preventDefault();if(k==='w'&&mode==='play'){keys.add('w');}else addMobileKey(k,true);if(btn.setPointerCapture&&e.pointerId!==undefined){try{btn.setPointerCapture(e.pointerId)}catch(err){}}};
  const up=e=>{e.preventDefault();if(k==='w')keys.delete('w');else addMobileKey(k,false);};
  btn.addEventListener('pointerdown',down);btn.addEventListener('pointerup',up);btn.addEventListener('pointercancel',up);btn.addEventListener('pointerleave',up);
 });
 document.querySelectorAll('#mobileControls [data-action]').forEach(btn=>btn.addEventListener('pointerdown',e=>{e.preventDefault();triggerMobileAction(btn.dataset.action);}));
}
function positionAtCell(){
 startingCell=true;
 interior=null;
 floor=1;
 camera=0;
 player.x=175;
 player.y=GROUND-player.h;
 player.vx=0;
 player.vy=0;
 player.facing=1;
 state.startEscaped=false;
}
function drawCellBlockAExterior(){
 if(chapter!=='ALCATRAZ'||interior)return;
 const b=buildings.find(v=>v.name==='CELL BLOCK A');
 if(!b)return;
 const x=b.x-camera;
 const h=288;
 const base=GROUND-h;
 px(x,base,b.w,h,'#22282a');
 px(x,base,b.w,9,'#4b5252');
 px(x+12,base+12,b.w-24,7,'#101416');
 for(let row=0;row<2;row++){
  const y=base+58+row*93;
  for(let col=0;col<15;col++){
   const wx=x+28+col*78;
   if(wx>x+b.w-35)continue;
   px(wx,y,58,55,'#0a0d0e');
   px(wx+6,y+6,46,6,'#2c3233');
   px(wx+7,y+13,3,35,'#69706c');
   px(wx+18,y+13,3,35,'#4b5250');
   px(wx+29,y+13,3,35,'#69706c');
   px(wx+40,y+13,3,35,'#4b5250');
   px(wx+51,y+13,3,35,'#69706c');
   if((col+row)%7===0)px(wx+12,y+19,24,12,'#433b33');
  }
 }
 for(let col=0;col<16;col++){
  const wx=x+18+col*78;
  px(wx,base+53,5,188,'#3b4241');
  px(wx+35,base+53,4,188,'#292f30');
 }
 const doorX=x+302;
 const open=state.startEscaped||startingCell===false;
 px(doorX,GROUND-88,70,88,'#090b0c');
 if(open){
  px(doorX+8,GROUND-78,8,68,'#4b514f');
  px(doorX+18,GROUND-78,6,68,'#303736');
  px(doorX+52,GROUND-78,6,68,'#303736');
 }else{
  px(doorX+8,GROUND-78,54,68,'#1b2021');
  for(let q=0;q<5;q++)px(doorX+12+q*10,GROUND-76,4,64,'#6a706d');
 }
 px(doorX+61,GROUND-48,5,5,'#847657');
 ctx.font='bold 11px Consolas';ctx.fillStyle='#a24945';ctx.fillText('CELL A-17',doorX-3,GROUND-98);
 ctx.font='10px Consolas';ctx.fillStyle=open?'#9aa19b':'#6f7571';ctx.fillText(open?'DOOR OPEN':'LOCKED',doorX+6,GROUND-8);
 px(x+690,base+18,155,26,'#151a1b');
 ctx.font='bold 13px Consolas';ctx.fillStyle='#b9b6aa';ctx.fillText('CELL BLOCK A',x+706,base+36);
 for(let i=0;i<5;i++){
  const bx=x+880+i*55;
  px(bx,GROUND-206,38,6,'#313839');
  px(bx+6,GROUND-200,5,85,'#4c5251');
  px(bx+27,GROUND-200,5,85,'#303636');
 }
 if(!state.startEscaped){
  ctx.fillStyle='rgba(25,0,0,.17)';ctx.fillRect(doorX-26,GROUND-140,122,120);
 }
}

function drawStartingCell(){
 if(chapter!=='ALCATRAZ'||!startingCell||interior)return;
 const x=-20-camera;
 px(x,GROUND-222,360,222,'#171b1d');
 px(x,GROUND-230,360,9,'#303536');
 px(x+18,GROUND-204,300,8,'#0b0e0f');
 px(x+34,GROUND-160,110,52,'#252a2b');
 px(x+46,GROUND-176,85,16,'#3d4140');
 px(x+54,GROUND-188,58,14,'#686158');
 px(x+190,GROUND-61,64,49,'#111516');
 px(x+206,GROUND-77,34,17,'#303334');
 px(x+24,GROUND-199,7,136,'#333838');
 px(x+75,GROUND-199,7,136,'#333838');
 px(x+126,GROUND-199,7,136,'#333838');
 px(x+177,GROUND-199,7,136,'#333838');
 px(x+228,GROUND-199,7,136,'#333838');
 px(x+279,GROUND-199,7,136,'#333838');
 for(let i=0;i<7;i++){
  line(x+18+i*48,GROUND-201,x+37+i*48,GROUND-59,'#494e4e',2);
  line(x+37+i*48,GROUND-59,x+18+i*48,GROUND-201,'#272c2d',1);
 }
 px(x+304,GROUND-186,24,125,'#080a0b');
 px(x+310,GROUND-174,11,108,'#202526');
 px(x+314,GROUND-124,5,6,'#8b7856');
 px(x+48,GROUND-56,32,6,'#16191a');
 px(x+62,GROUND-63,13,6,'#4a4740');
 px(x+15,GROUND-38,24,5,'#5c2325');
 for(let i=0;i<9;i++)px(x+12+i*31,GROUND-31-(i%3)*5,7+(i%4)*4,2,i%2?'#501b1e':'#641f21');
 ctx.font='bold 12px Consolas';ctx.fillStyle='#9a4140';ctx.fillText('A-17',x+257,GROUND-115);
 ctx.font='10px Consolas';ctx.fillStyle='#777d7a';ctx.fillText('MATTRESS',x+48,GROUND-193);
 ctx.fillStyle='#7d3032';ctx.fillText('DO NOT LET HIM SEE YOU',x+34,GROUND-246);
}
function enhancedStartAudio(){audio();tone(38,.7,'sine',.025,-12);setTimeout(()=>tone(27,1.1,'sine',.02,-4),180);}
function startGame(name){
 selectedCharacter=name;
 resetWorld();
 buildAlcatraz();
 positionAtCell();
 mode='intro';
 cutIndex=0;
 cutTimer=0;
 hide('menu');
 hide('hud');
 hide('pause');
 hide('ending');
 hide('death');
 show('cutscene');
 const line=document.getElementById('cutline');
 if(line)line.textContent=cutsceneLines[0];
 setControlMode(controlMode);
 enhancedStartAudio();
}
function finishIntro(){
 mode='play';
 startingCell=true;
 positionAtCell();
 hide('cutscene');
 show('hud');
 setObjective();
 setMsg('CELL A-17. Find the key beneath the mattress.',3);
 showWarning('DO NOT OPEN THE DOOR YET');
 setControlMode(controlMode);
 horrorPulse=1;
}
function interact(){
 if(mode!=='play'||gadgetOpen)return;
 if(chapter==='ALCATRAZ'&&startingCell&&!state.startEscaped){
  if(player.x<235){
   if(!state.startKey){state.startKey=true;state.keys++;setMsg('A brass key was taped beneath the mattress.',2.5);state.sanity=Math.max(0,state.sanity-1);tone(250,.18,'triangle',.03,25);}
   else setMsg('Nothing else is beneath the mattress.',1.1);
   return;
  }
  if(player.x>=235){
   if(state.startKey||state.keys>0){state.startEscaped=true;state.keys=Math.max(0,state.keys-1);startingCell=false;objectiveStep=1;setObjective();setMsg('CELL A-17 UNLOCKED. Do not look into the corridor.',2.8);scareSound();shake=7;return;}
   setMsg('The cell is locked. Find the key under the mattress.',1.7);return;
  }
 }
 const l=currentLoot();
 if(l){l.taken=true;addItem(l.item,l.count);setMsg(`Picked up ${itemName(l.item)} x${l.count}`,1.2);return;}
 if(interior){
  if(player.x>1100){exitBuilding();return;}
  if(Math.abs(player.x-620)<78){floor=floor===1?2:1;player.x=170;setMsg(`STAIRS — FLOOR ${floor}`,1.2);tone(130,.25,'square',.04,-20);return;}
  if(player.x>760&&player.x<900){addChest(820,480,false,true);const c=chests[chests.length-1];if(!c.opened){openChest(c);return;}}
  return;
 }
 const c=currentCell();
 if(c){
  if(!c.open){if(state.keys>0){state.keys--;c.open=true;setMsg(`${c.id} unlocked.`,1.2);}else setMsg('Locked. Search for a key.',1.5);return;}
  if(!c.searched){c.searched=true;state.sanity=Math.max(0,state.sanity-2);if(c.id==='B-4'){state.dockPass=true;objectiveStep=4;setMsg('The Medical Wing should have the Dock Pass.',2.4);addItem('ammo',8);}else{const roll=Math.random();if(roll<.4)addItem('bandage',1);else if(roll<.7)addItem('ammo',6);else addItem('scrap',randi(1,3));setMsg('Cell searched.',1);}}return;
 }
 const ch=currentChest();if(ch){openChest(ch);return;}
 const b=currentBuilding();
 if(b&&player.x>b.x+20&&player.x<b.x+b.w-20){insideBuilding(b);return;}
 if(chapter==='ALCATRAZ'&&player.x>3850&&state.dockPass){enterSF();return;}
 if(chapter==='SAN FRANCISCO'){
  for(const sv of survivors){if(!sv.found&&Math.abs(player.x-sv.x)<65){sv.found=true;survivorsFound++;sv.follow=true;state.sanity=Math.min(100,state.sanity+8);setMsg(`${sv.name}: "Stay close. We need the others."`,2.5);setObjective();return;}}
  if(player.x>5250&&player.x<5970&&survivorsFound>=3){archiveOpened=true;setMsg('ARCHIVE OPENED. The files mention a ferry route.',3);setObjective();return;}
  if(player.x>4420&&player.x<5040&&survivorsFound>=3&&archiveOpened){shelterReached=true;win('Mara, Eli and Noah reached the shelter. The city is still screaming beyond the doors, but you made it through the night.');}
 }
}
function updateSmarterHorror(dt){
 if(mode!=='play')return;
 horrorPulse=Math.max(0,horrorPulse-dt*.45);
 horrorMessageTimer=Math.max(0,horrorMessageTimer-dt);
 lastDoorBang=Math.max(0,lastDoorBang-dt);
 if(smiler.active&&Math.abs(smiler.x-player.x)<600){state.sanity=Math.max(0,state.sanity-dt*1.15);horrorPulse=Math.max(horrorPulse,.5);}
 if(state.sanity<65&&Math.random()<dt*.012){horrorEyes=1.2;setMsg('You heard a second set of footsteps.',1.1);tone(44,.45,'sine',.018,-5);}
 if(state.sanity<42&&Math.random()<dt*.006){horrorEyes=1.8;showWarning(Math.random()<.5?'DON’T TURN AROUND':'HE IS CLOSER NOW');scareSound();shake=5;}
 if(chapter==='ALCATRAZ'&&startingCell&&!state.startEscaped&&Math.random()<dt*.003){if(lastDoorBang<=0){lastDoorBang=3;tone(48,.12,'square',.035,-5);setMsg('Something touched the cell bars.',1.3);horrorPulse=.75;}}
 if(chapter==='ALCATRAZ'&&state.startEscaped&&Math.random()<dt*.0025){horrorEyes=1.4;showWarning('SOMEONE IS STANDING AT THE FAR END');}
 if(chapter==='SAN FRANCISCO'&&Math.random()<dt*.002){spawnZombie(clamp(player.x+rand(-650,650),120,SF_WIDTH-120),Math.random()<.22?'runner':'walker');}
}
function drawStartingCellOverlay(){
 if(chapter!=='ALCATRAZ'||!startingCell||state.startEscaped||interior)return;
 const cx=318-camera;
 ctx.save();ctx.fillStyle='rgba(0,0,0,.5)';ctx.fillRect(0,0,360,430);
 ctx.fillStyle='#0a0c0d';ctx.fillRect(cx,0,10,GROUND);
 ctx.fillStyle='#373b3b';ctx.fillRect(cx-2,0,3,GROUND);ctx.fillRect(cx+18,0,3,GROUND);ctx.fillRect(cx+38,0,3,GROUND);ctx.fillRect(cx+58,0,3,GROUND);
 ctx.fillStyle='#4b4f4e';ctx.fillRect(cx-4,GROUND-155,66,4);
 ctx.fillStyle='#080909';ctx.fillRect(cx+2,GROUND-154,57,151);
 ctx.fillStyle='#1d2222';ctx.fillRect(cx+10,GROUND-142,40,131);
 ctx.fillStyle='#716e61';ctx.fillRect(cx+43,GROUND-78,5,5);
 for(let i=0;i<5;i++){ctx.fillStyle='#343737';ctx.fillRect(cx+7+i*12,GROUND-150,3,148);}
 ctx.fillStyle='rgba(150,25,28,.22)';ctx.fillRect(cx+4,GROUND-210,57,5);
 ctx.restore();
}
function drawCellBlockAHint(){if(chapter!=='ALCATRAZ'||interior||!state.startEscaped||player.x>760)return;ctx.save();ctx.globalAlpha=.7;ctx.font='10px Consolas';ctx.fillStyle='#737a76';ctx.fillText('CELL BLOCK A // A-17 BEHIND YOU',24,GROUND-252);ctx.restore();}
function drawHorrorOverlay(){
 if(mode!=='play')return;
 if(horrorPulse>0){ctx.fillStyle=`rgba(35,0,6,${horrorPulse*.08})`;ctx.fillRect(0,0,W,H);}
 if(horrorEyes>0){
  const edge=smiler.active?smiler.x-camera:(player.facing>0?W-75:75);
  ctx.save();ctx.globalAlpha=Math.min(1,horrorEyes/1.2)*.7;ctx.fillStyle='#010101';ctx.fillRect(edge-34,195,68,235);ctx.fillStyle='#e4dfd2';ctx.fillRect(edge-17,229,7,5);ctx.fillRect(edge+10,229,7,5);ctx.fillStyle='#050505';ctx.fillRect(edge-21,250,42,45);ctx.restore();
 }
 if(interior&&blackout>0.2){ctx.fillStyle=`rgba(0,0,0,${clamp(blackout/2.4,0,.9)})`;ctx.fillRect(0,0,W,H);}
 if(state.sanity<55){ctx.save();ctx.globalAlpha=(55-state.sanity)/420;for(let i=0;i<11;i++){const y=100+i*47+Math.sin(totalTime*4+i)*5;ctx.fillStyle='#b6a7a0';ctx.fillRect((i*137+totalTime*70)%W,y,16,1);}ctx.restore();}
}
function draw(){
 ctx.save();
 const sx=shake?(Math.random()*shake-shake/2):0;
 ctx.translate(sx,0);
 ctx.fillStyle='#06090b';ctx.fillRect(0,0,W,H);
 if(interior)drawInterior();else drawWorld();
 drawWeather();
 drawHorrorOverlay();
 if(flash>0){ctx.fillStyle=`rgba(255,245,230,${flash})`;ctx.fillRect(0,0,W,H);}
 if(state.sanity<45){ctx.fillStyle=`rgba(30,5,15,${(45-state.sanity)/180})`;ctx.fillRect(0,0,W,H);}
 ctx.restore();
}
function update(dt){
 totalTime+=dt;
 infoFlashCooldown=Math.max(0,infoFlashCooldown-dt);
 if(mode==='play'&&!infoFlashOpen){infoFlashTimer-=dt;if(infoFlashTimer<=0){infoFlashTimer=46+Math.random()*52;showInfoFlash();}}
 updateMessage(dt);
 updatePlayer(dt);
 updateZombies(dt);
 updateSurvivors(dt);
 updateBullets(dt);
 updateHunger(dt);
 randomHorror(dt);
 updateSmiler(dt);
 updateSmarterHorror(dt);
 triggerSmilerVision();
 updateParticles(dt);
 if(state.battery>0&&state.light)state.battery=Math.max(0,state.battery-dt*.22);
 if(state.sanity<=0)die('You could no longer tell what was real.');
 if(chapter==='ALCATRAZ'&&player.x>4100&&state.dockPass){objectiveStep=5;setObjective();}
 if(chapter==='SAN FRANCISCO'&&survivorsFound>=3&&!archiveOpened)setObjective();
 flash=Math.max(0,flash-dt*2);shake=Math.max(0,shake-dt*10);
 const maxCam=(chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH)-W;
 const targetCamera=startingCell?0:player.x-W*.42+enhCamLead;
 camera=lerp(camera,targetCamera,Math.min(1,dt*6));
 camera=clamp(camera,0,maxCam);
 drawHUD();
}
function renderLoop(){requestAnimationFrame(renderLoop);const now=performance.now();const dt=Math.min(.035,(now-last)/1000);last=now;if(mode==='play'||mode==='pause')update(dt);draw();}
function setupModeUi(){
 document.querySelectorAll('#modePicker [data-mode]').forEach(b=>b.onclick=()=>{setControlMode(b.dataset.mode);closeModePicker();});
 const auto=document.getElementById('modeAuto');if(auto)auto.onclick=()=>{controlMode=window.matchMedia&&window.matchMedia('(pointer:coarse)').matches?'mobile':'laptop';closeModePicker();};
 const reopen=document.getElementById('privacyReopen');if(reopen)reopen.onclick=openPrivacyDashboard;
 const modeOpen=document.getElementById('controlModeOpen');if(modeOpen)modeOpen.onclick=openModePicker;
 setupMobileControls();
 setControlMode(controlMode);
}
setupModeUi();


document.getElementById('privacyClose').onclick=closePrivacyDashboard;
document.addEventListener('visibilitychange',()=>{if(document.hidden){keys.clear();mouse.down=false;}});

let chestUIOpen=false;
let chestTarget=null;
let jumpPulse=false;
let jumpCount=0;
let jumpWasGrounded=true;
let cinematicPulse=0;
let foregroundPulse=0;
const chestCatalog={ammo:{name:'9MM ROUNDS',icon:'▣',value:1,display:'AMMO'},bandage:{name:'BANDAGE',icon:'✚',value:1,display:'BAND'},medkit:{name:'MEDKIT',icon:'✚',value:2,display:'MED'},food:{name:'RATION',icon:'◆',value:1,display:'FOOD'},scrap:{name:'SCRAP',icon:'◇',value:1,display:'SCRP'},battery:{name:'BATTERY',icon:'▰',value:1,display:'CELL'}};
function chestMake(c){
 if(c.contents)return c.contents;
 const seed=Math.floor(Math.abs(c.x*13+(c.rare?71:19)));
 const randLocal=n=>((seed*9301+n*49297)%233280)/233280;
 const slots=new Array(27).fill(null);
 const put=(id,count,index)=>{slots[index]={id,count};};
 put('ammo',c.rare?24:10,2+(seed%5));
 put('bandage',c.rare?3:1,8);
 put(c.rare?'medkit':'food',c.rare?1:2,13);
 put('scrap',c.rare?7:3,17);
 if(c.rare)put('battery',2,21);
 if(randLocal(3)>.45)put('food',1,24);
 c.contents=slots;
 return slots;
}
function chestPlayerStacks(){
 const stacks=[];
 const add=(id,count)=>{if(count<=0)return;stacks.push({id,count});};
 add('ammo',state.ammoReserve);add('bandage',state.bandages);add('medkit',state.medkits);add('food',state.food);add('scrap',state.scrap);add('battery',Math.floor(state.battery/20));add('grenade',state.grenades);add('key',state.keys);return stacks;
}
function chestAddState(id,count){if(id==='grenade')state.grenades+=count;else if(id==='key')state.keys+=count;else addItem(id,count);}
function chestSetStatus(t){const f=document.getElementById('chestFooter');if(f)f.textContent=t;}
function drawChestSlots(){
 const c=chestTarget;if(!c)return;
 const slots=document.getElementById('chestSlots');const ps=document.getElementById('playerSlots');if(!slots||!ps)return;
 slots.innerHTML='';ps.innerHTML='';
 const data=chestMake(c);
 for(let i=0;i<27;i++){
  const item=data[i];const el=document.createElement('button');el.className='slot'+(item?'':' empty');el.type='button';
  if(item){const d=chestCatalog[item.id]||{name:item.id.toUpperCase(),icon:'?',display:item.id.toUpperCase()};el.innerHTML='<span class="slotIcon">'+d.icon+'</span><span class="slotCount">'+item.count+'</span><span class="slotName">'+d.display+'</span>';if(c.rare)el.classList.add('rare');el.title=d.name+' x'+item.count;el.onclick=()=>takeChestSlot(i);}
  slots.appendChild(el);
 }
 const pitems=chestPlayerStacks();
 for(let i=0;i<27;i++){
  const item=pitems[i];const el=document.createElement('button');el.className='slot'+(item?'':' empty');el.type='button';
  if(item){const d=chestCatalog[item.id]||({name:item.id.toUpperCase(),icon:'◆',display:item.id.toUpperCase()});el.innerHTML='<span class="slotIcon">'+d.icon+'</span><span class="slotCount">'+item.count+'</span><span class="slotName">'+d.display+'</span>';el.title=d.name+' x'+item.count;}
  ps.appendChild(el);
 }
 const remaining=data.filter(Boolean).length;
 chestSetStatus((c.rare?'MILITARY CACHE':'SUPPLY CHEST')+' • '+remaining+' STACKS REMAINING • '+(remaining?'SEARCH THE WHOLE CHEST':'CHEST EMPTY'));
}
function openChestUI(c){
 chestTarget=c;
 chestMake(c);
 chestUIOpen=true;
 c.opened=true;
 const title=document.getElementById('chestTitle');if(title)title.textContent=c.rare?'MILITARY CACHE':'SUPPLY CHEST';
 const ui=document.getElementById('chestUI');if(ui){ui.style.display='grid';ui.classList.remove('hidden');}
 hide('pause');mode='chest';
 drawChestSlots();tone(c.rare?240:190,.2,'triangle',.035,25);shake=2;
}
function closeChestUI(){
 chestUIOpen=false;chestTarget=null;
 const ui=document.getElementById('chestUI');if(ui){ui.style.display='none';ui.classList.add('hidden');}
 mode='play';
}
function takeChestSlot(index){
 if(!chestTarget)return;
 const item=chestTarget.contents[index];if(!item)return;
 chestAddState(item.id,item.count);chestTarget.contents[index]=null;
 drawChestSlots();
 const p=document.getElementById('chestPanel');if(p){p.classList.remove('pixelPulse');void p.offsetWidth;p.classList.add('pixelPulse');}
 setMsg('TAKEN: '+(chestCatalog[item.id]?.name||item.id.toUpperCase())+' x'+item.count,1.1);
 tone(330,.08,'triangle',.018,45);
}
function takeAllChest(){
 if(!chestTarget)return;
 let moved=0;
 for(let i=0;i<chestTarget.contents.length;i++){const item=chestTarget.contents[i];if(item){chestAddState(item.id,item.count);moved+=item.count;chestTarget.contents[i]=null;}}
 drawChestSlots();setMsg(moved?'CHEST LOOT TRANSFERRED':'CHEST IS EMPTY',1.2);tone(300,.12,'triangle',.02,50);
}
function sortChest(){
 if(!chestTarget)return;
 const items=chestTarget.contents.filter(Boolean).sort((a,b)=>a.id.localeCompare(b.id));
 chestTarget.contents=items.concat(new Array(27-items.length).fill(null));drawChestSlots();tone(210,.1,'square',.016,30);
}
function upgradeChestSystem(){
 currentChest=function(){
  if(!chests.length||interior)return null;
  return chests.find(c=>Math.abs(c.x-player.x)<68&&(!c.opened||(c.contents&&c.contents.some(Boolean))))||null;
 };
 openChest=function(c){openChestUI(c);};
 const oldInteract=interact;
 interact=function(){
  if(mode!=='play'||gadgetOpen||chestUIOpen)return;
  const nearby=interior?chests.find(c=>c.inside&&Math.abs(c.x-player.x)<72):currentChest();
  if(nearby){openChestUI(nearby);return;}
  oldInteract();
 };
 const close=document.getElementById('chestClose');if(close)close.onclick=closeChestUI;
 const all=document.getElementById('takeAllChest');if(all)all.onclick=takeAllChest;
 const sort=document.getElementById('sortChest');if(sort)sort.onclick=sortChest;
}
function upgradeJumpSystem(){
 const oldUpdatePlayer=updatePlayer;
 updatePlayer=function(dt){
  const wasGrounded=player.onGround;
  oldUpdatePlayer(dt);
  if(player.onGround){jumpCount=0;jumpWasGrounded=true;}
  else if(wasGrounded){jumpCount=1;jumpWasGrounded=false;}
  if(jumpPulse){
   if(!wasGrounded&&!player.onGround&&jumpCount<2){
    player.vy=-485;player.onGround=false;jumpCount=2;stepParticles(player.x,player.y+player.h-3,9,'dust');tone(155,.1,'triangle',.025,70);shake=Math.max(shake,2);setMsg('DOUBLE JUMP',.55);
   }
   jumpPulse=false;
  }
  if(Math.abs(player.vy)>760)player.vy=player.vy>0?760:-760;
 };
 window.addEventListener('keydown',e=>{
  const k=e.key.length===1?e.key.toLowerCase():e.key;
  if(!e.repeat&&(k==='w'||k===' '||k==='ArrowUp'))jumpPulse=true;
 });
 document.querySelectorAll('#mobileControls [data-key="w"]').forEach(btn=>btn.addEventListener('pointerdown',()=>{jumpPulse=true;}));
}
function upgradeVisuals(){
 const oldDraw=draw;
 draw=function(){
  oldDraw();
  if(mode!=='menu'&&mode!=='intro'){
   ctx.save();
   const focus=player.x-camera;
   const moving=Math.abs(player.vx)>120;
   if(moving&&player.onGround){ctx.globalAlpha=.08;for(let i=0;i<4;i++)px(focus-player.facing*(18+i*9),player.y+18+i*10,3,2,'#b8b5a7');}
   const horizon=GROUND-110;
   for(let i=0;i<12;i++){const x=((i*139+totalTime*(8+(i%3)*3)-camera*.1)%W+W)%W;px(x,horizon+(i%5)*28,2+(i%3),1,i%3?'rgba(105,111,111,.12)':'rgba(175,174,161,.08)');}
   if(player.hitTimer>0){ctx.globalAlpha=.15;for(let i=0;i<7;i++){const x=focus+rand(-60,60);const y=player.y+rand(0,player.h);px(x,y,randi(1,3),randi(1,3),'#b44b46');}}
   if(state.sanity<38){ctx.globalAlpha=.11+Math.sin(totalTime*8)*.03;for(let i=0;i<18;i++){const x=(i*97+totalTime*170)%W;const y=80+(i*43)%480;px(x,y,1+(i%4),1,'#d3cac0');}}
   ctx.globalAlpha=.08;for(let y=0;y<H;y+=6)px(0,y,W,1,'#d8d8ce');
   ctx.globalAlpha=1;
   if(mode==='play'&&state.light&&controlMode==='laptop'){
    ctx.strokeStyle='rgba(220,216,188,.55)';ctx.lineWidth=1;ctx.strokeRect(mouse.x-5,mouse.y-5,10,10);px(mouse.x-1,mouse.y-1,3,3,'#e0d9b8');
   }
   ctx.restore();
  }
 };
}
function upgradeHorror(){
 const oldHorror=updateSmarterHorror;
 updateSmarterHorror=function(dt){
  oldHorror(dt);
  if(mode!=='play'||chestUIOpen)return;
  if(state.sanity<70&&Math.random()<dt*.008){cinematicPulse=.8;shake=Math.max(shake,2);tone(57,.35,'sine',.012,-9);}
  cinematicPulse=Math.max(0,cinematicPulse-dt*2.5);
  foregroundPulse=Math.max(0,foregroundPulse-dt*1.8);
  if(Math.random()<dt*.0016){foregroundPulse=.55;}
 };
 const oldDrawSmiler=drawEnhancedSmiler;
 drawEnhancedSmiler=function(){
  oldDrawSmiler();
  if(mode!=='play'||smiler.active||foregroundPulse<=0)return;
  const edge=player.facing>0?Math.min(W+60,player.x-camera+420):Math.max(-60,player.x-camera-420);
  ctx.save();ctx.globalAlpha=foregroundPulse*.35;px(edge-24,GROUND-175,48,116,'#020203');px(edge-33,GROUND-133,66,60,'#020203');px(edge-19,GROUND-209,38,41,'#010102');ctx.fillStyle='#d6d0c7';ctx.fillRect(edge-9,GROUND-190,5,3);ctx.fillRect(edge+6,GROUND-190,5,3);ctx.restore();
 };
}
function upgradeStartingCell(){
 const oldPosition=positionAtCell;
 positionAtCell=function(){
  oldPosition();
  player.x=165;player.y=GROUND-player.h;camera=0;startingCell=true;state.startEscaped=false;state.startKey=false;state.keys=0;
 };
 const oldDrawStart=drawStartingCell;
 drawStartingCell=function(){
  oldDrawStart();
  if(chapter!=='ALCATRAZ'||!startingCell||state.startEscaped||interior)return;
  const x=0-camera;
  for(let i=0;i<7;i++){
   const bx=x+34+i*47;
   px(bx,GROUND-214,6,210,'#4a4d4a');px(bx+2,GROUND-208,2,198,'#25292a');
  }
  px(x+7,GROUND-258,312,14,'#0e1112');px(x+18,GROUND-250,294,5,'#5a5650');
  px(x+30,GROUND-236,18,5,'#7a3a37');px(x+57,GROUND-230,13,4,'#7a3a37');px(x+78,GROUND-226,22,5,'#7a3a37');
  ctx.font='bold 16px Consolas';ctx.fillStyle='#7d3636';ctx.fillText('CELL BLOCK A',x+70,GROUND-268);ctx.font='10px Consolas';ctx.fillStyle='#7f8581';ctx.fillText('A-17 // ISOLATION',x+108,GROUND-118);
  const breathe=Math.sin(totalTime*2.7)*1.3;px(x+57,GROUND-114+breathe,92,12,'#706a5b');px(x+63,GROUND-104+breathe,83,9,'#514e46');px(x+71,GROUND-111+breathe,65,6,'#a0967e');
  if(!state.startKey){px(x+92,GROUND-118+breathe,9,5,'#c5a35d');px(x+102,GROUND-116+breathe,4,3,'#ead68c');}
  ctx.save();ctx.globalAlpha=.35+Math.sin(totalTime*1.4)*.08;ctx.fillStyle='#b7b0a7';ctx.fillRect(x+214,GROUND-233,2,31);ctx.restore();
 };
}
function activateFinalEnhancements(){upgradeChestSystem();upgradeJumpSystem();upgradeVisuals();upgradeHorror();upgradeStartingCell();}
activateFinalEnhancements();
let finalBoat={x:4050,y:548,w:144,h:42,lit:false,signal:0};
let finalHorrorPulse=0;
let finalWaterPhase=0;
let finalStepPhase=0;
let finalInsideChestCount=0;

const legacyBuildAlcatraz=buildAlcatraz;
const legacyBuildSanFrancisco=buildSanFrancisco;
const legacyPositionAtCell=positionAtCell;
const legacyDrawCharacterSprite=drawCharacterSprite;
const legacyDrawZombies=drawEnhancedZombies;
const legacyDrawSurvivors=drawEnhancedSurvivors;
const legacyDrawChests=drawEnhancedChests;
const legacyDrawInteriorLoot=drawInteriorLoot;
const legacyInsideBuilding=insideBuilding;
const legacyExitBuilding=exitBuilding;

function finalSetupLimitedChests(list){
 chests=chests.filter(c=>!c.inside).slice(0,2);
 for(const item of list){
  const b=buildings.find(x=>x.name===item.name);
  if(!b)continue;
  if(!chests.some(c=>c.inside&&c.buildingName===b.name))chests.push({x:item.x||780,y:GROUND-90,w:58,h:38,rare:!!item.rare,opened:false,inside:true,buildingName:b.name});
 }
}
function finalBuildAlcatrazV2(){
 legacyBuildAlcatraz();
 const block=buildings.find(b=>b.name==='CELL BLOCK A');
 if(block){block.x=0;block.w=1250;}
 const start=cells.find(c=>c.id==='A-17');
 if(start){start.x=170;start.open=true;start.searched=true;}
 else cells.push({x:170,id:'A-17',open:true,searched:true,block:0});
 skeletons=skeletons.slice(0,3);
 finalSetupLimitedChests([
  {name:'CELL BLOCK B',x:790,rare:true},
  {name:'MEDICAL WING',x:820,rare:false},
  {name:'WORKSHOP',x:820,rare:true}
 ]);
 finalBoat={x:4050,y:548,w:144,h:42,lit:false,signal:0};
}
function finalBuildSanFranciscoV2(){
 legacyBuildSanFrancisco();
 skeletons=[];
 finalSetupLimitedChests([
  {name:'HOSPITAL',x:820,rare:true},
  {name:'OLD HOTEL',x:790,rare:false},
  {name:'RESEARCH ANNEX',x:820,rare:true}
 ]);
}
buildAlcatraz=finalBuildAlcatrazV2;
buildSanFrancisco=finalBuildSanFranciscoV2;

function finalPositionAtCell(){
 legacyPositionAtCell();
 startingCell=true;
 camera=0;
 player.x=165;
 player.y=GROUND-player.h;
 player.vx=0;
 player.vy=0;
 player.onGround=true;
 player.facing=1;
 state.startEscaped=false;
 state.startKey=false;
 state.keys=0;
}
positionAtCell=finalPositionAtCell;

function finalInsideBuildingV2(b){
 if(!b)return;
 const side=player.x<(b.x+b.w*.5)?'left':'right';
 interior={building:b,entryX:player.x,entrySide:side};
 floor=1;
 player.x=side==='left'?105:1095;
 player.y=GROUND-player.h;
 player.vx=0;
 player.vy=0;
 if(['CELL BLOCK B','MEDICAL WING','WORKSHOP','HOSPITAL','OLD HOTEL','RESEARCH ANNEX'].includes(b.name)){
  const c=chests.find(x=>x.inside&&x.buildingName===b.name);
  if(c&&!c.contents)chestMake(c);
 }
 setMsg(`${b.name} — FLOOR 1 • FIND THE ROOM`,1.6);
 tone(105,.18,'square',.03,-18);
}
insideBuilding=finalInsideBuildingV2;

function finalExitBuildingV2(side){
 if(!interior)return;
 const b=interior.building;
 const chosen=side||(player.x<610?'left':'right');
 interior=null;
 floor=1;
 player.y=GROUND-player.h;
 player.vx=0;
 player.vy=0;
 player.x=chosen==='left'?Math.max(25,b.x-32):Math.min((chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH)-25,b.x+b.w+32);
 setMsg(`Exited ${b.name}.`,1.1);
}
exitBuilding=finalExitBuildingV2;

function finalCurrentBuildingV2(){
 if(interior)return null;
 let best=null;
 let bestDistance=99999;
 for(const b of buildings){
  const door=b.x+b.w*.5;
  const d=Math.abs(player.x-door);
  if(d<bestDistance&&d<205){best=b;bestDistance=d;}
 }
 return best;
}
currentBuilding=finalCurrentBuildingV2;

function finalCurrentChestV2(){
 if(interior){
  const name=interior.building.name;
  return chests.find(c=>c.inside&&c.buildingName===name&&c.contents&&c.contents.some(Boolean))||chests.find(c=>c.inside&&c.buildingName===name)||null;
 }
 return chests.find(c=>!c.inside&&Math.abs(c.x-player.x)<78&&(!c.contents||c.contents.some(Boolean)))||null;
}
currentChest=finalCurrentChestV2;

function finalInteractV2(){
 if(mode!=='play'||gadgetOpen||chestUIOpen)return;
 const nearbyLoot=currentLoot();
 if(nearbyLoot){nearbyLoot.taken=true;addItem(nearbyLoot.item,nearbyLoot.count);setMsg(`Picked up ${itemName(nearbyLoot.item)} x${nearbyLoot.count}`,1.1);stepParticles(player.x,player.y+40,5,'spark');return;}
 if(chapter==='ALCATRAZ'&&startingCell&&!state.startEscaped){
  if(player.x<230){
   if(!state.startKey){state.startKey=true;state.keys=1;setMsg('KEY FOUND UNDER THE MATTRESS.',2.3);stepParticles(player.x,GROUND-8,8,'spark');tone(270,.16,'triangle',.03,40);}
   else setMsg('Nothing else is under the mattress.',1);
  }else if(state.startKey||state.keys>0){
   state.startEscaped=true;startingCell=false;state.keys=Math.max(0,state.keys-1);player.x=Math.max(player.x,330);player.y=GROUND-player.h;player.vx=55;objectiveStep=1;setObjective();setMsg('CELL A-17 UNLOCKED. The corridor is watching.',2.6);finalHorrorPulse=.8;finalDoorFlash=1;shake=7;scareSound();
  }else setMsg('The cell is locked. Search under the mattress.',1.5);
  return;
 }
 if(interior){
  const c=finalCurrentChestV2();
  if(c&&Math.abs(c.x-player.x)<92){openChestUI(c);return;}
  if(player.x<75){finalExitBuildingV2('left');return;}
  if(player.x>1150){finalExitBuildingV2('right');return;}
  if(Math.abs(player.x-620)<115){floor=floor===1?2:1;player.x=170;setMsg(`STAIRS — FLOOR ${floor}`,1.15);stepParticles(620,500,9,'dust');tone(135,.18,'square',.03,-20);return;}
  return;
 }
 const c=finalCurrentChestV2();
 if(c&&Math.abs(c.x-player.x)<92){openChestUI(c);return;}
 if(chapter==='ALCATRAZ'&&state.dockPass&&player.x>3900){
  if(finalBoat.signal===0){finalBoat.signal=1;finalBoat.lit=true;objectiveStep=5;setObjective();setMsg('DOCK BEACON LIT. The ferry is waiting beyond the pier.',2.4);tone(180,.25,'triangle',.035,50);stepParticles(finalBoat.x,finalBoat.y,12,'spark');return;}
  if(player.x>3975){finalEnterSF();return;}
 }
 const b=finalCurrentBuildingV2();
 if(b){const d=b.x+b.w*.5;if(Math.abs(player.x-d)<205){finalInsideBuildingV2(b);return;}}
 const cell=currentCell();
 if(cell&&!startingCell){
  if(!cell.open){if(state.keys>0){state.keys--;cell.open=true;setMsg(`${cell.id} unlocked.`,1.1);}else setMsg('Locked. Search another cell first.',1.1);return;}
  if(!cell.searched){cell.searched=true;if(cell.id==='B-4'){state.dockPass=true;objectiveStep=4;addItem('ammo',8);setMsg('The Dock Pass is in the Medical Wing.',2.0);setObjective();}else{const r=Math.random();addItem(r<.45?'bandage':r<.78?'ammo':'scrap',r<.45?1:r<.78?6:randi(1,3));setMsg(`${cell.id} searched.`,1);}}return;
 }
 if(chapter==='SAN FRANCISCO'){
  for(const sv of survivors){if(!sv.found&&Math.abs(player.x-sv.x)<82){sv.found=true;sv.follow=true;survivorsFound++;state.sanity=Math.min(100,state.sanity+7);setMsg(`${sv.name}: "Stay close. I heard something behind us."`,2.5);setObjective();tone(115,.2,'triangle',.025,35);return;}}
  if(player.x>5200&&player.x<5750&&survivorsFound>=3){archiveOpened=true;setMsg('THE ARCHIVE IS OPEN. Project Eclipse mentions the ferry.',2.6);setObjective();return;}
  if(player.x>4050&&player.x<4750&&survivorsFound>=3&&archiveOpened){win('You got Mara, Eli and Noah inside the emergency shelter. The city is still alive with screams, but the door is locked.');}
 }
}
interact=finalInteractV2;

function finalStartGameV2(name){selectedCharacter=name;resetWorld();buildAlcatraz();positionAtCell();keys.clear();inputState.left=false;inputState.right=false;inputState.down=false;inputState.run=false;inputState.jump=false;mode='intro';cutIndex=0;cutTimer=0;hide('menu');hide('hud');hide('pause');hide('ending');hide('death');hide('modePicker');show('cutscene');const line=document.getElementById('cutline');if(line)line.textContent=cutsceneLines[0];setControlMode(controlMode);enhancedStartAudio();}
startGame=finalStartGameV2;

function finalEnterSFV2(){if(chapter!=='ALCATRAZ'||!state.dockPass)return;chapter='SAN FRANCISCO';finalBoat.signal=2;player.x=150;player.y=GROUND-player.h;player.vx=0;player.vy=0;camera=0;buildSanFrancisco();objectiveStep=0;setObjective();setMsg('SAN FRANCISCO. The ferry is gone. Something else arrived.',2.8);finalHorrorPulse=1;scareSound();}
enterSF=finalEnterSFV2;

function drawFinalBoat(){
 if(chapter!=='ALCATRAZ'||interior)return;
 const x=finalBoat.x-camera;
 if(x<-230||x>W+230)return;
 finalWaterPhase+=.018;
 const bob=Math.sin(totalTime*1.7)*2;
 const y=finalBoat.y+bob;
 for(let i=0;i<6;i++)line(x-75+i*35,GROUND+2+Math.sin(totalTime*2+i)*2,x-45+i*35,GROUND+2+Math.sin(totalTime*2+i)*2,'#2c4750',2);
 px(x-58,y+23,126,19,'#101516');px(x-44,y+14,99,15,'#3c4545');px(x-30,y+2,73,16,'#252b2c');px(x-20,y-7,54,11,'#171c1d');px(x-15,y-18,11,12,'#3f4545');px(x+20,y-18,11,12,'#3f4545');px(x+5,y-1,23,6,'#70634b');px(x-10,y-14,6,5,'#7e6e4d');px(x+30,y-13,6,5,'#7e6e4d');
 ctx.save();ctx.globalAlpha=finalBoat.lit?.9:.3;ctx.fillStyle=finalBoat.lit?'#efd47c':'#8a7b59';ctx.fillRect(x+3,y-28,7,7);ctx.restore();
 ctx.font='bold 11px Consolas';ctx.fillStyle='#c4c2b7';ctx.fillText('FERRY',x-25,y-38);
}

function finalDrawCharacterSprite(x,y,who,dir,anim,role){
 const run=Math.sin(anim*1.25);
 const run2=Math.sin(anim*1.25+Math.PI);
 const idle=Math.sin(totalTime*2.1)*.7;
 const p=who==='May'?{coat:'#343744',coat2:'#5b5f6c',shirt:'#d0c8bb',skin:'#d2b49b',hair:'#1b1716',hair2:'#3b2925',pants:'#25272d',boot:'#0b0e10',badge:'#d2b46d',scarf:'#778087'}:who==='Yumi'?{coat:'#29403b',coat2:'#4d6157',shirt:'#d0c9bd',skin:'#d3b79e',hair:'#111415',hair2:'#242a29',pants:'#20272a',boot:'#0a0e10',badge:'#d8b86b',scarf:'#5b776c'}:{coat:'#2c4145',coat2:'#516369',shirt:'#d1c8b7',skin:'#d0b198',hair:'#352322',hair2:'#66453a',pants:'#22272a',boot:'#0b0e10',badge:'#d6b66c',scarf:'#65736f'};
 ctx.save();ctx.translate(x,y);ctx.scale(dir||1,1);
 px(-25,74,50,7,'rgba(0,0,0,.48)');
 px(-15+run2*3,47,13,25,p.pants);px(3+run*3,47,13,25,p.pants);
 px(-18+run2*3,69,18,7,p.boot);px(1+run*3,69,18,7,p.boot);
 px(-19,20,39,31,p.coat);px(-13,18,29,18,p.shirt);px(-4,20,8,14,p.scarf);
 px(-22+run*2,25,10,29,p.coat2);px(27+run2*2,25,10,29,p.coat2);
 px(-25+run*3,48,15,9,p.coat);px(27+run2*3,48,15,9,p.coat);
 px(-11,-2,30,27,p.skin);px(-16,-8,40,11,p.hair);px(-12,-15,31,9,p.hair2);
 if(who==='Julia'){px(13,-6,13,18,p.hair2);px(24,1,8,23,p.hair2);px(-17,-1,7,17,p.hair2);}
 if(who==='May'){px(-20,-2,8,28,p.hair2);px(22,-3,10,21,p.hair2);px(27,6,7,17,p.hair2);}
 if(who==='Yumi'){px(-20,-1,8,27,p.hair2);px(23,-1,9,27,p.hair2);px(-5,-16,20,6,p.hair);px(12,-20,8,7,p.hair2);}
 px(-2,7,4,4,'#151719');px(15,7,4,4,'#151719');px(2,15,16,3,'#9b6258');
 px(-8,29,8,14,p.coat2);px(13,29,8,14,p.coat2);px(-10,25,6,7,p.badge);px(-8,26,3,3,'#fff1a5');
 px(25,32,6,19,'#151a1b');px(27,35,3,8,'#73706a');
 ctx.restore();
}
drawCharacterSprite=finalDrawCharacterSprite;

function finalDrawZombies(){
 for(const z of zombies){if(z.dead)continue;const x=z.x-camera;if(x<-90||x>W+90)continue;const bob=Math.sin(z.phase)*2;const sway=Math.sin(z.phase*.7)*6;const skin=z.type==='brute'?'#67625b':'#77796f';const cloth=z.type==='runner'?'#39433c':'#343a37';
  px(x-13,GROUND-7,54,7,'rgba(0,0,0,.5)');
  px(x-11+sway*.08,z.y+29+bob,12,31,cloth);px(x+4+sway*.06,z.y+29+bob,19,31,cloth);
  px(x-18,z.y+32+bob,12,29,cloth);px(x+21,z.y+31+bob,12,29,cloth);
  px(x-10,z.y+1+bob,28,z.type==='brute'?29:25,skin);px(x-13,z.y-7+bob,34,11,cloth);
  const arm=Math.sin(z.phase*1.2)*12;line(x-6,z.y+38+bob,x-21,z.y+56+bob+arm,'#4a514d',7);line(x+18,z.y+39+bob,x+34,z.y+55+bob-arm,'#4a514d',7);
  px(x-5,z.y+9+bob,5,5,'#ded7c7');px(x+12,z.y+9+bob,5,5,'#ded7c7');px(x+1,z.y+18+bob,13,3,'#1a1716');
  if(z.type==='runner'){px(x-17,z.y+18+bob,9,6,'#7b312f');px(x+21,z.y+44+bob,10,5,'#7b312f');}
 }
}
drawEnhancedZombies=finalDrawZombies;

function finalDrawSurvivors(){
 for(const sv of survivors){const x=sv.x-camera;if(x<-70||x>W+70)continue;const bob=Math.sin(totalTime*2.2+sv.x)*1.2;drawCharacterSprite(x,GROUND-76+bob,selectedCharacter,1,totalTime*1.2,sv.role);ctx.font='10px Consolas';ctx.fillStyle='#c8c5bb';ctx.fillText(sv.name,x-20,GROUND-92);}
}
drawEnhancedSurvivors=finalDrawSurvivors;

function finalDrawChests(){
 for(const c of chests){if(c.inside)continue;const x=c.x-camera;if(x<-90||x>W+90)continue;const open=c.opened;const lid=open?'#2b2521':c.rare?'#5e4934':'#4a3a2d';px(x,c.y+8,c.w,30,'#322820');px(x,c.y+6,c.w,8,'#765a40');px(x,c.y+18,c.w,20,open?'#1f1a17':lid);px(x+c.w/2-5,c.y+16,10,10,'#d1a65d');if(!open){px(x+2,c.y,c.w-4,7,c.rare?'#6b5139':'#564131');}else{line(x+2,c.y+1,x+c.w-2,c.y-8,'#7a6348',3);}if(c.rare)px(x+8,c.y+8,7,4,'#a0824d');}
}
drawEnhancedChests=finalDrawChests;

function finalDrawInteriorLoot(){
 if(!interior)return;
 const c=chests.find(x=>x.inside&&x.buildingName===interior.building.name);if(!c)return;const x=c.x;const y=c.y;const open=c.opened;px(x-30,y-32,60,32,open?'#2c241f':c.rare?'#5e4934':'#4a3a2d');px(x-30,y-36,60,8,c.rare?'#77583b':'#624937');px(x-5,y-22,10,9,'#d2a65b');if(open)line(x-28,y-28,x+26,y-38,'#806548',3);else px(x-27,y-29,54,6,'#4e3a2d');ctx.font='9px Consolas';ctx.fillStyle='#8d918c';ctx.fillText('SUPPLY CHEST',x-46,y-43);
}
drawInteriorLoot=finalDrawInteriorLoot;

function finalDrawBuildingDetails(){
 for(const b of buildings){const x=b.x-camera;if(x<-b.w-100||x>W+100)continue;const door=b.x+b.w*.5-camera;const near=Math.abs(player.x-(b.x+b.w*.5))<210&&!interior;ctx.save();ctx.globalAlpha=near?.95:.35;ctx.fillStyle=near?'#d6c886':'#595a54';ctx.fillRect(door-10,GROUND-92,20,14);ctx.fillRect(door-5,GROUND-70,10,5);ctx.font='10px Consolas';ctx.fillStyle=near?'#d6d0bf':'#7c7e78';ctx.fillText('ENTER',door-28,GROUND-102);ctx.restore();}
}
function finalDrawIslandDock(){
 if(chapter!=='ALCATRAZ'||interior)return;
 const dockX=3920-camera;px(dockX,GROUND-32,250,32,'#292d2d');for(let i=0;i<10;i++){px(dockX+i*24,GROUND-39,17,7,'#4b4942');px(dockX+i*24+5,GROUND-8,7,28,'#343736');}ctx.fillStyle='#4a4640';ctx.fillRect(dockX+30,GROUND-116,8,84);ctx.fillRect(dockX+195,GROUND-116,8,84);ctx.fillRect(dockX+25,GROUND-116,184,7);if(finalBoat.lit){ctx.fillStyle='#dbbe6e';ctx.fillRect(dockX+108,GROUND-151,10,36);ctx.fillRect(dockX+101,GROUND-145,24,5);}ctx.font='bold 11px Consolas';ctx.fillStyle='#92918a';ctx.fillText('FERRY DOCK',dockX+76,GROUND-126);
}

function finalUpdateHorror(dt){
 if(mode!=='play')return;
 finalHorrorPulse=Math.max(0,finalHorrorPulse-dt*.55);
 finalStepPhase=Math.max(0,finalStepPhase-dt);
 if(state.sanity<72&&Math.random()<dt*.0028){finalHorrorPulse=.7;showWarning(Math.random()<.5?'SOMETHING MOVED IN THE RAIN':'YOU HEARD YOUR NAME');tone(52,.28,'sine',.015,-8);}
 if(state.sanity<42&&Math.random()<dt*.0012){showWarning('DO NOT LOOK INTO THE WINDOWS');shake=Math.max(shake,4);scareSound();}
}
const legacyUpdateSmarterHorror=updateSmarterHorror;
updateSmarterHorror=function(dt){legacyUpdateSmarterHorror(dt);finalUpdateHorror(dt);}

function finalDraw(){
 const baseDraw=finalBaseDraw;
 baseDraw();
 finalDrawBuildingDetails();
 finalDrawIslandDock();
 drawFinalBoat();
 if(finalHorrorPulse>0){ctx.save();ctx.globalAlpha=finalHorrorPulse*.18;ctx.fillStyle='#320008';ctx.fillRect(0,0,W,H);ctx.restore();}
}
const finalBaseDraw=draw;
draw=function(){
 finalBaseDraw();
 if(mode!=='menu'&&mode!=='intro'){
  finalDrawBuildingDetails();
  finalDrawIslandDock();
  drawFinalBoat();
  const focus=player.x-camera;
  if(mode==='play'&&Math.abs(player.vx)>60&&player.onGround){for(let i=0;i<4;i++){const xx=focus-player.facing*(22+i*11);const yy=player.y+player.h-3-(i%2)*2;px(xx,yy,3,2,'#656b68');}}
  if(finalHorrorPulse>0){ctx.save();ctx.globalAlpha=finalHorrorPulse*.16;ctx.fillStyle='#280007';ctx.fillRect(0,0,W,H);ctx.restore();}
 }
}

if(!document.getElementById('privacyGate')){
 const gate=document.createElement('div');gate.id='privacyGate';gate.innerHTML='<div class="privacyBox"><h1>NIGHTWATCH SECURITY TERMINAL</h1><p class="privacyLead">ASHES OF THE DEAD — DEVICE INFORMATION NOTICE</p><div class="privacyGrid"><div class="privacyCard"><b>WHAT MAY BE DISPLAYED</b>Browser, platform, screen, language, timezone, network hints, CPU threads, touch support, cookies state and server-seen network address.</div><div class="privacyCard"><b>WHAT IS NOT READ</b>No passwords, personal files, photos, contacts, saved documents or account contents.</div><div class="privacyCard"><b>PERMISSIONS</b>Location, camera and microphone require separate browser permission.</div><div class="privacyCard"><b>FICTIONAL SURVEILLANCE</b>CCTV, tracking alerts and The Smiler are fictional game elements.</div></div><div class="privacyNotice">The server sees only the network address that reaches it. A proxy, VPN or carrier network can change it.</div><div style="margin-top:18px"><button id="privacyAccept">ENTER ASHES OF THE DEAD</button></div></div></div>';document.body.appendChild(gate);gate.querySelector('#privacyAccept').onclick=()=>{gate.remove();mode='menu';show('menu');};
}


let fourthWallState={idle:0,away:0,messageCooldown:0,returnFlash:0,cursorSeen:0,watching:false};
let exitDoorFlash=0;
let exitHintTimer=0;
function fourthWallSay(text,intensity=1){
 if(mode!=='play'||chestUIOpen)return;
 setMsg(text,2.4);
 showWarning(text);
 fourthWallState.returnFlash=Math.max(fourthWallState.returnFlash,.55*intensity);
 finalHorrorPulse=Math.max(finalHorrorPulse,.4*intensity);
 shake=Math.max(shake,2*intensity);
}
window.addEventListener('pointermove',e=>{fourthWallState.idle=0;fourthWallState.cursorSeen++;});
window.addEventListener('keydown',()=>{fourthWallState.idle=0;});
window.addEventListener('pointerleave',()=>{if(mode==='play')fourthWallState.away=Math.max(fourthWallState.away,.7);});
window.addEventListener('pointerenter',()=>{if(mode==='play'&&fourthWallState.away>0){fourthWallSay('I SAW YOU COME BACK.',.8);fourthWallState.away=0;}});
window.addEventListener('visibilitychange',()=>{
 if(document.hidden){fourthWallState.away=2;return;}
 if(mode==='play'&&fourthWallState.away>0){fourthWallState.away=0;fourthWallSay('YOU LEFT THE ISLAND. SHE DID NOT.',1);}
});
function robustExitSide(){if(!interior)return null;if(player.x<=190)return'left';if(player.x>=1010)return'right';return null;}
function robustExitBuilding(side){
 if(!interior)return;
 const b=interior.building;
 const chosen=side||robustExitSide()||(player.x<610?'left':'right');
 interior=null;
 floor=1;
 player.y=GROUND-player.h;
 player.vx=0;
 player.vy=0;
 const minX=28;
 const maxX=(chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH)-28;
 if(chosen==='left')player.x=clamp(b.x-46,minX,maxX);else player.x=clamp(b.x+b.w+46,minX,maxX);
 camera=clamp(lerp(camera,player.x-W*.42,.5),0,maxX-W);
 exitDoorFlash=1;
 exitHintTimer=0;
 stepParticles(player.x,GROUND-3,10,'dust');
 tone(88,.18,'square',.028,-18);
 setMsg(`EXITED ${b.name.toUpperCase()} — STREET`,1.4);
}
exitBuilding=robustExitBuilding;
const exitAwareInteract=interact;
interact=function(){
 if(mode!=='play'||gadgetOpen||chestUIOpen)return;
 if(interior){
  const side=robustExitSide();
  if(side){robustExitBuilding(side);return;}
 }
 exitAwareInteract();
};
const interiorDrawBase=drawEnhancedInterior;
drawEnhancedInterior=function(){
 interiorDrawBase();
 if(!interior)return;
 const b=interior.building;
 const left=62;
 const right=1138;
 const active=robustExitSide();
 ctx.save();
 ctx.globalAlpha=.95;
 px(left-28,375,82,140,'#080a0b');
 px(left-20,386,66,129,'#202526');
 px(left-13,398,52,6,'#4b504d');
 px(left-7,450,5,5,'#8e7e5d');
 px(right-26,375,82,140,'#080a0b');
 px(right-18,386,66,129,'#202526');
 px(right-11,398,52,6,'#4b504d');
 px(right+34,450,5,5,'#8e7e5d');
 ctx.font='bold 11px Consolas';
 ctx.fillStyle=active==='left'?'#e0d19a':'#777d79';
 ctx.fillText('EXIT',left-8,366);
 ctx.fillStyle=active==='right'?'#e0d19a':'#777d79';
 ctx.fillText('EXIT',right-5,366);
 if(active){
  const ax=active==='left'?left:right;
  ctx.fillStyle='#d0c28e';
  ctx.fillRect(ax-9,340,18,3);
  ctx.fillRect(ax-5,334,10,3);
  ctx.font='10px Consolas';
  ctx.fillText('E  EXIT TO STREET',ax-55,324);
 }
 ctx.font='10px Consolas';
 ctx.fillStyle='#5f6863';
 ctx.fillText(b.name.toUpperCase(),485,690);
 ctx.restore();
};
const interiorUpdateBase=update;
update=function(dt){
 interiorUpdateBase(dt);
 if(exitDoorFlash>0)exitDoorFlash=Math.max(0,exitDoorFlash-dt*3);
 if(mode!=='play')return;
 fourthWallState.idle+=dt;
 fourthWallState.messageCooldown=Math.max(0,fourthWallState.messageCooldown-dt);
 fourthWallState.returnFlash=Math.max(0,fourthWallState.returnFlash-dt*1.8);
 if(fourthWallState.idle>21&&fourthWallState.messageCooldown<=0){
  fourthWallState.messageCooldown=28+Math.random()*25;
  fourthWallSay(Math.random()<.5?'STILL THERE?':'JULIA CAN HEAR YOU BREATHING.',.65);
 }
 if(fourthWallState.idle>46&&fourthWallState.messageCooldown>12){
  fourthWallState.idle=18;
  fourthWallSay('MOVE THE CURSOR. I KNOW YOU ARE WATCHING.',.9);
 }
 if(state.sanity<58&&Math.random()<dt*.0018&&fourthWallState.messageCooldown<=0){
  fourthWallState.messageCooldown=18;
  fourthWallSay(Math.random()<.5?'DON’T CHECK THE OTHER TAB.':'THE GAME REMEMBERS WHEN YOU LEAVE.',.75);
 }
};
const renderBase=draw;
draw=function(){
 renderBase();
 if(mode==='play'&&interior&&robustExitSide()){
  ctx.save();
  ctx.globalAlpha=.72;
  ctx.font='bold 11px Consolas';
  ctx.fillStyle='#d9ce9a';
  ctx.fillText('E  EXIT',robustExitSide()==='left'?70:1090,305);
  ctx.restore();
 }
 if(mode==='play'&&exitDoorFlash>0){
  ctx.save();
  ctx.globalAlpha=exitDoorFlash*.12;
  ctx.fillStyle='#efe0a0';
  ctx.fillRect(0,0,W,H);
  ctx.restore();
 }
 if(mode==='play'&&fourthWallState.returnFlash>0){
  ctx.save();
  ctx.globalAlpha=fourthWallState.returnFlash*.18;
  ctx.strokeStyle='#d5d0c2';
  ctx.lineWidth=1;
  const edge=mouse.x< W*.5 ? 24:W-24;
  ctx.strokeRect(edge-10,mouse.y-10,20,20);
  ctx.restore();
 }
};


function ferryZone(){
 if(chapter!=='ALCATRAZ'||interior)return false;
 return Math.abs(player.x-finalBoat.x)<250;
}
function ferryStatusPrompt(){
 if(chapter!=='ALCATRAZ'||interior)return '';
 const d=Math.abs(player.x-finalBoat.x);
 if(d>290)return '';
 if(!state.dockPass)return 'E — NEED DOCK PASS';
 if(finalBoat.signal===0)return 'E — LIGHT FERRY BEACON';
 if(d<165)return 'E — BOARD FERRY';
 return 'MOVE CLOSER TO THE FERRY';
}
function boardFerryNow(){
 if(chapter!=='ALCATRAZ'||interior)return false;
 if(!state.dockPass){setMsg('You need the Dock Pass from the Medical Wing.',1.8);showWarning('DOCK PASS REQUIRED');tone(74,.25,'square',.025,-20);return true;}
 const d=Math.abs(player.x-finalBoat.x);
 if(d>250){setMsg('The ferry is farther down the pier.',1.2);return true;}
 if(finalBoat.signal===0){finalBoat.signal=1;finalBoat.lit=true;objectiveStep=5;setObjective();setMsg('FERRY BEACON LIT. The engine starts in the fog.',2.4);stepParticles(finalBoat.x,finalBoat.y,18,'spark');tone(180,.3,'triangle',.035,50);shake=3;return true;}
 if(d<=175){setMsg('BOARDING FERRY...',1.1);tone(92,.55,'square',.035,-22);stepParticles(player.x,GROUND-2,18,'water');shake=6;finalBoat.signal=2;setTimeout(()=>{if(mode==='play')finalEnterSFV2();},650);return true;}
 setMsg('Move closer to the ferry ladder.',1.1);return true;
}
function ferryAwareInteract(){
 if(mode!=='play'||gadgetOpen||chestUIOpen)return;
 if(ferryZone()){boardFerryNow();return;}
 finalInteractV2();
}
interact=ferryAwareInteract;
const ferryAwareUpdateBase=update;
update=function(dt){
 ferryAwareUpdateBase(dt);
 if(mode!=='play'||chapter!=='ALCATRAZ'||interior)return;
 if(finalBoat.signal===1){finalBoat.lit=true;finalBoat.signal=1;}
};
const ferryAwareDrawBase=draw;
draw=function(){
 ferryAwareDrawBase();
 if(mode==='play'&&chapter==='ALCATRAZ'&&!interior){
  const prompt=ferryStatusPrompt();
  if(prompt){ctx.save();ctx.globalAlpha=.92;ctx.font='bold 12px Consolas';ctx.fillStyle=state.dockPass?'#ddd2a2':'#a58c86';ctx.fillText(prompt,Math.max(18,Math.min(W-270,finalBoat.x-camera-100)),GROUND-174);ctx.restore();}
  const near=Math.abs(player.x-finalBoat.x)<180&&state.dockPass;
  if(near&&finalBoat.signal===1){ctx.save();ctx.globalAlpha=.16;ctx.strokeStyle='#e3cf8b';ctx.strokeRect(finalBoat.x-camera-90,GROUND-145,180,96);ctx.restore();}
 }
};
const ferryTapHandler=()=>{if(mode==='play'&&ferryZone())boardFerryNow();};
canvas.addEventListener('dblclick',ferryTapHandler);
document.querySelectorAll('#mobileControls button').forEach(btn=>btn.addEventListener('pointerup',()=>{if(mode==='play'&&ferryZone()&&btn.dataset.key==='e')boardFerryNow();}));


function ultimateObjectiveData(){if(chapter==='ALCATRAZ'){return[{t:'SEARCH CELL A-17 AND ESCAPE CELL BLOCK A.',steps:['1. Walk to the mattress on the left side of Cell A-17.','2. Press E to search beneath it and take the brass key.','3. Walk to the barred cell door on the right.','4. Press E again to unlock the door.'],d:0},{t:'SEARCH CELL BLOCK A AND FOLLOW THE BLOOD MARKS.',steps:['1. Walk through the Cell Block A corridor.','2. Look for open or locked cells and blood writing.','3. Press E at cells that can be searched.','4. Keep moving toward the center of the island.'],d:1},{t:'CROSS CELL BLOCK B AND FIND THE DOCK ROUTE.',steps:['1. Continue right past the guard station.','2. Search Cell Block B for useful supplies.','3. Unlock cells when you find spare keys.','4. Look for the B-4 clue near the prison route.'],d:2},{t:'FIND THE DOCK PASS IN THE MEDICAL WING.',steps:['1. Follow the red MEDICAL WING sign.','2. Enter the Medical Wing through the main door.','3. Go to the clearly marked supply desk.','4. Press E to take the Dock Pass.'],d:3},{t:'REACH THE DOCK BEACON AND SIGNAL THE FERRY.',steps:['1. Follow the dock signs all the way right.','2. Stand near the ferry beacon.','3. Press E to light the beacon when the Dock Pass is in your inventory.','4. Stay near the dock and listen for the ferry engine.'],d:4},{t:'ESCAPE ALCATRAZ BY BOARDING THE FERRY.',steps:['1. Walk close to the ferry ladder.','2. Wait until the prompt says BOARD FERRY.','3. Press E to board.','4. Do not leave the dock until the boarding sequence begins.'],d:5}];}return[{t:'FIND THE THREE SURVIVORS.',steps:['1. Explore the abandoned city from left to right.','2. Approach Mara, Eli and Noah.','3. Press E near each survivor to recruit them.','4. Check OBJECTIVES again after each rescue.'],d:0},{t:'FIND THE RESEARCH ANNEX ARCHIVE.',steps:['1. Keep the survivors together.','2. Travel to the Research Annex.','3. Enter the building through the main entrance.','4. Reach the archive area and press E to open it.'],d:1},{t:'RETURN TO THE EMERGENCY SHELTER.',steps:['1. Leave the Research Annex.','2. Travel back toward the Emergency Shelter.','3. Enter the shelter area with all three survivors found.','4. Press E at the shelter objective point to finish the chapter.'],d:2}];}
function ultimateCurrentObjectiveIndex(){if(chapter==='ALCATRAZ')return Math.min(objectiveStep,5);if(archiveOpened)return 2;if(survivorsFound>=3)return 1;return 0;}
function ultimateRenderObjectivePanel(){const list=document.getElementById('objectiveList');const sub=document.getElementById('objectivePanelSub');if(!list||!sub)return;const data=ultimateObjectiveData();const current=ultimateCurrentObjectiveIndex();sub.textContent=chapter==='ALCATRAZ'?'ALCATRAZ ISLAND • CELL BLOCK A / ESCAPE ROUTE':'SAN FRANCISCO • SURVIVOR / ARCHIVE ROUTE';list.innerHTML='';data.forEach((o,i)=>{const item=document.createElement('div');item.className='objectiveItem '+(i<current?'done ':'')+(i===current?'current':'');const mark=i<current?'✓':i===current?'›':'○';const steps=o.steps.map((step,n)=>'<div class="'+(i<current?'stepDone':i===current&&n===0?'stepNow':'')+'">'+step+'</div>').join('');const help=i===current?'<div class="objectiveHelp">Need help? Follow the numbered steps above. Use E when a prompt appears.</div>':'';item.innerHTML='<div class="objectiveMark">'+mark+'</div><div><strong>'+o.t+'</strong><div class="objectiveSteps">'+steps+'</div>'+help+'</div>';list.appendChild(item);});}
function ultimateSetObjective(){const data=ultimateObjectiveData();const current=ultimateCurrentObjectiveIndex();const el=document.getElementById('objective');if(el){const lead='OBJECTIVE\n'+data[current].t;const next=data[current].steps[0]||'';el.textContent=lead+'\nNEXT STEP\n'+next;}ultimateRenderObjectivePanel();}
renderObjectivePanel=ultimateRenderObjectivePanel;
setObjective=ultimateSetObjective;

let ultimateScare={timer:24+Math.random()*20,cooldown:0,static:0,heartbeat:0,shadow:0,drip:0,glitch:0,flash:0};
function ultimatePixelArchitecture(){if(mode==='menu'||mode==='intro')return;const left=camera-40,right=camera+W+60;for(let i=0;i<34;i++){const wx=140+i*210;const x=wx-camera;if(wx<left||wx>right)continue;const h=40+(i%5)*16;px(x,GROUND-h,4,h,'#161a1b');px(x-7,GROUND-h,18,4,'#2a2f30');if(chapter==='SAN FRANCISCO'&&i%3===0){px(x+7,GROUND-h+8,19,5,'#3b3a34');px(x+12,GROUND-h+5,8,7,'#58503b');}else if(chapter==='ALCATRAZ'&&i%4===0){line(x,GROUND-h+8,x+16,GROUND-h-5,'#3a403f',2);line(x+16,GROUND-h-5,x+29,GROUND-h+10,'#303635',2);}}}
function ultimateBrickDetail(){if(mode==='menu'||mode==='intro')return;if(interior){for(let y=95;y<520;y+=28){for(let x=18;x<W;x+=74){if(((x+y)/74)%3===0)line(x,y,x+30,y,'#242a29',1);}}return;}for(const b of buildings){const x=b.x-camera;if(x<-b.w||x>W)continue;for(let row=0;row<6;row++){const yy=GROUND-90-row*31;for(let col=0;col<Math.floor(b.w/52);col++){const xx=x+14+col*52+(row%2)*11;if(xx>x+8&&xx<x+b.w-10)line(xx,yy,xx+27,yy,'#2b3030',1);}}if(b.type!=='prison'){px(x+10,GROUND-60,5,42,'#3c403e');px(x+b.w-16,GROUND-60,5,42,'#131718');}}}
function ultimateGroundDecals(){if(interior)return;for(let i=0;i<46;i++){const wx=i*173+77;const x=wx-camera;if(x<-30||x>W+30)continue;const y=GROUND-2+(i%3)*5;if(i%5===0){ctx.save();ctx.globalAlpha=.24;ctx.fillStyle='#5b4740';ctx.beginPath();ctx.ellipse(x,y+3,18+(i%4)*4,4,0,0,Math.PI*2);ctx.fill();ctx.restore();}else if(i%3===0){line(x,y,x+18,y+1,'#414443',1);line(x+8,y+2,x+13,y+9,'#303332',1);}else{px(x,y,3+(i%4),2,'#353938');}}}
function ultimateInteriorProps(){if(!interior)return;const b=interior.building;for(let i=0;i<15;i++){const x=32+i*82;const y=330+(i%3)*58;px(x,y,42,4,'#343a39');px(x+5,y+5,30,3,'#161b1b');if(i%4===0){px(x+10,y-18,5,18,'#4b504d');px(x+5,y-23,15,6,'#5c5c52');}if(i%5===0){line(x+38,y+7,x+54,y-13,'#4b4f4d',2);line(x+54,y-13,x+63,y-3,'#333837',2);}}ctx.font='bold 9px Consolas';ctx.fillStyle='#656d69';ctx.fillText(b.name.toUpperCase(),22,95);}
function ultimateRain(){if(interior)return;ctx.save();ctx.globalAlpha=.18;for(let i=0;i<95;i++){const x=(i*67+totalTime*460-camera*.95)%W;const y=(i*41+totalTime*720)%430;line(x,y,x-5,y+16,'#a9bac0',1);}ctx.restore();}
function ultimateLens(){if(mode!=='play')return;const pulse=Math.max(0,ultimateScare.static);if(pulse>0){ctx.save();ctx.globalAlpha=pulse*.22;for(let i=0;i<95;i++){const x=(i*97+Math.floor(totalTime*700))%W;const y=(i*43+Math.floor(totalTime*270))%H;px(x,y,1+(i%2),1,'#c9d0ce');}ctx.restore();}ctx.save();ctx.globalAlpha=.12;for(let i=0;i<9;i++)line(0,92+i*63,W,92+i*63,'#c6c8c1',1);ctx.restore();}
function ultimateForegroundHorror(){if(mode!=='play')return;if(ultimateScare.shadow>0){ctx.save();const side=player.facing>0?W-120:120;ctx.globalAlpha=ultimateScare.shadow*.25;px(side-32,180,64,260,'#020203');px(side-21,152,42,49,'#020203');px(side-10,188,6,5,'#d9d2bc');px(side+5,188,6,5,'#d9d2bc');line(side-20,300,side-62,370,'#030304',7);line(side+20,300,side+62,370,'#030304',7);ctx.restore();}if(ultimateScare.drip>0){ctx.save();ctx.globalAlpha=.35;ctx.fillStyle='#6d2022';for(let i=0;i<7;i++){const x=(i*177+totalTime*30)%W;ctx.fillRect(x,0,2,28+((i*17)%39));}ctx.restore();}}
function ultimateHorrorDirector(dt){if(mode!=='play')return;ultimateScare.cooldown=Math.max(0,ultimateScare.cooldown-dt);ultimateScare.static=Math.max(0,ultimateScare.static-dt*2.2);ultimateScare.heartbeat=Math.max(0,ultimateScare.heartbeat-dt*1.7);ultimateScare.shadow=Math.max(0,ultimateScare.shadow-dt*1.4);ultimateScare.drip=Math.max(0,ultimateScare.drip-dt*1.1);ultimateScare.glitch=Math.max(0,ultimateScare.glitch-dt*2);ultimateScare.flash=Math.max(0,ultimateScare.flash-dt*3);ultimateScare.timer-=dt;const danger=state.sanity<65?1.3:1;if(ultimateScare.timer<=0&&ultimateScare.cooldown<=0){ultimateScare.timer=34+Math.random()*46;ultimateScare.cooldown=7;const roll=Math.random();if(roll<.28&&state.sanity<78){ultimateScare.shadow=.9;setMsg('Something shifted at the edge of your vision.',1.6);tone(41,.42,'sine',.022,-7);shake=Math.max(shake,2);}else if(roll<.52){ultimateScare.static=.8;showWarning(Math.random()<.5?'THE CAMERA JUST BLINKED':'LISTEN TO THE RAIN');tone(58,.35,'triangle',.012,-3);}else if(roll<.72&&chapter==='ALCATRAZ'){ultimateScare.drip=1.2;setMsg('Fresh blood is running down the wall.',1.8);state.sanity=Math.max(0,state.sanity-2.5);}else{ultimateScare.heartbeat=.9;tone(32,.7,'sine',.025,0);if(state.sanity<50){showWarning(Math.random()<.5?'SHE KNOWS YOU ARE HERE':'DO NOT TRUST THE NEXT DOOR');shake=Math.max(shake,4);}}}if(smiler.active&&Math.abs(smiler.x-player.x)<480){ultimateScare.static=Math.max(ultimateScare.static,.35);ultimateScare.heartbeat=Math.max(ultimateScare.heartbeat,.45);}}
function ultimateDrawCharacterPulse(){if(mode!=='play')return;const run=Math.abs(player.vx)>65;const x=player.x-camera;if(run&&player.onGround){ctx.save();ctx.globalAlpha=.22;for(let i=1;i<4;i++){drawCharacterSprite(x-player.facing*i*13,player.y+2,selectedCharacter,player.facing,player.anim-i*.35,'ghost');}ctx.restore();}if(state.health<35){ctx.save();ctx.globalAlpha=.08;ctx.fillStyle='#8e2527';ctx.fillRect(0,0,W,H);ctx.restore();}}
function ultimateDrawWorldPolish(){if(mode==='menu'||mode==='intro')return;ultimatePixelArchitecture();ultimateBrickDetail();ultimateGroundDecals();ultimateInteriorProps();ultimateRain();ultimateDrawCharacterPulse();ultimateForegroundHorror();ultimateLens();if(ultimateScare.heartbeat>0){ctx.save();ctx.globalAlpha=.12+Math.sin(totalTime*18)*.05;ctx.fillStyle='#5d0710';ctx.fillRect(0,0,W,H);ctx.restore();}if(ultimateScare.glitch>0){ctx.save();for(let i=0;i<8;i++){const y=(i*89+totalTime*200)%H;ctx.globalAlpha=.09;ctx.fillStyle='#d7d1c6';ctx.fillRect((i*163+totalTime*70)%W,y,70,2);}ctx.restore();}}
const ultimateUpdateBase=update;
update=function(dt){ultimateUpdateBase(dt);ultimateHorrorDirector(dt);if(mode==='play'&&interior){if(Math.abs(player.x-610)<95)showWarning('STAIRS • PRESS E');}}
const ultimateDrawBase=draw;
draw=function(){ultimateDrawBase();ultimateDrawWorldPolish();if(mode==='play'&&interior&&Math.abs(player.x-610)<100){ctx.save();ctx.font='bold 10px Consolas';ctx.fillStyle='#cfc7a4';ctx.fillText('E  USE STAIRS',540,332);ctx.restore();}}
renderObjectivePanel=ultimateRenderObjectivePanel;
setObjective=ultimateSetObjective;


const screamJamStyle=document.createElement('style');
screamJamStyle.textContent=`
#jamFearHud{position:absolute;left:18px;bottom:18px;z-index:27;pointer-events:none;font:700 10px Consolas,monospace;letter-spacing:1.5px;color:#b8beb8;text-shadow:2px 2px #000;opacity:0;transition:opacity .2s}
#jamFearHud.on{opacity:1}
#jamFearHud .meter{width:124px;height:5px;background:#161a19;border:1px solid #464d4a;margin-top:5px}
#jamFearHud i{display:block;height:100%;width:0;background:#8c4545;transition:width .15s}
#jamScareFlash{position:absolute;inset:0;z-index:39;pointer-events:none;opacity:0;background:radial-gradient(circle at 50% 48%,rgba(230,224,212,.28),rgba(110,10,15,.09) 22%,transparent 58%)}
#jamWallText{position:absolute;left:50%;top:35%;z-index:38;transform:translate(-50%,-50%);pointer-events:none;opacity:0;color:#c9c4ba;font:700 18px Consolas,monospace;letter-spacing:4px;text-shadow:0 0 16px #000,3px 3px #000;text-align:center}
`;
document.head.appendChild(screamJamStyle);
const jamFearHud=document.createElement('div');
jamFearHud.id='jamFearHud';
jamFearHud.innerHTML='<div id="jamFearText">ADRENALINE</div><div class="meter"><i id="jamFearFill"></i></div>';
document.body.appendChild(jamFearHud);
const jamScareFlashEl=document.createElement('div');
jamScareFlashEl.id='jamScareFlash';
document.body.appendChild(jamScareFlashEl);
let jamScareFlash=0;
const jamWallText=document.createElement('div');
jamWallText.id='jamWallText';
document.body.appendChild(jamWallText);

let jamFear=0;
let jamFearFlash=0;
let jamWallTimer=0;
let jamWallCooldown=10;
let jamCombo=0;
let jamLastPlayerX=0;
let jamStuckTimer=0;
let jamHiddenTimer=0;
let jamNearSmiler=0;
let jamAmbientClock=0;
let jamBlink=0;

function jamMessage(text,duration=1.6){
 jamWallText.textContent=text;
 jamWallTimer=Math.max(jamWallTimer,duration);
 jamScareFlashEl.style.opacity='.22';
}
function jamPixelNoise(amount=28,alpha=.08){
 ctx.save();ctx.globalAlpha=alpha;
 for(let i=0;i<amount;i++){
  const x=((i*149+Math.floor(totalTime*420))%W+W)%W;
  const y=(i*61+Math.floor(totalTime*160))%H;
  px(x,y,1+(i%3),1+(i%2),i%3?'#bfc3bc':'#6b1c20');
 }
 ctx.restore();
}
function jamBackgroundDetail(){
 if(mode==='menu'||mode==='intro'||interior)return;
 const left=camera-60,right=camera+W+60;
 for(let i=0;i<24;i++){
  const wx=180+i*260;
  if(wx<left||wx>right)continue;
  const x=wx-camera;
  const h=28+(i%5)*9;
  px(x,GROUND-h,3,h,'#111516');
  px(x-5,GROUND-h,13,3,'#2b3030');
  if(i%4===0){
   line(x+3,GROUND-h+4,x+29,GROUND-h-10,'#303433',1);
   line(x+29,GROUND-h-10,x+46,GROUND-h+2,'#252a29',1);
  }
  if(chapter==='SAN FRANCISCO'&&i%5===0){
   px(x+10,GROUND-116,34,38,'#131718');
   px(x+14,GROUND-109,26,7,'#373a36');
   px(x+18,GROUND-97,18,20,'#242a29');
   px(x+21,GROUND-94,3,6,'#6c6046');
  }
  if(chapter==='ALCATRAZ'&&i%6===0){
   for(let q=0;q<4;q++)line(x+9+q*7,GROUND-74,x+4+q*7,GROUND-30,'#464a49',2);
   px(x-4,GROUND-84,39,4,'#454845');
  }
 }
}
function jamInteriorDetail(){
 if(!interior||mode!=='play')return;
 for(let i=0;i<16;i++){
  const x=25+i*83;
  const y=110+(i%4)*77;
  px(x,y,38,3,'#323736');
  px(x+5,y+7,4,23,'#1b2020');
  if(i%3===0){
   line(x+10,y+32,x+28,y+15,'#474b47',2);
   px(x+25,y+12,7,4,'#5c5142');
  }
 }
 for(let i=0;i<5;i++){
  const x=145+i*205;
  px(x,535,86,4,'#292e2d');
  px(x+10,528,13,7,'#464844');
  px(x+58,528,17,7,'#303534');
 }
}
function jamNearMiss(){
 if(mode!=='play'||!smiler.active)return;
 const d=Math.abs(smiler.x-player.x);
 if(d<270){
  jamNearSmiler=Math.min(1,jamNearSmiler+.06);
  jamFear=Math.min(100,jamFear+0.9);
 }else{
  jamNearSmiler=Math.max(0,jamNearSmiler-.045);
 }
}
function jamSpawnScare(){
 if(mode!=='play'||chestUIOpen||infoFlashOpen||interior===null&&chapter!=='ALCATRAZ'&&chapter!=='SAN FRANCISCO')return;
 if(jamWallCooldown>0)return;
 const sanityDanger=state.sanity<62?1.35:1;
 const probability=.0026*sanityDanger;
 if(Math.random()>probability)return;
 jamWallCooldown=8+Math.random()*13;
 const roll=Math.random();
 if(roll<.22){
  jamFear=Math.min(100,jamFear+34);
  jamFearFlash=.8;
  jamMessage('DON’T LOOK BEHIND YOU',1.55);
  tone(38,.35,'sine',.024,-10);
  shake=Math.max(shake,6);
 }else if(roll<.42){
  jamFear=Math.min(100,jamFear+20);
  jamMessage('THE CAMERA KNOWS WHERE YOU ARE',1.7);
  ultimateScare.static=Math.max(ultimateScare.static,.7);
  tone(51,.28,'triangle',.015,-4);
 }else if(roll<.62){
  jamFear=Math.min(100,jamFear+17);
  jamWallText.textContent='';
  horrorEyes=Math.max(horrorEyes,.65);
  showWarning(chapter==='ALCATRAZ'?'CELL BLOCK A IS NOT EMPTY':'SOMEONE IS FOLLOWING THE SURVIVORS');
  shake=Math.max(shake,4);
  tone(44,.5,'sine',.02,-5);
 }else if(roll<.8){
  jamFear=Math.min(100,jamFear+26);
  jamScareFlash=.5;
  for(let i=0;i<12;i++)stepParticles(player.x+rand(-40,40),player.y+rand(0,70),4,'blood');
  jamMessage(Math.random()<.5?'YOU HEARD THAT':'THAT WAS NOT THE WIND',1.4);
  tone(64,.4,'sawtooth',.012,-7);
 }else{
  jamFear=Math.min(100,jamFear+15);
  jamMessage('SHE MOVED WHEN YOU BLINKED',1.65);
  cinematicPulse=.75;
  shake=Math.max(shake,3);
 }
}
function jamWallUpdate(dt){
 jamWallCooldown=Math.max(0,jamWallCooldown-dt);
 jamWallTimer=Math.max(0,jamWallTimer-dt);
 jamScareFlash=Math.max(0,jamScareFlash-dt*2.8);
 if(jamWallTimer<=0)jamWallText.style.opacity='0';else jamWallText.style.opacity=String(Math.min(1,jamWallTimer/.25));
 jamScareFlashEl.style.opacity=String(Math.max(0,jamScareFlash));
 if(mode==='play')jamFear=Math.max(0,jamFear-dt*1.7);
 if(Math.abs(player.x-jamLastPlayerX)<1.4&&Math.abs(player.vx)<6&&mode==='play'&&interior===null)jamStuckTimer+=dt;else jamStuckTimer=0;
 jamLastPlayerX=player.x;
 if(jamStuckTimer>6&&mode==='play'){jamStuckTimer=0;jamMessage('YOU ARE STILL HERE.',1.2);jamFear=Math.min(100,jamFear+12);}
 if(document.hidden&&mode==='play')jamHiddenTimer+=dt;else jamHiddenTimer=Math.max(0,jamHiddenTimer-dt*2);
 if(jamHiddenTimer>.8){jamHiddenTimer=0;jamMessage('YOU LEFT. SHE DID NOT.',2.1);jamFear=Math.min(100,jamFear+25);tone(33,.7,'sine',.022,-9);}
 jamAmbientClock+=dt;
}
function jamHudUpdate(){
 const on=mode==='play'&&jamFear>3;
 jamFearHud.classList.toggle('on',on);
 const fill=document.getElementById('jamFearFill');
 const text=document.getElementById('jamFearText');
 if(fill)fill.style.width=Math.min(100,jamFear)+'%';
 if(text)text.textContent=jamNearSmiler>.35?'PROXIMITY WARNING':'ADRENALINE';
}
function jamDrawAtmosphere(){
 if(mode==='menu'||mode==='intro')return;
 jamBackgroundDetail();
 jamInteriorDetail();
 if(mode==='play'){
  const pxs=player.x-camera;
  ctx.save();
  ctx.globalAlpha=.16;
  for(let i=0;i<18;i++){
   const ox=(i*53+totalTime*20)%220-110;
   const oy=(i*31)%80;
   px(pxs+ox,GROUND-10-oy,1+(i%2),1,'#b8b5a9');
  }
  ctx.restore();
 }
 if(jamNearSmiler>.25){
  ctx.save();
  const a=jamNearSmiler*.11;
  ctx.globalAlpha=a;
  ctx.fillStyle='#8f1218';
  ctx.fillRect(0,0,W,H);
  ctx.restore();
 }
 jamPixelNoise(state.sanity<45?46:26,state.sanity<45?.11:.045);
 if(state.sanity<34){
  ctx.save();
  ctx.globalAlpha=.08;
  for(let i=0;i<7;i++){
   const y=(i*97+Math.floor(totalTime*90))%H;
   ctx.fillStyle=i%2?'#efe8db':'#5f171c';
   ctx.fillRect(0,y,W,2);
  }
  ctx.restore();
 }
}
function jamFourthWall(dt){
 if(mode!=='play')return;
 if(Math.random()<dt*.0005&&state.sanity<56){
  jamMessage(Math.random()<.5?'YOU CAN STOP PLAYING.':'WE CAN SEE YOU.',1.35);
 }
}
const jamOldUpdate=update;
update=function(dt){
 jamOldUpdate(dt);
 jamNearMiss();
 jamSpawnScare();
 jamWallUpdate(dt);
 jamFourthWall(dt);
 jamHudUpdate();
 if(mode==='play'&&jamNearSmiler>.72&&smiler.active){
  state.sanity=Math.max(0,state.sanity-dt*.8);
 }
};
const jamOldDraw=draw;
draw=function(){
 jamOldDraw();
 jamDrawAtmosphere();
 if(mode==='play'&&jamFear>74){
  ctx.save();
  ctx.globalAlpha=.035+Math.sin(totalTime*22)*.02;
  ctx.fillStyle='#f0eade';
  ctx.fillRect(0,0,W,H);
  ctx.restore();
 }
};
window.addEventListener('visibilitychange',()=>{if(document.hidden&&mode==='play'){jamHiddenTimer=1;}});


let enhJumpWasDown=false;
let enhJumpsUsed=0;
let enhLandingSquash=0;
let enhRunDust=0;
let enhFootClock=.12;
let enhRecoil=0;
let enhLastGround=true;
let enhAirTime=0;
let enhCamLead=0;
function enhJumpPressed(){return keys.has('w')||keys.has('ArrowUp')||keys.has(' ');}
function enhPixelBurst(x,y,count,color){for(let i=0;i<count;i++){if(particles.length>230)particles.shift();const a=Math.random()*Math.PI*2;const sp=rand(30,170);particles.push({x:x+rand(-5,5),y:y+rand(-3,3),life:rand(.18,.5),vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-rand(10,75),size:randi(1,3),c:color});}}
function enhPhysicsBefore(dt){
 const jump=enhJumpPressed();
 const edge=jump&&!enhJumpWasDown;
 const wasGround=player.onGround;
 if(player.onGround){enhJumpsUsed=0;enhAirTime=0;}
 else enhAirTime+=dt;
 if(edge&&!wasGround&&enhJumpsUsed<1&&mode==='play'&&!gadgetOpen&&!chestUIOpen&&interior===null){
  player.vy=-485;
  enhJumpsUsed=1;
  enhLandingSquash=.22;
  enhPixelBurst(player.x+player.w/2,player.y+player.h/2,8,'#8a8e89');
  tone(150,.08,'triangle',.025,55);
  shake=Math.max(shake,2.2);
 }
 enhJumpWasDown=jump;
 enhRecoil=Math.max(0,enhRecoil-dt*7);
 enhLandingSquash=Math.max(0,enhLandingSquash-dt*5);
 enhFootClock-=dt;
}
function enhPhysicsAfter(dt){
 if(!player.onGround&&enhLastGround){
  enhLandingSquash=Math.min(1,enhLandingSquash+.65);
  enhPixelBurst(player.x+player.w/2,GROUND-2,10,'#6f7471');
 }
 if(player.onGround&&Math.abs(player.vx)>70){
  enhRunDust=Math.min(1,enhRunDust+dt*5);
  if(enhFootClock<=0){enhFootClock=Math.abs(player.vx)>300?.18:.29;stepParticles(player.x+rand(-4,4),GROUND-2,Math.abs(player.vx)>300?3:2,'dust');}
 }else enhRunDust=Math.max(0,enhRunDust-dt*3);
 if(player.shootTimer>0)enhRecoil=.16;
 enhLastGround=player.onGround;
 const desired=clamp(player.vx*.18,-68,68);
 enhCamLead=lerp(enhCamLead,desired,Math.min(1,dt*4));
 const maxCam=(chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH)-W;
 camera=lerp(camera,startingCell?0:player.x-W*.42+enhCamLead,Math.min(1,dt*5.8));
 camera=clamp(camera,0,maxCam);
 if(Math.abs(player.vx)>330&&player.onGround&&mode==='play')shake=Math.max(shake,.35);
}
const enhBaseUpdate=update;
update=function(dt){
 enhPhysicsBefore(dt);
 const prevVy=player.vy;
 enhBaseUpdate(dt);
 if(prevVy>520&&player.onGround)enhLandingSquash=Math.min(1,enhLandingSquash+.35);
 enhPhysicsAfter(dt);
};
function enhBrickDetail(){
 if(mode==='menu'||mode==='intro')return;
 if(interior){
  ctx.save();
  ctx.globalAlpha=.5;
  for(let row=0;row<5;row++){
   const y=98+row*92+(floor%2)*4;
   const off=row%2?31:0;
   for(let i=-1;i<18;i++){
    const x=i*76+off;
    line(x,y,x+54,y,'#383d3d',2);
    line(x+55,y,x+55,y+40,'#242929',2);
   }
  }
  for(let i=0;i<7;i++){
   const x=90+i*180;
   px(x,184,46,5,'#4b4e4b');
   px(x+7,189,32,3,'#202526');
   if(i%2===0){px(x+17,177,5,7,'#7b6d50');px(x+24,176,4,8,'#5f5848');}
  }
  for(let i=0;i<11;i++){
   const x=18+i*123;
   px(x,GROUND-26,72,4,'#333634');
   if(i%3===0)px(x+12,GROUND-31,27,4,'#57554d');
  }
  ctx.restore();
 }else{
  ctx.save();
  ctx.globalAlpha=.6;
  for(let i=0;i<17;i++){
   const wx=115+i*355;
   const x=wx-camera;
   if(x<-90||x>W+90)continue;
   const y=GROUND-185-(i%4)*18;
   line(x,y,x+64,y,'#303536',2);
   for(let q=0;q<4;q++)line(x+12+q*14,y,x+9+q*14,y+22,'#24292a',1);
   if(i%3===0)px(x+26,y-20,22,6,'#444744');
  }
  ctx.restore();
 }
}
function enhRainAndPuddles(){
 if(mode==='menu'||mode==='intro')return;
 ctx.save();
 const rainBoost=interior?.12:1;
 ctx.globalAlpha=.22*rainBoost;
 for(let i=0;i<90;i++){
  const x=(i*97+totalTime*520-camera*.92)%W;
  const y=(i*53+totalTime*760)%442;
  line(x,y,x-5,y+15,'#a4b7bf',1);
 }
 if(!interior){
  ctx.globalAlpha=.16;
  for(let i=0;i<22;i++){
   const x=(i*181-camera)%W;
   const y=GROUND-6-(i%4)*3;
   ctx.fillStyle=i%3===0?'#5b686b':'#3c4547';
   ctx.fillRect(x,y,48+(i%4)*11,2);
   ctx.fillRect(x+9,y+4,28,1);
  }
 }
 ctx.restore();
}
function enhStreetGlints(){
 if(interior||mode==='menu'||mode==='intro')return;
 ctx.save();
 for(let i=0;i<18;i++){
  const x=(i*211-camera*.58)%W;
  const y=GROUND-24-(i%5)*7;
  const pulse=.08+Math.max(0,Math.sin(totalTime*1.6+i))*.07;
  ctx.globalAlpha=pulse;
  px(x,y,32,2,i%2?'#758184':'#9b8e6c');
  px(x+8,y-3,13,2,'#4f595b');
 }
 ctx.restore();
}
const enhSkyBase=drawEnhancedSky;
drawEnhancedSky=function(){enhSkyBase();ctx.save();ctx.globalAlpha=.18;for(let i=0;i<70;i++){const x=(i*181-camera*.08)%W;const y=38+(i*67)%285;px(x,y,1+(i%3),1+(i%2),i%9===0?'#8f9597':'#354047');}for(let i=0;i<7;i++){const x=i*215-(camera*.04%240);const y=92+(i%3)*42;px(x,y,52,5,'#242b30');px(x+18,y-5,33,5,'#1b2227');}ctx.restore();enhBrickDetail();};
const enhGroundBase=drawEnhancedGround;
drawEnhancedGround=function(){enhGroundBase();enhStreetGlints();};
const enhInteriorBase=drawEnhancedInterior;
drawEnhancedInterior=function(){enhInteriorBase();enhBrickDetail();};
const enhWeatherBase=drawEnhancedWeather;
drawEnhancedWeather=function(){enhWeatherBase();enhRainAndPuddles();};
const enhPlayerBase=drawEnhancedPlayer;
drawEnhancedPlayer=function(){
 const x=player.x-camera;
 const bob=player.onGround?Math.sin(player.anim*1.12)*1.4:0;
 const speed=Math.abs(player.vx);
 if(mode==='play'&&player.onGround&&speed>250){
  ctx.save();
  ctx.globalAlpha=Math.min(.16,(speed-250)/900);
  for(let i=0;i<4;i++){
   const ghostX=x-player.facing*(i*8+8);
   drawCharacterSprite(ghostX+8,player.y+bob,selectedCharacter,player.facing,player.anim-i*.38,'');
  }
  ctx.restore();
 }
 enhPlayerBase();
 ctx.save();
 const squash=1+enhLandingSquash*.12;
 const sy=player.y+player.h-(player.h*0.1)*squash;
 ctx.globalAlpha=.28;
 ctx.fillStyle='#000';
 ctx.beginPath();
 ctx.ellipse(x+player.w/2,GROUND+3,23+speed*.028,5+Math.max(0,1-player.onGround)*3,0,0,Math.PI*2);
 ctx.fill();
 ctx.restore();
 if(enhRecoil>0&&mode==='play'){
  const gx=x+27*player.facing;
  const gy=player.y+39;
  ctx.save();ctx.globalAlpha=enhRecoil*2.2;
  px(gx+29*player.facing,gy-6,3,13,'#f0df9c');
  px(gx+35*player.facing,gy-3,12,5,'#d0b46e');
  ctx.restore();
 }
 if(player.onGround&&speed>280&&mode==='play'){
  ctx.save();ctx.globalAlpha=.25+enhRunDust*.2;
  for(let i=0;i<5;i++){
   const dx=x-player.facing*(12+i*12);
   const dy=GROUND-5-(i%2)*4;
   px(dx,dy,3+(i%2),2,'#777a74');
  }
  ctx.restore();
 }
};
const enhInteriorPlayerBase=drawEnhancedInteriorPlayer;
drawEnhancedInteriorPlayer=function(){enhInteriorPlayerBase();if(enhRecoil>0){ctx.save();ctx.globalAlpha=enhRecoil*1.5;px(player.x+player.facing*58,player.y+35,8,3,'#e0c37b');ctx.restore();}};
const enhSmilerBase=drawEnhancedSmiler;
drawEnhancedSmiler=function(){
 enhSmilerBase();
 if(smiler.active&&mode==='play'){
  const sx=smiler.x-camera;
  if(sx>-220&&sx<W+220){ctx.save();const beat=.5+.5*Math.sin(totalTime*7);ctx.globalAlpha=.06+.05*beat;ctx.fillStyle='#b20f18';for(let i=0;i<6;i++)px(sx-40+i*16,GROUND-250+(i%3)*34,3,18,'#741117');ctx.restore();}
 }
};
function enhDrawOverlay(){
 if(mode==='menu'||mode==='intro')return;
 ctx.save();
 if(mode==='play'){
  const speed=Math.abs(player.vx);
  if(speed>300&&player.onGround){ctx.globalAlpha=.04+Math.min(.035,(speed-300)/1800);ctx.fillStyle='#d8d3c7';ctx.fillRect(0,0,W,2);ctx.fillRect(0,H-3,W,3);}
  if(enhAirTime>.18&&!player.onGround){ctx.globalAlpha=Math.min(.06,enhAirTime*.025);ctx.fillStyle='#b6bab4';ctx.fillRect(0,0,W,H);}
 }
 ctx.restore();
}
const enhDrawBase=draw;
draw=function(){enhDrawBase();enhDrawOverlay();};

let jamGoalFocus='escape';
function jamMainMenu(){mode='menu';hide('menu');hide('hud');hide('pause');hide('ending');hide('death');hide('cutscene');hide('gadget');hide('infoFlash');hide('modePicker');hide('credits');show('mainMenu');}
function jamOpenCharacterSelect(){hide('mainMenu');hide('credits');show('menu');mode='menu';}
function jamOpenCredits(){hide('mainMenu');show('credits');mode='menu';}
function jamSimpleGoalData(){
 if(chapter==='ALCATRAZ')return[
  {t:'FIND THE DOCKS',steps:['Follow the prison signs toward the dock.','Enter the Medical Wing and search the clearly marked supply desk for the Dock Pass.','Reach the ferry beacon.']},
  {t:'ESCAPE THE ISLAND',steps:['Use the Dock Pass at the ferry beacon.','Light the beacon and listen for the engine.','Walk to the ferry ladder and press E.']}
 ];
 return[
  {t:'FIND 2 SURVIVORS',steps:['Explore the city streets.','Stand near a survivor and press E.','Repeat until two survivors are with you.']}
 ];
}
function jamGoalIndex(){
 if(chapter==='ALCATRAZ')return finalBoat&&finalBoat.signal>=1?1:0;
 return 0;
}
function jamRenderGoalFocus(){
 const holder=document.getElementById('goalFocus');
 if(!holder)return;
 const buttons=holder.querySelectorAll('button[data-goal]');
 const allowed=chapter==='ALCATRAZ'?['escape','search']:['survivors','search'];
 buttons.forEach(b=>{const g=b.dataset.goal;b.disabled=allowed.indexOf(g)<0;b.classList.toggle('active',g===jamGoalFocus&&!b.disabled);});
}
function jamRenderSimpleObjectives(){
 const list=document.getElementById('objectiveList');
 const sub=document.getElementById('objectivePanelSub');
 const el=document.getElementById('objective');
 if(!list||!sub)return;
 const data=jamSimpleGoalData();
 const current=jamGoalIndex();
 sub.textContent=chapter==='ALCATRAZ'?'ALCATRAZ ISLAND • SIMPLE GOALS':'SAN FRANCISCO • SIMPLE GOAL';
 list.innerHTML='';
 data.forEach((o,i)=>{
  const item=document.createElement('div');
  item.className='objectiveItem '+(i<current?'done ':'')+(i===current?'current':'');
  const mark=i<current?'✓':i===current?'›':'○';
  const steps=o.steps.map((step,n)=>'<div class="'+(i<current?'stepDone':i===current&&n===0?'stepNow':'')+'">'+step+'</div>').join('');
  const note=i===current?'<div class="goalNote">MAIN GOAL • Pick a goal focus above for extra direction.</div>':'';
  item.innerHTML='<div class="objectiveMark">'+mark+'</div><div><strong>'+o.t+'</strong><div class="objectiveSteps">'+steps+'</div>'+note+'</div>';
  list.appendChild(item);
 });
 jamRenderGoalFocus();
 if(el){const o=data[current];const next=o.steps[0]||'';el.textContent='OBJECTIVE\n'+o.t+'\nNEXT STEP\n'+next;}
}
setObjective=jamRenderSimpleObjectives;
renderObjectivePanel=jamRenderSimpleObjectives;

const jamOrigInteractForGoal=interact;
interact=function(){
 const before=survivorsFound;
 jamOrigInteractForGoal();
 if(chapter==='SAN FRANCISCO'&&survivorsFound>=2&&before<2){win('You found two survivors. The city is still full of things that should not be alive.');}
};

document.querySelectorAll('#goalFocus button[data-goal]').forEach(b=>b.addEventListener('click',()=>{jamGoalFocus=b.dataset.goal;jamRenderSimpleObjectives();setMsg('GOAL FOCUS: '+b.textContent,1.1);}));
document.getElementById('mainMenuPlay').onclick=jamOpenCharacterSelect;
document.getElementById('mainMenuCredits').onclick=jamOpenCredits;
document.getElementById('creditsBack').onclick=jamMainMenu;
document.getElementById('mainMenuControls').onclick=()=>{hide('mainMenu');showModePicker();};
document.getElementById('charBack').onclick=jamMainMenu;
document.getElementById('backMenu').onclick=jamMainMenu;
document.getElementById('endingMenu').onclick=jamMainMenu;
document.getElementById('deathMenu').onclick=jamMainMenu;
const jamAccept=document.getElementById('privacyAccept');
if(jamAccept)jamAccept.onclick=()=>{const gate=document.getElementById('privacyGate');if(gate)gate.remove();jamMainMenu();};

function jamExtraPixelGraphics(){
 if(mode==='menu'||mode==='intro')return;
 ctx.save();
 const seedX=Math.floor(camera/17);
 for(let i=0;i<55;i++){
  const wx=(seedX*17+i*127)%((chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH));
  const x=wx-camera;
  if(x<-30||x>W+30)continue;
  const y=GROUND-(i%5)*9-(i%3)*4;
  if(i%4===0){px(x,y,9,3,'#252a29');px(x+3,y-4,3,4,'#3a3f3c');}
  else if(i%4===1){px(x,y,3,12,'#343a37');px(x+4,y+2,5,3,'#525650');}
  else if(i%4===2){line(x,y,x+12,y+1,'#3b403e',1);line(x+7,y+1,x+10,y+7,'#282d2c',1);}
  else{px(x,y,2,2,'#656863');px(x+6,y+3,2,2,'#4b4f4d');}
 }
 if(chapter==='ALCATRAZ'&&!interior){
  const waterY=GROUND+95;
  ctx.globalAlpha=.18;
  for(let i=0;i<18;i++){const x=(i*89-camera*.35)%W;line(x,waterY+(i%4)*7,x+38,waterY+(i%4)*7,'#6a7778',1);}
 }
 if(chapter==='SAN FRANCISCO'&&!interior){
  for(let i=0;i<12;i++){const x=(i*123-camera*.18)%W;const h=28+(i%4)*13;px(x,GROUND-115-h,4,h,'#1b2020');px(x-7,GROUND-115-h,18,4,'#2f3331');}
 }
 if(interior){
  for(let y=105;y<520;y+=47){for(let x=30;x<W;x+=96){if(((x+y)/47)%2===0)px(x,y,17,2,'#222827');}}
 }
 ctx.restore();
}
const jamBaseDrawUltra=draw;
draw=function(){jamBaseDrawUltra();jamExtraPixelGraphics();};

hide('menu');
hide('credits');
show('mainMenu');


function competitionMenuBuild(){
 const menu=document.getElementById('mainMenu');
 if(!menu||menu.querySelector('.competitionMenu'))return;
 const fx=document.createElement('div');
 fx.className='competitionMenu';
 fx.innerHTML='<div class="menuMoon"></div><div class="menuFog"></div><div class="menuFog two"></div><div class="menuScan"></div><div class="menuEyes"><i></i><i></i></div><div class="menuBadge">NIGHTWATCH // ALCATRAZ INCIDENT 01</div><div id="menuSignal" class="menuSignal">SIGNAL: <b>UNSTABLE</b></div>';
 menu.appendChild(fx);
 const threat=menu.querySelector('.menuThreat');
 if(threat)threat.classList.add('menuThreatPulse');
 const logo=menu.querySelector('.menuLogo');
 if(logo){logo.addEventListener('mouseenter',()=>logo.classList.add('menuGlitch'));logo.addEventListener('animationend',()=>logo.classList.remove('menuGlitch'));}
 const buttons=menu.querySelectorAll('button');
 buttons.forEach((b,i)=>{b.addEventListener('mouseenter',()=>{if(window.audioCtx)tone(110+i*16,.025,'square',.006,-4);});});
}
competitionMenuBuild();

const competitionPixelState={time:0,flash:0,blackout:0,shock:0,stepDust:0,menuTick:0,wallEvent:0,wallCooldown:0,returnPulse:0,ambient:0};
function competitionPixel(x,y,w,h,c){px(Math.floor(x),Math.floor(y),Math.max(1,Math.floor(w)),Math.max(1,Math.floor(h)),c);}
function competitionDrawBrickwork(){
 if(mode!=='play')return;
 if(interior){
  for(let row=0;row<5;row++){
   const y=112+row*84;
   const offset=row%2?38:0;
   for(let x=-30+offset;x<W+40;x+=76){
    competitionPixel(x,y,68,2,'#292e2d');
    competitionPixel(x+2,y+3,2,8,'#1a1e1e');
    competitionPixel(x+55,y+3,2,8,'#15191a');
   }
  }
 }else{
  const base=Math.floor(camera/76)*76;
  for(let i=-2;i<20;i++){
   const x=base+i*76-camera;
   const h=45+(i%5)*11;
   competitionPixel(x,GROUND-h,68,2,'#2b302f');
   competitionPixel(x+5,GROUND-h+4,2,10,'#171b1c');
   competitionPixel(x+39,GROUND-h+4,2,10,'#171b1c');
   if(i%3===0)competitionPixel(x+11,GROUND-h+16,24,3,'#383b39');
  }
 }
}
function competitionDrawStreetTexture(){
 if(mode!=='play'||interior)return;
 for(let i=0;i<75;i++){
  const wx=i*181+41;
  const x=wx-camera;
  if(x<-35||x>W+35)continue;
  const y=GROUND+4+(i%10)*13;
  if(i%7===0){competitionPixel(x,y,31,3,'#353838');competitionPixel(x+6,y+5,17,2,'#222626');}
  else if(i%5===0){competitionPixel(x,y,8,4,'#4e504b');competitionPixel(x+9,y+2,4,3,'#343736');}
  else{competitionPixel(x,y,2+(i%3),2,'#4b4d49');}
 }
 for(let i=0;i<13;i++){
  const x=(i*131-camera*.7)%W;
  const y=GROUND+31+(i%3)*14;
  ctx.save();ctx.globalAlpha=.18;ctx.fillStyle='#879198';ctx.fillRect(x,y,52,2);ctx.fillRect(x+9,y+5,31,1);ctx.restore();
 }
}
function competitionDrawInteriorDetail(){
 if(mode!=='play'||!interior)return;
 for(let i=0;i<7;i++){
  const x=76+i*188;
  competitionPixel(x,112,82,5,'#101415');
  competitionPixel(x+6,117,69,4,'#3d4240');
  competitionPixel(x+12,121,54,2,'#1a1e1e');
  competitionPixel(x+34,124,4,23,'#4a4f4c');
 }
 for(let i=0;i<5;i++){
  const x=110+i*236;
  competitionPixel(x,465,75,5,'#363b39');
  competitionPixel(x+8,470,58,3,'#181c1c');
  competitionPixel(x+13,456,22,5,'#4e514c');
 }
}
function competitionDrawPlayerMotion(){
 if(mode!=='play')return;
 const x=player.x-camera;
 const lean=Math.max(-3,Math.min(3,player.vx*.012));
 const stride=Math.sin(player.anim)*4;
 const coat=selectedCharacter==='Julia'?'#385154':selectedCharacter==='May'?'#4d5163':'#3b554e';
 ctx.save();
 if(!player.onGround){ctx.globalAlpha=.26;competitionPixel(x-12,player.y+player.h-8,46,4,'#000');}
 ctx.translate(lean,0);
 if(player.onGround&&Math.abs(player.vx)>45){
  competitionPixel(x-13-stride*.35,player.y+player.h-26,10,4,coat);
  competitionPixel(x+28+stride*.35,player.y+player.h-23,10,4,coat);
 }
 if(state.light&&mode==='play'){
  const fx=x+player.facing*52;
  const fy=player.y+37;
  const grad=ctx.createRadialGradient(fx,fy,5,fx+player.facing*150,fy,205);
  grad.addColorStop(0,'rgba(235,229,203,.20)');
  grad.addColorStop(.35,'rgba(215,215,198,.08)');
  grad.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=grad;ctx.fillRect(fx-15,fy-90,330,180);
 }
 ctx.restore();
}
function competitionDrawRainSplash(){
 if(mode!=='play'||interior)return;
 for(let i=0;i<18;i++){
  const x=(i*79+Math.floor(totalTime*310))%W;
  const y=GROUND-2+(i%4)*2;
  ctx.save();ctx.globalAlpha=.08+.03*(i%3);ctx.strokeStyle='#b8c1c0';ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-4,y+5);ctx.moveTo(x,y);ctx.lineTo(x+5,y+4);ctx.stroke();ctx.restore();
 }
}
function competitionDrawHorrorLayers(){
 if(mode!=='play')return;
 if(interior&&competitionPixelState.blackout>0){ctx.save();ctx.fillStyle='rgba(0,0,0,'+Math.min(.78,competitionPixelState.blackout)+')';ctx.fillRect(0,0,W,H);ctx.restore();}
 if(competitionPixelState.shock>0){
  ctx.save();const a=competitionPixelState.shock*.14;ctx.fillStyle='rgba(133,17,24,'+a+')';ctx.fillRect(0,0,W,H);ctx.globalAlpha=a*1.3;
  for(let i=0;i<18;i++){const y=(i*41+Math.floor(totalTime*260))%H;ctx.fillRect(0,y,W,1+(i%2));}
  ctx.restore();
 }
 if(competitionPixelState.flash>0){ctx.save();ctx.fillStyle='rgba(235,230,215,'+competitionPixelState.flash*.16+')';ctx.fillRect(0,0,W,H);ctx.restore();}
 if(competitionPixelState.wallEvent>0){
  const side=player.facing>0?W-94:94;
  ctx.save();ctx.globalAlpha=Math.min(1,competitionPixelState.wallEvent)*.42;
  const tall=220+Math.sin(totalTime*5)*4;
  competitionPixel(side-22,GROUND-tall,44,tall,'#020203');
  competitionPixel(side-14,GROUND-tall-29,28,32,'#020203');
  competitionPixel(side-9,GROUND-tall-20,5,4,'#d0c6b8');
  competitionPixel(side+4,GROUND-tall-20,5,4,'#d0c6b8');
  ctx.restore();
 }
}
function competitionHorrorUpdate(dt){
 competitionPixelState.time+=dt;
 competitionPixelState.flash=Math.max(0,competitionPixelState.flash-dt*3.8);
 competitionPixelState.blackout=Math.max(0,competitionPixelState.blackout-dt*1.7);
 if(!interior)competitionPixelState.blackout=0;
 competitionPixelState.shock=Math.max(0,competitionPixelState.shock-dt*2.2);
 competitionPixelState.wallEvent=Math.max(0,competitionPixelState.wallEvent-dt*1.35);
 competitionPixelState.wallCooldown=Math.max(0,competitionPixelState.wallCooldown-dt);
 competitionPixelState.returnPulse=Math.max(0,competitionPixelState.returnPulse-dt*2);
 competitionPixelState.ambient+=dt;
 if(mode!=='play')return;
 const danger=state.sanity<55?1.45:state.sanity<75?1.16:1;
 if(competitionPixelState.wallCooldown<=0&&Math.random()<dt*.0009*danger){
  competitionPixelState.wallCooldown=18+Math.random()*34;
  const r=Math.random();
  if(r<.28){competitionPixelState.flash=.6;competitionPixelState.shock=.8;showWarning('DID YOU SEE THAT?');tone(36,.55,'sine',.025,-10);shake=Math.max(shake,5);}
  else if(r<.52&&interior){competitionPixelState.blackout=.72;setMsg('The interior lights flicker.',1.4);tone(29,.45,'sine',.025,-9);}
  else if(r<.76){competitionPixelState.wallEvent=.95;setMsg('Something is standing at the edge of the hall.',1.25);tone(47,.5,'triangle',.018,-8);}
  else{competitionPixelState.shock=.55;jamMessage(Math.random()<.5?'KEEP WALKING.':'THE DOOR BEHIND YOU IS OPEN.',1.35);tone(52,.3,'sawtooth',.01,-6);}
 }
 if(document.hidden&&competitionPixelState.returnPulse<=0){competitionPixelState.returnPulse=2;competitionPixelState.flash=.55;jamMessage('YOU CAME BACK.',1.4);tone(31,.5,'sine',.02,-8);}
 if(Math.abs(player.vx)>150&&player.onGround&&Math.random()<dt*.5){stepParticles(player.x,GROUND-3,2,'debris');}
}
const competitionUpdateBase=update;
update=function(dt){competitionUpdateBase(dt);competitionHorrorUpdate(dt);};
const competitionDrawBase=draw;
draw=function(){competitionDrawBase();competitionDrawBrickwork();competitionDrawStreetTexture();competitionDrawInteriorDetail();competitionDrawPlayerMotion();competitionDrawRainSplash();competitionDrawHorrorLayers();};

function competitionMenuPulse(){
 if(mode!=='menu')return;
 const signal=document.getElementById('menuSignal');
 if(signal&&Math.random()<.018){signal.classList.add('menuGlitch');setTimeout(()=>signal.classList.remove('menuGlitch'),140);}
}
const competitionMenuBaseUpdate=update;
update=function(dt){competitionMenuBaseUpdate(dt);competitionMenuPulse();};

window.addEventListener('keydown',e=>{
 if(e.key==='Enter'&&mode==='menu'&&document.getElementById('mainMenu')&&!document.getElementById('mainMenu').classList.contains('hidden')){jamOpenCharacterSelect();return;}
 if((e.key==='c'||e.key==='C')&&mode==='menu'&&document.getElementById('mainMenu')&&!document.getElementById('mainMenu').classList.contains('hidden')){jamOpenCredits();return;}
});

const competitionOriginalStart=startGame;
startGame=function(name){competitionPixelState.flash=.35;competitionPixelState.shock=.2;competitionOriginalStart(name);setTimeout(()=>{const line=document.getElementById('cutline');if(line)line.classList.add('menuGlitch');setTimeout(()=>line&&line.classList.remove('menuGlitch'),160);},120);};

const competitionAccept=document.getElementById('privacyAccept');
if(competitionAccept&&!competitionAccept.dataset.competitionBound){competitionAccept.dataset.competitionBound='1';competitionAccept.addEventListener('click',()=>{const gate=document.getElementById('privacyGate');if(gate)gate.remove();jamMainMenu();});}


const aotdSoundscapeV1=(()=>{
 let ctx=null;
 let master=null;
 let musicGain=null;
 let sfxGain=null;
 let rainGain=null;
 let droneA=null;
 let droneB=null;
 let hum=null;
 let rainSource=null;
 let rainFilter=null;
 let rainBuffer=null;
 let noiseBuffer=null;
 let started=false;
 let enabled=true;
 let stepTimer=0;
 let rainTimer=0;
 let heartbeatTimer=0;
 let musicTimer=0;
 let prevGround=true;
 let prevLight=false;
 let prevInterior=false;
 let prevStartCell=true;
 let prevChapter='ALCATRAZ';
 let prevHealth=100;
 let prevSmiler=false;
 let prevWall=0;
 let prevMode=mode;
 let lastScream=0;
 function ensure(){
  if(!enabled)return null;
  ctx=audio();
  if(!ctx)return null;
  if(!master){
   master=ctx.createGain();master.gain.value=1.42;
   const limiter=ctx.createDynamicsCompressor();limiter.threshold.value=-8;limiter.knee.value=12;limiter.ratio.value=6;limiter.attack.value=.003;limiter.release.value=.16;master.connect(limiter);limiter.connect(ctx.destination);
   musicGain=ctx.createGain();musicGain.gain.value=.34;musicGain.connect(master);
   sfxGain=ctx.createGain();sfxGain.gain.value=1.78;sfxGain.connect(master);
   rainGain=ctx.createGain();rainGain.gain.value=.16;rainGain.connect(master);
  }
  return ctx;
 }
 function noise(seconds){
  const ac=ensure();
  if(!ac)return null;
  const n=Math.max(1,Math.floor(ac.sampleRate*seconds));
  const b=ac.createBuffer(1,n,ac.sampleRate);const d=b.getChannelData(0);
  for(let i=0;i<n;i++)d[i]=(Math.random()*2-1)*.65;
  return b;
 }
 function burst(freq,duration,type,volume,slide,filterType,filterFreq){
  const ac=ensure();if(!ac)return;
  const t=ac.currentTime;
  const o=ac.createOscillator();const g=ac.createGain();
  o.type=type;o.frequency.setValueAtTime(Math.max(20,freq),t);
  if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(20,freq+slide),t+duration);
  g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(Math.max(.0002,volume),t+.008);g.gain.exponentialRampToValueAtTime(.0001,t+duration);
  if(filterType){const f=ac.createBiquadFilter();f.type=filterType;f.frequency.value=filterFreq||900;o.connect(f);f.connect(g);}else{o.connect(g);}
  g.connect(sfxGain);o.start(t);o.stop(t+duration+.025);
 }
 function noiseBurst(duration,volume,filterType,filterFreq,lowpass){
  const ac=ensure();if(!ac)return;
  const src=ac.createBufferSource();const g=ac.createGain();const f=ac.createBiquadFilter();
  src.buffer=noiseBuffer||noise(Math.min(1.5,Math.max(.1,duration+.04)));f.type=filterType||'bandpass';f.frequency.value=filterFreq||1400;f.Q.value=lowpass||.7;
  g.gain.setValueAtTime(.0001,ac.currentTime);g.gain.linearRampToValueAtTime(volume,ac.currentTime+.015);g.gain.exponentialRampToValueAtTime(.0001,ac.currentTime+duration);
  src.connect(f);f.connect(g);g.connect(sfxGain);src.start();src.stop(ac.currentTime+duration+.02);
 }
 function startRain(){
  const ac=ensure();if(!ac||rainSource)return;
  rainBuffer=noise(2.4);rainSource=ac.createBufferSource();rainFilter=ac.createBiquadFilter();rainFilter.type='bandpass';rainFilter.frequency.value=3100;rainFilter.Q.value=.55;rainSource.buffer=rainBuffer;rainSource.loop=true;rainGain.gain.value=.105;rainSource.connect(rainFilter);rainFilter.connect(rainGain);rainSource.start();
 }
 function startMusic(){
  const ac=ensure();if(!ac||droneA)return;
  droneA=ac.createOscillator();droneB=ac.createOscillator();hum=ac.createOscillator();
  const filter=ac.createBiquadFilter();const g=ac.createGain();
  filter.type='lowpass';filter.frequency.value=760;filter.Q.value=2.4;g.gain.value=.0001;
  droneA.type='sine';droneA.frequency.value=43;droneB.type='triangle';droneB.frequency.value=64.5;hum.type='sine';hum.frequency.value=21.5;
  droneA.connect(filter);droneB.connect(filter);hum.connect(filter);filter.connect(g);g.connect(musicGain);
  droneA.start();droneB.start();hum.start();
  musicTimer=0;
 }
 function start(){
  if(!enabled)return;
  ensure();if(!ctx)return;
  startRain();startMusic();started=true;
 }
 function stop(){
  try{if(rainSource){rainSource.stop();rainSource.disconnect();}}catch(e){}
  try{if(droneA)droneA.stop();if(droneB)droneB.stop();if(hum)hum.stop();}catch(e){}
  rainSource=null;droneA=null;droneB=null;hum=null;started=false;
 }
 function setEnabled(v){
  enabled=!!v;
  const panel=document.getElementById('aotdSoundPanel');
  if(panel){panel.classList.toggle('off',!enabled);panel.innerHTML='SOUND: <b>'+(enabled?'ON':'OFF')+'</b>';panel.setAttribute('aria-pressed',enabled?'true':'false');panel.classList.toggle('hidden',typeof mode!=='undefined'&&mode!=='play');}
  const on=document.getElementById('soundOn'),off=document.getElementById('soundOff');
  if(on)on.classList.toggle('active',enabled);if(off)off.classList.toggle('active',!enabled);
  if(enabled)start();else stop();
 }
 function unlock(){if(enabled){audio();start();}}
 function footstep(){
  noiseBurst(.095,.18,'lowpass',1050,1);
  burst(72,.10,'sine',.085,-15,'lowpass',430);
  burst(118,.045,'triangle',.042,-10,'bandpass',760);
 }
 function jump(){burst(180,.12,'triangle',.07,55,'lowpass',900);noiseBurst(.09,.04,'highpass',1500,1);}
 function land(){burst(58,.14,'sine',.09,-22,'lowpass',360);noiseBurst(.13,.05,'lowpass',700,1);}
 function door(){burst(50,.26,'square',.10,-23,'lowpass',650);noiseBurst(.18,.055,'bandpass',520,1.2);}
 function chest(){burst(150,.16,'square',.09,85,'lowpass',1050);setTimeout(()=>burst(235,.14,'triangle',.07,130,'lowpass',1500),85);setTimeout(()=>burst(520,.08,'sine',.045,160,'highpass',1800),160);}
 function pickup(){burst(440,.09,'square',.06,90,'lowpass',2000);burst(700,.07,'triangle',.035,120,'highpass',1800);}
 function reload(){burst(190,.08,'square',.027,35,'highpass',700);setTimeout(()=>burst(280,.1,'triangle',.025,55,'bandpass',1500),85);}
 function shot(){burst(94,.075,'sawtooth',.08,-38,'lowpass',1500);noiseBurst(.065,.06,'highpass',1800,1);}
 function grenade(){burst(52,.38,'sawtooth',.11,-30,'lowpass',600);setTimeout(()=>noiseBurst(.26,.09,'lowpass',740,1),75);}
 function flashlight(){burst(prevLight?125:210,.075,'square',.022,20,'highpass',1300);}
 function playerHit(){burst(69,.16,'sawtooth',.055,-25,'bandpass',430);noiseBurst(.075,.02,'highpass',1900,1);}
 function survivor(){burst(330,.15,'triangle',.026,80,'lowpass',1700);setTimeout(()=>burst(495,.18,'sine',.018,50,'lowpass',1800),80);}
 function ferry(){burst(72,.5,'sine',.055,22,'lowpass',500);setTimeout(()=>burst(118,.5,'triangle',.034,-12,'lowpass',740),180);}
 function scream(power=1){
  const now=performance.now();if(now-lastScream<1300)return;lastScream=now;
  const ac=ensure();if(!ac)return;
  const t=ac.currentTime;
  const o=ac.createOscillator();const g=ac.createGain();const f=ac.createBiquadFilter();
  o.type='sawtooth';o.frequency.setValueAtTime(760,t);o.frequency.exponentialRampToValueAtTime(145,t+.34);o.frequency.exponentialRampToValueAtTime(300,t+.83);
  f.type='bandpass';f.frequency.value=1350;f.Q.value=1.1;
  g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.13*power,t+.025);g.gain.exponentialRampToValueAtTime(.0001,t+.9);
  o.connect(f);f.connect(g);g.connect(sfxGain);o.start(t);o.stop(t+.93);
  noiseBurst(.78,.09*power,'bandpass',2100,1.2);
  setTimeout(()=>burst(52,.16*power,'square',.25*power,-18,'lowpass',520),65);
 }
 function whisper(){burst(240,.32,'sine',.008,-80,'bandpass',1100);noiseBurst(.31,.006,'bandpass',1700,1.4);}
 function update(dt){
  if(!enabled)return;
  const ac=ensure();if(!ac)return;
  if(!started)start();
  stepTimer=Math.max(0,stepTimer-dt);rainTimer=Math.max(0,rainTimer-dt);heartbeatTimer=Math.max(0,heartbeatTimer-dt);musicTimer=Math.max(0,musicTimer-dt);lastScream=Math.max(0,lastScream-0);
  if(master&&musicGain&&rainGain){
   const sanity=typeof state!=='undefined'?clamp(state.sanity||100,0,100):100;
   const stress=1+(100-sanity)/130+(typeof smiler!=='undefined'&&smiler.active?.55:0);
   musicGain.gain.setTargetAtTime(.18+.035*stress,ac.currentTime,.12);
   rainGain.gain.setTargetAtTime((typeof interior!=='undefined'&&interior)?.035:.085,ac.currentTime,.25);
  }
  if(mode==='play'&&!chestUIOpen&&!gadgetOpen){
   const moving=Math.abs(player.vx)>48&&player.onGround;
   if(moving&&stepTimer<=0){const run=Math.abs(player.vx)>260;stepTimer=run?.26:.42;footstep();}
   if(typeof player!=='undefined'&&prevGround!==player.onGround){if(player.onGround)land();else jump();}
   
   if(typeof state!=='undefined'&&state.light!==prevLight){flashlight();}
   if(typeof startingCell!=='undefined'&&prevStartCell&&!startingCell){door();}
   if(typeof interior!=='undefined'&&!!interior!==prevInterior)door();
   if(typeof state!=='undefined'&&state.health<prevHealth-2)playerHit();
   if(typeof smiler!=='undefined'&&smiler.active&&!prevSmiler){whisper();}
   if(typeof competitionPixelState!=='undefined'&&competitionPixelState.wallEvent>0&&prevWall<=0){scream(1);}
   if(typeof chapter!=='undefined'&&chapter!==prevChapter){ferry();}
   if(typeof state!=='undefined'&&typeof survivorsFound!=='undefined'&&survivorsFound>soundStatePrevSurvivors){survivor();}
   if(typeof chapter!=='undefined'&&chapter==='ALCATRAZ'&&!interior&&rainTimer<=0){rainTimer=.16+Math.random()*.28;if(Math.random()<.8){noiseBurst(.025,.006,'highpass',2600,1);}}
  }
  if(mode==='menu'&&musicTimer<=0){musicTimer=2.8;burst(88+Math.random()*28,.26,'sine',.006,-20,'lowpass',500);}
  prevGround=typeof player!=='undefined'?player.onGround:prevGround;
  prevLight=typeof state!=='undefined'?state.light:prevLight;
  prevInterior=typeof interior!=='undefined'&&!!interior;
  prevStartCell=typeof startingCell!=='undefined'?startingCell:prevStartCell;
  prevChapter=typeof chapter!=='undefined'?chapter:prevChapter;
  prevHealth=typeof state!=='undefined'?state.health:prevHealth;
  prevSmiler=typeof smiler!=='undefined'?smiler.active:prevSmiler;
  prevWall=typeof competitionPixelState!=='undefined'?competitionPixelState.wallEvent:prevWall;
  soundStatePrevSurvivors=typeof survivorsFound!=='undefined'?survivorsFound:soundStatePrevSurvivors;
 }
 let soundStatePrevSurvivors=0;
 return {start,stop,setEnabled,unlock,update,footstep,jump,land,door,chest,pickup,reload,shot,grenade,flashlight,playerHit,scream,whisper};
})();

function aotdSyncControlMode(){
 const btns=document.querySelectorAll('#modePicker [data-mode]');btns.forEach(b=>{const on=b.dataset.mode===controlMode;b.classList.toggle('active',on);b.setAttribute('aria-pressed',on?'true':'false');});
 const sub=document.querySelector('#modePicker .modeSub');if(sub)sub.textContent=controlMode==='mobile'?'MOBILE / TOUCH — virtual buttons are active.':'LAPTOP / DESKTOP — keyboard and mouse are active.';
}
const aotdOriginalSetControlMode=setControlMode;
setControlMode=function(next){aotdOriginalSetControlMode(next);aotdSyncControlMode();};
function aotdBindSoundUi(){
 const panel=document.getElementById('aotdSoundPanel');
 if(panel)panel.onclick=()=>aotdSoundscapeV1.setEnabled(!panel.classList.contains('off'));
 const on=document.getElementById('soundOn'),off=document.getElementById('soundOff');
 if(on)on.onclick=()=>aotdSoundscapeV1.setEnabled(true);
 if(off)off.onclick=()=>aotdSoundscapeV1.setEnabled(false);
 document.querySelectorAll('#modePicker [data-mode]').forEach(b=>b.addEventListener('click',()=>setTimeout(aotdSyncControlMode,0)));
 aotdSyncControlMode();
}
aotdBindSoundUi();
const aotdOldStartGame=startGame;
startGame=function(name){aotdSoundscapeV1.unlock();aotdSoundscapeV1.start();aotdOldStartGame(name);};
const aotdOldFinishIntro=finishIntro;
finishIntro=function(){aotdSoundscapeV1.unlock();aotdSoundscapeV1.start();aotdOldFinishIntro();};
const aotdOldOpenChestUI=openChestUI;
openChestUI=function(c){aotdOldOpenChestUI(c);aotdSoundscapeV1.chest();};
const aotdOldCloseChestUI=closeChestUI;
closeChestUI=function(){aotdOldCloseChestUI();aotdSoundscapeV1.door();};
const aotdOldReload=reload;
reload=function(){aotdOldReload();aotdSoundscapeV1.reload();};
const aotdOldUseItem=useItem;
useItem=function(){aotdOldUseItem();aotdSoundscapeV1.pickup();};
const aotdOldShoot=shoot;
shoot=function(){const old=player.shootTimer;aotdOldShoot();if(player.shootTimer!==old)aotdSoundscapeV1.shot();};
const aotdOldInteract=interact;
interact=function(){aotdOldInteract();};
const aotdOldUpdate=update;
update=function(dt){aotdOldUpdate(dt);aotdSoundscapeV1.update(dt);};
window.addEventListener('pointerdown',()=>aotdSoundscapeV1.unlock(),{passive:true});
window.addEventListener('keydown',()=>aotdSoundscapeV1.unlock(),{passive:true});


let interiorAnimClock=0;
function aotdInteriorAnimationUpgrade(){
 drawCharacterSprite=function(x,y,who,dir,anim,role){
  const t=anim||0;
  const walk=Math.sin(t)*1;
  const step=Math.sin(t)*5;
  const lift=Math.max(0,Math.sin(t*2.0))*1.2;
  const breathe=Math.sin(totalTime*2.3+x*.01)*.7;
  const run=Math.min(1,Math.abs(player&&player.vx?player.vx:0)/330);
  const skin=who==='Yumi'?'#d0b79f':who==='May'?'#d0b49b':'#c9ac95';
  const hair=who==='Yumi'?'#101415':who==='May'?'#51362b':'#2b2222';
  const hairHi=who==='Yumi'?'#2b3030':who==='May'?'#76503d':'#4d3732';
  const coat=who==='Yumi'?'#2e3b37':who==='May'?'#343845':'#29383a';
  const coatHi=who==='Yumi'?'#47564f':who==='May'?'#555b6d':'#405355';
  const shirt='#c9c3b5';
  const pants='#1c2224';
  const boot='#0c1012';
  const metal='#c6b26f';
  const dirSign=dir||1;
  const yy=y+Math.sin(t*.5)*.4-lift;
  px(x-22,yy+70,60,7,'rgba(0,0,0,.46)');
  px(x-6+step*.12,yy+48,13,21,pants);
  px(x+10-step*.12,yy+48,13,21,pants);
  px(x-9-step*.10,yy+67,17,7,boot);
  px(x+8+step*.10,yy+67,17,7,boot);
  px(x-12,yy+23,43,30,coat);
  px(x-6,yy+23,31,16,shirt);
  px(x+1,yy+25,7,12,who==='May'?'#515c67':'#3e4b47');
  px(x-15+step*.09,yy+26,10,28,coatHi);
  px(x+29-step*.09,yy+26,10,28,coatHi);
  px(x-16+step*.2,yy+49,13,9,coat);
  px(x+27-step*.2,yy+49,13,9,coat);
  px(x-8,yy+2+breathe,32,28,skin);
  px(x-11,yy-7+breathe,39,13,hair);
  px(x-8,yy-13+breathe,33,9,hairHi);
  if(who==='Julia'){px(x+18,yy-9+breathe,11,8,hairHi);px(x+24,yy-2+breathe,9,23,hairHi);px(x+30,yy+7+breathe,6,13,hairHi);}
  if(who==='May'){px(x-14,yy-5+breathe,8,29,hairHi);px(x+24,yy-3+breathe,11,23,hairHi);px(x+29,yy+7+breathe,7,17,hairHi);}
  if(who==='Yumi'){px(x-14,yy-1+breathe,8,27,hairHi);px(x+26,yy-1+breathe,10,31,hairHi);px(x-10,yy-14+breathe,30,6,hair);}
  px(x-1,yy+10+breathe,4,4,'#111415');
  px(x+18,yy+10+breathe,4,4,'#111415');
  px(x+3,yy+18+breathe,17,3,'#8a5c55');
  px(x-5,yy+30,8,13,coatHi);
  px(x+18,yy+30,8,13,coatHi);
  px(x-10,yy+24,6,7,metal);
  px(x-8,yy+25,3,3,'#fff2a0');
  if(role==='Soldier'){px(x-15,yy-5,40,9,'#3f4c43');px(x-6,yy-10,25,5,'#29332e');}
  if(role==='Nurse'){px(x-8,yy+30,34,7,'#737d77');px(x+2,yy+31,5,18,'#e5e1d8');px(x,yy+37,10,5,'#e5e1d8');}
  if(role==='Mechanic'){px(x-9,yy+20,35,7,'#5e4a3a');px(x+28,yy+35,8,14,'#8e7359');}
 };
 const oldEnhancedInteriorPlayer=drawEnhancedInteriorPlayer;
 drawEnhancedInteriorPlayer=function(){
  drawCharacterSprite(player.x,player.y,selectedCharacter,player.facing,player.anim,'');
  const gunX=player.x+25*player.facing;
  const gunY=player.y+39;
  px(gunX+(player.facing>0?0:-28),gunY-3,30,6,'#101416');
  px(gunX+(player.facing>0?21:-7),gunY-5,9,3,'#737773');
  if(player.shootTimer>0){
   px(gunX+player.facing*29,gunY-6,8,12,'#f0d789');
   px(gunX+player.facing*38,gunY-3,6,6,'#fff0ae');
  }
 };
 const oldEnhancedPlayer=drawEnhancedPlayer;
 drawEnhancedPlayer=function(){
  const x=player.x-camera;
  ctx.save();
  if(player.hitTimer>0&&Math.floor(totalTime*20)%2===0)ctx.globalAlpha=.45;
  drawCharacterSprite(x+8,player.y,selectedCharacter,player.facing,player.anim,'');
  const gunX=x+25*player.facing;
  const gunY=player.y+39;
  px(gunX+(player.facing>0?0:-28),gunY-3,30,6,'#101416');
  px(gunX+(player.facing>0?21:-7),gunY-5,9,3,'#737773');
  if(player.shootTimer>0){
   px(gunX+player.facing*29,gunY-6,8,12,'#f0d789');
   px(gunX+player.facing*38,gunY-3,6,6,'#fff0ae');
  }
  ctx.restore();
 };
}
aotdInteriorAnimationUpgrade();
function aotdInteriorAmbience(dt){
 if(mode!=='play'||!interior)return;
 if(typeof interiorAnimClock==='undefined')interiorAnimClock=0;
 interiorAnimClock+=dt;
 if(Math.random()<dt*.9){
  const x=35+Math.random()*(W-70);
  const y=100+Math.random()*390;
  px(x,y,1,1,Math.random()<.5?'#59615c':'#2e3532');
 }
}
const aotdPreAnimUpdate=update;
update=function(dt){aotdPreAnimUpdate(dt);aotdInteriorAmbience(dt);};
function aotdMenuPolish(){
 const m=document.getElementById('mainMenu');
 if(!m)return;
 const box=m.querySelector('.mainMenuBox');
 if(box&&!box.querySelector('.menuSignal')){
  const signal=document.createElement('div');signal.className='menuSignal';signal.textContent='SIGNAL // 07';signal.style.cssText='position:absolute;left:18px;bottom:10px;color:#4f5954;font:9px Consolas,monospace;letter-spacing:2px';box.appendChild(signal);
 }
}
aotdMenuPolish();

const aotdCompetitionFixStyle=document.createElement('style');
aotdCompetitionFixStyle.textContent=`
#aotdJumpScare{position:absolute;inset:0;z-index:68;pointer-events:none;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.18)}
#aotdJumpScare.show{display:flex}
#aotdJumpScare .face{position:relative;width:220px;height:250px;background:#030304;border:3px solid #111;box-shadow:0 0 70px rgba(255,255,255,.12),0 0 24px rgba(130,0,10,.35);image-rendering:pixelated}
#aotdJumpScare .eye{position:absolute;top:70px;width:28px;height:14px;background:#e8e0d2;box-shadow:0 0 16px rgba(255,240,210,.7)}
#aotdJumpScare .eye.left{left:45px}.aotdJumpScare .eye.right{right:45px}
#aotdJumpScare .mouth{position:absolute;left:45px;right:45px;bottom:55px;height:60px;border-top:5px solid #8c7370;border-bottom:5px solid #8c7370;background:#0a0809}
#aotdRoomBanner{position:absolute;left:18px;top:83px;z-index:28;pointer-events:none;color:#d5cfc2;font:700 10px Consolas,monospace;letter-spacing:2px;text-shadow:2px 2px #000;opacity:0;transition:opacity .15s}
`;
document.head.appendChild(aotdCompetitionFixStyle);
const aotdJumpScareEl=document.createElement('div');
aotdJumpScareEl.id='aotdJumpScare';
aotdJumpScareEl.innerHTML='<div class="face"><div class="eye left"></div><div class="eye right"></div><div class="mouth"></div></div>';
document.body.appendChild(aotdJumpScareEl);
const aotdRoomBanner=document.createElement('div');
aotdRoomBanner.id='aotdRoomBanner';
document.body.appendChild(aotdRoomBanner);
let aotdScareDirector={timer:10+Math.random()*12,cooldown:0,flash:0,active:false,face:0};
let aotdFootAudioSafety=0;
function aotdTriggerJumpscare(power=1){
 if(mode!=='play'||chestUIOpen||gadgetOpen||aotdScareDirector.cooldown>0)return;
 aotdScareDirector.cooldown=18+Math.random()*17;
 aotdScareDirector.flash=.85*power;
 aotdScareDirector.face=.42+.18*power;
 aotdScareDirector.active=true;
 aotdJumpScareEl.classList.add('show');
 aotdJumpScareEl.style.opacity=String(Math.min(1,.82+.12*power));
 showWarning('RUN.');
 jamMessage(Math.random()<.5?'HE WAS CLOSER THAN YOU THOUGHT':'DON’T TURN AROUND.',1.4);
 aotdSoundscapeV1.scream(1.7*power);
 shake=Math.max(shake,10*power);
 flash=Math.max(flash,.55*power);
 setTimeout(()=>{aotdJumpScareEl.classList.remove('show');aotdScareDirector.active=false;},Math.max(260,520-power*80));
}
function aotdUpdateScareDirector(dt){
 if(mode!=='play')return;
 aotdScareDirector.timer-=dt;
 aotdScareDirector.cooldown=Math.max(0,aotdScareDirector.cooldown-dt);
 aotdScareDirector.flash=Math.max(0,aotdScareDirector.flash-dt*2.7);
 if(aotdScareDirector.timer<=0&&aotdScareDirector.cooldown<=0){
  const danger=state.sanity<55?1.35:state.sanity<75?1.12:1;
  aotdScareDirector.timer=(18+Math.random()*20)/danger;
  if(Math.random()<.48||state.sanity<38)aotdTriggerJumpscare(state.sanity<38?1.18:1);
 }
 if(smiler.active&&Math.abs(smiler.x-player.x)<320&&Math.random()<dt*.085)aotdSoundscapeV1.scream(.75);
}
function aotdRoomRender(){
 if(mode!=='play'||!interior)return;
 const b=interior.building;
 const ground=GROUND-20;
 ctx.save();
 ctx.fillStyle='#06090b';ctx.fillRect(0,0,W,H);
 const wall=ctx.createLinearGradient(0,60,0,560);wall.addColorStop(0,'#0e1316');wall.addColorStop(.52,b.type==='prison'?'#303536':'#242b2c');wall.addColorStop(1,'#111516');ctx.fillStyle=wall;ctx.fillRect(0,62,W,505);
 px(0,62,W,9,'#4b504f');px(0,72,W,5,'#181d1e');
 for(let row=0;row<9;row++)for(let col=0;col<18;col++){const x=col*78+(row%2)*39;const y=92+row*50;line(x,y,x+50,y,'#3a3f3e',1);px(x+2,y+3,2,11,'#242928');}
 px(0,545,W,175,'#0a0e0f');
 for(let i=0;i<18;i++){const x=i*73;px(x,545,50,5,'#282d2c');px(x+8,551,2,115,'#161b1b');}
 px(38,395,235,120,'#161b1c');px(52,364,205,35,'#414644');px(84,321,92,44,'#080c0d');px(82,354,128,7,'#50524b');
 px(770,407,190,108,'#332e2a');px(789,368,150,39,'#252a2a');px(812,380,23,9,'#615844');
 px(1048,361,105,154,'#161b1c');for(let i=0;i<5;i++)px(1056,375+i*26,87,5,'#555b57');
 const doorX=610;px(doorX-68,365,136,150,'#090c0d');px(doorX-58,378,116,137,'#1c2223');px(doorX+36,430,5,5,'#9f8b5d');
 ctx.fillStyle='#d2c8a2';ctx.fillRect(doorX-77,344,154,2);
 ctx.font='bold 16px Consolas';ctx.fillStyle='#ba4c4b';ctx.fillText(b.name.toUpperCase(),270,104);
 ctx.font='11px Consolas';ctx.fillStyle='#8f9893';ctx.fillText(`FLOOR ${floor}  •  INTERIOR`,500,128);
 for(let i=0;i<5;i++){const x=150+i*205;px(x,152,82,48,'#111617');px(x+9,162,64,6,'#4f5350');px(x+20,178,41,12,'#272c2c');if(i%2===0)px(x+33,192,9,5,'#7d6b49');}
 if(floor>=2){px(382,165,140,12,'#141919');px(382,177,10,220,'#2d3332');px(512,177,10,220,'#202727');for(let i=0;i<6;i++){line(392+i*20,390,432+i*20,180,'#414745',3);}}
 for(let i=0;i<15;i++){const x=20+i*86;const y=220+(i%4)*66;px(x,y,42,4,'#303534');px(x+6,y+6,28,3,'#171c1c');if(i%4===0){px(x+12,y-14,6,14,'#4d524f');px(x+7,y-19,16,6,'#6d6554');}}
 if(chests.some(c=>c.inside&&c.buildingName===b.name))drawInteriorLoot();
 drawEnhancedInteriorPlayer();
 for(const p of particles){const x=p.x;ctx.save();ctx.globalAlpha=clamp(p.life*2,0,1);px(x,p.y,p.size,p.size,p.c);ctx.restore();}
 ctx.font='bold 10px Consolas';ctx.fillStyle='#c9c4b5';ctx.fillText('LEFT EXIT',32,338);ctx.fillText('RIGHT EXIT',1090,338);
 ctx.font='9px Consolas';ctx.fillStyle='#777f7a';ctx.fillText('WALLS / FLOOR / DOOR / PROPS',32,690);
 ctx.restore();
}
function aotdRoomUi(dt){
 const b=document.getElementById('aotdRoomBanner');
 if(!b)return;
 if(mode==='play'&&interior){b.textContent=`${interior.building.name.toUpperCase()}  //  FLOOR ${floor}  //  SEARCH THE ROOM`;b.style.opacity='1';}
 else b.style.opacity='0';
}
const aotdPreFinalUpdate=update;
update=function(dt){aotdPreFinalUpdate(dt);aotdUpdateScareDirector(dt);aotdRoomUi(dt);if(mode==='play'&&!interior){aotdFootAudioSafety=Math.max(0,aotdFootAudioSafety-dt);if(Math.abs(player.vx)>55&&player.onGround&&aotdFootAudioSafety<=0){aotdFootAudioSafety=Math.abs(player.vx)>260?.23:.34;aotdSoundscapeV1.footstep();}}};
const aotdPreFinalDraw=draw;
draw=function(){
 if(mode==='play'&&interior){aotdRoomRender();drawHorrorOverlay();if(aotdScareDirector.flash>0){ctx.save();ctx.globalAlpha=aotdScareDirector.flash*.12;ctx.fillStyle='#f0e8dc';ctx.fillRect(0,0,W,H);ctx.restore();}return;}
 aotdPreFinalDraw();
 if(mode==='play'&&aotdScareDirector.flash>0){ctx.save();ctx.globalAlpha=aotdScareDirector.flash*.12;ctx.fillStyle='#f0e8dc';ctx.fillRect(0,0,W,H);ctx.restore();}
};


const aotdUpgradeRoot=document.querySelector('.shell')||document.body;
const aotdRoomTransition=document.createElement('div');
aotdRoomTransition.className='roomTransitionScreen';
aotdRoomTransition.innerHTML='<div class="roomTransitionLabel"></div>';
aotdUpgradeRoot.appendChild(aotdRoomTransition);
let aotdRoomTransitionState={active:false,phase:'idle',timer:0,duration:.44,pending:null};
function aotdRoomTransitionStart(label,fn){
 if(aotdRoomTransitionState.active)return;
 aotdRoomTransitionState={active:true,phase:'out',timer:0,duration:.44,pending:fn};
 const labelEl=aotdRoomTransition.querySelector('.roomTransitionLabel');
 if(labelEl)labelEl.textContent=label||'ENTERING...';
 aotdRoomTransition.classList.add('on');
 tone(42,.18,'sine',.025,-6);
}
function aotdRoomTransitionUpdate(dt){
 if(!aotdRoomTransitionState.active)return;
 aotdRoomTransitionState.timer+=dt;
 if(aotdRoomTransitionState.phase==='out'&&aotdRoomTransitionState.timer>=aotdRoomTransitionState.duration*.52){
  aotdRoomTransitionState.phase='in';
  aotdRoomTransitionState.timer=0;
  const fn=aotdRoomTransitionState.pending;
  aotdRoomTransitionState.pending=null;
  if(fn)fn();
  tone(58,.2,'triangle',.02,18);
 }
 if(aotdRoomTransitionState.phase==='in'&&aotdRoomTransitionState.timer>=aotdRoomTransitionState.duration){
  aotdRoomTransition.classList.remove('on');
  aotdRoomTransitionState={active:false,phase:'idle',timer:0,duration:.44,pending:null};
 }
}
const aotdOriginalInsideBuildingV3=finalInsideBuildingV2;
const aotdOriginalExitBuildingV3=finalExitBuildingV2;
function aotdInsideBuildingSmooth(b){
 if(!b||aotdRoomTransitionState.active)return;
 aotdRoomTransitionStart(b.name.toUpperCase(),()=>aotdOriginalInsideBuildingV3(b));
}
function aotdExitBuildingSmooth(side){
 if(!interior||aotdRoomTransitionState.active)return;
 const name=interior.building.name;
 aotdRoomTransitionStart('RETURNING TO STREET',()=>aotdOriginalExitBuildingV3(side));
}
finalInsideBuildingV2=aotdInsideBuildingSmooth;
finalExitBuildingV2=aotdExitBuildingSmooth;
insideBuilding=aotdInsideBuildingSmooth;
exitBuilding=aotdExitBuildingSmooth;
const aotdFinalUpdateV3=update;
update=function(dt){
 aotdFinalUpdateV3(dt);
 aotdRoomTransitionUpdate(dt);
};
const aotdFinalInteractV3=interact;
let aotdMedicalPassClaimed=false;
const aotdOriginalResetWorldV3=resetWorld;
resetWorld=function(){aotdOriginalResetWorldV3();aotdMedicalPassClaimed=false;};
function aotdMedicalPassInteract(){
 if(mode!=='play'||!interior||interior.building.name!=='MEDICAL WING'||aotdMedicalPassClaimed)return false;
 if(player.x>=650&&player.x<=980){
  aotdMedicalPassClaimed=true;
  state.dockPass=true;
  state.sanity=Math.min(100,state.sanity+4);
  objectiveStep=Math.max(objectiveStep,4);
  addItem('ammo',8);
  setObjective();
  setMsg('DOCK PASS FOUND — MEDICAL WING SUPPLY DESK.',3);
  stepParticles(820,460,16,'spark');
  aotdSoundscapeV1.pickup();
  aotdSoundscapeV1.chest();
  aotdTriggerJumpscare(.72);
  return true;
 }
 return false;
}
interact=function(){
 if(mode!=='play'||gadgetOpen||chestUIOpen||aotdRoomTransitionState.active)return;
 if(interior&&interior.building.name==='MEDICAL WING'&&aotdMedicalPassInteract())return;
 if(interior){
  if(player.x<95){aotdExitBuildingSmooth('left');return;}
  if(player.x>1135){aotdExitBuildingSmooth('right');return;}
 }
 if(!interior){
  const b=finalCurrentBuildingV2();
  if(b&&Math.abs(player.x-(b.x+b.w*.5))<220){aotdInsideBuildingSmooth(b);return;}
 }
 aotdFinalInteractV3();
};
function aotdRoomProximityPrompt(){
 const b=document.getElementById('aotdRoomBanner');
 if(!b||mode!=='play')return;
 if(interior&&interior.building.name==='MEDICAL WING'&&!aotdMedicalPassClaimed){
  b.textContent='MEDICAL WING  //  SUPPLY DESK → DOCK PASS';
  b.style.opacity='1';
 }else if(interior){
  b.textContent=`${interior.building.name.toUpperCase()}  //  FLOOR ${floor}  //  SEARCH THE ROOM`;
  b.style.opacity='1';
 }
 const pm=document.getElementById('medicalPassMarker');
 if(pm){
  const visible=mode==='play'&&interior&&interior.building.name==='MEDICAL WING'&&!aotdMedicalPassClaimed;
  pm.style.display=visible?'block':'none';
  if(visible){pm.style.left='52%';pm.style.top='48%';}
 }
}
const aotdRoomPromptUpdate=update;
update=function(dt){aotdRoomPromptUpdate(dt);aotdRoomProximityPrompt();};

const aotdOldGetObjectiveData=getObjectiveData;
getObjectiveData=function(){
 if(chapter==='ALCATRAZ')return[
  {t:'FIND THE DOCKS',d:0},
  {t:'ESCAPE THE ISLAND',d:1},
  {t:'FIND 2 SURVIVORS',d:2}
 ];
 return[{t:'FIND 2 SURVIVORS',d:0}];
};
const aotdOldJamSimpleGoalData=jamSimpleGoalData;
jamSimpleGoalData=function(){
 if(chapter==='ALCATRAZ')return[
  {t:'FIND THE DOCKS',steps:['Leave Cell A-17 and follow the prison signs.','Enter the Medical Wing and search the clearly marked supply desk for the Dock Pass.','Reach the ferry dock beacon.']},
  {t:'ESCAPE THE ISLAND',steps:['Use the Dock Pass at the ferry dock.','Light the beacon and wait for the ferry.','Walk to the ferry ladder and press E to board.']}
 ];
 return[{t:'FIND 2 SURVIVORS',steps:['Explore the city streets.','Approach a survivor and press E.','Repeat until two survivors are found.']}];
};
jamRenderSimpleObjectives();


const aotdMedicalMarker=document.createElement('div');
aotdMedicalMarker.id='medicalPassMarker';
aotdMedicalMarker.className='medicalPassMarker';
aotdMedicalMarker.textContent='DOCK PASS • SUPPLY DESK • PRESS E';
aotdUpgradeRoot.appendChild(aotdMedicalMarker);
const aotdControlFix=document.createElement('div');
aotdControlFix.className='controlChoiceFix hidden';
aotdControlFix.innerHTML='<div class="controlChoiceBox"><h2>CONTROL MODE</h2><p>Choose exactly how you want to play. The selected mode stays active until you change it here again.</p><div class="controlChoiceGrid"><button id="chooseLaptop">LAPTOP / DESKTOP<small>A / D or ARROWS • W / SPACE • MOUSE • KEYBOARD</small></button><button id="chooseMobile">MOBILE / TOUCH<small>VIRTUAL MOVE + ACTION BUTTONS • TOUCH AIM</small></button></div><div class="controlChoiceFoot">You can change this any time from the menu.</div></div>';
aotdUpgradeRoot.appendChild(aotdControlFix);
function aotdOpenControlChoice(){
 aotdControlFix.classList.remove('hidden');
 aotdControlFix.style.display='grid';
 const l=document.getElementById('chooseLaptop');const m=document.getElementById('chooseMobile');
 if(l)l.classList.toggle('selected',controlMode==='laptop');
 if(m)m.classList.toggle('selected',controlMode==='mobile');
}
function aotdCloseControlChoice(){aotdControlFix.classList.add('hidden');aotdControlFix.style.display='none';}
function aotdChooseMode(v){setControlMode(v);aotdCloseControlChoice();setMsg(v==='mobile'?'MOBILE MODE ENABLED.':'LAPTOP MODE ENABLED.',1.5);}
document.getElementById('chooseLaptop').onclick=()=>aotdChooseMode('laptop');
document.getElementById('chooseMobile').onclick=()=>aotdChooseMode('mobile');
document.getElementById('mainMenuControls').onclick=aotdOpenControlChoice;
document.getElementById('controlModeOpen').onclick=aotdOpenControlChoice;

const aotdOldDrawCharacter=drawCharacterSprite;
function aotdPremiumCharacter(x,y,who,dir,anim,role){
 const facing=dir||1;
 const t=anim||0;
 const isPlayer=!role||role==='player';
 const moving=isPlayer?(mode==='play'&&Math.abs(player.vx)>28):true;
 const cycle=moving?Math.sin(t*1.45):Math.sin(t*.7);
 const cycle2=-cycle;
 const breathe=Math.sin(totalTime*2.1+(x%47)*.07)*.8;
 const idleShift=Math.sin(t*.5+(x%31)*.04)*.45;
 const jump=isPlayer&&mode==='play'&&!player.onGround;
 const fall=jump&&player.vy>180;
 const skin=who==='Yumi'?'#d9b79c':who==='May'?'#d7b89f':'#d2b399';
 const hair=who==='Yumi'?'#16181a':who==='May'?'#3d2926':'#2b2221';
 const hairHi=who==='Yumi'?'#3d4442':who==='May'?'#6a483d':'#65483e';
 const coat=who==='Yumi'?'#31524a':who==='May'?'#4a5062':'#355459';
 const coatHi=who==='Yumi'?'#648176':who==='May'?'#737b8c':'#5d777b';
 const shirt='#e8dfd0';
 const pants=who==='Yumi'?'#222b2c':who==='May'?'#282b32':'#252c2e';
 const boot='#090c0e';
 const gold='#ddbf70';
 const scarf=who==='Yumi'?'#78978d':who==='May'?'#737c8d':'#708488';
 const legLift=jump?(fall?2:4):0;
 const armSwing=moving?cycle*2.5:idleShift;
 const legA=moving?cycle*4.2:idleShift;
 const legB=moving?cycle2*4.2:-idleShift;
 ctx.save();
 ctx.translate(Math.round(x),Math.round(y-(fall?1:0)));
 ctx.scale(facing,1);
 const shadow=ctx.createRadialGradient(0,75,2,0,75,31);
 shadow.addColorStop(0,'rgba(0,0,0,.48)');
 shadow.addColorStop(1,'rgba(0,0,0,0)');
 ctx.fillStyle=shadow;ctx.fillRect(-38,59,76,24);
 px(-15+legA,48+legLift,12,23,pants);
 px(5+legB,48+legLift,12,23,pants);
 px(-19+legA,69+legLift,18,7,boot);
 px(1+legB,69+legLift,18,7,boot);
 px(-21,20+breathe,42,32,coat);
 px(-13,18+breathe,30,16,shirt);
 px(-3,19+breathe,10,16,scarf);
 px(-26+armSwing*.3,23+breathe,10,27,coatHi);
 px(30-armSwing*.3,23+breathe,10,27,coatHi);
 px(-27+armSwing*.35,48,15,8,coat);
 px(29-armSwing*.35,48,15,8,coat);
 px(-10,0+breathe,30,28,skin);
 px(-16,-10+breathe,42,13,hair);
 px(-13,-18+breathe,35,8,hairHi);
 if(who==='Yumi'){
  px(-22,-3+breathe,10,34,hairHi);
  px(23,-3+breathe,12,35,hairHi);
  px(-18,7+breathe,9,24,hair);
  px(27,8+breathe,8,25,hair);
  px(-7,-21+breathe,28,7,hair);
  px(11,-16+breathe,13,9,hairHi);
  px(-4,-11+breathe,23,4,hairHi);
 }
 if(who==='May'){
  px(-21,-3+breathe,9,30,hairHi);
  px(23,-4+breathe,11,27,hairHi);
  px(28,6+breathe,8,20,hairHi);
  px(-25,7+breathe,7,18,hairHi);
 }
 if(who==='Julia'){
  px(16,-8+breathe,14,23,hairHi);
  px(25,1+breathe,9,24,hairHi);
  px(-22,2+breathe,8,19,hairHi);
 }
 px(-2,7+breathe,4,4,'#141719');
 px(14,7+breathe,4,4,'#141719');
 px(3,16+breathe,14,3,'#a1635a');
 px(-8,31+breathe,8,14,coatHi);
 px(13,31+breathe,8,14,coatHi);
 px(-10,25,7,8,gold);
 px(-8,26,3,3,'#fff2a8');
 px(-4,44+breathe,22,5,coat);
 px(-10,52,7,7,scarf);
 px(19,52,8,7,scarf);
 px(-19+armSwing*.18,37,5,12,skin);
 px(27-armSwing*.18,37,5,12,skin);
 if(jump){
  px(-22,43+legLift,9,5,coatHi);
  px(26,43+legLift,9,5,coatHi);
 }
 if(role==='Nurse'){
  px(-8,30,31,6,'#7e8d86');px(2,31,5,18,'#f4efe5');px(0,37,11,5,'#f4efe5');
 }
 if(role==='Soldier'){
  px(-18,-6,41,8,'#414e45');px(-7,-11,24,5,'#2b352f');
 }
 if(role==='Mechanic'){
  px(-12,20,36,7,'#664b3c');px(27,34,8,15,'#96725a');
 }
 ctx.restore();
}
const aotdOldCharacterFinal=drawCharacterSprite;
drawCharacterSprite=aotdPremiumCharacter;
const aotdOldEnhancedPlayerFinal=drawEnhancedPlayer;
drawEnhancedPlayer=function(){aotdOldEnhancedPlayerFinal();if(mode==='play'){const x=player.x-camera;const y=player.y;const moving=Math.abs(player.vx)>65;if(moving&&player.onGround){ctx.save();ctx.globalAlpha=.18;for(let i=0;i<3;i++){const ghost=x-player.facing*(i+1)*9;drawCharacterSprite(ghost+8,y,selectedCharacter,player.facing,player.anim-(i+1)*.32,'ghost');}ctx.restore();}}};
function aotdDetailMap(){aotdMapArt();aotdMapForeground();}
const aotdMapDrawBase=draw;
draw=function(){aotdMapDrawBase();if(mode==='play'&&interior){ctx.save();ctx.globalAlpha=.12;for(let i=0;i<16;i++){const xx=20+i*83;const yy=90+(i%6)*64;px(xx,yy,36,3,'#4e5451');if(i%2===0)px(xx+10,yy+4,14,18,'#181d1d');}ctx.restore();}};
function aotdWorldLabel(){const el=document.getElementById('aotdWorldLabel');if(!el)return;if(mode!=='play'){el.textContent='';return;}if(interior)el.textContent=interior.building.name+'  //  '+(floor===1?'GROUND FLOOR':'UPPER FLOOR');else if(chapter==='ALCATRAZ')el.textContent='ALCATRAZ ISLAND  //  CELL BLOCK A → MEDICAL WING → DOCKS';else el.textContent='SAN FRANCISCO  //  FIND THE SURVIVORS';}
const aotdLabelUpdateBase=update;
update=function(dt){aotdLabelUpdateBase(dt);aotdWorldLabel();};

function aotdReadableText(text,x,y,size=12,color='#f1ead8'){
 ctx.save();
 ctx.font='700 '+size+'px Consolas';
 ctx.textAlign='center';
 ctx.textBaseline='middle';
 ctx.lineJoin='round';
 ctx.lineWidth=4;
 ctx.strokeStyle='rgba(0,0,0,.92)';
 ctx.strokeText(text,x,y);
 ctx.fillStyle=color;
 ctx.fillText(text,x,y);
 ctx.restore();
}
function aotdCharacterLabel(x,y,text,accent='#d8c68f'){
 const w=Math.max(72,text.length*7.2+22);
 const h=22;
 ctx.save();
 ctx.globalAlpha=.94;
 ctx.fillStyle='rgba(5,7,7,.86)';
 ctx.fillRect(x-w/2,y-h/2,w,h);
 ctx.strokeStyle='rgba(218,209,184,.5)';
 ctx.lineWidth=1;
 ctx.strokeRect(x-w/2+.5,y-h/2+.5,w-1,h-1);
 aotdReadableText(text,x,y,11,accent);
 ctx.restore();
}
function aotdInteriorVisualFix(){
 if(mode!=='play'||!interior)return;
 ctx.save();
 const fixtures=[150,355,560,765,970];
 for(const x of fixtures){
  px(x,152,82,48,'#1b2324');
  px(x+4,156,74,40,'#3b4342');
  px(x+9,163,64,25,'#101718');
  px(x+13,167,56,5,'#85877d');
  px(x+18,178,46,6,'#273131');
  px(x+28,192,27,4,'#b0a77b');
  px(x+1,199,80,3,'#121719');
 }
 px(38,395,235,120,'#202627');
 px(45,380,220,12,'#4a4c48');
 px(52,392,205,17,'#333938');
 px(52,411,205,71,'#171d1e');
 px(65,423,50,40,'#252d2d');
 px(123,423,50,40,'#202727');
 px(181,423,51,40,'#272d2d');
 px(58,484,18,28,'#121718');
 px(205,484,18,28,'#121718');
 px(86,338,88,6,'#4f5552');
 px(91,347,78,22,'#222829');
 px(98,352,29,9,'#8d8160');
 px(136,352,27,9,'#6f746c');
 px(770,407,190,108,'#3a342e');
 px(779,398,172,16,'#51483e');
 px(786,420,158,78,'#2b2b2a');
 px(792,430,67,57,'#202526');
 px(866,430,67,57,'#242a2a');
 px(804,446,42,4,'#766d5a');
 px(878,446,42,4,'#766d5a');
 px(804,468,42,4,'#515753');
 px(878,468,42,4,'#515753');
 px(1048,361,105,154,'#232a2a');
 px(1055,368,91,141,'#151b1c');
 for(let i=0;i<5;i++){
  const yy=376+i*26;
  px(1058,yy,86,5,'#646963');
  px(1068,yy+7,23,11,i%2?'#4b4d49':'#765f47');
  px(1100,yy+7,31,11,'#2c3332');
 }
 px(534,365,152,150,'#202728');
 px(542,375,136,140,'#303738');
 px(551,384,118,131,'#1b2223');
 px(659,425,8,8,'#b69f65');
 px(536,355,148,6,'#69716d');
 px(84,321,92,44,'#202729');
 px(89,326,82,8,'#505753');
 px(96,338,68,20,'#1a2021');
 px(101,342,58,4,'#7a6e54');
 aotdReadableText(interior.building.name.toUpperCase(),W/2,104,16,'#f0d8b4');
 aotdReadableText('FLOOR '+floor,W/2,127,10,'#c9d0ca');
 ctx.restore();
}
function aotdReadableCharacterNames(){
 if(mode!=='play')return;
 const pxpos=player.x-camera;
 const pyy=player.y-24;
 aotdCharacterLabel(pxpos,pyy,selectedCharacter.toUpperCase());
 if(chapter==='SAN FRANCISCO'){
  for(const s of survivors){
   if(s.found)continue;
   const sx=s.x-camera;
   if(sx<-70||sx>W+70)continue;
   aotdCharacterLabel(sx,GROUND-108,s.name.toUpperCase(),'#d5cdbb');
  }
 }
}
const aotdLastDrawForReadableFix=draw;
draw=function(){
 if(mode==='play'&&interior){
  aotdLastDrawForReadableFix();
  aotdInteriorVisualFix();
  aotdReadableCharacterNames();
  return;
 }
 aotdLastDrawForReadableFix();
 aotdReadableCharacterNames();
};


function aotdCharacterSpriteV3(x,y,who,dir,anim,role){
 const d=dir||1,t=anim||0,moving=mode==='play'&&Math.abs(player.vx)>26;const walk=moving?Math.sin(t*1.15):Math.sin(totalTime*1.2)*.2;const walk2=-walk;const breathe=Math.sin(totalTime*2.05+x*.013)*.7;const coatSwing=moving?Math.sin(t*.8)*1.4:Math.sin(totalTime*1.1+x*.01)*.45;const jump=mode==='play'&&!player.onGround;const skin=who==='Yumi'?'#d7b99f':who==='May'?'#d9b9a1':'#d4b49d';const hair=who==='Yumi'?'#121415':who==='May'?'#4d3028':'#2f2424';const hairHi=who==='Yumi'?'#39413e':who==='May'?'#76513d':'#63453b';const coat=who==='Yumi'?'#315047':who==='May'?'#4b5061':'#355154';const coatHi=who==='Yumi'?'#628075':who==='May'?'#73798a':'#5e777a';const shirt='#e7ded0',pants=who==='Yumi'?'#242c2e':who==='May'?'#272a31':'#252b2d',boot='#0a0e10',gold='#d9bd70',scarf=who==='Yumi'?'#769088':who==='May'?'#737c8c':'#708080';
 ctx.save();ctx.translate(Math.round(x),Math.round(y));ctx.scale(d,1);
 const shadow=ctx.createRadialGradient(0,74,1,0,74,30);shadow.addColorStop(0,'rgba(0,0,0,.5)');shadow.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=shadow;ctx.fillRect(-38,56,76,26);
 const legLift=jump?3:0;px(-15+walk2*3,46+legLift,12,24,pants);px(4+walk*3,46+legLift,12,24,pants);px(-20+walk2*3,68+legLift,18,7,boot);px(0+walk*3,68+legLift,18,7,boot);
 px(-19,22+breathe,38,31,coat);px(-13,19+breathe,27,17,shirt);px(-3,21+breathe,9,14,scarf);px(-17+walk*.55,25+coatSwing,9,26,coatHi);px(28+walk2*.55,25-coatSwing,9,26,coatHi);px(-22+walk*.7,48,14,9,coat);px(28+walk2*.7,48,14,9,coat);
 px(-10,0+breathe,29,28,skin);px(-15,-9+breathe,40,13,hair);px(-11,-16+breathe,32,8,hairHi);
 if(who==='Yumi'){
  px(-22,-3+breathe,10,32,hairHi);px(23,-2+breathe,11,34,hairHi);px(-17,6+breathe,8,25,hair);px(26,8+breathe,7,23,hair);px(-5,-19+breathe,22,6,hair);px(11,-15+breathe,12,7,hairHi);px(-2,-3+breathe,20,3,hairHi);
 }
 if(who==='May'){
  px(-20,-3+breathe,9,29,hairHi);px(23,-2+breathe,10,24,hairHi);px(27,6+breathe,7,19,hairHi);px(-24,7+breathe,7,18,hairHi);
 }
 if(who==='Julia'){
  px(15,-7+breathe,14,21,hairHi);px(24,0+breathe,9,24,hairHi);px(-22,1+breathe,8,18,hairHi);
 }
 px(-2,7+breathe,4,3,'#151718');px(14,7+breathe,4,3,'#151718');px(-1,5+breathe,3,2,'#f0e4d5');px(13,5+breathe,3,2,'#f0e4d5');px(3,16+breathe,13,3,'#9c6159');
 px(-9,30+breathe,8,15,coatHi);px(13,30+breathe,8,15,coatHi);px(-10,25,7,8,gold);px(-8,26,3,3,'#fff3af');px(-4,45+breathe,19,5,coat);px(-9,52,7,7,scarf);px(18,52,8,7,scarf);
 px(-18,37,5,12,skin);px(26,37,5,12,skin);
 if(jump){px(-22,43+legLift,8,5,coatHi);px(26,43+legLift,8,5,coatHi);}
 if(role==='Nurse'){px(-7,30,31,6,'#8b958f');px(2,31,5,18,'#f5f1e8');px(0,37,10,5,'#f5f1e8');}
 if(role==='Soldier'){px(-18,-6,41,8,'#425248');px(-7,-11,24,5,'#2b362f');}
 if(role==='Mechanic'){px(-11,20,35,7,'#674c3b');px(28,34,8,15,'#99765c');}
 ctx.restore();
}
drawCharacterSprite=aotdCharacterSpriteV3;

function aotdBuildCharacterCards(){
 const cards=document.querySelectorAll('.charCard');
 cards.forEach(card=>{
  const who=card.dataset.char;if(!who||card.querySelector('.charMeta'))return;
  const existing=card.innerHTML;card.innerHTML='';
  const title=document.createElement('span');title.className='charName';title.textContent=who.toUpperCase();
  const desc=document.createElement('span');desc.className='charMeta';desc.textContent=who==='Yumi'?'FEMALE DETECTIVE • INTELLIGENCE • CALM UNDER PRESSURE':who==='May'?'FEMALE DETECTIVE • CRIME SCENE • OBSERVANT':'FEMALE DETECTIVE • FIELD FILES • DETERMINED';
  card.appendChild(title);card.appendChild(desc);
  card.setAttribute('aria-label',who+' — '+desc.textContent);
 });
}
aotdBuildCharacterCards();
function aotdCharacterCardCss(){
 const s=document.createElement('style');s.textContent='.charCard .charName{display:block;position:relative;z-index:3;color:#fff7e8!important;font:800 22px Consolas,monospace!important;letter-spacing:4px;text-shadow:3px 3px #000,0 0 7px #000!important;margin-top:auto}.charCard .charMeta{display:block;position:relative;z-index:3;color:#ddd6c8!important;font:700 10px Consolas,monospace!important;letter-spacing:1px;text-shadow:2px 2px #000,0 0 5px #000!important;line-height:1.4;margin-top:5px}.charCard[data-char="Yumi"] .charName{color:#e7f0e8!important}.charCard:focus-visible{outline:2px solid #e8d9ad;outline-offset:2px}';document.head.appendChild(s);
}
aotdCharacterCardCss();

function aotdSafeMapLayer(){
 if(mode!=='play'||interior)return;
 const sf=chapter==='SAN FRANCISCO';
 ctx.save();
 ctx.globalAlpha=.92;
 for(let i=0;i<12;i++){
  const x=i*132-(camera*.10%132);const h=70+(i%5)*24;const top=GROUND-230-h;
  px(x,top,84,h,'#111619');px(x+7,top+9,70,5,'#242a2b');
  for(let q=0;q<4;q++){if((i+q)%3!==1)px(x+12+(q%2)*34,top+25+q*27,18,15,(sf&&(q+i)%4===0)?'#5b5546':'#202628');}
  px(x+8,top+h-8,68,8,'#181d1e');
 }
 for(let i=0;i<22;i++){
  const x=(i*79-camera*.35)%W;const y=GROUND-18-(i%4)*5;
  px(x,y,7+(i%5)*3,2,i%4===0?'#64665f':'#353a38');
 }
 if(sf){
  for(let i=0;i<6;i++){const x=110+i*230-(camera*.22%230);px(x,GROUND-188-(i%2)*22,3,150,'#252b2e');px(x-10,GROUND-190-(i%2)*22,23,4,'#343a3b');}
 }else{
  for(let i=0;i<5;i++){const x=120+i*250-(camera*.15%250);px(x,GROUND-164-(i%2)*18,3,124,'#2c3232');px(x-9,GROUND-166-(i%2)*18,21,4,'#3a403e');}
 }
 ctx.restore();
}
aotdMapArt=aotdSafeMapLayer;
function aotdSafeMapForeground(){
 if(mode!=='play'||interior)return;
 ctx.save();
 for(let i=0;i<30;i++){
  const x=(i*113-camera*.55)%W;const y=GROUND-3-(i%6)*7;
  px(x,y,2+(i%4),2,i%5===0?'#76766d':'#454844');
  if(i%6===0){px(x+7,y-6,2,6,'#262a29');px(x+5,y-8,6,2,'#55574f');}
 }
 ctx.restore();
}
aotdMapForeground=aotdSafeMapForeground;

function aotdFixDrawPipeline(){
 const base=draw;
 draw=function(){base();if(mode==='play'){aotdReadableCharacterNames();}};
}
aotdFixDrawPipeline();

function aotdVisibleDistantSky(){
 const sf=chapter==='SAN FRANCISCO';
 const g=ctx.createLinearGradient(0,0,0,GROUND);
 g.addColorStop(0,sf?'#091019':'#0a1117');
 g.addColorStop(.42,sf?'#17252d':'#1a272d');
 g.addColorStop(1,sf?'#293436':'#273236');
 ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 for(let i=0;i<18;i++){
  const x=(i*137-camera*.08)%W;
  const h=70+(i%6)*19;
  const y=GROUND-145-h;
  px(x,y,92+(i%4)*12,h,sf?(i%2?'#172127':'#1b2529'):(i%2?'#1a2529':'#1d292c'));
  px(x+8,y+10,72+(i%3)*8,5,'#344247');
  for(let q=0;q<3;q++){
   const lit=(i+q)%4===0;
   px(x+14+q*24,y+28,12,18,lit?'#6b634f':'#273236');
   if(lit)px(x+17+q*24,y+32,5,8,'#a08c5d');
  }
 }
 if(sf){
  px(0,GROUND-132,W,7,'#394446');
  for(let i=0;i<9;i++){
   const x=i*164-camera*.14;
   line(x,GROUND-126,x+35,GROUND-182,'#596467',3);
   line(x+35,GROUND-182,x+70,GROUND-126,'#485255',3);
  }
 }
 if(chapter==='ALCATRAZ'){
  ctx.save();ctx.globalAlpha=.7;px(0,GROUND-118,W,118,'#1a2428');ctx.restore();
  for(let i=0;i<7;i++){
   const x=70+i*210-camera*.12;
   px(x,GROUND-168,108,168,'#283236');
   px(x+12,GROUND-154,84,8,'#434b4c');
   for(let q=0;q<5;q++)px(x+18+q*15,GROUND-128,5,64,'#11191b');
  }
 }
}
function aotdVisibleGround(){
 const g=ctx.createLinearGradient(0,GROUND-4,0,H);
 g.addColorStop(0,'#343b39');g.addColorStop(.2,'#252c2c');g.addColorStop(1,'#13191a');
 ctx.fillStyle=g;ctx.fillRect(0,GROUND,W,H-GROUND);
 ctx.fillStyle='#46504e';ctx.fillRect(0,GROUND-8,W,8);
 for(let i=0;i<54;i++){
  const x=(i*83-camera*.92)%W;
  const y=GROUND+14+(i%10)*14;
  if(i%5===0){px(x,y,24,3,'#59605b');px(x+5,y+5,9,2,'#252b29');}
  else if(i%3===0){px(x,y,5+(i%4),3,'#666960');px(x+8,y+2,3,2,'#414742');}
  else{px(x,y,2+(i%3),2,'#525754');}
 }
 if(chapter==='SAN FRANCISCO'){
  ctx.fillStyle='#39403f';ctx.fillRect(0,GROUND+39,W,76);
  for(let x=-20;x<W+160;x+=155)px(x,GROUND+68,72,4,'#7a7970');
 }else{
  ctx.fillStyle='#2d3534';ctx.fillRect(0,GROUND+45,W,95);
  for(let i=0;i<11;i++){
   const x=i*132-camera*.42;
   px(x,GROUND+62,68,7,'#4c514c');
   px(x+8,GROUND+77,42,3,'#1f2625');
  }
 }
}
function aotdVisibleStructures(){
 for(const b of buildings){
  const x=b.x-camera;
  if(x<-b.w-80||x>W+80)continue;
  const h=b.type==='prison'?250:b.floors*105+82;
  const main=b.type==='hospital'?'#354044':b.type==='police'?'#334047':b.type==='prison'?'#3a4142':'#343b3d';
  const trim=b.type==='hospital'?'#697476':b.type==='police'?'#626c70':'#666c69';
  const shadow='#20282a';
  px(x,GROUND-h,b.w,h,main);
  px(x,GROUND-h,b.w,9,trim);
  px(x+10,GROUND-h+11,b.w-20,8,shadow);
  for(let f=0;f<b.floors;f++){
   const fy=GROUND-74-f*105;
   px(x+17,fy,b.w-34,5,'#555e5e');
   const cols=Math.max(2,Math.floor((b.w-56)/46));
   for(let q=0;q<cols;q++){
    const wx=x+25+q*46;
    const lit=(q+f+Math.floor(b.x/100))%6===0;
    px(wx,fy-31,24,24,lit?'#6b604d':'#1b2427');
    px(wx+3,fy-28,18,18,lit?'#8d7a52':'#263236');
    if(lit){px(wx+7,fy-24,4,7,'#b29a65');px(wx+14,fy-24,4,7,'#927d54');}
   }
  }
  const door=b.x+b.w*.5-camera;
  px(door-30,GROUND-73,60,73,'#11181a');
  px(door-24,GROUND-66,48,66,'#253033');
  px(door+17,GROUND-43,5,5,'#b19c68');
  if(b.type==='police'){px(x+18,GROUND-h+17,b.w-36,23,'#20292c');aotdReadableText('POLICE',x+30,GROUND-h+31,13,'#ddd8c8');}
  if(b.type==='hospital'){px(x+b.w/2-62,GROUND-h+18,124,34,'#526064');px(x+b.w/2-8,GROUND-h+23,16,23,'#d8dbd5');px(x+b.w/2-20,GROUND-h+31,40,8,'#d8dbd5');}
  if(b.type==='funeral'){px(x+22,GROUND-h+18,b.w-44,25,'#242b2d');aotdReadableText('MERCY FUNERAL',x+105,GROUND-h+31,11,'#c2c5c0');}
  if(b.type==='research'){px(x+b.w/2-96,GROUND-h+16,192,27,'#1b2527');aotdReadableText('ECLIPSE RESEARCH',x+b.w/2,GROUND-h+29,10,'#c7cec8');}
 }
}
function aotdVisibleExteriorScene(){
 aotdVisibleDistantSky();
 aotdVisibleGround();
 aotdVisibleStructures();
 if(chapter==='SAN FRANCISCO')drawSFStreetProps();else drawAlcatrazProps();
 drawStreetDebris();
 if(chapter==='ALCATRAZ'){drawCellBlockAExterior();drawStartingCell();}
 drawEnhancedBloodWriting();
 drawEnhancedChests();
 drawEnhancedLoot();
 drawEnhancedSurvivors();
 drawEnhancedZombies();
 for(const b of bullets){const x=b.x-camera;if(x>-25&&x<W+25){px(x-4,b.y-2,8,4,'#e9d99c');px(x+2,b.y-1,5,2,'#fff6c9');}}
 drawEnhancedPlayer();
 drawEnhancedSmiler();
 if(typeof finalDrawBuildingDetails==='function')finalDrawBuildingDetails();
 if(typeof finalDrawIslandDock==='function')finalDrawIslandDock();
 if(typeof drawFinalBoat==='function')drawFinalBoat();
 drawParticles();
 drawLighting();
 drawEnhancedWeather();
}
function aotdVisibleInteriorScene(){
 const b=interior.building;
 const wall=ctx.createLinearGradient(0,50,0,530);
 wall.addColorStop(0,b.type==='prison'?'#394344':'#303b3d');
 wall.addColorStop(.48,'#252e30');
 wall.addColorStop(1,'#151d1f');
 ctx.fillStyle=wall;ctx.fillRect(0,0,W,H);
 px(0,64,W,8,'#67706d');
 for(let row=0;row<8;row++){
  const y=94+row*52;
  for(let col=-1;col<18;col++){
   const x=col*76+(row%2)*38;
   line(x,y,x+49,y,'#46504e',1);
   px(x+2,y+4,2,10,'#252d2d');
  }
 }
 px(0,530,W,190,'#11191a');
 for(let i=0;i<19;i++){const x=i*68;px(x,539,50,4,'#3e4745');px(x+8,546,2,126,'#202727');}
 const doorX=610;
 px(doorX-65,360,130,154,'#101719');
 px(doorX-55,374,110,140,'#2c3739');
 px(doorX+35,431,5,5,'#c0a768');
 px(doorX-71,347,142,3,'#aaa27f');
 px(52,392,214,122,'#202a2b');
 px(43,370,232,23,'#4b5351');
 px(83,334,99,34,'#11181a');
 px(778,405,192,109,'#443a31');
 px(790,378,168,27,'#2b3536');
 px(807,387,20,9,'#766b53');
 px(1050,360,104,154,'#202a2b');
 for(let i=0;i<5;i++){px(1057,374+i*27,88,5,'#727873');}
 for(let i=0;i<5;i++){
  const x=132+i*205;
  px(x,145,88,46,'#1b2426');
  px(x+8,153,72,6,'#66706b');
  px(x+17,167,54,13,'#303b3c');
  if(i%2===0)px(x+36,185,10,6,'#90774f');
 }
 if(floor>=2){px(388,156,118,240,'#1b2426');px(522,156,12,240,'#3a4443');for(let i=0;i<6;i++)line(401+i*20,388,442+i*20,174,'#59615e',3);}
 ctx.font='700 16px Consolas';ctx.fillStyle='#d0c5ac';ctx.strokeStyle='#000';ctx.lineWidth=3;ctx.strokeText(b.name.toUpperCase(),255,104);ctx.fillText(b.name.toUpperCase(),255,104);
 ctx.font='11px Consolas';ctx.fillStyle='#b5beb8';ctx.fillText(`FLOOR ${floor} • INTERIOR`,500,126);
 drawInteriorLoot();
 drawEnhancedInteriorPlayer();
 drawParticles();
}
function aotdFinalVisibleDraw(){
 if(mode!=='play')return;
 ctx.save();
 ctx.setTransform(1,0,0,1,0,0);
 ctx.globalAlpha=1;
 ctx.globalCompositeOperation='source-over';
 ctx.filter='none';
 ctx.shadowBlur=0;
 ctx.shadowColor='transparent';
 ctx.clearRect(0,0,W,H);
 const sx=shake?(Math.random()*shake-shake/2):0;
 ctx.translate(sx,0);
 let rendered=false;
 try{
  if(interior)aotdVisibleInteriorScene();else aotdVisibleExteriorScene();
  rendered=true;
 }catch(err){
  console.error('Ashes render recovered:',err);
  ctx.setTransform(1,0,0,1,0,0);
  ctx.globalAlpha=1;
  ctx.globalCompositeOperation='source-over';
  const g=ctx.createLinearGradient(0,0,0,GROUND);
  g.addColorStop(0,'#0b1820');g.addColorStop(.55,'#1b3033');g.addColorStop(1,'#344744');
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  ctx.fillStyle='#2c3735';ctx.fillRect(0,GROUND,W,H-GROUND);
  px(0,GROUND-160,W,160,'#1e292c');
  for(let i=0;i<7;i++){const bx=50+i*195-camera*.08;px(bx,GROUND-210,150,210,'#2d3a3d');px(bx+12,GROUND-194,126,8,'#58615e');for(let q=0;q<4;q++)px(bx+22+q*29,GROUND-160,15,28,'#151d1f');}
  if(chapter==='ALCATRAZ'){px(90,GROUND-260,300,260,'#3a4444');px(118,GROUND-230,244,10,'#59605d');for(let q=0;q<10;q++)px(132+q*23,GROUND-200,4,190,'#161b1c');}
  if(interior){px(0,0,W,H,'#101719');px(0,GROUND-80,W,80,'#2e3637');px(500,290,280,190,'#202729');px(555,320,170,150,'#4b4137');}
  drawCharacterSprite(player.x-camera+8,player.y,selectedCharacter,player.facing,player.anim,'');
  rendered=true;
 }
 if(!rendered){
  ctx.fillStyle='#172025';ctx.fillRect(0,0,W,H);
 }
 ctx.setTransform(1,0,0,1,0,0);
 if(ultimateScare&&ultimateScare.shadow>0){ctx.save();ctx.globalAlpha=Math.min(.18,ultimateScare.shadow*.08);const side=player.facing>0?W-105:105;px(side-18,210,36,210,'#050708');px(side-11,192,22,24,'#050708');ctx.restore();}
 if(flash>0){ctx.save();ctx.globalAlpha=Math.min(.22,flash*.18);ctx.fillStyle='#fff4dc';ctx.fillRect(0,0,W,H);ctx.restore();}
 if(state.sanity<45){ctx.save();ctx.globalAlpha=Math.min(.12,(45-state.sanity)/300);ctx.fillStyle='#3b0b18';ctx.fillRect(0,0,W,H);ctx.restore();}
 ctx.restore();
}
draw=aotdFinalVisibleDraw;

function aotdEmergencyScene(){
 ctx.save();
 ctx.setTransform(1,0,0,1,0,0);
 ctx.globalAlpha=1;
 ctx.globalCompositeOperation='source-over';
 ctx.filter='none';
 ctx.clearRect(0,0,W,H);
 const sf=chapter==='SAN FRANCISCO';
 const g=ctx.createLinearGradient(0,0,0,GROUND);
 g.addColorStop(0,sf?'#172631':'#16242a');
 g.addColorStop(.55,sf?'#26393b':'#28383a');
 g.addColorStop(1,sf?'#3a4744':'#3b4544');
 ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 ctx.fillStyle=sf?'#333a3a':'#303738';ctx.fillRect(0,GROUND,W,H-GROUND);
 ctx.fillStyle='#4b5350';ctx.fillRect(0,GROUND-7,W,7);
 for(let i=0;i<14;i++){
  const bx=((i*118)-(camera*.12))%W;
  const x=bx<0?bx+W:bx;
  const bh=100+(i%5)*28;
  px(x,GROUND-190-bh,90,bh,sf?(i%2?'#1a2429':'#1c292d'):'#202a2d');
  px(x+10,GROUND-180-bh,70,5,'#3a4548');
  for(let q=0;q<3;q++)px(x+16+q*23,GROUND-150-bh,14,18,(i+q)%5===0?'#776b4f':'#263235');
 }
 if(chapter==='ALCATRAZ'){
  px(70,GROUND-250,300,250,'#3d4646');
  px(94,GROUND-232,252,10,'#59605d');
  for(let i=0;i<12;i++)px(106+i*20,GROUND-218,4,190,'#171c1d');
 }
 for(let i=0;i<34;i++){
  const x=(i*97-camera*.72)%W;
  const y=GROUND+8+(i%8)*16;
  px(x<0?x+W:x,y,3+(i%4),2,i%3===0?'#656861':'#444846');
 }
 if(chapter==='SAN FRANCISCO'){
  ctx.fillStyle='#3d4140';ctx.fillRect(0,GROUND+40,W,76);
  for(let x=-30;x<W+120;x+=150)px(x,GROUND+68,72,4,'#77766c');
 }else{
  ctx.fillStyle='#2b3332';ctx.fillRect(0,GROUND+42,W,98);
  for(let x=-40;x<W+120;x+=132)px(x,GROUND+62,68,6,'#4b514d');
 }
 const px0=Number.isFinite(player.x)?player.x-camera:W*.5;
 const py0=Number.isFinite(player.y)?player.y:GROUND-70;
 ctx.save();
 ctx.globalAlpha=.48;
 ctx.fillStyle='#000';ctx.fillRect(px0-18,GROUND-4,54,8);
 ctx.restore();
 const body=selectedCharacter==='Yumi'?'#31524a':selectedCharacter==='May'?'#4a5062':'#355459';
 const skin='#d8b99f';
 const hair=selectedCharacter==='Yumi'?'#151719':selectedCharacter==='May'?'#4a3028':'#302424';
 const swing=(typeof player.anim==='number'?Math.sin(player.anim*1.35):0);
 px(px0-12+swing*3,py0+45,12,24,'#242b2d');
 px(px0+5-swing*3,py0+45,12,24,'#242b2d');
 px(px0-16+swing*3,py0+67,18,7,'#080c0e');
 px(px0+1-swing*3,py0+67,18,7,'#080c0e');
 px(px0-20,py0+20,40,32,body);
 px(px0-11,py0+18,27,15,'#e7dfd0');
 px(px0-9,py0+1,29,28,skin);
 px(px0-15,py0-9,40,13,hair);
 if(selectedCharacter==='Yumi'){
  px(px0-21,py0,10,35,'#3a4240');px(px0+22,py0,11,36,'#3a4240');
  px(px0-17,py0+8,8,23,'#17191a');px(px0+26,py0+8,8,24,'#17191a');
 }
 px(px0-2,py0+8,4,3,'#111');px(px0+13,py0+8,4,3,'#111');
 px(px0+1,py0+16,13,3,'#9a6259');
 px(px0-25+swing*2,py0+26,10,27,'#628075');
 px(px0+28-swing*2,py0+26,10,27,'#628075');
 px(px0-8,py0+31,8,14,'#e7dfd0');px(px0+14,py0+31,8,14,'#e7dfd0');
 px(px0-10,py0+24,6,8,'#ddbf70');
 ctx.restore();
}
function aotdSafeFallbackPhysics(dt){
 if(mode!=='play'||typeof player==='undefined')return;
 const left=inputState.left||keys.has('a')||keys.has('ArrowLeft');
 const right=inputState.right||keys.has('d')||keys.has('ArrowRight');
 const run=inputState.run||keys.has('Shift');
 const jump=inputState.jump||keys.has('w')||keys.has(' ')||keys.has('ArrowUp');
 const dir=(right?1:0)-(left?1:0);
 const speed=run?300:210;
 if(dir!==0){player.vx=dir*speed;player.facing=dir;}
 else player.vx*=Math.pow(.0001,dt);
 if(!Number.isFinite(player.vy))player.vy=0;
 if(!Number.isFinite(player.x))player.x=160;
 if(!Number.isFinite(player.y))player.y=GROUND-(player.h||70);
 if(jump&&player.onGround){player.vy=-470;player.onGround=false;inputState.jump=false;keys.delete('w');keys.delete(' ');keys.delete('ArrowUp');}
 player.vy+=1250*dt;
 player.x+=player.vx*dt;
 player.y+=player.vy*dt;
 if(player.y+(player.h||70)>=GROUND){player.y=GROUND-(player.h||70);player.vy=0;player.onGround=true;}
 const maxWorld=chapter==='ALCATRAZ'?ALCATRAZ_WIDTH:SF_WIDTH;
 player.x=Math.max(0,Math.min(maxWorld-(player.w||40),player.x));
 if(Number.isFinite(player.anim))player.anim+=Math.max(.5,Math.abs(player.vx)/120)*dt*5;
 const maxCam=Math.max(0,maxWorld-W);
 camera=Math.max(0,Math.min(maxCam,player.x-W*.38));
}
function aotdCompetitionRenderLoop(){
 requestAnimationFrame(aotdCompetitionRenderLoop);
 const now=performance.now();
 const dt=Math.min(.033,Math.max(.001,(now-last)/1000));
 last=now;
 if(mode==='play'){
  let failed=false;
  try{update(dt);}catch(err){failed=true;console.error('Ashes update recovered:',err);}
  if(failed)aotdSafeFallbackPhysics(dt);
  try{if(typeof setHud==='function')setHud();}catch(err){}
  try{draw();}catch(err){console.error('Ashes draw recovered:',err);aotdEmergencyScene();}
  try{
   const overlays=['mainMenu','menu','credits','cutscene','pause','ending','death','gadget','infoFlash','modePicker'];
   overlays.forEach(id=>{const el=document.getElementById(id);if(el)el.classList.add('hidden');});
   const hud=document.getElementById('hud');if(hud)hud.classList.remove('hidden');
  }catch(err){}
 }else{
  try{update(dt);}catch(err){console.error('Ashes menu update recovered:',err);}
  try{draw();}catch(err){console.error('Ashes menu draw recovered:',err);}
 }
 totalTime+=dt;
}
aotdCompetitionRenderLoop();

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
