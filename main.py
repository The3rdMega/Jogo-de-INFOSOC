#
# Arquivo: main.py
# (O ponto de entrada do seu jogo)
#
import pygame

# Importa as constantes (tamanho da tela, FPS)
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Importa os "estados" do jogo.
# Por enquanto, só temos o GameplayState.
from states.gameplay import GameplayState
# TODO: Importar o CutsceneState quando ele for criado
from states.cutscene import CutsceneState 


class Game:
    """
    Classe principal que gerencia o loop do jogo, a tela
    e a máquina de estados.
    """
    
    def __init__(self):
        """Inicializa o Pygame e a janela."""
        pygame.init()
        
        # Cria a tela principal
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("O Hack da UnB")
        
        # Cria o relógio para controlar o FPS
        self.clock = pygame.time.Clock()
        
        # Variáveis de controle do loop
        self.running = True
        self.dt = 0 # Delta Time (tempo desde o último frame)
        
        # --- A Máquina de Estados ---
        self.states = {} # Dicionário para guardar todos os estados
        self.current_state_name = None # O nome do estado ativo (ex: "GAMEPLAY")
        self.current_state = None # O objeto do estado ativo
        
    def setup_states(self):
        """
        Cria as instâncias de todos os estados do jogo
        e define o estado inicial.
        """
        
        # TODO: Adicionar o estado de Cutscene aqui
        self.states["CUTSCENE"] = CutsceneState()
        
        self.states["GAMEPLAY"] = GameplayState()
        
        # TODO: Mudar para "CUTSCENE" quando ela estiver pronta
        self.current_state_name = "GAMEPLAY" 
        
        self.current_state = self.states[self.current_state_name]
        
        # Chama a função 'startup' do estado inicial
        self.current_state.startup({})

    def flip_state(self):
        """Função para trocar do estado atual para o próximo."""
        
        # Pega o nome do próximo estado (ex: "END_SCREEN")
        next_state_name = self.current_state.next_state
        
        # Pega os dados persistentes (se houver)
        persistent_data = self.current_state.persist
        
        # Sinaliza o fim do estado atual
        self.current_state.done = False
        
        # Se o próximo estado for 'None' ou 'QUIT', fecha o jogo
        if next_state_name is None:
            self.running = False
            return
            
        # Pega o objeto do próximo estado no dicionário
        self.current_state = self.states[next_state_name]
        self.current_state_name = next_state_name
        
        # Inicia o novo estado, passando os dados persistentes
        self.current_state.startup(persistent_data)

    def event_loop(self):
        """Processa todos os eventos do Pygame e os passa para o estado ativo."""
        for event in pygame.event.get():
            self.current_state.handle_event(event)
            
    def update(self):
        """
        Atualiza a lógica do estado ativo e checa por
        sinais de 'quit' ou 'done'.
        """
        
        # Passa o 'dt' (delta time) para o update do estado.
        # dt é o tempo em segundos desde o último frame.
        self.current_state.update(self.dt)
        
        # Checa se o estado pediu para fechar o jogo
        if self.current_state.quit:
            self.running = False
        
        # Checa se o estado pediu para trocar para o próximo estado
        elif self.current_state.done:
            self.flip_state()

    def draw(self):
        """Limpa a tela e desenha o estado ativo."""
        
        # Limpa a tela com uma cor de fundo (ex: preto)
        self.screen.fill((0, 0, 0))
        
        # Chama a função 'draw' do estado ativo
        self.current_state.draw(self.screen)
        
        # Atualiza o display (mostra o que foi desenhado)
        pygame.display.flip()

    def run(self):
        """O Loop Principal do Jogo."""
        
        while self.running:
            # 1. Processa Eventos
            self.event_loop()
            
            # 2. Atualiza a Lógica
            self.update()
            
            # 3. Desenha na Tela
            self.draw()
            
            # 4. Controla o FPS
            # self.dt é guardado em segundos (ex: 0.016)
            self.dt = self.clock.tick(FPS) / 1000.0
            
        # Fim do loop, fecha o Pygame
        pygame.quit()


# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    game = Game()
    game.setup_states()
    game.run()