import pygame
import os
import csv
import math
from config import *

# Global variables
FLAG_IMAGES = {}
DATA_EXPERT = []
BG_EASY = BG_EXPERT = BG_TIME = BG_SURVIVAL = None
img_halaman_judul = img_halaman_level = None
HEART_FULL = HEART_EMPTY = None
GAMEOVER_BG = None

def get_asset_path(filename):
    if os.path.exists(os.path.join("assets", filename)):
        return os.path.join("assets", filename)
    elif os.path.exists(filename):
        return filename
    return None

def scale_keep_ratio(image, max_w, max_h):
    img_w, img_h = image.get_size()
    ratio = min(max_w / img_w, max_h / img_h)
    new_w = int(img_w * ratio)
    new_h = int(img_h * ratio)
    return pygame.transform.smoothscale(image, (new_w, new_h))

def draw_star(surface, color, cx, cy, radius):
    points = []
    for i in range(10):
        angle = i * 36 - 90
        r = radius if i % 2 == 0 else radius * 0.4
        x = cx + math.cos(math.radians(angle)) * r
        y = cy + math.sin(math.radians(angle)) * r
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

def draw_crescent(surface, color, x, y, radius):
    pygame.draw.circle(surface, color, (x, y), radius)

def draw_heart(surface, x, y, size=20, color=(255, 0, 0)):
    points = [
        (x, y + size),
        (x - size, y),
        (x, y - size),
        (x + size, y),
    ]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.circle(surface, color, (x - size//2, y - size//2), size//1.4)
    pygame.draw.circle(surface, color, (x + size//2, y - size//2), size//1.4)

def draw_lives(surface, x, y, lives, max_lives=3):
    for i in range(max_lives):
        pos_x = x + i * 45
        if HEART_FULL and i < lives:
            surface.blit(HEART_FULL, (pos_x, y))
        else:
            col = (255, 0, 0) if i < lives else (180, 180, 180)
            draw_heart(surface, pos_x + 20, y + 20, size=16, color=col)

def flag_generic(s, x, y, w, h):
    pygame.draw.rect(s, GRAY, (x, y, w, h))
    pygame.draw.rect(s, BLACK, (x, y, w, h), 2)
    t = SMALL_FONT.render("Bendera", True, BLACK)
    s.blit(t, (x+10, y+10))

def normalize_country(name: str):
    if not name:
        return ""
    n = name.strip().lower()
    mapping = {
        "indonesia": "Indonesia", "jepang": "Japan", "japan": "Japan",
        "perancis": "France", "france": "France", "italia": "Italy",
        "italy": "Italy", "jerman": "Germany", "germany": "Germany",
        "bangladesh": "Bangladesh", "india": "India", "nigeria": "Nigeria",
        "turki": "Turkey", "turkey": "Turkey", "swiss": "Switzerland",
        "switzerland": "Switzerland"
    }
    return mapping.get(n, name.strip().title())

# Button images
BTN_EXIT = None
BTN_BACK = None

def load_all_assets():
    global FLAG_IMAGES, DATA_EXPERT
    global BG_EASY, BG_EXPERT, BG_TIME, BG_SURVIVAL
    global img_halaman_judul, img_halaman_level
    global HEART_FULL, HEART_EMPTY
    global BTN_EXIT, BTN_BACK
    global GAMEOVER_BG
    # Load backgrounds
    try:
        BG_EASY = pygame.transform.scale(pygame.image.load("assets/easy.png"), (WIDTH, HEIGHT))
        BG_EXPERT = pygame.transform.scale(pygame.image.load("assets/easy.png"), (WIDTH, HEIGHT))
        BG_TIME = pygame.transform.scale(pygame.image.load("assets/easy.png"), (WIDTH, HEIGHT))
        BG_SURVIVAL = pygame.transform.scale(pygame.image.load("assets/easy.png"), (WIDTH, HEIGHT))
        GAMEOVER_BG = pygame.transform.scale(pygame.image.load("assets/gameover.png"), (WIDTH, HEIGHT))
    except:
        print("Background images tidak ditemukan!")
    
    # Load UI images
    try:
        path_start = get_asset_path("start.png")
        if path_start:
            img_halaman_judul = scale_keep_ratio(pygame.image.load(path_start), WIDTH, HEIGHT)
        path_menu = get_asset_path("menu.png")
        if path_menu:
            img_halaman_level = scale_keep_ratio(pygame.image.load(path_menu), WIDTH, HEIGHT)
    except Exception as e:
        print(f"Error loading UI images: {e}")
    
    # Load heart images
    try:
        HEART_FULL = pygame.transform.scale(pygame.image.load("assets/heart.png").convert_alpha(), (40, 40))
        HEART_EMPTY = pygame.transform.scale(pygame.image.load("assets/heart_empty.png").convert_alpha(), (40, 40))
    except:
        print("Heart images tidak ditemukan!")
    
    # Load button images
    try:
        BTN_EXIT = pygame.image.load("assets/exit.png").convert_alpha()
        BTN_EXIT = pygame.transform.scale(BTN_EXIT, (60, 60))
        print("Loaded: exit button")
    except:
        print("exit.png tidak ditemukan!")
    
    try:
        BTN_BACK = pygame.image.load("assets/back.png").convert_alpha()
        BTN_BACK = pygame.transform.scale(BTN_BACK, (60, 60))
        print("Loaded: back button")
    except:
        print("back.png tidak ditemukan!")
    
    # Load flag images
    folder = "flags"
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.endswith(".png"):
                name = file.replace(".png", "").capitalize()
                try:
                    FLAG_IMAGES[name] = pygame.image.load(os.path.join(folder, file)).convert_alpha()
                    print("Loaded:", name)
                except:
                    print("Error load:", file)
    
    # Load CSV
    if os.path.exists("quiz.csv"):
        with open("quiz.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) >= 3:
                    DATA_EXPERT.append((row[1].strip(), normalize_country(row[2])))
        print("Loaded CSV:", len(DATA_EXPERT), "soal")