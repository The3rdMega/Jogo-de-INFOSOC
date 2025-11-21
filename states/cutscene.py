#
# Arquivo: states/cutscene.py
#
import pygame
from states.base_state import BaseState
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class CutsceneState(BaseState):
    """
    Estado genérico para exibir uma cena estática (imagem + texto).
    Usado para: Intro, Game Over, Finais, etc.
    """
    
    def __init__(self):
        super().__init__()
        self.next_state = "GAMEPLAY" # Padrão
        
        # Dados da cena
        self.background_image = None
        self.title_text = ""
        self.subtitle_text = ""
        self.duration = 0
        self.wait_for_input = False
        self.start_time = 0
        
        # Configuração de Fontes
        try:
            self.font_title = pygame.font.SysFont('Arial', 60, bold=True)
            self.font_subtitle = pygame.font.SysFont('Arial', 32)
            self.font_prompt = pygame.font.SysFont('Arial', 20, italic=True)
        except:
            self.font_title = pygame.font.SysFont('sans-serif', 60, bold=True)
            self.font_subtitle = pygame.font.SysFont('sans-serif', 32)
            self.font_prompt = pygame.font.SysFont('sans-serif', 20, italic=True)
            
        self.text_color = (255, 255, 255) # Branco

    def startup(self, persistent_data):
        """
        Configura a cena com os dados recebidos.
        persistent_data pode conter:
        - 'image_path': Caminho da imagem de fundo.
        - 'title': Título principal.
        - 'subtitle': Texto secundário.
        - 'duration': Tempo em ms (se wait_for_input for False).
        - 'wait_for_input': Se True, espera clique para sair.
        - 'next_state': Para qual estado ir depois.
        """
        super().startup(persistent_data)
        
        self.start_time = pygame.time.get_ticks()
        
        # 1. Configurações Básicas
        self.next_state = persistent_data.get('next_state', "GAMEPLAY")
        self.duration = persistent_data.get('duration', 3000)
        self.wait_for_input = persistent_data.get('wait_for_input', False)
        self.title_text = persistent_data.get('title', "")
        self.subtitle_text = persistent_data.get('subtitle', "")
        
        # 2. Carrega a Imagem
        image_path = persistent_data.get('image_path')
        self.background_image = None
        
        if image_path:
            try:
                raw_image = pygame.image.load(image_path).convert() # .convert() é mais rápido para bg
                self.background_image = pygame.transform.scale(
                    raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
            except Exception as e:
                print(f"Erro ao carregar imagem da cutscene '{image_path}': {e}")
                # Se falhar, cria um fundo preto ou vermelho (se for game over)
                self.background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                if "ransomware" in str(image_path):
                    self.background_image.fill((150, 0, 0)) # Vermelho escuro
                else:
                    self.background_image.fill((0, 0, 0)) # Preto

    def handle_event(self, event):
        """Lida com cliques para pular a cena."""
        super().handle_event(event)
        
        # Se o jogo estiver esperando input para continuar
        if self.wait_for_input:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.done = True # Encerra a cena

    def update(self, dt):
        """Checa o tempo se não estiver esperando input."""
        
        if not self.wait_for_input:
            # Se o tempo passou
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                self.done = True

    def draw(self, screen):
        """Desenha a cena."""
        
        # 1. Fundo
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((0, 0, 0))
            
        # 2. Texto do Título (Centralizado)
        if self.title_text:
            title_surf = self.font_title.render(self.title_text, True, self.text_color)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            
            # Sombra simples para leitura melhor
            shadow_surf = self.font_title.render(self.title_text, True, (0, 0, 0))
            screen.blit(shadow_surf, (title_rect.x + 2, title_rect.y + 2))
            screen.blit(title_surf, title_rect)
            
        # 3. Texto do Subtítulo (Abaixo do título)
        if self.subtitle_text:
            sub_surf = self.font_subtitle.render(self.subtitle_text, True, self.text_color)
            sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            
            shadow_surf = self.font_subtitle.render(self.subtitle_text, True, (0, 0, 0))
            screen.blit(shadow_surf, (sub_rect.x + 2, sub_rect.y + 2))
            screen.blit(sub_surf, sub_rect)
            
        # 4. Aviso de "Clique para continuar" (se necessário)
        if self.wait_for_input:
            # Faz o texto piscar levemente
            alpha = abs(pygame.time.get_ticks() % 1000 - 500) / 2.0 # 0 a 250
            
            prompt_surf = self.font_prompt.render("Pressione qualquer tecla...", True, (200, 200, 200))
            # Hack para alpha em fontes
            prompt_surf.set_alpha(int(alpha + 50)) 
            
            prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            screen.blit(prompt_surf, prompt_rect)