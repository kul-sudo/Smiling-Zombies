TEST_MODE = False

# Constants to make the code cleaner
TITLE = 'Smiling Zombies'
PAUSE_RESUME = 'Use your right mouse button in order to pause/resume the evolution.'
WHAT_A_WONDERFUL_GAME = 'What a wonderful game!'
SMILIES = 'smilies'
PLANTS = 'plants'

SPEED = 0
VISION_DISTANCE = 1

RUN = 0
PAUSE = 1

SLEEPING = 0
RUNNING_AWAY = 1
FOLLOWING_PLANT = 2
FOLLOWING_SMILEY = 3

CONTROL_PREPARATION = 0
DELETE_ERASE_EVERYTHING = 1
EVOLUTION_PREPARATION = 2
EVOLUTION = 3
USER_SELECTING_ZOMBIE_BOSS = 4
RESULTS = 5
PAUSED = 6

BOSS = 0
SMILEY = 1

NO_CREATURES = 0
ONE_SMILEY_SPECIES_WON = 1
ALL_ZOMBIES = 2
ONLY_ZOMBIE_BOSS = 3

SMILIES_AMOUNT = 20 if TEST_MODE is False else 2 # The initial number of smilies on the evolution field

# Plants
PLANT_PREFERENCE_CHANCE = 0.5 # The chance that the smiley will prefer eating plant
PLANT_ENERGY = 100 # Energy to a smiley for eating a plant
INITIALLY_PLANTED = SMILIES_AMOUNT*3 if TEST_MODE is False else 100 # Amount of plants that have to be planted initially

# Smilies
SMILEY_SIZE = 14
HALF_SMILEY_SIZE = SMILEY_SIZE/2
PROCREATION_THRESHOLD = 5*PLANT_ENERGY
INITIAL_ENERGY = 4*PLANT_ENERGY # Initial energy at the start for the smiley not to die immediately

# Zombie
NEW_ZOMBIE_HEALTH = 120

# Smilies & Zombies
PLACEMENT_GAP = 2.5

# Misc
SPEED_RATIO = 100 # Multiplying the speed by SPEED_RATIO to make it more readable
EXTENSION = 1.2 # Adding some void space to images to make it easier to click them