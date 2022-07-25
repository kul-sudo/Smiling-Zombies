TEST_MODE = False
STRAIGHTFORWARD_FIX = True

from math import sqrt

# Common settings for windows
TITLE = 'Smiling Zombies'

# Window settings
FPS = 200

# Scale
SPEED_LABEL = 'Speed'
VISION_DISTANCE_LABEL = 'Vision\ndistance'

WHAT_A_WONDERFUL_GAME = 'What a wonderful game!'

SPEED = 0
VISION_DISTANCE = 1

RUN = 0
PAUSE = 1

# Help maintenance
GEOMETRY_RATIO = 0.7
POPULATED_ROOM = 80 # Room populated by the bottom items of the help window (defined experimentally)
HELP_SCROLLED_TEXT_FONT_SIZE = 10 # The initial height of the letters in points
SCROLLED_TEXT_FONT_SIZE_IN_PIXELS = HELP_SCROLLED_TEXT_FONT_SIZE*1.3333 # Retrieving the text with its size being transformed from points into pixels (1.333 must not be changed)
SCROLLED_FONT_SIZE_GAP_HEIGHT = SCROLLED_TEXT_FONT_SIZE_IN_PIXELS*1.13 # Retrieving the height of lines (the factor must not be changed)
LETTER_WIDTH = SCROLLED_TEXT_FONT_SIZE_IN_PIXELS/2 # Retrieving the width of letters (the divisior must not be changed)
TEXT_COLOR = '#ffffff'
HELP_WINDOW_BG = '#303030'

# Bodies
# Shapes
BODY_SIZE = 14 if STRAIGHTFORWARD_FIX else 10
OLD_VISION_DISTANCE = 75 # A satisfying value for the size of the evolution field being {'width': 950, 'height': 500}
DOUBLE_BODY_SIZE = BODY_SIZE*2

NEWLY_BORN_PERIOD = 4 # In seconds

CIRCLE = 0
SQUARE = 1
RHOMBUS = 2

# Rhombus shape
RHOMBUS_SIZE = BODY_SIZE*1.4
HALF_RHOMBUS_SIZE = RHOMBUS_SIZE/2

# Food preference
BODY = 'bodies'
PLANT = 'plants'

# Status
SLEEPING = 0
RUNNING_AWAY = 1
FOLLOWING_PLANT = 2
FOLLOWING_BODY = 3

CONTROL_PREPARATION = 0
DELETE_EVERYTHING = 1
EVOLUTION_PREPARATION = 2
EVOLUTION = 3
USER_SELECTING_BODY = 4
PAUSED = 5

FROM = 0
TO = 1

# Tips
PAUSE_RESUME = 'Use your right mouse button in order to pause/resume the evolution.'

# Related to plants
PLANT_ENERGY = 100
PLANT_PREFERENCE_CHANCE = 0.5 # The chance that the body will prefer eating plant
PROCREATION_THRESHOLD = 5*PLANT_ENERGY
USER_BODY_PLANT_GAP = BODY_SIZE*0.9

# Zombie boss
ZOMBIE_PLANT_HEALTH_LOSS = 30
BOSS_PLANT_HEALTH_LOSS = 60

VISION_DISTANCE_LOSS_1680_1050 = PLANT_ENERGY*0.000012
SPEED_LOSS_1680_1050 = PLANT_ENERGY*0.002

NEW_ZOMBIE_HEALTH = 120

# Related to other bodies
USER_BODY_BODY_GAP = BODY_SIZE*0.7

# Appearance
HALF_BODY_SIZE = BODY_SIZE/2
MAXIMUM_COLOUR = 220
MAX_COLOUR_DISTANCE = sqrt(3*MAXIMUM_COLOUR**2) # This is the maximum of sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

# First generation
PLANT_ENERGY = 100 # Energy to a body for eating a plant
INITIAL_ENERGY = 4*PLANT_ENERGY # Initial energy at the start for the body not to die immediately

# Procreating
FOOD_PREFERENCE_CHANCE_CHILD = 0.9 # The chance that the child will inherit the food preference of the parent
DEVIATION_OF_RANDOM_PROPERTIES = 0.1 # Proportionates to standard deviation
DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION = 0.4 # Proportionates to standard deviation for the zero generation
PLACEMENT_GAP = 2.5

OLD_BODY_SPEED = 0.6 # A satisfying value for the size of the evolution field being {'width': 950, 'height': 500}
BODIES_AMOUNT = 20 if TEST_MODE is False else 2 # Amount of bodies on the window
OLD_ENERGY_FOR_VISION = 0.00007*PLANT_ENERGY if TEST_MODE is False else 0.01 # A satisfying value for the size of the evolution field being {'width': 950, 'height': 500}
OLD_ENERGY_FOR_MOVING = 0.007*PLANT_ENERGY if TEST_MODE is False else 0.000000000001

# Canvas
BOTTOM_CONTROLS_AREA_SIZE = 68

RIGHT_CONTROLS_AREA_SIZE = 105
INDENTATION = 10

NOTHING_CLICKED = 0

# Plants
PLANT_COLOUR = (14, 209, 69) # Not defining the colour, but saying that the RGB of the plant is this one
TIMES_ATTEMPTED = 1000 # Limit of times for trying to place a plant on the window
PLANT_SIZE_RATIO = 25 # Higher => smaller
PLANT_CHANCE = 0.2 if TEST_MODE is False else 0 # The chance (percent = PLANT_CHANCE * 100) of Plant emerging
INITIALLY_PLANTED = BODIES_AMOUNT*3 if TEST_MODE is False else 100 # Amount of plants that have to be planted initially

# Crosses
CROSS_LIFETIME = 3 # Lifetime of a cross

# Cross appearance
CROSS_SIZE_RATIO = 3 # Higher => smaller

# Display results
RATIO = 100 # Making the results that are displayed more readable
NO_CREATURES = 0
SQUARES_ONE_SPECIES_WON = 1
ALL_ZOMBIES = 2
ONLY_ZOMBIE_BOSS = 3

# Other
DELTA = 0.1 # Window update every DELTA seconds

if STRAIGHTFORWARD_FIX:
    ZOMBIE_BOSS_SIZE_RATIO = 27 # Higher => smaller
    ZOMBIE_SIZE_RATIO = 30 # Higher => smaller