from tkinter import PhotoImage
from random import random

from config import *
from images import PLANT_IMAGE
from zombies import zombies
from global_items import random_place, distance_between_objects, handle, plants, bodies, evolution_status

import global_items

def create_plant_image():
    global_items.plant_shape = PhotoImage(data=PLANT_IMAGE).subsample(PLANT_SIZE_RATIO, PLANT_SIZE_RATIO) # Registering a new shape with the plant_base64
    global_items.plant_size = max(global_items.plant_shape.width(), global_items.plant_shape.height())
    
    global_items.half_plant_size = global_items.plant_size/2
    global_items.half_image_size = max(HALF_BODY_SIZE, global_items.half_plant_size)
    
class Plant: # Food for the Bodies which is not able to move
    def __init__(self):
        self.image_reference = None
        # Situating plant_pattern to a random place so that it does not overlap other plants or other boies. If the spot is not found in TIMES_ATTEMPTED times, then stop placing the plants
        double_plant_size = global_items.plant_size*2
        double_plant_size_plus_body_size = double_plant_size+BODY_SIZE
        for _ in range(TIMES_ATTEMPTED):
            self.x, self.y = random_place(global_items.plant_size)
            zombie_boss = evolution_status.zombie_boss
            if zombie_boss is not None:
                if distance_between_objects(self, zombie_boss) < double_plant_size_plus_body_size:
                
                    continue # Repeat if plant_pattern does overlap the zombie boss, otherwise go ahead
            if any(distance_between_objects(self, creature) < double_plant_size_plus_body_size for creature in bodies+zombies): # Check if the Plant is not that close to either of the Bodies
                continue # Repeat if plant_pattern does overlap another body, otherwise go ahead

            if plants != set():
                if any(distance_between_objects(self, plant) < double_plant_size for plant in plants):
                    continue # Repeat if plant_pattern does overlap another plant, otherwise go ahead

            break # If the condition is satisfied, the good place for placing the plant is found. So, we can obviously finish the while-loop
    
@handle
def create_plant(chance: float | float):
    if random() < chance: # Putting a plant with a chance determined in PLANT_CHANCE
        plants.add(Plant())

@handle
def create_initial_plants():
    for _ in range(INITIALLY_PLANTED): # Initial plant placing
        create_plant(chance=1)

@handle
def delete_all_plants():
    plants.clear()