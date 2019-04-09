import os

import pomoclock_gui
import pomoclock_logic


class PomoClock():
    def __init__(self):
        self.pom_logic = pomoclock_logic.PomoClockLogic(do_search=True)
        self.pom_gui = pomoclock_gui.PomoClockGui()


if __name__ == "__main__":
    PomoClock()