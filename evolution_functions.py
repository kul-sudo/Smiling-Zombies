from pygame.time import Clock

from config import *
from display_results import display_results
from plants import create_plant
from crosses import delete_old_cross
from draw_erase import init_stimulus_time, stimulus_off, handle_properties, update_arrows, update_cross_images, update_plant_images, update_body_images, update_zombie_boss_image, update_zombie_images
from tips import prepare_info_handle, info_handle, prepare_tips
from global_items import handle, window_commands, bodies, evolution_status
from mask import create_hole
from zombies import zombie_boss_one_action, zombie_one_action, zombies

import global_items

fps_clock = Clock()

def one_evolution():
    zombie_boss = evolution_status.zombie_boss
    if zombie_boss is not None:
        bodies.remove(zombie_boss)
        zombie_boss.species = (0, 0, 0)

    handle_properties()
    prepare_tips()
    init_stimulus_time()

    while True:
        one_evolution_step()
        fps_clock.tick(FPS)

        bodies_empty, zombies_empty = bodies == [], zombies == []
        if bodies_empty and not zombies_empty:
            display_results(ALL_ZOMBIES)
            return
        elif bodies_empty and zombies_empty:
            if evolution_status.zombie_boss is None:
                display_results(NO_CREATURES)
            else:
                display_results(ONLY_ZOMBIE_BOSS)
            return
        elif zombies_empty and evolution_status.zombie_boss is None and len(set(body.species for body in bodies)) == 1:
            display_results(SQUARES_ONE_SPECIES_WON)
            return

def memory_things():
    for body in bodies:
        body.one_action()
    for zombie in zombies:
        zombie_one_action(zombie)
    if evolution_status.zombie_boss is not None and global_items.mask_exists:
        zombie_boss_one_action()
    create_plant(chance=PLANT_CHANCE)

@handle
def one_evolution_step():
    memory_things()
    update_plant_images()
    update_body_images()
    update_zombie_images()
    stimulus_off()
    if evolution_status.zombie_boss is not None:
        update_zombie_boss_image()
    update_arrows()
    delete_old_cross()
    update_cross_images()
    handle_properties()
    global_items.canvas.update()
    if window_commands['run/pause'] == PAUSE:
        evolution_status.description = PAUSED
        prepare_info_handle()
        while window_commands['run/pause'] == PAUSE:
            handle_properties()
            info_handle()
            zombie_boss = evolution_status.zombie_boss
            if zombie_boss is not None:
                create_hole(zombie_boss)
                
        evolution_status.description = EVOLUTION