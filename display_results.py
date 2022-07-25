from tkinter.messagebox import showinfo
from statistics import fmean

from config import *
from global_items import handle, bodies
from mask import delete_mask
from tips import show_tip

import global_items, config

@handle
def find_average_from_bodies():
    bodies_amount = len(bodies)
    bodies_zero = bodies[0]
    bodies_zero_element_shape = bodies_zero.shape
    write_text_eventual = ''

    averaged = {
        'generation_n': round(fmean(body.generation_n for body in bodies)),
        'plant_preference': round(fmean(1 if body.food_preference == PLANT else 0 for body in bodies)), # Percent of bodies preferring plants
        'vision_distance': round(fmean(body.vision_distance for body in bodies)),
        'average_body_speed': round(fmean(body.speed for body in bodies)*RATIO),
        'procreation_threshold': round(fmean(body.procreation_threshold for body in bodies)),
        'energy': round(fmean(body.energy for body in bodies)),
        'descendants left': bodies_amount,
    }

    averaged_analysis = {}

    one_species_survived_line = 'One of the species has survived'
    average_generation_number = f'The average generation number of the bodies of the survived species: {averaged["generation_n"]}'
    
    user_predicted_line = 'You won' if bodies_zero_element_shape == CIRCLE else ''

    def ending() -> str: # Handling the 's' at the end of the word 'descendant'
        return f"{bodies_amount} descendant{'s' if bodies_amount > 1 else ''} left"

    descendants_left_line = ending()

    initial_values = {
        'vision_distance': global_items.average_body_vision_distance,
        'body_speed': global_items.average_body_speed,
        'procreation_threshold': PROCREATION_THRESHOLD,
        'energy': INITIAL_ENERGY
    }

    plant_preference_chance_text_turtle = round(sum(1 if body.food_preference == PLANT else 0 for body in bodies)/bodies_amount*100) # Percent of bodies preferring plants
    for property in averaged:
        if property not in ('generation_n', 'descendants left', 'average_body_speed'):
            if property == 'plant_preference':
                averaged_analysis['plant_preference-now'] = f'The chance that the food preference is "plant" for the survived species now: {plant_preference_chance_text_turtle}%'
                averaged_analysis['plant_preference-initial'] = f'The chance that the food preference is "plant" for every species initially: {round(PLANT_PREFERENCE_CHANCE*RATIO)}%\n'
                averaged_analysis['body_preference-now'] = f'The chance that the food preference is "body" for the survived species now: {100-plant_preference_chance_text_turtle}%'
                averaged_analysis['body_preference-initial'] = f'The chance that the food preference is "body" for every species initially: {100-round(PLANT_PREFERENCE_CHANCE*RATIO)}%\n'
            else:
                averaged_analysis[property+'-now'] = f'The average {property.replace("_", " ")} of the survived species now:\xa0{averaged[property]}'
                value_ = initial_values[property]*100 if float(initial_values[property]) != int(initial_values[property]) else initial_values[property]
                averaged_analysis[property+'-initial'] = f'The average {property.replace("_", " ")} for every species initially:\xa0{int(value_)}\n'

    write_text = [
        one_species_survived_line,
        user_predicted_line,
        descendants_left_line+'\n',
        average_generation_number+'\n'] + [averaged_analysis[text] for text in averaged_analysis]
    
    for text in write_text:
        if text != '':
            write_text_eventual += text+'\n'
    return write_text_eventual

@handle
def display_results(way: int):
    delete_mask()
    match way:
        case config.NO_CREATURES:
            write_text_eventual = 'Neither bodies nor zombies have survived'
        case config.SQUARES_ONE_SPECIES_WON:
            write_text_eventual = find_average_from_bodies()
        case config.ONLY_ZOMBIE_BOSS:
            write_text_eventual = 'Only the zombie boss has survived. This happens tremendously infrequently :)'
        case _:
            write_text_eventual = 'The zombies have won'
    show_tip('')
    showinfo(title=TITLE, message=write_text_eventual)