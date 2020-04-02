import tkinter as tk

from FileDescriptorWindowConstants import *
from EntryFrame import EntryFrame


class NameFrame:
    def __init__(self, id_, parent):
        self.__id = str(id_)

        self.parent = parent

        self.__frame = None

        self.page_num = tk.StringVar()
        self.next_enabled = tk.StringVar(value=tk.NORMAL)
        self.prev_enabled = tk.StringVar(value=tk.DISABLED)

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
        name = children[CONTROL_FRAME].children[NAME_ENTRY].get()
        if name != "Name" and name != "":
            return False
        for frame in self.__tags_frames:
            if not frame.is_empty():
                return False
        for frame in self.__ext_frames:
            if not frame.is_empty():
                return False

        return True

    def initialize(self, parent, page_num=0, row=0, col=0, prev_function=None, next_function=None):
        self.__frame = tk.Frame(parent, name=NAME_FRAME + self.__id)

        self.__frame.grid(row=row, column=col, pady=2)

        # 2.1 Name Controls Frame
        controls_frame = tk.Frame(self.__frame, name=CONTROL_FRAME)
        controls_frame.grid(row=0, pady=2)

        self.page_num.set(page_num)
        tk.Label(controls_frame, textvariable=self.page_num, name="page_num").grid(row=0, column=0)

        prev_name_button = tk.Button(controls_frame, name=PREV_BUTTON,
                                     text=PREV_BUTTON_TEXT,
                                     state=tk.DISABLED if self.__id < str(1) else tk.NORMAL,
                                     command=prev_function)
        prev_name_button.grid(row=0, column=1, padx=2, sticky=tk.W)

        name_entry = tk.Entry(controls_frame, name=NAME_ENTRY)
        name_entry.insert(0, "Name")
        name_entry.bind(LEFT_CLICK, lambda event: name_entry.delete(0, tk.END))
        name_entry.grid(row=0, column=2, padx=2)

        next_name_button = tk.Button(controls_frame, name=NEXT_BUTTON,
                                     text=NEXT_BUTTON_TEXT,
                                     command=next_function)
        next_name_button.grid(row=0, column=3, padx=2, sticky=tk.E)

        self.__create_tag_frame()
        self.__create_ext_frame()

    def next_tag_click(self):
        if self.__tags_current_page == self.__tags_num_pages:
            self.__tags_num_pages += 1
            self.__create_tag_frame()
        self.__tags_frames[self.__tags_current_page].hide()
        self.__tags_current_page += 1
        self.__tags_frames[self.__tags_current_page].show()

    def prev_tag_click(self):
        if self.__tags_current_page <= 0:
            return
        entry_frame = self.__tags_frames[self.__tags_current_page]
        should_destroy = entry_frame.is_empty()

        if should_destroy:
            self.__tags_frames[self.__tags_current_page].destroy()
            self.__tags_frames.pop(self.__tags_current_page)
            for i in range(self.__tags_current_page, self.__tags_num_pages):
                self.__tags_frames[i].update_page_num(i)
            self.__tags_num_pages -= 1
        else:
            self.__tags_frames[self.__tags_current_page].hide()

        self.__tags_current_page -= 1
        self.__tags_frames[self.__tags_current_page].show()

    def next_ext_click(self):
        if self.__ext_current_page == self.__ext_num_pages:
            self.__ext_num_pages += 1
            self.__create_ext_frame()
        self.__ext_frames[self.__ext_current_page].hide()
        self.__ext_current_page += 1
        self.__ext_frames[self.__ext_current_page].show()

    def prev_ext_click(self):
        if self.__ext_current_page <= 0:
            return
        entry_frame = self.__ext_frames[self.__ext_current_page]
        should_destroy = entry_frame.is_empty()

        if should_destroy:
            self.__ext_frames[self.__ext_current_page].destroy()
            self.__ext_frames.pop(self.__ext_current_page)
            for i in range(self.__ext_current_page, self.__ext_num_pages):
                self.__ext_frames[i].update_page_num(i)
            self.__ext_num_pages -= 1
        else:
            self.__ext_frames[self.__ext_current_page].hide()

        self.__ext_current_page -= 1
        self.__ext_frames[self.__ext_current_page].show()

    def __create_tag_frame(self):
        tag_frame = EntryFrame(self.__tags_next_id, self)
        self.__tags_next_id += 1

        tag_frame.initialize(self.__frame, "Tags", 5, 2, row=1, page_num=self.__tags_num_pages,
                             prev_function=self.prev_tag_click, next_function=self.next_tag_click)
        self.__tags_frames.append(tag_frame)

    def __create_ext_frame(self):
        ext_frame = EntryFrame(self.__ext_next_id, self)
        self.__ext_next_id += 1

        ext_frame.initialize(self.__frame, "Extensions", 3, 2, row=2, page_num=self.__ext_num_pages,
                             prev_function=self.prev_ext_click, next_function=self.next_ext_click)
        self.__ext_frames.append(ext_frame)

    def hide(self):
        self.__frame.grid_remove()

    def show(self):
        self.__frame.grid()

    def destroy(self):
        self.__frame.destroy()

    def get(self):
        return self.__frame

    def get_tag_frames(self):
        return self.__tags_frames

    def get_ext_frames(self):
        return self.__ext_frames

    def update_page_num(self, num):
        self.page_num.set(num)
        control_frame = self.__frame.children[CONTROL_FRAME]
        if num > 0:
            control_frame.children[PREV_BUTTON]["state"] = tk.NORMAL
        else:
            control_frame.children[PREV_BUTTON]["state"] = tk.DISABLED

    def load_tags(self, tags):
        self.purge_tags()
        for tag_i in range(len(tags)):
            text = tags[tag_i]
            if tag_i % 10 == 0:
                self.__create_tag_frame()
                entry_frame = self.__tags_frames[tag_i // 10].get().children["entry_frame"]
                keys = list(entry_frame.children.keys())
            entry_frame.children[keys[tag_i % 10]].insert(0, text)
            
    def load_ext(self, exts):
        self.purge_ext()
        for tag_i in range(len(exts)):
            text = exts[tag_i]
            if text[0] == ".":
                text = text[1:]
            if tag_i % 6 == 0:
                self.__create_ext_frame()
                entry_frame = self.__ext_frames[tag_i // 6].get().children["entry_frame"]
                keys = list(entry_frame.children.keys())
            entry_frame.children[keys[tag_i % 6]].insert(0, text)

    def set_text(self, text):
        name_entry = self.__frame.children[CONTROL_FRAME].children[NAME_ENTRY]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, text)

    def purge(self):
        self.purge_tags()
        self.purge_ext()

        self.page_num = tk.StringVar()
        self.next_enabled = tk.StringVar(value=tk.NORMAL)
        self.prev_enabled = tk.StringVar(value=tk.DISABLED)

    def purge_tags(self):
        for frame in self.__tags_frames:
            frame.destroy()
        self.__tags_frames.clear()
        self.__tags_num_pages = 0
        self.__tags_current_page = 0
        self.__tags_next_id = 0

    def purge_ext(self):
        for frame in self.__ext_frames:
            frame.destroy()
        self.__ext_frames.clear()
        self.__ext_num_pages = 0
        self.__ext_current_page = 0
        self.__ext_next_id = 0
