import pygame

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

# Ukuran layar
WIDTH, HEIGHT = 1068, 600

# Font
FONT = pygame.font.SysFont("verdana", 26)
FONT_BOLD = pygame.font.SysFont("verdana", 28, bold=True)
BIG_FONT = pygame.font.SysFont("verdana", 38, bold=True)
SMALL_FONT = pygame.font.SysFont("verdana", 18)