import tkinter as tk
from tkinter import ttk
import puzzle_pieces


class Board():
    """Creates a frame that contains the game puzzle"""

    @staticmethod
    def get_tile_positions(sqrtOfTiles):
        """Returns the grid coordinates for tiles"""
        tilePositions = {}
        # x and y seems more relevant than the typical i and j iteration variables as they are grid coordinates
        for x in range(sqrtOfTiles):
            for y in range(sqrtOfTiles):
                tilePosition = len(tilePositions)
                tilePositions[tilePosition] = [x,y]
        return tilePositions
    
    @staticmethod
    def pieces_match_tiles(tiles):
        """Returns True if all puzzle pieces are on correct tiles"""
        # create a list of boolean values for whether puzzle pieces match the tile they are on
        matchingTiles = [tile.number == tile.puzzlePiece.id for tile in tiles]
        # if there are no False values in list then all pieces are on correct tiles and True is returned
        return not False in matchingTiles

    @staticmethod
    def get_active_tiles(emptyTile, numberOfTiles, sqrtOfTiles):
        """Returns a list of tile positions that neighbour the given tile position"""
        activeTiles = []
        # if on right edge include tile to left
        if emptyTile % sqrtOfTiles == sqrtOfTiles - 1:
            activeTiles.append(emptyTile - 1)
        # else if on left edge include tile to right
        elif emptyTile % sqrtOfTiles == 0:
            activeTiles.append(emptyTile + 1)
        # else not on right or left edge include tiles on both sides
        else:
            activeTiles.append(emptyTile - 1)
            activeTiles.append(emptyTile + 1)
        # if on top edge include tile below 
        if emptyTile < sqrtOfTiles:
            activeTiles.append(emptyTile + sqrtOfTiles)
        # else if on bottom edge include tile above
        elif emptyTile >= numberOfTiles - sqrtOfTiles:
            activeTiles.append(emptyTile - sqrtOfTiles)
        # else not on top or bottom edge include tiles above and below
        else:
            activeTiles.append(emptyTile + sqrtOfTiles)
            activeTiles.append(emptyTile - sqrtOfTiles)
        return activeTiles

    def __init__(self, base, tiles):
        self.numberOfTiles = tiles
        self.base = base
        self.showNumbers = False
        self.noHints = True
        self.frame = ttk.Frame(self.base.frame)
        self.frame.pack(fill="both", expand=True)
         # get square root of the number of tiles
        sqrtOfTiles = self.numberOfTiles ** 0.5
        self.sqrtOfTiles = int(sqrtOfTiles)
        # configure grid
        for i in range(self.sqrtOfTiles):
            self.frame.columnconfigure(i, weight=1)
            self.frame.rowconfigure(i, weight=1)     
        # get rows and columns for each tile position
        tilePositions = Board.get_tile_positions(self.sqrtOfTiles)
        # list comprehension to create tiles by passing self as reference to puzzle board, value as the tuple containing xy position and key as the tile number 
        self.tiles = [Tile(self, value, key) for key, value in tilePositions.items()]
        # before we can get the board width, idle tasks need to be updated or winfo_width will return 0
        self.frame.update_idletasks()
        # boardwidth is needed to crop the images to correct size on puzzle pieces
        boardWidth = self.frame.winfo_width()
        # get the puzzle pieces and get a copy of the whole image that is used in the puzzle
        self.img, puzzlePieces = puzzle_pieces.get(self.numberOfTiles, boardWidth)
        # assign the puzzle pieces to their initial tiles
        for i, tile in enumerate(self.tiles):
            tile.assign_puzzle_piece(puzzlePieces[i])
        # configure which tiles should be disabled and which active
        self.configure_tiles()

    def configure_tiles(self):
        """Finds the empty tile and configures other tiles so only the neighbouring ones are active"""
        # get the empty tile 
        self.emptyTile = self.get_empty_tile()
        # gets a list of tiles that neighbour the empty tile
        self.activeTiles = Board.get_active_tiles(self.emptyTile.number, self.numberOfTiles, self.sqrtOfTiles)
        # set the tiles neighbouring the empty tile to active
        self.set_active_tiles()

    def get_empty_tile(self):
        """Iterate over the list of tiles and return the tile that has the blank puzzle piece"""
        for tile in self.tiles:
            if tile.puzzlePiece.isBlank:
                return tile

    def set_active_tiles(self):
        """Sets the tiles that neighbour the empty tile to active and disables the rest"""
        for tile in self.tiles:
            if tile.number in self.activeTiles:
                tile.set_to_active()
            else:
                tile.set_to_disabled()

    def swap_pieces(self, selectedTile):
        """Moves the puzzle piece from the selected tile to the empty tile"""
        # the piece from the selected tile 
        selectedPiece = selectedTile.puzzlePiece
        # the blank piece from the empty tile
        blankPiece = self.emptyTile.puzzlePiece
        # assign the blank puzzle piece to the current selected tile
        selectedTile.assign_puzzle_piece(blankPiece)
        # assign the selected piece to the current empty tile
        self.emptyTile.assign_puzzle_piece(selectedPiece)
        self.base.move_completed()
        self.configure_tiles()
        self.check_for_win()
    
    def toggle_show_numbers(self, showNumbers):
        self.showNumbers = showNumbers
        self.noHints = False
        for tile in self.tiles:
            tile.configure_image()

    def check_for_win(self):
        """Compares all tiles to their position on the board, if all in correct position puzzle is completed"""
        if Board.pieces_match_tiles(self.tiles):
            for tile in self.tiles:
                tile.set_to_disabled()
            self.base.puzzle_completed(self.noHints)
    

class Tile():
    """Tile object"""
    def __init__(self, puzzleBoard, tilePosition, tileNumber):
        self.puzzleBoard = puzzleBoard
        self.number = int(tileNumber)
        self.puzzlePiece = None   
        self.row = tilePosition[0]
        self.column = tilePosition[1]
        
    def assign_puzzle_piece(self, piece):
        """When a puzzle piece is assigned a button is created in this tile position"""
        self.puzzlePiece = piece
        if not self.puzzlePiece.isBlank:
            # a button is used to represent the tile
            self.btn = tk.Button(self.puzzleBoard.frame)
            self.configure_image()
            self.btn.grid(column=self.column, row=self.row, sticky='nsew')
        else:
            # when board is created blank tile doesn't exist and will throw an error when trying grid forget
            try:
                self.btn.grid_forget()
            except:
                pass
    
    def configure_image(self):
        """Sets the image that is on the tile. The image comes from the puzzle piece that is currently assigned."""
        if not self.puzzlePiece.isBlank:
            id, fontSize, fontColour = self.puzzlePiece.display_properties
            if self.puzzleBoard.showNumbers:
                text = str(id)
            else:
                text = ""
            # configure the image that is displayed on the button
            self.btn.config(
                text=text, 
                font=('verdana', fontSize), 
                image=self.puzzlePiece.image, 
                compound='center', 
                foreground=fontColour, 
                activeforeground="#808080"
            )

    def tile_selected(self):
        """When tile is selected execute method in puzzleboard object to swap pieces with blank tile"""
        self.puzzleBoard.swap_pieces(self)

    def set_to_active(self):
        """Sets this tile to active"""
        self.btn.config(command=self.tile_selected)
    
    def set_to_disabled(self):
        """Sets this tile to disabled. Clicking has no action"""
        if not self.puzzlePiece.isBlank:
            self.btn.config(command=0)