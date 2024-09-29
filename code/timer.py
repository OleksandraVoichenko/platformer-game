import pygame.time

from settings import *

class Timer:
    """Handles timer functions. With custom created methods like autostart, repeat, update."""

    def __init__(self, duration, func = None, repeat = None, autostart = False):
        self.duration = duration
        self.start_time = 0
        self.active= False
        self.func = func
        self.repeat = repeat

        if autostart:
            self.activate()


    def __bool__(self):
        """Handles & boolean operation."""

        return self.active


    def activate(self):
        """Activates timer."""

        self.active = True
        self.start_time = pygame.time.get_ticks()


    def deactivate(self):
        """Deactivates timer, and starts timer again if repeat is turned on."""

        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()


    def update(self):
        """Updates timer value"""

        if pygame.time.get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()