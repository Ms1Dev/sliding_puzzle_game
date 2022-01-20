import tkinter as tk
from tkinter import ttk
import threading
from tkinter.constants import RAISED, SUNKEN

class Frame():
    def __init__(self, base):
        self.base = base
        frame = ttk.Frame(self.base.frame, height=50, relief=RAISED, borderwidth=3, style='Header.TFrame')
        frame.pack(side="top", fill="x")
        frame.pack_propagate(False)
        self.stopTimer = False
        # create the frame that contains the move counter
        moveDisplayFrame = ttk.Frame(frame, style='Header.TFrame')
        moveDisplayFrame.pack(side="left", fill="x", expand=True, pady=3)
        moveDisplayFrame.grid_columnconfigure(0, weight=1)
        self.moveCounter = 0
        self.moves = tk.StringVar()
        self.moves.set("0")
        moveDisplay = ttk.Label(moveDisplayFrame, textvariable=self.moves, font=("verdana", 12))
        moveDisplay.config(width=5, anchor='w', relief=SUNKEN, borderwidth=1, padding=1)
        moveDisplay.grid(column=1, row=0, sticky="ew")
        moveLabel = ttk.Label(moveDisplayFrame, text="Moves:", anchor='e', font=("verdana", 10))
        moveLabel.grid(column=0, row=0, sticky="ew")
        # create the frame that contains the timer display
        time = ttk.Frame(frame, style='Header.TFrame')
        time.pack(side="right", fill="x", expand=True, pady=3)
        self.timeElapsed = 0
        self.displayTime = tk.StringVar()
        self.displayTime.set("00:00:00")
        timeDisplay = ttk.Label(time, textvariable=self.displayTime, font=("verdana", 12))
        timeDisplay.config(anchor='w', relief=SUNKEN, borderwidth=1, padding=1)
        timeDisplay.grid(column=1, row=0, sticky="ew")
        timeLabel = ttk.Label(time, text="Time:", width=10, anchor="e", font=("verdana", 10))
        timeLabel.grid(column=0, row=0, sticky="ew")
        self.timer = threading.Timer(1.0, self.increment_timer)
        self.timer.start()

    @property
    def score(self):
        """Returns: move counter (int), time sec (int), time HH:MM:SS (str)"""
        timer = self.displayTime.get()
        return self.moveCounter, self.timeElapsed, timer

    def increment_timer(self):
        """Increments the timer. Calls itself every second as long as stopTimer variable is False"""
        if not self.stopTimer:
            self.timeElapsed +=1
            self.update_time_display(self.timeElapsed)
            self.timer = threading.Timer(1.0, self.increment_timer)
            self.timer.start()
    
    def update_time_display(self, timeElapsed):
        """Takes the time elapsed in seconds and converts it to a formatted string 'HH:MM:SS' then updates the time display"""
        hours = int(timeElapsed / 3600)
        minutes = int((timeElapsed % 3600) / 60)
        seconds = timeElapsed % 60
        # zfill(2) use 00 format - will keep the leading zero even if value is less than 10
        hours = str(hours).zfill(2)
        minutes = str(minutes).zfill(2)
        seconds = str(seconds).zfill(2)
        display = "{0}:{1}:{2}".format(hours,minutes,seconds)
        self.displayTime.set(display)
    
    def increment_moveCounter(self):
        """Increments the move counter by one every time this method is called""" 
        self.moveCounter += 1
        self.moves.set(f"{self.moveCounter}")

    def stop_timer(self):
        """Sets stopTimer to True which prevents timer from being incremented. Also cancels the timer thread"""
        self.timer.cancel()
        self.stopTimer = True
