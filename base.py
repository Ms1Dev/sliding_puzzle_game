from tkinter import BooleanVar, messagebox, ttk
from tkinter.constants import RAISED
from PIL import Image, ImageTk
import tkinter as tk
import header, scoreboard, puzzle
import sys

class Frame():
    """Creates the base frame. Takes the root window as a parameter"""
    def __init__(self, root):
        bgImage = Image.open("app_images/bg.jpg")
        bgImage = bgImage.resize((960,600), Image.ANTIALIAS)
        # save the image in memory to be used later
        self.bgImage = ImageTk.PhotoImage(bgImage)
        self.frame = tk.Frame(root)
        self.frame.pack(fill='both', expand=True)
        self.main_menu()
        self.root = root
        
    def main_menu(self):
        """Create the main menu buttons"""
        self.clear_frame()
        # set the background to image we have saved in memory
        background = tk.Label(self.frame, image=self.bgImage)
        background.place(x=0, y=0, relwidth=1, relheight=1)
        # create a frame in the centre of the window to contain the menu buttons
        menu = ttk.Frame(self.frame, padding=5)
        menu.place(relx=0.5, rely=0.5, anchor='center')
        # label frame with border to seperate the three play buttons from the others
        labelFrame = ttk.Frame(menu, padding=10, relief=RAISED)
        labelFrame.pack(pady=3)
        label = ttk.Label(labelFrame, text="Play", style='Dark.Label')
        label.pack(fill='x', pady=3)
        # create three buttons for playing different difficulties
        easyButton = ttk.Button(labelFrame, text="Easy", command=lambda: self.play_game(9), width=20)
        easyButton.pack(fill='x', pady=3)
        interButton = ttk.Button(labelFrame, text="Intermediate", command=lambda: self.play_game(16))
        interButton.pack(fill='x', pady=3)
        expButton = ttk.Button(labelFrame, text="Expert", command=lambda: self.play_game(25))
        expButton.pack(fill='x', pady=3)
        # below the frame that has the play buttons create two more buttons for showing scores and exit
        scoreButton = ttk.Button(menu, text="Show scores", command=self.view_scores)
        scoreButton.pack(fill='x', pady=3)
        scoreButton = ttk.Button(menu, text="Exit", command=self.exit)
        scoreButton.pack(fill='x', pady=3)

    def clear_frame(self):
        """Remove all objects from frame"""
        for object in self.frame.winfo_children():
            object.destroy()
    
    def view_scores(self):
        """Display player scores. Takes up full window"""
        self.clear_frame()
        scores = scoreboard.Full_scoreboard(self)

    def play_game(self, numberOfTiles):
        """Creates the puzzle frame as well as a header and scoreboard frame. 
        Accepts a number of tiles to create the puzzle with"""
        self.clear_frame()
        self.numberOfTiles = numberOfTiles
        # create the top menu bar
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        fileMenu = tk.Menu(menu, tearoff=False)
        helpMenu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=fileMenu)
        menu.add_cascade(label="Help", menu=helpMenu)
        newGame = tk.Menu(fileMenu, tearoff=False)
        fileMenu.add_cascade(label="New game", menu=newGame)
        newGame.add_command(label="Easy", command=lambda: self.new_game(9))
        newGame.add_command(label="Intermediate", command=lambda: self.new_game(16))
        newGame.add_command(label="Expert", command=lambda: self.new_game(25))
        fileMenu.add_command(label="Restart", command=self.restart)
        fileMenu.add_command(label="Main menu", command=self.end_game)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exit)     
        self.showNumVar = BooleanVar()
        self.showNumVar.set(False)
        helpMenu.add_checkbutton(label="Show numbers", variable=self.showNumVar, onvalue=1, offvalue=0, command=self.show_numbers)
        helpMenu.add_command(label="View Image", command=self.view_image)
        # create scoreboard, header containing timer and number of moves and the puzzle board
        self.scoreboard = scoreboard.Scoreboard(self)
        self.header = header.Frame(self)
        self.puzzle = puzzle.Board(self, tiles=numberOfTiles)
    
    def move_completed(self):
        """Increments the number of moves in the header"""
        self.header.increment_moveCounter()

    def puzzle_completed(self, noHints):
        """Stops the timer and retrieves the score data from the header. Presents user with pop up to capture name"""
        # stop the timer
        self.header.stop_timer()
        # get the score that has been recorded in the header
        score = self.header.score
        # get the centre of the screen
        xCentre = int(self.root.winfo_screenwidth() / 2)
        yCentre = int(self.root.winfo_screenheight() / 2)
        # create an input window for user to enter name 
        Input_window(self.frame, score, self.numberOfTiles, self.save_score, xCentre, yCentre, noHints)

    def save_score(self, scoreData):
        """Passes the score data to the scoreboard module to be saved to file"""
        self.scoreboard.write_score_to_file(scoreData)

    def show_numbers(self):
        """Toggles the display of numbers on puzzle tiles"""
        if self.puzzle.showNumbers:
            self.puzzle.toggle_show_numbers(False)
            self.showNumVar.set(False)
        else:
            self.puzzle.toggle_show_numbers(True)
            self.showNumVar.set(True)

    def new_game(self, numberOfTiles):
        """Starts a new game for given number of tiles. Asks for user confirmation"""
        answer = messagebox.askyesno('New game', 'Are you sure you want to start a new game?')
        if answer == True:
            self.header.stop_timer()
            self.play_game(numberOfTiles)

    def view_image(self):
        """Opens the image currently being used in the puzzle in a seperate window"""
        self.puzzle.img.whole_image.show()

    def end_game(self):
        """Clear puzzle, header and scoreboard and display main menu. Asks for user confirmation"""
        answer = messagebox.askyesno('Return to menu', 'Are you sure you want to return to the main menu?')
        if answer == True:    
            self.clear_frame()
            self.header.stop_timer()
            self.root.config(menu=0)
            self.main_menu()
    
    def restart(self):
        """Start a new game with the same number of tiles. Asks for user confirmation"""
        answer = messagebox.askyesno('Restart', 'Are you sure you want to restart the game?')
        if answer == True:
            self.header.stop_timer()
            self.play_game(self.numberOfTiles)

    def exit(self):
        """Exits the app. Asks for user confirmation"""
        answer = messagebox.askyesno('Exit', 'Are you sure you want to exit?')
        if answer == True:
            try:
                self.header.stop_timer()
            finally:
                sys.exit('Program terminated')


class Input_window():
    """Pop up window that prompts user for their name"""
    def __init__(self, root, score, numberOfTiles, submitMethod, xCoord, yCoord, noHints):
        # this function will be called on press of submit
        self.submitMethod = submitMethod
        self.score = score
        self.numberOfTiles = numberOfTiles
        self.noHints = noHints
        self.maxNameLength = 15
        self.window = tk.Toplevel(root)
        # set the geometry of the window "width x height + x-Coordinate + y-Coordinate"
        self.window.geometry("220x220+{0}+{1}".format(xCoord - 110 , yCoord - 110))
        # no minimise and maximise buttons
        self.window.transient(root)
        # prevent window from being resized
        self.window.resizable(False,False)

        message = "\nCompletion time\n{0}\n\nNumber of moves\n{1}\n\nEnter a name to save score\n(max {2} characters)".format(score[2], score[0], self.maxNameLength)
        label = tk.Label(self.window, text=message, font=('verdana', 10))
        label.grid(column=0, row=0, columnspan=2, padx=15)

        self.userInput = tk.StringVar()
        entryField = tk.Entry(self.window, textvariable=self.userInput, font=('verdana', 10))
        entryField.bind('<KeyPress>', self.key_press_event)
        entryField.grid(column=0, row=1, columnspan=2, pady=5, padx=5)
        entryField.focus_set()
        submitBtn = tk.Button(self.window, text="Submit", command=self.submit_data)
        submitBtn.grid(column=0, row=2, padx=8, pady=5, sticky='ew')
        cancelBtn = tk.Button(self.window, text="Cancel", command=self.window.destroy)
        cancelBtn.grid(column=1, row=2, padx=8, pady=5, sticky='ew')
    
    def key_press_event(self, event):
        """Event triggered on key press. If string is maximum length ignore key press. If Return is pressed then attempt to submit data"""
        # get the length of the current string
        textLength = self.userInput.get()
        # get the keysym from the event
        key = event.keysym
        # if return is pressed then submit the data
        if key == "Return":
            self.submit_data()
        # tuple of keys that need to be operational even if string is max length
        permissibleKeys = ('BackSpace', 'Left', 'Right', 'Tab')
        # if the string is max length and key is not in list of permissible keys return "break"
        if len(textLength) >= self.maxNameLength and not key in permissibleKeys:
            return "break"

    def submit_data(self):
        """Passes list containing score data back to the base frame object. 
        [moves (int), time sec (int), time "HH:MM:SS"(str), name (str), num of tiles (int)]"""
        name = self.userInput.get()
        if len(name) == 0:
            messagebox.showwarning('Invalid name', 'Name cannot be blank')
        else:
            data = list(self.score)
            data.append(name)
            data.append(self.numberOfTiles)
            data.append(self.noHints)
            self.submitMethod(data)
            self.window.destroy()