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
        
    def activate(self, prompt, answer_data):
        """Ativa a caixa de entrada com uma nova pergunta."""
        self.is_active = True
        self.prompt_text = prompt
        self.answer_data = answer_data
        self.current_text = "" # Limpa a resposta anterior
        self.cursor_visible = True
        
    def deactivate(self):
        """Desativa a caixa de entrada."""
        self.is_active = False
        self.prompt_text = ""
        self.current_text = ""
        self.answer_data = None
        
    def handle_event(self, event):
        """
        Processa um único evento do Pygame (teclado).
        Retorna um status se uma ação foi concluída.
        """
        if not self.is_active or event.type != pygame.KEYDOWN:
            return None # Não faz nada se não estiver ativo
            
        if event.key == pygame.K_RETURN:
            # --- Jogador pressionou Enter ---
            user_answer = self.current_text.strip().lower()
            
            # Limpa a linha de entrada atual
            self.current_text = ""
            
            # --- Lógica de verificação de resposta ---
            
            # 1. Caso: 'ask_question' (resposta simples)
            if isinstance(self.answer_data, str):
                expected = self.answer_data.lower()
                if user_answer == expected:
                    self.deactivate()
                    return "correct" # Resposta correta simples
                else:
                    return "incorrect" # Resposta errada simples
            
            # 2. Caso: 'ask_question_branching' (múltiplas respostas)
            elif isinstance(self.answer_data, dict):
                if user_answer in self.answer_data:
                    handler = self.answer_data[user_answer]
                    
                    if handler["action"] == "proceed":
                        self.deactivate()
                        return "correct" # Resposta correta que avança a história
                    elif handler["action"] == "show_event":
                        # Retorna o dicionário de evento inteiro
                        # para o gameplay.py processar
                        return handler 
                else:
                    # O jogador digitou algo que não é uma opção
                    return "invalid_option"
                    
            return None # Não deve chegar aqui
            
        elif event.key == pygame.K_BACKSPACE:
            # --- Jogador pressionou Backspace ---
            self.current_text = self.current_text[:-1]
            
        else:
            # --- Outra tecla (letra, número, símbolo) ---
            # Garante que o texto não ultrapasse a largura da caixa
            prompt_width = self.font.size("> " + self.current_text)[0]
            if prompt_width < self.rect.width - 20: # 20px de margem
                self.current_text += event.unicode
                
        return None # Nenhum evento de "fim de ação"

    def update(self):
        """Atualiza o estado interno (cursor)."""
        if not self.is_active:
            return
            
        # Lógica do cursor piscando
        now = pygame.time.get_ticks()
        if now - self.cursor_timer > self.cursor_blink_rate:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now

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