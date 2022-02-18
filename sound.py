import pygame


class Sound:

    def __init__(self):
        self.swoosh_sound = pygame.mixer.Sound('assets/audio/wing.wav')
        self.die_sound = pygame.mixer.Sound('assets/audio/die.wav')
        self.die_sound = pygame.mixer.Sound('assets/audio/hit.wav')

