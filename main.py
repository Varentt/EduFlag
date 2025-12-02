import pygame
import sys
from config import *
from utils import load_all_assets
import utils
from game_modes import EasyMode, ExpertMode, TimeMode, SurvivalMode

# Inisialisasi
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EduFlag: Grafika Komputer Edition")
clock = pygame.time.Clock()

# Load semua aset
load_all_assets()

# Game state
state = "TITLE"
current_mode = None
mode_name = None

# Rectangles untuk klik
rect_tombol_masuk = pygame.Rect(WIDTH//2 - 175, 260, 380, 80)
button_w, button_h = 260, 110
rect_easy = pygame.Rect(200, 200, button_w, button_h)
rect_time = pygame.Rect(WIDTH - 200 - button_w, 210, button_w, button_h)
rect_expert = pygame.Rect(200, 390, button_w, button_h)
rect_survival = pygame.Rect(WIDTH - 200 - button_w, 390, button_w, button_h)

# Tombol keluar dan kembali (posisi untuk gambar PNG)
btn_exit_title = pygame.Rect(WIDTH//2 - 30, 420, 60, 60)
btn_exit_menu = pygame.Rect(WIDTH - 80, HEIGHT - 80, 60, 60)
btn_back_play = pygame.Rect(20, HEIGHT - 80, 60, 60)
btn_menu_gameover = pygame.Rect(WIDTH//2 - 100, 350, 200, 50)

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            if state == "TITLE":
                if rect_tombol_masuk.collidepoint(pos):
                    state = "MENU"
                elif btn_exit_title.collidepoint(pos):
                    running = False
            
            elif state == "MENU":
                if rect_easy.collidepoint(pos):
                    current_mode = EasyMode(screen)
                    mode_name = "EASY"
                    current_mode.generate_question()
                    state = "PLAY"
                elif rect_time.collidepoint(pos):
                    current_mode = TimeMode(screen)
                    mode_name = "TIME"
                    current_mode.generate_question()
                    state = "PLAY"
                elif rect_expert.collidepoint(pos):
                    current_mode = ExpertMode(screen)
                    mode_name = "EXPERT"
                    current_mode.generate_question()
                    state = "PLAY"
                elif rect_survival.collidepoint(pos):
                    current_mode = SurvivalMode(screen)
                    mode_name = "SURVIVAL"
                    current_mode.generate_question()
                    state = "PLAY"
                elif btn_exit_menu.collidepoint(pos):
                    running = False
            
            elif state == "PLAY":
                if btn_back_play.collidepoint(pos):
                    state = "MENU"
                    current_mode = None
                    mode_name = None
                else:
                    result = current_mode.handle_click(pos)
                    if result == "GAMEOVER":
                        state = "GAMEOVER"
            
            elif state == "GAMEOVER":
                if btn_menu_gameover.collidepoint(pos):
                    state = "MENU"
                    current_mode = None
                    mode_name = None
    
    # Update
    if state == "PLAY" and current_mode:
        result = current_mode.update()
        if result == "GAMEOVER":
            state = "GAMEOVER"
    
    # Draw
    screen.fill(WHITE)
    
    if state == "TITLE":
        if utils.img_halaman_judul:
            screen.blit(utils.img_halaman_judul, (0, 0))
        else:
            screen.fill(LIGHT_BLUE)
            t = BIG_FONT.render("EDUFLAG - Grafika Komputer", True, BLACK)
            screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 50))
        
        # Tombol exit di halaman awal
        if utils.BTN_EXIT:
            screen.blit(utils.BTN_EXIT, btn_exit_title.topleft)
        else:
            pygame.draw.rect(screen, RED, btn_exit_title)
            t_exit = SMALL_FONT.render("EXIT", True, WHITE)
            screen.blit(t_exit, (btn_exit_title.centerx - t_exit.get_width()//2, 
                                  btn_exit_title.centery - t_exit.get_height()//2))
    
    elif state == "MENU":
        if utils.img_halaman_level:
            screen.blit(utils.img_halaman_level, (0, 0))
        else:
            screen.fill(YELLOW)
            t = BIG_FONT.render("PILIH MODE", True, BLACK)
            screen.blit(t, (WIDTH//2 - t.get_width()//2, 50))
        
        # Tombol exit di menu
        if utils.BTN_EXIT:
            screen.blit(utils.BTN_EXIT, btn_exit_menu.topleft)
        else:
            pygame.draw.rect(screen, RED, btn_exit_menu)
            t_exit = SMALL_FONT.render("EXIT", True, WHITE)
            screen.blit(t_exit, (btn_exit_menu.centerx - t_exit.get_width()//2, 
                                  btn_exit_menu.centery - t_exit.get_height()//2))
    
    elif state == "PLAY":
        bg = None
        if mode_name == "EASY":
            bg = utils.BG_EASY
        elif mode_name == "EXPERT":
            bg = utils.BG_EXPERT
        elif mode_name == "TIME":
            bg = utils.BG_TIME
        elif mode_name == "SURVIVAL":
            bg = utils.BG_SURVIVAL
        
        current_mode.draw(bg)
        
        # Tombol back saat main
        if utils.BTN_BACK:
            screen.blit(utils.BTN_BACK, btn_back_play.topleft)
        else:
            pygame.draw.rect(screen, ORANGE, btn_back_play)
            t_back = SMALL_FONT.render("←", True, WHITE)
            screen.blit(t_back, (btn_back_play.centerx - t_back.get_width()//2, 
                                  btn_back_play.centery - t_back.get_height()//2))
    
    elif state == "GAMEOVER":
        # Tampilkan background gameover jika tersedia
        if hasattr(utils, "GAMEOVER_BG") and utils.GAMEOVER_BG:
            screen.blit(utils.GAMEOVER_BG, (0, 0))
        else:
            screen.fill(WHITE)

        # Teks Game Over
        t_go = BIG_FONT.render("GAME OVER", True, RED)
        screen.blit(t_go, (WIDTH//2 - t_go.get_width()//2, 120))

        # Score
        score = current_mode.score if current_mode else 0
        t_sc = FONT.render(f"Final Score: {score}", True, BLACK)
        screen.blit(t_sc, (WIDTH//2 - t_sc.get_width()//2, 220))

        # Tombol ke menu
        pygame.draw.rect(screen, BLUE, btn_menu_gameover)
        t_menu = FONT.render("Main Menu", True, WHITE)
        screen.blit(t_menu, (WIDTH//2 - t_menu.get_width()//2, 360))

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()