from global_items import bodies, evolution_status, handle
from math import dist
from config import *
from time import time

import global_items

def show_tip(tip: str):
    '''Setting the text of the area of tips to the parameter of this function.'''
    global_items.tip_text.set(tip)

def show_tip_for_body(body: object):
    '''Display a tip according to the shape of body.'''
    if body.shape == CIRCLE:
        tip = 'The body your cursor is currently on will be able to be supervised by you.\nClick this body or a void area on the evolution field in order to discard your pick.'
    else:
        tip = 'If you click the body your cursor is currently on, then you will be able to supervise it.\nIf you want to discard your pick, then click this body once again or click a void area within the evolution field.'
    show_tip(tip)

def mouse_clicked_on_body(body: object):
    '''Altering the text of the tip instantaneously.'''
    global selected_creature
    if selected_creature is not None:
        show_tip_for_body(body)

GAP = 3
DELAY = 0.3

def mouse_over():
    # Finding the coordinates of the mouse
    canvas_mouse_x = global_items.canvas.winfo_pointerx() - global_items.canvas.winfo_rootx()
    canvas_mouse_y = global_items.canvas.winfo_pointery() - global_items.canvas.winfo_rooty()
    for body in bodies:
        if dist((canvas_mouse_x, canvas_mouse_y),
                (body.x, body.y)) <= HALF_BODY_SIZE*1.2:
            return body
    return None

def prepare_info_handle():
    global previous_hovered_body, hovering_start, selected_creature

    previous_hovered_body = None
    selected_creature = None

    hovering_start = float('-inf')

def select_creature():
    global previous_hovered_body, hovering_start, selected_creature
    hovered_over = mouse_over()
    if hovered_over is None:
        previous_hovered_body = None
        selected_creature = None
    else:
        if hovered_over is previous_hovered_body:
            if time() >= hovering_start + DELAY:
                selected_creature = hovered_over
        else:
            previous_hovered_body = hovered_over
            hovering_start = time()
            selected_creature = None

@handle
def info_handle():
    '''Handling the mouse hovering upon bodies and displaying all of the needed info.'''
    global selected_creature
    select_creature()
    show_tips()
    global_items.canvas.update()

BASE_TIP_TEXT = 'If you place your mouse cursor on a body, then you will see the further tips.\nClick the right mouse button to commence the evolution '
def show_tips():
    global selected_creature
    if evolution_status.description == PAUSED:
        return
    if selected_creature is None:
        if evolution_status.zombie_boss is None:
            show_tip(BASE_TIP_TEXT + 'without a zombie boss.')
        else:
            show_tip(BASE_TIP_TEXT + 'with a zombie boss.')
    else:
        show_tip_for_body(selected_creature)

def prepare_tips():
    if evolution_status.zombie_boss is None:
        tip = PAUSE_RESUME
    else:
        tip = PAUSE_RESUME+'\n'+'You can see the whole evolution field losing the ability to move by clicking LMB. You can undo everything clicking again.'
    show_tip(tip)