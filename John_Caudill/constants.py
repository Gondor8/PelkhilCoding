import pygame

PTWD = "John_Caudill/"
WIDTH, HEIGHT = 1000,1000
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH/5, HEIGHT/10
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 40
NPC_WIDTH, NPC_HEIGHT = 20, 40
MAP_WIDTH, MAP_HEIGHT = 100, 100
TILE_WIDTH, TILE_HEIGHT = 10, 10
MAX_VEL = 5
FPS = 60

red = pygame.sprite.Group()
white = pygame.sprite.Group()
blue = pygame.sprite.Group()
green = pygame.sprite.Group()
black = pygame.sprite.Group()
yellow = pygame.sprite.Group()
npc = pygame.sprite.Group()