#
# Arquivo: ui/speech_bubble.py
#
import pygame

# --- Cores (Exemplo, mova para settings.py depois) ---
COLOR_BUBBLE_BG = (230, 230, 230) # Cinza claro
COLOR_BUBBLE_BORDER = (10, 10, 10) # Preto
COLOR_BUBBLE_TEXT = (10, 10, 10) # Preto
# ---

class SpeechBubble:
    """
    Gerencia a exibição do balão de fala do professor.
    Inclui lógica de quebra de linha (word wrap).
    """
    
    def __init__(self, rect):
        """
        Inicializa o balão de fala.
        'rect' é um pygame.Rect que define a posição e o tamanho.
        """
        self.rect = rect
        self.bg_color = COLOR_BUBBLE_BG
        self.border_color = COLOR_BUBBLE_BORDER
        self.text_color = COLOR_BUBBLE_TEXT
        
        # --- Estado do Texto ---
        # self.rendered_lines será uma lista de Pygame Surfaces,
        # prontas para serem desenhadas (blitted).
        self.rendered_lines = []
        
        # --- Fonte ---
        try:
            self.font = pygame.font.SysFont('Arial', 16) # Uma fonte mais "normal"
        except:
            self.font = pygame.font.SysFont('sans-serif', 16)
            
        self.line_height = self.font.get_height() + 2
        
        # Margem interna do balão
        self.padding = 25

        try:
            # 1. Carrega sua imagem PNG
            raw_image = pygame.image.load("assets/images/balao_fala.png").convert_alpha()
            # 2. Redimensiona a imagem para o tamanho exato do Rect
            self.image = pygame.transform.scale(raw_image, (self.rect.width, self.rect.height))
        except Exception as e:
            print(f"ERRO: Não foi possível carregar 'assets/images/balao_fala.png': {e}")
            # 3. Plano B: Se falhar, self.image fica None
            self.image = None
            # E guardamos as cores do fallback
            self.fallback_bg = COLOR_BUBBLE_BG
            self.fallback_border = COLOR_BUBBLE_BORDER

    def set_text(self, new_text):
        """
        Define o novo texto do balão.
        Processa e quebra o texto em linhas imediatamente.
        """
        self.rendered_lines = []
        
        # Largura máxima de texto permitida dentro do balão
        max_width = self.rect.width - (self.padding * 2)
        
        # --- Lógica de Quebra de Linha (Word Wrap) ---
        words = new_text.split(' ')
        current_line_str = ""
        
        for word in words:
            # Testa se a palavra cabe na linha atual
            test_line = current_line_str + word + " "
            
            if self.font.size(test_line)[0] <= max_width:
                # Palavra cabe, adiciona à linha atual
                current_line_str = test_line
            else:
                # Palavra não cabe, "fecha" a linha anterior
                line_surface = self.font.render(current_line_str, True, self.text_color)
                self.rendered_lines.append(line_surface)
                
                # Começa uma nova linha com a palavra atual
                current_line_str = word + " "
                
        # Adiciona a última linha que sobrou
        if current_line_str:
            line_surface = self.font.render(current_line_str, True, self.text_color)
            self.rendered_lines.append(line_surface)
            
    def update(self):
        """
        Função de atualização.
        Este componente é simples e não precisa de lógica de update,
        mas mantemos a função por consistência.
        """
        pass # Nada para atualizar a cada frame

    def draw(self, screen):
        """
        Desenha o balão de fala e o texto dentro dele.
        """
        # 1. Desenha o fundo e a borda
        # (Nota: um balão de fala real teria uma "ponta",
        # mas por enquanto um retângulo funciona)

        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            # 1. (Plano B) Desenha o retângulo cinza se a imagem falhou
            pygame.draw.rect(screen, self.fallback_bg, self.rect)
            pygame.draw.rect(screen, self.fallback_border, self.rect, 2)
        
        # 2. Desenha cada linha de texto renderizada
        
        # Posição Y inicial (com margem)
        y_pos = self.rect.top + self.padding
        
        for line_surface in self.rendered_lines:
            # Para de desenhar se o texto passar da altura do balão
            if y_pos + self.line_height > self.rect.bottom - self.padding:
                break
                
            # Posição X (com margem)
            x_pos = self.rect.left + self.padding
            
            screen.blit(line_surface, (x_pos, y_pos))
            
            # Move o Y para a próxima linha
            y_pos += self.line_height