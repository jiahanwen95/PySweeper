import pygame as pg
from constants import (CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR, TOOLBARHEIGHT)
class GUI():
    """ GUI Class:
        Handles all window elements.
    """
    def __init__(self, board):
        """ Constructor
            Calculate the game window based on board size.
            Defaults: ROWS=10, COLS=10
            PARAMS need to be changed to (self, board). Board object
            will have all the sizes we need.
        """
        #@todo: Generate dynamically based on uiElements
        self.board = board
        self.toolbarOffset = 50
        self.width = ((CELLWIDTH + MARGIN) * board.columns) + (BORDER * 2)
        self.height = ((CELLHEIGHT + MARGIN) * board.rows) + (BORDER * 2) + TOOLBARHEIGHT
        #@todo: Set min/max values based on user input
        if True:
            self.size = self.width, self.height
        elif False:
            pass
        print("Width: ", self.width, "Height: ", self.height)
        self.window = pg.display.set_mode(self.size)

    def drawBoard(self):
        for row in range(self.board.rows):
            for col in range(self.board.columns):
                cellColor = COLOR['WHITE']
                if self.board.grid[row][col].mine == True:
                    cellColor = COLOR['RED']
                cellX = ((MARGIN + CELLWIDTH) * col + MARGIN) + BORDER
                cellY = ((MARGIN + CELLHEIGHT) * row + MARGIN) + BORDER + self.toolbarOffset
                cell = pg.Rect([cellX, cellY, CELLWIDTH, CELLHEIGHT])

                pg.draw.rect(self.window, cellColor, cell)

    def uiElement(self, x, y, w, h, type='None', label='None'):
        """ Handles creation of all UI elements except board.
        """
        pass

    def mouseClick(self, event):
        """ Handles any mouse event inside the window.
        """
        if True:
            mousePosition = pg.mouse.get_pos()
            column = (mousePosition[0] - BORDER) // (CELLWIDTH + MARGIN)
            row = (mousePosition[1] - BORDER - TOOLBARHEIGHT) // (CELLHEIGHT + MARGIN)
            if event.button == 1:
                print("You pressed the left mouse button at:", mousePosition, ":", column, row, self.board.grid[row][column].mine)
            elif event.button == 3:
                print("You pressed the right mouse button at:", mousePosition, ":", column, row, self.board.grid[row][column].mine)