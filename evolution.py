from tkinter import DISABLED
from config import *
from bodies_functions import create_zero_generation, delete_all_bodies
from mask import delete_mask, handle_mask
from plants import create_initial_plants, create_plant_image, delete_all_plants
from draw_erase import update_body_images, update_plant_images, update_zombie_images
from crosses import create_cross_image, delete_all_crosses
from window_functions import selecting_body, set_active_scale, change_user_control_widgets_state, pause_mode, user_select_body
from evolution_functions import one_evolution
from zombies import delete_all_zombies
from tips import show_tip
from global_items import evolution_field, ExceptionToRestart, evolution_status, window, start_pause_request
if STRAIGHTFORWARD_FIX:
    from draw_creatures import create_zombies_image

import global_items

def evolution():
    create_plant_image()
    create_cross_image()
    if STRAIGHTFORWARD_FIX:
        create_zombies_image()
    while True:
        try:
            evolution_status.description = CONTROL_PREPARATION
            change_user_control_widgets_state(DISABLED)
            global_items.canvas.unbind('<Button-3>')
            set_active_scale()
            global_items.wonderful_game_button.pack_forget()
 
            evolution_status.description = DELETE_EVERYTHING

            global_items.stimulus_on = False 
            delete_mask()
            show_tip('')
            # Nothing in DELETE_EVERYTHING is done if there was no preceding evolution
            delete_all_bodies()
            delete_all_zombies()
            delete_all_plants()
            delete_all_crosses()
            global_items.canvas.delete('all')

            window.update()

            evolution_status.description = EVOLUTION_PREPARATION
            
            global_items.canvas.create_rectangle(2, 2, evolution_field['width']+1, evolution_field['height']+1)

            create_zero_generation()
            create_initial_plants()
            update_body_images()
            update_plant_images()
            update_zombie_images()

            evolution_status.description = USER_SELECTING_BODY
            evolution_status.zombie_boss = None
            global_items.canvas.bind('<Button-3>', start_pause_request)
            global_items.canvas.bind('<Button-1>', selecting_body)
            pause_mode(True)
            user_select_body()
            global_items.canvas.unbind('<Button-1>')

            evolution_status.description = EVOLUTION
            evolution_status.survivor = None
            global_items.canvas.bind('<Button-1>', handle_mask)
            one_evolution()
            delete_mask()
            show_tip('')
            global_items.canvas.unbind('<Button-1>')
            global_items.canvas.unbind('<Button-3>')
            change_user_control_widgets_state(DISABLED)
            global_items.wonderful_game_button.pack_forget()
        except ExceptionToRestart:
            continue