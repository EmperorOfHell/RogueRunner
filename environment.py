import random

import pygame
from settings import *
from support import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, image, speed, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.z = z
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(pos)
        self.to_remove = False

    def update(self, dt, speed):
        self.pos.x -= self.speed * dt
        if self.pos.x <= -self.rect.width:
            self.to_remove = True
            self.kill()
        self.rect.topleft = round(self.pos)
        self.speed = speed


class Background(Generic):
    def __init__(self, pos, images, speed, speed_coff, groups):
        self.start_pos = pygame.math.Vector2(pos)
        self.speed_coff = speed_coff
        super().__init__(pos=pos,
                         image=images,
                         speed=speed * speed_coff,
                         groups=groups,
                         z=LAYERS['background'])

    def update(self, dt, speed):
        self.pos.x -= self.speed * dt
        if self.pos.x <= self.start_pos.x - self.rect.width:
            self.pos.x = self.start_pos.x
        self.rect.topleft = round(self.pos)
        self.speed = speed * self.speed_coff


class Ground(Generic):
    def __init__(self, pos, types, speed, groups):
        self.type = random.randint(0, len(types) - 1)
        self.image = types[self.type]
        super().__init__(pos=pos,
                         image=self.image,
                         speed=speed,
                         groups=groups)


class Decoration(Generic):
    def __init__(self, pos, types, speed, groups):
        self.type = random.randint(0, len(types) - 1)
        self.image = types[self.type]
        self.pos = (pos[0], pos[1] - self.image.get_rect().height)
        super().__init__(pos=self.pos,
                         image=self.image,
                         speed=speed,
                         groups=groups,
                         z=LAYERS['decoration'])


class Rock(Generic):
    def __init__(self, pos, types, speed, groups):
        self.type = random.randint(0, len(types) - 1)
        self.image = types[self.type]
        self.pos = (pos[0], pos[1] - self.image.get_rect().height)
        super().__init__(pos=self.pos,
                         image=self.image,
                         speed=speed,
                         groups=groups)
