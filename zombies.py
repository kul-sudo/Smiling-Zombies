from math import dist
from tkinter import DISABLED, RIGHT

from config import *
from crosses import add_cross
from mask import create_hole, delete_mask
from window_functions import blink, change_user_control_widgets_state
from tips import show_tip
from global_items import distance_between_objects, new_pos, handle, plants, bodies, zombies, evolution_field, evolution_status

import global_items

def calculate_data_for_zombie_boss():
    global energy_for_vision_zombie_boss, energy_for_moving_zombie_boss

    d_1680_1050 = sqrt(1680**2+1050**2) # Diagonal of the evolution field with the screen resolution being 1680x1050
    d = sqrt(evolution_field['width']**2+evolution_field['height']**2)
    ratio = d/d_1680_1050
    energy_for_vision_zombie_boss = VISION_DISTANCE_LOSS_1680_1050/ratio
    energy_for_moving_zombie_boss = SPEED_LOSS_1680_1050/ratio

@handle
def delete_all_zombies():
    zombies.clear()

def zombie_boss_off() -> bool:
    zombie_boss = evolution_status.zombie_boss
    if zombie_boss.health <= 0: # Checking if it is time to remove the zombie boss
        # global_items.canvas.delete(zombie_boss.image_reference)
        add_cross(zombie_boss.x, zombie_boss.y)
        evolution_status.zombie_boss = None
        change_user_control_widgets_state(DISABLED)
        global_items.wonderful_game_button.pack(side=RIGHT, pady=8, padx=2)
        blink()
        show_tip(PAUSE_RESUME)
        delete_mask()
        return True
    return False    

@handle
def zombie_boss_one_action():
    global energy_for_vision_zombie_boss, energy_for_moving_zombie_boss

    zombie_boss = evolution_status.zombie_boss
    create_hole(zombie_boss)

    # Calculating health
    zombie_boss.health -= zombie_boss.vision_distance*energy_for_vision_zombie_boss
    canvas_mouse_x = global_items.canvas.winfo_pointerx() - global_items.canvas.winfo_rootx()
    canvas_mouse_y = global_items.canvas.winfo_pointery() - global_items.canvas.winfo_rooty()
    standing_put = dist(
        (canvas_mouse_x, canvas_mouse_y),
        (zombie_boss.x, zombie_boss.y)) <= HALF_BODY_SIZE*1.2
    if not standing_put:
        zombie_boss.health -= zombie_boss.speed*energy_for_moving_zombie_boss

    if zombie_boss_off():
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
        if distance_between_objects(zombie_boss, plant) <= USER_BODY_PLANT_GAP:
            zombie_boss.health -= BOSS_PLANT_HEALTH_LOSS
            to_remove = plant # Evading 'RuntimeError: Set changed size during iteration'
            break
    if to_remove is not None:
        plants.remove(to_remove)
        zombie_boss_off()
        return

    # Consuming bodies
    transfer_to_zombies = None
    for body in bodies:
        if distance_between_objects(zombie_boss, body) <= USER_BODY_BODY_GAP:
            transfer_to_zombies = body
            min_health = min(body.energy, NEW_ZOMBIE_HEALTH)
            body.health = min_health
            body.species = (0, 0, 0)

            zombie_boss.health += body.energy - min_health
            break
    if transfer_to_zombies is not None:
        bodies.remove(transfer_to_zombies)
        zombies.append(transfer_to_zombies)
        transfer_to_zombies.status.description = SLEEPING

@handle
def zombie_one_action(zombie: object):
    '''Maintaining the behaviour of the zombie.'''
    
    # If the zombie reaches the plant, then the plant is consumed with a negative effect on the health
    to_remove = None
    for plant in plants:
        if distance_between_objects(zombie, plant) <= global_items.half_plant_size:   
            zombie.health -= ZOMBIE_PLANT_HEALTH_LOSS
            to_remove = plant # Evading 'RuntimeError: Set changed size during iteration'
            break
    if to_remove is not None:
        plants.remove(to_remove)

        # Checking whether it is time for body to die or not
        if zombie.health <= 0:
            add_cross(zombie.x, zombie.y)
            zombies.remove(zombie)
        return
    
    # Find a satisfactory body to chase for the zombie
    visible_bodies = tuple(filter(lambda body: zombie.vision_distance >= distance_between_objects(zombie, body), bodies))
    closest_body = min(visible_bodies, key=lambda body: distance_between_objects(zombie, body), default=None)
    
    if closest_body is None:
        zombie.status.description = SLEEPING
        return
    else:
        zombie.status.description = FOLLOWING_BODY
        zombie.status.parameter = closest_body
        
    # If the zombie chased a body and caught it, then the prey also becomes a zombie
    prey = zombie.status.parameter
    if prey not in bodies:
        zombie.status.description = SLEEPING
        return
    dx, dy = prey.x - zombie.x, prey.y - zombie.y
    distance = distance_between_objects(zombie, prey)
    coeff = zombie.speed/distance
    zombie.x, zombie.y = zombie.x + coeff*dx, zombie.y + coeff*dy
    if distance_between_objects(zombie, prey) <= zombie.speed:
        prey.species = (0, 0, 0)
        min_health = min(prey.energy, NEW_ZOMBIE_HEALTH)
        prey.health = min_health
        zombie.health += prey.energy - min_health
        bodies.remove(prey)
        zombies.append(prey)
        prey.status.description = SLEEPING
        zombie.status.description = SLEEPING
        prey.y += PLACEMENT_GAP