import random

import pygame
from pygame.locals import *
from sprites import Bird, Ground, Pipe
import setting
from ui import UI
from sound import Sound

pygame.init()


class Game:

    def __init__(self, debug=False):

        self.width = setting.WIDTH
        self.height = setting.HEIGHT
        self.window_size = (self.width, self.height)
        self.timer = pygame.time.Clock()
        self.max_fps = setting.MAX_FPS

        self.window = self.create_window(self.window_size)

        self.ui = UI()
        self.sound = Sound()

        self.debug = debug

        self.running = True
        self.game_over = False
        self.score = 0

        self.pipe_frequency = 1500  # milliseconds
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency
        self.pass_pipe = False

        self.background_image_full = pygame.image.load('assets/sprites/background-night.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image_full, (self.width, self.height))

        self.bird = Bird()
        self.pipe_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.GroupSingle(self.bird)
        self.ground_group = pygame.sprite.GroupSingle(Ground())

        self.title = "Flappy bird"

    def run(self):

        while self.running:
            self.timer.tick(self.max_fps) / 1000

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_SPACE and self.game_over == False:
                        self.sound.swoosh_sound.play()
                        self.bird.flying = True
                        self.bird.jump()

            self.window.blit(self.background_image, (0, 0))

            self.pipe_group.draw(self.window)
            self.ground_group.draw(self.window)
            self.bird_group.draw(self.window)
            self.bird_group.update()

            if not self.bird.flying and not self.game_over:
                self.ui.draw_welcome_screen()

            if not self.bird.flying and self.game_over:
                self.ui.draw_game_over_screen()

            if self.bird.flying and not self.game_over:
                self.generate_pipes()
                self.ground_group.update()
                self.pipe_group.update()
                self.scoring()
                self.draw_score()

            self.check_collision()

            pygame.display.update()

        self.teardown()

    def create_window(self, size):
        return pygame.display.set_mode(size)

    def teardown(self):
        pygame.quit()

    def shutdown(self):
        self.running = False

    def check_collision(self):
        if self.bird.rect.bottom >= setting.GROUND_POSITION:
            self.bird.flying = False
            self.game_over = True
            self.sound.die_sound.play()
            self.reset_game()

        if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.bird.rect.top < 0:
            self.game_over = True
            self.bird.fall()

    def scoring(self):
        if self.pipe_group:
            # If a bird flew through the pipe
            if (self.bird_group.sprite.rect.left > self.pipe_group.sprites()[0].rect.left
                    and self.bird_group.sprite.rect.right < self.pipe_group.sprites()[0].rect.right
                    and not self.pass_pipe):
                self.pass_pipe = True

            if self.pass_pipe:
                if self.bird_group.sprite.rect.left > self.pipe_group.sprites()[0].rect.right:
                    self.score += 1
                    self.pass_pipe = False

    def draw_score(self):
        font = pygame.font.SysFont('Lucida Grande', 60)
        image = font.render(str(self.score), True, 'white')
        rect_center = image.get_rect(center=(setting.WIDTH / 2, setting.HEIGHT / 5))
        self.window.blit(image, rect_center)

    def generate_pipes(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_pipe > self.pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(self.width, int(self.height / 2) + pipe_height, 'bottom')
            top_pipe = Pipe(self.width, int(self.height / 2) + pipe_height, 'top')
            self.pipe_group.add(btm_pipe, top_pipe)
            self.last_pipe = time_now

    def reset_game(self):
        self.pipe_group.empty()
        self.bird_group.empty()
        self.bird = Bird()
        self.bird_group.add(self.bird)
        self.score = 0
        self.game_over = False


def main():
    app = Game(debug=True)
    app.run()


if __name__ == '__main__':
    main()
