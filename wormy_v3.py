# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

"""
Simple Wormy game made with pygame.

This program runs a basic snake-style game where a worm moves around,
eats apples, and grows longer. The game ends if the worm hits the wall
or runs into itself.
"""

import random, pygame, sys
from pygame.locals import *

FPS = 10  # Elijah Priestley change 1a: Game speed FPS from 15 to 10
STARTFPS = 15  # Elijah Priestley change 1b: Start screen keeps same FPS of 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BLUE      = ( 18,   0, 181)  # Elijah Priestley change 2: added blue color
BGCOLOR = DARKGRAY  # Elijah Priestley change 3: background color from black to dark gray

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head


def main():
    """
    Sets up the game window and keeps the main game loop running.
    Shows the start screen, plays a round, and then shows the
    game-over screen.
    """
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    """
    Run one full round of the game.

    Handles movement, collisions, score updates, and drawing everything
    on the screen until the player loses the game.
    """
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if (wormCoords[HEAD]['x'] == -1 or
            wormCoords[HEAD]['x'] == CELLWIDTH or
            wormCoords[HEAD]['y'] == -1 or
            wormCoords[HEAD]['y'] == CELLHEIGHT):
            return  # game over
        for wormBody in wormCoords[1:]:
            if (wormBody['x'] == wormCoords[HEAD]['x'] and
                wormBody['y'] == wormCoords[HEAD]['y']):
                return  # game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    """
    Draw a small message telling the player to press a key to begin.
    """
    pressKeySurf = BASICFONT.render('Press a key to play.', True, WHITE)  # Elijah Priestley change 4, pressKeySurf font from DARKGRAY to WHITE
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    """
    Check if the player released a key.

    Returns the key that was released, or none if nothing was pressed.
    Also quits the game if needed.
    """
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    """
    Show the starting title screen with rotating text.
    Waits until the player presses a key to continue.
    """
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(STARTFPS)  # Elijah Priestley change 1c: Start screen FPS stays at 15
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    """
    Close pygame and exit the program.
    """
    pygame.quit()
    sys.exit()


def getRandomLocation():
    """
    Return a random x and y spot on the grid to place an apple.
    """
    return {'x': random.randint(0, CELLWIDTH - 1),
            'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    """
    Show the 'Game Over' screen and wait for the player to either
    play again or quit the game.
    """
    # Title
    gameOverFont = pygame.font.Font('8-bit-pusab.ttf', 75)  # Elijah Priestley change 5: font size from 150 to 75
    gameSurf = gameOverFont.render('Game', True, RED)
    overSurf = gameOverFont.render('Over', True, RED)  # Elijah Priestley change 6: "Game Over" red instead of white
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH // 2, 10)
    overRect.midtop = (WINDOWWIDTH // 2, gameRect.height + 35)

    # Prompt
    prompt = 'Press R to play again   |   Q to quit'  # added by Joshua Sherwood
    promptSurf = BASICFONT.render(prompt, True, WHITE)
    promptRect = promptSurf.get_rect()
    promptRect.midtop = (WINDOWWIDTH // 2, overRect.bottom + 30)

    # Draw once
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(promptSurf, promptRect)
    pygame.display.update()

    # Wait for a clear choice
    while True:
        key = checkForKeyPress()  # added by Joshua Sherwood
        if key is None:
            FPSCLOCK.tick(STARTFPS)
            continue
        if key in (K_r, K_SPACE, K_RETURN):
            pygame.event.get()  # clear queue
            return              # back to main loop -> runGame()
        if key in (K_q, K_ESCAPE):
            terminate()


def drawScore(score):
    """
    Draw the player's score in the top-right corner.

    score: the number of points to show.
    """
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    """
    Draw the worm on the screen using the list of its coordinates.
    """
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, (128, 0, 128), wormSegmentRect)  # Wesley Gibbs change 1, from DARKGREEN to purple
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, (186, 85, 211), wormInnerSegmentRect)  # Wesley Gibbs change 2, from GREEN to lighter purple


def drawApple(coord):
    """
    Draw the apple at the given grid location.
    """
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, (255, 165, 0), appleRect)  # Wesley Gibbs change 3, changed the color of the apple to orange


def drawGrid():
    """
    Draw the grid lines across the window so the game has a clear layout.
    """
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLUE, (x, 0), (x, WINDOWHEIGHT))  # Elijah Priestley change 7a: changed vertical grid lines from dark gray to blue
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLUE, (0, y), (WINDOWWIDTH, y))  # Elijah Priestley change 7b: changed horizontal grid lines from dark gray to blue


if __name__ == '__main__':
    main()
