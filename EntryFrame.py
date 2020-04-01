import tkinter as tk

from FileDescriptorWindowConstants import *


class EntryFrame:
    def __init__(self, id_, parent):
        self.__id = str(id_)
        self.__parent = parent
        self.page_num = 0
        self.__frame = None

    def is_empty(self):
        entries = self.__frame.children["entry_frame"].children
        for entry in entries:
            if entries[entry].get() != "":
                return False
        return True

    def initialize(self, parent, name, num_rows, num_cols, row=0,
                   col=0, page_num=0, prev_function=None, next_function=None):
        self.__frame = tk.Frame(parent, name=name.lower() + "_frame#" + self.__id)
        self.__frame.grid(row=row, column=col, pady=1)
        tk.Label(self.__frame, text=name).grid(row=0, sticky=tk.W)

        entry_frame = tk.Frame(self.__frame, name="entry_frame")
        entry_frame.grid(row=1, pady=1)
        for row in range(1, num_rows + 1):
            for col in range(num_cols):
                entry = tk.Entry(entry_frame, name="entry#" + str((row - 1) * num_cols + col))
                entry.grid(row=row, column=col, padx=7, pady=2)

        controls_frame = tk.Frame(self.__frame, name="controls_frame")
        controls_frame.grid(row=2, pady=1)

        prev_button = tk.Button(controls_frame, name=PREV_BUTTON,
                                text=PREV_BUTTON_TEXT,
                                state=tk.DISABLED if page_num < 1 else tk.NORMAL)
        prev_button.bind(LEFT_CLICK, prev_function)
        prev_button.grid(row=0, column=0, padx=2, sticky=tk.W)

        tk.Label(controls_frame, text=page_num, name="page_num").grid(row=0, column=1)
        self.page_num = page_num

        next_button = tk.Button(controls_frame, name=NEXT_BUTTON,
                                text=NEXT_BUTTON_TEXT)
        prev_button.bind(LEFT_CLICK, next_function)
        next_button.grid(row=0, column=2, padx=2, sticky=tk.E)

    def get(self):
        return self.__frame

    def update_page_num(self, num):
        self.page_num = num
        if num > 0:
            self.__frame.children[PREV_BUTTON]["state"] = tk.NORMAL
        else:
            self.__frame.children[PREV_BUTTON]["state"] = tk.DISABLED
        self.__frame.children["page_num"].set(str(num))
