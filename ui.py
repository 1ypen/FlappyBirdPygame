import pygame
import setting


class UI:
    def __init__(self):
        self.window = pygame.display.get_surface()

    def draw_welcome_screen(self):
        image_full = pygame.image.load('assets/sprites/message.png').convert_alpha()
        image = pygame.transform.scale(image_full, (setting.WIDTH // 1.5, setting.HEIGHT // 1.5))
        rect = image.get_rect(center=(setting.WIDTH / 2, setting.HEIGHT / 2))
        self.window.blit(image, rect)

    def draw_game_over_screen(self):
        image_full = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
        image = pygame.transform.scale(image_full, (image_full.get_width()*2, image_full.get_height()*2))
        rect = image.get_rect(center=(setting.WIDTH / 2, setting.HEIGHT / 5))
        self.window.blit(image, rect)


