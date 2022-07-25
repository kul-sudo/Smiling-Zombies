from tkinter import Toplevel, Button, DISABLED, WORD, INSERT
from tkinter.scrolledtext import ScrolledText

from config import *
from help_text import HELP_TEXT
from global_items import center_window, delete_help

import global_items

def show_help():
    # Creating the help window

    global_items.help_window = Toplevel(takefocus=True)
    global_items.help_window.attributes('-topmost', True)
    global_items.help_window.overrideredirect(True)
    global_items.help_window.resizable(width=False, height=False)
    global_items.help_window['bg'] = HELP_WINDOW_BG
    global_items.help_window.geometry(f'{round(GEOMETRY_RATIO*global_items.help_window.winfo_screenwidth())}x{round(GEOMETRY_RATIO*global_items.help_window.winfo_screenheight())}') # Setting the window geometry according to the size of the screen
    global_items.help_window.update() # If this update is not done, nothing further works
    center_window(global_items.help_window)
    global_items.help_window.title(TITLE)
    
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
        command=delete_help
    ).pack(pady=10)