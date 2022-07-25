from tkinter import FLAT, LEFT, RIGHT, TOP, Canvas, Frame, PhotoImage, StringVar, Label, LabelFrame, Scale, Toplevel
from tkinter.ttk import OptionMenu, Button
from tkinter.font import Font

from config import *
from images import LOGO
from help_maintenance import show_help
from evolution import evolution
from bodies_functions import calculate_data_for_body, create_new_boss
from tips import prepare_tips
from zombies import calculate_data_for_zombie_boss
from global_items import start_pause_request, switch_scales, mouse_wheel, delete_help, window_commands, window, evolution_field, evolution_status
from draw_erase import display_stimulus, init_stimulus_time
import global_items

def window_handling(): # Creating and handling the window
    # Creating the window
    window.title(TITLE)
    window.iconphoto(True, PhotoImage(data=LOGO))
    window.attributes('-fullscreen', True)
    window.bind('<Button-1>', delete_help)
    window.bind('<Button-2>', delete_help)

    # add='+' means that another bind is tacked
    window.bind('<Button-2>', switch_scales, add='+')

    window.bind('<Button-3>', delete_help)
    window.bind('<MouseWheel>', mouse_wheel)

    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    # Creating top_frame
    (top_frame := Frame()).pack()
     
    # Creating canvas

    evolution_field['width'] = window_width-RIGHT_CONTROLS_AREA_SIZE-INDENTATION*2
    evolution_field['height'] = window_height-BOTTOM_CONTROLS_AREA_SIZE

    calculate_data_for_body()
    calculate_data_for_zombie_boss()

    global_items.canvas = Canvas(
        master=top_frame,
        width=evolution_field['width'],
        height=evolution_field['height'],
        bd=0, # Canvas outline width
        relief=FLAT # Appearence of the outline of canvas
    )

    global_items.canvas.pack(side=LEFT, padx=INDENTATION, pady=INDENTATION)
    global_items.canvas.bind('<Button-3>', start_pause_request)

    global_items.canvas_after_id = global_items.canvas.after(0, display_stimulus)

    # Creating a frame for controlling the behaviour of the body
    global_items.user_control_frame = Frame(master=top_frame)
    global_items.user_control_frame.pack(side=TOP)

    # Creating a label which displays the energy of the zombie boss
    global_items.health_to_display = StringVar()
    global_items.health_to_display.set('Health:\n--')
    Label(
        master=global_items.user_control_frame,
        textvariable=global_items.health_to_display,
        font=Font(size=20, font='Courier')
    ).pack(side=TOP, pady=10)

    # Creating a scale for controlling the speed
    Label(
        master=global_items.user_control_frame,
        text=SPEED_LABEL,
        font=Font(size=20, font='Courier')
    ).pack(side=TOP, pady=5)

    def change_zombie_boss_speed(value: str):
        '''Changing the speed of the circle-shaped zombie boss to the value of the corresponding scale.'''
        evolution_status.zombie_boss.speed = int(value)/RATIO

    global_items.user_selected_body_speed = Scale(
        master=global_items.user_control_frame,
        from_=round(global_items.average_body_speed*RATIO*3),
        to=round(global_items.average_body_speed*RATIO*0.1) ,
        length=200,
        sliderlength=0,
        showvalue=False,
        command=change_zombie_boss_speed
    )
    global_items.user_selected_body_speed.pack(side=TOP)

    # Goofy fix
    Label(master=global_items.user_control_frame, text=' ').pack()

    # Creating a scale for controlling the vision distance
    Label(
        master=global_items.user_control_frame,
        text=VISION_DISTANCE_LABEL,
        font=Font(size=20, font='Courier')
    ).pack(side=TOP, pady=5)

    def change_zombie_boss_vision_distance(value: str):
        '''Changing the vision distance of the circle-shaped zombie boss to the value of the corresponding scale.'''
        evolution_status.zombie_boss.vision_distance = int(value)
        
    global_items.user_selected_vision_distance = Scale(
        master=global_items.user_control_frame,
        from_=round(global_items.average_body_vision_distance*5),
        to=BODY_SIZE,
        length=200,
        sliderlength=0,
        showvalue=False,
        command=change_zombie_boss_vision_distance
    )
    global_items.user_selected_vision_distance.pack(side=TOP)

    # Creating a label for tips
    global_items.tip_text = StringVar()
    Label(textvariable=global_items.tip_text).pack(side=LEFT, padx=5)

    # Creating a LabelFrame with a title describing what the menu can be used for
    (menu_frame := LabelFrame(
        bd=0,
        text='Which creature properties to display',
        labelanchor='n'
    )).pack(side=RIGHT, padx=5)

    # Creating a OptionMenu for selecting which properties have to be shown over the bodies
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
        'Amount of bodies with this species',
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
    exit_button = Button(
        text='exit',
        width=5,
        takefocus=False,
        command=lambda: [global_items.canvas.after_cancel(global_items.canvas_after_id), window.destroy()]
    )
    exit_button.pack(side=RIGHT, pady=8, padx=2)

    # Creating the 'What a wonderful game!' button
    def wonderful_game_request():
        create_new_boss()
        init_stimulus_time()
        prepare_tips()
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

window_handling()