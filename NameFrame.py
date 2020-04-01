import tkinter as tk
from FileDescriptorWindowConstants import *


class NameFrame:
    def __init__(self, id_):
        self.__id = str(id_)

        self.__frame = None

        self.__tags_num_pages = 0
        self.__tags_current_page = 0
        self.__tags_next_id = 0
        self.__tags_frames = []

        self.__ext_num_pages = 0
        self.__ext_current_page = 0
        self.__ext_next_id = 0
        self.__ext_frames = []

    def is_empty(self):
        children = self.__frame.children
        name = children[NAMES_CONTROL_FRAME].children[NAME_ENTRY].get()
        if name != "Name":
            return False
        # for item in [children[key] for key in children if "name" not in key.lower()]:
        #     empty = FileDescriptorWindow.check_empty_entry_frame(item.children["entry_frame"])
        #     if not empty:
        #         return False

        return True

    def initialize(self, parent, row=0, col=0):
        self.__frame = tk.Frame(parent, name=NAME_FRAME + self.__id)
        
        self.__frame.grid(row=row, col=col, pady=2)

        # 2.1 Name Controls Frame
        name_controls_frame = tk.Frame(self.__frame, name=NAMES_CONTROL_FRAME)
        name_controls_frame.grid(row=0, pady=2)

        prev_name_button = tk.Button(name_controls_frame, name=PREV_BUTTON,
                                     text=PREV_BUTTON_TEXT,
                                     state=tk.DISABLED if self.__id < str(1) else tk.NORMAL)
        prev_name_button.bind(LEFT_CLICK, self.prev_name_click)
        prev_name_button.grid(row=0, column=0, padx=2, sticky=tk.W)

        name_entry = tk.Entry(name_controls_frame, name=NAME_ENTRY)
        name_entry.insert(0, "Name")
        name_entry.bind(LEFT_CLICK, lambda event: name_entry.delete(0, tk.END))
        name_entry.grid(row=0, column=1, padx=2)

        next_name_button = tk.Button(name_controls_frame, name=NEXT_BUTTON,
                                     text=NEXT_BUTTON_TEXT)
        next_name_button.bind(LEFT_CLICK, self.next_name_click)
        next_name_button.grid(row=0, column=2, padx=2, sticky=tk.E)
