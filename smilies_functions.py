from math import dist, sqrt
from random import randrange, random

from config import *
from smilies_class import Smiley
from global_items import smilies_data, distance_between_objects, handle, random_attribute, random_place, handle, smilies, evolution_field

OLD_VISION_DISTANCE = 75 # A satisfying value for the size of the evolution field being {'width': 950, 'height': 500}
OLD_SMILEY_SPEED = 0.6 # A satisfying value for the size of the evolution field being {'width': 950, 'height': 500}
OLD_ENERGY_FOR_VISION = 0.00007*PLANT_ENERGY if TEST_MODE is False else 0.01 # A satisfying value for the size of the evolution field being {'width': 950, 'height': 500}
OLD_ENERGY_FOR_MOVING = 0.007*PLANT_ENERGY if TEST_MODE is False else 0.000000000001

def calculate_data_for_smilies():
    d_old = sqrt(950**2+500**2) # Diagonal of the evolution field in the preceding version of the project
    ratio = evolution_field['diagonal']/d_old
    smilies_data['average_speed'] = OLD_SMILEY_SPEED*ratio
    smilies_data['average_vision_distance'] = OLD_VISION_DISTANCE*ratio
    smilies_data['energy_for_vision'] = OLD_ENERGY_FOR_VISION/ratio
    smilies_data['energy_for_moving'] = OLD_ENERGY_FOR_MOVING/ratio

PLANT_COLOUR = (14, 209, 69) # Not defining the colour, but saying that the RGB of the plant is this one
def create_zero_generation():
    '''Creating the zeroth generation of smileys.'''
    global used_colours
    used_colours = [PLANT_COLOUR]
    for id_ in range(SMILIES_AMOUNT):
        D_create_one_smiley(id_)

@handle
def D_suitable_colours(expected_colour: tuple[int], used_colour: tuple[int], distance: int | float) -> bool:
    '''Making sure expected_colour is different enough from used_colour using the distance formula.'''
    return dist(expected_colour, used_colour) >= distance

DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION = 0.4 # Proportionates to standard deviation for the zero generation
MAXIMUM_COLOUR = 220
MAX_COLOUR_DISTANCE = sqrt(3*MAXIMUM_COLOUR**2) # This is the maximum of sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)
DOUBLE_SMILEY_SIZE = SMILEY_SIZE*2
DISTANCE_DELTA = 0.04

@handle
def D_create_one_smiley(id_: int):
    distance = MAX_COLOUR_DISTANCE
    while True:
        expected_colour = (randrange(0, MAXIMUM_COLOUR), randrange(0, MAXIMUM_COLOUR), randrange(0, MAXIMUM_COLOUR))
        if expected_colour in used_colours:
            continue
        if all(D_suitable_colours(expected_colour, used_colour, distance) for used_colour in used_colours):
            break
        distance -= DISTANCE_DELTA

    used_colours.append(expected_colour)

    smiley = Smiley(
        generation_n=0,
        energy=random_attribute(INITIAL_ENERGY, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        food_preference=PLANTS if random() < PLANT_PREFERENCE_CHANCE else SMILIES,
        vision_distance=random_attribute(smilies_data['average_vision_distance'], deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        speed=random_attribute(smilies_data['average_speed'], deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        procreation_threshold=random_attribute(PROCREATION_THRESHOLD, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        colour=expected_colour,
        species_id=id_,
        x=0,
        y=0
    )

    while True:
        smiley.x, smiley.y = random_place(shape_size=SMILEY_SIZE)
        if all(distance_between_objects(smiley, another_smiley) > DOUBLE_SMILEY_SIZE for another_smiley in smilies):
            break
    smilies.append(smiley)
    
@handle
def D_delete_all_smilies():
    smilies.clear()