import tkinter as tk
import style
import base

# create the window
root = tk.Tk()

# get the centre of the screen
xCentre = int(root.winfo_screenwidth() / 2)
yCentre = int(root.winfo_screenheight() / 2)
# set window size and launch app in centre of screen
root.geometry("750x550+{0}+{1}".format(xCentre - 350, yCentre - 300))

# resizing the window may cause issues so set both axis to False
root.resizable(False, False)

# set title
root.title("Sliding Puzzle Game")
# set icon
root.iconbitmap('app_images/smart_cat.ico')

# create the base frame in this window
baseFrame = base.Frame(root)

# tell the window manager to run baseFrame.exit() when the window close button is pressed
# this is a healthier way to terminate the program as it cancels the timer thread if it is running
root.protocol("WM_DELETE_WINDOW", baseFrame.exit)

# configure the style of all widgets
style.configuration()

root.mainloop()
