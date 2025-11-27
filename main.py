import pygame
import sys

pygame.init()

# WINDOW
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EduFlag")

# LOAD IMAGES
start_img = pygame.image.load("assets/start.png")
menu_img = pygame.image.load("assets/menu.png")

start_img = pygame.transform.scale(start_img, (WIDTH, HEIGHT))
menu_img = pygame.transform.scale(menu_img, (WIDTH, HEIGHT))

# FONT
font_big = pygame.font.Font(None, 72)
font_small = pygame.font.Font(None, 40)

# GAME STATE
state = "start"
current_question = 0

# Tombol start
start_button = pygame.Rect(WIDTH//2 - 150, 350, 300, 100)

# Tombol menu sesuai gambar
easy_btn      = pygame.Rect(260, 300, 300, 110)
time_btn      = pygame.Rect(760, 300, 300, 110)
expert_btn    = pygame.Rect(260, 460, 300, 110)
survive_btn   = pygame.Rect(760, 460, 300, 110)


# --- DRAW FUNCTIONS ---
def draw_start():
    screen.blit(start_img, (0, 0))


def draw_menu():
    screen.blit(menu_img, (0, 0))


def draw_easy():
    screen.fill((255, 255, 255))

    text = font_big.render(f"Soal Easy #{current_question+1}", True, (0,0,0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 50))

    # Placeholder gambar bendera
    pygame.draw.rect(screen, (200,200,200), (440, 150, 400, 250), border_radius=20)

    info = font_small.render("Klik untuk lanjut ke soal berikutnya", True, (0,0,0))
    screen.blit(info, (WIDTH//2 - info.get_width()//2, 500))


# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # START SCREEN
            if state == "start":
                if start_button.collidepoint(mx, my):
                    state = "menu"

            # MENU SCREEN
            elif state == "menu":
                if easy_btn.collidepoint(mx, my):
                    print("Mode EASY dipilih")
                    state = "easy"
                    current_question = 0

                elif expert_btn.collidepoint(mx, my):
                    print("Mode EXPERT dipilih")

                elif time_btn.collidepoint(mx, my):
                    print("Mode TIME ATTACK dipilih")

                elif survive_btn.collidepoint(mx, my):
                    print("Mode SURVIVAL dipilih")

            # EASY MODE
            elif state == "easy":
                current_question += 1
                if current_question >= 10:
                    print("Selesai mode easy")
                    state = "menu"


    # DRAW STATE
    if state == "start":
        draw_start()
    elif state == "menu":
        draw_menu()
    elif state == "easy":
        draw_easy()

    pygame.display.update()
