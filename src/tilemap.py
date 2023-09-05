import pygame


# given a large image, split it into smaller ones with a grid
def parse(surf: pygame.Surface, size=(21, 21), scale=(0, 0)):
    surfs = []  # a 2d array - access image from coordinate using surfs[y][x]

    for y in range(0, surf.get_height(), size[1]):
        surfs.append([])

        for x in range(0, surf.get_width(), size[0]):
            cutout = surf.subsurface((x, y, *size))
            if scale != (0, 0):
                cutout = pygame.transform.scale(cutout, scale)
            surfs[-1].append(cutout.convert_alpha())

    return surfs
