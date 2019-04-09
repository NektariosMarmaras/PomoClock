import os
import tkinter as tk
from tkinter import ttk

import pomoclock_logic


class PomoClockGui():
    def __init__(self):
        self.ptl = pomoclock_logic.PomoClockLogic(check_for_goal=True)
        self.sound_list = self.ptl.get_the_sounds_in_data_folder(
            self.ptl.get_data_folder_path())
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM)

        self.lbl_time = ttk.Label(
            self.top_frame, text="00:00", font=("Times New Roman", 16))
        self.lbl_time.pack(side=tk.TOP, padx=10, pady=5)

        self.b_radio = tk.IntVar()
        self.add_buttons(self.bottom_frame, self.lbl_time)
        self.add_menu(self.frame, self.root)
        self.win_hei = self.root.winfo_reqheight()
        self.win_wid = self.root.winfo_reqwidth()
        self.root.geometry("{0}x{1}".format(
            int(self.win_wid * 1.5), int(self.win_hei/2.5)))

        self.root.iconbitmap(os.path.join(
            self.ptl.get_data_folder_path(), 'pomo_icon.ico'))
        self.root.mainloop()

    def add_buttons(self, bot_fr, lbl):
        for c in range(2):
            if c == 0:
                ttk.Button(bot_fr, text="Start",
                           command=lambda: self.ptl.start_timer(self.root, self.lbl_time)).grid(
                               column=3, row=0, columnspan=3, padx=5, pady=5, sticky='NESW')
            elif c == 1:
                ttk.Button(bot_fr, text="Reset",
                           command=lambda: self.ptl.reset_timer(self.root, self.lbl_time)).grid(column=0, row=0, columnspan=3, padx=5, pady=5, sticky='NESW')

    def add_menu(self, win_fr, win_root):
        self.menu_bar = tk.Menu(win_fr)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.show_available_sounds(self.file_menu)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        win_root.config(menu=self.menu_bar)

    def show_available_sounds(self, filemenu):
        self.test_menu = tk.Menu(filemenu, tearoff=0)
        self.b_radio.set(len(self.sound_list) + 1)
        self.sel_sound = self.ptl.get_selected_sound()
        self.b_radio.set(self.sound_list.index(self.sel_sound))
        for i in range(len(self.sound_list)):
            self.s_name = os.path.splitext(self.sound_list[i])[0]
            self.test_menu.add_radiobutton(label=self.s_name.capitalize(), variable=self.b_radio, value=i, command=lambda: self.ptl.change_selected_sound_to(
                self.sound_list[self.b_radio.get()]))
        self.test_menu.add_command(
            label='Pick Another Sound', command=lambda: self.ptl.choose_another_sound())
        filemenu.add_cascade(label='Available Songs', menu=self.test_menu)