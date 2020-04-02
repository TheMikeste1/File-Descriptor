import tkinter as tk

from tkinter import filedialog
from NameFrame import NameFrame
from FileDescriptorWindowConstants import *


class FileDescriptorWindow:

    def __init__(self):
        self.__window = None

        self.__directory_entry = None

        self.__name_num_pages = 0
        self.__name_current_page = 0
        self.__name_next_id = 0
        self.__name_frames = []

    def initialize(self):
        DIR_FRAME_ROW = 0
        GO_ROW = 2

        # Initialize window
        self.__window = tk.Tk(screenName="File Descriptor")
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

        # 2. Name Frame
        self.__create_name_frame()

        # 3. Go
        go_button = tk.Button(self.__window, name="go_button", text="GO")
        go_button.grid(row=GO_ROW, padx=2, pady=7)

    def get_directory(self):
        directory = filedialog.askdirectory(initialdir="/", title="Select file")
        self.__directory_entry.delete(0, tk.END)
        self.__directory_entry.insert(0, directory)

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

        self.__name_frames.append(name_frame)

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
