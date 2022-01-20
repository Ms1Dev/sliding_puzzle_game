from tkinter import ttk
import shelve
import operator
from tkinter.constants import RAISED

class Scoreboard():
    """Scoreboard object that displays lists of high scores"""
    @staticmethod
    def shelve_setup(filePath):
        """creates file and shelves if they do not exist already"""
        # open scores file - will create one if doesn't exist
        file = shelve.open(filePath)
        # iterate over difficulties and if shelf doesn't exist for that difficulty then create one
        for difficulty in ('Easy','Intermediate','Expert'):
            if difficulty not in file.keys():
                file[difficulty] = []
        file.close()

    @staticmethod
    def get_difficulty(numberOfTiles):
        """Returns difficulty as a string from the given number of tiles"""
        if numberOfTiles == 9:
            return 'Easy'
        elif numberOfTiles == 16:
            return 'Intermediate'
        elif numberOfTiles == 25:
            return 'Expert'

    def __init__(self, base):
        self.base = base
        self.filePath = "scores.dat"
        Scoreboard.shelve_setup(self.filePath)
        self.create_score_frames()

    def write_score_to_file(self, scoreData):
        """Shelves the incoming score data and updates the scoreboard display"""
        file = shelve.open(self.filePath, writeback=True)
        # scoreData[4] is the number of tiles the game was played on
        difficulty = Scoreboard.get_difficulty(scoreData[4])
        # store the score data in relevent folder
        file[difficulty].append(scoreData)
        file.close()
        # update the score display
        self.update_specific(difficulty, 5)
    
    def get_ordered_scores(self, difficulty):
        """Returns an ordered list of scores from file for a given difficulty"""
        file = shelve.open(self.filePath)
        # sort list on moves and then time(sec)
        sortedList = sorted(file[difficulty], key=operator.itemgetter(0,1))
        file.close()
        return sortedList

    def create_score_frames(self):
        """Creates the frame the scores will be displayed in"""
        self.frame = ttk.Frame(self.base.frame, borderwidth=1, relief=RAISED)
        self.frame.grid_propagate(False)
        self.board = ttk.Frame(self.frame)
        self.scoreDisplay = {}
        self.configure_display()
        self.update_all(self.showScores)
    
    def configure_display(self):
        """Configuration of the score displays and titles"""
        self.showScores = 5
        self.frame.pack(side="right", fill="y")
        title = ttk.Label(self.frame, text="High Scores", style='Dark.Label', font=('verdana', 10))
        title.pack(side='top', fill='x', pady=3)
        self.board.pack(side='top', fill='x')
        # create 3 score displays for each difficulty and arrange vertically
        for i, difficulty in enumerate(('Expert', 'Intermediate', 'Easy')):
            self.board.rowconfigure(i ,weight=1)
            self.scoreDisplay[difficulty] = Score_list(self.board, 0, i, difficulty)
    
    def update_specific(self, difficulty, rows):
        """Update one specific score display"""
        self.scoreDisplay[difficulty].update(self.get_ordered_scores(difficulty), rows)

    def update_all(self, rows):
        """Update all score displays"""
        for difficulty, scoreList in self.scoreDisplay.items():
            scoreList.update(self.get_ordered_scores(difficulty), rows)


class Full_scoreboard(Scoreboard):
    """Scoreboard that takes up the entire window. Inherits Scoreboard"""
    def configure_display(self):
        self.showScores = 20
        self.frame.pack(side="top", fill="both", expand=True)
        headerFrame = ttk.Frame(self.frame)
        headerFrame.pack(side='top', fill='x', pady=10, padx=5)
        backBtn = ttk.Button(headerFrame, text=" << Back ", command=self.base.main_menu)
        backBtn.pack(side='left')
        title = ttk.Label(headerFrame, text="Scores              ", font=('verdana', 12), style='Dark.Label')
        title.pack(side='left', fill='x', expand=True)
        self.board.pack(side='top', fill='both', expand=True)
        comment = ttk.Label(self.frame, text="* puzzle completed without showing numbers", style='Dark.Label')
        comment.pack(side='bottom' , pady=5, padx=5)
        self.board.rowconfigure(0, weight=1)
        # create 3 score displays for each difficulty and arrange horizontally
        for i, difficulty in enumerate(('Expert', 'Intermediate', 'Easy')):
            self.board.columnconfigure(i, weight=1)
            self.scoreDisplay[difficulty] = Score_list(self.board, i, 0, difficulty)


class Score_list():
    """A list box showing player scores"""
    def __init__(self, root, col, row, title):
        self.frame = ttk.Frame(root)
        self.frame.grid(column=col, row=row, sticky='ns')
        title = ttk.Label(self.frame, text=title, style='Dark.Label')
        title.pack(side='top', fill='x')
        self.scores = ttk.Treeview(self.frame)
        self.scores.pack(side='top', fill='both', expand=True)
        self.scores.config(columns=(1,2,3,4), show="headings", selectmode='none')
        # configure columns and headers
        self.scores.column(1, width=10)
        self.scores.column(2, width=100)
        self.scores.column(3, width=55)
        self.scores.column(4, width=75)
        self.scores.heading(1, text="")
        self.scores.heading(2, text="Name", anchor='w')
        self.scores.heading(3, text="Moves", anchor='w')
        self.scores.heading(4, text="Time", anchor='w')
    
    def update(self, scoreData, numberOfRows):
        """Updates the list box with latest scores"""
        self.clear_scores()
        numOfScores = len(scoreData)
        # iterate over the number of rows given
        for i in range(numberOfRows):
            # end the for loop if there are no more scores
            if i >= numOfScores:
                break
            score = scoreData[i]
            # add an asterisk to number of moves if the game was completed without showing numbers
            moves = str(score[0]) + ('*' if score[5] else '')
            time = score[2]
            name = score[3]
            row = (i + 1, name, moves, time)
            # insert the values into the list
            self.scores.insert(parent='', index=i, iid=i, values=row)
    
    def clear_scores(self):
        """Clears the entire list of scores"""
        for score in self.scores.get_children():
            self.scores.delete(score)
            
