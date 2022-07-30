from math import dist, sqrt
from tkinter import DISABLED, RIGHT, NORMAL

from config import *
from crosses import add_cross
from mask import D_create_hole, D_delete_mask, D_create_mask
from special_window_functions import blink, D_change_user_control_widgets_state
from tips import D_show_tip
from global_items import Unalive, smilies_data, distance_between_objects, new_pos, handle, plants, smilies, zombies, evolution_field, evolution_status
from zombies import create_zombie

import global_items

VISION_DISTANCE_LOSS_1680_1050 = PLANT_ENERGY*0.000012
SPEED_LOSS_1680_1050 = PLANT_ENERGY*0.002

def calculate_data_for_zombie_boss():
    global energy_for_vision_zombie_boss, energy_for_moving_zombie_boss
    d_1680_1050 = sqrt(1680**2+1050**2) # Diagonal of the evolution field with the screen resolution being 1680x1050
    ratio = evolution_field['diagonal']/d_1680_1050
    energy_for_vision_zombie_boss = VISION_DISTANCE_LOSS_1680_1050/ratio
    energy_for_moving_zombie_boss = SPEED_LOSS_1680_1050/ratio

class Boss(Unalive):
     def __init__(
        self,
        vision_distance: float,
        speed: float,
        health: float,
        x: float,
        y: float
        ):
        super().__init__(
            vision_distance=vision_distance,
            speed=speed, 
            health=health,
            x=x,
            y=y) 
        self.sleeping = False                        

@handle
def D_create_new_boss(speed, vision_distance, health, x, y): 
    evolution_status.zombie_boss = Boss(speed=speed, vision_distance=vision_distance, 
                            health=health, x=x, y=y)

def recreating_zombie_boss():
    '''Recreating the zombie boss when the secret button was clicked.'''
    D_create_new_boss(
        speed=smilies_data['average_speed'], 
        vision_distance=smilies_data['average_vision_distance'], 
        health=INITIAL_ENERGY, 
        x=evolution_field['width']/2,
        y=evolution_field['height']/2)
    D_change_user_control_widgets_state(NORMAL)
    D_create_mask(rerun=True)

def is_zombie_boss_okay() -> bool: # If the health of the zombie boss is okay, then True is returned; whereas if it is not okay, then it ceases living
    zombie_boss = evolution_status.zombie_boss
    if zombie_boss.health <= 0: # Checking if it is time to remove the zombie boss
        global_items.canvas.delete(zombie_boss.image_reference)
        add_cross(zombie_boss.x, zombie_boss.y)
        evolution_status.zombie_boss = None
        D_change_user_control_widgets_state(DISABLED)
        global_items.wonderful_game_button.pack(side=RIGHT, pady=8, padx=2)
        blink()
        D_show_tip(PAUSE_RESUME)
        D_delete_mask()
        return False
    return True   

ZOMBIE_BOSS_PLANT_GAP_TO_REACH = SMILEY_SIZE*0.9
ZOMBIE_BOSS_SMILEY_GAP_TO_REACH = SMILEY_SIZE*0.7
ZOMBIE_BOSS_PLANT_HEALTH_LOSS = 60

def zombie_boss_one_action():
    global energy_for_vision_zombie_boss, energy_for_moving_zombie_boss

    zombie_boss = evolution_status.zombie_boss
    D_create_hole()

    # Calculating health
    zombie_boss.health -= zombie_boss.vision_distance*energy_for_vision_zombie_boss
    canvas_mouse_x = global_items.canvas.winfo_pointerx() - global_items.canvas.winfo_rootx()
    canvas_mouse_y = global_items.canvas.winfo_pointery() - global_items.canvas.winfo_rooty()
    standing_put = dist(
        (canvas_mouse_x, canvas_mouse_y),
        (zombie_boss.x, zombie_boss.y)) <= HALF_SMILEY_SIZE*1.2
    if not standing_put:
        zombie_boss.health -= zombie_boss.speed*energy_for_moving_zombie_boss

    if not is_zombie_boss_okay():
        return
    
    if standing_put: # Doing nothing if the zombie boss is standing put
        return

    # Checking if it is time to do a Wrap
    new_x, new_y = new_pos(zombie_boss)
    if (new_x, new_y) != (zombie_boss.x, zombie_boss.y):
        zombie_boss.x, zombie_boss.y = new_x, new_y
        return
    
    # Moving the zombie boss
    dx, dy = canvas_mouse_x - zombie_boss.x, canvas_mouse_y - zombie_boss.y
    distance = dist((zombie_boss.x, zombie_boss.y), (canvas_mouse_x, canvas_mouse_y))
    coeff = zombie_boss.speed/distance
    zombie_boss.x, zombie_boss.y = zombie_boss.x + coeff*dx, zombie_boss.y + coeff*dy

    # Consuming plants
    to_remove = None
    for plant in plants:
        if distance_between_objects(zombie_boss, plant) <= ZOMBIE_BOSS_PLANT_GAP_TO_REACH:
            zombie_boss.health -= ZOMBIE_BOSS_PLANT_HEALTH_LOSS
            to_remove = plant # Evading 'RuntimeError: Set changed size during iteration'
            break
    if to_remove is not None:
        plants.remove(to_remove)
        is_zombie_boss_okay()
        return

    # Consuming smileys
    transfer_to_zombies = None
    for smiley in smilies:
        if distance_between_objects(zombie_boss, smiley) <= ZOMBIE_BOSS_SMILEY_GAP_TO_REACH:
            transfer_to_zombies = smiley
            min_health = min(smiley.energy, NEW_ZOMBIE_HEALTH)
            zombie_boss.health += smiley.energy - min_health
            break
    if transfer_to_zombies is not None:
        zombies.append(create_zombie(speed=transfer_to_zombies.speed,
                                 vision_distance=transfer_to_zombies.vision_distance, 
                                 health=min_health, 
                                 x=transfer_to_zombies.x,
                                 y=transfer_to_zombies.y))
        smilies.remove(transfer_to_zombies)