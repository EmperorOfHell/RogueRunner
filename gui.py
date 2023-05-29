import math

import pygame
from settings import *
from support import *
from timer import Timer


class Score(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.score = 0
        self.fnt = pygame.font.Font('fonts/Abaddon-Bold.ttf', 30)
        self.fnt2 = pygame.font.Font('fonts/Abaddon-Bold.ttf', 30)
        self.offset = pygame.math.Vector2(5, 5)
        self.z = LAYERS['gui']
        self.setup()

    def setup(self):
        self.image = self.fnt.render(f"Score: {self.score}", False, 'white')
        self.rect = self.image.get_rect(topleft=self.offset)

    def update(self, dt, score):
        self.setup()




class Heart(pygame.sprite.Sprite):
    def __init__(self, group, pos, frame):
        super().__init__(group)
        # general
        self.math = None
        self.frame_index = frame
        self.import_assets()
        self.z = LAYERS['gui']
        self.state = "full"
        self.image = self.states[self.state]
        self.rect = self.image.get_rect(topright=(pos))
        self.pos = pygame.math.Vector2(pos)
        self.offset = self.pos.y
        self.c_points = 3
        self.timer = Timer(500, self.make_empty)

    def import_assets(self):
        full_path = 'graphics/gui/health'
        self.states = {'full': [], 'empty': [], 'hit': []}
        for state in self.states.keys():
            self.states[state] = pygame.image.load(full_path + '/' + state + ".png")

    def animate(self):
        self.pos.y = self.offset + math.sin(2 * math.pi / self.c_points * self.frame_index)
        self.rect.y = round(self.pos.y)

    def update(self, dt, speed):
        self.frame_index += self.c_points * dt
        self.frame_index %= self.c_points
        self.animate()
        self.update_state()
        if self.timer.active:
            self.timer.update()

    def make_empty(self):
        self.state = "empty"

    def take_hit(self):
        self.state = "hit"
        self.timer.activate()

    def update_state(self):
        self.image = self.states[self.state]


class Hearts:
    def __init__(self, group, health):
        self.health = health
        self.hearts = []
        self.current_heart = 0
        self.offset = pygame.math.Vector2(5, 10)
        for i in range(self.health):
            self.hearts.append(Heart(group,
                                     (SCREEN_WIDTH - (self.offset.x + 30) * i - self.offset.x,
                                      self.offset.y),
                                     i))

    def update(self, health):
        if health < self.health and self.health != 0:
            self.health -= 1
            self.hearts[self.current_heart].take_hit()
            self.current_heart += 1
