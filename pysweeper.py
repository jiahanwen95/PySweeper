# Input box code based on https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame/46390412

# Imports system and operating system specific parameters and functions.
import os, sys 

# Imports the pygame library, makes use of the SDL library for easy multimedia applications.
# as pg allows us to just type pg, instead of pygame, to invoke a pygame function.
import pygame as pg 

# Imports each class from the .py file, our files and classes used identical names.
# It is convention in python to capitalize all class names.
from board import Board 
from cell import Cell
from gui import GUI, InputBox, InputButton
# from inputbox import InputBox

# Imports the needed variables, capitalized due to being constants, from the constants.py file
from constants import (CELLWIDTH, CELLHEIGHT,
                      MARGIN, BORDER, COLOR, TOOLBARHEIGHT)

# Initializes all imported pygame modules, as opposed to initalizing them one by one manually.
pg.init()
# Initializes font, must be called after pygame.init to avoid issues.
pg.font.init()
# Initalizes time, by invoking the Clock class. Set equal to a variable called clock.
# Is used to control framerate and avoid flashing images on the screen.
clock = pg.time.Clock()

# Initialize screen/windows
#@todo: Start the GUI here

gameBoard = Board()

screen = GUI(gameBoard)

pg.display.set_caption("Minesweeper")

# Defines inputBoxes that display on the screen, one each for row, column, and mines.
# InputBox takes parameters as such InputBox(x position, y position, length of box, width of box,
#  surface to display onto, text to take from user input converted to a string from an int)
inputRowBox = InputBox(BORDER + 66, BORDER + 3, 40, 20, screen, 32, 2,  str(gameBoard.rows))
inputColumnBox = InputBox(BORDER + 66, BORDER + 27, 40, 20, screen, 32, 2, str(gameBoard.columns))
inputMineBox = InputBox(BORDER + 163, BORDER + 3, 40, 20, screen, 10, 1, str(gameBoard.mines))

inputQuitButton = InputButton(BORDER + 60, BORDER + 30, 40, 20, screen, "Quit")
inputRestartButton = InputButton(BORDER + 110, BORDER + 30, 55, 20, screen, "Restart")

# Places the inputRowBox, inputColumnBox, and inputMineBox into an array called input_boxes.
input_boxes = [inputRowBox, inputColumnBox, inputMineBox]
input_buttons = [inputQuitButton, inputRestartButton]

# Defines a boolean value done that is used to control the main game loop.
done = False

# Defines a while loop that represents the main game loop
# While done is false the game will continue. All code indented from this point is in this while loop.
while not done:
    # Keep the game running until the user decides to quit the game.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        # An event handler for when the user presses a mouse button.
        elif event.type == pg.MOUSEBUTTONDOWN:
            # GUI.mouseClick() handles clicking anywhere on the board.
            screen.mouseClick(event)
            # Handle input boxes here.
            # Users can only left click input boxes. Restricting to button 1.
            if event.button == 1:
                for button in input_buttons:
                    if button.rect.collidepoint(event.pos):
                       button.active = not button.active
                for box in input_boxes:
                    # If the user clicked on the input box, toggle state.
                    if box.rect.collidepoint(event.pos):
                        box.active = not box.active
                    else:
                        box.active = False
                    # Feedback color for active input box.
                    box.color = COLOR['RED'] if box.active else COLOR['WHITE']
        # Listen for key presses. Input boxes that are active take all inputs.
        elif event.type == pg.KEYDOWN:
            for box in input_boxes:
                if box.active:
                    if event.key == pg.K_RETURN:
                        box.active = not box.active
                        box.color = COLOR['WHITE']
                        # Only call update one per user hitting enter.
                        # Calling all 3 works for the time being.
                        inputRowBox.update(screen, gameBoard, "rows", inputRowBox.text)
                        inputColumnBox.update(screen, gameBoard, "columns", inputColumnBox.text)
                        # Check maxValue before calling box.update() on mines.
                        inputMineBox.maxValue = (screen.board.rows * screen.board.columns) - 1
                        inputMineBox.update(screen, gameBoard, "mines", inputMineBox.text)
                    elif event.key == pg.K_BACKSPACE:
                        box.text = box.text[:-1]
                    else:
                        box.text += event.unicode
                    box.txt_surface = box.font.render(box.text, True, COLOR['WHITE'])


    # Fills the screen with a single color, we chose black, every other element will be drawn ontop of this.
    screen.window.fill(COLOR['BLACK'])

    # Using box, from the InputBox class, call the draw definition on each element in the input_boxes array.
    # This will blit the box onto the screen.
    # Blit works by drawing something onto the surface of something else.
    # In this case, we draw the inputbox onto the screen, which why we pass the screen as a parameter.
    for box in input_boxes:
        box.draw()

    # Using screen, from the GUI class, call the uiElement defintion passing in parameters for 
    # X position, Y position, width, height, borderWidth, type to display (text), label to show on screen.
    screen.uiElement(BORDER, BORDER, screen.width - (BORDER * 2), TOOLBARHEIGHT, 1)
    screen.uiElement(BORDER + 6, BORDER + 8, 0, 0, 0, "text", "Rows:")
    screen.uiElement(BORDER + 6, BORDER + 33, 0, 0, 0, "text", "Columns:")
    screen.uiElement(BORDER + 120, BORDER + 8, 0, 0, 0, "text", "Mines:")
    screen.uiElement(BORDER + 120, BORDER + 33, 0, 0, 0, "text", "Flags:    " + str(gameBoard.mines - gameBoard.flagsPlaced))
    if gameBoard.gameOver:
        screen.uiElement(BORDER, BORDER, screen.width - (BORDER * 2), TOOLBARHEIGHT, 0)
        if gameBoard.wonGame:
            screen.uiElement(BORDER + 85, BORDER + 10, 0, 0, 0, "text", "WINNER!")
        else:
            screen.uiElement(BORDER + 75, BORDER + 10, 0, 0, 0, "text", "GAME OVER")
             
        for button in input_buttons:
            button.draw()
        if inputQuitButton.active == True:
            done = True
        if inputRestartButton.active == True:
            inputRestartButton.restart(screen, gameBoard)

        #Draw Play Again box Here ---HINT: in event handler code, check if click collides with play again, then call gameBoard.generateGrid()

    # Call the drawBoard definition on screen.
    screen.drawBoard()

    # display.flip will redraw entire window each frame. Good enough for Minesweeper.
    pg.display.flip()
    # clock.tick limits the fps of the program.  Using 20 as a parameter runs the program at 20 fps.
    # We do this to limit flashes on the screen or tearing of an image.  Minesweeper doesn't need much.
    clock.tick(20)

# Quits the game when the user closes the window the game is displayed in.
pg.quit()
