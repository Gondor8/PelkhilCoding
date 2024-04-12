import pygame
import random
import math
import json
import os


import constants as c
from constants import Identity
import utilities
import npc
import map
import player as plr

os.chdir(c.PTWD)

WIDTH, HEIGHT = c.WIDTH, c.HEIGHT
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH/5, HEIGHT/10
PLAYER_WIDTH, PLAYER_HEIGHT = c.PLAYER_WIDTH, c.PLAYER_HEIGHT
NPC_WIDTH, NPC_HEIGHT = c.NPC_WIDTH, c.NPC_HEIGHT
MAX_VEL = c.MAX_VEL
FPS = c.FPS

game_map: map.Map

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = plr.Player(pygame.Rect(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT))
ref_x, ref_y = 0,0

pygame.display.set_caption("Coding Club Example Code")
    

def draw(p_rect):
    """ Used to handle graphics to the screen. Drawn once per tick
    
    :param player (pygame.sprit.Sprite):
    """
    window.fill("red")
    window.blit(game_map.get_surface(), (ref_x-c.MAP_WIDTH/2, ref_y-c.MAP_HEIGHT/2))
    pygame.draw.rect(window, "blue", p_rect)    
    pygame.display.update()


def update_position(vel_x, vel_y):
    #TODO: handle this using the groups provided by pygame
    global ref_x, ref_y
    if player.rect.x + vel_x < WIDTH/10:
        ref_x -= vel_x
    elif player.rect.x + vel_x > WIDTH * 9/10:
        ref_x -= vel_x
    else:
        player.rect.x += vel_x
    if player.rect.y + vel_y < HEIGHT/10:
        ref_y -= vel_y
    elif player.rect.y + vel_y > HEIGHT * 9/10:
        ref_y -= vel_y
    else:
        player.rect.y += vel_y

def save():
    """ save the current game data

    TODO: impliment multiple saves
    """
    print("Saving Data:")
    
    index = 0
    for npc_obj in c.npc:
        if isinstance(npc_obj, Identity):
            continue
        npc_file = open(f"saves/player_save{index}.json", "w")
        npc_dict = utilities.get_npc_data_dict()
        for variable in npc_dict:
            npc_dict[variable] = npc_obj.get(variable)
        json.dump(npc_dict, npc_file, indent=4)
        npc_file.close()

def load_saves():
    print("Save Loaded")
    #make player object with the needed rect pass
    player_main = plr.Player(None)
    with open("saves/player_save.json", "r") as player_save:
        player_main.load(json.load(player_save))
        player_save.close()
    for file in os.listdir("saves"):
        if file != "player_save.json":
            with open(f"saves/{file}", "r") as npc_save:
                #change this so the loaded npc is not always a Combatant
                npc_obj = npc.Combatant(None)
                npc_obj.load(json.load(npc_save))
                c.npc.append(npc_obj)
                npc_save.close()

def new_save():
    global game_map
    print("Load New Save")
    game_map = map.Map()


def check_for_save() -> bool :
    for file in os.listdir():
        if os.path.isdir(file) and file == "saves" :
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
        window.blit(utilities.get_text_surface("Coding Club Example", title_font), (WIDTH/2 - 300, HEIGHT/10))
        pygame.draw.rect(window, new_game_button_color, new_game_button_rect)
        window.blit(new_game_button_text, (new_game_button_rect.x + 10, new_game_button_rect.y + 10))
        pygame.draw.rect(window, load_save_button_color, load_save_button_rect)
        window.blit(load_save_button_text, (load_save_button_rect.x + 10, load_save_button_rect.y + 10))
        pygame.display.update()
    


def main():
    """ main function, 
    this is where we control things and call all of the stuff we want to happen in the game
    
    """
    
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

        # Exit the game, can be used later to handle other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #TODO: add if player is loaded to prevent unnecisary saves (maybe never mind)
                save()
                running = False
    pygame.quit()


def startup():
    print("Finish Startup")
    pass


if __name__ == "__main__":
    startup()
    main()

