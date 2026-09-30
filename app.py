"""
ASHES OF THE DEAD
Advanced 2D WW2 Zombie Survival Game Prototype
Single-file Pygame application.

Features:
- Main menu / pause / game-over screens
- Side-view platform movement
- Camera and parallax world
- Multiple zones
- Procedural environmental decoration
- Zombies with multiple AI archetypes
- Boss encounter
- Weapons, reloads, melee, grenades
- Inventory and loot
- Chests and interactables
- Health/stamina/hunger
- XP, levels and skill points
- Quest system
- Dialogue
- Safehouse
- Crafting
- Save/load
- Minimap
- Day/night cycle
- Weather
- Particles
- Damage numbers
- Screen shake
- Sound hooks
- Settings
- Debug overlay
- Respawn/checkpoint
- Story progression

Controls:
A/D or arrows  - move
W/Space        - jump
Left mouse     - shoot
Right mouse    - aim/flashlight
R              - reload
F              - flashlight
E              - interact
G              - grenade
Q              - melee
1/2/3/4        - weapon slot
I              - inventory
K              - skills
J              - quests
M              - map
C              - crafting
P/ESC          - pause
F5             - save
F9             - load
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pygame

# ============================================================
# CONFIGURATION
# ============================================================

pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass

WIDTH = 1280
HEIGHT = 720
FPS = 60

WORLD_WIDTH = 18000
GROUND_Y = 600
GRAVITY = 1550.0
PLAYER_SPEED = 290.0
JUMP_SPEED = -650.0

TITLE = "Ashes of the Dead"
VERSION = "0.9.0 Advanced Prototype"

ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets"
SAVE_DIR = ROOT / "saves"
SAVE_DIR.mkdir(exist_ok=True)

SAVE_FILE = SAVE_DIR / "savegame.json"

# ============================================================
# COLORS
# ============================================================

BLACK = (8, 9, 9)
WHITE = (240, 240, 232)
OFFWHITE = (218, 216, 204)
RED = (190, 55, 55)
DARK_RED = (105, 30, 30)
GREEN = (78, 170, 95)
YELLOW = (220, 185, 70)
BLUE = (80, 130, 200)
GREY = (105, 108, 105)
DARK_GREY = (43, 45, 43)
BROWN = (100, 72, 47)
DARK_BROWN = (57, 42, 30)
METAL = (82, 89, 88)
PURPLE = (130, 80, 160)
ORANGE = (205, 125, 45)

# ============================================================
# DISPLAY / FONTS
# ============================================================

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"{TITLE} - {VERSION}")
clock = pygame.time.Clock()

FONT_TINY = pygame.font.Font(None, 18)
FONT_SMALL = pygame.font.Font(None, 24)
FONT = pygame.font.Font(None, 30)
FONT_MED = pygame.font.Font(None, 38)
FONT_BIG = pygame.font.Font(None, 58)
FONT_TITLE = pygame.font.Font(None, 86)

# ============================================================
# UTILITIES
# ============================================================

def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def lerp(a, b, t):
    return a + (b - a) * t


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def sign(v):
    if v < 0:
        return -1
    if v > 0:
        return 1
    return 0


def world_to_screen(x, camera_x):
    return int(x - camera_x)


def draw_text(surface, value, x, y, font=FONT, color=WHITE, center=False):
    img = font.render(str(value), True, color)
    rect = img.get_rect()
    if center:
        rect.center = (int(x), int(y))
    else:
        rect.topleft = (int(x), int(y))
    surface.blit(img, rect)
    return rect


def draw_panel(surface, rect, alpha=210, border=True):
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    panel.fill((12, 15, 14, alpha))
    surface.blit(panel, rect.topleft)
    if border:
        pygame.draw.rect(surface, (105, 110, 101), rect, 2, border_radius=8)


def draw_bar(surface, rect, value, maximum, fill_color, back=(28, 30, 28)):
    pygame.draw.rect(surface, back, rect, border_radius=5)
    ratio = 0 if maximum <= 0 else clamp(value / maximum, 0, 1)
    inner = rect.copy()
    inner.width = int((rect.width - 4) * ratio)
    inner.x += 2
    inner.y += 2
    inner.height -= 4
    if inner.width > 0:
        pygame.draw.rect(surface, fill_color, inner, border_radius=4)


def safe_load_image(path: Path, size=None):
    if not path.exists():
        return None
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.smoothscale(image, size)
        return image
    except pygame.error:
        return None


# ============================================================
# ENUM-LIKE CONSTANTS
# ============================================================

GAME_MENU = "menu"
GAME_PLAYING = "playing"
GAME_PAUSED = "paused"
GAME_INVENTORY = "inventory"
GAME_SKILLS = "skills"
GAME_QUESTS = "quests"
GAME_MAP = "map"
GAME_CRAFTING = "crafting"
GAME_DIALOGUE = "dialogue"
GAME_GAMEOVER = "gameover"
GAME_VICTORY = "victory"

WEAPON_PISTOL = "pistol"
WEAPON_RIFLE = "rifle"
WEAPON_SMG = "smg"
WEAPON_SHOTGUN = "shotgun"
WEAPON_AXE = "axe"
WEAPON_GRENADE = "grenade"

# ============================================================
# DATA DEFINITIONS
# ============================================================

@dataclass
class WeaponDefinition:
    name: str
    slot: int
    damage: float
    fire_rate: float
    magazine: int
    reload_time: float
    spread: float
    pellets: int = 1
    automatic: bool = False
    ammo_type: str = "9mm"
    range: float = 1100.0
    melee: bool = False


WEAPONS: Dict[str, WeaponDefinition] = {
    WEAPON_PISTOL: WeaponDefinition(
        "M1935 Pistol", 1, 30, 0.22, 8, 1.05, 0.035, ammo_type="9mm"
    ),
    WEAPON_RIFLE: WeaponDefinition(
        "Bolt Rifle", 2, 78, 0.95, 5, 1.55, 0.012, ammo_type="rifle"
    ),
    WEAPON_SMG: WeaponDefinition(
        "WW2 SMG", 3, 24, 0.085, 32, 1.75, 0.075, automatic=True, ammo_type="9mm"
    ),
    WEAPON_SHOTGUN: WeaponDefinition(
        "Trench Shotgun", 4, 28, 0.85, 5, 1.8, 0.12, pellets=7, ammo_type="shell"
    ),
    WEAPON_AXE: WeaponDefinition(
        "Field Axe", 5, 70, 0.65, 1, 0.0, 0.0, melee=True
    ),
}


@dataclass
class Item:
    item_id: str
    name: str
    amount: int = 1


ITEM_NAMES = {
    "bandage": "Bandage",
    "medkit": "Medical Kit",
    "food": "Canned Food",
    "scrap": "Scrap Metal",
    "cloth": "Cloth",
    "wood": "Wood",
    "fuel": "Fuel",
    "gunpowder": "Gunpowder",
    "ammo_9mm": "9mm Ammunition",
    "ammo_rifle": "Rifle Ammunition",
    "ammo_shell": "Shotgun Shells",
    "key": "Rusty Key",
    "eclipse": "Eclipse Fragment",
    "flare": "Signal Flare",
}


@dataclass
class Quest:
    quest_id: str
    title: str
    description: str
    target: str
    required: int
    progress: int = 0
    reward_xp: int = 100
    reward_items: Dict[str, int] = field(default_factory=dict)
    completed: bool = False
    claimed: bool = False

    def update(self, target, amount=1):
        if self.completed:
            return
        if self.target == target:
            self.progress += amount
            if self.progress >= self.required:
                self.progress = self.required
                self.completed = True


@dataclass
class Skill:
    skill_id: str
    name: str
    description: str
    level: int = 0
    maximum: int = 5


SKILLS = {
    "survivor": Skill(
        "survivor", "Survivor", "+5 maximum health per level."
    ),
    "marksman": Skill(
        "marksman", "Marksman", "+6% firearm damage per level."
    ),
    "scavenger": Skill(
        "scavenger", "Scavenger", "Improves chest and loot rewards."
    ),
    "runner": Skill(
        "runner", "Runner", "+4% movement speed per level."
    ),
    "medic": Skill(
        "medic", "Field Medic", "+8% healing effectiveness per level."
    ),
}


@dataclass
class WeatherState:
    kind: str = "clear"
    timer: float = 45.0


@dataclass
class Message:
    text: str
    timer: float
    color: Tuple[int, int, int] = WHITE


# ============================================================
# PARTICLES
# ============================================================

class Particle:
    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        color,
        life=0.7,
        size=4,
        gravity=0.0,
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = gravity

    def update(self, dt):
        self.life -= dt
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface, camera_x):
        if self.life <= 0:
            return
        alpha = int(255 * clamp(self.life / self.max_life, 0, 1))
        radius = max(1, int(self.size * self.life / self.max_life))
        layer = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(
            layer,
            (*self.color, alpha),
            (radius * 2, radius * 2),
            radius,
        )
        surface.blit(
            layer,
            (
                int(self.x - camera_x - radius * 2),
                int(self.y - radius * 2),
            ),
        )


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []

    def burst(self, x, y, color, count=12, speed=150, life=0.7):
        for _ in range(count):
            angle = random.random() * math.tau
            velocity = random.uniform(speed * 0.3, speed)
            self.particles.append(
                Particle(
                    x,
                    y,
                    math.cos(angle) * velocity,
                    math.sin(angle) * velocity,
                    color,
                    random.uniform(life * 0.5, life),
                    random.randint(2, 5),
                    150,
                )
            )

    def blood(self, x, y):
        self.burst(x, y, (165, 35, 35), 10, 130, 0.55)

    def dust(self, x, y):
        self.burst(x, y, (130, 120, 100), 8, 75, 0.8)

    def update(self, dt):
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self, surface, camera_x):
        for particle in self.particles:
            particle.draw(surface, camera_x)


# ============================================================
# DAMAGE NUMBERS
# ============================================================

class FloatingText:
    def __init__(self, x, y, value, color=WHITE):
        self.x = x
        self.y = y
        self.value = value
        self.color = color
        self.life = 0.85

    def update(self, dt):
        self.life -= dt
        self.y -= 38 * dt

    def draw(self, surface, camera_x):
        if self.life <= 0:
            return
        draw_text(
            surface,
            self.value,
            self.x - camera_x,
            self.y,
            FONT_SMALL,
            self.color,
            True,
        )


# ============================================================
# PROJECTILES
# ============================================================

class Projectile:
    def __init__(self, x, y, dx, dy, damage, owner, speed=1200, color=YELLOW):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.owner = owner
        self.speed = speed
        self.life = 1.8
        self.color = color
        self.radius = 3

    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt
        self.life -= dt

    def draw(self, surface, camera_x):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x - camera_x), int(self.y)),
            self.radius,
        )


# ============================================================
# WORLD OBJECTS
# ============================================================

class WorldObject:
    def __init__(self, x, y, w, h, kind):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.kind = kind
        self.solid = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

    def draw(self, surface, camera_x):
        r = self.rect.move(-int(camera_x), 0)
        if self.kind == "crate":
            pygame.draw.rect(surface, BROWN, r)
            pygame.draw.rect(surface, DARK_BROWN, r, 3)
            pygame.draw.line(surface, DARK_BROWN, r.topleft, r.bottomright, 3)
            pygame.draw.line(surface, DARK_BROWN, r.topright, r.bottomleft, 3)
        elif self.kind == "barrel":
            pygame.draw.ellipse(surface, METAL, r)
            pygame.draw.rect(surface, DARK_GREY, (r.x, r.y + 8, r.w, r.h - 16))
            pygame.draw.line(surface, BLACK, (r.x, r.centery), (r.right, r.centery), 3)
        elif self.kind == "sandbags":
            for row in range(2):
                for i in range(4):
                    bx = r.x + i * 32 + (row * 12)
                    by = r.bottom - 30 - row * 22
                    pygame.draw.ellipse(surface, (135, 118, 84), (bx, by, 45, 28))
        elif self.kind == "wreck":
            pygame.draw.polygon(
                surface,
                (65, 70, 67),
                [
                    (r.left, r.bottom),
                    (r.left + 18, r.top + 25),
                    (r.centerx, r.top),
                    (r.right - 15, r.top + 18),
                    (r.right, r.bottom),
                ],
            )
            pygame.draw.circle(surface, BLACK, (r.left + 30, r.bottom - 6), 18)
            pygame.draw.circle(surface, BLACK, (r.right - 30, r.bottom - 6), 18)


class Chest(WorldObject):
    def __init__(self, x, rare=False):
        super().__init__(x, GROUND_Y - 45, 68, 45, "chest")
        self.rare = rare
        self.opened = False

    def interact(self, game):
        if self.opened:
            game.notify("This chest has already been searched.", GREY)
            return

        self.opened = True
        game.quest_event("open_chest")

        bonus = 1 + game.player.skills["scavenger"].level * 0.12
        ammo = int((20 if self.rare else 9) * bonus)

        game.player.add_item("ammo_9mm", ammo)
        game.player.add_item("bandage", 2 if self.rare else 1)
        game.player.add_item("scrap", 5 if self.rare else 2)

        if self.rare:
            game.player.add_item("medkit", 1)
            game.player.xp += 75
            game.notify("RARE MILITARY CACHE: supplies recovered!", YELLOW)
        else:
            game.player.xp += 25
            game.notify("Supply chest searched.", GREEN)

    def draw(self, surface, camera_x):
        r = self.rect.move(-int(camera_x), 0)
        color = PURPLE if self.rare else BROWN
        pygame.draw.rect(surface, color, r, border_radius=5)
        pygame.draw.rect(surface, DARK_BROWN, r, 3, border_radius=5)

        if self.opened:
            pygame.draw.line(surface, DARK_BROWN, (r.left, r.top), (r.right, r.bottom), 3)
        else:
            pygame.draw.rect(
                surface,
                YELLOW,
                (r.centerx - 4, r.centery - 4, 8, 8),
            )


# ============================================================
# PLAYER
# ============================================================

class Player:
    def __init__(self):
        self.w = 58
        self.h = 108
        self.x = 230.0
        self.y = GROUND_Y - self.h
        self.vx = 0
        self.vy = 0
        self.facing = 1
        self.on_ground = True

        self.max_hp = 100
        self.hp = 100
        self.stamina = 100
        self.max_stamina = 100
        self.hunger = 100

        self.level = 1
        self.xp = 0
        self.next_xp = 250
        self.skill_points = 0

        self.inventory: Dict[str, int] = {
            "bandage": 2,
            "food": 2,
            "scrap": 8,
            "cloth": 4,
            "wood": 5,
            "ammo_9mm": 40,
            "ammo_rifle": 15,
            "ammo_shell": 8,
            "fuel": 2,
        }

        self.weapons = {
            WEAPON_PISTOL: {"owned": True, "ammo": 8},
            WEAPON_RIFLE: {"owned": False, "ammo": 0},
            WEAPON_SMG: {"owned": False, "ammo": 0},
            WEAPON_SHOTGUN: {"owned": False, "ammo": 0},
            WEAPON_AXE: {"owned": True, "ammo": 1},
        }

        self.weapon = WEAPON_PISTOL
        self.fire_timer = 0
        self.reload_timer = 0
        self.invulnerability = 0
        self.attack_timer = 0
        self.grenades = 2

        self.flashlight = False
        self.aiming = False

        self.sprite = safe_load_image(ASSET_DIR / "player.png")

        if self.sprite:
            ratio = self.h / max(1, self.sprite.get_height())
            self.sprite = pygame.transform.smoothscale(
                self.sprite,
                (
                    max(1, int(self.sprite.get_width() * ratio)),
                    self.h,
                ),
            )
            self.w = self.sprite.get_width()

        self.skills = {
            key: Skill(
                skill.skill_id,
                skill.name,
                skill.description,
                skill.level,
                skill.maximum,
            )
            for key, skill in SKILLS.items()
        }

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            int(self.w),
            int(self.h),
        )

    @property
    def center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def speed_multiplier(self):
        return 1 + self.skills["runner"].level * 0.04

    def damage_multiplier(self):
        return 1 + self.skills["marksman"].level * 0.06

    def heal_multiplier(self):
        return 1 + self.skills["medic"].level * 0.08

    def add_item(self, item_id, amount):
        self.inventory[item_id] = self.inventory.get(item_id, 0) + amount

    def remove_item(self, item_id, amount):
        current = self.inventory.get(item_id, 0)
        if current < amount:
            return False
        self.inventory[item_id] = current - amount
        return True

    def has_item(self, item_id, amount=1):
        return self.inventory.get(item_id, 0) >= amount

    def current_weapon(self):
        return WEAPONS[self.weapon]

    def switch_weapon(self, weapon_id):
        definition = WEAPONS.get(weapon_id)
        if not definition:
            return False
        if not self.weapons.get(weapon_id, {}).get("owned", False):
            return False
        self.weapon = weapon_id
        self.reload_timer = 0
        self.fire_timer = 0
        return True

    def unlock_weapon(self, weapon_id, ammo=0):
        if weapon_id in self.weapons:
            self.weapons[weapon_id]["owned"] = True
            self.weapons[weapon_id]["ammo"] += ammo
        else:
            self.weapons[weapon_id] = {"owned": True, "ammo": ammo}

    def receive_damage(self, amount, game):
        if self.invulnerability > 0:
            return

        self.hp -= amount
        self.invulnerability = 0.65
        game.screen_shake = max(game.screen_shake, 8)
        game.particles.blood(self.center[0], self.y + 50)
        game.notify(f"-{int(amount)} health", RED)

        if self.hp <= 0:
            self.hp = 0
            game.state = GAME_GAMEOVER

    def gain_xp(self, amount, game):
        self.xp += amount

        while self.xp >= self.next_xp:
            self.xp -= self.next_xp
            self.level += 1
            self.skill_points += 1
            self.next_xp = int(self.next_xp * 1.35)
            self.max_hp += 5
            self.hp = self.max_hp
            game.notify(
                f"LEVEL UP! You are now level {self.level}. Skill point gained.",
                YELLOW,
            )

    def use_bandage(self, game):
        if self.has_item("bandage") and self.hp < self.max_hp:
            self.remove_item("bandage", 1)
            amount = int(25 * self.heal_multiplier())
            self.hp = min(self.max_hp, self.hp + amount)
            game.notify(f"Bandaged +{amount} HP", GREEN)
            return True
        return False

    def use_medkit(self, game):
        if self.has_item("medkit") and self.hp < self.max_hp:
            self.remove_item("medkit", 1)
            amount = int(65 * self.heal_multiplier())
            self.hp = min(self.max_hp, self.hp + amount)
            game.notify(f"Medical kit +{amount} HP", GREEN)
            return True
        return False

    def eat(self, game):
        if self.has_item("food"):
            self.remove_item("food", 1)
            self.hunger = min(100, self.hunger + 35)
            self.stamina = min(100, self.stamina + 25)
            game.notify("You ate canned food.", GREEN)
            return True
        return False

    def update(self, game, dt):
        self.fire_timer = max(0, self.fire_timer - dt)
        self.reload_timer = max(0, self.reload_timer - dt)
        self.invulnerability = max(0, self.invulnerability - dt)
        self.attack_timer = max(0, self.attack_timer - dt)

        keys = pygame.key.get_pressed()

        movement = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement += 1

        speed = PLAYER_SPEED * self.speed_multiplier()

        if self.stamina < 20:
            speed *= 0.82

        self.vx = movement * speed

        if movement:
            self.facing = movement

        jump = keys[pygame.K_w] or keys[pygame.K_SPACE]
        if jump and self.on_ground:
            self.vy = JUMP_SPEED
            self.on_ground = False
            game.particles.dust(self.x + self.w / 2, GROUND_Y)

        self.vy += GRAVITY * dt

        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt

        # Basic world bounds.
        self.x = clamp(new_x, 0, WORLD_WIDTH - self.w)
        self.y = new_y

        if self.y + self.h >= GROUND_Y:
            self.y = GROUND_Y - self.h
            self.vy = 0
            self.on_ground = True

        if movement and not self.on_ground:
            self.stamina = max(0, self.stamina - 2 * dt)
        else:
            self.stamina = min(self.max_stamina, self.stamina + 8 * dt)

        self.hunger -= 0.45 * dt
        if self.hunger <= 0:
            self.hunger = 0
            self.hp -= 1.5 * dt

    def reload(self, game):
        definition = self.current_weapon()
        if definition.melee:
            return

        if self.reload_timer > 0:
            return

        current = self.weapons[self.weapon]["ammo"]
        if current >= definition.magazine:
            return

        ammo_key = {
            "9mm": "ammo_9mm",
            "rifle": "ammo_rifle",
            "shell": "ammo_shell",
        }[definition.ammo_type]

        available = self.inventory.get(ammo_key, 0)
        needed = definition.magazine - current

        if available <= 0:
            game.notify("No ammunition for this weapon.", RED)
            return

        take = min(needed, available)
        self.inventory[ammo_key] -= take
        self.weapons[self.weapon]["ammo"] += take
        self.reload_timer = definition.reload_time
        game.notify("Reloading...", OFFWHITE)

    def shoot(self, game, target_x, target_y):
        definition = self.current_weapon()

        if definition.melee:
            self.melee_attack(game)
            return

        if self.reload_timer > 0:
            return

        if self.fire_timer > 0:
            return

        current = self.weapons[self.weapon]["ammo"]

        if current <= 0:
            game.notify("Empty magazine. Press R to reload.", RED)
            self.reload(game)
            return

        self.weapons[self.weapon]["ammo"] -= 1
        self.fire_timer = definition.fire_rate

        origin_x = self.x + self.w / 2 + self.facing * 25
        origin_y = self.y + self.h * 0.43

        base_dx = target_x - origin_x
        base_dy = target_y - origin_y
        length = max(1, math.hypot(base_dx, base_dy))
        base_angle = math.atan2(base_dy, base_dx)

        for _ in range(definition.pellets):
            angle = base_angle + random.uniform(
                -definition.spread,
                definition.spread,
            )

            dx = math.cos(angle)
            dy = math.sin(angle)

            damage = definition.damage * self.damage_multiplier()
            game.projectiles.append(
                Projectile(
                    origin_x,
                    origin_y,
                    dx,
                    dy,
                    damage,
                    "player",
                    definition.range,
                )
            )

        game.muzzle_flash = 0.06
        game.screen_shake = max(game.screen_shake, 3)

    def melee_attack(self, game):
        if self.attack_timer > 0:
            return

        self.attack_timer = 0.55

        attack_rect = pygame.Rect(
            int(self.x + (self.w if self.facing > 0 else -75)),
            int(self.y + 30),
            75,
            60,
        )

        for enemy in game.enemies:
            if enemy.dead:
                continue
            if attack_rect.colliderect(enemy.rect):
                damage = 70 * self.damage_multiplier()
                enemy.take_damage(damage, game)
                game.particles.blood(enemy.x, enemy.y + enemy.h / 2)

        game.screen_shake = max(game.screen_shake, 5)

    def throw_grenade(self, game, target_x, target_y):
        if self.grenades <= 0:
            game.notify("No grenades.", RED)
            return

        self.grenades -= 1
        ox = self.x + self.w / 2
        oy = self.y + 35

        dx = target_x - ox
        dy = target_y - oy
        length = max(1, math.hypot(dx, dy))

        game.grenades_projectiles.append(
            Grenade(
                ox,
                oy,
                dx / length * 460,
                dy / length * 460,
            )
        )

    def draw(self, surface, camera_x):
        r = self.rect.move(-int(camera_x), 0)

        if self.sprite:
            sprite = self.sprite
            if self.facing < 0:
                sprite = pygame.transform.flip(sprite, True, False)

            if self.invulnerability > 0:
                sprite = sprite.copy()
                sprite.set_alpha(
                    150 if int(self.invulnerability * 10) % 2 == 0 else 255
                )

            surface.blit(sprite, r.topleft)
        else:
            # Fallback if the character image is unavailable.
            pygame.draw.ellipse(
                surface,
                (70, 50, 40),
                (r.x + 12, r.y, 36, 36),
            )
            pygame.draw.rect(
                surface,
                OFFWHITE,
                (r.x + 7, r.y + 30, 46, 64),
                border_radius=8,
            )
            pygame.draw.line(
                surface,
                DARK_GREY,
                (r.centerx, r.y + 88),
                (r.centerx - 12, r.bottom),
                6,
            )
            pygame.draw.line(
                surface,
                DARK_GREY,
                (r.centerx + 8, r.y + 88),
                (r.centerx + 17, r.bottom),
                6,
            )

        # Weapon visual.
        if not self.current_weapon().melee:
            gx = r.centerx + self.facing * 30
            gy = r.y + 54
            pygame.draw.line(
                surface,
                (35, 35, 33),
                (r.centerx, gy),
                (gx, gy),
                7,
            )

# ============================================================
# GRENADES
# ============================================================

class Grenade:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.timer = 1.8
        self.radius = 8

    def update(self, game, dt):
        self.timer -= dt
        self.vy += GRAVITY * 0.55 * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.y >= GROUND_Y - 10:
            self.y = GROUND_Y - 10
            self.vy *= -0.35
            self.vx *= 0.65

        if self.timer <= 0:
            radius = 180
            for enemy in game.enemies:
                if enemy.dead:
                    continue

                d = dist(
                    (self.x, self.y),
                    (enemy.x + enemy.w / 2, enemy.y + enemy.h / 2),
                )

                if d < radius:
                    damage = 120 * (1 - d / radius)
                    enemy.take_damage(damage, game)

            game.particles.burst(
                self.x,
                self.y,
                ORANGE,
                55,
                360,
                1.1,
            )
            game.screen_shake = 18
            return False

        return True

    def draw(self, surface, camera_x):
        pygame.draw.circle(
            surface,
            (35, 40, 36),
            (int(self.x - camera_x), int(self.y)),
            self.radius,
        )


# ============================================================
# ZOMBIE AI
# ============================================================

class Zombie:
    ARCHETYPES = {
        "walker": {
            "hp": 65,
            "speed": 55,
            "damage": 9,
            "attack_range": 50,
            "attack_rate": 1.0,
            "size": (48, 86),
            "color": (100, 110, 82),
            "xp": 30,
        },
        "runner": {
            "hp": 48,
            "speed": 135,
            "damage": 13,
            "attack_range": 48,
            "attack_rate": 0.85,
            "size": (44, 84),
            "color": (132, 85, 75),
            "xp": 40,
        },
        "soldier": {
            "hp": 90,
            "speed": 75,
            "damage": 14,
            "attack_range": 55,
            "attack_rate": 0.95,
            "size": (52, 94),
            "color": (74, 92, 69),
            "xp": 55,
        },
        "brute": {
            "hp": 260,
            "speed": 38,
            "damage": 28,
            "attack_range": 75,
            "attack_rate": 1.25,
            "size": (76, 125),
            "color": (92, 66, 62),
            "xp": 120,
        },
        "screamer": {
            "hp": 80,
            "speed": 55,
            "damage": 6,
            "attack_range": 45,
            "attack_rate": 1.1,
            "size": (50, 95),
            "color": (100, 76, 115),
            "xp": 90,
        },
    }

    def __init__(self, x, archetype="walker", level=1):
        data = self.ARCHETYPES[archetype]

        self.archetype = archetype
        self.x = float(x)
        self.w, self.h = data["size"]
        self.y = GROUND_Y - self.h

        self.max_hp = data["hp"] * (1 + (level - 1) * 0.12)
        self.hp = self.max_hp

        self.speed = data["speed"] * (1 + (level - 1) * 0.025)
        self.damage = data["damage"] * (1 + (level - 1) * 0.08)

        self.attack_range = data["attack_range"]
        self.attack_rate = data["attack_rate"]

        self.attack_timer = random.uniform(0.1, 1.0)
        self.alert = False
        self.alert_timer = 0
        self.dead = False
        self.hit_flash = 0
        self.direction = -1
        self.xp_reward = int(data["xp"] * (1 + level * 0.08))

        self.scream_timer = random.uniform(5, 10)

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            int(self.w),
            int(self.h),
        )

    def take_damage(self, amount, game):
        if self.dead:
            return

        self.hp -= amount
        self.hit_flash = 0.1

        game.floating_texts.append(
            FloatingText(
                self.x + self.w / 2,
                self.y,
                str(int(amount)),
                YELLOW,
            )
        )

        if self.hp <= 0:
            self.dead = True
            game.player.gain_xp(self.xp_reward, game)
            game.quest_event("kill_zombie")
            game.particles.blood(
                self.x + self.w / 2,
                self.y + self.h / 2,
            )

            if random.random() < 0.14:
                game.drop_item(
                    self.x + self.w / 2,
                    self.y + self.h / 2,
                )

    def update(self, game, dt):
        if self.dead:
            return

        self.attack_timer = max(0, self.attack_timer - dt)
        self.hit_flash = max(0, self.hit_flash - dt)
        self.alert_timer = max(0, self.alert_timer - dt)

        player = game.player

        dx = player.x - self.x
        distance = abs(dx)

        if distance < 760:
            self.alert = True

        if not self.alert:
            return

        if dx != 0:
            self.direction = sign(dx)

        if distance > self.attack_range:
            self.x += self.direction * self.speed * dt
        else:
            if self.attack_timer <= 0:
                player.receive_damage(self.damage, game)
                self.attack_timer = self.attack_rate

        if self.archetype == "screamer":
            self.scream_timer -= dt
            if self.scream_timer <= 0 and distance < 900:
                self.scream_timer = random.uniform(7, 12)
                game.spawn_horde_near(self.x, 3)
                game.notify("A Screamer has attracted more undead!", RED)

        self.x = clamp(self.x, 0, WORLD_WIDTH - self.w)

    def draw(self, surface, camera_x):
        r = self.rect.move(-int(camera_x), 0)
        data = self.ARCHETYPES[self.archetype]

        body_color = data["color"]

        if self.hit_flash > 0:
            body_color = WHITE

        pygame.draw.ellipse(
            surface,
            body_color,
            (r.x + 4, r.y, r.w - 8, 35),
        )

        pygame.draw.rect(
            surface,
            body_color,
            (r.x + 8, r.y + 25, r.w - 16, r.h - 25),
            border_radius=8,
        )

        # Eyes.
        pygame.draw.circle(
            surface,
            (220, 45, 35),
            (r.x + r.w // 3, r.y + 15),
            3,
        )
        pygame.draw.circle(
            surface,
            (220, 45, 35),
            (r.x + 2 * r.w // 3, r.y + 15),
            3,
        )

        # Soldier helmet.
        if self.archetype == "soldier":
            pygame.draw.rect(
                surface,
                (65, 72, 54),
                (r.x + 2, r.y - 3, r.w - 4, 10),
                border_radius=3,
            )

        # Brute arm.
        if self.archetype == "brute":
            pygame.draw.line(
                surface,
                (58, 48, 44),
                (r.left, r.y + 50),
                (r.left - 25, r.y + 78),
                10,
            )

        # Screamer mouth.
        if self.archetype == "screamer":
            pygame.draw.ellipse(
                surface,
                BLACK,
                (r.centerx - 9, r.y + 20, 18, 15),
            )

        if self.hp < self.max_hp:
            draw_bar(
                surface,
                pygame.Rect(r.x, r.y - 13, r.w, 7),
                self.hp,
                self.max_hp,
                RED,
            )


class Boss(Zombie):
    def __init__(self, x):
        super().__init__(x, "brute", level=12)
        self.name = "THE WARDEN"
        self.max_hp = 1600
        self.hp = self.max_hp
        self.speed = 45
        self.damage = 45
        self.attack_rate = 1.4
        self.xp_reward = 900
        self.phase = 1
        self.special_timer = 4

    def update(self, game, dt):
        if self.dead:
            return

        super().update(game, dt)

        self.special_timer -= dt

        if self.hp < self.max_hp * 0.6:
            self.phase = 2

        if self.hp < self.max_hp * 0.25:
            self.phase = 3

        if self.special_timer <= 0:
            self.special_timer = max(2.0, 5.0 - self.phase)

            if self.phase >= 2:
                game.spawn_horde_near(self.x, 2 + self.phase)

            if self.phase >= 3:
                game.screen_shake = 14
                game.particles.burst(
                    self.x,
                    GROUND_Y - 20,
                    RED,
                    30,
                    250,
                    0.9,
                )

    def draw(self, surface, camera_x):
        super().draw(surface, camera_x)

        r = self.rect.move(-int(camera_x), 0)

        draw_text(
            surface,
            self.name,
            r.centerx,
            r.top - 38,
            FONT_SMALL,
            RED,
            True,
        )

        draw_bar(
            surface,
            pygame.Rect(
                WIDTH // 2 - 250,
                24,
                500,
                18,
            ),
            self.hp,
            self.max_hp,
            RED,
        )


# ============================================================
# DROPS
# ============================================================

class WorldDrop:
    def __init__(self, x, y, item_id, amount):
        self.x = x
        self.y = y
        self.item_id = item_id
        self.amount = amount
        self.life = 45

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - 15),
            int(self.y - 15),
            30,
            30,
        )

    def update(self, game, dt):
        self.life -= dt

        if self.life <= 0:
            return False

        if self.rect.colliderect(game.player.rect):
            game.player.add_item(self.item_id, self.amount)
            game.notify(
                f"+{self.amount} {ITEM_NAMES.get(self.item_id, self.item_id)}",
                GREEN,
            )
            return False

        return True

    def draw(self, surface, camera_x):
        sx = int(self.x - camera_x)
        sy = int(self.y)

        color = {
            "ammo_9mm": YELLOW,
            "ammo_rifle": YELLOW,
            "ammo_shell": ORANGE,
            "bandage": WHITE,
            "medkit": RED,
            "scrap": GREY,
            "fuel": ORANGE,
            "eclipse": PURPLE,
        }.get(self.item_id, GREEN)

        pygame.draw.circle(surface, color, (sx, sy), 9)
        draw_text(
            surface,
            ITEM_NAMES.get(self.item_id, self.item_id),
            sx,
            sy - 28,
            FONT_TINY,
            WHITE,
            True,
        )


# ============================================================
# QUEST SYSTEM
# ============================================================

class QuestSystem:
    def __init__(self):
        self.quests = [
            Quest(
                "escape",
                "Escape the Asylum",
                "Reach the first military checkpoint.",
                "reach_checkpoint",
                1,
                reward_xp=150,
                reward_items={"bandage": 2},
            ),
            Quest(
                "scavenge",
                "Scavenger",
                "Open 5 supply containers.",
                "open_chest",
                5,
                reward_xp=220,
                reward_items={"ammo_9mm": 25},
            ),
            Quest(
                "undead",
                "Clean the Streets",
                "Destroy 15 zombies.",
                "kill_zombie",
                15,
                reward_xp=400,
                reward_items={"ammo_rifle": 12},
            ),
            Quest(
                "eclipse",
                "Project Eclipse",
                "Recover 3 Eclipse fragments.",
                "collect_eclipse",
                3,
                reward_xp=750,
                reward_items={"medkit": 2},
            ),
        ]

    def event(self, target, amount=1):
        for quest in self.quests:
            quest.update(target, amount)

    def claim(self, quest, game):
        if not quest.completed or quest.claimed:
            return

        quest.claimed = True
        game.player.gain_xp(quest.reward_xp, game)

        for item, amount in quest.reward_items.items():
            game.player.add_item(item, amount)

        game.notify(
            f"Quest reward: +{quest.reward_xp} XP",
            YELLOW,
        )


# ============================================================
# CRAFTING
# ============================================================

@dataclass
class Recipe:
    recipe_id: str
    name: str
    description: str
    cost: Dict[str, int]
    result: Dict[str, int]


RECIPES = [
    Recipe(
        "bandage",
        "Bandage",
        "Basic emergency dressing.",
        {"cloth": 2},
        {"bandage": 1},
    ),
    Recipe(
        "medkit",
        "Medical Kit",
        "Improvised medical supplies.",
        {"cloth": 4, "scrap": 2},
        {"medkit": 1},
    ),
    Recipe(
        "ammo",
        "9mm Ammo",
        "A small ammunition batch.",
        {"scrap": 2, "gunpowder": 1},
        {"ammo_9mm": 12},
    ),
    Recipe(
        "shell",
        "Shotgun Shells",
        "Four improvised shells.",
        {"scrap": 3, "gunpowder": 2},
        {"ammo_shell": 4},
    ),
    Recipe(
        "flare",
        "Signal Flare",
        "Marks a location for survivors.",
        {"cloth": 1, "gunpowder": 2, "wood": 1},
        {"flare": 1},
    ),
]


# ============================================================
# SAFEHOUSE
# ============================================================

class Safehouse:
    def __init__(self):
        self.x = 850
        self.level = 1
        self.stash: Dict[str, int] = {}
        self.medical_upgrade = 0
        self.workbench_upgrade = 0

    def inside(self, player):
        return abs(player.x - self.x) < 230

    def upgrade_medical(self, player, game):
        cost = 8 + self.medical_upgrade * 6

        if player.has_item("scrap", cost):
            player.remove_item("scrap", cost)
            self.medical_upgrade += 1
            player.max_hp += 10
            player.hp = player.max_hp
            game.notify("Safehouse medical station upgraded.", GREEN)
        else:
            game.notify(f"Need {cost} scrap.", RED)

    def upgrade_workbench(self, player, game):
        cost = 10 + self.workbench_upgrade * 7

        if player.has_item("scrap", cost):
            player.remove_item("scrap", cost)
            self.workbench_upgrade += 1
            game.notify("Workbench upgraded.", GREEN)
        else:
            game.notify(f"Need {cost} scrap.", RED)

    def draw(self, surface, camera_x):
        sx = int(self.x - camera_x)

        pygame.draw.rect(
            surface,
            (72, 73, 67),
            (sx - 160, GROUND_Y - 200, 320, 200),
        )
        pygame.draw.polygon(
            surface,
            (45, 48, 44),
            [
                (sx - 185, GROUND_Y - 200),
                (sx, GROUND_Y - 285),
                (sx + 185, GROUND_Y - 200),
            ],
        )

        draw_text(
            surface,
            "SAFEHOUSE",
            sx,
            GROUND_Y - 235,
            FONT,
            YELLOW,
            True,
        )


# ============================================================
# DIALOGUE
# ============================================================

class DialogueSystem:
    def __init__(self):
        self.active = False
        self.speaker = ""
        self.lines: List[str] = []
        self.index = 0
        self.callback = None

    def start(self, speaker, lines, callback=None):
        self.active = True
        self.speaker = speaker
        self.lines = lines
        self.index = 0
        self.callback = callback

    def advance(self):
        if not self.active:
            return

        self.index += 1

        if self.index >= len(self.lines):
            self.active = False

            if self.callback:
                callback = self.callback
                self.callback = None
                callback()

    def draw(self, surface):
        if not self.active:
            return

        box = pygame.Rect(
            90,
            HEIGHT - 205,
            WIDTH - 180,
            155,
        )

        draw_panel(surface, box, 235)

        draw_text(
            surface,
            self.speaker,
            box.x + 25,
            box.y + 20,
            FONT_MED,
            YELLOW,
        )

        if self.lines:
            draw_text(
                surface,
                self.lines[self.index],
                box.x + 25,
                box.y + 70,
                FONT,
                WHITE,
            )

        draw_text(
            surface,
            "SPACE / ENTER — Continue",
            box.right - 245,
            box.bottom - 35,
            FONT_SMALL,
            GREY,
        )


# ============================================================
# WEATHER / DAY NIGHT
# ============================================================

class EnvironmentSystem:
    def __init__(self):
        self.time_of_day = 8.0
        self.weather = WeatherState()
        self.lightning = 0
        self.rain_particles = []

    def update(self, dt):
        self.time_of_day += dt * 0.08

        if self.time_of_day >= 24:
            self.time_of_day -= 24

        self.weather.timer -= dt

        if self.weather.timer <= 0:
            self.weather.kind = random.choice(
                ["clear", "clear", "fog", "rain", "storm"]
            )
            self.weather.timer = random.uniform(35, 75)

        if self.weather.kind in ("rain", "storm"):
            for _ in range(5 if self.weather.kind == "rain" else 9):
                self.rain_particles.append(
                    [
                        random.randint(0, WIDTH),
                        random.randint(0, HEIGHT),
                        random.randint(450, 750),
                    ]
                )

        for p in self.rain_particles[:]:
            p[1] += p[2] * dt

            if p[1] > HEIGHT:
                self.rain_particles.remove(p)

    def draw_overlay(self, surface):
        # Night darkness.
        hour = self.time_of_day

        if hour < 6 or hour > 19:
            darkness = 125
        elif hour < 8:
            darkness = int(125 * (8 - hour) / 2)
        elif hour > 17:
            darkness = int(125 * (hour - 17) / 2)
        else:
            darkness = 0

        if darkness:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((10, 15, 28, darkness))
            surface.blit(overlay, (0, 0))

        if self.weather.kind == "fog":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((190, 195, 188, 42))
            surface.blit(overlay, (0, 0))

        if self.weather.kind in ("rain", "storm"):
            for x, y, speed in self.rain_particles:
                pygame.draw.line(
                    surface,
                    (155, 180, 195),
                    (int(x), int(y)),
                    (int(x - 6), int(y + 15)),
                    1,
                )


# ============================================================
# WORLD / MAP
# ============================================================

@dataclass
class Zone:
    name: str
    start: float
    end: float
    description: str
    color: Tuple[int, int, int]


ZONES = [
    Zone(
        "Abandoned Asylum",
        0,
        1500,
        "Where the nightmare began.",
        (70, 75, 72),
    ),
    Zone(
        "Ruined Village",
        1500,
        3700,
        "A town abandoned in the middle of a war.",
        (86, 77, 62),
    ),
    Zone(
        "No Man's Land",
        3700,
        6800,
        "Trenches and infected soldiers.",
        (73, 70, 57),
    ),
    Zone(
        "Military Front",
        6800,
        10500,
        "A fortified war zone.",
        (62, 70, 64),
    ),
    Zone(
        "Dead City",
        10500,
        14000,
        "A city swallowed by the outbreak.",
        (65, 63, 66),
    ),
    Zone(
        "Project Eclipse",
        14000,
        WORLD_WIDTH,
        "The source of the infection.",
        (58, 55, 70),
    ),
]


class World:
    def __init__(self):
        self.objects: List[WorldObject] = []
        self.chests: List[Chest] = []
        self.zone_messages = set()
        self.generate()

    def generate(self):
        random.seed(1945)

        # Environmental props.
        for x in range(150, WORLD_WIDTH - 100, 210):
            roll = random.random()

            if roll < 0.20:
                self.objects.append(
                    WorldObject(
                        x,
                        GROUND_Y - 55,
                        70,
                        55,
                        "crate",
                    )
                )
            elif roll < 0.32:
                self.objects.append(
                    WorldObject(
                        x,
                        GROUND_Y - 65,
                        50,
                        65,
                        "barrel",
                    )
                )
            elif roll < 0.39:
                self.objects.append(
                    WorldObject(
                        x,
                        GROUND_Y - 55,
                        150,
                        55,
                        "sandbags",
                    )
                )
            elif roll < 0.44:
                self.objects.append(
                    WorldObject(
                        x,
                        GROUND_Y - 85,
                        180,
                        85,
                        "wreck",
                    )
                )

        # Chests.
        for x in range(450, WORLD_WIDTH - 400, 850):
            self.chests.append(
                Chest(
                    x,
                    rare=(random.random() < 0.23),
                )
            )

    def zone_at(self, x):
        for zone in ZONES:
            if zone.start <= x < zone.end:
                return zone
        return ZONES[-1]

    def draw_background(self, surface, camera_x, environment):
        zone = self.zone_at(camera_x + WIDTH / 2)

        # Sky.
        surface.fill(zone.color)

        # Far mountains / ruins.
        parallax = camera_x * 0.15

        for i in range(-2, 60):
            x = i * 330 - parallax
            height = 90 + ((i * 71) % 130)

            pygame.draw.polygon(
                surface,
                tuple(max(0, c - 18) for c in zone.color),
                [
                    (int(x), GROUND_Y),
                    (int(x + 150), GROUND_Y - height),
                    (int(x + 300), GROUND_Y),
                ],
            )

        # Ruined buildings.
        building_parallax = camera_x * 0.35

        for i in range(-3, 80):
            x = i * 270 - building_parallax
            height = 110 + ((i * 43) % 180)
            width = 170 + ((i * 29) % 90)

            pygame.draw.rect(
                surface,
                (54, 56, 53),
                (int(x), GROUND_Y - height, width, height),
            )

            for wy in range(
                int(GROUND_Y - height + 25),
                GROUND_Y - 20,
                48,
            ):
                pygame.draw.rect(
                    surface,
                    (28, 31, 29),
                    (int(x + 25), wy, 25, 28),
                )

        # Ground.
        pygame.draw.rect(
            surface,
            (72, 68, 56),
            (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y),
        )

        # Road.
        pygame.draw.rect(
            surface,
            (82, 78, 67),
            (0, GROUND_Y + 35, WIDTH, 85),
        )

        for x in range(-100, WIDTH + 100, 160):
            pygame.draw.rect(
                surface,
                (112, 104, 86),
                (x, GROUND_Y + 72, 75, 5),
            )

        # War details.
        for x in range(-50, WIDTH + 50, 230):
            pygame.draw.circle(
                surface,
                (55, 52, 44),
                (x, GROUND_Y + 22),
                12,
            )

        # Zone label.
        draw_panel(
            surface,
            pygame.Rect(
                WIDTH // 2 - 190,
                120,
                380,
                70,
            ),
            150,
            False,
        )

        draw_text(
            surface,
            zone.name,
            WIDTH // 2,
            143,
            FONT_MED,
            YELLOW,
            True,
        )

        draw_text(
            surface,
            zone.description,
            WIDTH // 2,
            171,
            FONT_SMALL,
            OFFWHITE,
            True,
        )

    def draw_objects(self, surface, camera_x):
        for obj in self.objects:
            if -200 < obj.x - camera_x < WIDTH + 200:
                obj.draw(surface, camera_x)

        for chest in self.chests:
            if -200 < chest.x - camera_x < WIDTH + 200:
                chest.draw(surface, camera_x)


# ============================================================
# GAME CLASS
# ============================================================

class Game:
    def __init__(self):
        self.state = GAME_MENU
        self.running = True

        self.player = Player()
        self.world = World()
        self.safehouse = Safehouse()

        self.enemies: List[Zombie] = []
        self.projectiles: List[Projectile] = []
        self.grenades_projectiles: List[Grenade] = []
        self.drops: List[WorldDrop] = []

        self.particles = ParticleSystem()
        self.floating_texts: List[FloatingText] = []
        self.messages: List[Message] = []

        self.quest_system = QuestSystem()
        self.dialogue = DialogueSystem()
        self.environment = EnvironmentSystem()

        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_target_x = 0.0

        self.screen_shake = 0.0
        self.muzzle_flash = 0.0

        self.spawn_timer = 2.0
        self.total_time = 0
        self.kills = 0

        self.minimap = True
        self.show_debug = False

        self.main_menu_selection = 0
        self.inventory_selection = 0
        self.skill_selection = 0
        self.quest_selection = 0
        self.crafting_selection = 0

        self.story_flags = {
            "checkpoint": False,
            "boss_spawned": False,
            "boss_defeated": False,
            "eclipse_started": False,
        }

        self.last_zone = self.world.zone_at(self.player.x).name

        self.initialize_world()

    # --------------------------------------------------------
    # Initialization
    # --------------------------------------------------------

    def initialize_world(self):
        self.spawn_initial_enemies()

    def spawn_initial_enemies(self):
        positions = [
            930,
            1120,
            1370,
            1680,
            1900,
            2150,
            2400,
            2780,
            3100,
            3450,
            3900,
            4300,
            4750,
            5200,
            5700,
            6200,
            6900,
            7500,
            8200,
            8900,
            9600,
            10300,
            11100,
            11800,
            12500,
            13200,
            13800,
        ]

        for x in positions:
            archetype = random.choices(
                ["walker", "runner", "soldier", "screamer"],
                [45, 20, 25, 10],
            )[0]

            level = max(1, int(x / 2200))
            self.enemies.append(
                Zombie(x, archetype, level)
            )

    # --------------------------------------------------------
    # Messaging
    # --------------------------------------------------------

    def notify(self, message, color=WHITE, duration=3):
        self.messages.append(
            Message(message, duration, color)
        )

        self.messages = self.messages[-6:]

    # --------------------------------------------------------
    # Quest Events
    # --------------------------------------------------------

    def quest_event(self, target, amount=1):
        self.quest_system.event(target, amount)

    # --------------------------------------------------------
    # Drops
    # --------------------------------------------------------

    def drop_item(self, x, y):
        choices = [
            ("ammo_9mm", random.randint(5, 14)),
            ("ammo_rifle", random.randint(3, 8)),
            ("scrap", random.randint(1, 5)),
            ("cloth", random.randint(1, 3)),
            ("food", 1),
            ("bandage", 1),
        ]

        item, amount = random.choice(choices)

        self.drops.append(
            WorldDrop(x, y, item, amount)
        )

    # --------------------------------------------------------
    # Enemy Spawning
    # --------------------------------------------------------

    def spawn_horde_near(self, x, count):
        for _ in range(count):
            spawn_x = x + random.choice(
                [-1, 1]
            ) * random.randint(300, 650)

            spawn_x = clamp(spawn_x, 0, WORLD_WIDTH - 100)

            archetype = random.choice(
                ["walker", "runner", "soldier"]
            )

            self.enemies.append(
                Zombie(
                    spawn_x,
                    archetype,
                    max(1, int(spawn_x / 2200)),
                )
            )

    def spawn_boss(self):
        if self.story_flags["boss_spawned"]:
            return

        self.story_flags["boss_spawned"] = True

        boss = Boss(15100)
        self.enemies.append(boss)

        self.notify(
            "WARNING: THE WARDEN HAS AWAKENED.",
            RED,
            6,
        )

    # --------------------------------------------------------
    # Story
    # --------------------------------------------------------

    def update_story(self):
        player_x = self.player.x

        if (
            not self.story_flags["checkpoint"]
            and player_x > 1450
        ):
            self.story_flags["checkpoint"] = True
            self.quest_event("reach_checkpoint")

            self.dialogue.start(
                "Mara",
                [
                    "You made it out of the asylum...",
                    "But this isn't a war anymore.",
                    "Whatever happened here changed everything.",
                    "Find the military radio. Someone may still be alive.",
                ],
            )

        if (
            player_x > 6800
            and not self.story_flags["eclipse_started"]
        ):
            self.story_flags["eclipse_started"] = True

            self.dialogue.start(
                "Unknown Radio",
                [
                    "If anyone can hear this...",
                    "Do not enter the Eclipse facility.",
                    "The dead are not the worst thing inside.",
                ],
            )

        if player_x > 14000:
            self.spawn_boss()

        if (
            self.story_flags["boss_spawned"]
            and not self.story_flags["boss_defeated"]
        ):
            if not any(
                isinstance(enemy, Boss) and not enemy.dead
                for enemy in self.enemies
            ):
                self.story_flags["boss_defeated"] = True
                self.state = GAME_VICTORY

    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if self.state == GAME_MENU:
            self.handle_menu_event(event)
            return

        if self.state == GAME_DIALOGUE:
            if event.type == pygame.KEYDOWN:
                if event.key in (
                    pygame.K_SPACE,
                    pygame.K_RETURN,
                    pygame.K_e,
                ):
                    self.dialogue.advance()
                    if not self.dialogue.active:
                        self.state = GAME_PLAYING
            return

        if self.state == GAME_GAMEOVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = GAME_MENU
            return

        if self.state == GAME_VICTORY:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = GAME_MENU
            return

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse(event)

    def handle_menu_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_DOWN, pygame.K_s):
            self.main_menu_selection = (
                self.main_menu_selection + 1
            ) % 4

        elif event.key in (pygame.K_UP, pygame.K_w):
            self.main_menu_selection = (
                self.main_menu_selection - 1
            ) % 4

        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.main_menu_selection == 0:
                self.new_game()

            elif self.main_menu_selection == 1:
                if SAVE_FILE.exists():
                    self.load_game()
                else:
                    self.notify("No save file found.", RED)

            elif self.main_menu_selection == 2:
                self.state = GAME_PLAYING
                self.notify(
                    "Demo mode started. Your progress will not be reset.",
                    YELLOW,
                )

            elif self.main_menu_selection == 3:
                self.running = False

    def handle_keydown(self, key):
        if key in (pygame.K_ESCAPE, pygame.K_p):
            if self.state == GAME_PLAYING:
                self.state = GAME_PAUSED
            elif self.state == GAME_PAUSED:
                self.state = GAME_PLAYING
            return

        if self.state == GAME_PAUSED:
            if key == pygame.K_F5:
                self.save_game()
            elif key == pygame.K_F9:
                self.load_game()
            return

        if key == pygame.K_F5:
            self.save_game()
            return

        if key == pygame.K_F9:
            self.load_game()
            return

        if key == pygame.K_F3:
            self.show_debug = not self.show_debug
            return

        if key == pygame.K_i:
            self.state = (
                GAME_PLAYING
                if self.state == GAME_INVENTORY
                else GAME_INVENTORY
            )
            return

        if key == pygame.K_k:
            self.state = (
                GAME_PLAYING
                if self.state == GAME_SKILLS
                else GAME_SKILLS
            )
            return

        if key == pygame.K_j:
            self.state = (
                GAME_PLAYING
                if self.state == GAME_QUESTS
                else GAME_QUESTS
            )
            return

        if key == pygame.K_m:
            self.state = (
                GAME_PLAYING
                if self.state == GAME_MAP
                else GAME_MAP
            )
            return

        if key == pygame.K_c:
            self.state = (
                GAME_PLAYING
                if self.state == GAME_CRAFTING
                else GAME_CRAFTING
            )
            return

        if self.state == GAME_INVENTORY:
            self.handle_inventory_key(key)
            return

        if self.state == GAME_SKILLS:
            self.handle_skill_key(key)
            return

        if self.state == GAME_QUESTS:
            self.handle_quest_key(key)
            return

        if self.state == GAME_CRAFTING:
            self.handle_crafting_key(key)
            return

        if key == pygame.K_r:
            self.player.reload(self)

        elif key == pygame.K_f:
            self.player.flashlight = not self.player.flashlight

        elif key == pygame.K_q:
            self.player.melee_attack(self)

        elif key == pygame.K_g:
            mx, my = pygame.mouse.get_pos()
            self.player.throw_grenade(
                self,
                mx + self.camera_x,
                my,
            )

        elif key == pygame.K_1:
            self.player.switch_weapon(WEAPON_PISTOL)

        elif key == pygame.K_2:
            self.player.switch_weapon(WEAPON_RIFLE)

        elif key == pygame.K_3:
            self.player.switch_weapon(WEAPON_SMG)

        elif key == pygame.K_4:
            self.player.switch_weapon(WEAPON_SHOTGUN)

        elif key == pygame.K_5:
            self.player.switch_weapon(WEAPON_AXE)

        elif key == pygame.K_h:
            self.player.use_bandage(self)

        elif key == pygame.K_t:
            self.player.use_medkit(self)

        elif key == pygame.K_y:
            self.player.eat(self)

        elif key == pygame.K_e:
            self.interact()

    def handle_inventory_key(self, key):
        if key == pygame.K_ESCAPE:
            self.state = GAME_PLAYING
            return

        if key == pygame.K_h:
            self.player.use_bandage(self)

        elif key == pygame.K_t:
            self.player.use_medkit(self)

        elif key == pygame.K_y:
            self.player.eat(self)

    def handle_skill_key(self, key):
        if key == pygame.K_ESCAPE:
            self.state = GAME_PLAYING
            return

        skills = list(self.player.skills.keys())

        if key in (pygame.K_DOWN, pygame.K_s):
            self.skill_selection = (
                self.skill_selection + 1
            ) % len(skills)

        elif key in (pygame.K_UP, pygame.K_w):
            self.skill_selection = (
                self.skill_selection - 1
            ) % len(skills)

        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            skill_id = skills[self.skill_selection]
            skill = self.player.skills[skill_id]

            if (
                self.player.skill_points > 0
                and skill.level < skill.maximum
            ):
                skill.level += 1
                self.player.skill_points -= 1
                self.notify(
                    f"{skill.name} upgraded to level {skill.level}.",
                    GREEN,
                )

    def handle_quest_key(self, key):
        if key == pygame.K_ESCAPE:
            self.state = GAME_PLAYING
            return

        if key in (pygame.K_DOWN, pygame.K_s):
            self.quest_selection = (
                self.quest_selection + 1
            ) % len(self.quest_system.quests)

        elif key in (pygame.K_UP, pygame.K_w):
            self.quest_selection = (
                self.quest_selection - 1
            ) % len(self.quest_system.quests)

        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            quest = self.quest_system.quests[
                self.quest_selection
            ]

            if quest.completed and not quest.claimed:
                self.quest_system.claim(quest, self)

    def handle_crafting_key(self, key):
        if key == pygame.K_ESCAPE:
            self.state = GAME_PLAYING
            return

        if key in (pygame.K_DOWN, pygame.K_s):
            self.crafting_selection = (
                self.crafting_selection + 1
            ) % len(RECIPES)

        elif key in (pygame.K_UP, pygame.K_w):
            self.crafting_selection = (
                self.crafting_selection - 1
            ) % len(RECIPES)

        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self.craft(RECIPES[self.crafting_selection])

    def handle_mouse(self, event):
        if self.state != GAME_PLAYING:
            return

        if event.button == 1:
            mx, my = pygame.mouse.get_pos()
            self.player.shoot(
                self,
                mx + self.camera_x,
                my + self.camera_y,
            )

        elif event.button == 3:
            self.player.aiming = not self.player.aiming

    # --------------------------------------------------------
    # Interactions
    # --------------------------------------------------------

    def interact(self):
        # Chest interaction.
        nearby = [
            chest
            for chest in self.world.chests
            if abs(chest.x - self.player.x) < 105
        ]

        if nearby:
            nearby.sort(
                key=lambda chest: abs(
                    chest.x - self.player.x
                )
            )
            nearby[0].interact(self)
            return

        # Safehouse interaction.
        if self.safehouse.inside(self.player):
            self.dialogue.start(
                "Survivor",
                [
                    "This place can be rebuilt.",
                    "Scrap metal can improve the medical station.",
                    "A stronger workbench will unlock better equipment.",
                ],
            )
            self.state = GAME_DIALOGUE
            return

        self.notify("Nothing nearby to interact with.", GREY)

    # --------------------------------------------------------
    # Crafting
    # --------------------------------------------------------

    def craft(self, recipe):
        for item, amount in recipe.cost.items():
            if not self.player.has_item(item, amount):
                self.notify(
                    f"Missing {ITEM_NAMES.get(item, item)}.",
                    RED,
                )
                return

        for item, amount in recipe.cost.items():
            self.player.remove_item(item, amount)

        for item, amount in recipe.result.items():
            self.player.add_item(item, amount)

        self.notify(
            f"Crafted {recipe.name}.",
            GREEN,
        )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    def update(self, dt):
        if self.state != GAME_PLAYING:
            self.update_messages(dt)
            return

        self.total_time += dt

        self.environment.update(dt)
        self.player.update(self, dt)

        self.update_camera(dt)
        self.update_enemies(dt)
        self.update_projectiles(dt)
        self.update_grenades(dt)
        self.update_drops(dt)
        self.update_particles(dt)
        self.update_floating_text(dt)
        self.update_messages(dt)
        self.update_story()

        self.muzzle_flash = max(0, self.muzzle_flash - dt)
        self.screen_shake = max(0, self.screen_shake - 24 * dt)

        # Checkpoint.
        if self.player.x > 1450:
            self.player_checkpoint = 1450

        # Zone transition notification.
        zone = self.world.zone_at(self.player.x)

        if zone.name != self.last_zone:
            self.last_zone = zone.name
            self.notify(
                f"Entering: {zone.name}",
                YELLOW,
                4,
            )

        # Unlock some weapons as the player reaches zones.
        if (
            self.player.x > 2500
            and not self.player.weapons[WEAPON_RIFLE]["owned"]
        ):
            self.player.unlock_weapon(WEAPON_RIFLE, 5)
            self.notify(
                "Weapon found: Bolt Rifle",
                YELLOW,
            )

        if (
            self.player.x > 5600
            and not self.player.weapons[WEAPON_SMG]["owned"]
        ):
            self.player.unlock_weapon(WEAPON_SMG, 32)
            self.notify(
                "Weapon found: WW2 SMG",
                YELLOW,
            )

        if (
            self.player.x > 8900
            and not self.player.weapons[WEAPON_SHOTGUN]["owned"]
        ):
            self.player.unlock_weapon(WEAPON_SHOTGUN, 5)
            self.notify(
                "Weapon found: Trench Shotgun",
                YELLOW,
            )

        # Procedural spawns near player.
        self.spawn_timer -= dt

        if self.spawn_timer <= 0:
            self.spawn_timer = random.uniform(5, 10)

            alive = sum(
                1 for enemy in self.enemies
                if not enemy.dead
            )

            if alive < 24:
                side = random.choice([-1, 1])

                spawn_x = self.player.x + side * random.randint(
                    800,
                    1250,
                )

                spawn_x = clamp(
                    spawn_x,
                    0,
                    WORLD_WIDTH - 100,
                )

                archetype = random.choices(
                    ["walker", "runner", "soldier", "screamer"],
                    [50, 20, 25, 5],
                )[0]

                self.enemies.append(
                    Zombie(
                        spawn_x,
                        archetype,
                        max(1, int(spawn_x / 2200)),
                    )
                )

    def update_camera(self, dt):
        target = self.player.x - WIDTH * 0.38

        self.camera_x = lerp(
            self.camera_x,
            target,
            clamp(dt * 6, 0, 1),
        )

        self.camera_x = clamp(
            self.camera_x,
            0,
            WORLD_WIDTH - WIDTH,
        )

    def update_enemies(self, dt):
        for enemy in self.enemies:
            enemy.update(self, dt)

        # Keep dead enemies for a while for quest/story references.
        if len(self.enemies) > 80:
            self.enemies = [
                enemy
                for enemy in self.enemies
                if not enemy.dead
            ]

    def update_projectiles(self, dt):
        for projectile in self.projectiles[:]:
            projectile.update(dt)

            if projectile.life <= 0:
                self.projectiles.remove(projectile)
                continue

            hit = False

            if projectile.owner == "player":
                for enemy in self.enemies:
                    if enemy.dead:
                        continue

                    if projectile.rect().colliderect(enemy.rect):
                        enemy.take_damage(
                            projectile.damage,
                            self,
                        )

                        self.particles.blood(
                            projectile.x,
                            projectile.y,
                        )

                        hit = True
                        break

            if hit and projectile in self.projectiles:
                self.projectiles.remove(projectile)

    def update_grenades(self, dt):
        for grenade in self.grenades_projectiles[:]:
            if not grenade.update(self, dt):
                self.grenades_projectiles.remove(grenade)

    def update_drops(self, dt):
        for drop in self.drops[:]:
            if not drop.update(self, dt):
                self.drops.remove(drop)

    def update_particles(self, dt):
        self.particles.update(dt)

    def update_floating_text(self, dt):
        for item in self.floating_texts[:]:
            item.update(dt)
            if item.life <= 0:
                self.floating_texts.remove(item)

    def update_messages(self, dt):
        for message in self.messages[:]:
            message.timer -= dt
            if message.timer <= 0:
                self.messages.remove(message)

    # --------------------------------------------------------
    # Save / Load
    # --------------------------------------------------------

    def save_game(self):
        data = {
            "player": {
                "x": self.player.x,
                "hp": self.player.hp,
                "max_hp": self.player.max_hp,
                "stamina": self.player.stamina,
                "hunger": self.player.hunger,
                "level": self.player.level,
                "xp": self.player.xp,
                "next_xp": self.player.next_xp,
                "skill_points": self.player.skill_points,
                "inventory": self.player.inventory,
                "weapons": self.player.weapons,
                "weapon": self.player.weapon,
                "grenades": self.player.grenades,
                "skills": {
                    key: asdict(skill)
                    for key, skill in self.player.skills.items()
                },
            },
            "chests": [
                chest.opened
                for chest in self.world.chests
            ],
            "quests": [
                asdict(quest)
                for quest in self.quest_system.quests
            ],
            "safehouse": {
                "level": self.safehouse.level,
                "medical_upgrade": self.safehouse.medical_upgrade,
                "workbench_upgrade": self.safehouse.workbench_upgrade,
            },
            "story_flags": self.story_flags,
            "total_time": self.total_time,
        }

        try:
            SAVE_FILE.write_text(
                json.dumps(data, indent=2),
                encoding="utf-8",
            )
            self.notify(
                "Game saved.",
                GREEN,
            )
        except OSError as exc:
            self.notify(
                f"Save failed: {exc}",
                RED,
            )

    def load_game(self):
        if not SAVE_FILE.exists():
            self.notify(
                "No save game exists.",
                RED,
            )
            return

        try:
            data = json.loads(
                SAVE_FILE.read_text(
                    encoding="utf-8"
                )
            )

            pdata = data["player"]

            self.player.x = pdata["x"]
            self.player.hp = pdata["hp"]
            self.player.max_hp = pdata["max_hp"]
            self.player.stamina = pdata["stamina"]
            self.player.hunger = pdata["hunger"]
            self.player.level = pdata["level"]
            self.player.xp = pdata["xp"]
            self.player.next_xp = pdata["next_xp"]
            self.player.skill_points = pdata["skill_points"]
            self.player.inventory = pdata["inventory"]
            self.player.weapons = pdata["weapons"]
            self.player.weapon = pdata["weapon"]
            self.player.grenades = pdata["grenades"]

            for key, skill_data in pdata["skills"].items():
                if key in self.player.skills:
                    self.player.skills[key].level = skill_data["level"]

            for chest, opened in zip(
                self.world.chests,
                data.get("chests", []),
            ):
                chest.opened = opened

            for quest, saved in zip(
                self.quest_system.quests,
                data.get("quests", []),
            ):
                quest.progress = saved["progress"]
                quest.completed = saved["completed"]
                quest.claimed = saved["claimed"]

            safehouse = data.get("safehouse", {})
            self.safehouse.level = safehouse.get(
                "level",
                1,
            )
            self.safehouse.medical_upgrade = safehouse.get(
                "medical_upgrade",
                0,
            )
            self.safehouse.workbench_upgrade = safehouse.get(
                "workbench_upgrade",
                0,
            )

            self.story_flags.update(
                data.get("story_flags", {})
            )

            self.total_time = data.get(
                "total_time",
                0,
            )

            self.state = GAME_PLAYING
            self.notify(
                "Game loaded.",
                GREEN,
            )

        except (
            OSError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
        ) as exc:
            self.notify(
                f"Load failed: {exc}",
                RED,
            )

    # --------------------------------------------------------
    # New Game
    # --------------------------------------------------------

    def new_game(self):
        self.__init__()
        self.state = GAME_PLAYING
        self.notify(
            "You escaped the asylum. Find supplies and survive.",
            YELLOW,
            5,
        )

    # --------------------------------------------------------
    # Drawing
    # --------------------------------------------------------

    def draw(self):
        # Camera shake.
        shake_x = 0
        shake_y = 0

        if self.screen_shake > 0:
            shake_x = random.randint(
                -int(self.screen_shake),
                int(self.screen_shake),
            )
            shake_y = random.randint(
                -int(self.screen_shake),
                int(self.screen_shake),
            )

        world_surface = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        self.world.draw_background(
            world_surface,
            self.camera_x,
            self.environment,
        )

        self.safehouse.draw(
            world_surface,
            self.camera_x,
        )

        self.world.draw_objects(
            world_surface,
            self.camera_x,
        )

        # Drops.
        for drop in self.drops:
            drop.draw(
                world_surface,
                self.camera_x,
            )

        # Enemies.
        for enemy in self.enemies:
            if not enemy.dead:
                enemy.draw(
                    world_surface,
                    self.camera_x,
                )

        # Projectiles.
        for projectile in self.projectiles:
            projectile.draw(
                world_surface,
                self.camera_x,
            )

        # Grenades.
        for grenade in self.grenades_projectiles:
            grenade.draw(
                world_surface,
                self.camera_x,
            )

        self.player.draw(
            world_surface,
            self.camera_x,
        )

        self.particles.draw(
            world_surface,
            self.camera_x,
        )

        self.floating_texts_draw(
            world_surface
        )

        screen.fill(BLACK)
        screen.blit(
            world_surface,
            (shake_x, shake_y),
        )

        # Environment overlays.
        self.environment.draw_overlay(screen)

        # Flashlight.
        self.draw_flashlight()

        # Muzzle flash.
        if self.muzzle_flash > 0:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.circle(
                screen,
                (255, 225, 135),
                (mx, my),
                24,
            )

        # State UI.
        if self.state == GAME_PLAYING:
            self.draw_hud()

        elif self.state == GAME_PAUSED:
            self.draw_hud()
            self.draw_pause()

        elif self.state == GAME_INVENTORY:
            self.draw_hud()
            self.draw_inventory()

        elif self.state == GAME_SKILLS:
            self.draw_hud()
            self.draw_skills()

        elif self.state == GAME_QUESTS:
            self.draw_hud()
            self.draw_quests()

        elif self.state == GAME_MAP:
            self.draw_hud()
            self.draw_map()

        elif self.state == GAME_CRAFTING:
            self.draw_hud()
            self.draw_crafting()

        elif self.state == GAME_DIALOGUE:
            self.draw_hud()
            self.dialogue.draw(screen)

        elif self.state == GAME_GAMEOVER:
            self.draw_gameover()

        elif self.state == GAME_VICTORY:
            self.draw_victory()

        self.draw_messages()

        if self.show_debug:
            self.draw_debug()

    def floating_texts_draw(self, surface):
        for item in self.floating_texts:
            item.draw(
                surface,
                self.camera_x,
            )

    # --------------------------------------------------------
    # Flashlight
    # --------------------------------------------------------

    def draw_flashlight(self):
        if not self.player.flashlight:
            return

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (0, 0, 0, 135)
        )

        mx, my = pygame.mouse.get_pos()

        # Transparent circular light.
        pygame.draw.circle(
            overlay,
            (0, 0, 0, 0),
            (mx, my),
            205,
        )

        # Additional subtle light.
        pygame.draw.circle(
            overlay,
            (255, 255, 210, 18),
            (mx, my),
            220,
        )

        screen.blit(
            overlay,
            (0, 0),
        )

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------

    def draw_hud(self):
        # Left player panel.
        panel = pygame.Rect(
            15,
            15,
            365,
            125,
        )

        draw_panel(
            screen,
            panel,
            205,
        )

        draw_text(
            screen,
            f"LEVEL {self.player.level}",
            30,
            25,
            FONT_SMALL,
            YELLOW,
        )

        draw_text(
            screen,
            f"XP {int(self.player.xp)}/{self.player.next_xp}",
            120,
            25,
            FONT_SMALL,
            OFFWHITE,
        )

        draw_bar(
            screen,
            pygame.Rect(30, 52, 210, 18),
            self.player.hp,
            self.player.max_hp,
            RED,
        )

        draw_text(
            screen,
            f"{int(self.player.hp)}/{self.player.max_hp}",
            250,
            48,
            FONT_SMALL,
            WHITE,
        )

        draw_bar(
            screen,
            pygame.Rect(30, 78, 210, 14),
            self.player.stamina,
            self.player.max_stamina,
            GREEN,
        )

        draw_bar(
            screen,
            pygame.Rect(30, 100, 210, 14),
            self.player.hunger,
            100,
            ORANGE,
        )

        draw_text(
            screen,
            f"{WEAPONS[self.player.weapon].name}",
            250,
            77,
            FONT_SMALL,
            YELLOW,
        )

        ammo = self.player.weapons[
            self.player.weapon
        ]["ammo"]

        draw_text(
            screen,
            f"{ammo} / {self.ammo_reserve()}",
            250,
            100,
            FONT_SMALL,
            WHITE,
        )

        # Right controls panel.
        draw_panel(
            screen,
            pygame.Rect(
                WIDTH - 300,
                15,
                285,
                125,
            ),
            180,
        )

        draw_text(
            screen,
            "A/D Move   SPACE Jump",
            WIDTH - 285,
            25,
            FONT_TINY,
            OFFWHITE,
        )
        draw_text(
            screen,
            "LMB Shoot   R Reload",
            WIDTH - 285,
            47,
            FONT_TINY,
            OFFWHITE,
        )
        draw_text(
            screen,
            "E Search   F Light",
            WIDTH - 285,
            69,
            FONT_TINY,
            OFFWHITE,
        )
        draw_text(
            screen,
            "I Inventory   J Quests",
            WIDTH - 285,
            91,
            FONT_TINY,
            OFFWHITE,
        )
        draw_text(
            screen,
            "K Skills   C Craft",
            WIDTH - 285,
            113,
            FONT_TINY,
            OFFWHITE,
        )

        # Minimap.
        if self.minimap:
            self.draw_minimap()

    def ammo_reserve(self):
        ammo_type = WEAPONS[
            self.player.weapon
        ].ammo_type

        item = {
            "9mm": "ammo_9mm",
            "rifle": "ammo_rifle",
            "shell": "ammo_shell",
        }.get(ammo_type)

        if not item:
            return 0

        return self.player.inventory.get(
            item,
            0,
        )

    # --------------------------------------------------------
    # Minimap
    # --------------------------------------------------------

    def draw_minimap(self):
        rect = pygame.Rect(
            WIDTH - 300,
            HEIGHT - 130,
            285,
            100,
        )

        draw_panel(
            screen,
            rect,
            190,
        )

        # World line.
        line = pygame.Rect(
            rect.x + 15,
            rect.y + 50,
            rect.w - 30,
            8,
        )

        pygame.draw.rect(
            screen,
            (62, 65, 61),
            line,
        )

        player_ratio = self.player.x / WORLD_WIDTH
        px = int(
            line.x + player_ratio * line.width
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (px, line.centery),
            7,
        )

        for zone in ZONES:
            zx = int(
                line.x
                + zone.start / WORLD_WIDTH * line.width
            )

            pygame.draw.line(
                screen,
                zone.color,
                (zx, line.y - 4),
                (zx, line.bottom + 4),
                3,
            )

        draw_text(
            screen,
            "WORLD MAP",
            rect.x + 15,
            rect.y + 12,
            FONT_SMALL,
            OFFWHITE,
        )

        draw_text(
            screen,
            self.world.zone_at(self.player.x).name,
            rect.x + 15,
            rect.y + 68,
            FONT_TINY,
            YELLOW,
        )

    # --------------------------------------------------------
    # Inventory
    # --------------------------------------------------------

    def draw_inventory(self):
        draw_panel(
            screen,
            pygame.Rect(
                120,
                70,
                WIDTH - 240,
                HEIGHT - 140,
            ),
            235,
        )

        draw_text(
            screen,
            "INVENTORY",
            WIDTH // 2,
            100,
            FONT_BIG,
            YELLOW,
            True,
        )

        y = 165

        items = [
            (key, value)
            for key, value in self.player.inventory.items()
            if value > 0
        ]

        if not items:
            draw_text(
                screen,
                "Empty backpack.",
                WIDTH // 2,
                y,
                FONT,
                GREY,
                True,
            )

        for item_id, amount in items:
            draw_text(
                screen,
                ITEM_NAMES.get(
                    item_id,
                    item_id,
                ),
                190,
                y,
                FONT,
                WHITE,
            )

            draw_text(
                screen,
                str(amount),
                560,
                y,
                FONT,
                YELLOW,
            )

            y += 34

        # Weapons.
        draw_text(
            screen,
            "WEAPONS",
            690,
            160,
            FONT_MED,
            YELLOW,
        )

        y = 205

        for weapon_id, data in self.player.weapons.items():
            definition = WEAPONS[weapon_id]

            owned = data["owned"]

            draw_text(
                screen,
                definition.name,
                690,
                y,
                FONT_SMALL,
                WHITE if owned else GREY,
            )

            if owned:
                draw_text(
                    screen,
                    f"{data['ammo']} loaded",
                    940,
                    y,
                    FONT_SMALL,
                    GREEN,
                )
            else:
                draw_text(
                    screen,
                    "LOCKED",
                    940,
                    y,
                    FONT_SMALL,
                    RED,
                )

            y += 34

        draw_text(
            screen,
            "H Bandage   T Medkit   Y Food",
            WIDTH // 2,
            HEIGHT - 105,
            FONT_SMALL,
            OFFWHITE,
            True,
        )

        draw_text(
            screen,
            "I / ESC to close",
            WIDTH // 2,
            HEIGHT - 75,
            FONT_SMALL,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    def draw_skills(self):
        draw_panel(
            screen,
            pygame.Rect(
                180,
                70,
                WIDTH - 360,
                HEIGHT - 140,
            ),
            235,
        )

        draw_text(
            screen,
            "SKILLS",
            WIDTH // 2,
            105,
            FONT_BIG,
            YELLOW,
            True,
        )

        draw_text(
            screen,
            f"Skill Points: {self.player.skill_points}",
            WIDTH // 2,
            155,
            FONT,
            GREEN,
            True,
        )

        skills = list(
            self.player.skills.values()
        )

        y = 205

        for index, skill in enumerate(skills):
            selected = (
                index == self.skill_selection
            )

            if selected:
                pygame.draw.rect(
                    screen,
                    (65, 75, 65),
                    (235, y - 7, 810, 72),
                    border_radius=7,
                )

            draw_text(
                screen,
                f"{skill.name}  [{skill.level}/{skill.maximum}]",
                260,
                y,
                FONT_MED,
                YELLOW if selected else WHITE,
            )

            draw_text(
                screen,
                skill.description,
                260,
                y + 35,
                FONT_SMALL,
                OFFWHITE,
            )

            y += 82

        draw_text(
            screen,
            "UP/DOWN select   ENTER upgrade   K/ESC close",
            WIDTH // 2,
            HEIGHT - 95,
            FONT_SMALL,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Quests
    # --------------------------------------------------------

    def draw_quests(self):
        draw_panel(
            screen,
            pygame.Rect(
                100,
                60,
                WIDTH - 200,
                HEIGHT - 120,
            ),
            235,
        )

        draw_text(
            screen,
            "MISSIONS",
            WIDTH // 2,
            95,
            FONT_BIG,
            YELLOW,
            True,
        )

        y = 165

        for index, quest in enumerate(
            self.quest_system.quests
        ):
            selected = (
                index == self.quest_selection
            )

            if selected:
                pygame.draw.rect(
                    screen,
                    (63, 72, 64),
                    (140, y - 8, 1000, 92),
                    border_radius=8,
                )

            status = (
                "CLAIMED"
                if quest.claimed
                else "COMPLETED"
                if quest.completed
                else f"{quest.progress}/{quest.required}"
            )

            draw_text(
                screen,
                quest.title,
                165,
                y,
                FONT_MED,
                YELLOW if selected else WHITE,
            )

            draw_text(
                screen,
                quest.description,
                165,
                y + 38,
                FONT_SMALL,
                OFFWHITE,
            )

            draw_text(
                screen,
                status,
                960,
                y + 10,
                FONT_SMALL,
                GREEN if quest.completed else WHITE,
            )

            y += 105

        draw_text(
            screen,
            "UP/DOWN select   ENTER claim reward   J/ESC close",
            WIDTH // 2,
            HEIGHT - 80,
            FONT_SMALL,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Crafting
    # --------------------------------------------------------

    def draw_crafting(self):
        draw_panel(
            screen,
            pygame.Rect(
                180,
                65,
                WIDTH - 360,
                HEIGHT - 130,
            ),
            235,
        )

        draw_text(
            screen,
            "FIELD WORKBENCH",
            WIDTH // 2,
            105,
            FONT_BIG,
            YELLOW,
            True,
        )

        y = 180

        for index, recipe in enumerate(
            RECIPES
        ):
            selected = (
                index == self.crafting_selection
            )

            if selected:
                pygame.draw.rect(
                    screen,
                    (65, 74, 66),
                    (225, y - 8, 830, 80),
                    border_radius=7,
                )

            draw_text(
                screen,
                recipe.name,
                250,
                y,
                FONT_MED,
                YELLOW if selected else WHITE,
            )

            costs = ", ".join(
                f"{ITEM_NAMES.get(k,k)} x{v}"
                for k, v in recipe.cost.items()
            )

            result = ", ".join(
                f"{ITEM_NAMES.get(k,k)} x{v}"
                for k, v in recipe.result.items()
            )

            draw_text(
                screen,
                f"Cost: {costs}",
                250,
                y + 34,
                FONT_SMALL,
                OFFWHITE,
            )

            draw_text(
                screen,
                f"Produces: {result}",
                700,
                y + 34,
                FONT_SMALL,
                GREEN,
            )

            y += 88

        draw_text(
            screen,
            "UP/DOWN select   ENTER craft   C/ESC close",
            WIDTH // 2,
            HEIGHT - 80,
            FONT_SMALL,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Map
    # --------------------------------------------------------

    def draw_map(self):
        draw_panel(
            screen,
            pygame.Rect(
                60,
                55,
                WIDTH - 120,
                HEIGHT - 110,
            ),
            235,
        )

        draw_text(
            screen,
            "TACTICAL MAP",
            WIDTH // 2,
            90,
            FONT_BIG,
            YELLOW,
            True,
        )

        map_rect = pygame.Rect(
            110,
            165,
            WIDTH - 220,
            330,
        )

        pygame.draw.rect(
            screen,
            (44, 50, 45),
            map_rect,
            border_radius=8,
        )

        for zone in ZONES:
            x = (
                map_rect.x
                + zone.start / WORLD_WIDTH
                * map_rect.width
            )

            width = (
                zone.end - zone.start
            ) / WORLD_WIDTH * map_rect.width

            pygame.draw.rect(
                screen,
                zone.color,
                (
                    int(x),
                    map_rect.y,
                    int(width),
                    map_rect.height,
                ),
            )

            draw_text(
                screen,
                zone.name,
                x + width / 2,
                map_rect.centery,
                FONT_SMALL,
                WHITE,
                True,
            )

        player_x = (
            map_rect.x
            + self.player.x / WORLD_WIDTH
            * map_rect.width
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (int(player_x), map_rect.centery),
            10,
        )

        draw_text(
            screen,
            "● YOU",
            int(player_x) + 18,
            map_rect.centery - 10,
            FONT_SMALL,
            YELLOW,
        )

        draw_text(
            screen,
            "M / ESC to close",
            WIDTH // 2,
            HEIGHT - 100,
            FONT_SMALL,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Pause
    # --------------------------------------------------------

    def draw_pause(self):
        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA,
        )
        overlay.fill(
            (0, 0, 0, 175)
        )
        screen.blit(
            overlay,
            (0, 0),
        )

        draw_text(
            screen,
            "PAUSED",
            WIDTH // 2,
            HEIGHT // 2 - 70,
            FONT_TITLE,
            YELLOW,
            True,
        )

        draw_text(
            screen,
            "ESC / P — Resume",
            WIDTH // 2,
            HEIGHT // 2 + 10,
            FONT,
            WHITE,
            True,
        )

        draw_text(
            screen,
            "F5 — Save     F9 — Load",
            WIDTH // 2,
            HEIGHT // 2 + 55,
            FONT_SMALL,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Menu
    # --------------------------------------------------------

    def draw_menu(self):
        screen.fill(
            (19, 23, 21)
        )

        # Large background.
        for i in range(10):
            pygame.draw.rect(
                screen,
                (
                    35 + i * 2,
                    39 + i * 2,
                    36 + i * 2,
                ),
                (
                    i * 70,
                    0,
                    WIDTH - i * 140,
                    HEIGHT,
                ),
                3,
            )

        draw_text(
            screen,
            "ASHES",
            WIDTH // 2,
            145,
            FONT_TITLE,
            OFFWHITE,
            True,
        )

        draw_text(
            screen,
            "OF THE DEAD",
            WIDTH // 2,
            215,
            FONT_TITLE,
            RED,
            True,
        )

        draw_text(
            screen,
            "WW2 ZOMBIE SURVIVAL",
            WIDTH // 2,
            280,
            FONT_MED,
            YELLOW,
            True,
        )

        options = [
            "NEW GAME",
            "LOAD GAME",
            "CONTINUE DEMO",
            "QUIT",
        ]

        y = 380

        for index, option in enumerate(options):
            selected = (
                index == self.main_menu_selection
            )

            if selected:
                pygame.draw.rect(
                    screen,
                    (70, 75, 67),
                    (WIDTH // 2 - 180, y - 8, 360, 52),
                    border_radius=7,
                )

            draw_text(
                screen,
                option,
                WIDTH // 2,
                y + 16,
                FONT_MED,
                YELLOW if selected else OFFWHITE,
                True,
            )

            y += 62

        draw_text(
            screen,
            VERSION,
            WIDTH // 2,
            HEIGHT - 35,
            FONT_TINY,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Game Over
    # --------------------------------------------------------

    def draw_gameover(self):
        screen.fill(
            (20, 13, 14)
        )

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA,
        )
        overlay.fill(
            (90, 10, 15, 80)
        )
        screen.blit(
            overlay,
            (0, 0),
        )

        draw_text(
            screen,
            "THE DEAD FOUND YOU",
            WIDTH // 2,
            245,
            FONT_TITLE,
            RED,
            True,
        )

        draw_text(
            screen,
            f"Level reached: {self.player.level}",
            WIDTH // 2,
            345,
            FONT_MED,
            WHITE,
            True,
        )

        draw_text(
            screen,
            f"XP earned: {int(self.player.xp)}",
            WIDTH // 2,
            390,
            FONT,
            OFFWHITE,
            True,
        )

        draw_text(
            screen,
            "ENTER — Restart",
            WIDTH // 2,
            480,
            FONT_MED,
            YELLOW,
            True,
        )

        draw_text(
            screen,
            "ESC — Main Menu",
            WIDTH // 2,
            530,
            FONT_SMALL,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Victory
    # --------------------------------------------------------

    def draw_victory(self):
        screen.fill(
            (17, 23, 20)
        )

        draw_text(
            screen,
            "PROJECT ECLIPSE",
            WIDTH // 2,
            190,
            FONT_TITLE,
            YELLOW,
            True,
        )

        draw_text(
            screen,
            "THE WARDEN HAS FALLEN",
            WIDTH // 2,
            275,
            FONT_BIG,
            RED,
            True,
        )

        draw_text(
            screen,
            "But the outbreak may not be over...",
            WIDTH // 2,
            360,
            FONT_MED,
            WHITE,
            True,
        )

        draw_text(
            screen,
            f"Survival Level: {self.player.level}",
            WIDTH // 2,
            425,
            FONT,
            OFFWHITE,
            True,
        )

        draw_text(
            screen,
            "ENTER — New Game",
            WIDTH // 2,
            500,
            FONT_MED,
            YELLOW,
            True,
        )

        draw_text(
            screen,
            "ESC — Main Menu",
            WIDTH // 2,
            545,
            FONT_SMALL,
            GREY,
            True,
        )

    # --------------------------------------------------------
    # Messages
    # --------------------------------------------------------

    def draw_messages(self):
        if not self.messages:
            return

        y = HEIGHT - 180

        for message in reversed(
            self.messages[-4:]
        ):
            draw_panel(
                screen,
                pygame.Rect(
                    20,
                    y,
                    480,
                    34,
                ),
                180,
                False,
            )

            draw_text(
                screen,
                message.text,
                32,
                y + 8,
                FONT_SMALL,
                message.color,
            )

            y -= 39

    # --------------------------------------------------------
    # Debug
    # --------------------------------------------------------

    def draw_debug(self):
        lines = [
            f"FPS: {clock.get_fps():.1f}",
            f"State: {self.state}",
            f"Player X: {self.player.x:.1f}",
            f"Enemies: {len(self.enemies)}",
            f"Projectiles: {len(self.projectiles)}",
            f"Particles: {len(self.particles.particles)}",
            f"Time: {self.total_time:.1f}",
            f"Weather: {self.environment.weather.kind}",
        ]

        y = 150

        for line in lines:
            draw_text(
                screen,
                line,
                20,
                y,
                FONT_TINY,
                GREEN,
            )
            y += 18

    # --------------------------------------------------------
    # Main Loop
    # --------------------------------------------------------

    def run(self):
        while self.running:
            dt = min(
                clock.tick(FPS) / 1000.0,
                0.035,
            )

            for event in pygame.event.get():
                self.handle_event(event)

            if self.state == GAME_MENU:
                self.update_messages(dt)
            elif self.state not in (
                GAME_GAMEOVER,
                GAME_VICTORY,
            ):
                self.update(dt)

            if self.state == GAME_MENU:
                self.draw_menu()
            else:
                self.draw()

            pygame.display.flip()

        pygame.quit()


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
