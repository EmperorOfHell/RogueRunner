import random
import time

import pygame
from settings import *
from player import Player
from environment import *
from creatures import *
from gui import *


class Level:
    def __init__(self, game_speed, display_surface):
        # get the display
        self.display_surface = display_surface
        self.start_speed = game_speed
        self.game_speed = game_speed
        # sprite groups
        self.all_sprites = CameraGroup(self.display_surface)
        self.collision_sprite = pygame.sprite.Group()
        self.setup()
        self.is_active = True

    def setup(self):
        self.import_decoration()
        self.import_creature()
        self.background = []
        self.ground = []
        self.creatures_call = [self.create_skeleton, self.create_eye]

        # background
        for i in range(len(self.environment['background'])):
            self.background.append(Background((0, 0),
                                              self.environment['background'][i],
                                              self.game_speed,
                                              SPEED_COFF['background'][i],
                                              self.all_sprites))
            self.background.append(Background((self.background[i].rect.width , 0),
                                              self.environment['background'][i],
                                              self.game_speed,
                                              SPEED_COFF['background'][i],
                                              self.all_sprites))
        # ground
        for i in range(round(SCREEN_WIDTH / self.environment['ground'][0].get_rect().width) + 1):
            self.ground.append(Ground((i * self.environment['ground'][0].get_width(), HORIZON_HEIGHT),
                                      self.environment['ground'],
                                      self.game_speed * SPEED_COFF['main'],
                                      self.all_sprites))
        # decoration
        self.decoration = Decoration((SCREEN_WIDTH, HORIZON_HEIGHT),
                                     self.environment['decoration'],
                                     self.game_speed * SPEED_COFF['decoration'],
                                     self.all_sprites)
        self.rock = Rock((SCREEN_WIDTH / 2, HORIZON_HEIGHT),
                         self.environment['rock'],
                         self.game_speed * SPEED_COFF['rock'],
                         self.all_sprites)
        # creature
        self.creature = self.creatures_call[random.randint(0, 1)]()

        self.player = Player((HORIZON_POS, HORIZON_HEIGHT + 3), self.all_sprites, self.collision_sprite)

        self.hearts = Hearts(self.all_sprites, self.player.health)
        self.score = Score(self.all_sprites)

    def create_skeleton(self):
        return Creature((1.2 * SCREEN_WIDTH, HORIZON_HEIGHT),
                        self.creatures['skeleton'],
                        self.game_speed * SPEED_COFF['main'],
                        [self.all_sprites, self.collision_sprite])

    def create_eye(self):
        return Creature((1.2 * SCREEN_WIDTH, random.randint(HORIZON_HEIGHT / 2 - 50, HORIZON_HEIGHT - 50)),
                        self.creatures['flying_eye'],
                        self.game_speed * SPEED_COFF['main'],
                        [self.all_sprites, self.collision_sprite])

    def import_decoration(self):
        self.environment = {'background': [], 'ground': [], 'grass': [], 'decoration': [], 'rock': []}

        for asset in self.environment.keys():
            full_path = 'graphics/environment/' + asset
            self.environment[asset] = import_folder(full_path)

    def import_creature(self):
        self.creatures = {'skeleton': [], 'flying_eye': []}
        status = {'idle': [], 'attack': []}
        for c_type in self.creatures.keys():
            for s_type in status.keys():
                full_path = 'graphics/monsters/' + c_type + "/" + s_type
                status[s_type] = import_folder(full_path)
                self.creatures[c_type] = status.copy()

    def update(self):

        if not self.collision_sprite.has(self.creature):
            self.creature = self.creatures_call[random.randint(0, 1)]()
            if self.player.status.find('hit') == -1:
                self.score.score += 1
                self.game_speed = self.start_speed + 20 * self.score.score // 5
        self.hearts.update(self.player.health)

        for gr in self.ground:
            if gr.to_remove:
                self.ground.remove(gr)
                del gr
                self.ground.append(Ground((self.ground[-1].rect.x + self.ground[-1].rect.width - 1,
                                           HORIZON_HEIGHT),
                                          self.environment['ground'],
                                          self.game_speed * SPEED_COFF['main'],
                                          self.all_sprites))
        if self.decoration.to_remove:
            self.decoration = Decoration((SCREEN_WIDTH, HORIZON_HEIGHT),
                                         self.environment['decoration'],
                                         self.game_speed * SPEED_COFF['decoration'],
                                         self.all_sprites)
        if self.rock.to_remove:
            self.rock = Rock((SCREEN_WIDTH, HORIZON_HEIGHT),
                             self.environment['rock'],
                             self.game_speed * SPEED_COFF['rock'],
                             self.all_sprites)
        if self.hearts.health < 1:
            self.game_speed = self.game_speed * .97
            self.player.death()
            if round(self.game_speed) == 0:
                self.is_active = False

    def run(self, dt):
        if self.is_active:
            self.display_surface.fill('black')
            self.update()
            self.all_sprites.layer_draw()
            self.all_sprites.update(dt, self.game_speed)



class CameraGroup(pygame.sprite.Group):
    def __init__(self, display_surface):
        super().__init__()
        self.display_surface = display_surface
        self.offset = pygame.math.Vector2()

    def layer_draw(self):

        for layer in LAYERS.values():
            for sprite in self.sprites():

                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
