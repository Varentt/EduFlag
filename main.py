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

# GAME STATE
state = "start"

# Tombol start (di tengah gambar)
# Sesuaikan posisi tombol start kamu
start_button = pygame.Rect(WIDTH//2 - 150, 350, 300, 100)

# Tombol menu
easy_btn      = pygame.Rect(200, 300, 250, 100)
expert_btn    = pygame.Rect(200, 450, 250, 100)
time_btn      = pygame.Rect(830, 300, 250, 100)
survive_btn   = pygame.Rect(830, 450, 250, 100)


def draw_start():
    screen.blit(start_img, (0, 0))
    # Debug button area (optional)
    # pygame.draw.rect(screen, (255,0,0), start_button, 3)


def draw_menu():
    screen.blit(menu_img, (0, 0))
    # Optional: debug outline
    # pygame.draw.rect(screen, (0,255,0), easy_btn, 3)
    # pygame.draw.rect(screen, (0,255,0), expert_btn, 3)
    # pygame.draw.rect(screen, (0,255,0), time_btn, 3)
    # pygame.draw.rect(screen, (0,255,0), survive_btn, 3)


# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if state == "start":
                if start_button.collidepoint(mx, my):
                    state = "menu"

            elif state == "menu":
                if easy_btn.collidepoint(mx, my):
                    print("Mode EASY dipilih")
                if expert_btn.collidepoint(mx, my):
                    print("Mode EXPERT dipilih")
                if time_btn.collidepoint(mx, my):
                    print("Mode TIME ATTACK dipilih")
                if survive_btn.collidepoint(mx, my):
                    print("Mode SURVIVAL dipilih")

    # DRAW STATE
    if state == "start":
        draw_start()
    elif state == "menu":
        draw_menu()

    pygame.display.update()
