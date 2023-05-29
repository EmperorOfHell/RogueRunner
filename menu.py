import pygame
from settings import *
from support import *


class Menu:
    def __init__(self, screen):
        self.display_surface = screen
        self.blood_start_gr = pygame.sprite.Group()
        self.blood_end_gr = pygame.sprite.Group()
        self.fnt_large = pygame.font.Font('fonts/Abaddon-Bold.ttf', 40)
        self.fnt_small = pygame.font.Font('fonts/Abaddon-Bold.ttf', 20)
        self.blood_start = BloodScreen(self.blood_start_gr, "backward")
        self.blood_end = BloodScreen(self.blood_end_gr, "forward")
        self.setup()

    def setup(self):
        self.lose_img = pygame.image.load('graphics/gui/death.png')
        self.wish = self.fnt_large.render("LOL", False, 'white')
        self.score = self.fnt_large.render("Score: 0", False, 'white')
        self.name = pygame.image.load('graphics/gui/name.png')
        self.start = self.fnt_small.render("Press ENTER to START GAME!", False, 'white')
        self.lose = self.fnt_large.render("You lose!", False, 'white')


    def update_score(self, score):
        self.score = self.fnt_small.render(f"Score: {score}", False, 'white')
        if score < 10:
            self.wish = self.fnt_small.render(f"Pfff! You can do better.", False, 'white')
        elif score < 30:
            self.wish = self.fnt_small.render(f"Great result!", False, 'white')
        else:
            self.wish = self.fnt_small.render(f"LOOOOL!", False, 'white')
    def start_menu(self):
        self.display_surface.fill((75, 16, 1))
        self.display_surface.blit(self.start, self.start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120)))
        self.display_surface.blit(self.name, self.name.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

    def start_anim(self, dt):
        self.blood_start_gr.update(dt)
        self.blood_start_gr.draw(self.display_surface)

    def lose_anim(self, dt):
        self.blood_end_gr.update(dt)
        self.blood_end_gr.draw(self.display_surface)
        if not self.blood_end.animation:
            self.display_surface.blit(self.lose, self.lose.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
            self.display_surface.blit(self.lose_img, self.lose_img.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 2 * self.lose_img.get_rect().height)))
            self.display_surface.blit(self.wish, self.wish.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 3 * self.wish.get_rect().height)))
            self.display_surface.blit(self.score, self.score.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 4 * self.score.get_rect().height)))


class BloodScreen(pygame.sprite.Sprite):
    def __init__(self, group, direct):
        super().__init__(group)

        # images
        self.import_assets()
        self.direct = direct
        self.frame_index = 0
        self.image = self.frames[self.direct][self.frame_index]
        self.rect = self.image.get_rect()
        self.animation = True

    def import_assets(self):
        full_path = 'graphics/gui/blood_screen/'
        self.frames = {"forward": [], "backward": []}
        for direct in self.frames.keys():
            self.frames[direct] = import_folder(full_path + direct)

    def animate(self, dt):

        if self.animation:
            self.image = self.frames[self.direct][round(self.frame_index)]
            self.frame_index += len(self.frames[self.direct]) * dt

    def update(self, dt):

        if not len(self.frames[self.direct]) - 8 < self.frame_index:
            self.animate(dt)
        else:
            self.animation = False
            self.frame_index = 0
