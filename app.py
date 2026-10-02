from flask import Flask, Response, jsonify

app = Flask(__name__)

GAME_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ashes of the Dead</title>

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #050607;
    color: white;
    font-family: monospace;
}

body {
    display: flex;
    align-items: center;
    justify-content: center;
}

#game-container {
    position: relative;
    width: min(100vw, 1280px);
    aspect-ratio: 16 / 9;
    background: #111;
    box-shadow: 0 0 50px #000;
}

canvas {
    width: 100%;
    height: 100%;
    display: block;
    image-rendering: pixelated;
}

#menu {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(circle at center,
        rgba(50,50,50,.2),
        rgba(0,0,0,.96));
    z-index: 10;
}

.menu-box {
    width: min(760px, 90%);
    padding: 35px;
    text-align: center;
    background: rgba(8,10,10,.96);
    border: 2px solid #777;
    box-shadow: 0 0 50px #000;
}

.title {
    font-size: clamp(35px, 7vw, 75px);
    letter-spacing: 5px;
    margin-bottom: 5px;
}

.subtitle {
    color: #999;
    margin-bottom: 25px;
}

button {
    background: #242925;
    border: 1px solid #777;
    color: white;
    padding: 12px 25px;
    margin: 5px;
    font-family: monospace;
    cursor: pointer;
}

button:hover,
button.selected {
    background: #514a32;
    border-color: #d8c27a;
}

.instructions {
    margin-top: 25px;
    color: #999;
    font-size: 12px;
    line-height: 1.7;
}

#touch {
    display: none;
}

@media (pointer: coarse) {
    #touch {
        display: block;
        position: absolute;
        inset: 0;
        pointer-events: none;
    }

    .touch-left,
    .touch-right {
        position: absolute;
        bottom: 15px;
        display: flex;
        gap: 8px;
        pointer-events: auto;
    }

    .touch-left {
        left: 15px;
    }

    .touch-right {
        right: 15px;
    }

    .touch-left button,
    .touch-right button {
        width: 55px;
        height: 55px;
        padding: 0;
        background: rgba(20,20,20,.7);
    }
}
</style>
</head>

<body>

<div id="game-container">

<canvas id="game" width="1280" height="720"></canvas>

<div id="menu">

<div class="menu-box">

<div class="title">ASHES OF THE DEAD</div>

<div class="subtitle">
PIXELATED 2D DETECTIVE HORROR
</div>

<div>
<button class="character selected" data-character="Julia">
JULIA
</button>

<button class="character" data-character="May">
MAY
</button>

<button class="character" data-character="Yumi">
YUMI
</button>
</div>

<br>

<button id="start-game">
START GAME
</button>

<div class="instructions">
A / D or Arrow Keys — Move<br>
W / Space — Jump<br>
Shift — Run<br>
Mouse — Aim<br>
Left Mouse — Shoot<br>
F — Flashlight<br>
E — Interact<br>
R — Reload<br>
Q — Melee<br>
P / ESC — Pause
<br><br>
This is a fictional horror game.
</div>

</div>
</div>

<div id="touch">
    <div class="touch-left">
        <button data-key="ArrowLeft">◀</button>
        <button data-key="Space">▲</button>
        <button data-key="ArrowRight">▶</button>
    </div>

    <div class="touch-right">
        <button data-key="f">☼</button>
        <button data-key="e">E</button>
    </div>
</div>

</div>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

ctx.imageSmoothingEnabled = false;

const WIDTH = 1280;
const HEIGHT = 720;

let selectedCharacter = "Julia";
let gameStarted = false;
let paused = false;
let gameOver = false;

const keys = {};

const mouse = {
    x: WIDTH / 2,
    y: HEIGHT / 2,
    down: false
};

document.querySelectorAll(".character").forEach(button => {

    button.addEventListener("click", () => {

        selectedCharacter = button.dataset.character;

        document.querySelectorAll(".character")
            .forEach(b => b.classList.remove("selected"));

        button.classList.add("selected");
    });

});

document.getElementById("start-game").addEventListener("click", () => {

    document.getElementById("menu").style.display = "none";

    gameStarted = true;

    startGame();

});

window.addEventListener("keydown", event => {

    keys[event.key] = true;
    keys[event.code] = true;

    if (
        event.code === "ArrowLeft" ||
        event.code === "ArrowRight" ||
        event.code === "Space"
    ) {
        event.preventDefault();
    }

    if (event.key.toLowerCase() === "p") {
        if (gameStarted && !gameOver) {
            paused = !paused;
        }
    }

    if (event.key === "Escape") {
        paused = !paused;
    }

    if (event.key.toLowerCase() === "f") {
        player.flashlight = !player.flashlight;
    }

    if (event.key.toLowerCase() === "r") {
        reload();
    }

    if (event.key.toLowerCase() === "q") {
        melee();
    }

});

window.addEventListener("keyup", event => {

    keys[event.key] = false;
    keys[event.code] = false;

});

canvas.addEventListener("mousemove", event => {

    const rect = canvas.getBoundingClientRect();

    mouse.x =
        (event.clientX - rect.left)
        * WIDTH / rect.width;

    mouse.y =
        (event.clientY - rect.top)
        * HEIGHT / rect.height;

});

canvas.addEventListener("mousedown", event => {

    if (event.button === 0) {
        mouse.down = true;
    }

});

window.addEventListener("mouseup", event => {

    if (event.button === 0) {
        mouse.down = false;
    }

});

document.querySelectorAll("#touch button").forEach(button => {

    const key = button.dataset.key;

    button.addEventListener("pointerdown", event => {

        event.preventDefault();
        keys[key] = true;

    });

    button.addEventListener("pointerup", event => {

        event.preventDefault();
        keys[key] = false;

    });

});


// ------------------------------------------------------------
// PLAYER
// ------------------------------------------------------------

const player = {

    x: 250,
    y: 538,

    width: 32,
    height: 62,

    velocityX: 0,
    velocityY: 0,

    grounded: true,

    health: 100,
    sanity: 100,
    stamina: 100,

    ammo: 12,
    reserveAmmo: 72,

    flashlight: false,

    invulnerable: 0,

    shootingCooldown: 0,
    meleeCooldown: 0,

    kills: 0

};


// ------------------------------------------------------------
// WORLD
// ------------------------------------------------------------

const WORLD_WIDTH = 12000;

let cameraX = 0;

let worldTime = 0;

let weather = "rain";
let weatherTimer = 15;

let objective =
    "Find a way out of the abandoned asylum.";

let message = "";
let messageTimer = 0;

const doors = [
    { x: 1150, open: false },
    { x: 2250, open: false },
    { x: 3250, open: false },
    { x: 5200, open: false }
];

const keysItems = [
    { x: 800, taken: false },
    { x: 1780, taken: false }
];

const chests = [
    { x: 1100, opened: false },
    { x: 3050, opened: false },
    { x: 7000, opened: false }
];

const buildings = [

    { x: 520, y: 500, width: 160, height: 100 },
    { x: 930, y: 470, width: 140, height: 130 },

    { x: 1500, y: 520, width: 300, height: 80 },
    { x: 2050, y: 450, width: 180, height: 150 },

    { x: 2650, y: 520, width: 330, height: 80 },

    { x: 3500, y: 470, width: 220, height: 130 },

    { x: 4400, y: 520, width: 500, height: 80 },

    { x: 5600, y: 480, width: 260, height: 120 },

    { x: 6700, y: 510, width: 420, height: 90 },

    { x: 7900, y: 450, width: 200, height: 150 },

    { x: 9000, y: 510, width: 500, height: 90 },

    { x: 10300, y: 470, width: 250, height: 130 }

];


// ------------------------------------------------------------
// ZOMBIES
// ------------------------------------------------------------

let zombies = [];

function spawnZombie(x, type = "walker") {

    zombies.push({

        x: x,
        y: 535,

        width: 35,
        height: 65,

        hp:
            type === "brute"
                ? 100
                : 45,

        speed:
            type === "runner"
                ? 115
                : type === "brute"
                    ? 35
                    : 55,

        type: type,

        attackCooldown: 0,

        hitFlash: 0

    });

}

function spawnZombies() {

    zombies = [];

    [
        1400,
        1650,
        2400,
        2850,
        3650,
        4700,
        5750,
        6900,
        8150,
        9250,
        10800

    ].forEach((x, index) => {

        spawnZombie(
            x,
            index % 5 === 0
                ? "runner"
                : "walker"
        );

    });

    spawnZombie(10150, "brute");

}


// ------------------------------------------------------------
// BULLETS
// ------------------------------------------------------------

let bullets = [];


// ------------------------------------------------------------
// EFFECTS
// ------------------------------------------------------------

let particles = [];

let floatingTexts = [];


// ------------------------------------------------------------
// SMILER
// ------------------------------------------------------------

let smiler = null;

function spawnSmiler() {

    if (smiler) return;

    smiler = {

        x:
            player.x +
            (Math.random() < .5 ? -500 : 500),

        lifetime: 5

    };

}


// ------------------------------------------------------------
// UTILITY
// ------------------------------------------------------------

function clamp(value, min, max) {

    return Math.max(
        min,
        Math.min(max, value)
    );

}

function showMessage(text, duration = 3) {

    message = text;
    messageTimer = duration;

}

function reload() {

    if (
        player.ammo >= 12 ||
        player.reserveAmmo <= 0
    ) {
        return;
    }

    const amount =
        Math.min(
            12 - player.ammo,
            player.reserveAmmo
        );

    player.ammo += amount;
    player.reserveAmmo -= amount;

    showMessage("RELOADED", 1);

}

function melee() {

    if (player.meleeCooldown > 0) {
        return;
    }

    player.meleeCooldown = .5;

    zombies.forEach(zombie => {

        if (
            Math.abs(zombie.x - player.x) < 75 &&
            Math.abs(zombie.y - player.y) < 80
        ) {

            zombie.hp -= 35;

            zombie.hitFlash = .15;

            showMessage(
                "MELEE HIT",
                .6
            );

        }

    });

}

function shoot() {

    if (
        player.shootingCooldown > 0 ||
        player.ammo <= 0
    ) {
        return;
    }

    player.ammo--;

    player.shootingCooldown = .18;

    const direction =
        mouse.x + cameraX >
        player.x
            ? 1
            : -1;

    bullets.push({

        x: player.x + 15,

        y: player.y + 25,

        velocityX:
            direction * 950,

        lifetime: 1

    });

    particles.push({

        x:
            player.x +
            direction * 30,

        y:
            player.y + 25,

        velocityX:
            direction * 100,

        velocityY: -30,

        lifetime: .15,

        type: "muzzle"

    });

    if (player.ammo === 0) {

        showMessage(
            "OUT OF AMMO — PRESS R",
            1.2
        );

    }

}


// ------------------------------------------------------------
// SAVE SYSTEM
// ------------------------------------------------------------

function saveGame() {

    localStorage.setItem(
        "ashes_of_the_dead_save",

        JSON.stringify({

            character: selectedCharacter,

            x: player.x,

            health: player.health,

            sanity: player.sanity,

            ammo: player.ammo,

            reserveAmmo: player.reserveAmmo,

            kills: player.kills

        })

    );

    showMessage(
        "GAME SAVED",
        1.2
    );

}

function loadGame() {

    const raw =
        localStorage.getItem(
            "ashes_of_the_dead_save"
        );

    if (!raw) {
        return;
    }

    try {

        const data =
            JSON.parse(raw);

        selectedCharacter =
            data.character ||
            selectedCharacter;

        player.x =
            data.x || 250;

        player.health =
            data.health ?? 100;

        player.sanity =
            data.sanity ?? 100;

        player.ammo =
            data.ammo ?? 12;

        player.reserveAmmo =
            data.reserveAmmo ?? 72;

        player.kills =
            data.kills || 0;

        showMessage(
            "SAVE LOADED",
            2
        );

    } catch (error) {

        console.error(error);

    }

}


// ------------------------------------------------------------
// START
// ------------------------------------------------------------

function startGame() {

    player.x = 250;

    player.health = 100;

    player.sanity = 100;

    player.ammo = 12;

    player.reserveAmmo = 72;

    player.kills = 0;

    objective =
        "Find a way out of the abandoned asylum.";

    spawnZombies();

    showMessage(
        "WAKE UP, " +
        selectedCharacter.toUpperCase() +
        ".",
        4
    );

}


// ------------------------------------------------------------
// UPDATE
// ------------------------------------------------------------

function update(delta) {

    if (
        !gameStarted ||
        paused ||
        gameOver
    ) {
        return;
    }

    worldTime += delta;

    messageTimer -= delta;

    player.invulnerable =
        Math.max(
            0,
            player.invulnerable - delta
        );

    player.shootingCooldown =
        Math.max(
            0,
            player.shootingCooldown - delta
        );

    player.meleeCooldown =
        Math.max(
            0,
            player.meleeCooldown - delta
        );


    const left =
        keys.a ||
        keys.A ||
        keys.ArrowLeft;

    const right =
        keys.d ||
        keys.D ||
        keys.ArrowRight;

    const running =
        keys.Shift &&
        player.stamina > 1;


    let movementSpeed =
        running
            ? 410
            : 260;


    if (running && (left || right)) {

        player.stamina -=
            30 * delta;

    } else {

        player.stamina =
            Math.min(
                100,
                player.stamina +
                20 * delta
            );

    }


    if (left) {

        player.velocityX =
            -movementSpeed;

    } else if (right) {

        player.velocityX =
            movementSpeed;

    } else {

        player.velocityX = 0;

    }


    if (
        (keys.w ||
        keys.W ||
        keys.Space) &&
        player.grounded
    ) {

        player.velocityY =
            -620;

        player.grounded = false;

    }


    player.velocityY +=
        1500 * delta;


    player.x +=
        player.velocityX * delta;

    player.y +=
        player.velocityY * delta;


    player.x =
        clamp(
            player.x,
            30,
            WORLD_WIDTH - 50
        );


    if (player.y >= 538) {

        player.y = 538;

        player.velocityY = 0;

        player.grounded = true;

    }


    if (mouse.down) {
        shoot();
    }


    // Bullets

    for (const bullet of bullets) {

        bullet.x +=
            bullet.velocityX * delta;

        bullet.lifetime -= delta;

    }


    bullets =
        bullets.filter(
            bullet =>
                bullet.lifetime > 0 &&
                bullet.x > 0 &&
                bullet.x < WORLD_WIDTH
        );


    // Zombies

    for (const zombie of zombies) {

        zombie.attackCooldown =
            Math.max(
                0,
                zombie.attackCooldown -
                delta
            );

        zombie.hitFlash =
            Math.max(
                0,
                zombie.hitFlash -
                delta
            );


        const distance =
            player.x -
            zombie.x;


        if (Math.abs(distance) < 850) {

            zombie.x +=
                Math.sign(distance) *
                zombie.speed *
                delta;

        }


        if (
            Math.abs(distance) < 55 &&
            zombie.attackCooldown <= 0 &&
            player.invulnerable <= 0
        ) {

            const damage =
                zombie.type === "brute"
                    ? 18
                    : 8;

            player.health -= damage;

            player.sanity -= 2;

            player.invulnerable =
                .35;

            zombie.attackCooldown =
                1.1;

            showMessage(
                "THE INFECTED FOUND YOU.",
                1
            );

        }

    }


    // Bullet collision

    for (const bullet of bullets) {

        for (const zombie of zombies) {

            if (
                Math.abs(
                    bullet.x -
                    zombie.x
                ) < 30 &&
                Math.abs(
                    bullet.y -
                    (zombie.y + 25)
                ) < 45
            ) {

                zombie.hp -= 34;

                zombie.hitFlash = .15;

                bullet.lifetime = 0;

                break;

            }

        }

    }


    // Remove dead zombies

    for (
        let i = zombies.length - 1;
        i >= 0;
        i--
    ) {

        if (zombies[i].hp <= 0) {

            player.kills++;

            floatingTexts.push({

                x: zombies[i].x,

                y: 470,

                text: "+1",

                lifetime: 1

            });

            zombies.splice(i, 1);

        }

    }


    // Particles

    for (const particle of particles) {

        particle.x +=
            particle.velocityX *
            delta;

        particle.y +=
            particle.velocityY *
            delta;

        particle.velocityY +=
            180 * delta;

        particle.lifetime -=
            delta;

    }

    particles =
        particles.filter(
            p => p.lifetime > 0
        );


    // Floating text

    for (const text of floatingTexts) {

        text.y -=
            25 * delta;

        text.lifetime -=
            delta;

    }

    floatingTexts =
        floatingTexts.filter(
            t => t.lifetime > 0
        );


    // Story progression

    if (
        player.x > 1100 &&
        objective.startsWith("Find")
    ) {

        objective =
            "Find the brass key.";

        showMessage(
            "Something is watching from the hallway.",
            3
        );

    }


    if (
        player.x > 800 &&
        !keysItems[0].taken
    ) {

        keysItems[0].taken = true;

        objective =
            "Reach the generator.";

        showMessage(
            "BRASS KEY ACQUIRED",
            2
        );

    }


    if (
        player.x > 3200 &&
        objective === "Reach the generator."
    ) {

        objective =
            "Escape the asylum.";

        showMessage(
            "POWER RESTORED. RUN.",
            3
        );

    }


    if (
        player.x > 6000 &&
        objective === "Escape the asylum."
    ) {

        objective =
            "Cross No Man's Land.";

        showMessage(
            "YOU ESCAPED THE ASYLUM... FOR NOW.",
            3
        );

    }


    if (
        player.x > 9000 &&
        objective === "Cross No Man's Land."
    ) {

        objective =
            "Find the source of the infection.";

        showMessage(
            "THE CITY IS FULL OF THE DEAD.",
            3
        );

    }


    if (player.x > 9600 && player.x < 10300) {

        player.sanity -=
            7 * delta;

        if (
            Math.random() <
            delta * .12
        ) {

            spawnSmiler();

        }

    }


    if (player.x > 11300) {

        objective =
            "PROJECT ECLIPSE: FIND THE SMILER.";

        showMessage(
            "YOU WERE NEVER ALONE.",
            3
        );

    }


    player.sanity =
        clamp(
            player.sanity,
            0,
            100
        );


    if (
        player.health <= 0 ||
        player.sanity <= 0
    ) {

        gameOver = true;

        saveGame();

    }


    // Weather

    weatherTimer -= delta;

    if (weatherTimer <= 0) {

        const options = [
            "clear",
            "rain",
            "fog",
            "storm"
        ];

        weather =
            options[
                Math.floor(
                    Math.random() *
                    options.length
                )
            ];

        weatherTimer =
            15 +
            Math.random() * 25;

    }


    // Camera

    cameraX +=
        (
            player.x -
            cameraX -
            WIDTH / 2
        ) *
        Math.min(
            1,
            delta * 6
        );


    cameraX =
        clamp(
            cameraX,
            0,
            WORLD_WIDTH - WIDTH
        );

}


// ------------------------------------------------------------
// SMILER UPDATE
// ------------------------------------------------------------

function updateSmiler(delta) {

    if (!smiler) {
        return;
    }

    smiler.lifetime -= delta;

    smiler.x +=
        (
            player.x -
            smiler.x
        ) *
        delta *
        .15;


    if (smiler.lifetime <= 0) {

        smiler = null;

    }

}


// ------------------------------------------------------------
// DRAW
// ------------------------------------------------------------

function draw() {

    ctx.clearRect(
        0,
        0,
        WIDTH,
        HEIGHT
    );


    // Sky

    ctx.fillStyle =
        "#141a1d";

    ctx.fillRect(
        0,
        0,
        WIDTH,
        HEIGHT
    );


    // Distant buildings

    for (
        let i = 0;
        i < 50;
        i++
    ) {

        const x =
            i * 260 -
            (cameraX * .18 % 260);

        const height =
            80 +
            (i * 37 % 170);

        ctx.fillStyle =
            i % 3 === 0
                ? "#202322"
                : "#171c1c";

        ctx.fillRect(
            x,
            600 - height,
            170,
            height
        );

        for (
            let window = 0;
            window < 5;
            window++
        ) {

            ctx.fillStyle =
                "#756d45";

            ctx.fillRect(
                x + 20 + window * 28,
                620 - height,
                8,
                10
            );

        }

    }


    // Moon

    ctx.fillStyle =
        "#aaa58e";

    ctx.fillRect(
        1020,
        80,
        35,
        35
    );


    // Ground

    ctx.fillStyle =
        "#343832";

    ctx.fillRect(
        0,
        600,
        WIDTH,
        120
    );


    for (
        let x = -(cameraX % 80);
        x < WIDTH;
        x += 80
    ) {

        ctx.fillStyle =
            "#45483d";

        ctx.fillRect(
            x,
            610,
            40,
            3
        );

        ctx.fillRect(
            x + 48,
            650,
            17,
            3
        );

    }


    // Buildings

    for (const building of buildings) {

        const x =
            building.x -
            cameraX;

        if (
            x < -300 ||
            x > WIDTH + 300
        ) {
            continue;
        }

        ctx.fillStyle =
            "#44433d";

        ctx.fillRect(
            x,
            building.y,
            building.width,
            building.height
        );

        ctx.fillStyle =
            "#272925";

        ctx.fillRect(
            x + 8,
            building.y + 10,
            building.width - 16,
            12
        );


        for (
            let wx = x + 18;
            wx < x + building.width - 20;
            wx += 42
        ) {

            ctx.fillStyle =
                "#9a8650";

            ctx.fillRect(
                wx,
                building.y + 35,
                13,
                10
            );

        }

    }


    // Doors

    for (const door of doors) {

        const x =
            door.x -
            cameraX;

        if (
            x > -100 &&
            x < WIDTH + 100
        ) {

            ctx.fillStyle =
                door.open
                    ? "#687064"
                    : "#252825";

            ctx.fillRect(
                x,
                480,
                55,
                120
            );

            ctx.strokeStyle =
                "#888";

            ctx.strokeRect(
                x,
                480,
                55,
                120
            );

        }

    }


    // Keys

    for (const item of keysItems) {

        if (item.taken) {
            continue;
        }

        const x =
            item.x -
            cameraX;

        ctx.fillStyle =
            "#d8bd4c";

        ctx.fillRect(
            x,
            555,
            20,
            7
        );

        ctx.fillRect(
            x + 14,
            555,
            4,
            15
        );

    }


    // Chests

    for (const chest of chests) {

        const x =
            chest.x -
            cameraX;

        ctx.fillStyle =
            "#684a2f";

        ctx.fillRect(
            x,
            550,
            70,
            42
        );

        ctx.fillStyle =
            "#b08a43";

        ctx.fillRect(
            x + 30,
            568,
            10,
            9
        );

    }


    // Zombies

    for (const zombie of zombies) {

        drawZombie(
            zombie.x - cameraX,
            zombie.y,
            zombie
        );

    }


    // Smiler

    if (smiler) {

        const x =
            smiler.x -
            cameraX;

        ctx.fillStyle =
            "#080909";

        ctx.fillRect(
            x - 20,
            445,
            40,
            105
        );

        ctx.fillStyle =
            "#eee";

        ctx.fillRect(
            x - 12,
            470,
            5,
            5
        );

        ctx.fillRect(
            x + 7,
            470,
            5,
            5
        );

        ctx.fillRect(
            x - 13,
            490,
            27,
            4
        );

    }


    // Player

    drawPlayer(
        player.x - cameraX,
        player.y
    );


    // Bullets

    ctx.fillStyle =
        "#f2df85";

    for (const bullet of bullets) {

        ctx.fillRect(
            bullet.x - cameraX,
            bullet.y,
            10,
            3
        );

    }


    // Particles

    for (const particle of particles) {

        ctx.fillStyle =
            "#e4b35c";

        ctx.fillRect(
            particle.x - cameraX,
            particle.y,
            4,
            4
        );

    }


    // Weather

    if (
        weather === "rain" ||
        weather === "storm"
    ) {

        ctx.strokeStyle =
            "rgba(160,190,205,.5)";

        for (
            let i = 0;
            i <
            (
                weather === "storm"
                    ? 130
                    : 70
            );
            i++
        ) {

            const x =
                (
                    i * 83 +
                    worldTime * 500
                ) % WIDTH;

            const y =
                (
                    i * 47 +
                    worldTime * 700
                ) % HEIGHT;

            ctx.beginPath();

            ctx.moveTo(
                x,
                y
            );

            ctx.lineTo(
                x - 5,
                y + 18
            );

            ctx.stroke();

        }

    }


    if (weather === "fog") {

        ctx.fillStyle =
            "rgba(180,185,180,.10)";

        ctx.fillRect(
            0,
            300,
            WIDTH,
            320
        );

    }


    // Flashlight

    if (player.flashlight) {

        const px =
            player.x -
            cameraX +
            15;

        const py =
            player.y +
            25;

        const direction =
            mouse.x > px
                ? 1
                : -1;

        const gradient =
            ctx.createRadialGradient(
                px,
                py,
                20,
                px + direction * 180,
                py,
                260
            );

        gradient.addColorStop(
            0,
            "rgba(255,245,190,.28)"
        );

        gradient.addColorStop(
            1,
            "rgba(255,245,190,0)"
        );

        ctx.fillStyle =
            gradient;

        ctx.fillRect(
            0,
            0,
            WIDTH,
            HEIGHT
        );

    }


    drawHUD();

}


// ------------------------------------------------------------
// PLAYER DRAW
// ------------------------------------------------------------

function drawPlayer(x, y) {

    ctx.save();

    ctx.translate(
        x,
        y
    );


    // body

    ctx.fillStyle =
        player.invulnerable > 0
            ? "#eee"
            : "#b8b6ad";

    ctx.fillRect(
        5,
        8,
        20,
        25
    );


    // head

    ctx.fillStyle =
        "#d2ad8a";

    ctx.fillRect(
        7,
        0,
        16,
        17
    );


    // hair

    ctx.fillStyle =
        "#292b2b";

    ctx.fillRect(
        5,
        0,
        20,
        5
    );


    // legs

    ctx.fillStyle =
        "#343936";

    ctx.fillRect(
        4,
        33,
        9,
        29
    );

    ctx.fillRect(
        18,
        33,
        9,
        29
    );


    // arm + gun

    const direction =
        mouse.x > x
            ? 1
            : -1;

    ctx.fillStyle =
        "#c3a080";

    ctx.fillRect(
        direction > 0
            ? 24
            : -7,
        15,
        13,
        7
    );


    ctx.fillStyle =
        "#222";

    ctx.fillRect(
        direction > 0
            ? 31
            : -15,
        14,
        18,
        5
    );


    ctx.restore();

}


// ------------------------------------------------------------
// ZOMBIE DRAW
// ------------------------------------------------------------

function drawZombie(
    x,
    y,
    zombie
) {

    ctx.save();

    ctx.translate(
        x,
        y
    );


    ctx.fillStyle =
        zombie.hitFlash > 0
            ? "#eee"
            : zombie.type === "brute"
                ? "#513b39"
                : "#59645a";


    ctx.fillRect(
        5,
        10,
        25,
        42
    );


    ctx.fillStyle =
        "#777d6b";

    ctx.fillRect(
        8,
        0,
        20,
        20
    );


    ctx.fillStyle =
        "#111";

    ctx.fillRect(
        11,
        7,
        4,
        4
    );

    ctx.fillRect(
        21,
        7,
        4,
        4
    );


    ctx.fillStyle =
        "#31352f";

    ctx.fillRect(
        4,
        52,
        9,
        13
    );

    ctx.fillRect(
        21,
        52,
        9,
        13
    );


    ctx.restore();

}


// ------------------------------------------------------------
// HUD
// ------------------------------------------------------------

function drawHUD() {

    ctx.fillStyle =
        "rgba(5,7,7,.82)";

    ctx.fillRect(
        18,
        18,
        330,
        112
    );


    ctx.fillStyle =
        "#eee";

    ctx.font =
        "18px monospace";

    ctx.fillText(
        selectedCharacter.toUpperCase(),
        32,
        42
    );


    drawBar(
        32,
        52,
        140,
        14,
        player.health,
        100,
        "#b83d3d"
    );

    ctx.fillStyle =
        "#fff";

    ctx.fillText(
        "HP",
        178,
        65
    );


    drawBar(
        32,
        78,
        140,
        14,
        player.sanity,
        100,
        "#8c6ab0"
    );

    ctx.fillText(
        "SANITY",
        178,
        91
    );


    ctx.fillText(
        "AMMO " +
        player.ammo +
        "/" +
        player.reserveAmmo,
        32,
        115
    );


    ctx.fillText(
        "KILLS " +
        player.kills,
        178,
        115
    );


    // Objective panel

    ctx.fillStyle =
        "rgba(5,7,7,.82)";

    ctx.fillRect(
        370,
        18,
        600,
        55
    );


    ctx.fillStyle =
        "#d6c27b";

    ctx.fillText(
        "OBJECTIVE",
        390,
        39
    );


    ctx.fillStyle =
        "#eee";

    ctx.fillText(
        objective,
        390,
        60
    );


    // Message

    if (message && messageTimer > 0) {

        ctx.fillStyle =
            "rgba(0,0,0,.78)";

        ctx.fillRect(
            300,
            635,
            680,
            45
        );

        ctx.fillStyle =
            "#eee";

        ctx.textAlign =
            "center";

        ctx.fillText(
            message,
            640,
            663
        );

        ctx.textAlign =
            "left";

    }


    ctx.fillStyle =
        "#999";

    ctx.fillText(
        "F flashlight  E interact  R reload  Q melee  P pause",
        20,
        700
    );


    if (paused) {

        ctx.fillStyle =
            "rgba(0,0,0,.72)";

        ctx.fillRect(
            0,
            0,
            WIDTH,
            HEIGHT
        );

        ctx.fillStyle =
            "#eee";

        ctx.font =
            "50px monospace";

        ctx.textAlign =
            "center";

        ctx.fillText(
            "PAUSED",
            640,
            320
        );

        ctx.font =
            "18px monospace";

        ctx.fillText(
            "Press P or ESC to continue",
            640,
            355
        );

        ctx.textAlign =
            "left";

    }


    if (gameOver) {

        ctx.fillStyle =
            "rgba(0,0,0,.85)";

        ctx.fillRect(
            0,
            0,
            WIDTH,
            HEIGHT
        );

        ctx.fillStyle =
            "#c44";

        ctx.font =
            "60px monospace";

        ctx.textAlign =
            "center";

        ctx.fillText(
            player.health <= 0
                ? "YOU DIED"
                : "YOUR MIND BROKE",
            640,
            310
        );

        ctx.fillStyle =
            "#eee";

        ctx.font =
            "18px monospace";

        ctx.fillText(
            "Refresh the page to restart.",
            640,
            350
        );

        ctx.textAlign =
            "left";

    }

}


function drawBar(
    x,
    y,
    width,
    height,
    value,
    maximum,
    color
) {

    ctx.fillStyle =
        "#222";

    ctx.fillRect(
        x,
        y,
        width,
        height
    );


    ctx.fillStyle =
        color;

    ctx.fillRect(
        x + 2,
        y + 2,
        (
            width - 4
        ) *
        clamp(
            value / maximum,
            0,
            1
        ),
        height - 4
    );

}


// ------------------------------------------------------------
// GAME LOOP
// ------------------------------------------------------------

let lastTime = 0;

function gameLoop(timestamp) {

    const delta =
        Math.min(
            .033,
            (timestamp - lastTime) / 1000
        );

    lastTime = timestamp;

    update(delta);

    updateSmiler(delta);

    draw();

    requestAnimationFrame(
        gameLoop
    );

}

requestAnimationFrame(
    gameLoop
);

</script>

</body>
</html>
"""


@app.route("/")
def index():
    return Response(
        GAME_HTML,
        mimetype="text/html"
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "game": "Ashes of the Dead",
        "version": "Browser 2.0"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
