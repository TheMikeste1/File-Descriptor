import tkinter as tk


class CPPInt:
    def __init__(self, value: int):
        self.value = value

    def plusplus(self):
        temp = self.value
        self.value += 1
        return temp


def create_input_frame(parent, name, position, rows, columns, page_num=0):
    frame = tk.Frame(parent, name=name.lower() + "_frame#" + str(page_num))
    frame.grid(row=position[0], column=position[1], pady=1)
    tk.Label(frame, text=name).grid(row=0, sticky=tk.W)

    entry_frame = tk.Frame(frame, name="entry_frame")
    entry_frame.grid(row=1, pady=1)
    entries = []
    for row in range(1, rows + 1):
        for col in range(columns):
            entry = tk.Entry(entry_frame, name="entry#" + str((row - 1) * columns + col))
            entry.grid(row=row, column=col, padx=7, pady=2)
            entries.append(entry)

    controls_frame = tk.Frame(frame, name="controls_frame")
    controls_frame.grid(row=2, pady=1)

    prev_button = tk.Button(controls_frame, name="prev_button", text="<<",
                            state=tk.DISABLED if page_num < 1 else tk.NORMAL)
    prev_button.grid(row=0, column=0, padx=2, sticky=tk.W)
    tk.Label(controls_frame, text=page_num, name="page_num").grid(row=0, column=1)
    next_button = tk.Button(controls_frame, name="next_button", text=">>")
    next_button.grid(row=0, column=2, padx=2, sticky=tk.E)

    return frame, entries


def initialize_window():
    row = CPPInt(0)

    # Initialize window
    window = tk.Tk(screenName="File Descriptor")
    window.title("File Descriptor")

    # 1. Directory Frame
    directory_frame = tk.Frame(window, name="directory_frame")
    directory_frame.grid(row=row.value, sticky=tk.W, pady=2)

    tk.Label(directory_frame, text="Directory:").grid(row=0)
    directory_entry = tk.Entry(directory_frame, name="directory_entry")
    directory_entry.grid(row=row.value, column=1, padx=2)
    directory_button = tk.Button(directory_frame, name="directory_button")
    directory_button.grid(row=row.plusplus(), column=2, padx=2, sticky=tk.E)

    # 2. Name Frame
    name_frame = tk.Frame(window, name="name_frame")
    name_frame.grid(row=row.plusplus(), pady=2)

    # 2.1 Name Controls Frame
    name_controls_frame = tk.Frame(name_frame, name="name_controls_frame")
    name_controls_frame.grid(row=0, pady=2)

    prev_name_button = tk.Button(name_controls_frame, name="prev_name_button", text="<<", state=tk.DISABLED)
    prev_name_button.grid(row=0, column=0, padx=2, sticky=tk.W)

    name_entry = tk.Entry(name_controls_frame, name="name_entry")
    name_entry.grid(row=0, column=1, padx=2)

    next_name_button = tk.Button(name_controls_frame, name="next_name_button", text=">>")
    next_name_button.grid(row=0, column=2, padx=2, sticky=tk.E)

    # 2.2 Tag Frame
    tag_frame, tag_entries = create_input_frame(name_frame, "Tags", (1, 0), 5, 2)

    # 2.3 Extension Frame
    ext_frame, ext_entries = create_input_frame(name_frame, "Extensions", (2, 0), 3, 2)

    # Go
    go_button = tk.Button(window, name="go_button", text="GO")
    go_button.grid(row=row.plusplus(), padx=2, pady=7)

    return window


def main():
    # Initialize window
    window = initialize_window()

    # Start GUI
    window.mainloop()


if __name__ == "__main__":
    # execute only if run as a script
    main()
