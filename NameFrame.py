import tkinter as tk
from FileDescriptorWindowConstants import *
from EntryFrame import *
from file_descriptor import FileDescriptorWindow


class NameFrame:
    def __init__(self, id_, parent: FileDescriptorWindow):
        self.__id = str(id_)

        self.__parent = parent

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
        if name != "Name" and name != "":
            return False
        for frame in self.__tags_frames:
            if not frame.is_empty():
                return False
        for frame in self.__ext_frames:
            if not frame.is_empty():
                return False

        return True

    def initialize(self, parent, row=0, col=0):
        self.__frame = tk.Frame(parent, name=NAME_FRAME + self.__id)

        self.__frame.grid(row=row, column=col, pady=2)

        # 2.1 Name Controls Frame
        name_controls_frame = tk.Frame(self.__frame, name=NAMES_CONTROL_FRAME)
        name_controls_frame.grid(row=0, pady=2)

        prev_name_button = tk.Button(name_controls_frame, name=PREV_BUTTON,
                                     text=PREV_BUTTON_TEXT,
                                     state=tk.DISABLED if self.__id < str(1) else tk.NORMAL)
        prev_name_button.bind(LEFT_CLICK, self.__parent.prev_name_click)
        prev_name_button.grid(row=0, column=0, padx=2, sticky=tk.W)

        name_entry = tk.Entry(name_controls_frame, name=NAME_ENTRY)
        name_entry.insert(0, "Name")
        name_entry.bind(LEFT_CLICK, lambda event: name_entry.delete(0, tk.END))
        name_entry.grid(row=0, column=1, padx=2)

        next_name_button = tk.Button(name_controls_frame, name=NEXT_BUTTON,
                                     text=NEXT_BUTTON_TEXT)
        next_name_button.bind(LEFT_CLICK, self.__parent.next_name_click)
        next_name_button.grid(row=0, column=2, padx=2, sticky=tk.E)

        self.__create_tag_frame()
        self.__create_ext_frame()

    def next_tag_click(self, event):
        pass


    def prev_tag_click(self, event):
        pass

    def __create_tag_frame(self):
        tag_frame = EntryFrame(self.__tags_next_id, self)
        self.__tags_next_id += 1

        tag_frame.initialize(self.__frame, "Tags", 5, 2, row=1, page_num=self.__tags_num_pages,
                             prev_function=self.prev_tag_click, next_function=self.next_tag_click)
        self.__tags_num_pages += 1
        self.__tags_frames.append(tag_frame)

    def __create_ext_frame(self):
        ext_frame = EntryFrame(self.__ext_next_id, self)
        self.__ext_next_id += 1

        ext_frame.initialize(self.__frame, "Extensions", 3, 2, row=2, page_num=self.__ext_num_pages)
        self.__ext_num_pages += 1
        self.__ext_frames.append(ext_frame)

    def hide(self):
        self.__frame.grid_remove()

    def show(self):
        self.__frame.grid()

    def destroy(self):
        self.__frame.destroy()
