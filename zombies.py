from time import time

from config import *
from crosses import add_cross
from global_items import CreatureStatus, Unalive, distance_between_objects, handle, plants, smilies, zombies

import global_items

class Zombie(Unalive):
    def __init__(
        self,
        vision_distance: float,
        speed: float,
        health: float,
        x: float,
        y: float
        ):
        super().__init__(vision_distance=vision_distance, speed=speed, health=health,
                                 x=x, y=y)
        self.status=CreatureStatus()

def create_zombie(speed, vision_distance, health, x, y):
    new_zombie = Zombie(vision_distance=vision_distance, speed=speed,
                            health=health, x=x, y=y)
    new_zombie.status.description = SLEEPING
    return new_zombie

@handle
def D_delete_all_zombies():
    zombies.clear()

ZOMBIE_PLANT_HEALTH_LOSS = 30

def zombie_one_action(zombie: object):
    '''Maintaining the behaviour of the zombie.'''
    
    # If the zombie reaches the plant, then the plant is consumed with a negative effect on the health
    to_remove = None
    for plant in plants:
        if distance_between_objects(zombie, plant) <= global_items.half_plant_size:   
            zombie.health -= ZOMBIE_PLANT_HEALTH_LOSS

            # Storing the data about the collision with a plant
            zombie.collision.result = -ZOMBIE_PLANT_HEALTH_LOSS
            zombie.collision.moment = time()

            to_remove = plant # Evading 'RuntimeError: Set changed size during iteration'
            break
    if to_remove is not None:
        plants.remove(to_remove)

        # Checking whether it is time for the zombie to die or not
        if round(zombie.health) <= 0:    
            add_cross(zombie.x, zombie.y)
            zombies.remove(zombie)
        return
    
    # Find a satisfactory smiley to chase for the zombie
    visible_smilies = tuple(filter(lambda smiley: zombie.vision_distance >= distance_between_objects(zombie, smiley), smilies))
    closest_smiley = min(visible_smilies, key=lambda smiley: distance_between_objects(zombie, smiley), default=None)
    
    if closest_smiley is None:
        zombie.status.description = SLEEPING
        return
    else:
        zombie.status.description = FOLLOWING_SMILEY
        zombie.status.parameter = closest_smiley
        
    # If the zombie chased a smiley and caught it, then the prey also becomes a zombie
    prey = zombie.status.parameter
    if prey not in smilies: # The smiley could have ceased living by this moment
        zombie.status.description = SLEEPING
        return
    dx, dy = prey.x - zombie.x, prey.y - zombie.y
    distance = distance_between_objects(zombie, prey)
    coeff = zombie.speed/distance
    zombie.x, zombie.y = zombie.x + coeff*dx, zombie.y + coeff*dy # Moving the zombie toward the prey
    if distance_between_objects(zombie, prey) <= zombie.speed:
        min_health = min(prey.energy, NEW_ZOMBIE_HEALTH)

        # Storing the data about the collision with a smiley
        extra_health = prey.energy - min_health
        zombie.health += extra_health
        zombie.collision.result = extra_health
        zombie.collision.moment = time()

        zombies.append(create_zombie(
            speed=prey.speed,
            vision_distance=prey.vision_distance, 
            health=min_health, 
            x=prey.x+PLACEMENT_GAP,
            y=prey.y+PLACEMENT_GAP))
        smilies.remove(prey)
        zombie.status.description = SLEEPING