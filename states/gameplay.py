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
        self.speech_list = None

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
        # <-- MODIFICAÇÃO: Usa a nova função set_speech
        self.set_speech(step_data.get("professor_speech"))
    
    def startup(self, persistent_data):
        """Chamado uma vez quando o estado começa (depois da cutscene)."""
        super().startup(persistent_data)
        
        # <-- NOVO: Adiciona a lógica de persistência que fizemos antes
        self.persist['override_speech'] = None 

        # Reseta o estado
        self.current_step = 0
        self.terminal.clear_history()
        
        # Carrega o primeiro passo da história
        self.load_story_step(self.current_step)

    # --- NOVA FUNÇÃO AUXILIAR ---
    def activate_input_for_current_step(self):
        """
        Lê o passo atual e ativa o componente de input correto.
        (Esta é a lógica 'roubada' do load_story_step)
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
        A função MAIS IMPORTANTE.
        Lê um passo da história e configura toda a UI.
        """
        
        # 1. Verifica se a história terminou
        if step_index >= len(STORY_STEPS):
            print("Fim da história!")
            self.done = True
            return
            
        # 2. Reseta timers e falas
        self.auto_proceed_timer = None
        self.event_image_timer = None
        self.current_speech_index = 0
        self.speech_list = None
        
        # 3. Pega os dados do passo atual
        self.current_step = step_index
        step_data = STORY_STEPS[self.current_step]
        
        # 4. Atualiza os componentes de "saída" (display)
        
        # --- LÓGICA DE FALA (Sua lógica atual, está perfeita) ---
        persistent_speech = self.persist.get('override_speech', None)
        if persistent_speech:
            speech_data = persistent_speech
            self.persist['override_speech'] = None 
        else:
            speech_data = step_data.get("professor_speech")
        self.set_speech(speech_data)
        # --- FIM DA LÓGICA DE FALA ---
            
        if step_data.get("objective"):
            self.objective_list.set_objective(step_data.get("objective"))
            
        if step_data.get("terminal_text"):
            self.terminal.add_to_history(step_data.get("terminal_text"))

        # --- MODIFICAÇÃO PRINCIPAL: LÓGICA DE IMAGEM ---
        image_path = step_data.get("terminal_event_display")
        
        if image_path is None:
            # Chave NÃO existe = limpa a imagem (default)
            self.terminal.show_event_image(None)
            self.showing_event_image = False # Garante que a flag de clique é resetada
        elif image_path == "...":
            # Chave existe e é "..." = não faz nada, mantém a imagem
            pass 
        else:
            # Chave existe e é um path = carrega a nova imagem
            self.terminal.show_event_image(image_path)
            # Nota: Não ativamos 'showing_event_image'
            # pois não queremos que ela seja "clicável" para fechar.
            # Ela é um fundo de evidência.
        

        # 5. Configura os componentes de "entrada" (ação)
        action = step_data.get("action_type")
        
        if not self.speech_list: # (Sua lógica de "input paciente", está perfeita)
            self.activate_input_for_current_step()

    # --- NOVA FUNÇÃO AUXILIAR ---
    def set_speech(self, speech_data):
        """
        Processa um 'speech_data' e decide se é
        uma fala única ou uma lista de falas.
        """
        # Limpa o indicador por padrão
        self.speech_bubble.set_indicator(False) 

        if isinstance(speech_data, (list, tuple)):
            # É uma lista de falas!
            self.speech_list = speech_data
            self.current_speech_index = 0 # Reseta o índice
            self.advance_speech() # Mostra a *primeira* fala da lista
        elif speech_data:
            # É uma fala única (string)
            self.speech_list = None # Garante que está limpo
            self.speech_bubble.set_text(speech_data)
        else:
            # Não há fala (string vazia ou None)
            self.speech_list = None
            self.speech_bubble.set_text("")

    def proceed_to_next_step(self):
        """Função helper para carregar o próximo passo."""
        # Limpa qualquer imagem de evento (ex: Minions)
        #self.terminal.show_event_image(None)
        
        self.load_story_step(self.current_step + 1)

    # --- FUNÇÃO 'handle_event' MODIFICADA E REORGANIZADA ---
    def handle_event(self, event):
        """
        Passa os eventos (teclado/mouse) para o componente ATIVO.
        """
        super().handle_event(event) # Lida com o evento QUIT
        
        # --- REORGANIZAÇÃO DE PRIORIDADE ---
        
        # Prioridade 1: Imagem de evento (Facebook)
        if self.showing_event_image:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.close_event_image()
            return # Ignora todo o resto

        # Prioridade 2: Avançar fala com clique
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Checa se o clique foi DENTRO do balão de fala
            if self.speech_bubble.rect.collidepoint(event.pos):
                if self.speech_list: # Se estivermos em modo de multi-fala
                    self.advance_speech()
                    # Se avançamos a fala, não queremos que o clique
                    # "caia" para o terminal ou input_box
                    return 

        # Prioridade 3: Input do jogador (Terminal ou Caixa)
        result = None
        if self.terminal.is_active:
            result = self.terminal.handle_event(event)
            if result == "correct_command":
                self.proceed_to_next_step()
            elif result == "incorrect_command":
                # <-- MODIFICAÇÃO: Usa set_speech
                self.set_speech("Não... não é esse o comando.")
                
        elif self.input_box.is_active:
            result = self.input_box.handle_event(event)
            
            if result == "correct":
                self.proceed_to_next_step()
            elif result == "incorrect":
                # <-- MODIFICAÇÃO: Usa set_speech
                self.set_speech("Não, não é isso... Tente de novo.")
            elif result == "invalid_option":
                # <-- MODIFICAÇÃO: Usa set_speech
                self.set_speech("Isso não parece ser um dos serviços da lista.")
            
            # --- LÓGICA DE EVENTO MODIFICADA (INCLUINDO LÓGICA FALTANTE) ---
            elif isinstance(result, dict):
                action = result.get("action")
                
                if action == "show_event":
                    self.handle_branch_event(result) 
                
                # (Lógica do "auto_proceed" que fizemos antes)
                elif action == "show_speech_and_proceed":
                    # (Esta função é adicionada abaixo)
                    self.handle_speech_and_proceed(result) 
                
                # (Lógica do "sim"/"nao" que fizemos antes)
                elif action == "proceed_with_speech":
                    # 1. Armazena a fala para o PRÓXIMO passo
                    self.persist['override_speech'] = result.get("professor_speech")
                    # 2. Avança IMEDIATAMENTE
                    self.proceed_to_next_step()

    def handle_branch_event(self, event_data):
        """Lida com as respostas que não avançam a história."""
        
        # (Seu código antigo de 'ssh_ok_event' e 'show_ssh_explanation')
        if event_data.get("action") == "ssh_ok_event":
            print("Entrou aqui")
            next_step = event_data.get("next_step")
            # <-- MODIFICAÇÃO: Usa a nova função
            self.set_speech(event_data.get("professor_speech"))
            self.load_story_step(next_step)
            
        if event_data.get("action") == "show_ssh_explanation":
            next_step = event_data.get("next_step")
            # <-- MODIFICAÇÃO: Usa a nova função
            self.set_speech(event_data.get("professor_speech"))
            self.load_story_step(next_step)

        if event_data.get("action") == "show_event":
            # Atualiza a fala do professor
            if event_data.get("professor_speech"):
                # <-- MODIFICAÇÃO: Usa a nova função
                self.set_speech(event_data.get("professor_speech"))
            
            # Mostra a imagem no terminal
            image_path = event_data.get("terminal_event_display")
            self.terminal.show_event_image(image_path)
            
            if image_path:
                self.showing_event_image = True
                self.event_image_timer = pygame.time.get_ticks()

            # TODO: Tocar o 'sound_effect'
            
            # Importante: NÃO avançamos a história.
            
    # --- FUNÇÃO 'advance_speech' MODIFICADA ---
    def advance_speech(self):
        """Avança o índice da fala, atualiza o balão E o indicador."""
        if not self.speech_list: # Checagem de segurança
            return

        if self.current_speech_index >= len(self.speech_list):
             # Apenas re-exibe a última fala (índice -1) para não quebrar.
             self.speech_bubble.set_text(self.speech_list[-1])
             # E o mais importante: NÃO faz mais nada. Não incrementa, não ativa o input.
             return

        # Mostra a fala ANTES de incrementar
        self.speech_bubble.set_text(self.speech_list[self.current_speech_index])
        
        # Avança o índice
        self.current_speech_index += 1
        
        # Agora, checa se acabamos
        if self.current_speech_index == len(self.speech_list):
            # Acabamos de mostrar a ÚLTIMA fala
            self.speech_bubble.set_indicator(False) # <-- NOVO
            self.activate_input_for_current_step() # <-- NOVO: Ativa o input
        else:
            # Ainda há mais falas
            self.speech_bubble.set_indicator(True) # <-- NOVO
            
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

    # --- NOVO (Função que estava faltando) ---
    def handle_speech_and_proceed(self, event_data):
        """
        Mostra uma nova fala e, em seguida,
        ativa o timer para avançar para o próximo passo.
        """
        # <-- MODIFICAÇÃO: Usa a nova função
        self.set_speech(event_data.get("professor_speech"))
        self.auto_proceed_timer = pygame.time.get_ticks()
        self.auto_proceed_delay = event_data.get("next_step_delay", 1000)
        self.terminal.show_event_image(None)