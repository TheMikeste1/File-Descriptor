import tkinter as tk


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
        self.__name_frames = []

        self.__tags_num_pages = 0
        self.__tags_current_page = 0
        self.__tags_frames = []

        self.__ext_num_pages = 0
        self.__ext_current_page = 0
        self.__ext_frames = []

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
        self.__directory_entry.bind("<Button-1>", lambda event: self.__directory_entry.delete(0, tk.END))
        self.__directory_entry.grid(row=DIR_FRAME_ROW, column=1, padx=2)

        directory_button = tk.Button(directory_frame, name="directory_button")
        directory_button.grid(row=DIR_FRAME_ROW, column=2, padx=2, sticky=tk.E)

        # 2. Name Frame
        self.__create_name_frame(0)

        # 3. Go
        go_button = tk.Button(self.__window, name="go_button", text="GO")
        go_button.grid(row=GO_ROW, padx=2, pady=7)

    def __next_name_click(self, event):
        if self.__name_current_page == self.__name_num_pages:
            self.__name_current_page += 1
            self.__create_name_frame(self.__name_current_page)
            self.__name_num_pages += 1

    def __create_name_frame(self, number):
        NAME_FRAME_ROW = 1

        name_frame = tk.Frame(self.__window, name="name_frame#" + str(number))
        name_frame.grid(row=NAME_FRAME_ROW, pady=2)

        # 2.1 Name Controls Frame
        name_controls_frame = tk.Frame(name_frame, name="name_controls_frame")
        name_controls_frame.grid(row=0, pady=2)

        prev_name_button = tk.Button(name_controls_frame, name="prev_name_button", text="<<",
                                     state=tk.DISABLED if self.__name_current_page < 1 else tk.NORMAL)
        prev_name_button.grid(row=0, column=0, padx=2, sticky=tk.W)

        name_entry = tk.Entry(name_controls_frame, name="name_entry")
        name_entry.insert(0, "Name" + str(number))
        name_entry.bind("<Button-1>", lambda event: name_entry.delete(0, tk.END))
        name_entry.grid(row=0, column=1, padx=2)

        next_name_button = tk.Button(name_controls_frame, name="next_name_button", text=">>")
        next_name_button.bind("<Button-1>", self.__next_name_click)
        next_name_button.grid(row=0, column=2, padx=2, sticky=tk.E)

        # 2.2 Tag Frame
        tag_frame = self.__create_input_frame(name_frame, "Tags", (1, 0), 5, 2)
        self.__tags_frames.append([])
        self.__tags_frames[self.__name_current_page].append(tag_frame)

        # 2.3 Extension Frame
        ext_frame = self.__create_input_frame(name_frame, "Extensions", (2, 0), 3, 2)
        self.__ext_frames.append([])
        self.__ext_frames[self.__name_current_page].append(ext_frame)

        self.__name_frames.append(name_frame)

    @staticmethod
    def __create_input_frame(parent, name, position, rows, columns, page_num=0):
        frame = tk.Frame(parent, name=name.lower() + "_frame#" + str(page_num))
        frame.grid(row=position[0], column=position[1], pady=1)
        tk.Label(frame, text=name).grid(row=0, sticky=tk.W)

        entry_frame = tk.Frame(frame, name="entry_frame")
        entry_frame.grid(row=1, pady=1)
        for row in range(1, rows + 1):
            for col in range(columns):
                entry = tk.Entry(entry_frame, name="entry#" + str((row - 1) * columns + col))
                entry.grid(row=row, column=col, padx=7, pady=2)

        controls_frame = tk.Frame(frame, name="controls_frame")
        controls_frame.grid(row=2, pady=1)

        prev_button = tk.Button(controls_frame, name="prev_button", text="<<",
                                state=tk.DISABLED if page_num < 1 else tk.NORMAL)
        prev_button.grid(row=0, column=0, padx=2, sticky=tk.W)
        tk.Label(controls_frame, text=page_num, name="page_num").grid(row=0, column=1)
        next_button = tk.Button(controls_frame, name="next_button", text=">>")
        next_button.grid(row=0, column=2, padx=2, sticky=tk.E)

        return frame

    def start(self):
        error = False
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
