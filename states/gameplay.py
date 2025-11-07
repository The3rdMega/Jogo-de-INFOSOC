#
# Arquivo: states/gameplay.py
#
import pygame

# Importa o "molde" do estado
from states.base_state import BaseState

# Importa o cérebro (a história)
from story import STORY_STEPS

# Importa o layout (posições e cores)
# Usar '*' aqui é seguro, pois settings.py só contém constantes
from settings import *

# Importa todos os nossos componentes de UI
from ui.terminal import InteractiveTerminal
from ui.text_input import TextInputBox
from ui.speech_bubble import SpeechBubble
from ui.objective_list import ObjectiveList


class GameplayState(BaseState):
    """
    Este é o estado principal do jogo, onde toda a interação acontece.
    Ele gerencia todos os componentes da UI e a progressão da história.
    """
    
    def __init__(self):
        super().__init__()
        # Indice da fala do professor
        self.current_speech_index = 0

        # Para onde ir quando este estado terminar (self.done = True)
        self.next_state = "END_SCREEN" 
        
        # Rastreia qual passo da história estamos
        self.current_step = 0
        
        # Timer para os passos de 'auto_proceed'
        self.auto_proceed_timer = None
        self.auto_proceed_delay = 0

        # Flag para saber se estamos mostrando um evento (ex: facebook)
        self.showing_event_image = False
        self.event_image_timer = None
        self.event_image_duration = 5000 # ms

        # --- Carregar Assets Estáticos ---
        # (Você precisará criar esta pasta e imagem)
        try:
            professor_img_raw = pygame.image.load("assets/images/professor.png").convert_alpha()
            self.professor_image = pygame.transform.scale(
                professor_img_raw, (PROFESSOR_RECT.width, PROFESSOR_RECT.height)
            )
        except Exception as e:
            print(f"Erro ao carregar imagem do professor: {e}")
            # Cria um substituto para o jogo não quebrar
            self.professor_image = pygame.Surface((PROFESSOR_RECT.width, PROFESSOR_RECT.height))
            self.professor_image.fill((255, 0, 255)) # Rosa-choque indica asset faltando

        # --- Instanciar todos os Componentes da UI ---
        # (Passando os RECTs do settings.py)
        self.terminal = InteractiveTerminal(TERMINAL_RECT)
        self.input_box = TextInputBox(INPUT_BOX_RECT)
        self.speech_bubble = SpeechBubble(SPEECH_BUBBLE_RECT)
        self.objective_list = ObjectiveList(OBJECTIVE_LIST_RECT)
        

    def close_event_image(self):
        """
        Rotina auxiliar para fechar a imagem do evento.
        Restaura o estado para continuar a pergunta.
        """
        self.showing_event_image = False
        self.event_image_timer = None # <-- Reseta o timer
        self.terminal.show_event_image(None)
        
        # Restaura a fala original da pergunta
        step_data = STORY_STEPS[self.current_step]
        self.speech_bubble.set_text(step_data.get("professor_speech"))
    
    def startup(self, persistent_data):
        """Chamado uma vez quando o estado começa (depois da cutscene)."""
        super().startup(persistent_data)
        
        # Reseta o estado
        self.current_step = 0
        self.terminal.clear_history()
        
        # Carrega o primeiro passo da história
        self.load_story_step(self.current_step)

    def load_story_step(self, step_index):
        """
        A função MAIS IMPORTANTE.
        Lê um passo da história e configura toda a UI.
        """
        
        # 1. Verifica se a história terminou
        if step_index >= len(STORY_STEPS):
            print("Fim da história!")
            self.done = True # Sinaliza ao main.py para trocar de estado
            return
            
        # 2. Reseta o timer de auto-avanço
        self.auto_proceed_timer = None
            
        # 3. Pega os dados do passo atual
        self.current_step = step_index
        step_data = STORY_STEPS[self.current_step]
        
        # 4. Atualiza os componentes de "saída" (display)
        self.speech_list = step_data.get("professor_speech", ())
        print(self.speech_list)
        # Mostra automaticamente a primeira fala, se houver
        if self.speech_list:
            self.speech_bubble.set_text(self.speech_list[self.current_speech_index])
            
        if step_data.get("objective"):
            self.objective_list.set_objective(step_data.get("objective"))
            
        if step_data.get("terminal_text"):
            self.terminal.add_to_history(step_data.get("terminal_text"))

        # 5. Configura os componentes de "entrada" (ação)
        action = step_data.get("action_type")
        
        if action == "await_command":
            self.terminal.activate_input(
                step_data.get("command_prompt"),
                step_data.get("expected_command")
            )
            self.input_box.deactivate()
            
        elif action == "ask_question":
            self.terminal.deactivate_input()
            self.input_box.activate(
                step_data.get("question_prompt"),
                step_data.get("expected_answer")
            )
            
        elif action == "ask_question_branching":
            self.terminal.deactivate_input()
            self.input_box.activate(
                step_data.get("question_prompt"),
                step_data.get("answer_handlers")
            )
            
        elif action == "auto_proceed":
            self.terminal.deactivate_input()
            self.input_box.deactivate()
            # Ativa o timer para avançar automaticamente
            self.auto_proceed_timer = pygame.time.get_ticks()
            self.auto_proceed_delay = step_data.get("next_step_delay", 1000)
            
        else: # Caso padrão (ex: fim do jogo)
            self.terminal.deactivate_input()
            self.input_box.deactivate()

    def proceed_to_next_step(self):
        """Função helper para carregar o próximo passo."""
        # Limpa qualquer imagem de evento (ex: Minions)
        self.terminal.show_event_image(None)
        
        self.load_story_step(self.current_step + 1)

    def handle_event(self, event):
        """
        Passa os eventos (teclado/mouse) para o componente ATIVO.
        """
        super().handle_event(event) # Lida com o evento QUIT
        
        result = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.speech_list:
                self.advance_speech()
        if self.showing_event_image:
            # Se estivermos mostrando uma imagem de evento,
            # qualquer clique fecha a imagem e retorna ao input.
            
            super().handle_event(event)  # Lida com o evento QUIT

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.close_event_image()
            return

        # 1. O Terminal está ativo?
        if self.terminal.is_active:
            result = self.terminal.handle_event(event)
            if result == "correct_command":
                self.proceed_to_next_step()
            elif result == "incorrect_command":
                # Dá um feedback de comando errado
                self.speech_bubble.set_text("Não... não é esse o comando.")
                
        # 2. A Caixa de Resposta está ativa?
        elif self.input_box.is_active:
            result = self.input_box.handle_event(event)
            
            if result == "correct":
                self.proceed_to_next_step()
            elif result == "incorrect":
                self.speech_bubble.set_text("Não, não é isso... Tente de novo.")
            elif result == "invalid_option":
                self.speech_bubble.set_text("Isso não parece ser um dos serviços da lista.")
            elif isinstance(result, dict):
                # É um evento de ramificação! (ex: facebook)
                self.handle_branch_event(result)

    def handle_branch_event(self, event_data):
        """Lida com as respostas que não avançam a história."""
        
        if event_data.get("action") == "show_event":
            # Atualiza a fala do professor
            if event_data.get("professor_speech"):
                self.speech_bubble.set_text(event_data.get("professor_speech"))
            
            # Mostra a imagem no terminal
            image_path = event_data.get("terminal_event_display")
            self.terminal.show_event_image(image_path)
            
            if image_path:
                self.showing_event_image = True
                self.event_image_timer = pygame.time.get_ticks()

            # TODO: Tocar o 'sound_effect'
            # (Exigiria inicializar pygame.mixer)
            
            # Importante: NÃO avançamos a história.
            # O jogador é forçado a tentar outra resposta.
    def advance_speech(self):
        if self.speech_list:
            if self.current_speech_index < len(self.speech_list):
                self.speech_bubble.set_text(self.speech_list[self.current_speech_index])
                self.current_speech_index += 1
            else:
                self.speech_bubble.set_text(self.speech_list[self.current_speech_index-1])
    def update(self, dt):
        """
        Atualiza todos os componentes (para cursores piscando)
        e checa o timer de auto-avanço.
        """
        
        # 1. Atualiza todos os componentes
        self.terminal.update()
        self.input_box.update()
        self.speech_bubble.update()
        self.objective_list.update()
        
        # 2. Checa o timer de auto-avanço
        if self.auto_proceed_timer is not None:
            now = pygame.time.get_ticks()
            if now - self.auto_proceed_timer >= self.auto_proceed_delay:
                self.auto_proceed_timer = None # Desativa o timer
                self.proceed_to_next_step()

        # 3. Checa o timer de imagem de evento
        if self.event_image_timer is not None:
            now = pygame.time.get_ticks()
            if now - self.event_image_timer >= self.event_image_duration:
                self.close_event_image()

    def draw(self, screen):
        """
        Desenha todos os componentes na tela, na ordem correta.
        (O 'screen.fill' é feito no main.py)
        """
        
        # 1. Desenha a imagem estática do professor
        screen.blit(self.professor_image, PROFESSOR_RECT.topleft)
        
        # 2. Desenha todos os componentes de UI
        # (Cada um deles já sabe sua posição e desenha seu próprio fundo)
        self.objective_list.draw(screen)
        self.speech_bubble.draw(screen)
        self.terminal.draw(screen)
        self.input_box.draw(screen)