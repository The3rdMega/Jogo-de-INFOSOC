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
    Agora com redimensionamento dinâmico de fonte e word wrap.
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
        
        # --- CÁLCULO DINÂMICO DE FONTE ---
        # Queremos que caibam aproximadamente 22 linhas na altura do terminal.
        target_lines = 22
        # Calcula o tamanho em pixels baseado na altura do retangulo
        calculated_size = int(self.rect.height / target_lines)
        
        # Define limites: mínimo 12 (para ler) e máximo 32 (para não ficar gigante)
        self.font_size = max(12, min(calculated_size, 32))

        # --- Renderização de Fonte ---
        try:
            # Usa sua fonte escolhida com o tamanho calculado
            self.font = pygame.font.SysFont('ByteBounce', self.font_size)
        except:
            # Fallback
            self.font = pygame.font.SysFont('monospace', self.font_size)
            
        self.font_color = COLOR_TERMINAL_TEXT
        # Pega a altura real da linha da fonte carregada
        self.line_height = self.font.get_linesize() 
        
        # --- Cursor Piscando ---
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_rate = 500 # em milissegundos

        # --- Tecla Segurada ---
        self.key_held = None             # Armazena o CÓDIGO da tecla
        self.key_held_unicode = None     # Armazena o CARACTERE da tecla
        self.key_repeat_timer = 0        # Timer para controlar a repetição
        self.key_repeat_delay = 400      # Atraso inicial
        self.key_repeat_rate = 30        # Taxa de repetição
        
    
    def activate_input(self, prompt, expected_command):
        """Ativa o modo de entrada de comando."""
        self.is_active = True
        self.current_prompt = prompt + " " 
        self.expected_command = expected_command
        self.current_line = ""
        self.event_image = None 
        self.key_held = None 

    def deactivate_input(self):
        """Desativa o modo de entrada."""
        self.is_active = False
        self.current_prompt = ""
        self.current_line = ""
        self.key_held = None 
    
    # --- SISTEMA DE WORD WRAP (Quebra de Linha) ---
    def _wrap_text(self, text):
        """
        Recebe uma string e retorna uma lista de strings,
        garantindo que nenhuma ultrapasse a largura do terminal.
        """
        words = text.split(' ')
        wrapped_lines = []
        current_line = ""
        
        # Margem de segurança (padding lateral)
        max_width = self.rect.width - 15 
        
        for word in words:
            # Testa a linha com a nova palavra
            test_line = current_line + word + " "
            text_width, _ = self.font.size(test_line)
            
            if text_width < max_width:
                current_line = test_line
            else:
                # A linha estourou o limite!
                if current_line:
                    wrapped_lines.append(current_line)
                    current_line = word + " "
                else:
                    # Caso a palavra sozinha seja maior que a tela
                    wrapped_lines.append(word)
                    current_line = ""
                    
        if current_line:
            wrapped_lines.append(current_line)
            
        return wrapped_lines

    def add_to_history(self, text_block):
        """
        Adiciona um bloco de texto ao histórico.
        Processa quebra de linha automática.
        """
        if text_block == "...":
            return
            
        # Primeiro quebra os \n explícitos
        raw_lines = text_block.split('\n')
        
        for line in raw_lines:
            # Para cada linha, aplica o word wrap dinâmico
            wrapped = self._wrap_text(line)
            self.history.extend(wrapped)
            
    def clear_history(self):
        """Limpa o histórico do terminal."""
        self.history = []

    def show_event_image(self, image_path):
        """Carrega e exibe uma imagem sobre o terminal."""
        if image_path is None:
            self.event_image = None
            return
            
        try:
            image = pygame.image.load(image_path).convert_alpha()
            self.event_image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        except Exception as e:
            print(f"Erro ao carregar imagem do evento: {e}")
            self.event_image = None
            self.add_to_history(f"[Erro: Imagem {image_path} nao encontrada]")

    def handle_event(self, event):
        """
        Processa um único evento do Pygame (teclado).
        """
        if not self.is_active:
            return None

        # --- EVENTO DE SOLTAR A TECLA ---
        if event.type == pygame.KEYUP:
            if event.key == self.key_held:
                self.key_held = None
                self.key_held_unicode = None
            return None

        # --- EVENTO DE PRESSIONAR A TECLA ---
        if event.type == pygame.KEYDOWN:
            self.key_held = event.key
            self.key_held_unicode = event.unicode
            self.key_repeat_timer = pygame.time.get_ticks() + self.key_repeat_delay

            # --- Executa a Ação da Tecla (primeira vez) ---
            
            if event.key == pygame.K_RETURN:
                command_typed = self.current_line.strip()
                
                # Adiciona o que o jogador digitou ao histórico (com wrap!)
                self.add_to_history(self.current_prompt + command_typed)
                self.current_line = "" 
                self.key_held = None 
                
                if command_typed.lower() == self.expected_command.lower():
                    self.deactivate_input()
                    return "correct_command"
                else:
                    self.add_to_history(f"bash: command not found: {command_typed}")
                    return "incorrect_command"
                    
            elif event.key == pygame.K_BACKSPACE:
                self.current_line = self.current_line[:-1]
                
            else:
                # Verifica se cabe visualmente antes de adicionar
                prompt_width, _ = self.font.size(self.current_prompt + self.current_line + event.unicode)
                if prompt_width < self.rect.width - 15:
                    self.current_line += event.unicode
                    
            return None 
            
        return None 

    def update(self):
        """Atualiza o estado interno."""
        now = pygame.time.get_ticks() 
        
        # Cursor piscando
        if now - self.cursor_timer > self.cursor_blink_rate:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now

        # Repetição de Tecla
        if self.key_held and self.is_active: 
            if now >= self.key_repeat_timer:
                
                if self.key_held == pygame.K_BACKSPACE:
                    self.current_line = self.current_line[:-1]
                
                elif self.key_held != pygame.K_RETURN: 
                    prompt_width, _ = self.font.size(self.current_prompt + self.current_line + self.key_held_unicode)
                    if prompt_width < self.rect.width - 15:
                        self.current_line += self.key_held_unicode
                
                self.key_repeat_timer = now + self.key_repeat_rate

    def draw(self, screen):
        """Desenha o terminal na tela."""
        # 1. Desenha o fundo
        pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # 2. Se houver uma imagem de evento, desenha ela e encerra
        if self.event_image:
            screen.blit(self.event_image, self.rect.topleft)
            return
            
        # 3. Calcula quantas linhas cabem na tela (baseado na fonte atual)
        #    Isso garante que sempre desenhamos o máximo possível.
        max_lines_fit = int(self.rect.height // self.line_height)
        
        y_pos = self.rect.bottom - self.line_height
        
        # 4. Desenha a linha de comando ATIVA (se estiver ativa)
        if self.is_active:
            prompt_text = self.current_prompt + self.current_line
            if self.cursor_visible:
                prompt_text += "_"
                
            prompt_surface = self.font.render(prompt_text, True, COLOR_TERMINAL_PROMPT)
            screen.blit(prompt_surface, (self.rect.left + 5, y_pos))
            y_pos -= self.line_height
            
        # 5. Desenha o histórico (de baixo para cima)
        #    Como o histórico já foi quebrado pelo _wrap_text, só precisamos desenhar.
        lines_to_draw = self.history[-(max_lines_fit-1):] if self.is_active else self.history[-max_lines_fit:]
        
        for line in reversed(lines_to_draw):
            if y_pos < self.rect.top:
                break
                
            line_surface = self.font.render(line, True, self.font_color)
            screen.blit(line_surface, (self.rect.left + 5, y_pos))
            y_pos -= self.line_height