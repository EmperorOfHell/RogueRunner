import pygame
from settings import *
from support import *


class Creature(pygame.sprite.Sprite):
    def __init__(self, pos, images, speed, group):
        super().__init__(group)
        self.status = "idle"
        self.speed = speed

        self.images = images
        self.frame_index = 0
        self.image = self.images[self.status][self.frame_index]

        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(bottomright=pos)

        self.mask = pygame.mask.from_surface(self.image)

        self.z = LAYERS["player"]

    def animate(self, dt):
        self.frame_index += len(self.images[self.status]) * dt
        self.frame_index %= len(self.images[self.status])
        self.image = self.images[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect()

    def move(self, dt):
        self.pos.x -= self.speed * dt
        self.rect.bottomright = round(self.pos)
        if self.pos.x <= -self.rect.width:
            self.kill()


    def update_status(self):
        if not self.status == 'attack' and self.pos.x <= 400:
            self.status = 'attack'
            self.frame_index = 0

    def update(self, dt, speed):
        # self.screen = pygame.display.get_surface()
        # pygame.draw.rect(self.screen, "red", self.rect, 1)
        self.update_status()
        self.animate(dt)
        self.move(dt)
        self.speed = speed
