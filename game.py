import pygame, sys
from pygame import RESIZABLE

from settings import *
from level import Level
from menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.fake_screen = self.screen.copy()
        # self.screen = pygame.display.set_mode((1280, 720), RESIZABLE)
        self.clock = pygame.time.Clock()
        self.game_speed = 300
        self.level = Level(self.game_speed, self.screen)
        self.menu = Menu(self.screen)
        self.game_start = False

    def run(self):
        self.menu.start_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(FPS) / 1000
            self.input()
            # self.level.run(dt)

            if self.game_start:

                if self.level.is_active:
                    self.level.run(dt)
                    self.menu.start_anim(dt)
                else:
                    self.menu.update_score(self.level.score.score)
                    self.menu.lose_anim(dt)
            pygame.display.update()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.game_start = True
