import pygame

# TODO: figure out how to do this for all files and packages
WIDTH, HEIGHT = 1000,1000
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 40
NPC_WIDTH, NPC_HEIGHT = 20, 40
MAX_VEL = 5
FPS = 60


red = pygame.sprite.Group()
white = pygame.sprite.Group()
blue = pygame.sprite.Group()
green = pygame.sprite.Group()
black = pygame.sprite.Group()
yellow = pygame.sprite.Group()
npc = pygame.sprite.Group()

class AbstractNPC(pygame.sprite.Sprite):
    """
    Abstract class for any non-player characters
    used to give consistancy of how sprites should be handled in this game
    """
    rect: pygame.rect.Rect
    color: pygame.Color
    on_screen: bool
    health: int
    mana: int
    defence: int
    power: int
    class_type: str
    
    def __init__(self, rect, *groups):
        super().__init__(*groups)
        self.rect = rect
        self.on_screen = self.check_on_screen()
        self.add(npc)

    def change_group(self, old_group, new_group):
        """ used to do both remove and add groups in one method

        :param old_group: group whicht the NPC belongs to and needs to be removed from
        :param new_group: group to be added
        """
        self.remove(old_group)
        self.add(new_group)
    
    def move(self, velx, vely):
        """
        Takes in intended motion for each NPC and updates its postion
        NO CHECKING DONE AT THIS LEVEL

        :param velx: motion in the x direction
        :param vely: motion in the y direction
        """
        self.x += velx
        self.y += vely


    # check if the edges of the rectangle representing this NPC is on the screen, stored in a bool for all NPCs
    def check_on_screen(self):
        
        self.on_screen = not(self.rect.right < 0 
                             or self.rect.left > WIDTH 
                             or self.rect.bottom < 0 
                             or self.rect.top > HEIGHT)
        
    
    def load(self, save_dict):
        """
        
        TODO: add tryblocks to prevent save corruption
        """
        rect = self.rect_loader(save_dict["rect"])
        color = self.color_loader(save_dict["color"])
        on_screen = save_dict["on_screen"]
        health = save_dict["health"]
        mana = save_dict["mana"]
        defence = save_dict["defence"]
        power = save_dict["power"]
        class_type = save_dict["class_type"]

    def rect_loader(rect_save):
        """ for loading the converted/ overridden string cast for rect.
        
        :param rect_save: list(left(float),top(float),width(float),height(float))
        """
        return pygame.rect.Rect(rect_save[0], rect_save[1], rect_save[2], rect_save[3])
    
    def color_loader(color_save) -> pygame.color.Color:
        """ for loading the converted/overriden string cast for color
        
        :param color_save: list(r(int), g(int), b(int))
        """
        return pygame.color.Color(color_save[0], color_save[1], color_save[2])
        
    def get(self, variable):
        # pygame.Rect, string cast does not play nice with json so this fixes it
        print(variable)
        if (variable == "rect"):
            return [self.rect.left, self.rect.top, self.rect.width, self.rect.height]
        if (variable == "color"):
            return [self.color.r, self.color.g, self.color.b]
        print(eval(variable, globals(), self.__dict__))
        return eval(variable, globals(), self.__dict__)


class Combatant(AbstractNPC):
    """
    """
    def __init__(self, *groups, rect=None, x=WIDTH/2, y=HEIGHT/2, width=NPC_WIDTH, height=NPC_HEIGHT):
        if rect:
            super().__init__(rect, *groups)
        else:
            super().__init__(pygame.Rect(x, y, width, height), *groups)
    

class Civilian(AbstractNPC):
    """
    """
    def __init__(self, *groups, rect=None,  x=WIDTH/2, y=HEIGHT/2, width=NPC_WIDTH, height=NPC_HEIGHT):
        if rect:
            super().__init__(rect, *groups)
        else:
            super().__init__(pygame.Rect(x, y, width, height), *groups)

# class Soldier(pygame.sprite.Sprite):

#     def __init__(self, x, y, width, height, color):
#         super.__init__()
#         self.rect = pygame.Rect(x,y,width,height)
#         self.color = color
#         self.x_ind_vel = 0
#         self.y_ind_vel = 0
#         self.direction = 0
#         self.health = 1
#         self.mask = None

