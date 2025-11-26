import pygame
from states.base_state import BaseState
from story import STORY_STEPS
from settings import *
from ui.terminal import InteractiveTerminal
from ui.text_input import TextInputBox
from ui.speech_bubble import SpeechBubble
from ui.objective_list import ObjectiveList

class GameplayState(BaseState):
    
    def __init__(self):
        super().__init__()
        self.current_speech_index = 0
        self.speech_list = None
        
        # --- NOVO: Flag de Morte Pendente ---
        self.pending_game_over = False 

        self.error_message_timer = None
        self.error_message_duration = 4000 
        self.current_step_speech_data = None 

        self.next_state = "END_SCREEN" 
        self.current_step = 0
        self.auto_proceed_timer = None
        self.auto_proceed_delay = 0
        self.showing_event_image = False
        self.event_image_timer = None
        self.event_image_duration = 5000 

        try:
            professor_img_raw = pygame.image.load("assets/images/professor.png").convert_alpha()
            self.professor_image = pygame.transform.scale(
                professor_img_raw, (PROFESSOR_RECT.width, PROFESSOR_RECT.height)
            )
        except Exception as e:
            print(f"Erro ao carregar imagem do professor: {e}")
            self.professor_image = pygame.Surface((PROFESSOR_RECT.width, PROFESSOR_RECT.height))
            self.professor_image.fill((255, 0, 255)) 

        self.terminal = InteractiveTerminal(TERMINAL_RECT)
        self.input_box = TextInputBox(INPUT_BOX_RECT)
        self.speech_bubble = SpeechBubble(SPEECH_BUBBLE_RECT)
        self.objective_list = ObjectiveList(OBJECTIVE_LIST_RECT)

        self.strikes = MAX_STRIKES
        
    # ... (take_damage, trigger_game_over, close_event_image... MANTER IGUAIS) ...
    def take_damage(self):
        self.strikes -= 1
        self.objective_list.set_strikes(self.strikes)
        print(f"DANO! Strikes restantes: {self.strikes}")
        if self.strikes <= 0:
            self.trigger_game_over()
        else:
            self.set_speech("Cuidado! Se errarmos muito, eles vão perceber nossa conexão!", is_error_message=True)

    def trigger_game_over(self):
        self.next_state = "CUTSCENE" 
        self.persist = {
            'image_path': "assets/images/ransomware_screen.png",
            'title': "GAME OVER",
            'subtitle': "O invasor percebeu sua investigação e criptografou o sistema",
            'duration': 5000,
            'wait_for_input': True,
            'next_state': "GAMEPLAY" 
        }
        self.done = True 

    def close_event_image(self):
        self.showing_event_image = False
        self.event_image_timer = None 
        self.terminal.show_event_image(None)
        step_data = STORY_STEPS[self.current_step]
        self.set_speech(step_data.get("professor_speech"))

    def startup(self, persistent_data):
        super().startup(persistent_data)
        self.persist['override_speech'] = None 
        self.current_step = 0
        self.strikes = MAX_STRIKES 
        self.objective_list.set_strikes(self.strikes) 
        self.terminal.clear_history()     
        self.terminal.deactivate_input()  
        self.input_box.deactivate()       
        self.terminal.show_event_image(None)
        self.showing_event_image = False
        self.auto_proceed_timer = None
        self.event_image_timer = None
        self.error_message_timer = None 
        
        # Resetar flag de morte
        self.pending_game_over = False 
        
        self.load_story_step(self.current_step)

    # ... (activate_input_for_current_step... MANTER IGUAL) ...
    def activate_input_for_current_step(self):
        step_data = STORY_STEPS[self.current_step]
        action = step_data.get("action_type")
        if action == "await_command":
            self.terminal.activate_input(step_data.get("command_prompt"), step_data.get("expected_command"))
            self.input_box.deactivate()
        elif action == "ask_question":
            self.terminal.deactivate_input()
            self.input_box.activate(step_data.get("question_prompt"), step_data.get("expected_answer"))
        elif action == "ask_question_branching":
            self.terminal.deactivate_input()
            self.input_box.activate(step_data.get("question_prompt"), step_data.get("answer_handlers"))
        elif action == "auto_proceed":
            self.terminal.deactivate_input()
            self.input_box.deactivate()
            self.auto_proceed_timer = pygame.time.get_ticks()
            self.auto_proceed_delay = step_data.get("next_step_delay", 1000)
        else: 
            self.terminal.deactivate_input()
            self.input_box.deactivate()

    # ... (load_story_step... MANTER IGUAL) ...
    def load_story_step(self, step_index):
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
        self.auto_proceed_timer = None
        self.event_image_timer = None
        self.error_message_timer = None 
        self.current_speech_index = 0
        self.speech_list = None
        
        # Resetar flag de morte ao carregar novo passo (segurança)
        self.pending_game_over = False 

        self.terminal.deactivate_input()
        self.input_box.deactivate()

        self.current_step = step_index
        step_data = STORY_STEPS[self.current_step]
        
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

    # ... (set_speech... MANTER IGUAL) ...
    def set_speech(self, speech_data, is_error_message=False):
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
        self.load_story_step(self.current_step + 1)

    def handle_event(self, event):
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
                # --- NOVO: Handler para game_over_speech ---
                elif action == "game_over_speech":
                    self.handle_game_over_speech(result)
                # -------------------------------------------

    # --- FUNÇÃO advance_speech CORRIGIDA ---
    def advance_speech(self):
        """Avança o índice da fala."""
        if not self.speech_list: 
            return

        # 1. VERIFICAÇÃO DE FIM (Game Over ou Segurança)
        # Se o índice já chegou ao fim da lista, significa que o texto final já está na tela.
        if self.current_speech_index >= len(self.speech_list):
             # Se tem morte pendente, esse "clique extra" dispara o gatilho
             if self.pending_game_over:
                 self.trigger_game_over()
             else:
                 # Apenas segurança para não quebrar se clicar demais
                 self.speech_bubble.set_text(self.speech_list[-1])
             return

        # 2. FLUXO NORMAL: Mostra a fala atual
        self.speech_bubble.set_text(self.speech_list[self.current_speech_index])
        self.current_speech_index += 1
        
        # 3. VERIFICA SE ACABOU AGORA
        if self.current_speech_index == len(self.speech_list):
            if self.pending_game_over:
                # Se vai morrer, MANTÉM o indicador ligado para pedir o último clique
                self.speech_bubble.set_indicator(True)
            else:
                # Se é normal, desliga indicador e libera o jogo
                self.speech_bubble.set_indicator(False)
                self.activate_input_for_current_step()
        else:
            self.speech_bubble.set_indicator(True) 
    # -------------------------------------------

    # ... (handle_branch_event... MANTER IGUAL) ...
    def handle_branch_event(self, event_data):
        # ... (código existente) ...
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
                self.set_speech(event_data.get("professor_speech"), is_error_message=True) 
            
            image_path = event_data.get("terminal_event_display")
            if image_path:
                self.terminal.show_event_image(image_path)
                self.showing_event_image = True
                self.event_image_timer = pygame.time.get_ticks()
            
            text_append = event_data.get("terminal_text_append")
            if text_append:
                self.terminal.add_to_history(text_append)

    # ... (update e draw... MANTER IGUAIS) ...
    def update(self, dt):
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
        self.objective_list.draw(screen)
        self.speech_bubble.draw(screen)
        self.terminal.draw(screen)
        self.input_box.draw(screen)

    def handle_speech_and_proceed(self, event_data):
        self.set_speech(event_data.get("professor_speech"))
        self.auto_proceed_timer = pygame.time.get_ticks()
        self.auto_proceed_delay = event_data.get("next_step_delay", 1000)
        self.terminal.show_event_image(None) 

    # --- NOVO: Handler da morte ---
    def handle_game_over_speech(self, event_data):
        """Inicia o diálogo da morte."""
        # 1. Define a fala (que é uma lista)
        self.set_speech(event_data.get("professor_speech"))
        # 2. Marca a morte para acontecer no fim da fala
        self.pending_game_over = True