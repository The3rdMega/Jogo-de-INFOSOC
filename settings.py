#
# Arquivo: settings.py
#
import pygame

# --- Configurações Gerais da Tela ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# --- Padding (Espaçamento) ---
PADDING = 10

# --- Definições de Cores (Centralizadas) ---
# (Cores de texto, etc., podem ser movidas das classes de UI para cá)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
GREY = (100, 100, 100)
LIGHT_GREY = (230, 230, 230)
DARK_GREY = (30, 30, 30)

# Cores do Terminal
COLOR_TERMINAL_BG = (10, 10, 25)
COLOR_TERMINAL_TEXT = (25, 255, 25)
COLOR_TERMINAL_PROMPT = (100, 255, 100)

# Cores do Painel de Objetivos
COLOR_PANEL_BG = (20, 20, 30)
COLOR_TITLE_TEXT = (255, 255, 100)
COLOR_OBJECTIVE_TEXT = (220, 220, 220)

# Cores do Balão de Fala
COLOR_BUBBLE_BG = LIGHT_GREY
COLOR_BUBBLE_TEXT = BLACK

# Cores da Caixa de Entrada
COLOR_INPUT_BG = DARK_GREY
COLOR_INPUT_PROMPT = COLOR_TITLE_TEXT
COLOR_INPUT_TEXT = WHITE

# --- Definições de Fontes (Opcional, mas recomendado) ---
FONT_MONO = 'Consolas' # Ou 'monospace'
FONT_SANS = 'Arial' # Ou 'sans-serif'
FONT_SIZE_SM = 16
FONT_SIZE_MD = 18

# --- Layout (Os Retângulos de Posição) ---

# 1. Barra Lateral Esquerda (Professor e Objetivos)
LEFT_PANEL_WIDTH = 240
LEFT_PANEL_RECT = pygame.Rect(
    PADDING,
    PADDING,
    LEFT_PANEL_WIDTH,
    SCREEN_HEIGHT - (PADDING * 2)
)

# 1a. Posição da Imagem do Professor (dentro do painel esquerdo)
# (Assumindo uma imagem quadrada)
PROFESSOR_IMAGE_WIDTH = LEFT_PANEL_WIDTH - (PADDING * 2)
PROFESSOR_IMAGE_HEIGHT = PROFESSOR_IMAGE_WIDTH
PROFESSOR_RECT = pygame.Rect(
    LEFT_PANEL_RECT.left + PADDING,
    LEFT_PANEL_RECT.top + PADDING,
    PROFESSOR_IMAGE_WIDTH,
    PROFESSOR_IMAGE_HEIGHT
)

# 1b. Posição da Lista de Objetivos (dentro do painel esquerdo, abaixo do professor)
OBJECTIVE_LIST_RECT = pygame.Rect(
    LEFT_PANEL_RECT.left,
    PROFESSOR_RECT.bottom + PADDING,
    LEFT_PANEL_RECT.width,
    LEFT_PANEL_RECT.height - PROFESSOR_RECT.height - PADDING
)

# 2. Barra Inferior (Caixa de Entrada de Texto)
INPUT_BOX_HEIGHT = 100
INPUT_BOX_RECT = pygame.Rect(
    LEFT_PANEL_RECT.right + PADDING, # Começa à direita do painel esquerdo
    SCREEN_HEIGHT - INPUT_BOX_HEIGHT - PADDING,
    SCREEN_WIDTH - LEFT_PANEL_RECT.right - (PADDING * 2), # Largura restante
    INPUT_BOX_HEIGHT
)

# 3. Balão de Fala (Acima do Terminal)
SPEECH_BUBBLE_HEIGHT = 120
SPEECH_BUBBLE_RECT = pygame.Rect(
    LEFT_PANEL_RECT.right + PADDING,
    PADDING,
    INPUT_BOX_RECT.width, # Mesma largura da caixa de entrada
    SPEECH_BUBBLE_HEIGHT
)

# 4. Terminal (O restante do espaço)
TERMINAL_RECT = pygame.Rect(
    LEFT_PANEL_RECT.right + PADDING,
    SPEECH_BUBBLE_RECT.bottom + PADDING,
    INPUT_BOX_RECT.width, # Mesma largura
    INPUT_BOX_RECT.top - SPEECH_BUBBLE_RECT.bottom - (PADDING * 2) # Altura restante
)