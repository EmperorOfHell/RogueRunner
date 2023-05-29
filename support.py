from os import walk

import pygame.image


def import_folder(path):
    surface_list = []

    for _,__,folder_items in walk(path):
        for item in folder_items:
            full_path = path + '/' + item
            item_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(item_surf)

    return surface_list