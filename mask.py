from tkinter import Canvas, Tk
from time import sleep

from config import *
from global_items import handle, delete_help_window, window_commands, evolution_status, evolution_field
from draw_creatures import draw_z_z_z, erase_z_z_z, draw_zombie_boss
from draw_non_creatures import set_stimulus_start_time
from special_window_functions import mouse_wheel, switch_scales, start_pause_request

import global_items

global_items.mask_exists = False

@handle
def D_create_mask(rerun = False):
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

    # Deleting the help window when the mask is clicked (any clickable mouse button)
    global_items.mask.bind(
        '<Button-1>',
        lambda event: [
            delete_help_window(),
            draw_z_z_z(),
            set_stimulus_start_time(),
            D_delete_mask()
        ])
    global_items.mask.bind('<Button-2>', delete_help_window)
    global_items.mask.bind('<Button-3>', delete_help_window)

    # Tacking functions to buttons
    global_items.mask.bind('<Button-2>', switch_scales, add='+')
    global_items.mask.bind('<Button-3>', start_pause_request, add='+')

    mask_canvas = Canvas(
        master=global_items.mask,
        width=mask_width,
        height=mask_height,
        bd=0)
    mask_canvas.place(x=0, y=0)

    # Parading the fact that the evolution is still the same displaying a dwindling hole
    if rerun:
        STEPS = 100
        DURATION = 0.7 # In seconds
        half_diagonal = evolution_field['diagonal']/2
        delta = (half_diagonal-evolution_status.zombie_boss.vision_distance)/STEPS
        for step in range(STEPS):
            D_create_hole(special_radius=half_diagonal-delta*step)
            global_items.mask.update()
            sleep(DURATION/STEPS)
        draw_zombie_boss()
        window_commands['run/pause'] = PAUSE
    
@handle
def D_delete_mask(event=None):
    '''Deleting the mask window and nothing apart from that.'''
    if not global_items.mask_exists:
        return
    global_items.mask.destroy()
    global_items.mask_exists = False
    del global_items.mask

@handle
def D_create_hole(special_radius=None):
    if not global_items.mask_exists:
        return
    mask_canvas.delete('hole')

    center_x, center_y = evolution_status.zombie_boss.x, evolution_status.zombie_boss.y

    if special_radius is None:
        radius = evolution_status.zombie_boss.vision_distance-global_items.half_image_size
    else:
        radius = special_radius

    mask_canvas.create_oval(
        center_x-radius, center_y-radius,
        center_x+radius, center_y+radius,
        outline='#%02x%02x%02x' % evolution_status.zombie_boss.species,
        fill='white',
        tags='hole'
    )

@handle
def D_handle_mask(event=None):
    '''If the mask exists, then it is deleted, otherwise it is created.'''
    if evolution_status.zombie_boss is None:
        return
    if global_items.mask_exists:
        D_delete_mask()
        draw_z_z_z()
    else:
        D_create_mask()
        erase_z_z_z()