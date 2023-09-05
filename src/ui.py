import pygame

cached = {}  # create a dictionary called cached. a dictionary stores values in key: value format.


class TextData:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.w, self.h = x, y, width, height


# get an id for each font face (after being used)
def cache_name(name, size, bold=False, italic=False):
    return str(name) + str(size) + str(bold) + str(italic)


# stops a new font object being created every frame you render ui
def cache(font, name):
    cached[name] = font
    return font


# given a name (filename or system), a size, and if its bold or italic - return a pygame.font.Font object
def get_font(name, size, bold=False, italic=False) -> pygame.font.Font:
    cname = cache_name(name, size, bold, italic)
    try:
        return cached[cname]
    except KeyError:
        try:
            return cache(pygame.font.Font(name, size), cname)
        except FileNotFoundError:
            return cache(pygame.font.SysFont(name, size, bold=bold, italic=italic), cname)


# blit text into world space
def text_world(game, txt, position, size=32, color=(0, 0, 0), font=None, aa=True, align="top-left", bold=False,
               italic=False):
    surf = get_font(font, size, bold, italic).render(txt, aa, color)
    game.camera.blit(surf, align_font(position, align, surf))


# blit text into screen space
def text_screen(game, txt, position, size=32, color=(0, 0, 0), font=None, aa=True, align="top-left", bold=False,
                italic=False):
    surf = get_font(font, size, bold, italic).render(txt, aa, color)
    game.wn.blit(surf, align_font(position, align, surf))


# blit text into a custom pygame.Surface()
def text_surf(dest, txt, position, size=32, color=(0, 0, 0), font=None, aa=True, align="top-left", bold=False,
              italic=False):
    surf = get_font(font, size, bold, italic).render(txt, aa, color)
    dest.blit(surf, align_font(position, align, surf))


# get x, y, width, height of a peice of text
def text_data(txt, position, size=32, font=None, align="top-left", bold=False, italic=False) -> TextData:
    surf = get_font(font, size, bold, italic).render(txt, False, (0, 0, 0))
    pos = align_font(position, align, surf)
    data = TextData(*pos, surf.get_width(), surf.get_height())
    return data


def button(dest, txt, position, size=32, text_color=(0, 0, 0), bg_color=(255, 255, 255), bg_color_hover=(230, 230, 230),
           font=None, aa=True, align="top-left", padding=5, border_radius=0, bold=False, italic=False, width=None):
    data = text_data(txt, position, size, font, align, bold, italic)

    mod = 0  # x offset for button background in case of a custom width
    if width is not None:  # if width is None, set background width to minimum needed to cover the text
        mod = (width - data.w) / 2

    rect = pygame.Rect(data.x - padding - mod, data.y - padding, data.w + padding * 2 + mod*2, data.h + padding * 2)

    hover = rect.collidepoint(*pygame.mouse.get_pos())
    color = bg_color_hover if hover else bg_color

    pygame.draw.rect(dest, color, rect, border_radius=border_radius)
    text_surf(dest, txt, position, size, text_color, font, aa, align, bold, italic)

    return hover


# syntax: "top-center", "bottom-right" etc
def align_font(position, align, surf) -> list:
    pos = list(position)
    split = align.split("-")

    if split[0] == "bottom":
        pos[1] -= surf.get_height()
    elif split[0] == "center":
        pos[1] -= surf.get_height() / 2

    if split[1] == "right":
        pos[0] -= surf.get_width()
    elif split[1] == "center":
        pos[0] -= surf.get_width() / 2

    return pos
