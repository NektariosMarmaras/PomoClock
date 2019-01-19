import os
from tkinter import messagebox, filedialog

import playsound

seconds = int(0)
minutes = int(0)
dir_path = ''


class PomoClockLogic():
    def __init__(self, do_search=False):
        global dir_path
        self.selected_sound = 'chime.mp3'
        if do_search:
            print('LOGIC yay')
            dir_path = self.find_data_folder()
        self._job = None

    def start_timer(self, win_root, win_lbl):
        global seconds
        global minutes
        if minutes < 25:
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
                "Congratulations", "You have gone through 25 minutes of studying without taking a break!!!")

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
        playsound.playsound(sel_song_path)

    def show_pop_up(self, title='No Title', msg='No Message'):
        messagebox.showinfo(title, msg)

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
        print('selected_sound = {0}\nchosen_sound = {1}'.format(
            self.selected_sound, chosen_sound))
        self.selected_sound = chosen_sound
        print('selected_sound = {0}\nchosen_sound = {1}'.format(
            self.selected_sound, chosen_sound))

    def get_selected_sound(self):
        return self.selected_sound

    def choose_another_sound(self):
        # C:\Users\Public\Music
        self.init_dir = os.path.join('C:', 'Users', 'Public', 'Music')
        self.file_types = [("Music", "*.mp3|*.mp4|*.wav")]
        self.ret_val = filedialog.askopenfile(
            initialdir=self.init_dir, filetypes=self.file_types)
        print('ret_val  ->  {0}'.format(self.ret_val))
        self.selected_sound = self.ret_val if self.ret_val is not None else self.selected_sound
        print(self.selected_sound)
