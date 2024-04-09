import pygame
import random
import math
import json
from os import listdir
from os.path import isdir, join

import utilities
import npc
import player as plr

WIDTH, HEIGHT = 1000,1000
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH/5, HEIGHT/10
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 40
NPC_WIDTH, NPC_HEIGHT = 20, 40
MAX_VEL = 5
FPS = 60


pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Coding Club Example Code")

entities = []

class Entity:
    """
    Class for containing self made entities or as pygame calls them, sprites
    

    TODO: Change this out to make use of the Sprites from pygame
    """
    x, y = 0, 0
    on_screen = True
    rect = pygame.Rect(x,y,x,y)
    color = "green"

    def __init__(self, x=random.random()*WIDTH, y=random.random()*HEIGHT, width=PLAYER_WIDTH, height=PLAYER_HEIGHT):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

#TODO: make motion and direction deal by directions(rad) and distance(x)
def get_vel_towards(entity: pygame.sprite.Sprite, objective: pygame.sprite.Sprite):
    """
    When one entity needs to move towards another

    :param entity:
    :param objective
    """
    velx,vely = 0,0
    if entity.x < objective.x:
        velx = MAX_VEL
    else:
        velx = -MAX_VEL
    if entity.y < objective.y:
        vely = MAX_VEL
    else:
        vely = -MAX_VEL
    # Normalize the speed so the player doesn't move faster when going diagonal
    if math.sqrt(math.pow(velx, 2) + math.pow(vely, 2)) > MAX_VEL:
        velx, vely = velx/math.sqrt(2), vely/math.sqrt(2)
    

def draw(p_rect):
    """ Used to handle graphics to the screen. Drawn once per tick
    
    :param player (pygame.sprit.Sprite):
    """
    window.fill("black")
    pygame.draw.rect(window, "blue", p_rect)
    for ent in entities:
        pygame.draw.rect(window, ent.color, ent.rect)
    
    pygame.display.update()


def is_on_screen(ent):
    if ent.rect.right < 0 or ent.rect.left > WIDTH or ent.rect.bottom < 0 or ent.rect.top > HEIGHT:
        ent.on_screen = False
    return ent.on_screen


def update_position(vel_x, vel_y):
    #TODO: handle this using the groups provided by pygame
    for ent in entities:
        ent.x -= vel_x
        ent.y -= vel_y
        ent.update()

def save(player):
    """ save the current game data

    TODO: impliment multiple saves
    """
    print("Saving Data:")
    player_save_file = open("saves/player_save.json", "w")
    player_dict = utilities.get_player_data_dict()
    for variable in player_dict:
        player_dict[variable] = player.get(variable)
    json.dump(player_dict, player_save_file, indent=4)
    player_save_file.close()
    index = 0
    for npc_obj in npc.npc:
        npc_file = open(f"saves/player_save{index}.json", "w")
        npc_dict = utilities.get_npc_data_dict()
        for variable in npc_dict:
            npc_dict[variable] = npc.obj.get(variable)
        json.dump(npc_dict, npc_file, indent=4)
        npc_file.close()

def load_saves():
    print("Save Loaded")
    #make player object with the needed rect pass
    player_main = plr.Player(None)
    player_main.load(json.load("saves/player_save.json"))

def new_save():
    print("Load New Save")


def check_for_save() -> bool :
    for file in listdir("/"):
        if isdir(file) and file == "saves" :
            return True
    return False

def title_screen_loop():
    title_font = pygame.font.SysFont("Garamond", 80)
    new_game_button_color = "gray"
    new_game_button_rect = pygame.rect.Rect(WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/3 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
    new_game_button_text = utilities.get_text_surface("New Game")
    is_save = check_for_save()
    load_save_button_rect = pygame.rect.Rect(WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/3*2 - BUTTON_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)
    load_save_button_text = utilities.get_text_surface("Load Save")
    if is_save:
        load_save_button_color = "gray"
    else:
        load_save_button_color = "gray16"
    while True:
        clock.tick(60)
        mouse_pos= pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit(0)
        if is_save:
            if load_save_button_rect.collidepoint(*mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    load_saves()
                    break
                load_save_button_color = "gray69"
            else:
                load_save_button_color = "gray"
        if new_game_button_rect.collidepoint(*mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                new_save()
                break
            new_game_button_color = "gray69"
        else:
            new_game_button_color = "gray"
        window.fill("black")
        pygame.draw.rect(window, new_game_button_color, new_game_button_rect)
        window.blit(new_game_button_text, (new_game_button_rect.x + 10, new_game_button_rect.y + 10))
        pygame.draw.rect(window, load_save_button_color, load_save_button_rect)
        window.blit(load_save_button_text, (load_save_button_rect.x + 10, load_save_button_rect.y + 10))
        pygame.display.update()
    


def main():
    """ main function, 
    this is where we control things and call all of the stuff we want to happen in the game
    
    """
    player = plr.Player(pygame.Rect(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT))
    title_screen_loop() 
    running = True   
    while running:
        #Sets the Max FPS for the game to run at
        clock.tick(FPS)
        
        keys = pygame.key.get_pressed()
        vel_x, vel_y = 0, 0

        # Checks which keys are pressed sets the movement accordingly
        if keys[pygame.K_a]:
            vel_x -= MAX_VEL
        if keys[pygame.K_d]:
            vel_x += MAX_VEL
        if keys[pygame.K_s]:
            vel_y += MAX_VEL
        if keys[pygame.K_w]:
            vel_y -= MAX_VEL
        
        # Normalize the speed so the player doesn't move faster when going diagonal
        if math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)) > MAX_VEL:
            vel_x, vel_y = vel_x/math.sqrt(2), vel_y/math.sqrt(2)
        update_position(vel_x, vel_y)
        draw(player.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #TODO: add if player is loaded to prevent unnecisary saves (maybe never mind)
                save(player)
                running = False
    pygame.quit()


if __name__ == "__main__":
    main()

