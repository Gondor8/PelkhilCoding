import pygame
import random
import math

import constants as c

class Biome:
    """
    
    """
    owner: pygame.sprite.Group
    color: pygame.color.Color
    center: tuple
    #wall_radius: int
    
    def __init__(self, center:tuple, owner=None):
        self.center = center
        print(center)
        self.owner = owner

    def make_wall(self, radius):
        wall_list = []
        for i in range(0,c.MAP_WIDTH):
            for j in range(0,c.MAP_HEIGHT):
                dist = int(math.sqrt((i*c.TILE_WIDTH-self.center[0])**2 + (j*c.TILE_HEIGHT-self.center[1])**2))
                #base off of wall radius
                if dist > radius - (c.TILE_WIDTH) and dist < radius + (c.TILE_HEIGHT):
                    wall_list.append((i,j))
        return wall_list


class Biome_tiles():
    """ This class stores all of the different biome and land control data from all of the different groups.
    """

    rect: pygame.rect.Rect
    color: pygame.color.Color
    name: str
    biome_type: str
    index_i:int 
    index_j:int

    def __init__(self, index_i, index_j, rect=None, color="green", name=None, biome_type="plain") -> None:
        self.rect = rect
        #TODO: make this based off of the biome type
        # self.color = pygame.color.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = color
        self.name = name
        self.biome_type = biome_type
        self.index_i = index_i
        self.index_j = index_j


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
                # self.tiles[i][j] = Biome_tiles(i, j, pygame.rect.Rect(i*c.TILE_WIDTH-(c.MAP_WIDTH*c.TILE_WIDTH/2), j*c.TILE_HEIGHT-(c.MAP_HEIGHT*c.TILE_HEIGHT/2), c.TILE_WIDTH, c.TILE_HEIGHT), color="white")
                self.tiles[i][j] = Biome_tiles(i, j, pygame.rect.Rect(i*c.TILE_WIDTH, j*c.TILE_HEIGHT, c.TILE_WIDTH, c.TILE_HEIGHT), color="white")

                # TODO:Impliment render distance
        for group in ["red", "white", "blue", "green", "black","yellow"]:
            self.biome_dict[group] = Biome((random.randint(0,c.MAP_WIDTH)*c.TILE_WIDTH, random.randint(0,c.MAP_HEIGHT)*c.TILE_HEIGHT))
        self.make_fortresses()
        # #DEBUG START
        # for i in range(0, int(c.MAP_WIDTH/2)):
        #     for j in range(0, int(c.MAP_HEIGHT/2)):
        #         self.tiles[i][j].color = "black"
        # #DEBUG END


    def make_fortresses(self):
        for group in self.biome_dict:
            wall_list = self.biome_dict[group].make_wall(random.randint(c.TILE_WIDTH*4,c.TILE_WIDTH*10))
            for tup in wall_list:
                self.tiles[tup[0]][tup[1]].color = "black"


    def get(self, variable):
        """
        """
        return eval(variable, globals(), self.__dict__)
    
    def get_biome_data_dict(self, location: tuple):
        for tile in self.tiles:
            if tile.rect.collidepoint(location):
                return {
                    "rect": tile.rect,
                    "color": tile.color,
                    "name": tile.name,
                    "biome_type": tile.biome_type
                }
    
    def get_surface(self)-> pygame.surface.Surface:
        """
        """
        if self.surface == None:
            self.surface = pygame.surface.Surface((c.MAP_WIDTH*c.TILE_WIDTH, c.MAP_HEIGHT*c.TILE_HEIGHT))
            # DEBUG START
            temp_list = []
            # DEBUG END
            for k in range(0, c.MAP_WIDTH):
                temp_list.append([])
                for l in range(0,c.MAP_HEIGHT):
                    #DEBUG START
                    # if self.tiles[k][l].color == "black":
                    #     temp_list[k].append(1)
                    # else:
                    #     temp_list[k].append(0)
                    temp_list[k].append((self.tiles[k][l].rect.x, self.tiles[k][l].rect.y))
                    #DUBUG END
                    pygame.draw.rect(self.surface, self.tiles[k][l].color, self.tiles[k][l].rect)
        return self.surface
        
        
