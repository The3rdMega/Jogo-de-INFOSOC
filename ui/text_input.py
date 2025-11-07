#
# Arquivo: ui/text_input.py
#
import pygame

# --- Cores (Exemplo, mova para settings.py depois) ---
COLOR_INPUT_BG = (30, 30, 30) # Cinza escuro
COLOR_INPUT_BORDER = (100, 100, 100) # Cinza
COLOR_PROMPT_TEXT = (255, 255, 100) # Amarelo para a pergunta
COLOR_INPUT_TEXT = (255, 255, 255) # Branco para o texto do jogador
# ---

class TextInputBox:
    """
    Gerencia a caixa de entrada de resposta (para 'ask_question').
    Esta é a caixa na "barra de baixo" do layout.
    """
    
    def __init__(self, rect):
        """
        Inicializa a caixa de entrada.
        'rect' é um pygame.Rect que define a posição e o tamanho.
        """
        self.rect = rect
        self.bg_color = COLOR_INPUT_BG
        self.border_color = COLOR_INPUT_BORDER
        
        # --- Estado da Caixa ---
        self.is_active = False
        self.prompt_text = "" # A pergunta (ex: "Qual IP...?")
        self.current_text = "" # O que o jogador está digitando
        
        # 'answer_data' pode ser uma string (para ask_question)
        # ou um dict (para ask_question_branching)
        self.answer_data = None 
        
        # --- Renderização de Fonte ---
        try:
            self.font = pygame.font.SysFont('ByteBounce', 30)
        except:
            self.font = pygame.font.SysFont('monospace', 18)
            
        self.prompt_color = COLOR_PROMPT_TEXT
        self.input_color = COLOR_INPUT_TEXT
        self.line_height = self.font.get_height() + 5
        
        # --- Cursor Piscando ---
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_rate = 500 # ms

        # --- Tecla Segurada ---
        self.key_held = None             # Armazena o CÓDIGO da tecla (ex: K_BACKSPACE, K_a)
        self.key_held_unicode = None     # Armazena o CARACTERE da tecla (ex: 'a')
        self.key_repeat_timer = 0        # Timer para controlar a repetição
        self.key_repeat_delay = 400      # Atraso inicial antes de repetir (400ms)
        self.key_repeat_rate = 30        # Taxa de repetição (a cada 30ms)
        
    def activate(self, prompt, answer_data):
        """Ativa a caixa de entrada com uma nova pergunta."""
        self.is_active = True
        self.prompt_text = prompt
        self.answer_data = answer_data
        self.current_text = "" # Limpa a resposta anterior
        self.cursor_visible = True
        self.key_held = None # Garante que reseta ao ativar
        
    def deactivate(self):
        """Desativa a caixa de entrada."""
        self.is_active = False
        self.prompt_text = ""
        self.current_text = ""
        self.answer_data = None
        self.key_held = None # Garante que reseta ao desativar
        
    def handle_event(self, event):
        """
        Processa um único evento do Pygame (teclado).
        Retorna um status se uma ação foi concluída.
        """
        if not self.is_active:
            return None

        # --- EVENTO DE SOLTAR A TECLA ---
        if event.type == pygame.KEYUP:
            # Se a tecla que foi solta é a mesma que estávamos rastreando
            if event.key == self.key_held:
                self.key_held = None # Para de rastrear
                self.key_held_unicode = None
            return None

        # --- EVENTO DE PRESSIONAR A TECLA ---
        if event.type == pygame.KEYDOWN:
            # Armazena qual tecla está sendo segurada
            self.key_held = event.key
            self.key_held_unicode = event.unicode
            
            # Define o timer para o *atraso inicial*
            self.key_repeat_timer = pygame.time.get_ticks() + self.key_repeat_delay
            
            # --- Executa a Ação da Tecla (primeira vez) ---
            
            if event.key == pygame.K_RETURN:
                # --- Jogador pressionou Enter ---
                user_answer = self.current_text.strip().lower()
                self.current_text = ""
                self.key_held = None # Enter não se repete
                
                # --- Lógica de verificação de resposta (sem mudança) ---
                if isinstance(self.answer_data, str):
                    expected = self.answer_data.lower()
                    return "correct" if user_answer == expected else "incorrect"
                
                elif isinstance(self.answer_data, dict):
                    if user_answer in self.answer_data:
                        handler = self.answer_data[user_answer]
                        if handler["action"] == "proceed":
                            return "correct"
                        elif handler["action"] == "show_event":
                            return handler 
                    else:
                        return "invalid_option"
                return None
            
            elif event.key == pygame.K_BACKSPACE:
                # --- Jogador pressionou Backspace ---
                self.current_text = self.current_text[:-1] # Apaga um
            
            else:
                # --- Outra tecla (letra, número, símbolo) ---
                # Garante que o texto não ultrapasse a largura da caixa
                prompt_width = self.font.size("> " + self.current_text)[0]
                if prompt_width < self.rect.width - 20:
                    self.current_text += event.unicode # Adiciona um
                    
            return None # Evento de KEYDOWN processado
            
        return None # Nenhum evento de "fim de ação"

    def update(self):
        """Atualiza o estado interno (cursor E REPETIÇÃO DE TECLA)."""
        if not self.is_active:
            return
            
        now = pygame.time.get_ticks() # Pega o tempo atual
            
        # Lógica do cursor piscando (sem mudança)
        if now - self.cursor_timer > self.cursor_blink_rate:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now
            
        # --- LÓGICA DE REPETIÇÃO DE TECLA (MODIFICADA) ---
        if self.key_held: # Se *qualquer* tecla estiver sendo segurada
            
            # Se o timer de repetição estourou
            if now >= self.key_repeat_timer:
                
                # Executa a ação da tecla *novamente*
                
                if self.key_held == pygame.K_BACKSPACE:
                    self.current_text = self.current_text[:-1]
                
                # Não repete o Enter, só teclas de texto
                elif self.key_held != pygame.K_RETURN: 
                    prompt_width = self.font.size("> " + self.current_text)[0]
                    if prompt_width < self.rect.width - 20:
                         # Usa o caractere unicode que salvamos
                        self.current_text += self.key_held_unicode
                
                # Reinicia o timer para a *taxa de repetição* (mais rápida)
                self.key_repeat_timer = now + self.key_repeat_rate

    def draw(self, screen):
        """Desenha a caixa de entrada na tela."""
        if not self.is_active:
            return # Não desenha nada se estiver inativo
            
        # 1. Desenha o fundo e a borda
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2) # Borda de 2px
        
        # 2. Desenha o Prompt (A Pergunta)
        prompt_surface = self.font.render(self.prompt_text, True, self.prompt_color)
        screen.blit(prompt_surface, (self.rect.left + 10, self.rect.top + 10))
        
        # 3. Desenha a Linha de Entrada do Jogador
        
        # Monta o texto de entrada (com cursor)
        input_display_text = "> " + self.current_text
        if self.cursor_visible:
            input_display_text += "_"
            
        input_surface = self.font.render(input_display_text, True, self.input_color)
        
        # Posição da linha de entrada (abaixo do prompt)
        input_y_pos = self.rect.top + self.line_height + 15 
        screen.blit(input_surface, (self.rect.left + 10, input_y_pos))