import random
from tkinter import messagebox
from PIL import Image as Img
from PIL import ImageTk, ImageStat
import os
import sys


def __get_random_image():
    """Gets a random image from the images folder. Any images that are not valid are moved to invalidImages folder."""
    # try to get a list of the image files in the images folder
    try:
        imagesFolder = os.listdir("images")
    except FileNotFoundError:
        messagebox.showerror('Error', 'Images folder not found')
        sys.exit('Images folder not found')
    except Exception as error:
        messagebox.showerror('Error', error)
        sys.exit(error)
    # try to get a file from the images folder 
    try:
        imageFile = random.choice(imagesFolder)
    except IndexError:
        messagebox.showerror('Error', 'Cannot load image - images folder is empty')
        sys.exit('Cannot load image - images folder is empty')
    imagePath = "images/" + imageFile
    # create a folder to dump invalid images 
    if not os.path.exists("invalidImages"):
        os.mkdir("invalidImages")
    # try to open the image
    try:
        img = Img.open(imagePath)
    except:
        # if it throws an error move the image to the invalid images folder and repeat function
        os.rename(imagePath, "invalidImages/" + imageFile)
        # returning the function will run it again
        return  __get_random_image()
    # check the size of the image - anything above 4000 pixels is unnecessarily big and below 500 will be poor resolution
    isValidWidth = img.width < 4000 and img.width > 500
    isValidHeight = img.height < 4000 and img.height > 500
    img.close()
    # if the image is a jpeg and is the right size then return it, else move image to invalid images and run the function again
    if imagePath.endswith(('.jpg', '.jpeg')) and isValidWidth and isValidHeight:
        return imagePath
    else:
        os.rename(imagePath, "invalidImages/" + imageFile)
        return __get_random_image()


def get(numberOfPieces, boardWidth):
    """Returns a random list of puzzle pieces"""
    while True:
        randomList = random.sample(range(numberOfPieces), numberOfPieces)
        # it is possible to create a puzzle that is unsolveable so the list needs to be validated before continuing
        if __is_random_list_valid(randomList):
            break
    # get the square root of number of pieces
    sqrtNumberOfPieces = numberOfPieces ** 0.5
    sqrtNumberOfPieces = int(sqrtNumberOfPieces)
    # find the width of each piece by dividing width of board by square root of pieces
    pieceWidth = boardWidth // sqrtNumberOfPieces
    imageFile = __get_random_image()
    # create the image object that will be used to decorate the pieces
    image = Image(imageFile, sqrtNumberOfPieces)
    # create the list of pieces
    pieces = [Piece(number, numberOfPieces, image, pieceWidth) for number in randomList]
    return image, pieces


class Piece():
    """Puzzle piece"""
    @staticmethod
    def font_colour(image, imageWidth):
        """Returns either black or white depending on image brightness for greatest contrast"""
        cropWidth = imageWidth / 3
        # crop image to get the very centre - this is where the font should contrast with the most
        image = image.crop((cropWidth, cropWidth, imageWidth - cropWidth, imageWidth - cropWidth))
        # convert image to greyscale
        image = image.convert('L')
        # get the average brightness using image stat
        imageStat = ImageStat.Stat(image)
        avg = imageStat.mean[0]
        # brightness is from 0 - 256, if the average brightness is in upper half return black else return white
        if avg >= 128:
            return "#000000"
        else:
            return "#FFFFFF"
    
    @staticmethod
    def font_size(numberOfPieces):
        """Returns an appropriate font size depending on number of puzzle pieces"""
        if numberOfPieces == 9:
            return 38
        elif numberOfPieces == 16:
            return 30
        else:
            return 22
        
    def __init__(self, id, numberOfPieces, image, pieceWidth):
        self.id = id
        self.isBlank = False
        if self.id == numberOfPieces - 1:
            self.isBlank = True
        # get image fragment that matches id
        self.image = image.get_fragment(self.id)
        # resize the fragment to the size of a puzzle piece
        self.image = self.image.resize((pieceWidth,pieceWidth), Img.ANTIALIAS)
        # calculate the correct font colour before image is converted to photo image
        self.fontColour = Piece.font_colour(self.image, pieceWidth)
        # image is converted to photo image so it can be displayed by tk Button
        self.image = ImageTk.PhotoImage(self.image)
        # get the correct font size for displaying numbers on the puzzle piece
        self.fontSize = Piece.font_size(numberOfPieces)
    
    @property
    def display_properties(self):
        """Returns properties needed for displaying a number on puzzle piece"""
        return self.id + 1, self.fontSize, self.fontColour


class Image():
    """A square image that is used to decorate the puzzle pieces"""
    @staticmethod
    def crop_image_square(image):
        """Return the image cropped to a square"""
        # store image dimensions in variables
        width = image.width
        height = image.height
        # if image is square just return image
        if width == height:
            return image
        # if image is landscape crop the sides else crop the top and bottom
        if width > height:
            diff = (width - height) // 2
            left = 0 + diff
            top = 0
            right = width - diff
            bottom = height
        elif height > width:
            diff = (height - width) // 2
            left = 0 
            top = 0 + diff
            right = width
            bottom = height - diff
        cropped = image.crop((left,top,right,bottom))
        return cropped

    def __init__(self, imageFile, sqrtNumberOfPieces):
        self.img = Img.open(imageFile)
        self.img = Image.crop_image_square(self.img)
        self.fragments = self.generate_fragments(sqrtNumberOfPieces)

    @property
    def whole_image(self):
        return self.img

    def generate_fragments(self, sqrtNumberOfPieces):
        """Divides the whole image into fragments"""
        # find the size of each fragment
        fragSize = self.img.width // sqrtNumberOfPieces
        fragments = []
        # initial coordinates for cropping - starting top left corner
        left = 0
        top = 0
        right = fragSize
        bottom = fragSize
        # create fragments by cropping the image by row and column using the fragment size
        for row in range(sqrtNumberOfPieces):
            for column in range(sqrtNumberOfPieces):
                image = self.img.crop((left,top,right,bottom))
                fragments.append(image)
                # after appending image increase cropping coordinates to the right by one fragment size to move to next column
                left += fragSize
                right += fragSize
            # at the end of the row set the left/right coordinate back to start (first column) and move top/bottom coordinates to next row
            left = 0
            right = fragSize
            top += fragSize
            bottom += fragSize
        return fragments

    def get_fragment(self, fragNumber):
        """Returns a fragment of the whole image"""
        return self.fragments[fragNumber]


def __get_parity(randomList):
    """Returns True for even and False for odd depending on start position of empty tile (15 puzzle only)"""
    emptyTileIndex = randomList.index(15)
    evenRow = (0,1,2,3,8,9,10,11)
    # if empty tile starts on an even row (counting from bottom) the parity is odd else it is even
    if emptyTileIndex in evenRow:
        # blank tile on even row return false as the parity must be odd
        return False
    else:
        # blank tile is on odd row return true as parity must be even
        return True

def __is_random_list_valid(randomList):
    """Returns True if the list is valid.
    Validation requires the list to have a number of inversions with the correct parity.
    For the 8 and 24 puzzles the parity is always even.
    For the 15 puzzle the parity depends on whether the blank space starts on an odd or even row (counting from the bottom row)."""
    # if the 15 puzzle is selected then the parity depends on where the blank tile starts
    if len(randomList) == 16:
        parityIsEven = __get_parity(randomList)
    else:
        # for 8 and 24 puzzles the parity is always even
        parityIsEven = True
    # make a copy of the random list
    randomList = randomList[:]
    # remove the highest value - it represents the empty tile
    randomList.remove(len(randomList) - 1)
    # create variable to count the number of inversions
    inversions = 0
    # for every number in random list count how many ahead of it are less than itself - i.e. count inversions
    for i, number in enumerate(randomList):
        # for every iteration we shorten the list - we only care what is ahead of the current number hence [i:]
        inversions += sum(j < number for j in randomList[i:])
    # if number of inversions matches the parity then return True
    if inversions % 2 == 0 and parityIsEven:
        return True
    elif inversions % 2 != 0 and not parityIsEven:
        return True
    else:
        return False
