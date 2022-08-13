from tkinter import DISABLED
from config import *
from smilies_functions import create_zero_generation, D_delete_all_smilies
from mask import D_delete_mask, D_handle_mask
from plants import create_initial_plants, create_plant_image, D_delete_all_plants
from draw_non_creatures import update_plant_images
from draw_creatures import create_boss_image, update_smiley_images, update_zombie_images
from crosses import create_cross_image, D_delete_all_crosses
from window_functions import prepare_selection, selecting_creature, D_set_active_scale, D_set_pause_mode, user_select_zombie_boss
from special_window_functions import D_change_user_control_widgets_state, start_pause_request
from evolution_functions import one_evolution
from zombies import D_delete_all_zombies
from tips import D_show_tip
from global_items import evolution_field, ExceptionToRestart, evolution_status, window
from draw_creatures import create_zombies_image
from display_results import D_display_results

import global_items

def evolution():
    create_plant_image()
    create_cross_image()
    create_zombies_image()
    create_boss_image()
    while True:
        try:
            # Setting the default states for controls
            evolution_status.description = CONTROL_PREPARATION
            D_change_user_control_widgets_state(DISABLED)
            D_set_active_scale()
            global_items.canvas.unbind('<Button-3>')
            global_items.wonderful_game_button.pack_forget()
 
            # Deleting everything unneeded
            evolution_status.description = DELETE_ERASE_EVERYTHING
            global_items.stimulus_on = False 
            D_delete_mask()
            D_delete_all_smilies()
            D_delete_all_zombies()
            D_delete_all_plants()
            D_delete_all_crosses()
            global_items.canvas.delete('all')
            # Nothing in 'Deleting everything unneeded' is done if there was no preceding evolution
            D_show_tip('')
            window.update()

            # Evolution prep
            evolution_status.description = EVOLUTION_PREPARATION
            global_items.canvas.create_rectangle(2, 2, evolution_field['width']+1, evolution_field['height']+1, tags='frame') # Evolution field frame
            create_zero_generation()
            create_initial_plants()
            update_smiley_images()
            update_plant_images()
            update_zombie_images()

            # Selecting the zombie boss
            evolution_status.description = USER_SELECTING_ZOMBIE_BOSS
            global_items.canvas.bind('<Button-3>', start_pause_request)
            global_items.canvas.bind('<Button-1>', selecting_creature)
            D_set_pause_mode(True)
            prepare_selection()
            user_select_zombie_boss()
            global_items.canvas.unbind('<Button-1>')

            # The evolution has begun
            evolution_status.description = EVOLUTION
            evolution_status.survivor = None
            global_items.canvas.bind('<Button-1>', D_handle_mask)
            one_evolution()

            # Displaying the results of the evolution
            evolution_status.description = RESULTS
            D_delete_mask()
            D_show_tip('')
            global_items.canvas.unbind('<Button-1>')
            global_items.canvas.unbind('<Button-3>')
            D_change_user_control_widgets_state(DISABLED)
            global_items.wonderful_game_button.pack_forget()
            D_display_results()
        except ExceptionToRestart:
            continue