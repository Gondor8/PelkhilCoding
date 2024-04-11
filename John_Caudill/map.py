import pygame
import random
import math

import constants as c

#TODO: add save functionallity
#TODO: map change update handling
#TODO: Biome coloring and non npc related Biomes

class Biome:
    """
    
    """

    # REMINDER: Update the save funciton with any new data 
    owner: pygame.sprite.Group
    owner_name: str
    color: pygame.color.Color
    center: tuple
    #wall_radius: int
    
    def __init__(self, center:tuple, owner=None, color="grey"):
        self.color = color
        self.center = center
        self.owner = owner
        if owner == None:
            self.owner_name = ""
        else:
            self.owner_name = self.find_owner()


    def find_owner() -> str:
        """ TODO: Finish implimenting this
        """
        return ""

    def make_wall(self, radius):
        wall_list = [[],[]]
        for i in range(0,c.MAP_WIDTH):
            for j in range(0,c.MAP_HEIGHT):
                dist = int(math.sqrt((i*c.TILE_WIDTH-self.center[0])**2 + (j*c.TILE_HEIGHT-self.center[1])**2))
                #base off of wall radius
                if dist < radius + (c.TILE_HEIGHT):
                    if dist > radius - (c.TILE_WIDTH):
                        wall_list[0].append((i,j))
                    else:
                        wall_list[1].append((i,j))
        return wall_list
    

    def get_save_data(self) -> dict:
        return {
            "owner_name": self.owner_name,
            "color": self.color,
            "center": [self.center[0],self.center[1]]
        }


class Biome_tiles():
    """ This class stores all of the different biome and land control data from all of the different groups.
    """

    rect: pygame.rect.Rect
    color: pygame.color.Color
    name: str
    biome_type: str
    index_i:int 
    index_j:int

    def __init__(self, index_i, index_j, rect=None, color="light grey", name=None, biome_type="plain") -> None:
        self.rect = rect
        #TODO: make this based off of the biome type
        # self.color = pygame.color.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = color
        self.name = name
        self.biome_type = biome_type
        self.index_i = index_i
        self.index_j = index_j
    
    def get_save_data(self) -> dict:
        rect_list = [self.rect.x, self.rect.y, self.rect.w, self.rect.h]
        if isinstance(self.color, tuple):
            #color could be stored in two types, either a tuple of len 3 or 4
            color_list = list(self.color)
        else: 
            # or as string, and we can't put tuples in .json files
            color_list = self.color
        return{
            "index_i": self.index_i,
            "index_j": self.index_j,
            "rect": rect_list,
            "color": color_list,
            "name": self.name,
            "biome_type": self.biome_type,
        }


class Map:
    """ This class stores all of the different biome and land control data from all of the different groups.

    The different terains are stored as rectangles with a color and a name. 
    
    """
    biome_dict: dict
    tiles: list
    surface: pygame.surface.Surface

    def __init__(self) -> None:
        """
        """
        self.surface = None
        self.tiles = [[None for n in range(0,c.MAP_WIDTH)]for m in range(0,c.MAP_HEIGHT)]
        self.biome_dict = {}
        for i in range(0,c.MAP_WIDTH):
            for j in range(0,c.MAP_HEIGHT):
                self.tiles[i][j] = Biome_tiles(i, j, pygame.rect.Rect(i*c.TILE_WIDTH, j*c.TILE_HEIGHT, c.TILE_WIDTH, c.TILE_HEIGHT))
                # TODO:Impliment render distance
        for group in ["red", "white", "blue", "green", "black","yellow"]:
            self.biome_dict[group] = Biome((random.randint(0,c.MAP_WIDTH)*c.TILE_WIDTH, random.randint(0,c.MAP_HEIGHT)*c.TILE_HEIGHT), color=group)
        self.make_fortresses()


    def make_fortresses(self):
        for group in self.biome_dict:
            wall_list = self.biome_dict[group].make_wall(random.randint(c.TILE_WIDTH*4,c.TILE_WIDTH*10))
            for tup in wall_list[0]:
                # changes color of wall tiles
                self.tiles[tup[0]][tup[1]].color = "black"
            for tup in wall_list[1]:
                #changes color of interior of wall tiles
                self.tiles[tup[0]][tup[1]].color = self.biome_dict[group].color


    def get(self, variable):
        """
        """
        if variable == "biomes":
            temp_dict = {}
            for biome in self.biome_dict:
                temp_dict[biome] = self.biome_dict[biome].get_save()
        return eval(variable, globals(), self.__dict__)
    

    
    def get_surface(self)-> pygame.surface.Surface:
        """
        """
        if self.surface == None:
            self.surface = pygame.surface.Surface((c.MAP_WIDTH*c.TILE_WIDTH, c.MAP_HEIGHT*c.TILE_HEIGHT))
            for k in range(0, c.MAP_WIDTH):
                for l in range(0,c.MAP_HEIGHT):
                    pygame.draw.rect(self.surface, self.tiles[k][l].color, self.tiles[k][l].rect)
        return self.surface
        
        
