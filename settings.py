#
# Arquivo: settings.py
# (Com layout proporcional)
#
import pygame

COLOR_PANEL_BG = (20, 20, 30)      # Um azul-escuro/cinza
COLOR_PANEL_BORDER = (100, 100, 100) # Cinza
COLOR_TITLE_TEXT = (255, 255, 100) # Amarelo, para "OBJETIVOS"
COLOR_OBJECTIVE_TEXT = (220, 220, 220) # Branco-cinza

# --- 1. MUDE AQUI O TAMANHO DA TELA ---
# Tente 800x600, ou o que couber no seu notebook
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# --- FIM DA MUDANÇA PRINCIPAL ---

FPS = 60

# --- Padding (Espaçamento) ---
# Deixar o padding fixo em 10 pixels geralmente funciona bem
PADDING = 10

# --- Definições de Cores (Sem mudança) ---
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
# ... (e todas as suas outras cores) ...

# --- Layout (Os Retângulos de Posição) ---
# AGORA TUDO É CALCULADO COM BASE NO TAMANHO DA TELA

# 1. Barra Lateral Esquerda (Professor e Objetivos)
# (O painel tinha 240px de largura quando a tela era 1024px)
LEFT_PANEL_WIDTH = int(SCREEN_WIDTH * (240 / 1024)) # <-- Mágica proporcional
LEFT_PANEL_RECT = pygame.Rect(
    PADDING,
    PADDING,
    LEFT_PANEL_WIDTH,
    SCREEN_HEIGHT - (PADDING * 2)
)

# 1a. Posição da Imagem do Professor (se ajusta ao painel)
PROFESSOR_IMAGE_WIDTH = LEFT_PANEL_WIDTH - (PADDING * 2)
PROFESSOR_IMAGE_HEIGHT = PROFESSOR_IMAGE_WIDTH # Mantém quadrado
PROFESSOR_RECT = pygame.Rect(
    LEFT_PANEL_RECT.left + PADDING,
    LEFT_PANEL_RECT.top + PADDING,
    PROFESSOR_IMAGE_WIDTH,
    PROFESSOR_IMAGE_HEIGHT
)

# 1b. Posição da Lista de Objetivos (preenche o resto do painel)
OBJECTIVE_LIST_RECT = pygame.Rect(
    LEFT_PANEL_RECT.left,
    PROFESSOR_RECT.bottom + PADDING,
    LEFT_PANEL_RECT.width,
    LEFT_PANEL_RECT.height - PROFESSOR_RECT.height - PADDING * 2 # Ajuste de padding
)

# 2. Barra Inferior (Caixa de Entrada de Texto)
# (Tinha 100px de altura quando a tela era 768px)
INPUT_BOX_HEIGHT = int(SCREEN_HEIGHT * (100 / 768)) # <-- Mágica proporcional
INPUT_BOX_RECT = pygame.Rect(
    LEFT_PANEL_RECT.right + PADDING, 
    SCREEN_HEIGHT - INPUT_BOX_HEIGHT - PADDING,
    SCREEN_WIDTH - LEFT_PANEL_RECT.right - (PADDING * 2), # Largura restante
    INPUT_BOX_HEIGHT
)

# 3. Balão de Fala (Acima do Terminal)
# (Tinha 120px de altura quando a tela era 768px)
SPEECH_BUBBLE_HEIGHT = int(SCREEN_HEIGHT * (160 / 768)) # <-- Mágica proporcional
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

# 5. Sistema de Vida
MAX_STRIKES = 5
COLOR_STRIKE_GOOD = (50, 255, 50) # Verde
COLOR_STRIKE_BAD = (255, 50, 50)   # Vermelho