from pygame.time import Clock

from config import *
from plants import D_create_plant
from crosses import delete_old_cross
from draw_non_creatures import init_stimulus_time, erase_stimulus, D_handle_properties, update_arrows, update_cross_images, update_plant_images
from draw_creatures import update_smiley_images, update_zombie_boss_image, update_zombie_images
from tips import prepare_tips_handle, D_tips_handle, tips_for_evolution
from global_items import handle, window_commands, smilies, evolution_status
from mask import D_create_hole
from zombies import zombie_one_action, zombies
from zombie_boss import zombie_boss_one_action

import global_items

fps_clock = Clock()
FPS = 200

def one_evolution():
    evolution_status.result = None
    D_handle_properties()
    tips_for_evolution()
    init_stimulus_time()
    while True:
        D_one_evolution_step()
        fps_clock.tick(FPS)

        smilies_empty, zombies_empty = smilies == [], zombies == []
        if smilies_empty and not zombies_empty:
            evolution_status.result = ALL_ZOMBIES
        elif smilies_empty and zombies_empty:
            if evolution_status.zombie_boss is None:
                evolution_status.result = NO_CREATURES
            else:
                evolution_status.result = ONLY_ZOMBIE_BOSS
        elif zombies_empty and evolution_status.zombie_boss is None and len(set(smiley.species for smiley in smilies)) == 1:
            evolution_status.result = ONE_SMILEY_SPECIES_WON
        
        if evolution_status.result is not None:
            return    

PLANT_CHANCE = 0.2 if TEST_MODE is False else 0 # The chance (percent = PLANT_CHANCE * 100) of a plant emerging
def memory_things(): # Handling in the memory
    for smiley in smilies:
        smiley.D_one_action()
    for zombie in zombies:
        zombie_one_action(zombie)
    if evolution_status.zombie_boss is not None and global_items.mask_exists:
        zombie_boss_one_action()
    D_create_plant(chance=PLANT_CHANCE)

@handle
def D_one_evolution_step():
    memory_things()
    update_plant_images()
    update_smiley_images()
    update_zombie_images()
    erase_stimulus()
    if evolution_status.zombie_boss is not None:
        update_zombie_boss_image()
    update_arrows()
    delete_old_cross()
    update_cross_images()
    D_handle_properties()
    global_items.canvas.tag_raise('frame', 'all')
    global_items.canvas.update()
    if window_commands['run/pause'] == PAUSE:
        evolution_status.description = PAUSED
        prepare_tips_handle()
        while window_commands['run/pause'] == PAUSE:
            D_handle_properties()
            zombie_boss = evolution_status.zombie_boss
            if zombie_boss is not None:
                D_create_hole()
        evolution_status.description = EVOLUTION # The evolution has been unpaused