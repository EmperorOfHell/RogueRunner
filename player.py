import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprite):

        super().__init__(group)

        # general setup
        self.import_assets()
        self.status = 'run'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(bottomleft=self.pos)
        self.do_anim = True

        self.z = LAYERS['player']

        # collision
        self.health = HEALTH
        self.collision_sprite = collision_sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = Timer(1000, self.update_status)
        self.invisible = False
        # movement attribute
        self.gravity = GRAVITY

    def import_assets(self):
        self.animations = {'run': [], 'jump': [], 'run_hit': [], 'jump_hit': [], 'death': []}

        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):

        if self.do_anim:
            self.frame_index += len(self.animations[self.status]) * dt
            if self.status == 'death' and self.frame_index + 1 >= len(self.animations[self.status]):
                self.do_anim = False
            self.frame_index %= len(self.animations[self.status])
            self.image = self.animations[self.status][int(self.frame_index)]
            self.rect = self.image.get_rect(bottomleft=self.pos)

    def move(self):
        if self.status == 'jump' or\
                self.status == 'jump_hit':
            self.gravity += 1
            self.pos.y += self.gravity

            if self.pos.y >= HORIZON_HEIGHT:
                self.pos.y = HORIZON_HEIGHT
                self.frame_index = 0
                if self.status == 'jump':
                    self.status = 'run'
                elif self.status == "jump_hit":
                    self.status = 'run_hit'
                self.gravity = GRAVITY
            self.rect.y = round(self.pos.y)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.status != 'death':
            if self.status.find('hit') != -1:
                self.status = 'jump_hit'
            else:
                self.status = 'jump'
    def update_status(self):
        self.status = self.status.replace("_hit", "")
        self.invisible = False

    def death(self):
        if not self.status == 'death':
            self.frame_index = 0
        self.status = 'death'


    def collision(self):
        if self.status != 'death' and not self.invisible:
            if pygame.sprite.spritecollide(self, self.collision_sprite, False, pygame.sprite.collide_mask) \
                    and not self.status.find('hit') != -1:
                self.status = self.status + '_hit'
                self.timer.activate()
                self.health -= 1
                self.invisible = True

    def update(self, dt, speed):
        if self.timer.active:
            self.timer.update()
        self.collision()
        self.input()
        self.move()
        self.animate(dt)
