#
# Arquivo: ui/objective_list.py
#
import pygame

# --- Cores (Exemplo, mova para settings.py depois) ---
COLOR_PANEL_BG = (20, 20, 30)      # Um azul-escuro/cinza
COLOR_PANEL_BORDER = (100, 100, 100) # Cinza
COLOR_TITLE_TEXT = (255, 255, 100) # Amarelo, para "OBJETIVOS"
COLOR_OBJECTIVE_TEXT = (220, 220, 220) # Branco-cinza
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
            
    def update(self):
        """Não precisa de atualização a cada frame."""
        pass 

    def draw(self, screen):
        """
        Desenha o painel, o título e o texto do objetivo.
        """
        # 1. Desenha o fundo e a borda
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2) # Borda
        
        # 2. Desenha o Título (centralizado)
        title_x_pos = self.rect.centerx - (self.title_rect.width // 2)
        title_y_pos = self.rect.top + self.padding
        screen.blit(self.title_surface, (title_x_pos, title_y_pos))
        
        # 3. Desenha uma linha separadora
        line_y = title_y_pos + self.title_rect.height + 5
        pygame.draw.line(
            screen, 
            self.border_color, 
            (self.rect.left + 5, line_y), 
            (self.rect.right - 5, line_y),
            1
        )
        
        # 4. Desenha cada linha de texto do objetivo
        
        # Posição Y inicial (abaixo da linha separadora)
        y_pos = line_y + 10
        
        for line_surface in self.rendered_lines:
            # Para de desenhar se o texto passar da altura do painel
            if y_pos + self.line_height > self.rect.bottom - self.padding:
                break
                
            # Posição X (com margem)
            x_pos = self.rect.left + self.padding
            
            screen.blit(line_surface, (x_pos, y_pos))
            
            # Move o Y para a próxima linha
            y_pos += self.line_height