#
# Arquivo: settings.py
#
import pygame

COLOR_PANEL_BG = (20, 20, 30)      # Um azul-escuro/cinza
COLOR_PANEL_BORDER = (100, 100, 100) # Cinza
COLOR_TITLE_TEXT = (255, 255, 100) # Amarelo, para "OBJETIVOS"
COLOR_OBJECTIVE_TEXT = (220, 220, 220) # Branco-cinza


# --- Resolução Base (Interna) ---
# O jogo sempre vai "achar" que tem esse tamanho.
# Use a resolução que criamos no layout proporcional (800x600 é ótimo)
GAME_WIDTH = 800
GAME_HEIGHT = 600

# --- Resolução Inicial da Janela ---
# O tamanho que a janela abre ao iniciar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 60
PADDING = 10

WHITE = (255, 255, 255)
BLACK = (10, 10, 10)

# --- Layout (Usamos GAME_WIDTH/HEIGHT para os cálculos) ---

# 1. Barra Lateral Esquerda
LEFT_PANEL_WIDTH = int(GAME_WIDTH * (240 / 1024)) 
LEFT_PANEL_RECT = pygame.Rect(
    PADDING,
    PADDING,
    LEFT_PANEL_WIDTH,
    GAME_HEIGHT - (PADDING * 2)
)

# 1a. Posição da Imagem do Professor
PROFESSOR_IMAGE_WIDTH = LEFT_PANEL_WIDTH - (PADDING * 2)
PROFESSOR_IMAGE_HEIGHT = PROFESSOR_IMAGE_WIDTH
PROFESSOR_RECT = pygame.Rect(
    LEFT_PANEL_RECT.left + PADDING,
    LEFT_PANEL_RECT.top + PADDING,
    PROFESSOR_IMAGE_WIDTH,
    PROFESSOR_IMAGE_HEIGHT
)

# 1b. Objetivos
OBJECTIVE_LIST_RECT = pygame.Rect(
    LEFT_PANEL_RECT.left,
    PROFESSOR_RECT.bottom + PADDING,
    LEFT_PANEL_RECT.width,
    LEFT_PANEL_RECT.height - PROFESSOR_RECT.height - PADDING * 2 
)

# 2. Barra Inferior
INPUT_BOX_HEIGHT = int(GAME_HEIGHT * (100 / 768))
INPUT_BOX_RECT = pygame.Rect(
    LEFT_PANEL_RECT.right + PADDING, 
    GAME_HEIGHT - INPUT_BOX_HEIGHT - PADDING,
    GAME_WIDTH - LEFT_PANEL_RECT.right - (PADDING * 2),
    INPUT_BOX_HEIGHT
)

# 3. Balão de Fala
SPEECH_BUBBLE_HEIGHT = int(GAME_HEIGHT * (160 / 768))
SPEECH_BUBBLE_RECT = pygame.Rect(
    LEFT_PANEL_RECT.right + PADDING,
    PADDING,
    INPUT_BOX_RECT.width,
    SPEECH_BUBBLE_HEIGHT
)

# 4. Terminal
TERMINAL_RECT = pygame.Rect(
    LEFT_PANEL_RECT.right + PADDING,
    SPEECH_BUBBLE_RECT.bottom + PADDING,
    INPUT_BOX_RECT.width,
    INPUT_BOX_RECT.top - SPEECH_BUBBLE_RECT.bottom - (PADDING * 2)
)
# 5. Sistema de Vida
MAX_STRIKES = 5
COLOR_STRIKE_GOOD = (50, 255, 50) # Verde
COLOR_STRIKE_BAD = (255, 50, 50)   # Vermelho
