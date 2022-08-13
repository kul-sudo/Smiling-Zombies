from global_items import smilies, evolution_status, handle, boss_shape_size
from math import dist
from config import *

import global_items

@handle
def D_show_tip(tip: str):
    '''Setting the text of the area of tips to the parameter of this function.'''
    global_items.tip_text.set(tip)

def tips_for_evolution(): # This function only before the evolution is begun or before the zombie boss is recreated
    if evolution_status.zombie_boss is None:
        tip = PAUSE_RESUME
    else:
        tip = PAUSE_RESUME+'\n'+'You can see the whole evolution field losing the ability to move by clicking LMB. You can undo everything clicking again.'
    D_show_tip(tip)

def prepare_tips_handle(): # Preparing for the future calls of D_tips_handle()
    global previous_hovered_creature, after_id
    previous_hovered_creature = None
    after_id = None

DELAY = 300 # This amount of time has to pass (in ms) for the program to consider the user implies to see the tip for the smiley/zombie boss
BASE_TIP_TEXT = 'If you place your mouse cursor on a smiley, then you will see the further tips.\nClick the right mouse button to commence the evolution '

@handle
def D_tips_handle(): # This function restlessly works while the zombie boss selecting stage is active
    '''Handling the mouse hovering upon the smilies or the zombie boss and displaying all of the needed information.'''
    global previous_hovered_creature, after_id

    # Fetching the position of the mouse cursor
    canvas_mouse_x = global_items.canvas.winfo_pointerx() - global_items.canvas.winfo_rootx()
    canvas_mouse_y = global_items.canvas.winfo_pointery() - global_items.canvas.winfo_rooty()

    # Checking if the mouse cursor is currently hovering upon a smiley   
    hovered_over = None
    for smiley in smilies:
        if dist((canvas_mouse_x, canvas_mouse_y),
                (smiley.x, smiley.y)) <= HALF_SMILEY_SIZE*EXTENSION:
            hovered_over = smiley
            break

    # If hovered_over is None, then it is needed to check if the mouse cursor is currently hovering upon the zombie boss which was previously selected
    if hovered_over is None:         
        if evolution_status.zombie_boss is not None:
                if dist((canvas_mouse_x, canvas_mouse_y), 
                    (evolution_status.zombie_boss.x, evolution_status.zombie_boss.y)) <= boss_shape_size['half_height']*EXTENSION:
                    hovered_over = evolution_status.zombie_boss

    # Displaying the tip or starting the timer
    if hovered_over is None: # The mouse cursor is hovering upon a void area
        previous_hovered_creature = None
        stop_tips_timer()
        # Displaying a tip which is due to be displayed when the mouse cursor is hovering upon a void area
        if evolution_status.zombie_boss is None:
            D_show_tip(BASE_TIP_TEXT + 'without a zombie boss.')
        else:
            D_show_tip(BASE_TIP_TEXT + 'with a zombie boss.')
    else: # The mouse cursor is either on a smiley or on the zombie boss
        if hovered_over is not previous_hovered_creature: # The image the mouse cursor is on has been changed
            previous_hovered_creature = hovered_over
            stop_tips_timer()
            after_id = global_items.tips_label.after(DELAY, 
                    lambda: show_tip_for_creature(BOSS if hovered_over 
                    is evolution_status.zombie_boss else SMILEY)) # Starting a timer for the tip not to blink

def stop_tips_timer():
    global after_id
    if after_id is not None:
        global_items.tips_label.after_cancel(after_id) # Finishing the timer of the preceding image

def show_tip_for_creature(creature: int):
    '''Displaying a tip which fits the status of the creature.'''
    if creature == BOSS:
        tip = 'The creature your cursor is currently on will be able to be supervised by you.\nClick this creature or a void area on the evolution field in order to discard your pick.'
    else:
        tip = 'If you click the creature your cursor is currently on, you will be able to supervise it.\nIf you want to discard your pick, then click this creature once again or click a void area within the evolution field.'
    D_show_tip(tip)

def force_tip_for_creature(creature: int): # When an image is CLICKED, then the tip is displayed sans a timer
    stop_tips_timer()
    show_tip_for_creature(creature)