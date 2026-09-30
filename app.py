from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Ashes of the Dead</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #080b09;
    font-family: Arial, sans-serif;
    color: white;
}

body {
    display: flex;
    justify-content: center;
    align-items: center;
}

#game {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #182018;
}

canvas {
    width: 100%;
    height: 100%;
    display: block;
    image-rendering: auto;
}

#hud {
    position: absolute;
    left: 20px;
    top: 20px;
    width: 290px;
    pointer-events: none;
    text-shadow: 2px 2px 3px #000;
}

.stat {
    margin-bottom: 8px;
}

.label {
    font-size: 13px;
    font-weight: bold;
    margin-bottom: 3px;
}

.bar {
    width: 260px;
    height: 16px;
    background: #171917;
    border: 2px solid #777;
    border-radius: 5px;
    overflow: hidden;
}

.fill {
    height: 100%;
    width: 100%;
}

#healthFill {
    background: #bd3737;
}

#staminaFill {
    background: #c8a936;
}

#xpFill {
    background: #5685c5;
}

#info {
    margin-top: 12px;
    font-size: 15px;
    line-height: 1.5;
}

#crosshair {
    position: absolute;
    width: 22px;
    height: 22px;
    pointer-events: none;
    transform: translate(-50%, -50%);
}

#crosshair::before,
#crosshair::after {
    content: "";
    position: absolute;
    background: white;
    box-shadow: 0 0 4px black;
}

#crosshair::before {
    width: 22px;
    height: 2px;
    top: 10px;
    left: 0;
}

#crosshair::after {
    width: 2px;
    height: 22px;
    left: 10px;
    top: 0;
}

#message {
    position: absolute;
    left: 50%;
    bottom: 45px;
    transform: translateX(-50%);
    min-width: 300px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    text-shadow: 2px 2px 4px #000;
}

#menu,
#gameOver,
#victory {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background:
        radial-gradient(circle at center, rgba(60,65,48,.65), rgba(0,0,0,.95));
    z-index: 20;
    text-align: center;
}

.hidden {
    display: none !important;
}

.title {
    font-size: clamp(45px, 8vw, 100px);
    letter-spacing: 5px;
    text-transform: uppercase;
    font-weight: 900;
    color: #d4c59a;
    text-shadow:
        4px 4px 0 #29251b,
        0 0 20px #000;
}

.subtitle {
    margin-top: 10px;
    color: #bbb8a7;
    font-size: 18px;
}

button {
    margin-top: 30px;
    padding: 15px 45px;
    border: 2px solid #b7aa7b;
    background: #282a23;
    color: white;
    font-size: 19px;
    cursor: pointer;
    border-radius: 5px;
}

button:hover {
    background: #494b3d;
}

.controls {
    margin-top: 25px;
    color: #aaa;
    line-height: 1.8;
}

#mobileControls {
    position: absolute;
    inset: 0;
    pointer-events: none;
}

.touch {
    position: absolute;
    width: 65px;
    height: 65px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,.35);
    background: rgba(0,0,0,.3);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    pointer-events: auto;
    user-select: none;
}

#left {
    left: 25px;
    bottom: 30px;
}

#right {
    left: 105px;
    bottom: 30px;
}

#jump {
    right: 170px;
    bottom: 30px;
}

#shoot {
    right: 90px;
    bottom: 30px;
}

#grenade {
    right: 10px;
    bottom: 105px;
}

#reload {
    right: 10px;
    bottom: 30px;
}

@media (min-width: 900px) {
    #mobileControls {
        display: none;
    }
}
</style>
</head>

<body>

<div id="game">

<canvas id="canvas"></canvas>

<div id="hud">

    <div class="stat">
        <div class="label">HEALTH</div>
        <div class="bar">
            <div id="healthFill" class="fill"></div>
        </div>
    </div>

    <div class="stat">
        <div class="label">STAMINA</div>
        <div class="bar">
            <div id="staminaFill" class="fill"></div>
        </div>
    </div>

    <div class="stat">
        <div class="label">XP</div>
        <div class="bar">
            <div id="xpFill" class="fill"></div>
        </div>
    </div>

    <div id="info"></div>

</div>

<div id="crosshair"></div>
<div id="message"></div>

<div id="menu">

    <div class="title">Ashes of the Dead</div>

    <div class="subtitle">
        WWII • ZOMBIE SURVIVAL
    </div>

    <button id="startButton">
        START GAME
    </button>

    <div class="controls">
        A / D — Move<br>
        W / SPACE — Jump<br>
        Mouse — Aim<br>
        Left Click — Shoot<br>
        R — Reload<br>
        G — Grenade<br>
        E — Search Chest<br>
        SHIFT — Sprint
    </div>

</div>

<div id="gameOver" class="hidden">

    <div class="title">YOU DIED</div>

    <div class="subtitle" id="deathText"></div>

    <button onclick="restartGame()">
        TRY AGAIN
    </button>

</div>

<div id="victory" class="hidden">

    <div class="title">VICTORY</div>

    <div class="subtitle">
        The Warden has been defeated.
    </div>

    <button onclick="restartGame()">
        PLAY AGAIN
    </button>

</div>

<div id="mobileControls">

    <div class="touch" id="left">◀</div>
    <div class="touch" id="right">▶</div>
    <div class="touch" id="jump">JUMP</div>
    <div class="touch" id="shoot">FIRE</div>
    <div class="touch" id="grenade">G</div>
    <div class="touch" id="reload">R</div>

</div>

</div>

<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let W = 1280;
let H = 720;

function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
}

window.addEventListener("resize", resize);
resize();

const keys = {};

window.addEventListener("keydown", e => {
    keys[e.code] = true;

    if (e.code === "KeyR") reload();
    if (e.code === "KeyG") grenade();
    if (e.code === "KeyE") interact();
});

window.addEventListener("keyup", e => {
    keys[e.code] = false;
});

const mouse = {
    x: W / 2,
    y: H / 2,
    down: false
};

canvas.addEventListener("mousemove", e => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;

    updateCrosshair();
});

canvas.addEventListener("mousedown", e => {
    if (e.button === 0) mouse.down = true;
});

window.addEventListener("mouseup", e => {
    if (e.button === 0) mouse.down = false;
});

function updateCrosshair() {
    const c = document.getElementById("crosshair");
    c.style.left = mouse.x + "px";
    c.style.top = mouse.y + "px";
}

updateCrosshair();

const WORLD_WIDTH = 18000;
const GROUND = 560;

let gameRunning = false;
let gameTime = 0;
let cameraX = 0;
let wave = 1;
let zombiesKilled = 0;
let screenShake = 0;

let message = "";
let messageTimer = 0;

const player = {
    x: 500,
    y: 400,
    w: 44,
    h: 100,

    vx: 0,
    vy: 0,

    speed: 260,
    sprintSpeed: 390,
    jump: -620,

    health: 100,
    maxHealth: 100,

    stamina: 100,
    maxStamina: 100,

    hunger: 100,

    level: 1,
    xp: 0,
    nextXP: 250,

    ammo: 8,
    magazine: 8,

    reserveAmmo: 80,

    grenades: 3,

    fireCooldown: 0,
    reloadTimer: 0,

    invincible: 0,

    facing: 1,

    weapon: "M1935 Pistol",

    score: 0
};

const zombies = [];
const bullets = [];
const grenades = [];
const particles = [];
const chests = [];
const crates = [];
const wrecks = [];

let boss = null;

const zones = [
    { start: 0, end: 3000, name: "ABANDONED ASYLUM" },
    { start: 3000, end: 6500, name: "WAR-TORN VILLAGE" },
    { start: 6500, end: 10000, name: "MILITARY OUTPOST" },
    { start: 10000, end: 14000, name: "DEAD FOREST" },
    { start: 14000, end: 18000, name: "THE FINAL BUNKER" }
];

function zoneName() {

    for (const z of zones) {
        if (player.x >= z.start && player.x < z.end) {
            return z.name;
        }
    }

    return "UNKNOWN";
}

function showMessage(text, duration=2) {
    message = text;
    messageTimer = duration;
}

function random(min, max) {
    return Math.random() * (max - min) + min;
}

function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
}

function distance(a, b) {
    return Math.hypot(a.x - b.x, a.y - b.y);
}

function addXP(amount) {

    player.xp += amount;

    while (player.xp >= player.nextXP) {

        player.xp -= player.nextXP;

        player.level++;

        player.maxHealth += 8;
        player.health = player.maxHealth;

        player.nextXP = Math.floor(player.nextXP * 1.35);

        showMessage(
            "LEVEL UP! Level " + player.level,
            3
        );
    }
}

function createWorld() {

    chests.length = 0;
    crates.length = 0;
    wrecks.length = 0;

    for (let x = 700; x < WORLD_WIDTH; x += random(450, 850)) {

        if (Math.random() < 0.75) {

            chests.push({
                x: x,
                y: GROUND - 40,
                opened: false,
                rare: Math.random() < 0.16
            });
        }

        if (Math.random() < 0.7) {

            crates.push({
                x: x + random(-100, 100),
                y: GROUND - 40
            });
        }

        if (Math.random() < 0.35) {

            wrecks.push({
                x: x + random(-150, 150),
                y: GROUND - 70,
                w: random(150, 250)
            });
        }
    }
}

function spawnZombie(type = null) {

    let ztype = type;

    if (!ztype) {

        const roll = Math.random();

        if (roll < .65) ztype = "walker";
        else if (roll < .87) ztype = "runner";
        else ztype = "soldier";
    }

    let x;

    if (Math.random() < .5) {
        x = player.x + random(850, 1500);
    } else {
        x = player.x - random(850, 1500);
    }

    x = clamp(x, 100, WORLD_WIDTH - 100);

    const data = {
        walker: {
            hp: 65,
            speed: 55,
            damage: 9,
            size: 48,
            color: "#60705b"
        },

        runner: {
            hp: 42,
            speed: 105,
            damage: 12,
            size: 43,
            color: "#7e6655"
        },

        soldier: {
            hp: 110,
            speed: 42,
            damage: 17,
            size: 55,
            color: "#4d5b48"
        }
    }[ztype];

    zombies.push({
        type: ztype,

        x: x,
        y: GROUND - data.size,

        w: data.size,
        h: data.size,

        hp: data.hp * (1 + wave * .08),
        maxHp: data.hp * (1 + wave * .08),

        speed: data.speed * (1 + wave * .025),

        damage: data.damage * (1 + wave * .04),

        attackCooldown: 0,

        color: data.color,

        dead: false,

        hitFlash: 0
    });
}

function spawnWave() {

    const count = Math.min(30, 4 + wave * 2);

    for (let i = 0; i < count; i++) {
        spawnZombie();
    }

    showMessage(
        "WAVE " + wave + " — THE DEAD ARE COMING",
        3
    );
}

function spawnBoss() {

    boss = {
        x: 15300,
        y: GROUND - 145,

        w: 90,
        h: 145,

        hp: 1800,
        maxHp: 1800,

        speed: 65,

        attackCooldown: 0,

        color: "#252d27"
    };

    showMessage(
        "THE WARDEN HAS ARRIVED",
        5
    );
}

function shoot() {

    if (!gameRunning) return;

    if (player.reloadTimer > 0) return;

    if (player.fireCooldown > 0) return;

    if (player.ammo <= 0) {

        showMessage("EMPTY MAGAZINE — PRESS R");

        reload();

        return;
    }

    player.ammo--;

    player.fireCooldown = .22;

    const worldMouseX =
        mouse.x + cameraX;

    const worldMouseY =
        mouse.y;

    const ox =
        player.x +
        player.w / 2 +
        player.facing * 25;

    const oy =
        player.y + 38;

    let dx = worldMouseX - ox;
    let dy = worldMouseY - oy;

    const length =
        Math.hypot(dx, dy) || 1;

    dx /= length;
    dy /= length;

    bullets.push({
        x: ox,
        y: oy,

        vx: dx * 1200,
        vy: dy * 1200,

        damage: 34,

        life: 1.4
    });

    screenShake = 3;
}

function reload() {

    if (player.reloadTimer > 0) return;

    if (player.ammo >= player.magazine) return;

    if (player.reserveAmmo <= 0) {

        showMessage("NO AMMUNITION");

        return;
    }

    player.reloadTimer = 1.25;

    showMessage("RELOADING...");
}

function finishReload() {

    const needed =
        player.magazine - player.ammo;

    const amount =
        Math.min(needed, player.reserveAmmo);

    player.ammo += amount;
    player.reserveAmmo -= amount;
}

function grenade() {

    if (!gameRunning) return;

    if (player.grenades <= 0) {

        showMessage("NO GRENADES");

        return;
    }

    player.grenades--;

    const targetX =
        mouse.x + cameraX;

    const targetY =
        mouse.y;

    let dx =
        targetX - player.x;

    let dy =
        targetY - player.y;

    const len =
        Math.hypot(dx, dy) || 1;

    dx /= len;
    dy /= len;

    grenades.push({
        x: player.x,
        y: player.y + 30,

        vx: dx * 480,
        vy: dy * 480,

        timer: 1.0
    });
}

function interact() {

    for (const chest of chests) {

        if (chest.opened) continue;

        if (
            Math.abs(player.x - chest.x) < 100
        ) {

            chest.opened = true;

            const ammo =
                chest.rare ? 35 : 15;

            player.reserveAmmo += ammo;

            if (Math.random() < .5) {
                player.health = Math.min(
                    player.maxHealth,
                    player.health + 25
                );
            }

            if (Math.random() < .35) {
                player.grenades++;
            }

            addXP(chest.rare ? 100 : 35);

            showMessage(
                chest.rare
                    ? "RARE MILITARY CACHE FOUND!"
                    : "SUPPLIES FOUND!",
                3
            );

            return;
        }
    }
}

function hurtPlayer(amount) {

    if (player.invincible > 0) return;

    player.health -= amount;

    player.invincible = .7;

    screenShake = 10;

    showMessage("-" + Math.floor(amount) + " HEALTH");

    if (player.health <= 0) {

        player.health = 0;

        endGame();
    }
}

function killZombie(z) {

    if (z.dead) return;

    z.dead = true;

    zombiesKilled++;

    player.score += 100;

    addXP(45);

    for (let i = 0; i < 10; i++) {

        particles.push({
            x: z.x + z.w / 2,
            y: z.y + z.h / 2,

            vx: random(-180, 180),
            vy: random(-250, 50),

            life: random(.3, .8),

            color: "#a62d2d"
        });
    }
}

function damageZombie(z, amount) {

    z.hp -= amount;

    z.hitFlash = .08;

    if (z.hp <= 0) {
        killZombie(z);
    }
}

function updatePlayer(dt) {

    player.fireCooldown =
        Math.max(0, player.fireCooldown - dt);

    player.invincible =
        Math.max(0, player.invincible - dt);

    if (player.reloadTimer > 0) {

        player.reloadTimer -= dt;

        if (player.reloadTimer <= 0) {
            finishReload();
        }
    }

    let direction = 0;

    if (
        keys["KeyA"] ||
        keys["ArrowLeft"]
    ) {
        direction--;
    }

    if (
        keys["KeyD"] ||
        keys["ArrowRight"]
    ) {
        direction++;
    }

    const sprint =
        keys["ShiftLeft"] ||
        keys["ShiftRight"];

    let speed =
        sprint &&
        player.stamina > 0
            ? player.sprintSpeed
            : player.speed;

    if (sprint && direction !== 0) {

        player.stamina -= 28 * dt;

    } else {

        player.stamina += 20 * dt;
    }

    player.stamina =
        clamp(player.stamina, 0, player.maxStamina);

    player.vx =
        direction * speed;

    if (direction !== 0) {
        player.facing = direction;
    }

    if (
        (keys["KeyW"] ||
        keys["Space"]) &&
        player.y + player.h >= GROUND - 2
    ) {

        player.vy = -620;
    }

    player.vy += 1500 * dt;

    player.x += player.vx * dt;
    player.y += player.vy * dt;

    if (player.y + player.h >= GROUND) {

        player.y =
            GROUND - player.h;

        player.vy = 0;
    }

    player.x =
        clamp(
            player.x,
            0,
            WORLD_WIDTH - player.w
        );

    player.hunger -= .25 * dt;

    if (player.hunger <= 0) {

        player.hunger = 0;

        player.health -= 2 * dt;
    }

    if (mouse.down) {
        shoot();
    }
}

function updateBullets(dt) {

    for (let i = bullets.length - 1; i >= 0; i--) {

        const b = bullets[i];

        b.x += b.vx * dt;
        b.y += b.vy * dt;

        b.life -= dt;

        let hit = false;

        for (const z of zombies) {

            if (z.dead) continue;

            if (
                b.x > z.x &&
                b.x < z.x + z.w &&
                b.y > z.y &&
                b.y < z.y + z.h
            ) {

                damageZombie(z, b.damage);

                hit = true;

                break;
            }
        }

        if (
            boss &&
            b.x > boss.x &&
            b.x < boss.x + boss.w &&
            b.y > boss.y &&
            b.y < boss.y + boss.h
        ) {

            boss.hp -= b.damage;

            hit = true;

            if (boss.hp <= 0) {

                boss = null;

                document
                    .getElementById("victory")
                    .classList
                    .remove("hidden");

                gameRunning = false;
            }
        }

        if (
            hit ||
            b.life <= 0 ||
            b.x < 0 ||
            b.x > WORLD_WIDTH
        ) {

            bullets.splice(i, 1);
        }
    }
}

function updateZombies(dt) {

    for (const z of zombies) {

        if (z.dead) continue;

        z.hitFlash =
            Math.max(0, z.hitFlash - dt);

        z.attackCooldown =
            Math.max(
                0,
                z.attackCooldown - dt
            );

        const dx =
            player.x - z.x;

        const distance =
            Math.abs(dx);

        if (distance > 50) {

            z.x +=
                Math.sign(dx) *
                z.speed *
                dt;
        }

        if (
            distance < 65 &&
            z.attackCooldown <= 0
        ) {

            hurtPlayer(z.damage);

            z.attackCooldown = 1.0;
        }

        z.x =
            clamp(
                z.x,
                0,
                WORLD_WIDTH - z.w
            );
    }

    for (let i = zombies.length - 1; i >= 0; i--) {

        if (zombies[i].dead) {
            zombies.splice(i, 1);
        }
    }

    if (
        zombies.length === 0 &&
        player.x < 14500
    ) {

        wave++;

        spawnWave();
    }
}

function updateBoss(dt) {

    if (!boss) return;

    boss.attackCooldown =
        Math.max(
            0,
            boss.attackCooldown - dt
        );

    const dx =
        player.x - boss.x;

    if (Math.abs(dx) > 90) {

        boss.x +=
            Math.sign(dx) *
            boss.speed *
            dt;
    }

    if (
        Math.abs(dx) < 110 &&
        boss.attackCooldown <= 0
    ) {

        hurtPlayer(28);

        boss.attackCooldown = 1.2;
    }
}

function updateGrenades(dt) {

    for (
        let i = grenades.length - 1;
        i >= 0;
        i--
    ) {

        const g = grenades[i];

        g.x += g.vx * dt;
        g.y += g.vy * dt;

        g.vy += 700 * dt;

        g.timer -= dt;

        if (g.timer <= 0) {

            for (const z of zombies) {

                const d =
                    Math.hypot(
                        g.x - z.x,
                        g.y - z.y
                    );

                if (d < 230) {

                    damageZombie(
                        z,
                        160 * (1 - d / 300)
                    );
                }
            }

            if (boss) {

                const d =
                    Math.hypot(
                        g.x - boss.x,
                        g.y - boss.y
                    );

                if (d < 250) {

                    boss.hp -=
                        250 * (1 - d / 300);
                }
            }

            for (let p = 0; p < 35; p++) {

                particles.push({
                    x: g.x,
                    y: g.y,

                    vx: random(-350, 350),
                    vy: random(-350, 100),

                    life: random(.3, 1),

                    color: Math.random() < .5
                        ? "#e2a63b"
                        : "#9e3427"
                });
            }

            screenShake = 18;

            grenades.splice(i, 1);
        }
    }
}

function updateParticles(dt) {

    for (
        let i = particles.length - 1;
        i >= 0;
        i--
    ) {

        const p = particles[i];

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        p.vy += 500 * dt;

        p.life -= dt;

        if (p.life <= 0) {
            particles.splice(i, 1);
        }
    }
}

function updateCamera() {

    const target =
        player.x - W * .4;

    cameraX +=
        (target - cameraX) * .1;

    cameraX =
        clamp(
            cameraX,
            0,
            WORLD_WIDTH - W
        );
}

function drawBackground() {

    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            H
        );

    gradient.addColorStop(
        0,
        "#151b18"
    );

    gradient.addColorStop(
        .6,
        "#30382d"
    );

    gradient.addColorStop(
        1,
        "#151713"
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    // Moon
    ctx.fillStyle =
        "rgba(220,220,180,.18)";

    ctx.beginPath();

    ctx.arc(
        W * .78,
        120,
        70,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // Clouds
    for (let i = 0; i < 12; i++) {

        const x =
            ((i * 850 - cameraX * .15)
                % (W + 900)) - 400;

        const y =
            70 + (i % 4) * 50;

        ctx.fillStyle =
            "rgba(0,0,0,.18)";

        ctx.beginPath();

        ctx.ellipse(
            x,
            y,
            130,
            28,
            0,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    // Distant ruins
    for (
        let x = -500;
        x < W + 500;
        x += 300
    ) {

        const world =
            x + cameraX * .35;

        const height =
            80 + Math.sin(world * .01) * 40;

        ctx.fillStyle =
            "#20251f";

        ctx.fillRect(
            x,
            GROUND - height,
            170,
            height
        );

        ctx.fillStyle =
            "#10130f";

        for (
            let wx = x + 20;
            wx < x + 150;
            wx += 35
        ) {

            ctx.fillRect(
                wx,
                GROUND - height + 30,
                15,
                25
            );
        }
    }
}

function drawGround() {

    ctx.fillStyle = "#3d402d";

    ctx.fillRect(
        0,
        GROUND,
        W,
        H - GROUND
    );

    ctx.fillStyle = "#282b20";

    ctx.fillRect(
        0,
        GROUND,
        W,
        10
    );

    // road
    ctx.fillStyle = "#292a25";

    ctx.fillRect(
        0,
        GROUND + 30,
        W,
        150
    );

    ctx.strokeStyle =
        "rgba(190,170,105,.3)";

    ctx.lineWidth = 4;

    const roadOffset =
        -cameraX % 120;

    for (
        let x = roadOffset - 120;
        x < W + 120;
        x += 120
    ) {

        ctx.beginPath();

        ctx.moveTo(
            x,
            GROUND + 105
        );

        ctx.lineTo(
            x + 65,
            GROUND + 105
        );

        ctx.stroke();
    }
}

function drawWrecks() {

    for (const w of wrecks) {

        const sx =
            w.x - cameraX;

        if (
            sx < -300 ||
            sx > W + 300
        ) continue;

        ctx.fillStyle =
            "#353a34";

        ctx.beginPath();

        ctx.moveTo(
            sx,
            w.y + 70
        );

        ctx.lineTo(
            sx + w.w * .12,
            w.y + 25
        );

        ctx.lineTo(
            sx + w.w * .7,
            w.y
        );

        ctx.lineTo(
            sx + w.w,
            w.y + 30
        );

        ctx.lineTo(
            sx + w.w,
            w.y + 70
        );

        ctx.closePath();

        ctx.fill();

        ctx.fillStyle =
            "#121412";

        ctx.beginPath();

        ctx.arc(
            sx + 35,
            w.y + 65,
            20,
            0,
            Math.PI * 2
        );

        ctx.arc(
            sx + w.w - 35,
            w.y + 65,
            20,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }
}

function drawCrates() {

    for (const c of crates) {

        const x =
            c.x - cameraX;

        if (x < -80 || x > W + 80) continue;

        ctx.fillStyle =
            "#70543a";

        ctx.fillRect(
            x,
            c.y,
            55,
            40
        );

        ctx.strokeStyle =
            "#35291d";

        ctx.lineWidth = 4;

        ctx.strokeRect(
            x,
            c.y,
            55,
            40
        );

        ctx.beginPath();

        ctx.moveTo(
            x,
            c.y
        );

        ctx.lineTo(
            x + 55,
            c.y + 40
        );

        ctx.moveTo(
            x + 55,
            c.y
        );

        ctx.lineTo(
            x,
            c.y + 40
        );

        ctx.stroke();
    }
}

function drawChests() {

    for (const c of chests) {

        const x =
            c.x - cameraX;

        if (x < -100 || x > W + 100) continue;

        ctx.fillStyle =
            c.rare
                ? "#624f77"
                : "#765638";

        ctx.fillRect(
            x,
            c.y,
            65,
            40
        );

        ctx.strokeStyle =
            "#241d17";

        ctx.lineWidth = 4;

        ctx.strokeRect(
            x,
            c.y,
            65,
            40
        );

        ctx.fillStyle =
            "#d4b34b";

        ctx.fillRect(
            x + 28,
            c.y + 14,
            9,
            9
        );

        if (!c.opened) {

            ctx.fillStyle =
                "rgba(255,220,90,.25)";

            ctx.fillRect(
                x - 8,
                c.y - 8,
                81,
                56
            );
        }
    }
}

function drawPlayer() {

    const x =
        player.x - cameraX;

    const y =
        player.y;

    ctx.save();

    if (player.invincible > 0) {

        ctx.globalAlpha =
            Math.sin(
                Date.now() * .025
            ) > 0
                ? .35
                : 1;
    }

    // legs
    ctx.fillStyle = "#272b25";

    ctx.fillRect(
        x + 9,
        y + 67,
        11,
        33
    );

    ctx.fillRect(
        x + 27,
        y + 67,
        11,
        33
    );

    // boots
    ctx.fillStyle = "#171713";

    ctx.fillRect(
        x + 5,
        y + 94,
        18,
        8
    );

    ctx.fillRect(
        x + 26,
        y + 94,
        18,
        8
    );

    // body
    ctx.fillStyle = "#d6d0bd";

    ctx.fillRect(
        x + 7,
        y + 35,
        32,
        38
    );

    // jacket
    ctx.fillStyle = "#68705d";

    ctx.fillRect(
        x + 8,
        y + 42,
        30,
        30
    );

    // head
    ctx.fillStyle = "#dcae8e";

    ctx.beginPath();

    ctx.arc(
        x + 23,
        y + 25,
        18,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // hair
    ctx.fillStyle = "#563d2f";

    ctx.beginPath();

    ctx.arc(
        x + 23,
        y + 20,
        18,
        Math.PI,
        Math.PI * 2
    );

    ctx.fill();

    // hair back
    ctx.fillRect(
        x + 6,
        y + 20,
        7,
        28
    );

    // arm
    ctx.fillStyle = "#dcae8e";

    const gunDirection =
        player.facing;

    ctx.save();

    if (gunDirection < 0) {
        ctx.translate(
            x + 23,
            0
        );

        ctx.scale(-1, 1);

        ctx.translate(
            -(x + 23),
            0
        );
    }

    ctx.fillRect(
        x + 30,
        y + 42,
        28,
        9
    );

    // pistol
    ctx.fillStyle =
        "#171918";

    ctx.fillRect(
        x + 51,
        y + 38,
        23,
        7
    );

    ctx.fillRect(
        x + 55,
        y + 44,
        8,
        11
    );

    ctx.restore();

    ctx.restore();
}

function drawZombie(z) {

    const x =
        z.x - cameraX;

    const y =
        z.y;

    ctx.save();

    if (z.hitFlash > 0) {
        ctx.globalAlpha = .55;
    }

    // legs
    ctx.fillStyle = "#252a24";

    ctx.fillRect(
        x + 8,
        y + z.h - 28,
        10,
        28
    );

    ctx.fillRect(
        x + z.w - 18,
        y + z.h - 28,
        10,
        28
    );

    // body
    ctx.fillStyle =
        z.color;

    ctx.fillRect(
        x + 5,
        y + 25,
        z.w - 10,
        z.h - 40
    );

    // head
    ctx.fillStyle =
        "#8d9b76";

    ctx.beginPath();

    ctx.arc(
        x + z.w / 2,
        y + 19,
        18,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // eyes
    ctx.fillStyle =
        "#b92c2c";

    ctx.fillRect(
        x + z.w / 2 - 9,
        y + 15,
        5,
        5
    );

    ctx.fillRect(
        x + z.w / 2 + 5,
        y + 15,
        5,
        5
    );

    // arms
    ctx.strokeStyle =
        "#879273";

    ctx.lineWidth = 9;

    ctx.beginPath();

    ctx.moveTo(
        x + 8,
        y + 38
    );

    ctx.lineTo(
        x - 15,
        y + 60
    );

    ctx.moveTo(
        x + z.w - 8,
        y + 38
    );

    ctx.lineTo(
        x + z.w + 15,
        y + 55
    );

    ctx.stroke();

    // health bar
    const hpRatio =
        clamp(
            z.hp / z.maxHp,
            0,
            1
        );

    ctx.fillStyle =
        "#171717";

    ctx.fillRect(
        x,
        y - 13,
        z.w,
        6
    );

    ctx.fillStyle =
        "#b52f2f";

    ctx.fillRect(
        x,
        y - 13,
        z.w * hpRatio,
        6
    );

    ctx.restore();
}

function drawBoss() {

    if (!boss) return;

    const x =
        boss.x - cameraX;

    const y =
        boss.y;

    ctx.fillStyle =
        boss.color;

    ctx.fillRect(
        x + 12,
        y + 35,
        boss.w - 24,
        boss.h - 35
    );

    ctx.fillStyle =
        "#7c8b68";

    ctx.beginPath();

    ctx.arc(
        x + boss.w / 2,
        y + 28,
        28,
        0,
        Math.PI * 2
    );

    ctx.fill();

    // helmet
    ctx.fillStyle =
        "#30372e";

    ctx.fillRect(
        x + 20,
        y + 2,
        50,
        15
    );

    ctx.fillStyle =
        "#d52828";

    ctx.fillRect(
        x + 32,
        y + 25,
        8,
        8
    );

    ctx.fillRect(
        x + 50,
        y + 25,
        8,
        8
    );

    // health
    const ratio =
        clamp(
            boss.hp / boss.maxHp,
            0,
            1
        );

    ctx.fillStyle =
        "#171717";

    ctx.fillRect(
        x - 10,
        y - 25,
        boss.w + 20,
        12
    );

    ctx.fillStyle =
        "#bd2828";

    ctx.fillRect(
        x - 10,
        y - 25,
        (boss.w + 20) * ratio,
        12
    );

    ctx.fillStyle = "white";

    ctx.font = "bold 16px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        "THE WARDEN",
        x + boss.w / 2,
        y - 32
    );
}

function drawBullets() {

    ctx.fillStyle =
        "#ffd86b";

    for (const b of bullets) {

        const x =
            b.x - cameraX;

        ctx.beginPath();

        ctx.arc(
            x,
            b.y,
            4,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }
}

function drawGrenades() {

    for (const g of grenades) {

        ctx.fillStyle =
            "#2c322b";

        ctx.beginPath();

        ctx.arc(
            g.x - cameraX,
            g.y,
            9,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }
}

function drawParticles() {

    for (const p of particles) {

        ctx.globalAlpha =
            clamp(p.life, 0, 1);

        ctx.fillStyle =
            p.color;

        ctx.fillRect(
            p.x - cameraX,
            p.y,
            4,
            4
        );
    }

    ctx.globalAlpha = 1;
}

function drawZoneTitle() {

    const zone =
        zoneName();

    ctx.fillStyle =
        "rgba(0,0,0,.35)";

    ctx.fillRect(
        W / 2 - 220,
        20,
        440,
        45
    );

    ctx.fillStyle =
        "#d2c89e";

    ctx.font =
        "bold 22px Arial";

    ctx.textAlign =
        "center";

    ctx.fillText(
        zone,
        W / 2,
        50
    );
}

function drawNightOverlay() {

    const darkness =
        .28 +
        Math.sin(gameTime * .08) * .08;

    ctx.fillStyle =
        `rgba(5,10,18,${darkness})`;

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    // flashlight
    const px =
        player.x - cameraX;

    const py =
        player.y + 45;

    const angle =
        Math.atan2(
            mouse.y - py,
            mouse.x - px
        );

    const gradient =
        ctx.createRadialGradient(
            px,
            py,
            40,
            px,
            py,
            500
        );

    gradient.addColorStop(
        0,
        "rgba(255,245,200,.16)"
    );

    gradient.addColorStop(
        1,
        "rgba(255,245,200,0)"
    );

    ctx.fillStyle =
        gradient;

    ctx.beginPath();

    ctx.arc(
        px,
        py,
        500,
        0,
        Math.PI * 2
    );

    ctx.fill();
}

function draw() {

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    ctx.save();

    if (screenShake > 0) {

        ctx.translate(
            random(-screenShake, screenShake),
            random(-screenShake, screenShake)
        );

        screenShake *= .9;

        if (screenShake < .2) {
            screenShake = 0;
        }
    }

    drawBackground();

    drawGround();

    drawWrecks();

    drawCrates();

    drawChests();

    drawBullets();

    drawGrenades();

    for (const z of zombies) {
        if (!z.dead) {
            drawZombie(z);
        }
    }

    drawBoss();

    drawPlayer();

    drawParticles();

    drawNightOverlay();

    drawZoneTitle();

    ctx.restore();

    updateHUD();
}

function updateHUD() {

    document.getElementById(
        "healthFill"
    ).style.width =
        (player.health /
        player.maxHealth * 100) + "%";

    document.getElementById(
        "staminaFill"
    ).style.width =
        (player.stamina /
        player.maxStamina * 100) + "%";

    document.getElementById(
        "xpFill"
    ).style.width =
        (player.xp /
        player.nextXP * 100) + "%";

    document.getElementById(
        "info"
    ).innerHTML = `
        <b>LEVEL:</b> ${player.level}<br>
        <b>WEAPON:</b> ${player.weapon}<br>
        <b>AMMO:</b> ${player.ammo}/${player.reserveAmmo}<br>
        <b>GRENADES:</b> ${player.grenades}<br>
        <b>WAVE:</b> ${wave}<br>
        <b>ZOMBIES:</b> ${zombiesKilled}<br>
        <b>SCORE:</b> ${player.score}<br>
        <b>ZONE:</b> ${zoneName()}
    `;

    document.getElementById(
        "message"
    ).textContent =
        messageTimer > 0
            ? message
            : "";
}

function update(dt) {

    if (!gameRunning) return;

    gameTime += dt;

    if (messageTimer > 0) {
        messageTimer -= dt;
    }

    updatePlayer(dt);

    updateBullets(dt);

    updateZombies(dt);

    updateBoss(dt);

    updateGrenades(dt);

    updateParticles(dt);

    updateCamera();

    if (
        player.x > 14000 &&
        !boss
    ) {
        spawnBoss();
    }

    if (player.health <= 0) {
        endGame();
    }
}

function loop(timestamp) {

    if (!window.lastTime) {
        window.lastTime = timestamp;
    }

    let dt =
        (timestamp - window.lastTime)
        / 1000;

    window.lastTime =
        timestamp;

    dt =
        Math.min(dt, .033);

    update(dt);

    draw();

    requestAnimationFrame(loop);
}

function startGame() {

    document
        .getElementById("menu")
        .classList
        .add("hidden");

    document
        .getElementById("gameOver")
        .classList
        .add("hidden");

    document
        .getElementById("victory")
        .classList
        .add("hidden");

    gameRunning = true;

    resetGame();

    spawnWave();
}

function resetGame() {

    player.x = 500;
    player.y = GROUND - player.h;

    player.health = 100;
    player.maxHealth = 100;

    player.stamina = 100;

    player.hunger = 100;

    player.level = 1;
    player.xp = 0;
    player.nextXP = 250;

    player.ammo = 8;
    player.reserveAmmo = 80;

    player.grenades = 3;

    player.score = 0;

    player.reloadTimer = 0;
    player.fireCooldown = 0;

    zombies.length = 0;
    bullets.length = 0;
    grenades.length = 0;
    particles.length = 0;

    boss = null;

    wave = 1;
    zombiesKilled = 0;

    cameraX = 0;

    createWorld();
}

function endGame() {

    if (!gameRunning) return;

    gameRunning = false;

    document.getElementById(
        "deathText"
    ).textContent =
        `You reached level ${player.level}, `
        + `killed ${zombiesKilled} zombies `
        + `and scored ${player.score} points.`;

    document
        .getElementById("gameOver")
        .classList
        .remove("hidden");
}

function restartGame() {

    document
        .getElementById("gameOver")
        .classList
        .add("hidden");

    document
        .getElementById("victory")
        .classList
        .add("hidden");

    startGame();
}

document
    .getElementById("startButton")
    .addEventListener(
        "click",
        startGame
    );


// Mobile controls
function holdButton(id, code) {

    const element =
        document.getElementById(id);

    element.addEventListener(
        "touchstart",
        e => {
            e.preventDefault();
            keys[code] = true;
        }
    );

    element.addEventListener(
        "touchend",
        e => {
            e.preventDefault();
            keys[code] = false;
        }
    );

    element.addEventListener(
        "mousedown",
        () => {
            keys[code] = true;
        }
    );

    element.addEventListener(
        "mouseup",
        () => {
            keys[code] = false;
        }
    );
}

holdButton("left", "KeyA");
holdButton("right", "KeyD");
holdButton("jump", "Space");

document
    .getElementById("shoot")
    .addEventListener(
        "touchstart",
        e => {
            e.preventDefault();
            mouse.down = true;
        }
    );

document
    .getElementById("shoot")
    .addEventListener(
        "touchend",
        e => {
            e.preventDefault();
            mouse.down = false;
        }
    );

document
    .getElementById("grenade")
    .addEventListener(
        "click",
        grenade
    );

document
    .getElementById("reload")
    .addEventListener(
        "click",
        reload
    );

createWorld();

requestAnimationFrame(loop);

</script>

</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/health")
def health():
    return {
        "status": "ok",
        "game": "Ashes of the Dead"
    }


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
