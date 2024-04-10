import pygame.font


WHITE = (255,255,255)

pygame.font.init()

my_font = pygame.font.SysFont("Times New Roman", 30)


def get_text_surface(text, font=my_font, color=WHITE):
    """ used to get the text surface to display on the screen
        you will need to then call blit on the surface to display it using a location in the form of a tuple like this:

        window.blit(text_surface, (x, y))
        pygame.display.update()

    :param text: str
    :param font: pygame.font.Font
    :param color: pygame.Color
    """
    try:
        text = str(text)
        return font.render(text, False, color)
    except:
        print(f'Font Error: fix yo fonts. Trying to print: {text}')
        return font.render('Font Error', False, WHITE)
    
def normalize(list, max):
    #TODO: this stuff
    return 1

def get_npc_data_dict():
    return {
        "rect": None,
        "color": None,
        "on_screen": False,
        "health": 0,
        "mana": 0,
        "defence": 0,
        "power": 0,
        "npc_index":0,
        "class_type": None
    }

def get_player_data_dict():
    return {
        "rect": None,
        "color": None,
        "on_screen": False,
        "health": 0,
        "mana": 0,
        "defence": 0,
        "power": 0,
        "class_type": None
    }