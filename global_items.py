from typing import Callable
from tkinter import TclError, Tk
from time import time
from sys import exit as sys_exit
from math import dist
from random import uniform, randrange

from config import *

import global_items

window_commands = {
    'run/pause': PAUSE,
    'to-show-selected-property': 'Nothing',
    'display-properties': True,
    'new-game': False
}

def delete_help(event=None):
    try:
        global_items.help_window.destroy()
    except (NameError, AttributeError):
        return

    del global_items.help_window

def center_window(window: object):
    '''Centering a window on the screen.'''
    window.update()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = round(screen_width/2 - window_width/2)
    y = round(screen_height/2 - window_height/2)
    window.geometry(f'+{x}+{y}')

last_updating_time = time()

class ExceptionToRestart(Exception):
    pass

class EvolutionStatus:
    def __init__(self):
        self.description = None
        self.survivor = None
        self.zombie_boss = None

def time_to_update() -> bool:
    '''Checking if it is time to update the window where the evolution takes place.'''
    global last_updating_time
    now = time()
    if now > last_updating_time + DELTA:
        last_updating_time = now
        return True
    return False

def handle(func: Callable) -> Callable:
    '''Maintaining calls of functions making sure it is not time to do anything except this function which can affect the program.'''
    def wrapper(*arg, **kwargs):
        try:
            window.winfo_exists()
            # TclError is thrown if the window has been closed with the exit button
        except TclError:
            sys_exit()

        if time_to_update():
            window.update()
            window_is_active_ = window_is_active(window)
            if not window_is_active_: # Deleting the help window when an alt+tab is accomplished
                delete_help()

            if global_items.mask_exists:
                # If the main window is active, whilst the mask window is not active, then the mask is shown
                if window_is_active_:
                    if not window_is_active(global_items.mask):
                        global_items.mask.deiconify()
                        global_items.mask.attributes('-topmost', True)
                else:
                    if global_items.mask.state() != 'withdrawn':
                        global_items.mask.withdraw()

        if window_commands['new-game']:
            window_commands['new-game'] = False
            raise ExceptionToRestart     
        try: # The window might be closed by these time this command is accomplished, so the actions with the window are impossible
            return func(*arg, **kwargs)
        except TclError:
            sys_exit()
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

def new_pos(body: object) -> tuple[float]:
    '''Checking if the body is on the edge of the evolution field and bearing it to the opposite edge if it is needed.'''
    x_new = body.x
    y_new = body.y

    evolution_field_width, evolution_field_height = evolution_field['width'], evolution_field['height']

    if body.x > evolution_field_width:
        x_new = HALF_BODY_SIZE
    elif body.x < 0:
        x_new = evolution_field_width-HALF_BODY_SIZE

    if body.y > evolution_field_height:
        y_new = HALF_BODY_SIZE
    elif body.y < 0:
        y_new = evolution_field_height-HALF_BODY_SIZE
        
    return x_new, y_new

def start_pause_request(event):
    window_commands['run/pause'] = PAUSE if window_commands['run/pause'] == RUN else RUN

def mouse_wheel(event):
    scale = global_items.user_selected_body_speed if global_items.active_scale == SPEED else global_items.user_selected_vision_distance
    current_value = scale.get()
    if event.delta > 0:
        scale.set(current_value+1)
    else:
        scale.set(current_value-1)

def set_scales_colors():    
    if global_items.active_scale == VISION_DISTANCE:
        global_items.user_selected_vision_distance.configure(bg='light yellow')
        global_items.user_selected_body_speed.configure(bg='SystemButtonFace')
    else:
        global_items.user_selected_vision_distance.configure(bg='SystemButtonFace')
        global_items.user_selected_body_speed.configure(bg='light yellow')  
    window.update()

def switch_scales(event):
    global_items.active_scale = VISION_DISTANCE if global_items.active_scale == SPEED else SPEED
    set_scales_colors()

window = Tk()
evolution_status = EvolutionStatus()
plants: set[object] = set()

bodies: list[object] = []
zombies: list[object] = []

progenitor_properties: dict[str, dict] = {}
evolution_field = {'width': 0, 'height': 0}

average_body_speed = average_body_vision_distance = 0
energy_for_vision = energy_for_moving = 0