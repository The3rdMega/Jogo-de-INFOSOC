#
# Arquivo: main.py
# (Com redimensionamento de janela e escala de proporção)
#
import pygame

# Importa as constantes (tamanho da tela, FPS)
# Adicionamos GAME_WIDTH e GAME_HEIGHT que definimos no settings.py
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_WIDTH, GAME_HEIGHT, FPS

# Importa os "estados" do jogo.
from states.gameplay import GameplayState
from states.cutscene import CutsceneState 


class Game:
    """
    Classe principal que gerencia o loop do jogo, a tela
    e a máquina de estados.
    """
    
    def __init__(self):
        """Inicializa o Pygame e a janela."""
        pygame.init()
        
        # 1. Cria a Janela Real (Redimensionável)
        # A flag pygame.RESIZABLE permite que o usuário mude o tamanho ou maximize
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("O Hack da UnB")
        
        # 2. Cria a "Tela Falsa" (Resolução Fixa)
        # Onde o jogo será desenhado internamente (ex: 800x600)
        self.fake_screen = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        
        # Cria o relógio para controlar o FPS
        self.clock = pygame.time.Clock()
        
        # Variáveis de controle do loop
        self.running = True
        self.dt = 0 # Delta Time
        
        # --- Variáveis de Escala (NOVO) ---
        self.scale_ratio = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.calculate_scale() # Calcula a escala inicial
        
        # --- A Máquina de Estados ---
        self.states = {} 
        self.current_state_name = None 
        self.current_state = None 
        
    def calculate_scale(self):
        """
        Calcula como esticar a tela falsa para caber na janela
        mantendo a proporção (Aspect Ratio).
        """
        window_w, window_h = self.window.get_size()
        
        # Descobre qual lado "limita" o crescimento (largura ou altura)
        scale_w = window_w / GAME_WIDTH
        scale_h = window_h / GAME_HEIGHT
        self.scale_ratio = min(scale_w, scale_h)
        
        # Tamanho final da imagem do jogo na tela
        self.render_w = int(GAME_WIDTH * self.scale_ratio)
        self.render_h = int(GAME_HEIGHT * self.scale_ratio)
        
        # Centraliza a imagem na janela (calcula as barras pretas)
        self.offset_x = (window_w - self.render_w) // 2
        self.offset_y = (window_h - self.render_h) // 2

    def correct_mouse_position(self, event):
        """
        Traduz a posição do mouse da JANELA REAL para a TELA FALSA.
        """
        if hasattr(event, 'pos'):
            # Pega a posição real do mouse
            mx, my = event.pos
            
            # Remove as barras pretas (offset)
            mx -= self.offset_x
            my -= self.offset_y
            
            # Desfaz a escala (divide pelo ratio)
            mx /= self.scale_ratio
            my /= self.scale_ratio
            
            # Modifica o evento 'in place' para o resto do jogo usar
            event.pos = (int(mx), int(my))
            
        return event

    def setup_states(self):
        """
        Cria as instâncias de todos os estados do jogo.
        """
        
        self.states["CUTSCENE"] = CutsceneState()
        self.states["GAMEPLAY"] = GameplayState()
        
        # Define o estado inicial
        # (Se quiser testar a cutscene, mude para "CUTSCENE")
        self.current_state_name = "GAMEPLAY" 
        
        self.current_state = self.states[self.current_state_name]
        
        # Chama a função 'startup' do estado inicial
        self.current_state.startup({})

    def flip_state(self):
        """Função para trocar do estado atual para o próximo."""
        
        next_state_name = self.current_state.next_state
        persistent_data = self.current_state.persist
        
        self.current_state.done = False
        
        if next_state_name is None:
            self.running = False
            return
            
        self.current_state = self.states[next_state_name]
        self.current_state_name = next_state_name
        
        self.current_state.startup(persistent_data)

    def event_loop(self):
        """Processa todos os eventos."""
        for event in pygame.event.get():
            
            # 1. Lida com redimensionamento da janela
            if event.type == pygame.VIDEORESIZE:
                self.calculate_scale() 
                
            # 2. Corrige o mouse antes de mandar para o jogo
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                event = self.correct_mouse_position(event)

            self.current_state.handle_event(event)
            
    def update(self):
        """Atualiza a lógica."""
        self.current_state.update(self.dt)
        
        if self.current_state.quit:
            self.running = False
        elif self.current_state.done:
            self.flip_state()

    def draw(self):
        """Desenha com escala."""
        
        # 1. Desenha o jogo na TELA FALSA (800x600)
        self.fake_screen.fill((0, 0, 0))
        # Passamos a fake_screen, não a window real!
        self.current_state.draw(self.fake_screen)
        
        # 2. Escala a tela falsa para o tamanho que cabe na janela
        scaled_surface = pygame.transform.smoothscale(
            self.fake_screen, (self.render_w, self.render_h)
        )
        
        # 3. Limpa a janela real (preenche as barras pretas)
        self.window.fill((0, 0, 0))
        
        # 4. Cola a imagem do jogo centralizada na janela real
        self.window.blit(scaled_surface, (self.offset_x, self.offset_y))
        
        # Atualiza o display
        pygame.display.flip()

    def run(self):
        """O Loop Principal."""
        while self.running:
            self.event_loop()
            self.update()
            self.draw()
            self.dt = self.clock.tick(FPS) / 1000.0
            
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.setup_states()
    game.run()