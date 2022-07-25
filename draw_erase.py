from time import time
from typing import Callable
from tkinter import LAST, S, N

from config import *
from crosses import crosses_list
from global_items import zombies, distance_between_objects, handle, bodies, plants, window_commands, evolution_status
from draw_creatures import draw_smiley, draw_zombie_boss, draw_zombie
import global_items

def create_body_shape(body: object, shape: Callable) -> int:
    if STRAIGHTFORWARD_FIX:
        if shape == global_items.canvas.create_rectangle:
            return draw_smiley(body)
        else:
            return draw_zombie_boss()
    else:    
        center_x, center_y = body.x, body.y
        return shape(
            center_x - HALF_BODY_SIZE,
            center_y - HALF_BODY_SIZE,
            center_x + HALF_BODY_SIZE,
            center_y + HALF_BODY_SIZE,
            fill='#%02x%02x%02x' % body.species,
            width=0,
            tags='body'
        )

# Bodies
def update_body_images():
    '''Erasing all of the bodies that have already been drawn and drawing new ones.'''
    global_items.canvas.delete('body')
    for body in bodies:
        body.image_reference = create_body_shape(body, global_items.canvas.create_rectangle)

# Zombies
def update_zombie_boss_image():
    zombie_boss = evolution_status.zombie_boss
    global_items.canvas.delete(zombie_boss.image_reference)
    zombie_boss.image_reference = create_body_shape(zombie_boss, global_items.canvas.create_oval)

def update_zombie_images():
    '''Erasing all of the zombies that have already been drawn and drawing new ones.'''
    global_items.canvas.delete('zombie')
    for zombie in zombies:
        zombie.image_reference = draw_body_rhombus(zombie)

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
    prey_is_body = creature.status.description == FOLLOWING_BODY
    dist = distance_between_objects(creature, prey)

    min_distance = HALF_BODY_SIZE if prey_is_body else global_items.half_plant_size
    
    if dist < min_distance:
        return
    sine = (prey.y - creature.y)/dist
    cosine = (prey.x - creature.x)/dist
    arrow_start_x = creature.x + HALF_BODY_SIZE*cosine
    arrow_start_y = creature.y + HALF_BODY_SIZE*sine
    if STRAIGHTFORWARD_FIX:
        if prey_is_body:
            min_distance = BODY_SIZE
            if dist < min_distance:
                return 
            arrow_end_x = prey.x - HALF_BODY_SIZE*cosine
            arrow_end_y = prey.y - HALF_BODY_SIZE*sine
        else:
            arrow_end_x = prey.x
            arrow_end_y = prey.y
        global_items.canvas.create_line(
        arrow_start_x, arrow_start_y,
        arrow_end_x, arrow_end_y,
        arrow=LAST, arrowshape=(5, 5, 5), tags='arrow', dash=(4, 1))
    else:        
        global_items.canvas.create_line(
            arrow_start_x, arrow_start_y,
            prey.x, prey.y,
            arrow=LAST, arrowshape=(5, 5, 5), tags='arrow', dash=(4, 1))

def update_arrows():
    global_items.canvas.delete('arrow')
    for creature in bodies+zombies:
        if creature.status.description in (FOLLOWING_BODY, FOLLOWING_PLANT):
            append_arrow(creature)

def draw_rhombus(x: float, y: float, color: tuple):
    return global_items.canvas.create_polygon(
        x, y+HALF_RHOMBUS_SIZE, x+HALF_RHOMBUS_SIZE, y,
        x, y-HALF_RHOMBUS_SIZE, x-HALF_RHOMBUS_SIZE, y, 
        fill='#%02x%02x%02x' % color,
        tags='zombie')

def draw_body_rhombus(body: object):
    if STRAIGHTFORWARD_FIX:
        return draw_zombie(body)
    else:    
        return draw_rhombus(body.x, body.y, body.species)

def from_circle_to_initial_shape(body: object):
    '''This function is solely used when it is needed to turn the shape of a circle-shaped body into the initial shape of this body.'''
    if body.initial_shape == SQUARE:
        body.image_reference = create_body_shape(body, global_items.canvas.create_rectangle)
    else:
        body.image_reference = draw_body_rhombus(body)
    body.shape = body.initial_shape    

def change_shape_to_circle(body: object):
    '''Making the body circle-shaped.'''
    global_items.canvas.delete(body.image_reference)
    body.shape = CIRCLE
    body.image_reference = create_body_shape(body, global_items.canvas.create_oval)     

def restore_user_selected_body_shape():
    '''Restoring the initial shape of the zombie boss.'''
    for body in bodies:
        if body.shape == CIRCLE:
            global_items.canvas.delete(body.image_reference)    
            from_circle_to_initial_shape(body)

def restore_user_selected_body_speed():
    for body in bodies:
        if body.shape == CIRCLE:
            body.speed = body.initial_speed

def restore_user_selected_body_vision_distance():
    for body in bodies:
        if body.shape == CIRCLE:
            body.vision_distance = body.initial_vision_distance

# Vision distance circle
def draw_one_vision_distance_circle(creature: object):
    center_x, center_y = creature.x, creature.y
    radius = creature.vision_distance-global_items.half_image_size
    global_items.canvas.create_oval(
        center_x-radius, center_y-radius,
        center_x+radius, center_y+radius,
        outline='#%02x%02x%02x' % creature.species,
        tags='circle'
    )

def erase_circles():
    global_items.canvas.delete('circle')

# Writing properties of bodies over them
def display_property(creature: object, text: str):
    center_x, center_y = creature.x, creature.y
    global_items.canvas.create_text(
        center_x, center_y-HALF_BODY_SIZE,
        text=text,
        tags='property',
        anchor=S
    )    

@handle
def handle_properties():
    erase_properties_of_creatures()
    erase_circles()
    for body in bodies:
        # Writing for the normal bodies
        match window_commands['to-show-selected-property']:  
            case 'Energy/health':
                display_property(creature=body, text=round(body.energy))
            case 'Speed':
                display_property(creature=body, text=round(body.speed*RATIO))
            case '"Newly born" if newly born':
                display_property(creature=body, text='Newly born' if time() <= body.birth_time + NEWLY_BORN_PERIOD and body.generation_n != 0 else '')
            case 'Procreation threshold':
                display_property(creature=body, text=round(body.procreation_threshold))
            case 'Food preference':
                display_property(creature=body, text=body.food_preference)
            case 'Generation number':
                display_property(creature=body, text=body.generation_n)
            case 'Amount of bodies with this species':
                display_property(creature=body, text=len(tuple(filter(lambda body_: body_.species == body.species, bodies))))
            case 'ID of the species':
                display_property(creature=body, text=body.species_id)
            case 'Vision distance':
                draw_one_vision_distance_circle(creature=body)

    # Writing for the zombie boss
    zombie_boss = evolution_status.zombie_boss
    if zombie_boss is not None:
        global_items.health_to_display.set(f'Health:\n{round(zombie_boss.health)}')
        
        match window_commands['to-show-selected-property']:
            case 'Vision distance':
                if not global_items.mask_exists:
                    draw_one_vision_distance_circle(creature=zombie_boss)  
            case 'Energy/health':
                display_property(creature=zombie_boss, text=round(zombie_boss.health)) 
            case 'Speed':
                display_property(creature=zombie_boss, text=round(zombie_boss.speed*RATIO))          

    # Writing for zombies
    NONE = 'None'
    for zombie in zombies:
        # Writing for the normal bodies
        match window_commands['to-show-selected-property']:
            case 'Nothing':
                continue
            case 'Energy/health':
                display_property(creature=zombie, text=round(zombie.health))
            case 'Speed':
                display_property(creature=zombie, text=round(zombie.speed*RATIO))
            case 'Vision distance':
                draw_one_vision_distance_circle(creature=zombie)
            case _:
                display_property(creature=zombie, text=NONE)

def erase_properties_of_creatures():
    global_items.canvas.delete('property')

STIMULUS_DELAY: int = 25 # Displaying the stimulus toward the zombie boss in STIMULUS_DELAY seconds of inaction

def display_stimulus(): # This function is called every second
    '''Displaying the stimulus toward the zombie boss when it is time to do it.'''
    global lazy_time # How long the zombie boss has been inactive
    if evolution_status.description == EVOLUTION and not global_items.mask_exists:
        lazy_time += 1
        if lazy_time == STIMULUS_DELAY:
            zombie_boss = evolution_status.zombie_boss
            if zombie_boss is not None:
                global_items.canvas.create_text(
                    zombie_boss.x, zombie_boss.y+global_items.zombie_boss_height/2,
                    text='Lazy lounger!',
                    tags='stimulus',
                    anchor=N)
                global_items.stimulus_on = True        
    global_items.canvas_after_id = global_items.canvas.after(1000, display_stimulus)

def stimulus_off():
    '''Erasing the stimuli.'''
    if global_items.mask_exists:
        global_items.canvas.delete('stimulus')
        global_items.stimulus_on = False
        init_stimulus_time()

def init_stimulus_time():
    '''Whenever the zombie boss does not do anything for a certain amount of time, it is needed to initialise the lazy_time variable.'''
    global lazy_time
    lazy_time = 0