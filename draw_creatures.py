from ast import Return
from tkinter import ARC, PhotoImage
from tkinter.font import nametofont
from time import time

from config import *
from zombies_images import *
from global_items import window_commands, evolution_status, smilies, zombies, boss_shape_size, zombie_shape_size 

import global_items, config

# Zombie boss
def create_boss_image():
    ZOMBIE_BOSS_SIZE_RATIO = 27 # Higher => smaller
    # Equalizing the size of a smiley and the size of a zombie boss
    global zombie_boss_shape
    zombie_boss_shape = PhotoImage(data=ZOMBIE_BOSS).subsample(ZOMBIE_BOSS_SIZE_RATIO, ZOMBIE_BOSS_SIZE_RATIO)
    
    boss_shape_size['half_width'] = zombie_boss_shape.width()/2
    boss_shape_size['half_height'] = zombie_boss_shape.height()/2

def draw_zombie_boss():
    global zombie_boss_shape
    global_items.canvas.create_image(
    evolution_status.zombie_boss.x, evolution_status.zombie_boss.y, 
    image=zombie_boss_shape, tags='boss')

def update_zombie_boss_image():
    global_items.canvas.delete('boss')
    draw_zombie_boss()

# Demonstrating the fact that the zombie boss is sleeping/has wakened
def draw_z(x, y):
    global_items.canvas.create_text(x, y, text='z', tags='z_z_z')

def draw_z_z_z():
    '''Demonstrating the fact that the zombie boss is currently sleeping'''
    zombie_boss = evolution_status.zombie_boss
    if zombie_boss is None:
        return
    x_base = zombie_boss.x+boss_shape_size['half_width']    
    draw_z(x_base+2, zombie_boss.y-7)
    draw_z(x_base+7, zombie_boss.y-13)
    draw_z(x_base+12, zombie_boss.y-21)
    # Putting the zombie boss to sleep
    evolution_status.zombie_boss.sleeping = True

def erase_z_z_z():
    global_items.canvas.delete('z_z_z')
    # Wakening the zombie boss
    if evolution_status.zombie_boss is not None:
        evolution_status.zombie_boss.sleeping = False

# Zombies
def create_zombies_image():
    ZOMBIE_SIZE_RATIO = 30 # Higher => smaller
    # Equalizing the size of a smiley and the size of a zombie
    global zombie_shape
    zombie_shape = PhotoImage(data=ZOMBIE).subsample(ZOMBIE_SIZE_RATIO, ZOMBIE_SIZE_RATIO)
    
    zombie_shape_size['half_height'] = zombie_shape.height()/2
    zombie_shape_size['half_width'] = zombie_shape.width()/2

def draw_zombie(zombie):
    global zombie_shape
    global_items.canvas.create_image(zombie.x, zombie.y, image=zombie_shape, tags='zombie')

def update_zombie_images():
    '''Erasing all of the zombies that have already been drawn and drawing new ones.'''
    global_items.canvas.delete('zombie')
    for zombie in zombies:
        draw_zombie(zombie)

# Drawing the smilies
def update_smiley_images():
    '''Erasing all of the smilies that have already been drawn and drawing new ones.'''
    global_items.canvas.delete('smiley')
    for smiley in smilies:
        smiley.image_reference = draw_smiley(smiley)

class SmileyToDraw:
    def __init__(self, x, y, rgb, smart):
        self.x = x
        self.y = y
        self.draw_colour = 'black' if smart else 'white'
        self.hex = '#%02x%02x%02x' % rgb,
        self.smiley_tag = f'{x} {y}'

def draw_circle(x, y, radius, hex_colour, tags):
    global_items.canvas.create_oval(
        x-radius, y-radius, x+radius, y+radius,
        fill=hex_colour,
        width=0,
        tags=tags)

def draw_open_eye(smiley, right_eye):
    draw_circle(
        x=smiley.x+(-1 if right_eye else 1)*SMILEY_SIZE/6, 
        y=smiley.y-SMILEY_SIZE/6, radius=SMILEY_SIZE/20,
        hex_colour=smiley.draw_colour,
        tags=(smiley.smiley_tag, 'smiley')) 

def draw_closed_eye(smiley, right_eye):
    global_items.canvas.create_line(
        smiley.x+(-1 if right_eye else 1)*SMILEY_SIZE*.1, smiley.y-SMILEY_SIZE/6,
        smiley.x+(-1 if right_eye else 1)*SMILEY_SIZE*.3, smiley.y-SMILEY_SIZE/6,
        fill=smiley.draw_colour,
        tags=(smiley.smiley_tag, 'smiley'))

def draw_face_and_eyes(smiley, sleeping: bool):
    draw_circle(
        x=smiley.x,
        y=smiley.y,
        radius=SMILEY_SIZE/2,
        hex_colour=smiley.hex,
        tags=(smiley.smiley_tag, 'smiley'))
    if sleeping:                
        draw_closed_eye(smiley=smiley, right_eye=True) 
        draw_closed_eye(smiley=smiley, right_eye=False)
    else:
        draw_open_eye(smiley=smiley, right_eye=True) 
        draw_open_eye(smiley=smiley, right_eye=False) 

def draw_sleeping_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=True)
    delta_x = SMILEY_SIZE/6
    delta_y = SMILEY_SIZE/6
    global_items.canvas.create_line(
        smiley.x-delta_x, smiley.y+delta_y,
        smiley.x+delta_x, smiley.y+delta_y,
        fill=smiley.draw_colour,
        tags=(smiley.smiley_tag, 'smiley'))
    
def draw_sad_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=False)
    delta_x = SMILEY_SIZE/3
    global_items.canvas.create_arc(
        smiley.x-delta_x, smiley.y+SMILEY_SIZE*.1,
        smiley.x+delta_x, smiley.y+SMILEY_SIZE*1.5, 
        start=60,
        extent=60,
        style=ARC,
        outline=smiley.draw_colour,
        tags=(smiley.smiley_tag, 'smiley'))

def draw_smiling_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=False)
    delta_x = SMILEY_SIZE/2
    global_items.canvas.create_arc(
        smiley.x-delta_x, smiley.y+SMILEY_SIZE/5,
        smiley.x+delta_x, smiley.y-SMILEY_SIZE*1.5, 
        start=240,
        extent=60,
        style=ARC,
        outline=smiley.draw_colour,
        tags=(smiley.smiley_tag, 'smiley'))

def draw_frightened_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=False)
    delta_x = SMILEY_SIZE*.1
    global_items.canvas.create_oval(
        smiley.x-delta_x, smiley.y+SMILEY_SIZE*.1,
        smiley.x+delta_x, smiley.y+SMILEY_SIZE*.4,
        fill=smiley.draw_colour,
        width=0,
        tags=(smiley.smiley_tag, 'smiley'))

def draw_aggressive_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=False)
    delta_x = SMILEY_SIZE*.3
    global_items.canvas.create_oval(
        smiley.x-delta_x, smiley.y+SMILEY_SIZE*.1,
        smiley.x+delta_x, smiley.y+SMILEY_SIZE*.2,
        fill=smiley.draw_colour,
        width=0,
        tags=(smiley.smiley_tag, 'smiley'))

def_font = nametofont("TkDefaultFont")
DISPLAY_PERIOD = 3 # How long a stimulus is displayed

def draw_smiley(smiley):
    smiley_to_draw = SmileyToDraw(x=smiley.x, y=smiley.y, rgb=smiley.species, smart=smiley.smart)
    match smiley.status.description:
        case config.SLEEPING:
            fallen_asleep = smiley.x != smiley.previous_x or smiley.y != smiley.previous_y
            # fallen_asleep = True: has just fallen asleep
            # fallen_asleep = False: slept on the preceding tact
            # Stimuli shall not be displayed above newly born creatures, since the stimuli overlap one another otherwise
            smiley.previous_x, smiley.previous_y = smiley.x, smiley.y   
            now = time()
            if global_items.stimulus_on:
                if fallen_asleep: 
                    smiley.stimulus_start = now
                    # Storing the time when the stimulus was resolved to be displayed
                    # The stimulus might be displayed in a succeeding tact

                if time() > smiley.stimulus_start + DISPLAY_PERIOD\
                    or window_commands['to-show-selected-property'] != 'Nothing'\
                    or smiley.stimulus_start == now: # The stimulus is not displayed if there was one-tact-long sleep between active states (not sleeping)
                    
                    draw_sleeping_smiley(smiley_to_draw) 
                else:
                    draw_aggressive_smiley(smiley_to_draw)

                    # The stimulus by smilies
                    x0, y0 = smiley_to_draw.x+0.5*SMILEY_SIZE, smiley_to_draw.y-2.3*SMILEY_SIZE
                    x1, y1 = x0+46, y0+28, # 46 and 28 have been chosen manually
                    tags = ('stimulus', smiley_to_draw.smiley_tag, 'smiley')
                    global_items.canvas.create_oval(
                        x0, y0, x1, y1,
                        tags=tags, 
                        fill='SystemButtonFace')

                    global_items.canvas.create_text(
                        x0+(x1-x0)/2, y0+(y1-y0)/2,
                        text=smiley.stimulus,
                        tags=tags,
                        font=(def_font, '12'))

                    global_items.canvas.create_line(
                        smiley_to_draw.x+0.4*SMILEY_SIZE, smiley_to_draw.y-0.4*SMILEY_SIZE,
                        smiley_to_draw.x+0.8*SMILEY_SIZE, smiley_to_draw.y-0.8*SMILEY_SIZE,
                        tags=tags)
            else:
                draw_sleeping_smiley(smiley_to_draw)
        case config.RUNNING_AWAY:
            if smiley.status.parameter is None:
                draw_sad_smiley(smiley_to_draw)
            else:
                draw_frightened_smiley(smiley_to_draw)
        case config.FOLLOWING_PLANT:
            draw_smiling_smiley(smiley_to_draw)
        case _:
            draw_aggressive_smiley(smiley_to_draw)
    return smiley_to_draw.smiley_tag