import pygame
import setting
from pygame import sprite
from utils import load_images


class Bird(sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.animations = load_images('assets/sprites/bird')
        self.image_frame_index = 0
        self.image = self.animations[self.image_frame_index]
        self.rect = self.image.get_rect(x=100, y=setting.HEIGHT / 2)
        self.vel = 0
        self.flying = False

        self.animation_delta = 40
        self.animation_speed = 0.1

    def move(self):
        # gravity
        if self.flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            # ground
            if self.rect.bottom < setting.GROUND_POSITION:
                self.rect.y += int(self.vel)

        # sky
        if self.rect.y < 0:
            self.rect.y = 0

    def jump(self):
        self.vel = -10

    def animate(self):

        if self.flying:
            self.image_frame_index += self.animation_speed
            if self.image_frame_index >= len(self.animations):
                self.image_frame_index = 0

            self.image = pygame.transform.rotate(self.animations[int(self.image_frame_index)], self.vel * -2)

    def fall(self):
        self.image = pygame.transform.rotate(self.animations[int(self.image_frame_index)], -90)

    def update(self):
        self.move()
        self.animate()


class Ground(sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.rect = self.image.get_rect(center=(setting.WIDTH // 2, 0), y=setting.GROUND_POSITION)

        self.ground_scroll = 0
        self.scroll_speed = setting.SCROLL_SPEED

    def scroll(self):
        self.ground_scroll -= self.scroll_speed
        if abs(self.ground_scroll) > 45:
            self.ground_scroll = 0

        self.rect.x = self.ground_scroll

    def update(self):
        self.scroll()


class Pipe(sprite.Sprite):
    def __init__(self, x: int, y: int, direction: str):
        pygame.sprite.Sprite.__init__(self)

        self.image_full = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_full, (104, 640))
        self.rect = self.image.get_rect()
        self.pipe_gap = 160
        self.scroll_speed = setting.SCROLL_SPEED

        if direction == 'top':
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.pipe_gap / 2)]

        if direction == 'bottom':
            self.rect.topleft = [x, y + int(self.pipe_gap / 2)]

    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()
