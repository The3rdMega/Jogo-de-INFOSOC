#
# Arquivo: states/base_state.py
#
import pygame

class BaseState:
    """
    Uma classe "mãe" abstrata para todos os estados do jogo.
    
    Define a interface padrão que o main.py espera
    que cada estado tenha.
    """
    
    def __init__(self):
        """
        Inicializa as flags de controle de estado.
        """
        # Flag para sinalizar ao main.py que este estado terminou.
        self.done = False
        
        # Flag para sinalizar ao main.py que o jogo deve fechar.
        self.quit = False
        
        # O nome (string) do próximo estado para onde transicionar.
        # Ex: "GAMEPLAY", "END_SCREEN"
        self.next_state = None
        
        # (Opcional) Armazena dados para passar para o próximo estado.
        self.persist = {}

    def startup(self, persistent_data):
        """
        Chamado uma vez quando o estado se torna ativo.
        
        'persistent_data' é um dicionário vindo do estado anterior,
        útil para passar pontuação, nome do jogador, etc.
        """
        self.persist = persistent_data
        
    def handle_event(self, event):
        """
        Processa um único evento do Pygame (teclado, mouse).
        Deve ser sobrescrito pela classe filha.
        """
        # Exemplo: Lidar com o fechamento da janela
        if event.type == pygame.QUIT:
            self.quit = True

    def update(self, dt):
        """
        Atualiza a lógica do estado.
        'dt' (delta time) é o tempo em segundos desde o último frame.
        Deve ser sobrescrito pela classe filha.
        """
        pass # A lógica de atualização vai aqui

    def draw(self, screen):
        """
        Desenha o estado na tela.
        'screen' é a superfície principal (display) do Pygame.
        Deve ser sobrescrito pela classe filha.
        """
        # Exemplo: Limpar a tela (embora o main.py possa fazer isso)
        # screen.fill((0, 0, 0))
        pass # O código de desenho vai aqui