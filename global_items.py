from typing import Callable
from tkinter import TclError, Tk
from time import time
from sys import exit as sys_exit
from math import dist
from random import uniform, randrange

from config import *

import global_items

# Classes
class ExceptionToRestart(Exception):
    pass

class EvolutionStatus:
    def __init__(self):
        self.description = None
        self.survivor = None
        self.zombie_boss = None
        self.result = None

class Collision:
    '''Data about a collision with a smiley or a plant'''
    def __init__(self):
        self.result = None # The amount of received/spent energy/health
        self.moment = float('-inf') # The time when the collision took place

class Creature: # For the smilies, normal zombies and the zombie boss
     def __init__(
        self,
        vision_distance: float,
        speed: float,
        x: float,
        y: float
    ):
        self.vision_distance = vision_distance
        self.speed = speed
        self.x, self.y = x, y
        self.collision = Collision()

class CreatureStatus:
    def __init__(self):
        self.description = None
        self.parameter = None

class Unalive(Creature): # For normal zombies and the zombie boss
    def __init__(
        self,
        vision_distance: float,
        speed: float,
        health: float,
        x: float,
        y: float
        ):
        super().__init__(vision_distance=vision_distance, speed=speed, x=x, y=y)
        self.health = health
        self.species = (0, 0, 0) # Black colour

# Variables
window_commands = {
    'run/pause': PAUSE,
    'to-show-selected-property': 'Nothing',
    'display-properties': True,
    'new-game': False
}
window = Tk()
evolution_status = EvolutionStatus()
plants: set[object] = set()
smilies: list[object] = []
zombies: list[object] = []
evolution_field = {}
smilies_data ={}
scales = {}
boss_shape_size = {}
zombie_shape_size = {}

# Functions
def delete_help_window(event=None):
    try:
        global_items.help_window.destroy()
    except (NameError, AttributeError): # The help window may not exist yet
        return
    del global_items.help_window

DELTA = 0.1 # Window update every DELTA seconds
last_updating_time = time()

def time_to_update() -> bool:
    '''Checking if it is time to update the window where the evolution takes place.'''
    global last_updating_time
    now = time()
    if now > last_updating_time + DELTA:
        last_updating_time = now
        return True
    return False

def handle(func: Callable) -> Callable:
    '''Maintaining calls of functions making sure it is not time to do anything except this function which can affect the program. All of the functions which are decorated with this function have their names starting with "D_"'''
    def wrapper(*arg, **kwargs):
        try:
            window.winfo_exists() # Making sure the window hasn't been closed with the exit button
            
            if time_to_update():
                window.update()
                window_is_active_ = window_is_active(window)
                if not window_is_active_: # Deleting the help window when an alt+tab is accomplished
                    delete_help_window()
                if global_items.mask_exists:
                    # If the main window is active, whilst the mask window is not active, then the mask is shown
                    if window_is_active_:
                        if not window_is_active(global_items.mask):
                            global_items.mask.deiconify()
                            global_items.mask.attributes('-topmost', True)
                    else:
                        if global_items.mask.state() != 'withdrawn':
                            global_items.mask.withdraw()
                
            if window_commands['new-game']: # Implementing the transition to the new game
                window_commands['new-game'] = False
                raise ExceptionToRestart

            return func(*arg, **kwargs)

        except TclError: # TclError is thrown if the window has been closed with the exit button
            sys_exit() # Finishing the current evolution thread
    return wrapper

def window_is_active(window: object) -> bool:
    bottom_right_corner_x = window.winfo_rootx() + window.winfo_width() - 1
    bottom_right_corner_y = window.winfo_rooty() + window.winfo_height() - 1
    return window.winfo_containing(bottom_right_corner_x, bottom_right_corner_y) is not None

def distance_between_objects(object1: object, object2: object) -> float:
    return dist((object1.x, object1.y),
                (object2.x, object2.y))

def random_attribute(attribute, deviation: float) -> float:
    return uniform(attribute-deviation*attribute, attribute+deviation*attribute)

def random_place(shape_size: int) -> tuple[int, int]:
    max_horizontal = evolution_field['width'] - shape_size
    max_vertical = evolution_field['height'] - shape_size
    return randrange(shape_size, max_horizontal), randrange(shape_size, max_vertical)

def new_pos(creature: object) -> tuple[float]:
    '''Checking if the creature is on the edge of the evolution field and bearing it to the opposite edge if it is needed.'''
    x_new = creature.x
    y_new = creature.y

    evolution_field_width, evolution_field_height = evolution_field['width'], evolution_field['height']

    if creature.x > evolution_field_width:
        x_new = HALF_SMILEY_SIZE
    elif creature.x < 0:
        x_new = evolution_field_width-HALF_SMILEY_SIZE

    if creature.y > evolution_field_height:
        y_new = HALF_SMILEY_SIZE
    elif creature.y < 0:
        y_new = evolution_field_height-HALF_SMILEY_SIZE
        
    return x_new, y_new