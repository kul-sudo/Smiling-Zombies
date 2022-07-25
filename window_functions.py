from math import dist
from tkinter import NORMAL, DISABLED

from config import *
from draw_erase import change_shape_to_circle, handle_properties, restore_user_selected_body_shape, restore_user_selected_body_speed, restore_user_selected_body_vision_distance
from mask import create_mask
from tips import info_handle, mouse_clicked_on_body, prepare_info_handle
from global_items import set_scales_colors, handle, window_commands, bodies, evolution_status
import global_items

@handle
def mutate_scales(showvalue: bool, sliderlength: int):
    for widget in (global_items.user_selected_body_speed, global_items.user_selected_vision_distance):
        widget.configure(
            showvalue=showvalue,
            sliderlength=sliderlength)

def set_active_scale():
    global_items.active_scale = SPEED
    set_scales_colors()

@handle
def change_user_control_widgets_state(state: str):
    '''Changing the states of all of the buttons of the user control frame to the state specified as the parameter.'''
    for widget in global_items.user_control_frame.winfo_children():
        widget.configure(state=state)
    if state == NORMAL:
        selected_body = evolution_status.zombie_boss
        global_items.health_to_display.set(f'Health:\n{round(selected_body.health)}')
        mutate_scales(showvalue=True, sliderlength=20)
        global_items.user_selected_body_speed.set(round(selected_body.speed*RATIO))
        global_items.user_selected_vision_distance.set(round(selected_body.vision_distance))
    else:
        global_items.health_to_display.set('Health:\n--')
        mutate_scales(showvalue=False, sliderlength=0)

@handle
def pause_mode(enable: bool):
    if enable:
        window_commands['run/pause'] = PAUSE
    else:
        window_commands['run/pause'] = RUN

def restore_properties():
    restore_user_selected_body_speed()
    restore_user_selected_body_vision_distance()
    restore_user_selected_body_shape()

def selecting_body(event):
    '''Maintaining the features that work with the mouse when it is inside the evolution field.'''
    clicked_body = NOTHING_CLICKED
    for body in bodies:
        if dist((event.x, event.y),
                (body.x, body.y)) <= HALF_BODY_SIZE*1.2:
            clicked_body = body
            break
    if clicked_body == NOTHING_CLICKED:
        if any(body.shape == CIRCLE for body in bodies):
            evolution_status.zombie_boss = None
            restore_properties()
            change_user_control_widgets_state(DISABLED)
        return
    mouse_clicked_on_body(clicked_body)
    if clicked_body.shape == CIRCLE:
        evolution_status.zombie_boss = None
        change_user_control_widgets_state(DISABLED)
        restore_properties()
    else:
        restore_properties()
        evolution_status.zombie_boss = clicked_body
        evolution_status.zombie_boss.health = clicked_body.energy
        change_shape_to_circle(clicked_body)
        change_user_control_widgets_state(NORMAL)

def user_select_body():
    '''Maintaining the process of the user selecting the body.'''
    @handle
    def selected() -> bool:
        '''A separate function which is required for the decorator to work along with it.'''
        handle_properties()

        info_handle()
        return window_commands['run/pause'] == RUN
    prepare_info_handle()
    while not selected():
        continue
    if evolution_status.zombie_boss is not None:
        create_mask()

# 'What a wonderful game' button blinking
blink_text = {
    WHAT_A_WONDERFUL_GAME: '',
    '': WHAT_A_WONDERFUL_GAME
}

BLINK_TIMES = 9

blink_times = 0

def blink():
    global blink_times
    blink_times += 1
    if blink_times % BLINK_TIMES == 0:
        return
    global_items.wonderful_game_button.configure(text=blink_text[global_items.wonderful_game_button['text']])
    global_items.wonderful_game_button.after(500, blink)