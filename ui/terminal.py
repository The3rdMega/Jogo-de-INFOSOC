#
# Arquivo: ui/terminal.py
#
import pygame

# --- Cores (Exemplo, mova para settings.py depois) ---
COLOR_TERMINAL_BG = (10, 10, 25) # Um azul-quase-preto
COLOR_TERMINAL_TEXT = (25, 255, 25) # Verde "hacker"
COLOR_TERMINAL_PROMPT = (100, 255, 100) # Verde mais claro para o prompt
# ---

class InteractiveTerminal:
    """
    Gerencia a exibição do terminal, o histórico de texto e a entrada de comandos.
    """
    
    def __init__(self, rect):
        """
        Inicializa o terminal.
        'rect' é um pygame.Rect que define a posição e o tamanho.
        """
        self.rect = rect
        self.bg_color = COLOR_TERMINAL_BG
        
        # --- Estado do Terminal ---
        self.is_active = False # Está aceitando comandos?
        self.history = [] # Lista de strings, cada string é uma linha
        self.event_image = None # Usado para mostrar o asset (ex: Minions)
        
        # --- Estado da Linha de Comando ---
        self.current_prompt = "" # Ex: "user@professor-pc:~$"
        self.current_line = "" # O que o jogador está digitando
        self.expected_command = None # A resposta correta
        
        # --- Renderização de Fonte ---
        # (Você deve carregar a fonte uma vez e passar para cá,
        # mas por simplicidade, vamos carregar aqui)
        try:
            # Tenta carregar uma fonte monoespaçada legal
            self.font = pygame.font.SysFont('Consolas', 16)
        except:
            # Fallback
            self.font = pygame.font.SysFont('monospace', 16)
            
        self.font_color = COLOR_TERMINAL_TEXT
        self.line_height = self.font.get_height() + 2 # +2px de espaçamento
        
        # --- Cursor Piscando ---
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_rate = 500 # em milissegundos
        
    
    def activate_input(self, prompt, expected_command):
        """Ativa o modo de entrada de comando (para 'await_command')."""
        self.is_active = True
        self.current_prompt = prompt + " " # Adiciona espaço
        self.expected_command = expected_command
        self.current_line = ""
        self.event_image = None # Garante que nenhuma imagem esteja visível
        
    def deactivate_input(self):
        """Desativa o modo de entrada (para 'auto_proceed' ou 'ask_question')."""
        self.is_active = False
        self.current_prompt = ""
        self.current_line = ""
        
    def add_to_history(self, text_block):
        """
        Adiciona um bloco de texto ao histórico.
        Quebra automaticamente em novas linhas.
        """
        # Se for "...", não faz nada (comando para manter o terminal)
        if text_block == "...":
            return
            
        for line in text_block.split('\n'):
            self.history.append(line)
            
    def clear_history(self):
        """Limpa o histórico do terminal."""
        self.history = []

    def show_event_image(self, image_path):
        """
        Carrega e exibe uma imagem sobre o terminal (para 'terminal_event_display').
        Se image_path for None, limpa a imagem.
        """
        if image_path is None:
            self.event_image = None
            return
            
        try:
            image = pygame.image.load(image_path).convert_alpha()
            # Redimensiona a imagem para caber no Rect do terminal
            self.event_image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        except Exception as e:
            print(f"Erro ao carregar imagem do evento: {e}")
            self.event_image = None
            self.add_to_history(f"[Erro: Imagem {image_path} não encontrada]")

    def handle_event(self, event):
        """
        Processa um único evento do Pygame (teclado).
        Deve ser chamado pelo 'gameplay.py'.
        Retorna um status (string) se uma ação foi concluída.
        """
        if not self.is_active or event.type != pygame.KEYDOWN:
            return None # Não faz nada se não estiver ativo
            
        if event.key == pygame.K_RETURN:
            # --- Jogador pressionou Enter ---
            command_typed = self.current_line.strip()
            
            # Adiciona o que o jogador digitou ao histórico
            self.add_to_history(self.current_prompt + command_typed)
            self.current_line = "" # Limpa a linha de entrada
            
            # Compara com o comando esperado
            if command_typed.lower() == self.expected_command.lower():
                self.deactivate_input()
                return "correct_command"
            else:
                # Feedback de comando errado
                self.add_to_history(f"bash: command not found: {command_typed}")
                return "incorrect_command"
                
        elif event.key == pygame.K_BACKSPACE:
            # --- Jogador pressionou Backspace ---
            self.current_line = self.current_line[:-1]
            
        else:
            # --- Outra tecla (letra, número, símbolo) ---
            # Garante que o texto não ultrapasse a largura do terminal
            if self.font.size(self.current_prompt + self.current_line)[0] < self.rect.width - 15:
                self.current_line += event.unicode
                
        return None # Nenhum evento de "fim de ação"

    def update(self):
        """
        Atualiza o estado interno do terminal (ex: cursor piscando).
        Deve ser chamado a cada frame pelo 'gameplay.py'.
        """
        # Lógica do cursor piscando
        now = pygame.time.get_ticks()
        if now - self.cursor_timer > self.cursor_blink_rate:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now

    def draw(self, screen):
        """
        Desenha o terminal na tela.
        Deve ser chamado a cada frame pelo 'gameplay.py'.
        """
        # 1. Desenha o fundo
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # 2. Se houver uma imagem de evento, desenha ela e encerra
        if self.event_image:
            screen.blit(self.event_image, self.rect.topleft)
            return
            
        # 3. Calcula quantas linhas cabem na tela
        max_lines_fit = self.rect.height // self.line_height
        
        # Posição Y inicial (começa no fundo)
        y_pos = self.rect.bottom - self.line_height
        
        # 4. Desenha a linha de comando ATIVA (se estiver ativa)
        if self.is_active:
            # Monta o texto do prompt + o que o jogador está digitando
            prompt_text = self.current_prompt + self.current_line
            
            # Adiciona o cursor piscando
            if self.cursor_visible:
                prompt_text += "_"
                
            # Renderiza o prompt
            prompt_surface = self.font.render(prompt_text, True, COLOR_TERMINAL_PROMPT)
            screen.blit(prompt_surface, (self.rect.left + 5, y_pos))
            
            # Move o Y para cima para dar espaço ao histórico
            y_pos -= self.line_height
            
        # 5. Desenha o histórico (de baixo para cima)
        
        # Pega apenas as últimas 'max_lines_fit' linhas do histórico
        lines_to_draw = self.history[-(max_lines_fit-1):] if self.is_active else self.history[-max_lines_fit:]
        
        for line in reversed(lines_to_draw):
            # Para de desenhar se sair do topo do Rect
            if y_pos < self.rect.top:
                break
                
            line_surface = self.font.render(line, True, self.font_color)
            screen.blit(line_surface, (self.rect.left + 5, y_pos))
            
            # Move o Y para a próxima linha (para cima)
            y_pos -= self.line_height