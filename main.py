from tkinter import FLAT, LEFT, RIGHT, TOP, Canvas, Frame, PhotoImage, StringVar, Label, LabelFrame, Scale
from tkinter.ttk import OptionMenu, Button
from tkinter.font import Font

from config import *
from images import LOGO
from help_maintenance import show_help
from evolution import evolution
from smilies_functions import calculate_data_for_smilies
from zombie_boss import recreating_zombie_boss, calculate_data_for_zombie_boss
from tips import tips_for_evolution, stop_tips_timer
from global_items import smilies_data, scales, delete_help_window, window_commands, window, evolution_field, evolution_status
from draw_non_creatures import display_stimulus, init_stimulus_time
from special_window_functions import cancel_blink, mouse_wheel, switch_scales, start_pause_request
import global_items

def window_handling(): # Creating and handling the window
    '''Creating the window'''
    window.title(TITLE)
    window.iconphoto(True, PhotoImage(data=LOGO))
    window.attributes('-fullscreen', True)

    # Tacking functions to buttons
    window.bind('<Button-1>', delete_help_window)
    window.bind('<Button-2>', delete_help_window)
    window.bind('<Button-3>', delete_help_window)

    window.bind('<Button-2>', switch_scales, add='+')
    window.bind('<MouseWheel>', mouse_wheel)

    # Fetching the size of the window
    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    # Creating the top frame in which the evolution field and the zombie boss control panel are located
    (top_frame := Frame()).pack()

    # Creating the canvas for the evolution field
    BOTTOM_CONTROLS_AREA_SIZE = 68
    RIGHT_CONTROLS_AREA_SIZE = 105
    INDENTATION = 10
    evolution_field['width'] = window_width-RIGHT_CONTROLS_AREA_SIZE-INDENTATION*2
    evolution_field['height'] = window_height-BOTTOM_CONTROLS_AREA_SIZE
    evolution_field['diagonal'] = (evolution_field['width']**2+evolution_field['height']**2)**.5

    global_items.canvas = Canvas(
        master=top_frame,
        width=evolution_field['width'],
        height=evolution_field['height'],
        bd=0, # Canvas outline width
        relief=FLAT # Appearence of the outline of canvas
    )
    global_items.canvas.pack(side=LEFT, padx=INDENTATION, pady=INDENTATION)

    # Tacking functions to buttons
    global_items.canvas.bind('<Button-3>', start_pause_request)
    global_items.canvas_after_id = global_items.canvas.after(0, display_stimulus)

    # Calculating data for the smilies and the zombie boss
    calculate_data_for_smilies()
    calculate_data_for_zombie_boss()

    # Creating a frame for controlling the behaviour of the zombie boss
    global_items.user_control_frame = Frame(master=top_frame)
    global_items.user_control_frame.pack(side=TOP)

    # Creating a label which displays the energy of the zombie boss
    global_items.boss_health = StringVar()
    global_items.boss_health.set('Health:\n--')
    Label(
        master=global_items.user_control_frame,
        textvariable=global_items.boss_health,
        font=Font(size=20, font='Courier')
    ).pack(side=TOP, pady=10)

    # Creating a scale for controlling the speed
    Label(
        master=global_items.user_control_frame,
        text='Speed',
        font=Font(size=20, font='Courier')
    ).pack(side=TOP, pady=5)

    def change_zombie_boss_speed(value: str):
        evolution_status.zombie_boss.speed = int(value)/SPEED_RATIO

    scales['speed'] = Scale(
        master=global_items.user_control_frame,
        from_=round(smilies_data['average_speed']*SPEED_RATIO*3),
        to=round(smilies_data['average_speed']*SPEED_RATIO*0.1) ,
        length=200,
        sliderlength=0,
        showvalue=False,
        command=change_zombie_boss_speed
    )
    scales['speed'].pack(side=TOP)

    # Creating a scale for controlling the vision distance
    Label(
        master=global_items.user_control_frame,
        text='\nVision\ndistance',
        font=Font(size=20, font='Courier')
    ).pack(side=TOP, pady=5)

    def change_zombie_boss_vision_distance(value: str):
        evolution_status.zombie_boss.vision_distance = int(value)
        
    scales['vision distance'] = Scale(
        master=global_items.user_control_frame,
        from_=round(smilies_data['average_vision_distance']*5),
        to=SMILEY_SIZE,
        length=200,
        sliderlength=0,
        showvalue=False,
        command=change_zombie_boss_vision_distance
    )
    scales['vision distance'].pack(side=TOP)

    # Creating a label for tips
    global_items.tip_text = StringVar()
    global_items.tips_label = Label(textvariable=global_items.tip_text)
    global_items.tips_label.pack(side=LEFT, padx=5)

    # Creating a LabelFrame with a title describing what the menu can be used for
    (menu_frame := LabelFrame(
        bd=0,
        text='Which creature properties to display',
        labelanchor='n'
    )).pack(side=RIGHT, padx=5)

    # Creating an OptionMenu for selecting which properties have to be shown over the smilies
    def handle_selection(choice: str):
        window_commands['to-show-selected-property'] = choice

    menu_options = (
        'Nothing',
        '"Newly born" if newly born',
        'Energy/health',
        'Speed',
        'Vision distance',
        'Procreation threshold',
        'Food preference',
        'Generation number',
        'Amount of smilies with this species',
        'ID of the species'
    )

    selected = StringVar(value=menu_options[0])
    (properties_menu := OptionMenu(
        menu_frame,
        selected,
        menu_options[0],
        *menu_options,
        direction='right',
        command=handle_selection
    )).pack()
    properties_menu.configure(width=30)

    # Creating the help button
    Button(
        text='?',
        width=2,
        takefocus=False, 
        command=show_help
    ).pack(side=RIGHT, pady=8, padx=2)

    # Creating the new game button
    def new_game_request():
        window_commands['new-game'] = True

    global_items.new_game_button = Button(
        text='new game',
        width=10,
        takefocus=False,
        command=new_game_request
    )
    global_items.new_game_button.pack(side=RIGHT, pady=8, padx=2)

    # Creating the exit button
    Button(
        text='exit',
        width=5,
        takefocus=False,
        command=lambda: [
            global_items.canvas.after_cancel(global_items.canvas_after_id),
            stop_tips_timer(),
            cancel_blink(),
            window.destroy()
        ]).pack(side=RIGHT, pady=8, padx=2)

    # Creating the 'What a wonderful game!' button
    def wonderful_game_request():
        recreating_zombie_boss()
        init_stimulus_time()
        tips_for_evolution()
        global_items.wonderful_game_button.pack_forget()

    global_items.wonderful_game_button = Button(
        text=WHAT_A_WONDERFUL_GAME,
        width=23,
        takefocus=False,
        command=wonderful_game_request
    )

    # Starting the program
    window.after(0, evolution)
    window.mainloop()

if __name__ == '__main__':
    window_handling()