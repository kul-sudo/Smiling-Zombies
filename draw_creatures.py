from tkinter import ARC, PhotoImage
from tkinter.font import nametofont
from time import time

from config import *
from zombies_images import *
from global_items import evolution_status, bodies

import global_items, config

def create_zombies_image():
    global zombie_boss_shape, zombie_shape, zombie_boss_width
    zombie_boss_shape = PhotoImage(data=ZOMBIE_BOSS).subsample(ZOMBIE_BOSS_SIZE_RATIO, ZOMBIE_BOSS_SIZE_RATIO)
    global_items.zombie_boss_height = zombie_boss_shape.height()
    zombie_boss_width = zombie_boss_shape.width()
    zombie_shape = PhotoImage(data=ZOMBIE).subsample(ZOMBIE_SIZE_RATIO, ZOMBIE_SIZE_RATIO)

    # zombie_boss_shape = RGBTransform().mix_with((255, 0, 0),factor=.30).applied_to(zombie_boss_shape)

def draw_zombie_boss():
    global zombie_boss_shape
    return global_items.canvas.create_image(
        evolution_status.zombie_boss.x, evolution_status.zombie_boss.y, 
        image=zombie_boss_shape, tags='body')

def draw_z(x, y):
    global_items.canvas.create_text(x, y, text='z', tags='z_z_z')

def draw_z_z_z():
    global zombie_boss_width
    zombie_boss = evolution_status.zombie_boss
    if zombie_boss is None:
        return
    x_base = zombie_boss.x+zombie_boss_width/2    
    draw_z(x_base+2, zombie_boss.y-7) 
    draw_z(x_base+7, zombie_boss.y-13)   
    draw_z(x_base+12, zombie_boss.y-21)   

def erase_z_z_z():
    global_items.canvas.delete('z_z_z')      

def draw_zombie(body):
    global zombie_shape
    return global_items.canvas.create_image(body.x, body.y, image=zombie_shape, tags='zombie')

# Drawing the smilies
class Smiley:
    def __init__(self, x, y, rgb, smart):
        self.x = x
        self.y = y
        self.draw_color = 'black' if smart else 'white'
        self.hex = '#%02x%02x%02x' % rgb,
        self.body_tag = f'{x} {y}'

def draw_circle(x, y, radius, hex_color, tags):
    global_items.canvas.create_oval(
        x-radius, y-radius, x+radius, y+radius,
        fill=hex_color,
        width=0,
        tags=tags)

def draw_open_eye(smiley, right_eye):
    draw_circle(
        x=smiley.x+(-1 if right_eye else 1)*BODY_SIZE/6, 
        y=smiley.y-BODY_SIZE/6, radius=BODY_SIZE/20,
        hex_color=smiley.draw_color,
        tags=(smiley.body_tag, 'body')) 

def draw_closed_eye(smiley, right_eye):
    global_items.canvas.create_line(
        smiley.x+(-1 if right_eye else 1)*BODY_SIZE*.1, smiley.y-BODY_SIZE/6,
        smiley.x+(-1 if right_eye else 1)*BODY_SIZE*.3, smiley.y-BODY_SIZE/6,
        fill=smiley.draw_color,
        tags=(smiley.body_tag, 'body'))                

def draw_face_and_eyes(smiley, sleeping: bool):
    draw_circle(
        x=smiley.x,
        y=smiley.y,
        radius=BODY_SIZE/2,
        hex_color=smiley.hex,
        tags=(smiley.body_tag, 'body'))
    if sleeping:                
        draw_closed_eye(smiley=smiley, right_eye=True) 
        draw_closed_eye(smiley=smiley, right_eye=False)   
    else:
        draw_open_eye(smiley=smiley, right_eye=True) 
        draw_open_eye(smiley=smiley, right_eye=False) 

def draw_sleeping_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=True)
    delta_x = BODY_SIZE/6
    delta_y = BODY_SIZE/6
    global_items.canvas.create_line(
        smiley.x-delta_x, smiley.y+delta_y,
        smiley.x+delta_x, smiley.y+delta_y,
        fill=smiley.draw_color,
        tags=(smiley.body_tag, 'body'))
    
def draw_sad_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=False)
    delta_x = BODY_SIZE/3
    global_items.canvas.create_arc(
        smiley.x-delta_x, smiley.y+BODY_SIZE*.1,
        smiley.x+delta_x, smiley.y+BODY_SIZE*1.5, 
        start=60,
        extent=60,
        style=ARC,
        outline=smiley.draw_color,
        tags=(smiley.body_tag, 'body'))  

def draw_smiling_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=False)
    delta_x = BODY_SIZE/2
    global_items.canvas.create_arc(
        smiley.x-delta_x, smiley.y+BODY_SIZE/5,
        smiley.x+delta_x, smiley.y-BODY_SIZE*1.5, 
        start=240,
        extent=60,
        style=ARC,
        outline=smiley.draw_color,
        tags=(smiley.body_tag, 'body'))    

def draw_frightened_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=False)
    delta_x = BODY_SIZE*.1
    global_items.canvas.create_oval(
        smiley.x-delta_x, smiley.y+BODY_SIZE*.1,
        smiley.x+delta_x, smiley.y+BODY_SIZE*.4,
        fill=smiley.draw_color,
        width=0,
        tags=(smiley.body_tag, 'body'))   

def draw_aggressive_smiley(smiley):
    draw_face_and_eyes(smiley=smiley, sleeping=False)
    delta_x = BODY_SIZE*.3
    global_items.canvas.create_oval(
        smiley.x-delta_x, smiley.y+BODY_SIZE*.1,
        smiley.x+delta_x, smiley.y+BODY_SIZE*.2,
        fill=smiley.draw_color,
        width=0,
        tags=(smiley.body_tag, 'body'))

def_font = nametofont("TkDefaultFont")
DISPLAY_PERIOD = 3 # How long a stimulus is displayed

def draw_smiley(body):
    smiley = Smiley(x=body.x, y=body.y, rgb=body.species, smart=body.smart)
    match body.status.description:
        case config.SLEEPING:
            fallen_asleep = body.x != body.previous_x or body.y != body.previous_y
            # fallen_asleep = True: has just fallen asleep
            # fallen_asleep = False: slept on the preceding tact
            # Stimuli shall not be displayed above newly born creatures, since the stimuli overlap one another otherwise
            body.previous_x, body.previous_y = body.x, body.y   
            now = time()
            if global_items.stimulus_on:
                if fallen_asleep: 
                    body.stimulus_start = now
                    # Storing the time when the stimulus was resolved to be displayed
                    # The stimulus might be displayed in a succeeding tact
                if time() > body.stimulus_start + DISPLAY_PERIOD\
                    or body.stimulus_start == now: # The stimulus is not displayed if there was one-tact-long sleep between active states (not sleeping)
                    draw_sleeping_smiley(smiley) 
                else:
                    draw_aggressive_smiley(smiley)
                    x0, y0 = smiley.x+0.5*BODY_SIZE, smiley.y-2.3*BODY_SIZE
                    x1, y1 = x0+46, y0+28, # 46 and 28 have been chosen manually
                    tags = ('stimulus', smiley.body_tag, 'body')
                    global_items.canvas.create_oval(
                        x0, y0, x1, y1,
                        tags=tags, 
                        fill='SystemButtonFace')

                    global_items.canvas.create_text(
                        x0+(x1-x0)/2, y0+(y1-y0)/2,
                        text=body.stimulus,
                        tags=tags,
                        font=(def_font, '12'))

                    global_items.canvas.create_line(
                        smiley.x+0.4*BODY_SIZE, smiley.y-0.4*BODY_SIZE,
                        smiley.x+0.8*BODY_SIZE, smiley.y-0.8*BODY_SIZE,
                        tags=tags)
            else:
                draw_sleeping_smiley(smiley)
        case config.RUNNING_AWAY:
            if body.status.parameter is None:
                draw_sad_smiley(smiley)
            else:
                draw_frightened_smiley(smiley)
        case config.FOLLOWING_PLANT:
            draw_smiling_smiley(smiley)   
        case _:
            draw_aggressive_smiley(smiley)    
    return smiley.body_tag        

def set_stimulus_start():
    # The stimulus is only displayed above the bodies which recently started sleeping
    for body in bodies:
        body.stimulus_start = float('-inf')