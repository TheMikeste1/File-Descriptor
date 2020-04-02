import os
import tkinter as tk
import xml.etree.ElementTree as Et
import calendar
import time

from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from NameFrame import NameFrame
from FileDescriptorWindowConstants import *

# TODO: Documentation and reorganize
VERSION = "0.5"


class FileDescriptorWindow:
    def __init__(self):
        self.__window = tk.Tk(screenName="File Descriptor")

        self.__directory_entry = None

        self.enable_load = tk.BooleanVar(value=True)

        self.__name_num_pages = 0
        self.__name_current_page = 0
        self.__name_next_id = 0
        self.__name_frames = []

    def initialize(self):
        DIR_FRAME_ROW = 0
        GO_ROW = 2

        # Initialize window
        self.__window.title("File Descriptor")

        # 1. Directory Frame
        directory_frame = tk.Frame(self.__window, name="directory_frame")
        directory_frame.grid(row=DIR_FRAME_ROW, sticky=tk.W, pady=2)

        tk.Label(directory_frame, text="Directory:").grid(row=0)

        self.__directory_entry = tk.Entry(directory_frame, name="directory_entry")
        self.__directory_entry.insert(0, "C:/")
        self.__directory_entry.grid(row=DIR_FRAME_ROW, column=1, padx=2)

        directory_button = tk.Button(directory_frame, name="directory_button", text="F", command=self.get_directory)
        directory_button.grid(row=DIR_FRAME_ROW, column=2, padx=2, sticky=tk.E)
        tk.Checkbutton(directory_frame, name="enable_load_checkbox", text="Load", variable=self.enable_load) \
            .grid(row=0, column=3)

        # 2. Name Frame
        self.__create_name_frame().show()

        # 3. Bottom Controls
        go_button = tk.Button(self.__window, name="go_button", text="GO", command=self.save)
        go_button.grid(row=GO_ROW, column=0, padx=2, pady=7)
        clear_button = tk.Button(self.__window, name="clear_button", text="CLEAR",
                                 command=self.reload)
        clear_button.grid(row=GO_ROW, column=1, padx=2, pady=7)

    def get_directory(self):
        directory = filedialog.askdirectory(initialdir="/", title="Select file")
        if directory == "":
            return
        self.__directory_entry.delete(0, tk.END)
        self.__directory_entry.insert(0, directory)

        if self.enable_load.get():
            meta_exists = False
            for f in listdir(directory):
                if isfile(join(directory, f)) and f == "meta.xml":
                    meta_exists = True
                    break
            if meta_exists:
                self.load_meta(directory + "/")
            else:
                self.scan_directory(directory + "/")

    def purge(self):
        for frame in self.__name_frames:
            frame.destroy()
        self.__name_frames.clear()
        self.__name_num_pages = 0
        self.__name_current_page = 0
        self.__name_next_id = 0

    def reload(self):
        self.purge()
        self.__create_name_frame().show()

    def scan_directory(self, directory):
        self.purge()

        file_list = {}
        for path, subdirs, files in os.walk(directory):
            for file in files:
                split = file.split(".")
                name = ".".join(split[0:-1])
                ext = split[-1]
                if name in file_list:
                    file_list[name].append(ext)
                else:
                    file_list[name] = [ext]
        for file in file_list:
            name_frame = self.__create_name_frame()
            self.__name_num_pages += 1
            name_frame.set_text(file)
            name_frame.load_ext(file_list[file])
        self.__name_frames[0].show()
        self.__name_num_pages -= 1

    def load_meta(self, directory):
        self.purge()
        tree = Et.parse(directory + "meta.xml")
        meta = tree.getroot()

        for code in meta.findall("./code"):
            name_frame = self.__create_name_frame()
            self.__name_num_pages += 1
            name_frame.set_text(code.attrib["name"])
            tags = [tag.text for tag in code.findall("./tag")]
            name_frame.load_tags(tags)
            exts = [ext.text for ext in code.findall("./extension")]
            name_frame.load_ext(exts)
        self.__name_frames[0].show()
        self.__name_num_pages -= 1

    def save(self):
        directory = self.__directory_entry.get() + "/"
        meta_exists = False
        for f in listdir(directory):
            if isfile(join(directory, f)) and f == "meta.xml":
                meta_exists = True
                break
        if meta_exists:
            self.update(directory)
        else:
            self.create(directory)

    def create(self, directory):
        timestamp = str(calendar.timegm(time.gmtime()))

        meta = Et.Element("meta", timestamp=timestamp)
        for name in self.__name_frames:
            if name.is_empty():
                continue
            entry = name.get().children[CONTROL_FRAME].children[NAME_ENTRY]
            code = Et.SubElement(meta, "code", name=entry.get(), timestamp=timestamp)
            for tag_frame in name.get_tag_frames():
                entry_frame = tag_frame.get().children["entry_frame"]
                for entry_key in entry_frame.children:
                    entry = entry_frame.children[entry_key]
                    val = entry.get()
                    if val != "":
                        val = "_".join(val.split()).lower()
                        Et.SubElement(code, "tag").text = val
            for ext_frame in name.get_ext_frames():
                entry_frame = ext_frame.get().children["entry_frame"]
                for entry_key in entry_frame.children:
                    entry = entry_frame.children[entry_key]
                    val = entry.get()
                    if val != "":
                        if val[0] == ".":
                            val = val[1:]
                        Et.SubElement(code, "extension").text = val

        Et.ElementTree(meta).write(directory + "meta.xml")
        return

    def update(self, directory):
        # TODO: Make this actually work
        self.create(directory)

    def next_name_click(self):
        if self.__name_current_page == self.__name_num_pages:
            self.__name_num_pages += 1
            self.__create_name_frame()
        self.__name_frames[self.__name_current_page].hide()
        self.__name_current_page += 1
        self.__name_frames[self.__name_current_page].show()

    def prev_name_click(self):
        if self.__name_current_page <= 0:
            return
        name_frame = self.__name_frames[self.__name_current_page]
        should_destroy = name_frame.is_empty()

        if should_destroy:
            self.__name_frames[self.__name_current_page].destroy()
            self.__name_frames.pop(self.__name_current_page)
            for i in range(self.__name_current_page, self.__name_num_pages):
                self.__name_frames[i].update_page_num(i)
            self.__name_num_pages -= 1
        else:
            self.__name_frames[self.__name_current_page].hide()

        self.__name_current_page -= 1
        self.__name_frames[self.__name_current_page].show()

    def __create_name_frame(self):
        name_frame = NameFrame(self.__name_next_id, self)
        self.__name_next_id += 1

        name_frame.initialize(self.__window, page_num=self.__name_num_pages, row=1,
                              prev_function=self.prev_name_click, next_function=self.next_name_click)
        name_frame.hide()

        self.__name_frames.append(name_frame)
        return name_frame

    def start(self):
        try:
            self.__window.mainloop()
        except AttributeError:
            raise RuntimeError("Unable to start main loop! Make sure to initialize first!") from None


if __name__ == "__main__":
    # execute only if run as a script
    window = FileDescriptorWindow()
    # Initialize window
    window.initialize()

    # Start GUI
    window.start()
