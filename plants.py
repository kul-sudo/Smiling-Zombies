from tkinter import PhotoImage
from random import random

from config import *
from images import PLANT_IMAGE
from zombies import zombies
from global_items import random_place, distance_between_objects, handle, plants, smilies, evolution_status

import global_items


def create_plant_image():
    PLANT_SIZE_RATIO = 25 # Higher => smaller
    # Equalizing the size a smiley and the size of a plant
    global plant_size, double_plant_size, double_plant_size_plus_smiley_size
    global_items.plant_shape = PhotoImage(data=PLANT_IMAGE).subsample(PLANT_SIZE_RATIO, PLANT_SIZE_RATIO) # Registering a new shape with the plant_base64
    plant_size = max(global_items.plant_shape.width(), global_items.plant_shape.height())
    double_plant_size = plant_size*2
    double_plant_size_plus_smiley_size = double_plant_size+SMILEY_SIZE
    global_items.half_plant_size = plant_size/2
    global_items.half_image_size = max(HALF_SMILEY_SIZE, global_items.half_plant_size)

TIMES_ATTEMPTED = 200 # Limit of times for trying to place a plant on the window    

class Plant: # Food for the smilies which is not able to move
    def __init__(self):
        self.image_reference = None
        # Situating plant_pattern to a random place so that it does not overlap other plants or other boies. If the spot is not found in TIMES_ATTEMPTED times, then stop placing the plants
        for _ in range(TIMES_ATTEMPTED):
            self.x, self.y = random_place(plant_size)
            zombie_boss = evolution_status.zombie_boss
            if zombie_boss is not None:
                if distance_between_objects(self, zombie_boss) < double_plant_size_plus_smiley_size:
                    continue # Repeat if plant_pattern does overlap the zombie boss, otherwise go ahead
            if any(distance_between_objects(self, creature) < double_plant_size_plus_smiley_size for creature in smilies+zombies): # Check if the Plant is not that close to either of the creatures
                continue # Repeat if plant_pattern does overlap another creature, otherwise go ahead
            if plants != set():
                if any(distance_between_objects(self, plant) < double_plant_size for plant in plants):
                    continue # Repeat if plant_pattern does overlap another plant, otherwise go ahead
            break # If the condition is satisfied, the good place for placing the plant is found. So, we can obviously finish the while-loop
    
@handle
def D_create_plant(chance: float | float):
    if random() < chance: # Putting a plant with a chance determined in PLANT_CHANCE
        plants.add(Plant())

def create_initial_plants():
    for _ in range(INITIALLY_PLANTED): # Initial plant placing
        D_create_plant(chance=1)

@handle
def D_delete_all_plants():
    plants.clear()