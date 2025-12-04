#
# Arquivo: states/gameplay.py
#
import pygame

# Importa o "molde" do estado
from states.base_state import BaseState

# Importa o cérebro (a história)
from story import STORY_STEPS

# Importa o layout (posições e cores)
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
        self.speech_list = None

        # Inicialização do mixer pro som de dano
        try:
            pygame.mixer.init()
            self.damage_sound = pygame.mixer.Sound("assets/sounds/damage_sound.mp3")
        except:
            print("Aviso: damage_sound.mp3 não encontrado ou erro no mixer.")
            self.damage_sound = None

        # Flag de game over pendente
        self.pending_game_over = False 

        # Lidando com mensagem de erro
        self.error_message_timer = None
        self.error_message_duration = 4000 # 4 segundos para ler o erro
        self.current_step_speech_data = None # Armazena a fala "oficial" do passo atual

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
        try:
            professor_img_raw = pygame.image.load("assets/images/professor.png").convert_alpha()
            self.professor_image = pygame.transform.scale(
                professor_img_raw, (PROFESSOR_RECT.width, PROFESSOR_RECT.height)
            )
            # Seu código personalizado de suspeitos
            # (Assumindo que você usa isso em algum lugar do draw que não estava no código original,
            # mas mantive aqui para preservar sua lógica)
            suspects_img_raw = pygame.image.load("assets/images/suspects.png").convert_alpha()
            self.suspects_image = pygame.transform.scale(
                suspects_img_raw, (583, 230)
            )
        except Exception as e:
            print(f"Erro ao carregar imagens: {e}")
            self.professor_image = pygame.Surface((PROFESSOR_RECT.width, PROFESSOR_RECT.height))
            self.professor_image.fill((255, 0, 255)) 
            self.suspects_image = pygame.Surface((583, 230)) # Fallback para suspeitos

        # --- Instanciar todos os Componentes da UI ---
        self.terminal = InteractiveTerminal(TERMINAL_RECT)
        self.input_box = TextInputBox(INPUT_BOX_RECT)
        self.speech_bubble = SpeechBubble(SPEECH_BUBBLE_RECT)
        self.objective_list = ObjectiveList(OBJECTIVE_LIST_RECT)

        # Sistema de Vida
        self.strikes = MAX_STRIKES
        

    def take_damage(self):
        """Reduz uma vida e checa Game Over."""
        self.strikes -= 1
        
        # Atualiza a UI
        self.objective_list.set_strikes(self.strikes)
        
        print(f"DANO! Strikes restantes: {self.strikes}")
        
        # Toca som se existir
        if self.damage_sound:
            self.damage_sound.play()
        
        # Checa Game Over
        if self.strikes <= 0:
            self.trigger_game_over()
        else:
            # Feedback do professor
            self.set_speech("Cuidado! Se errarmos muito, eles vão perceber nossa conexão!", is_error_message=True)

    def trigger_game_over(self):
        """Transiciona para a tela de derrota (Ransomware)."""
        
        self.next_state = "CUTSCENE" 
        
        self.persist = {
            'image_path': "assets/images/ransomware_screen.png",
            'title': "CONEXÃO PERDIDA",
            'subtitle': "Ransomware detectado. Sistema comprometido.",
            'duration': 5000,
            'wait_for_input': True,
            'next_state': "GAMEPLAY" # Reinicia o jogo ao clicar
        }
        
        self.done = True 

    def close_event_image(self):
        """
        Rotina auxiliar para fechar a imagem do evento.
        """
        self.showing_event_image = False
        self.event_image_timer = None 
        self.terminal.show_event_image(None)
        
        # Restaura a fala original da pergunta
        step_data = STORY_STEPS[self.current_step]
        self.set_speech(step_data.get("professor_speech"))
    
    def startup(self, persistent_data):
        """Chamado uma vez quando o estado começa ou RECOMEÇA."""
        super().startup(persistent_data)
        
        # 1. Reseta a Lógica de Jogo
        self.persist['override_speech'] = None 
        self.current_step = 0
        
        # --- CORREÇÃO DAS VIDAS ---
        self.strikes = MAX_STRIKES 
        self.objective_list.set_strikes(self.strikes) 
        
        # 2. Reseta os Componentes de UI 
        self.terminal.clear_history()     
        self.terminal.deactivate_input()  
        self.input_box.deactivate()       
        
        # 3. Reseta Imagens e Timers
        self.terminal.show_event_image(None)
        self.showing_event_image = False
        self.auto_proceed_timer = None
        self.event_image_timer = None
        self.error_message_timer = None 
        
        self.pending_game_over = False
        
        # 4. Carrega o primeiro passo da história do zero
        self.load_story_step(self.current_step)

    # --- NOVA FUNÇÃO AUXILIAR ---
    def activate_input_for_current_step(self):
        """
        Lê o passo atual e ativa o componente de input correto.
        """
        step_data = STORY_STEPS[self.current_step]
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
            self.auto_proceed_timer = pygame.time.get_ticks()
            self.auto_proceed_delay = step_data.get("next_step_delay", 1000)
        else: 
            self.terminal.deactivate_input()
            self.input_box.deactivate()

    def load_story_step(self, step_index):
        """
        A função MAIS IMPORTANTE. Lê um passo da história.
        """
        
        if step_index >= len(STORY_STEPS):
            print("Fim da história!")
            # Configura a tela de Vitória
            self.next_state = "CUTSCENE"
            self.persist = {
                'title': "MISSÃO CUMPRIDA",
                'subtitle': "Você identificou o hacker e protegeu o sistema.",
                'duration': 5000,
                'wait_for_input': True,
                'next_state': None # None fará o jogo fechar após a tela de vitória
            }
            self.done = True
            return
        if step_index == 1:
            self.suspects_image.fill((250, 0, 255)) 
        # Reseta timers
        self.auto_proceed_timer = None
        self.event_image_timer = None
        self.error_message_timer = None 
        self.current_speech_index = 0
        self.speech_list = None
        
        # --- LIMPEZA PREVENTIVA ---
        self.pending_game_over = False
        self.terminal.deactivate_input()
        self.input_box.deactivate()
        # --------------------------

        self.current_step = step_index
        step_data = STORY_STEPS[self.current_step]
        
        # --- LÓGICA DE FALA ---
        persistent_speech = self.persist.get('override_speech', None)
        if persistent_speech:
            speech_data = persistent_speech
            self.persist['override_speech'] = None 
        else:
            speech_data = step_data.get("professor_speech")
        
        self.set_speech(speech_data)
            
        if step_data.get("objective"):
            self.objective_list.set_objective(step_data.get("objective"))
        if step_data.get("terminal_text"):
            self.terminal.add_to_history(step_data.get("terminal_text"))

        image_path = step_data.get("terminal_event_display")        
        if image_path is None:
            self.terminal.show_event_image(None)
            self.showing_event_image = False 
        elif image_path == "...":
            pass 
        else:
            self.terminal.show_event_image(image_path)
        
        if not self.speech_list: 
            self.activate_input_for_current_step()

    def set_speech(self, speech_data, is_error_message=False):
        """
        Processa um 'speech_data'.
        """
        if not is_error_message:
            self.current_step_speech_data = speech_data
        self.speech_bubble.set_indicator(False) 
        if isinstance(speech_data, (list, tuple)):
            self.speech_list = speech_data
            self.current_speech_index = 0 
            self.advance_speech() 
        elif speech_data:
            self.speech_list = None 
            self.speech_bubble.set_text(speech_data)
        else:
            self.speech_list = None
            self.speech_bubble.set_text("")

    def proceed_to_next_step(self):
        """Função helper para carregar o próximo passo."""
        self.load_story_step(self.current_step + 1)

    def handle_event(self, event):
        """Passa os eventos (teclado/mouse) para o componente ATIVO."""
        super().handle_event(event) 
        
        if self.showing_event_image:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.close_event_image()
            return 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.speech_bubble.rect.collidepoint(event.pos):
                if self.speech_list: 
                    self.advance_speech()
                    return 

        result = None
        if self.terminal.is_active:
            result = self.terminal.handle_event(event)
            if result == "correct_command":
                self.proceed_to_next_step()
            elif result == "incorrect_command":
                self.take_damage() 
                self.error_message_timer = pygame.time.get_ticks()

        elif self.input_box.is_active:
            result = self.input_box.handle_event(event)
            if result == "correct":
                self.proceed_to_next_step()
            elif result == "incorrect":
                self.take_damage()
                self.error_message_timer = pygame.time.get_ticks()
            elif result == "invalid_option":
                self.set_speech("Isso não parece ser um dos serviços da lista.", is_error_message=True)
                self.error_message_timer = pygame.time.get_ticks()
            
            elif isinstance(result, dict):
                action = result.get("action")
                if action == "show_event":
                    self.handle_branch_event(result) 
                elif action == "show_speech_and_proceed":
                    self.handle_speech_and_proceed(result) 
                elif action == "proceed_with_speech":
                    self.persist['override_speech'] = result.get("professor_speech")
                    self.proceed_to_next_step()
                elif action == "game_over_speech":
                    self.handle_game_over_speech(result)

    def handle_branch_event(self, event_data):
        """Lida com as respostas que não avançam a história."""
        
        # --- AQUI ESTAVA FALTANDO A LÓGICA DE DANO ---
        if event_data.get("take_damage"):
            # 1. Tira a vida
            self.strikes -= 1
            self.objective_list.set_strikes(self.strikes)
            print(f"DANO (Branch)! Strikes restantes: {self.strikes}")
            
            if self.damage_sound:
                self.damage_sound.play()

            # 2. Se morreu, ACABA TUDO.
            if self.strikes <= 0:
                self.trigger_game_over()
                return 
        
        # Lógica de Morte Instantânea (se necessário)
        if event_data.get("take_all_damage"):
            self.strikes = 0
            self.objective_list.set_strikes(0)
            self.trigger_game_over()
            return
        # ---------------------------------------------

        if event_data.get("action") == "ssh_ok_event":
            next_step = event_data.get("next_step")
            self.set_speech(event_data.get("professor_speech"))
            self.load_story_step(next_step)
        if event_data.get("action") == "show_ssh_explanation":
            next_step = event_data.get("next_step")
            self.set_speech(event_data.get("professor_speech"))
            self.load_story_step(next_step)
        if event_data.get("action") == "show_event":
            if event_data.get("professor_speech"):
                # Define is_error_message=True se houve dano, para o texto voltar depois
                is_err = event_data.get("take_damage", False)
                self.set_speech(event_data.get("professor_speech"), is_error_message=is_err) 
                # Se teve dano, ativa o timer para restaurar texto
                if is_err:
                    self.error_message_timer = pygame.time.get_ticks()
            
            image_path = event_data.get("terminal_event_display")
            if image_path:
                self.terminal.show_event_image(image_path)
                self.showing_event_image = True
                self.event_image_timer = pygame.time.get_ticks()
            
            text_append = event_data.get("terminal_text_append")
            if text_append:
                self.terminal.add_to_history(text_append)

    def advance_speech(self):
        """Avança o índice da fala."""
        if not self.speech_list: 
            return

        if self.current_speech_index >= len(self.speech_list):
             if self.pending_game_over:
                 self.trigger_game_over()
             else:
                 self.speech_bubble.set_text(self.speech_list[-1])
             return

        self.speech_bubble.set_text(self.speech_list[self.current_speech_index])
        self.current_speech_index += 1
        
        if self.current_speech_index == len(self.speech_list):
            if self.pending_game_over:
                self.speech_bubble.set_indicator(True)
            else:
                self.speech_bubble.set_indicator(False)
                self.activate_input_for_current_step()
        else:
            self.speech_bubble.set_indicator(True) 
            
    def update(self, dt):
        """Atualiza todos os componentes e checa timers."""
        self.terminal.update()
        self.input_box.update()
        self.speech_bubble.update()
        self.objective_list.update()
        if self.auto_proceed_timer is not None:
            now = pygame.time.get_ticks()
            if now - self.auto_proceed_timer >= self.auto_proceed_delay:
                self.auto_proceed_timer = None 
                self.proceed_to_next_step()
        if self.event_image_timer is not None:
            now = pygame.time.get_ticks()
            if now - self.event_image_timer >= self.event_image_duration:
                self.close_event_image()
        # --- TIMER PARA RESTAURAR FALA ORIGINAL ---
        if self.error_message_timer is not None:
            if pygame.time.get_ticks() - self.error_message_timer >= self.error_message_duration:
                self.error_message_timer = None
                data = self.current_step_speech_data
                if isinstance(data, (list, tuple)) and len(data) > 0:
                    self.set_speech(data[-1]) 
                else:
                    self.set_speech(data)

    def draw(self, screen):
        screen.blit(self.professor_image, PROFESSOR_RECT.topleft)
        # Se você quiser desenhar a imagem dos suspeitos, descomente:
        # screen.blit(self.suspects_image, (207, 300))
        self.objective_list.draw(screen)
        self.speech_bubble.draw(screen)
        self.terminal.draw(screen)
        self.input_box.draw(screen)

    def handle_speech_and_proceed(self, event_data):
        """Mostra fala e avança."""
        self.set_speech(event_data.get("professor_speech"))
        self.auto_proceed_timer = pygame.time.get_ticks()
        self.auto_proceed_delay = event_data.get("next_step_delay", 1000)
        self.terminal.show_event_image(None) 

    def handle_game_over_speech(self, event_data):
        """Inicia o diálogo da morte."""
        # Garante que desativa o input imediatamente
        self.input_box.deactivate() 
        self.terminal.deactivate_input()
        self.set_speech(event_data.get("professor_speech"))
        self.pending_game_over = True