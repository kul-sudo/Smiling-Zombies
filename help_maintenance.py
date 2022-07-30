from tkinter import Toplevel, Button, DISABLED, WORD, INSERT
from tkinter.scrolledtext import ScrolledText

from config import *
from help_text import HELP_TEXT
from global_items import delete_help_window

import global_items

GEOMETRY_RATIO = 0.7
POPULATED_ROOM = 80 # Room populated by the bottom items of the help window (defined experimentally)
HELP_SCROLLED_TEXT_FONT_SIZE = 10 # The initial height of the letters in points
SCROLLED_TEXT_FONT_SIZE_IN_PIXELS = HELP_SCROLLED_TEXT_FONT_SIZE*1.3333 # Retrieving the text with its size being transformed from points into pixels (1.333 must not be changed)
SCROLLED_FONT_SIZE_GAP_HEIGHT = SCROLLED_TEXT_FONT_SIZE_IN_PIXELS*1.13 # Retrieving the height of lines (the factor must not be changed)
LETTER_WIDTH = SCROLLED_TEXT_FONT_SIZE_IN_PIXELS/2 # Retrieving the width of letters (the divisior must not be changed)
TEXT_COLOR = '#ffffff'
HELP_WINDOW_BG = '#303030'

def show_help():
    # Creating the help window

    global_items.help_window = Toplevel(takefocus=True)
    global_items.help_window.attributes('-topmost', True)
    global_items.help_window.overrideredirect(True)
    global_items.help_window.resizable(width=False, height=False)
    global_items.help_window['bg'] = HELP_WINDOW_BG
    global_items.help_window.geometry(f'{round(GEOMETRY_RATIO*global_items.help_window.winfo_screenwidth())}x{round(GEOMETRY_RATIO*global_items.help_window.winfo_screenheight())}') # Setting the window geometry according to the size of the screen
    global_items.help_window.update() # If this update is not done, nothing further works
    global_items.help_window.title(TITLE)

    #Centering a window on the screen.
    screen_width = global_items.help_window.winfo_screenwidth()
    screen_height = global_items.help_window.winfo_screenheight()
    window_width = global_items.help_window.winfo_width()
    window_height = global_items.help_window.winfo_height()
    x = round(screen_width/2 - window_width/2)
    y = round(screen_height/2 - window_height/2)
    global_items.help_window.geometry(f'+{x}+{y}')
    
    # Creating the window with ScrolledText
    txt = ScrolledText(
        master=global_items.help_window,
        height=int((global_items.help_window.winfo_height()-POPULATED_ROOM)/(SCROLLED_FONT_SIZE_GAP_HEIGHT)),
        foreground=TEXT_COLOR,
        bg=HELP_WINDOW_BG,
        borderwidth=0,
        width=int(global_items.help_window.winfo_width()/LETTER_WIDTH),
        font=('Arial', HELP_SCROLLED_TEXT_FONT_SIZE),
        wrap=WORD
    )

    txt.pack()
    txt.insert(INSERT, HELP_TEXT)
    txt.configure(state=DISABLED)

    Button(
        master=global_items.help_window, text='I have read the guideline',
        command=delete_help_window
    ).pack(pady=10)