#
# Arquivo: ui/objective_list.py
#
import pygame
from settings import *

# --- Cores (Exemplo, mova para settings.py depois) ---

# ---

class ObjectiveList:
    """
    Gerencia a exibição da lista de objetivos do jogador.
    Inclui lógica de quebra de linha (word wrap).
    """
    
    def __init__(self, rect):
        """
        Inicializa o painel de objetivos.
        'rect' é um pygame.Rect que define a posição e o tamanho.
        """
        self.rect = rect
        self.bg_color = COLOR_PANEL_BG
        self.border_color = COLOR_PANEL_BORDER
        
        # --- Estado do Texto ---
        self.rendered_lines = [] # Lista de Pygame Surfaces (o texto do objetivo)
        
        # --- Fontes ---
        try:
            # Fonte maior e em negrito para o título
            self.title_font = pygame.font.SysFont('Consolas', 18, bold=True)
            # Fonte normal para o texto
            self.font = pygame.font.SysFont('Consolas', 16)
        except:
            self.title_font = pygame.font.SysFont('monospace', 18, bold=True)
            self.font = pygame.font.SysFont('monospace', 16)
            
        self.line_height = self.font.get_height() + 3
        
        # --- Título ---
        self.title_text = "OBJETIVOS"
        self.title_surface = self.title_font.render(
            self.title_text, True, COLOR_TITLE_TEXT
        )
        self.title_rect = self.title_surface.get_rect()
        
        self.current_strikes = MAX_STRIKES

        # Margem interna
        self.padding = 10 

    def set_objective(self, new_text):
        """
        Define o novo texto do objetivo.
        Processa e quebra o texto em linhas imediatamente.
        """
        self.rendered_lines = []
        
        # Largura máxima de texto permitida
        max_width = self.rect.width - (self.padding * 2)
        
        # --- Lógica de Quebra de Linha (Word Wrap) ---
        words = new_text.split(' ')
        current_line_str = ""
        
        for word in words:
            test_line = current_line_str + word + " "
            
            if self.font.size(test_line)[0] <= max_width:
                current_line_str = test_line
            else:
                # Linha anterior está cheia, renderiza ela
                line_surface = self.font.render(
                    current_line_str, True, COLOR_OBJECTIVE_TEXT
                )
                self.rendered_lines.append(line_surface)
                
                # Começa nova linha
                current_line_str = word + " "
                
        # Adiciona a última linha que sobrou
        if current_line_str:
            line_surface = self.font.render(
                current_line_str, True, COLOR_OBJECTIVE_TEXT
            )
            self.rendered_lines.append(line_surface)
    
    def set_strikes(self, strikes):
        """Atualiza o número de strikes para desenhar."""
        self.current_strikes = strikes

    def update(self):
        """Não precisa de atualização a cada frame."""
        pass 

    def draw(self, screen):
        # 1. Desenha o fundo e a borda
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # 2. Desenha o Título (Topo)
        title_x_pos = self.rect.centerx - (self.title_surface.get_width() // 2)
        title_y_pos = self.rect.top + self.padding
        screen.blit(self.title_surface, (title_x_pos, title_y_pos))
        
        # Linha abaixo do título
        line_y = title_y_pos + self.title_surface.get_height() + 5
        pygame.draw.line(screen, self.border_color, (self.rect.left + 5, line_y), (self.rect.right - 5, line_y), 1)
        
        # --- 3. Desenha a Integridade (ANCORADA NO FUNDO) ---
        
        # Define alturas
        bar_height = 10
        label_text = "INTEGRIDADE:"
        label_surface = self.font.render(label_text, True, (150, 150, 150))
        
        # Calcula posições de baixo para cima
        # Fundo do painel - padding - altura da barra
        bar_y = self.rect.bottom - self.padding - bar_height 
        # Acima da barra - padding - altura do texto
        label_y = bar_y - 5 - label_surface.get_height()
        # Linha separadora acima da integridade
        integrity_sep_y = label_y - 10
        
        # Desenha Label
        screen.blit(label_surface, (self.rect.left + self.padding, label_y))
        
        # Desenha Barras
        total_width = self.rect.width - (self.padding * 2)
        bar_width = (total_width / MAX_STRIKES) - 2
        start_x = self.rect.left + self.padding
        
        for i in range(MAX_STRIKES):
            color = COLOR_STRIKE_GOOD if i < self.current_strikes else COLOR_STRIKE_BAD
            pygame.draw.rect(screen, color, (start_x + (i * (bar_width + 2)), bar_y, bar_width, bar_height))
            
        # Linha separadora da integridade
        pygame.draw.line(screen, self.border_color, (self.rect.left + 5, integrity_sep_y), (self.rect.right - 5, integrity_sep_y), 1)

        # --- 4. Desenha o Texto do Objetivo (NO ESPAÇO QUE SOBROU) ---
        
        # Começa abaixo do título
        text_y = line_y + 10
        
        for line_surface in self.rendered_lines:
            # Se a próxima linha for bater na área da integridade, PARE.
            if text_y + self.line_height > integrity_sep_y:
                break
                
            screen.blit(line_surface, (self.rect.left + self.padding, text_y))
            text_y += self.line_height