from tkinter import Canvas, Tk
from time import sleep

from config import *
from global_items import handle, start_pause_request, switch_scales, mouse_wheel, delete_help, window_commands, evolution_status, evolution_field
from draw_creatures import draw_zombie_boss, draw_z_z_z, erase_z_z_z, set_stimulus_start

import global_items

global_items.mask_exists = False

@handle
def create_mask(rerun = False):
    '''Creating the mask window.'''
    global mask_canvas

    global_items.mask = Tk()
    global_items.mask_exists = True

    mask_width = round(evolution_field['width'])+2
    mask_height = round(evolution_field['height'])+2

    global_items.mask.title('do not touch me')

    global_items.mask.geometry(f"{mask_width}x{mask_height}+{global_items.canvas.winfo_rootx()}+{global_items.canvas.winfo_rooty()}")
    
    global_items.mask.overrideredirect(True)
    global_items.mask.attributes('-topmost', True)
    global_items.mask.attributes('-transparentcolor', 'white')
    global_items.mask.bind('<MouseWheel>', mouse_wheel)

    global_items.mask.bind(
        '<Button-1>',
        lambda event: [draw_z_z_z(), set_stimulus_start(), delete_help(), delete_mask()])

    global_items.mask.bind('<Button-2>', delete_help)
    global_items.mask.bind('<Button-2>', switch_scales, add='+')
    global_items.mask.bind('<Button-3>', delete_help)
    global_items.mask.bind('<Button-3>', start_pause_request, add='+')

    mask_canvas = Canvas(
        master=global_items.mask,
        width=mask_width,
        height=mask_height,
        bd=0)
    mask_canvas.place(x=0, y=0)

    # Parading the fact that the evolution is still the same
    if rerun:
        STEPS = 100
        DURATION = 0.7 # In seconds
        half_diagonal = global_items.diagonal/2
        delta = (half_diagonal-evolution_status.zombie_boss.vision_distance)/STEPS
        for step in range(STEPS):
            create_hole(evolution_status.zombie_boss, special_radius=half_diagonal-delta*step)
            global_items.mask.update()     
            sleep(DURATION/STEPS)
        draw_zombie_boss()
        window_commands['run/pause'] = PAUSE
    
@handle
def delete_mask(event=None):
    '''Deleting the mask window and nothing apart from that.'''
    if not global_items.mask_exists:
        return
    global_items.mask.destroy()
    global_items.mask_exists = False
    del global_items.mask

@handle
def create_hole(body: object, special_radius=None):
    if not global_items.mask_exists:
        return
    mask_canvas.delete('hole')

    center_x, center_y = body.x, body.y

    if special_radius is None:
        radius = body.vision_distance-global_items.half_image_size
    else:
        radius = special_radius

    mask_canvas.create_oval(
        center_x-radius, center_y-radius,
        center_x+radius, center_y+radius,
        outline='#%02x%02x%02x' % body.species,
        fill='white',
        tags='hole'
    )

@handle
def handle_mask(event=None):
    '''If the mask exists, then it is deleted, otherwise it is created.'''
    if evolution_status.zombie_boss is None:
        return
    if global_items.mask_exists:
        delete_mask()

        draw_z_z_z()

    else:
        create_mask()

        erase_z_z_z()