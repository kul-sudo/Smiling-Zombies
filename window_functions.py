from math import dist
from tkinter import NORMAL, DISABLED

from config import *
from draw_creatures import draw_smiley, draw_zombie_boss
from draw_non_creatures import D_handle_properties
from mask import D_create_mask
from tips import stop_tips_timer, D_tips_handle, force_tip_for_creature, prepare_tips_handle
from global_items import handle, window_commands, smilies, evolution_status, boss_shape_size
from zombie_boss import D_create_new_boss
from special_window_functions import D_change_user_control_widgets_state, set_scales_colours
import global_items

@handle
def D_set_active_scale():
    global_items.active_scale = SPEED
    set_scales_colours()

@handle
def D_set_pause_mode(enable: bool):
    if enable:
        window_commands['run/pause'] = PAUSE
    else:
        window_commands['run/pause'] = RUN

def prepare_selection(): # Preparation before the user can select the zombie boss
    global last_clicked_smiley # The last smiley to be clicked
    last_clicked_smiley = None
    evolution_status.zombie_boss = None

def replace_boss_with_smiley(): # Changing the zombie boss back to a smiley which was on its spot before it was changed to a zombie boss
    global last_clicked_smiley
    # Deleting the boss
    evolution_status.zombie_boss = None
    global_items.canvas.delete('boss')

    # Restoring a smiley on the zombie boss's spot
    smilies.append(last_clicked_smiley)
    draw_smiley(last_clicked_smiley)

def selecting_creature(event):
    '''Maintaining the features that work with the mouse when it is inside the evolution field.'''
    global last_clicked_smiley
    for smiley in smilies:
        if dist((event.x, event.y), (smiley.x, smiley.y)) <= HALF_SMILEY_SIZE*EXTENSION:
            # A smiley has been clicked
            force_tip_for_creature(BOSS) # Displaying a tip forthwith
            # If the zombie boss exits, then it is needed to replace the zombie boss with the smiley which was on its spot before it turned into a zombie boss
            if evolution_status.zombie_boss is not None:
                replace_boss_with_smiley()
            # Handling the smiley which will subsequently be deleted
            last_clicked_smiley = smiley
            global_items.canvas.delete(smiley.image_reference)
            smilies.remove(smiley)
            # Placing a zombie boss instead of a smiley
            D_create_new_boss(
                speed=smiley.speed,
                vision_distance=smiley.vision_distance,
                health=smiley.energy,
                x=smiley.x,
                y=smiley.y)
            draw_zombie_boss()
            D_change_user_control_widgets_state(NORMAL)
            return
    # Click the zombie boss or a void area
    if evolution_status.zombie_boss is not None:
        if dist((event.x, event.y), 
            (evolution_status.zombie_boss.x, evolution_status.zombie_boss.y)) <=\
                boss_shape_size['half_height']*EXTENSION: # Clicked the zombie boss; it is assumed that the height is greater than the width
            force_tip_for_creature(SMILEY) # Displaying a tip forthwith
        replace_boss_with_smiley()
        D_change_user_control_widgets_state(DISABLED)
        last_clicked_smiley = None

def user_select_zombie_boss():
    '''Maintaining the process of the user selecting the zombie boss.'''
    @handle
    def D_selected() -> bool:
        '''A separate function which is required for the decorator to work along with it.'''
        D_handle_properties()
        D_tips_handle()
        return window_commands['run/pause'] == RUN
    prepare_tips_handle()
    while not D_selected():
        continue
    stop_tips_timer()
    if evolution_status.zombie_boss is not None:
        D_create_mask()