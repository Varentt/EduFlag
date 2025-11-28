import pygame
import sys
import random
import math
import os

# --- KONFIGURASI AWAL ---
pygame.init()

# Warna
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

# Layar
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EduFlag: Grafika Komputer Edition")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont('Arial', 24, bold=True)
BIG_FONT = pygame.font.SysFont('Arial', 40, bold=True)
SMALL_FONT = pygame.font.SysFont('Arial', 16)

# --- LOAD GAMBAR (ALUR BARU) ---
img_halaman_judul = None  # start.png
img_halaman_level = None  # menu.png

def get_asset_path(filename):
    if os.path.exists(os.path.join("assets", filename)):
        return os.path.join("assets", filename)
    elif os.path.exists(filename):
        return filename
    return None

try:
    # 1. Load start.png (JADI HALAMAN JUDUL/AWAL)
    path_start = get_asset_path("start.png")
    if path_start:
        img_halaman_judul = pygame.image.load(path_start)
        img_halaman_judul = pygame.transform.scale(img_halaman_judul, (WIDTH, HEIGHT))
    
    # 2. Load menu.png (JADI HALAMAN PILIH LEVEL)
    path_menu = get_asset_path("menu.png")
    if path_menu:
        img_halaman_level = pygame.image.load(path_menu)
        img_halaman_level = pygame.transform.scale(img_halaman_level, (WIDTH, HEIGHT))

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

# --- FUNGSI BENDERA ---
def flag_indonesia(s, x, y, w, h):
    pygame.draw.rect(s, RED, (x, y, w, h/2))
    pygame.draw.rect(s, WHITE, (x, y+h/2, w, h/2))
    pygame.draw.rect(s, BLACK, (x, y, w, h), 1)

def flag_jepang(s, x, y, w, h):
    pygame.draw.rect(s, WHITE, (x, y, w, h))
    pygame.draw.circle(s, RED, (x + w//2, y + h//2), h//3)
    pygame.draw.rect(s, BLACK, (x, y, w, h), 1)

# Fungsi Generic (Fallback)
def flag_generic(s, x, y, w, h):
    pygame.draw.rect(s, GRAY, (x, y, w, h))
    pygame.draw.rect(s, BLACK, (x, y, w, h), 2)
    t = SMALL_FONT.render("Bendera", True, BLACK)
    s.blit(t, (x+10, y+10))

# MAPPING NEGARA
FLAG_FUNCS = {
    "Indonesia": flag_indonesia,
    "Jepang": flag_jepang,
    # Tambahkan negara lain...
}

DATA_EXPERT = [
    ("Negara kepulauan terbesar dengan ibukota Jakarta.", "Indonesia"),
    ("Negara Sakura yang terkenal dengan Gunung Fuji.", "Jepang"),
    ("Negara adidaya dengan 50 negara bagian.", "Amerika Serikat"),
]

# --- GAME ENGINE ---
class Game:
    def __init__(self):
        # State awal: TITLE (Menampilkan start.png)
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

        # --- PENGATURAN POSISI TOMBOL ---
        # Rect(x, y, lebar, tinggi)
        
        # 1. Tombol 'Masuk' di start.png
        # (Saya taruh di tengah bawah, ubah angkanya kalau tombolmu ada di tempat lain)
        self.rect_tombol_masuk = pygame.Rect(WIDTH//2 - 100, 450, 200, 100)
        
        # 2. Tombol di menu.png (Pilih Level)
        # Tombol Easy (Kiri)
        self.rect_easy = pygame.Rect(200, 300, 200, 100)
        # Tombol Expert (Kanan)
        self.rect_expert = pygame.Rect(500, 300, 200, 100)

    def start_level(self, mode):
        self.mode = mode
        self.score = 0
        self.question_index = 0
        self.lives = 3 if mode == "EXPERT" else 999
        self.state = f"PLAY_{mode}"
        self.generate_question()

    def generate_question(self):
        self.time_left = 20
        self.last_time_update = pygame.time.get_ticks()
        self.feedback_message = ""
        
        all_countries = list(FLAG_FUNCS.keys())
        if not all_countries: all_countries = ["Indonesia", "Jepang"]

        if self.mode == "EASY":
            correct = random.choice(all_countries)
            self.current_question = (f"Cari bendera: {correct}", correct)
        elif self.mode == "EXPERT":
            if DATA_EXPERT:
                desc, correct = random.choice(DATA_EXPERT)
            else:
                correct = random.choice(all_countries)
                desc = f"Deskripsi {correct}"
            self.current_question = (desc, correct)

        correct_country = self.current_question[1]
        remaining = [c for c in all_countries if c != correct_country]
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
            if self.mode == "EXPERT":
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
            
            # Debug: Kotak Merah (Hapus baris ini kalau posisi sudah pas)
            pygame.draw.rect(screen, RED, self.rect_tombol_masuk, 3)

        # --- HALAMAN 2: PILIH LEVEL (menu.png) ---
        elif self.state == "MENU":
            if img_halaman_level:
                screen.blit(img_halaman_level, (0, 0))
            else:
                screen.fill(YELLOW)
                t = BIG_FONT.render("PILIH LEVEL (menu.png)", True, BLACK)
                screen.blit(t, (150, 300))
            
            # Debug: Kotak Hijau (Hapus baris ini kalau posisi sudah pas)
            pygame.draw.rect(screen, GREEN, self.rect_easy, 3)
            pygame.draw.rect(screen, GREEN, self.rect_expert, 3)

        # --- HALAMAN 3: GAMEPLAY ---
        elif self.state.startswith("PLAY"):
            header = f"Score: {self.score} | Soal: {self.question_index+1}"
            if self.mode == "EXPERT":
                header += f" | Lives: {self.lives} | Time: {self.time_left}"
            
            t_head = FONT.render(header, True, BLACK)
            screen.blit(t_head, (20, 20))
            
            q_text = self.current_question[0]
            t_q = FONT.render(q_text, True, BLACK)
            rect_q = t_q.get_rect(center=(WIDTH//2, 80))
            screen.blit(t_q, rect_q)

            if self.feedback_message:
                t_feed = FONT.render(self.feedback_message, True, self.feedback_color)
                screen.blit(t_feed, (WIDTH//2 - t_feed.get_width()//2, 120))

            box_w, box_h = 200, 130
            gap_x, gap_y = 50, 50
            start_x = (WIDTH - (2*box_w + gap_x)) // 2
            start_y = 180
            mouse_pos = pygame.mouse.get_pos()
            
            for i, country in enumerate(self.options):
                col = i % 2
                row = i // 2
                x = start_x + col * (box_w + gap_x)
                y = start_y + row * (box_h + gap_y)
                
                rect = pygame.Rect(x, y, box_w, box_h)
                border_col = BLACK
                if rect.collidepoint(mouse_pos):
                    border_col = ORANGE
                
                if country in FLAG_FUNCS:
                    FLAG_FUNCS[country](screen, x, y, box_w, box_h)
                else:
                    flag_generic(screen, x, y, box_w, box_h)
                    
                pygame.draw.rect(screen, border_col, (x, y, box_w, box_h), 3)

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
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # 1. KLIK DI HALAMAN JUDUL (start.png)
            if game.state == "TITLE":
                # Jika klik area tombol masuk -> Pindah ke MENU LEVEL
                if game.rect_tombol_masuk.collidepoint(pos):
                    game.state = "MENU" 
            
            # 2. KLIK DI PILIH LEVEL (menu.png)
            elif game.state == "MENU":
                if game.rect_easy.collidepoint(pos):
                    game.start_level("EASY")
                elif game.rect_expert.collidepoint(pos):
                    game.start_level("EXPERT")
            
            # 3. KLIK SAAT MAIN
            elif game.state.startswith("PLAY"):
                box_w, box_h = 200, 130
                gap_x, gap_y = 50, 50
                start_x = (WIDTH - (2*box_w + gap_x)) // 2
                start_y = 180
                for i, country in enumerate(game.options):
                    col = i % 2
                    row = i // 2
                    x = start_x + col * (box_w + gap_x)
                    y = start_y + row * (box_h + gap_y)
                    rect = pygame.Rect(x, y, box_w, box_h)
                    if rect.collidepoint(pos):
                        game.check_answer(country)
            
            # 4. KLIK GAME OVER
            elif game.state == "GAMEOVER":
                 if WIDTH//2 - 100 < pos[0] < WIDTH//2 + 100 and 350 < pos[1] < 400:
                     game.state = "TITLE" # Balik ke awal

    game.update()
    game.draw()
    clock.tick(60)

pygame.quit()
sys.exit()