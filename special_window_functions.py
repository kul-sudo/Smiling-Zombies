from tkinter import NORMAL

from config import *
from global_items import scales, evolution_status, window, window_commands, handle

import global_items

@handle
def D_mutate_scales(showvalue: bool, sliderlength: int):
    for widget in (scales['speed'], scales['vision distance']):
        widget.configure(
            showvalue=showvalue,
            sliderlength=sliderlength)

@handle
def D_change_user_control_widgets_state(state: str):
    '''Changing the states of all of the buttons of the user control frame to the state specified as the parameter.'''
    for widget in global_items.user_control_frame.winfo_children():
        widget.configure(state=state)
    if state == NORMAL:
        selected_smiley = evolution_status.zombie_boss
        global_items.boss_health.set(f'Health:\n{round(selected_smiley.health)}')
        D_mutate_scales(showvalue=True, sliderlength=20)
        scales['speed'].set(round(selected_smiley.speed*SPEED_RATIO))
        scales['vision distance'].set(round(selected_smiley.vision_distance))
    else:
        global_items.boss_health.set('Health:\n--')
        D_mutate_scales(showvalue=False, sliderlength=0)

# 'What a wonderful game' button blinking
blink_text = {
    WHAT_A_WONDERFUL_GAME: '',
    '': WHAT_A_WONDERFUL_GAME
}

BLINK_TIMES = 9
blink_times = 0

def blink():
    global blink_times, blink_id 
    blink_times += 1
    if blink_times % BLINK_TIMES == 0:
        return
    global_items.wonderful_game_button.configure(text=blink_text[global_items.wonderful_game_button['text']])
    blink_id = global_items.wonderful_game_button.after(500, blink)

def cancel_blink():
    global blink_id
    try:
        global_items.wonderful_game_button.after_cancel(blink_id)
    except NameError:
        return

def mouse_wheel(event):
    scale = scales['speed'] if global_items.active_scale == SPEED else scales['vision distance']
    current_value = scale.get()
    if event.delta > 0:
        scale.set(current_value+1)
    else:
        scale.set(current_value-1)

def set_scales_colours():    
    if global_items.active_scale == VISION_DISTANCE:
        scales['vision distance'].configure(bg='light yellow')
        scales['speed'].configure(bg='SystemButtonFace')
    else:
        scales['vision distance'].configure(bg='SystemButtonFace')
        scales['speed'].configure(bg='light yellow')
    window.update()

def switch_scales(event):
    '''If the active scale is the one for vision distance then, the active one becomes the scale for speed, and vice versa.'''
    global_items.active_scale = VISION_DISTANCE if global_items.active_scale == SPEED else SPEED
    set_scales_colours()

def start_pause_request(event):
    '''Switching between evolution and pause'''
    window_commands['run/pause'] = PAUSE if window_commands['run/pause'] == RUN else RUN      