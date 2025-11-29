import pygame
import sys
import random
import math
import os

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 204, 0)
ORANGE = (255, 128, 0)
LIGHT_BLUE = (100, 150, 255)
MAROON = (128, 0, 0)
GRAY = (200, 200, 200)

WIDTH, HEIGHT = 1068, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EduFlag: Grafika Komputer Edition")
clock = pygame.time.Clock()
# ==== FONT ====
FONT = pygame.font.SysFont("verdana", 26)
FONT_BOLD = pygame.font.SysFont("verdana", 28, bold=True)
BIG_FONT = pygame.font.SysFont("verdana", 38, bold=True)
SMALL_FONT = pygame.font.SysFont("verdana", 18)

def scale_keep_ratio(image, max_w, max_h):
    img_w, img_h = image.get_size()
    ratio = min(max_w / img_w, max_h / img_h)
    new_w = int(img_w * ratio)
    new_h = int(img_h * ratio)
    return pygame.transform.smoothscale(image, (new_w, new_h))

# --- LOAD GAMBAR ---
img_halaman_judul = None  
img_halaman_level = None  

BG_EASY = pygame.image.load("assets/easy.png")
BG_EXPERT = pygame.image.load("assets/easy.png")
BG_TIME = pygame.image.load("assets/easy.png")
BG_SURVIVAL = pygame.image.load("assets/easy.png")

# Resize agar sesuai layar
BG_EASY = pygame.transform.scale(BG_EASY, (WIDTH, HEIGHT))
BG_EXPERT = pygame.transform.scale(BG_EXPERT, (WIDTH, HEIGHT))
BG_TIME = pygame.transform.scale(BG_TIME, (WIDTH, HEIGHT))
BG_SURVIVAL = pygame.transform.scale(BG_SURVIVAL, (WIDTH, HEIGHT))

try:
    HEART_FULL = pygame.image.load("assets/heart.png").convert_alpha()
    HEART_FULL = pygame.transform.scale(HEART_FULL, (40, 40))
except:
    HEART_FULL = None
    print("heart.png tidak ditemukan!")

try:
    HEART_EMPTY = pygame.image.load("assets/heart_empty.png").convert_alpha()
    HEART_EMPTY = pygame.transform.scale(HEART_EMPTY, (40, 40))
except:
    HEART_EMPTY = None


def get_asset_path(filename):
    if os.path.exists(os.path.join("assets", filename)):
        return os.path.join("assets", filename)
    elif os.path.exists(filename):
        return filename
    return None

# --- LOAD GAMBAR  ---
img_halaman_judul = None
img_halaman_level = None

def get_asset_path(filename):
    if os.path.exists(os.path.join("assets", filename)):
        return os.path.join("assets", filename)
    elif os.path.exists(filename):
        return filename
    return None

# Scale keeping ratio 
def scale_keep_ratio(image, max_w, max_h):
    img_w, img_h = image.get_size()
    ratio = min(max_w / img_w, max_h / img_h)
    new_w = int(img_w * ratio)
    new_h = int(img_h * ratio)
    return pygame.transform.smoothscale(image, (new_w, new_h))

try:
    # 1. start.png
    path_start = get_asset_path("start.png")
    if path_start:
        raw = pygame.image.load(path_start)
        img_halaman_judul = scale_keep_ratio(raw, WIDTH, HEIGHT)

    # 2. menu.png
    path_menu = get_asset_path("menu.png")
    if path_menu:
        raw = pygame.image.load(path_menu)
        img_halaman_level = scale_keep_ratio(raw, WIDTH, HEIGHT)

except Exception as e:
    print(f"Error loading gambar: {e}")


# --- FUNGSI HELPER GRAFIKA ---
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

# Fungsi Generic (Fallback)
def flag_generic(s, x, y, w, h):
    pygame.draw.rect(s, GRAY, (x, y, w, h))
    pygame.draw.rect(s, BLACK, (x, y, w, h), 2)
    t = SMALL_FONT.render("Bendera", True, BLACK)
    s.blit(t, (x+10, y+10))

# MAPPING NEGARA
FLAG_FUNCS = {
    "Indonesia": None,
    "Japan": None,
    "France": None,
    "Italy": None,
    "Germany": None,
    "India": None,
    "Bangladesh": None,
    "Nigeria": None,
    "Turkey": None,
    "Switzerland": None
}

import csv

DATA_EXPERT = []  
FLAG_IMAGES = {}

def load_flag_images():
    folder = "flags"
    if not os.path.exists(folder):
        print("Folder flags/ tidak ditemukan")
        return

    for file in os.listdir(folder):
        if not file.endswith(".png"):
            continue

        # Ambil nama negara dari nama file
        name = file.replace(".png", "")

        # Konversi nama agar kapital awal
        country = name.capitalize()

        # Khusus Japan (biar tidak jadi "Japan" saja, tapi tetap benar)
        if country.lower() == "japan":
            country = "Japan"

        # Load PNG
        path = os.path.join(folder, file)
        try:
            img = pygame.image.load(path).convert_alpha()
            FLAG_IMAGES[country] = img
            print("Loaded:", country)
        except:
            print("Error load:", path)

import csv

# normalisasi nama country dari CSV ke key yang sama dengan FLAG_IMAGES / FLAG_FUNCS
def normalize_country(name: str):
    if not name:
        return ""

    n = name.strip().lower()

    mapping = {
        "indonesia": "Indonesia",
        "jepang": "Japan",
        "japan": "Japan",
        "perancis": "France",
        "france": "France",
        "italia": "Italy",
        "italy": "Italy",
        "jerman": "Germany",
        "germany": "Germany",
        "bangladesh": "Bangladesh",
        "india": "India",
        "nigeria": "Nigeria",
        "turki": "Turkey",
        "turkey": "Turkey",
        "swiss": "Switzerland",
        "switzerland": "Switzerland"
    }

    if n in mapping:
        return mapping[n]

    return name.strip().title()


DATA_EXPERT = []  

def load_expert_csv(filename="quiz.csv"):
    global DATA_EXPERT
    DATA_EXPERT = []

    if not os.path.exists(filename):
        print("CSV expert tidak ditemukan:", filename)
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  

        for row in reader:
            if len(row) >= 3:
                desc = row[1].strip()         
                country = normalize_country(row[2])
                DATA_EXPERT.append((desc, country))

    print("Loaded expert CSV:", len(DATA_EXPERT), "soal")

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
        if HEART_FULL:
            if i < lives:
                surface.blit(HEART_FULL, (pos_x, y))
            else:
                draw_heart(surface, pos_x + 20, y + 20, size=16, color=col)
        else:
            col = (255, 0, 0) if i < lives else (180, 180, 180)
            draw_heart(surface, pos_x + 20, y + 20, size=16, color=col)

# --- GAME ENGINE ---
class Game:
    def get_background(self):
        if self.mode == "EASY":
            return BG_EASY
        elif self.mode == "EXPERT":
            return BG_EXPERT
        elif self.mode == "TIME":
            return BG_TIME
        elif self.mode == "SURVIVAL":
            return BG_SURVIVAL
        return None

    def __init__(self):
        # State awal
        self.state = "TITLE" 
        
        self.mode = None
        self.score = 0
        self.question_index = 0
        self.max_questions = 10
        self.lives = 3
        self.time_left = 20
        self.last_time_update = 0
        self.current_question = None 
        self.options = [] 
        self.feedback_message = ""
        self.feedback_color = BLACK
        self.expert_questions = DATA_EXPERT

        self.rect_tombol_masuk = pygame.Rect(
            WIDTH//2 - 175,   
            260,             
            380,             
            80               
        )

        # --- TOMBOL DI HALAMAN MENU LEVEL (4 TOMBOL) ---
        button_w = 260
        button_h = 110

        self.rect_easy = pygame.Rect(200, 200, button_w, button_h)
        self.rect_time = pygame.Rect(WIDTH - 200 - button_w, 210, button_w, button_h)
        self.rect_expert = pygame.Rect(200, 390, button_w, button_h)
        self.rect_survival = pygame.Rect(WIDTH - 200 - button_w, 390, button_w, button_h)

    def start_level(self, mode):
        self.mode = mode
        self.score = 0
        self.question_index = 0

        # === MODE SURVIVAL ===
        if mode == "SURVIVAL":
            self.lives = 3          
            self.time_left = None   
            self.state = "PLAY_SURVIVAL"
            self.generate_question()
            return

        # === MODE TIME ATTACK ===
        if mode == "TIME":
            self.lives = 999          
            self.time_left = 60       
            self.state = "PLAY_TIME"
            self.generate_question()
            return

        # === MODE EXPERT ===
        if mode == "EXPERT":
            self.lives = 3
            self.time_left = 20
            self.state = "PLAY_EXPERT"
            self.generate_question()
            return

        # === MODE EASY ===
        self.lives = 999
        self.time_left = 20
        self.state = "PLAY_EASY"
        self.generate_question()


    def generate_question(self):
        if self.mode != "TIME":
            self.time_left = 20

        self.last_time_update = pygame.time.get_ticks()
        self.feedback_message = ""

        available = list(FLAG_IMAGES.keys()) if FLAG_IMAGES else list(FLAG_FUNCS.keys())
        if not available:
            available = ["Indonesia", "Japan"]

        if self.mode == "EASY":
            correct = random.choice(available)
            self.current_question = (correct, correct)

        elif self.mode == "EXPERT":
            if DATA_EXPERT:
                attempts = 0
                desc = None
                correct = None
                while attempts < 50:
                    desc_candidate, country_candidate = random.choice(DATA_EXPERT)
                    country_norm = country_candidate
                    if country_norm in available:
                        desc = desc_candidate
                        correct = country_norm
                        break
                    alt = country_candidate.strip().title()
                    if alt in available:
                        desc = desc_candidate
                        correct = alt
                        break
                    attempts += 1

                if not desc:
                    correct = random.choice(available)
                    desc = f"Deskripsi {correct}"
                self.current_question = (desc, correct)
            else:
                correct = random.choice(available)
                desc = f"Deskripsi {correct}"
                self.current_question = (desc, correct)

        elif self.mode == "TIME":
            available = list(FLAG_IMAGES.keys())
            if DATA_EXPERT:
                desc, correct = random.choice(DATA_EXPERT)
                self.current_question = (desc, correct)
            else:
                correct = random.choice(available)
                desc = f"Deskripsi {correct}"
                self.current_question = (desc, correct)

            remaining = [c for c in available if c != correct]
            distractors = random.sample(remaining, 3)
            self.options = [correct] + distractors
            random.shuffle(self.options)

            return

        elif self.mode == "SURVIVAL":
            if DATA_EXPERT:
                desc, correct = random.choice(DATA_EXPERT)
                self.current_question = (desc, correct)
            else:
                correct = random.choice(available)
                desc = f"Deskripsi {correct}"
                self.current_question = (desc, correct)

            remaining = [c for c in available if c != correct]
            distractors = random.sample(remaining, 3)
            self.options = [correct] + distractors
            random.shuffle(self.options)
            return

        correct_country = self.current_question[1]
        remaining = [c for c in available if c != correct_country]
        if len(remaining) < 3:
            distractors = remaining
        else:
            distractors = random.sample(remaining, 3)

        self.options = [correct_country] + distractors
        random.shuffle(self.options)


    def check_answer(self, answer):
        correct = self.current_question[1]
        if answer == correct:
            self.score += 10
            self.feedback_message = "BENAR!"
            self.feedback_color = GREEN
        else:
            self.feedback_message = f"SALAH! Itu {answer}"
            self.feedback_color = RED
            if self.mode in ["EXPERT", "SURVIVAL"]:
                self.lives -= 1


        self.question_index += 1
        
        if self.mode == "EASY" and self.question_index >= self.max_questions:
             self.state = "GAMEOVER"
        elif self.lives <= 0:
            self.state = "GAMEOVER"
        else:
            self.generate_question()

    def update(self):
        if self.state == "PLAY_EXPERT":
            now = pygame.time.get_ticks()
            if now - self.last_time_update > 1000:
                self.time_left -= 1
                self.last_time_update = now
                if self.time_left <= 0:
                    self.lives -= 1
                    self.feedback_message = "WAKTU HABIS!"
                    self.question_index += 1
                    if self.lives <= 0:
                        self.state = "GAMEOVER"
                    else:
                        self.generate_question()

        if self.state == "PLAY_TIME":
            now = pygame.time.get_ticks()
            if now - self.last_time_update > 1000:
                self.time_left -= 1
                self.last_time_update = now
                if self.time_left <= 0:
                    self.state = "GAMEOVER"


    def draw(self):
        screen.fill(WHITE)
        
        # --- HALAMAN 1: JUDUL (start.png) ---
        if self.state == "TITLE":
            if img_halaman_judul:
                screen.blit(img_halaman_judul, (0, 0))

            else:
                screen.fill(LIGHT_BLUE)
                t = BIG_FONT.render("HALAMAN AWAL (start.png)", True, BLACK)
                screen.blit(t, (150, 300))

        # --- HALAMAN 2: PILIH LEVEL (menu.png) ---
        elif self.state == "MENU":
            if img_halaman_level:
                screen.blit(img_halaman_level, (0, 0))
            else:
                screen.fill(YELLOW)
                t = BIG_FONT.render("PILIH LEVEL (menu.png)", True, BLACK)
                screen.blit(t, (150, 300))
            
        # --- HALAMAN 3: GAMEPLAY ---
        elif self.state.startswith("PLAY"):
            if self.mode == "EASY":
                screen.blit(BG_EASY, (0, 0))
            elif self.mode == "EXPERT":
                screen.blit(BG_EXPERT, (0, 0))
            elif self.mode == "TIME":
                screen.blit(BG_TIME, (0, 0))
            elif self.mode == "SURVIVAL":
                screen.blit(BG_SURVIVAL, (0, 0))
            header = f"Score: {self.score} | Soal: {self.question_index+1}"
            if self.mode == "EXPERT":
                header += f" | Time: {self.time_left}"
            
            t_head = FONT.render(header, True, BLACK)
            screen.blit(t_head, (20, 20))
            if self.mode in ["EXPERT", "SURVIVAL"]:
                draw_lives(screen, 20, 60, self.lives)
            
            if self.mode == "EASY":
                negara = self.current_question[0]
                if negara in FLAG_IMAGES:
                    img = scale_keep_ratio(FLAG_IMAGES[negara], 250, 150)
                    screen.blit(img, (WIDTH//2 - img.get_width()//2, 40))
                else:
                    flag_generic(screen, WIDTH//2 - 125, 40, 250, 150)
                t_soal = FONT.render("Bendera negara apakah ini?", True, BLACK)
                screen.blit(t_soal, (WIDTH//2 - t_soal.get_width()//2, 220))

            else:
                q_text = self.current_question[0]
                t_q = FONT.render(q_text, True, BLACK)
                rect_q = t_q.get_rect(center=(WIDTH//2, 80))
                screen.blit(t_q, rect_q)

            if self.feedback_message:
                t_feed = FONT.render(self.feedback_message, True, self.feedback_color)
                screen.blit(t_feed, (WIDTH//2 - t_feed.get_width()//2, 120))

            mouse_pos = pygame.mouse.get_pos()

            if self.mode == "EASY":
                box_w, box_h = 320, 52
                gap_y = 18
                start_x = WIDTH//2 - box_w//2
                start_y = 290

                for i, country in enumerate(self.options):
                    y = start_y + i*(box_h + gap_y)
                    rect = pygame.Rect(start_x, y, box_w, box_h)

                    # ==== TOMBOL ====
                    bg_color = (255, 255, 255, 200) 
                    button_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
                
                    pygame.draw.rect(button_surf, bg_color, (0, 0, box_w, box_h), border_radius=20)
                    border_col = ORANGE if rect.collidepoint(mouse_pos) else (90, 90, 90)
                    pygame.draw.rect(button_surf, border_col, (0, 0, box_w, box_h), 3, border_radius=20)
                    screen.blit(button_surf, (start_x, y))

                    text = FONT.render(country, True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)


            elif self.mode == "TIME":
                header1 = f"Score: {self.score} | Soal: {self.question_index+1}"
                t_head1 = FONT.render(header1, True, BLACK)
                screen.blit(t_head1, (20, 20))

                header2 = f"Time: {self.time_left}"
                t_head2 = FONT.render(header2, True, BLACK)
                screen.blit(t_head2, (20, 55))

                q_text = self.current_question[0]
                t_q = FONT.render(q_text, True, BLACK)
                rect_q = t_q.get_rect(center=(WIDTH//2, 80))
                screen.blit(t_q, rect_q)

                mouse_pos = pygame.mouse.get_pos()
                box_w, box_h = 200, 130
                gap_x, gap_y = 40, 40
                start_x = (WIDTH - (2 * box_w + gap_x)) // 2
                start_y = 240

                for i, country in enumerate(self.options):
                    col = i % 2
                    row = i // 2
                    x = start_x + col*(box_w + gap_x)
                    y = start_y + row*(box_h + gap_y)

                    rect = pygame.Rect(x, y, box_w, box_h)
                    border_col = ORANGE if rect.collidepoint(mouse_pos) else BLACK

                    if country in FLAG_IMAGES:
                        img = scale_keep_ratio(FLAG_IMAGES[country], box_w, box_h)
                        screen.blit(img, (x, y))
                    else:
                        flag_generic(screen, x, y, box_w, box_h)

                    pygame.draw.rect(screen, border_col, rect, 3)

            elif self.mode == "SURVIVAL":
                header = f"Score: {self.score} | Soal: {self.question_index+1}"
                t_head = FONT.render(header, True, BLACK)
                screen.blit(t_head, (20, 20))

                q_text = self.current_question[0]
                t_q = FONT.render(q_text, True, BLACK)
                screen.blit(t_q, t_q.get_rect(center=(WIDTH//2, 80)))

                box_w, box_h = 200, 130
                gap_x, gap_y = 40, 40
                start_x = (WIDTH - (2 * box_w + gap_x)) // 2
                start_y = 240

                mouse_pos = pygame.mouse.get_pos()

                for i, country in enumerate(self.options):
                    col = i % 2
                    row = i // 2
                    x = start_x + col*(box_w + gap_x)
                    y = start_y + row*(box_h + gap_y)
                    rect = pygame.Rect(x, y, box_w, box_h)

                    border_col = ORANGE if rect.collidepoint(mouse_pos) else BLACK

                    if country in FLAG_IMAGES:
                        img = scale_keep_ratio(FLAG_IMAGES[country], box_w, box_h)
                        screen.blit(img, (x, y))
                    else:
                        flag_generic(screen, x, y, box_w, box_h)

                    pygame.draw.rect(screen, border_col, rect, 3)

            else:
                box_w, box_h = 200, 130
                gap_x, gap_y = 40, 40
                start_x = (WIDTH - (2*box_w + gap_x)) // 2
                start_y = 240

                for i, country in enumerate(self.options):
                    col = i % 2
                    row = i // 2
                    x = start_x + col*(box_w + gap_x)
                    y = start_y + row*(box_h + gap_y)

                    rect = pygame.Rect(x, y, box_w, box_h)
                    border_col = ORANGE if rect.collidepoint(mouse_pos) else BLACK

                    if country in FLAG_IMAGES:
                        img = scale_keep_ratio(FLAG_IMAGES[country], box_w, box_h)
                        screen.blit(img, (x, y))
                    else:
                        flag_generic(screen, x, y, box_w, box_h)

                    pygame.draw.rect(screen, border_col, rect, 3)

        # --- HALAMAN 4: GAME OVER ---
        elif self.state == "GAMEOVER":
            t_go = BIG_FONT.render("GAME OVER", True, RED)
            screen.blit(t_go, (WIDTH//2 - t_go.get_width()//2, 200))
            t_sc = FONT.render(f"Final Score: {self.score}", True, BLACK)
            screen.blit(t_sc, (WIDTH//2 - t_sc.get_width()//2, 260))
            
            btn_rect = pygame.Rect(WIDTH//2 - 100, 350, 200, 50)
            pygame.draw.rect(screen, BLUE, btn_rect)
            t_menu = FONT.render("Main Menu", True, WHITE)
            screen.blit(t_menu, (WIDTH//2 - t_menu.get_width()//2, 360))

        pygame.display.flip()

# --- MAIN LOOP ---
game = Game()
load_flag_images() 
load_expert_csv()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # 1. KLIK DI HALAMAN JUDUL (start.png)
            if game.state == "TITLE":
                if game.rect_tombol_masuk.collidepoint(pos):
                    game.state = "MENU" 
            
            # 2. KLIK DI PILIH LEVEL (menu.png)
            elif game.state == "MENU":
                if game.rect_easy.collidepoint(pos):
                    game.start_level("EASY")

                elif game.rect_time.collidepoint(pos):
                    game.start_level("TIME")

                elif game.rect_expert.collidepoint(pos):
                    game.start_level("EXPERT")

                elif game.rect_survival.collidepoint(pos):
                    game.start_level("SURVIVAL")

            # 3. KLIK SAAT MAIN
            elif game.state.startswith("PLAY"):
                if game.mode == "EASY":
                    # Klik opsi vertikal
                    box_w, box_h = 320, 52
                    gap_y = 18
                    start_x = WIDTH//2 - box_w//2
                    start_y = 290

                    for i, country in enumerate(game.options):
                        y = start_y + i*(box_h + gap_y)
                        rect = pygame.Rect(start_x, y, box_w, box_h)
                        if rect.collidepoint(pos):
                            game.check_answer(country)

                # --- klik TIME ATTACK 2x2 ---
                elif game.mode in ["EXPERT", "SURVIVAL"]:
                    box_w, box_h = 200, 130
                    gap_x, gap_y = 50, 50
                    start_x = (WIDTH - (2*box_w + gap_x)) // 2
                    start_y = 180

                    for i, country in enumerate(game.options):
                        col = i % 2
                        row = i // 2
                        x = start_x + col*(box_w + gap_x)
                        y = start_y + row*(box_h + gap_y)
                        if pygame.Rect(x, y, box_w, box_h).collidepoint(pos):
                            game.check_answer(country)
                
                else:
                    box_w, box_h = 200, 130
                    gap_x, gap_y = 50, 50
                    start_x = (WIDTH - (2*box_w + gap_x)) // 2
                    start_y = 180

                    for i, country in enumerate(game.options):
                        col = i % 2
                        row = i // 2
                        x = start_x + col*(box_w + gap_x)
                        y = start_y + row*(box_h + gap_y)
                        rect = pygame.Rect(x, y, box_w, box_h)
                        if rect.collidepoint(pos):
                            game.check_answer(country)

            # 4. KLIK GAME OVER
            elif game.state == "GAMEOVER":
                 if WIDTH//2 - 100 < pos[0] < WIDTH//2 + 100 and 350 < pos[1] < 400:
                     game.state = "TITLE" 

    game.update()
    game.draw()
    clock.tick(60)

pygame.quit()
sys.exit()