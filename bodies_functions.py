from math import dist, sqrt
from random import randrange, random
from tkinter import NORMAL

from config import *
from bodies_class import Body
from global_items import distance_between_objects, handle, random_attribute, random_place, handle, bodies, progenitor_properties, evolution_status, evolution_field
from mask import create_mask, handle_mask
from window_functions import change_user_control_widgets_state

import global_items

def calculate_data_for_body():
    d_old = sqrt(950**2+500**2) # Diagonal of the evolution field in the preceding version of the project
    global_items.diagonal = sqrt(evolution_field['width']**2+evolution_field['height']**2)
    ratio = global_items.diagonal/d_old
    global_items.average_body_speed = OLD_BODY_SPEED*ratio
    global_items.average_body_vision_distance = OLD_VISION_DISTANCE*ratio
    global_items.energy_for_vision = OLD_ENERGY_FOR_VISION/ratio
    global_items.energy_for_moving = OLD_ENERGY_FOR_MOVING/ratio

def create_zero_generation():
    '''Creating the zeroth generation of bodies.'''
    global used_colours
    used_colours = [PLANT_COLOUR]
    for id_ in range(BODIES_AMOUNT):
        create_one_body(id_)

@handle
def suitable_colours(expected_colour: tuple[int], used_colour: tuple[int], distance: int | float) -> bool:
    '''Making sure expected_colour is different enough from used_colour using the distance formula.'''
    return dist(expected_colour, used_colour) >= distance

@handle
def create_one_body(id_: int):
    distance = MAX_COLOUR_DISTANCE
    while True:
        expected_colour = (randrange(0, MAXIMUM_COLOUR), randrange(0, MAXIMUM_COLOUR), randrange(0, MAXIMUM_COLOUR))
        if expected_colour in used_colours:
            continue
        if all(suitable_colours(expected_colour, used_colour, distance) for used_colour in used_colours):
            break
        distance -= 0.04

    used_colours.append(expected_colour)

    body = Body(
        generation_n=0,
        energy=random_attribute(INITIAL_ENERGY, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        shape=SQUARE,
        food_preference=PLANT if random() < PLANT_PREFERENCE_CHANCE else BODY,
        vision_distance=random_attribute(global_items.average_body_vision_distance, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        speed=random_attribute(global_items.average_body_speed, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        procreation_threshold=random_attribute(PROCREATION_THRESHOLD, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        color=expected_colour,
        species_id=id_,
        x=0,
        y=0
    )

    while True:
        body.x, body.y = random_place(shape_size=BODY_SIZE)
        if all(distance_between_objects(body, another_body) > DOUBLE_BODY_SIZE for another_body in bodies):
            break
    bodies.append(body)
    
    progenitor_properties[body.species_id] = {
        'progenitor_food_preference': body.food_preference,
        'progenitor_vision_distance': body.vision_distance,
        'progenitor_body_speed': body.speed,
        'progenitor_procreation_threshold': body.procreation_threshold,
        'progenitor_energy': body.energy,
        'progenitor_x': body.x,
        'progenitor_y': body.y
    }

@handle
def delete_all_bodies():
    bodies.clear()
    progenitor_properties.clear()

@handle
def create_new_boss(): # This function is placed in the bodies_class module to evade a circular import
    evolution_status.zombie_boss = Body(
        generation_n=0,
        energy=None, # The health is set subsequently
        shape=CIRCLE,
        food_preference=None,
        vision_distance=global_items.average_body_vision_distance,
        speed=global_items.average_body_speed,
        procreation_threshold=None,
        color=(0, 0, 0),
        species_id=None,
        x=evolution_field['width']/2,
        y=evolution_field['height']/2
    )
    evolution_status.zombie_boss.health = INITIAL_ENERGY

    change_user_control_widgets_state(NORMAL)

    create_mask(rerun=True)