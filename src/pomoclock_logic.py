import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import playsound

seconds = int(0)
minutes = int(0)
goal_minutes = int(25)
dir_path = ''


class PomoClockLogic():
    def __init__(self, do_search=False, check_for_goal=False):
        global dir_path
        global goal_minutes
        self.selected_sound = 'chime.mp3'
        if do_search:
            dir_path = self.find_data_folder()
        if check_for_goal:
            self.entry_dialog_pop_up()
        if goal_minutes = 0:
            goal_minutes = 25
        self._job = None

    def start_timer(self, win_root, win_lbl):
        global seconds
        global minutes
        global goal_minutes
        if minutes < goal_minutes:
            if seconds > 59:
                seconds = 0
                minutes += 1
            seconds += 1
            str_min = str(minutes)
            str_sec = str(seconds)
            if minutes < 10:
                str_min = "0" + str(minutes)
            if seconds < 10:
                str_sec = "0" + str(seconds)
            txt = str_min + ":" + str_sec
            self._job = win_root.after(
                1000, lambda: self.start_timer(win_root, win_lbl))
            win_lbl.config(text=txt)
        else:
            self.reset_timer(win_root, win_lbl)
            self.play_sound(os.path.join(
                self.get_data_folder_path(), self.selected_sound))
            self.show_pop_up(
                "Congratulations", f"You have gone through {goal_minutes} minute(s) of studying without taking a break!!!")

    def reset_timer(self, app_root, app_lbl):
        global seconds
        global minutes
        if self._job is not None:
            app_root.after_cancel(self._job)
            self._job = None
            seconds = int(0)
            minutes = int(0)
        app_lbl.config(text="00:00")

    def play_sound(self, sel_song_path):
        try:
            playsound.playsound(sel_song_path)
        except NameError:
            self.show_pop_up(
                'NameError', "'playsound' module is either not installed in your system either not imported into the project.")
            sys.exit("'playsound' module is not installed in your system.")

    def show_pop_up(self, title='No Title', msg='No Message', isError=False):
        if isError:
            messagebox.showerror(title, msg)
        else:
            messagebox.showinfo(title, msg)
    
    def entry_dialog_pop_up(self):
        pop_up = tk.Tk()
        pop_up.title("Goal Minutes")
        fr = tk.Frame(pop_up)
        fr.pack()

        top_fr = tk.Frame(pop_up)
        top_fr.pack(side=tk.TOP)

        bottom_fr = tk.Frame(pop_up)
        bottom_fr.pack(side=tk.BOTTOM)

        lbl_msg = ttk.Label(top_fr, text=f"How long do you want\nyour pomodoro session to be?(Default={goal_minutes})", font=("Times New Roman", 15))
        lbl_msg.pack(side=tk.TOP, padx=10, pady=5)

        user_entry = tk.Entry(top_fr, bd=5)
        user_entry.pack(side=tk.BOTTOM)

        b_submit = ttk.Button(bottom_fr, text="Submit", command=lambda: self.set_goal_minutes(user_entry.get(), pop_up)).pack()
        pop_up.mainloop()
    
    def set_goal_minutes(self, entry_txt, entry_pop_up):
        global goal_minutes
        try:
            goal_minutes = int(entry_txt)
            if goal_minutes < 0:
                raise ValueError
            entry_pop_up.destroy()
        except ValueError:
            self.show_pop_up("Error", "Something went wrong with your given input... Try Again!", True)
            entry_pop_up.destroy()
            self.entry_dialog_pop_up()

    def find_data_folder(self):
        self.script_path = os.path.realpath(__file__)
        self.ret_val = os.path.dirname(self.script_path)
        while 'PomoClock' not in self.ret_val[-9:]:
            self.ret_val = os.path.dirname(self.ret_val)
        return self.ret_val

    def get_data_folder_path(self):
        return os.path.join(dir_path, 'data')

    def get_the_sounds_in_data_folder(self, dirpath):
        self.ret_val = [f for f in os.listdir(
            dirpath) if os.path.isfile(os.path.join(dirpath, f))]

        for sound in self.ret_val:
            if os.path.splitext(sound)[1] not in ['.mp3', '.mp4', '.wav']:
                self.ret_val.remove(sound)

        return self.ret_val

    def change_selected_sound_to(self, chosen_sound):
        self.selected_sound = chosen_sound

    def get_selected_sound(self):
        return self.selected_sound

    def choose_another_sound(self):
        self.init_dir = os.path.join('C:', 'Users', 'Public', 'Music')
        self.file_types = [("Music", "*.mp3|*.mp4|*.wav")]
        self.ret_val = filedialog.askopenfile(
            initialdir=self.init_dir, filetypes=self.file_types)
        self.selected_sound = self.ret_val if self.ret_val is not None else self.selected_sound