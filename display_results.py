from tkinter.messagebox import showinfo
from statistics import fmean

from config import *
from global_items import handle, smilies, smilies_data, evolution_status

import config

@handle
def D_find_average_from_smileys():
    smilies_amount = len(smilies)

    write_text_eventual = ''

    averaged = {
        'generation_n': round(fmean(smiley.generation_n for smiley in smilies)),
        'plant_preference': round(fmean(1 if smiley.food_preference == PLANTS else 0 for smiley in smilies)), # Percent of smileys preferring plants
        'vision_distance': round(fmean(smiley.vision_distance for smiley in smilies)),
        'average_smiley_speed': round(fmean(smiley.speed for smiley in smilies)*SPEED_RATIO),
        'procreation_threshold': round(fmean(smiley.procreation_threshold for smiley in smilies)),
        'energy': round(fmean(smiley.energy for smiley in smilies)),
        'descendants left': smilies_amount,
    }

    averaged_analysis = {}

    one_species_survived_line = 'One of the species has survived'
    average_generation_number = f'The average generation number of the smileys of the survived species: {averaged["generation_n"]}'
    
    def ending() -> str: # Handling the 's' at the end of the word 'descendant'
        return f"{smilies_amount} descendant{'s' if smilies_amount > 1 else ''} left"

    descendants_left_line = ending()

    initial_values = {
        'vision_distance': smilies_data['average_vision_distance'],
        'smiley_speed': smilies_data['average_speed'],
        'procreation_threshold': PROCREATION_THRESHOLD,
        'energy': INITIAL_ENERGY
    }

    plant_preference_chance_text_turtle = round(sum(1 if smiley.food_preference == PLANTS else 0 for smiley in smilies)/smilies_amount*100) # Percent of smileys preferring plants
    for property in averaged:
        if property not in ('generation_n', 'descendants left', 'average_smiley_speed'):
            if property == 'plant_preference':
                averaged_analysis['plant_preference-now'] = f'The chance that the food preference is "plant" for the survived species now: {plant_preference_chance_text_turtle}%'
                averaged_analysis['plant_preference-initial'] = f'The chance that the food preference is "plant" for every species initially: {round(PLANT_PREFERENCE_CHANCE*SPEED_RATIO)}%\n'
                averaged_analysis['smiley_preference-now'] = f'The chance that the food preference is "smiley" for the survived species now: {100-plant_preference_chance_text_turtle}%'
                averaged_analysis['smiley_preference-initial'] = f'The chance that the food preference is "smiley" for every species initially: {100-round(PLANT_PREFERENCE_CHANCE*SPEED_RATIO)}%\n'
            else:
                averaged_analysis[property+'-now'] = f'The average {property.replace("_", " ")} of the survived species now:\xa0{averaged[property]}'
                value_ = initial_values[property]*100 if float(initial_values[property]) != int(initial_values[property]) else initial_values[property]
                averaged_analysis[property+'-initial'] = f'The average {property.replace("_", " ")} for every species initially:\xa0{int(value_)}\n'

    write_text = [
        one_species_survived_line,
        descendants_left_line+'\n',
        average_generation_number+'\n'] + [averaged_analysis[text] for text in averaged_analysis]
    
    for text in write_text:
        if text != '':
            write_text_eventual += text+'\n'
    return write_text_eventual

@handle
def D_display_results():
    match evolution_status.result:
        case config.NO_CREATURES:
            write_text_eventual = 'Neither smileys nor zombies have survived'
        case config.SQUARES_ONE_SPECIES_WON:
            write_text_eventual = D_find_average_from_smileys()
        case config.ONLY_ZOMBIE_BOSS:
            write_text_eventual = 'Only the zombie boss has survived. This happens tremendously infrequently :)'
        case _:
            write_text_eventual = 'The zombies have won'
    showinfo(title=TITLE, message=write_text_eventual)