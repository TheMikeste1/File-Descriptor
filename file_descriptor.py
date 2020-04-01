import tkinter as tk
import NameFrame
from FileDescriptorWindowConstants import *

class CPPInt:
    def __init__(self, value: int):
        self.value = value

    def plusplus(self):
        temp = self.value
        self.value += 1
        return temp

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
        self.__directory_entry.bind(self.LEFT_CLICK, lambda event: self.__directory_entry.delete(0, tk.END))
        self.__directory_entry.grid(row=DIR_FRAME_ROW, column=1, padx=2)

        directory_button = tk.Button(directory_frame, name="directory_button")
        directory_button.grid(row=DIR_FRAME_ROW, column=2, padx=2, sticky=tk.E)

        # 2. Name Frame
        self.__create_name_frame(0)

        # 3. Go
        go_button = tk.Button(self.__window, name="go_button", text="GO")
        go_button.grid(row=GO_ROW, padx=2, pady=7)

    def next_name_click(self, event):
        if event.widget["state"] == tk.DISABLED:
            return
        if self.__name_current_page == self.__name_num_pages:
            self.__name_num_pages += 1
            self.__create_name_frame(self.__name_num_pages)
        self.__name_frames[self.__name_current_page].grid_remove()
        self.__name_current_page += 1
        self.__name_frames[self.__name_current_page].grid()

    def prev_name_click(self, event):
        if self.__name_current_page <= 0 or event.widget["state"] == tk.DISABLED:
            return
        name_frame = self.__name_frames[self.__name_current_page]
        should_destroy = self.check_empty_name_frame(name_frame)

        if should_destroy:
            self.__name_frames[self.__name_current_page].destroy()
            self.__name_frames.pop(self.__name_current_page)
            self.__name_num_pages -= 1
        else:
            self.__name_frames[self.__name_current_page].grid_remove()

        self.__name_current_page -= 1
        self.__name_frames[self.__name_current_page].grid()


    def __create_name_frame(self, number):
        NAME_FRAME_ROW = 1
        self.__name_next_id += 1
        # 2.2 Tag Frame
        tag_frame = self.__create_input_frame(name_frame, "Tags", (1, 0), 5, 2)
        self.__tags_frames.append([])
        self.__tags_frames[self.__name_current_page].append(tag_frame)

        # 2.3 Extension Frame
        ext_frame = self.__create_input_frame(name_frame, "Extensions", (2, 0), 3, 2)
        self.__ext_frames.append([])
        self.__ext_frames[self.__name_current_page].append(ext_frame)

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
