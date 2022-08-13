from time import time
from tkinter import LAST, S, N, E

from config import *
from zombies_images import *
from crosses import crosses_list
from global_items import zombies, distance_between_objects, handle, smilies, plants, window_commands, evolution_status, boss_shape_size, zombie_shape_size
import global_items

# Plants
drawn_plants: set[object] = set()

def update_plant_images():
    '''Erasing all of the plants that are due to be erased and drawing new ones.'''
    global drawn_plants

    for plant in drawn_plants - plants:
        global_items.canvas.delete(plant.image_reference)

    for plant in plants - drawn_plants:
        plant.image_reference = global_items.canvas.create_image(
            plant.x,
            plant.y,
            image=global_items.plant_shape,
            tags='plant'
        )

    drawn_plants = plants.copy()

# Crosses
drawn_crosses: set[object] = set()

def update_cross_images():
    '''Erasing all of the crosses that are due to be erased and drawing new ones.'''
    global drawn_crosses

    crosses_set: set[object] = set(crosses_list) # Creating a separate set for it to be handy to subtract a set from a set. Set of crosses that are due on the evolution field

    for cross in drawn_crosses - crosses_set:
        global_items.canvas.delete(cross.image_reference)

    for cross in crosses_set - drawn_crosses:
        cross.image_reference = global_items.canvas.create_image(
            cross.x,
            cross.y,
            image=global_items.cross_shape,
            tags='cross'
        )
    drawn_crosses = crosses_set.copy()

# Arrows
def append_arrow(creature: object):
    prey = creature.status.parameter
    prey_is_smiley = creature.status.description == FOLLOWING_SMILEY
    dist = distance_between_objects(creature, prey)

    min_distance = SMILEY_SIZE if prey_is_smiley else global_items.half_plant_size
    if dist < min_distance: # At short distances, the arrow looks bad; sometimes it is even reversed
        return

    sine = (prey.y - creature.y)/dist
    cosine = (prey.x - creature.x)/dist
    arrow_start_x = creature.x + HALF_SMILEY_SIZE*cosine
    arrow_start_y = creature.y + HALF_SMILEY_SIZE*sine
    if prey_is_smiley: # Smiley case: the arrow goes into the edge of the image
        arrow_end_x = prey.x - HALF_SMILEY_SIZE*cosine
        arrow_end_y = prey.y - HALF_SMILEY_SIZE*sine
    else: # Plant case: the arrow goes into the center of the image
        arrow_end_x = prey.x
        arrow_end_y = prey.y
    global_items.canvas.create_line(
        arrow_start_x, arrow_start_y,
        arrow_end_x, arrow_end_y,
        arrow=LAST, arrowshape=(5, 5, 5), tags='arrow', dash=(4, 1))

def update_arrows():
    global_items.canvas.delete('arrow')
    for creature in smilies+zombies:
        if creature.status.description in (FOLLOWING_SMILEY, FOLLOWING_PLANT):
            append_arrow(creature)

# Vision distance circle
def draw_one_vision_distance_circle(creature: object):
    center_x, center_y = creature.x, creature.y
    radius = creature.vision_distance-global_items.half_image_size # If only a half is visible, the item is still considered to be within the vision distance
    global_items.canvas.create_oval(
        center_x-radius, center_y-radius,
        center_x+radius, center_y+radius,
        outline='#%02x%02x%02x' % creature.species,
        tags='circle'
    )

# Properties displaying
def display_property(creature: object, text: str, exceeding_y=0):
    '''Writing properties of creatures over them.'''
    center_x, center_y = creature.x, creature.y
    global_items.canvas.create_text(
        center_x, center_y-exceeding_y,
        text=text,
        tags='property',
        anchor=S
    )

def display_collision_result(creature: object, decrease_x: int | float):
    '''Displaying stuff related to the collision.'''
    number = round(creature.collision.result)
    sign = '+' if number >= 0 else '–'
    text = f'{sign}{abs(number)}'
    global_items.canvas.create_text(
        creature.x-decrease_x-2, creature.y,
        text=text,
        tags='property',
        anchor=E,
        fill='blue' if sign == '+' else 'red' 
    )

NONE = 'None'
NEWLY_BORN_PERIOD = 4 # In seconds
COLLISION_RESULTS_DISPLAY_PERIOD = 1 # How long the stuff related to the collision shall be displaed

@handle
def D_handle_properties():
    # Handling the properties displayed over creatures
    global_items.canvas.delete('property')
    global_items.canvas.delete('circle')

    now = time()

    for smiley in smilies:
        match window_commands['to-show-selected-property']:  
            case 'Energy/health':
                display_property(creature=smiley, text=round(smiley.energy), exceeding_y=HALF_SMILEY_SIZE)
                if now < smiley.collision.moment + COLLISION_RESULTS_DISPLAY_PERIOD:
                    display_collision_result(smiley, HALF_SMILEY_SIZE)
            case 'Speed':
                display_property(creature=smiley, text=round(smiley.speed*SPEED_RATIO), exceeding_y=HALF_SMILEY_SIZE)
            case '"Newly born" if newly born':
                display_property(creature=smiley, text='Newly born' if now <= smiley.birth_time + NEWLY_BORN_PERIOD and smiley.generation_n != 0 else '', exceeding_y=HALF_SMILEY_SIZE)
            case 'Procreation threshold':
                display_property(creature=smiley, text=round(smiley.procreation_threshold), exceeding_y=HALF_SMILEY_SIZE)
            case 'Food preference':
                display_property(creature=smiley, text=smiley.food_preference, exceeding_y=HALF_SMILEY_SIZE)
            case 'Generation number':
                display_property(creature=smiley, text=smiley.generation_n, exceeding_y=HALF_SMILEY_SIZE)
            case 'Amount of smilies with this species':
                display_property(creature=smiley, text=len(tuple(filter(lambda smiley_: smiley_.species == smiley.species, smilies))), exceeding_y=HALF_SMILEY_SIZE)
            case 'ID of the species':
                display_property(creature=smiley, text=smiley.species_id, exceeding_y=HALF_SMILEY_SIZE)
            case 'Vision distance':
                draw_one_vision_distance_circle(creature=smiley)

    # Writing for the zombie boss
    zombie_boss = evolution_status.zombie_boss
    if zombie_boss is not None:
        global_items.boss_health.set(f'Health:\n{round(zombie_boss.health)}')
        match window_commands['to-show-selected-property']:
            case 'Nothing':
                display_property(creature=zombie_boss, text='')
            case 'Vision distance':
                if not global_items.mask_exists:
                    draw_one_vision_distance_circle(creature=zombie_boss)
            case 'Energy/health':
                display_property(creature=zombie_boss, text=round(zombie_boss.health), exceeding_y=boss_shape_size['half_height']) 
                if now < zombie_boss.collision.moment + COLLISION_RESULTS_DISPLAY_PERIOD:
                    display_collision_result(zombie_boss, boss_shape_size['half_width'])
            case 'Speed':
                display_property(creature=zombie_boss, text=round(zombie_boss.speed*SPEED_RATIO), exceeding_y=boss_shape_size['half_height'])
            case _:
                display_property(creature=zombie_boss, text=NONE, exceeding_y=boss_shape_size['half_height'])
    
    # Writing for zombies
    for zombie in zombies:
        match window_commands['to-show-selected-property']:
            case 'Nothing':
                continue
            case 'Energy/health':
                display_property(creature=zombie, text=round(zombie.health), exceeding_y=zombie_shape_size['half_height'])
                if now < zombie.collision.moment + COLLISION_RESULTS_DISPLAY_PERIOD:
                    display_collision_result(zombie, zombie_shape_size['half_width'])
            case 'Speed':
                display_property(creature=zombie, text=round(zombie.speed*SPEED_RATIO), exceeding_y=zombie_shape_size['half_height'])
            case 'Vision distance':
                draw_one_vision_distance_circle(creature=zombie)
            case _:
                display_property(creature=zombie, text=NONE, exceeding_y=zombie_shape_size['half_height'])

# Stimulus
STIMULUS_DELAY: int = 15 # Displaying the stimulus toward the zombie boss in STIMULUS_DELAY seconds of inaction

def set_stimulus_start_time():
    # The stimulus is only displayed above the smilies which recently started sleeping
    for smiley in smilies:
        smiley.stimulus_start = float('-inf')

def display_stimulus(): # This function is called every second
    '''Displaying the stimulus toward the zombie boss when it is time to do it.'''
    global lazy_time # How long the zombie boss has been inactive
    if evolution_status.description == EVOLUTION and not global_items.mask_exists:
        lazy_time += 1
        if lazy_time == STIMULUS_DELAY:
            zombie_boss = evolution_status.zombie_boss
            if zombie_boss is not None:
                global_items.canvas.create_text(
                    zombie_boss.x, zombie_boss.y+boss_shape_size['half_height'],
                    text='Lazy lounger!',
                    tags='stimulus',
                    anchor=N)
                global_items.stimulus_on = True        
    global_items.canvas_after_id = global_items.canvas.after(1000, display_stimulus)

def erase_stimulus():
    '''Erasing the stimuli.'''
    if global_items.mask_exists:
        global_items.canvas.delete('stimulus')
        global_items.stimulus_on = False
        init_stimulus_time()

def init_stimulus_time():
    '''Whenever the zombie boss does not do anything for a certain amount of time, it is needed to initialise the lazy_time variable.'''
    global lazy_time
    lazy_time = 0