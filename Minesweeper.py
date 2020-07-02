#Minesweeper

#Dependencies and Constants

import pygame
import pygame.gfxdraw
import random
import math
import numpy as np
import time
import sys

pygame.init()
pygame.mixer.init(44100, -16, 300, 64)

#Linear Algebra stuffs
e1 = math.cos(math.radians(22.5))
e2 = math.sin(math.radians(22.5))
rot = np.array([[e1, e2], [-(e2), e1]])
vecta = np.array([270, 0])
vectb = np.array([0, 270])
vectc = np.array([-270, 0])
vectd = np.array([0, -270])

#Color Codes
Yellow = (252, 186, 3)
Orange = (252, 140, 3)
Red = (255, 0, 0)
Light_green = (27, 94, 31)
Dark_green = (10, 48, 8)
Dark_blue = (0, 23, 36)
Light_blue = (0, 255, 255)

font = pygame.font.SysFont('impact', 25)
numfont = pygame.font.SysFont('impact', 10)

mine1 = pygame.image.load('Graphics/mine1.png')
mine2 = pygame.image.load('Graphics/mine2.png')
mine3 = pygame.image.load('Graphics/mine3.png')
mine4 = pygame.image.load('Graphics/mine4.png')
mine5 = pygame.image.load('Graphics/mine5.png')
mine6 = pygame.image.load('Graphics/mine6.png')
mine7 = pygame.image.load('Graphics/mine7.png')
mine8 = pygame.image.load('Graphics/mine8.png')
bomb = pygame.image.load('Graphics/minebomb.png')
flag = pygame.image.load('Graphics/mineflag.png')
hitmarker = pygame.image.load('Graphics/hitmarker.png')
icon = pygame.image.load('Graphics/icon.png')

pygame.display.set_icon(icon)

sonar = pygame.mixer.Sound('Sounds/Sonar.wav')
hitmarkerSound = pygame.mixer.Sound('Sounds/hitmarkersound.wav')
explode = pygame.mixer.Sound('Sounds/Explode.wav')
wasted = pygame.mixer.Sound('Sounds/Wasted.wav')
yay = pygame.mixer.Sound('Sounds/Yay.wav')

music = pygame.mixer.Sound('Sounds/Music.wav')
pygame.mixer.Sound.play(music, -1)

#Board dimensions by difficulty
easy_size = 8
medium_size = 16
hard_size = 24

LEFT = 1
RIGHT = 3

#Number of mines by difficulty
easy_mines = 13
medium_mines = 52
hard_mines = 117

#block dimension
block_side = 32
#margin will be 4 pixels

redlayer = []
orangelayer = []
yellowlayer = []
flagList = []
scoreList = []
initList = []
plotList = []
mineList = {} #stores mine coordinates

#------------------------------------------------------------------------------

#Classes and Functions Definitions

#Buttons Class
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None): #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            pygame.font.SysFont('impact', 25)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

#Draws the screen and the grid
def redrawWindow():
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_mode((36*dnum +4, 36*dnum +4))
    window.fill((27, 94, 31))
    mineSetter() #visual
    pygame.display.update()

#Draw plots on screen
def mineSetter(): #Buttons
    for j in range(dnum):
        for k in range(dnum):
            plot = pygame.draw.rect(window, (10, 48, 8), ((j*32) + (j*4) + 4, (k*32) + (k*4) + 4, block_side, block_side))
            pygame.display.update(plot)

#Code for clicking plots
def mineDigger():
    global run
    for tries in range(wnum):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            pos = pygame.mouse.get_pos()
            for m in range(dnum):
                for n in range(dnum):
                    x1 = (m*32) + (m*4) + 4
                    y1 = (n*32) + (n*4) + 4
                    x2 = x1 + 32
                    y2 = y1 + 32
                    if ((x1 < pos[0]) and (pos[0] < x2) and (y1 < pos[1]) and (pos[1] < y2)):
                        if ((x1 < pos[0]) and (pos[0] < x2) and (y1 < pos[1]) and (pos[1] < y2)):
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT: #If a certain plot is clicked
                                hitmarkerSound.play() #Plot click sound effect
                                hmr = window.blit(hitmarker, ((m*32) + (m*4) + 8, (n*32) + (n*4) + 8))
                                pygame.display.update(hmr)
                                pygame.time.delay(200)
                                if (mineList[m, n] == 0):
                                    dugPlot = pygame.draw.rect(window, (27, 94, 31), ((m*32) + (m*4) + 4, (n*32) + (n*4) + 4, block_side, block_side))
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                if (mineList[m, n] == 1):
                                    dugPlot = window.blit(mine1, (x1, y1)) #Display number
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                elif (mineList[m, n] == 2):
                                    dugPlot = window.blit(mine2, (x1, y1))
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                elif (mineList[m, n] == 3):
                                    dugPlot = window.blit(mine3, (x1, y1))
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                elif (mineList[m, n] == 4):
                                    dugPlot = window.blit(mine4, (x1, y1))
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                elif (mineList[m, n] == 5):
                                    dugPlot = window.blit(mine5, (x1, y1))
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                elif (mineList[m, n] == 6):
                                    dugPlot = window.blit(mine6, (x1, y1))
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                elif (mineList[m, n] == 7):
                                    dugPlot = window.blit(mine7, (x1, y1))
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                elif (mineList[m, n] == 8):
                                    dugPlot = window.blit(mine8, (x1, y1))
                                    pygame.display.update(dugPlot)
                                    if (m, n) not in scoreList:
                                        scoreList.append((m, n))
                                    else:
                                        pass
                                elif (mineList[m, n] == 9):
                                    dugPlot = window.blit(bomb, (x1, y1))
                                    pygame.display.update(dugPlot)
                                    pygame.time.delay(1500)
                                    explode.play() #Bomb sound effect

                                    for i in range(31):
                                        pygame.draw.circle(window, (255, 0, 0), (x1 + 16, y1 + 16), i) #Explosion animation
                                        pygame.display.update()
                                        time.sleep((0.00001)*dnum)

                                    for i in range(30, 61):
                                        pygame.draw.circle(window, (255, 0, 0), (x1 + 16, y1 + 16), i, 30)
                                        pygame.draw.circle(window, (252, 140, 3), (x1 + 16, y1 + 16), i - 30)
                                        pygame.display.update()
                                        time.sleep((0.00001)*dnum)

                                    for i in range(60, (51*dnum + 6)):
                                        pygame.draw.circle(window, (255, 0, 0), (x1 + 16, y1 + 16), i, 30)
                                        pygame.draw.circle(window, (252, 140, 3), (x1 + 16, y1 + 16), i - 30)
                                        pygame.draw.circle(window, (252, 186, 3), (x1 + 16, y1 + 16), i - 60)
                                        pygame.display.update()
                                        time.sleep((0.00001)*dnum)

                                    time.sleep(.5)
                                    for i in range(51*dnum + 6):
                                        blackcirc = pygame.draw.circle(window, (0, 0, 0), (x1 + 16, y1 + 16), i)
                                        pygame.display.update(blackcirc)
                                        if i == (36*dnum + 4):
                                            wasted.play() #Lost sound effect
                                        time.sleep((0.00001)*dnum)

                                    if dnum == 8:
                                        Ltext = font.render("YOU LOST!", 1, (255, 255, 255)) #Display "YOU LOST!"
                                        LC = Ltext.get_width()
                                        Ltext_render = window.blit(Ltext, (18*dnum +2 - LC/2, 4*block_side-60))

                                    elif dnum == 16:
                                        Ltext = font.render("YOU LOST!", 1, (255, 255, 255))
                                        LC = Ltext.get_width()
                                        Ltext_render = window.blit(Ltext, (18*dnum +2 - LC/2, 4*block_side-64))

                                    elif dnum == 24:
                                        Ltext = font.render("YOU LOST!", 1, (255, 255, 255))
                                        LC = Ltext.get_width()
                                        Ltext_render = window.blit(Ltext, (18*dnum +2 - LC/2, 4*block_side))

                                    pygame.display.update(Ltext_render) #Return back to mainmenu
                                    time.sleep(5)
                                    run = False
                                    mainmenu()

                            if (m, n) not in flagList:
                                if (m, n) not in scoreList:
                                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                                        dugPlot = window.blit(flag, (x1, y1))
                                        pygame.display.update(dugPlot)
                                        flagList.append((m, n))

                            elif (m, n) in flagList:
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                                    dugPlot = pygame.draw.rect(window, (10, 48, 8), ((m*32) + (m*4) + 4, (n*32) + (n*4) + 4, block_side, block_side))
                                    pygame.display.update(dugPlot)
                                    flagList.remove((m, n))

#Some code initialDig() depends on, helper function
def initDigCode(m, n):
    initdig = pygame.draw.rect(window, (27, 94, 31), ((m*32) + (m*4) + 4, (n*32) + (n*4) + 4, block_side, block_side))
    pygame.display.update(initdig)
    if (m, n) not in scoreList:
        scoreList.append((m, n))
    else:
        pass
    initList.append((m, n))

#First plot that the user clicks
def initialDig():
    t = 1
    while t == 1:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() #get mouse coord
            for j in range(dnum): #for all coords in the field
                for k in range(dnum):
                    plotList.append((j, k))
                    x1 = (j*32) + (j*4) + 4 #list coordinate to screen pixel coordinate conversion
                    y1 = (k*32) + (k*4) + 4
                    x2 = x1 + 32
                    y2 = y1 + 32
                    if ((x1 < pos[0]) and (pos[0] < x2) and (y1 < pos[1]) and (pos[1] < y2)): #if within plot boundary
                        if ((x1 < pos[0]) and (pos[0] < x2) and (y1 < pos[1]) and (pos[1] < y2)):
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT: #If a certain plot is clicked
                                hitmarkerSound.play() #Plot click sound effect
                                hmr = window.blit(hitmarker, ((j*32) + (j*4) + 8, (k*32) + (k*4) + 8))
                                pygame.display.update(hmr)
                                pygame.time.delay(200)
                                dugPlot = pygame.draw.rect(window, (27, 94, 31), ((j*32) + (j*4) + 4, (k*32) + (k*4) + 4, block_side, block_side))
                                pygame.display.update(dugPlot)
                                if (j, k) not in scoreList:
                                    scoreList.append((j, k))
                                else:
                                    pass
                                initList.append((j, k))

                                if (j+1, k) in plotList: #Clear any surrounding empty plots with zero mines around it
                                    m = j+1
                                    n = k
                                    initDigCode(m, n)

                                if (j+1, k+1) in plotList:
                                    m = j+1
                                    n = k+1
                                    initDigCode(m, n)

                                if (j, k+1) in plotList:
                                    m = j
                                    n = k+1
                                    initDigCode(m, n)

                                if (j-1, k) in plotList:
                                    m = j-1
                                    n = k
                                    initDigCode(m, n)

                                if (j-1, k-1) in plotList:
                                    m = j-1
                                    n = k-1
                                    initDigCode(m, n)

                                if (j, k-1) in plotList:
                                    m = j
                                    n = k-1
                                    initDigCode(m, n)

                                if (j+1, k-1) in plotList:
                                    m = j+1
                                    n = k-1
                                    initDigCode(m, n)

                                if (j-1, k+1) in plotList:
                                    m = j-1
                                    n = k+1
                                    initDigCode(m, n)

                                if (j, k+2) in plotList:
                                    m = j
                                    n = k+2
                                    initDigCode(m, n)

                                if (j+1, k+2) in plotList:
                                    m = j+1
                                    n = k+2
                                    initDigCode(m, n)

                                if (j-1, k+2) in plotList:
                                    m = j-1
                                    n = k+2
                                    initDigCode(m, n)

                                if (j, k-2) in plotList:
                                    m = j
                                    n = k-2
                                    initDigCode(m, n)

                                if (j+1, k-2) in plotList:
                                    m = j+1
                                    n = k-2
                                    initDigCode(m, n)

                                if (j-1, k-2) in plotList:
                                    m = j-1
                                    n = k-2
                                    initDigCode(m, n)

                                if (j-2, k) in plotList:
                                    m = j-2
                                    n = k
                                    initDigCode(m, n)

                                if (j-2, k+1) in plotList:
                                    m = j-2
                                    n = k+1
                                    initDigCode(m, n)

                                if (j-2, k-1) in plotList:
                                    m = j-2
                                    n = k-1
                                    initDigCode(m, n)

                                if (j+2, k) in plotList:
                                    m = j+2
                                    n = k
                                    initDigCode(m, n)

                                if (j+2, k-1) in plotList:
                                    m = j+2
                                    n = k-1
                                    initDigCode(m, n)

                                if (j+2, k+1) in plotList:
                                    m = j+2
                                    n = k+1
                                    initDigCode(m, n)

                                t -= 1

def minePicker(): #Randomly gives mine locations
    j = random.randrange(dnum)
    k = random.randrange(dnum)
    if (j, k) in mineList:
        minePicker()
    if (j, k) in initList:
        minePicker()
    else:
        mineList[j, k] = 9

def mineScanner(): #Gives mine proximity numbers
    for (j, k) in mineList:
        if mineList[j, k] == 9:
            pass
        else:
            prox = 0

            if (j+1, k) in mineList:
                if mineList[j+1, k] == 9:
                    prox += 1
                else:
                    pass

            if (j+1, k+1) in mineList:
                if mineList[j+1, k+1] == 9:
                    prox += 1
                else:
                    pass

            if (j, k+1) in mineList:
                if mineList[j, k+1] == 9:
                    prox += 1
                else:
                    pass

            if (j-1, k) in mineList:
                if mineList[j-1, k] == 9:
                    prox += 1
                else:
                    pass

            if (j-1, k-1) in mineList:
                if mineList[j-1, k-1] == 9:
                    prox += 1
                else:
                    pass

            if (j, k-1) in mineList:
                if mineList[j, k-1] == 9:
                    prox += 1
                else:
                    pass

            if (j+1, k-1) in mineList:
                if mineList[j+1, k-1] == 9:
                    prox += 1
                else:
                    pass

            if (j-1, k+1) in mineList:
                if mineList[j-1, k+1] == 9:
                    prox += 1
                else:
                    pass

            mineList[j, k] = prox

    for (j, k) in initList:
        x1 = (j*32) + (j*4) + 4
        y1 = (k*32) + (k*4) + 4

        if (mineList[j, k] == 0):
            dugPlot = pygame.draw.rect(window, (27, 94, 31), ((j*32) + (j*4) + 4, (k*32) + (k*4) + 4, block_side, block_side))
            pygame.display.update(dugPlot)

        elif (mineList[j, k] == 1):
            dugPlot = window.blit(mine1, (x1, y1))
            pygame.display.update(dugPlot)

        elif (mineList[j, k] == 2):
            dugPlot = window.blit(mine2, (x1, y1))
            pygame.display.update(dugPlot)

        elif (mineList[j, k] == 3):
            dugPlot = window.blit(mine3, (x1, y1))
            pygame.display.update(dugPlot)

        elif (mineList[j, k] == 4):
            dugPlot = window.blit(mine4, (x1, y1))
            pygame.display.update(dugPlot)

        elif (mineList[j, k] == 5):
            dugPlot = window.blit(mine5, (x1, y1))
            pygame.display.update(dugPlot)

        elif (mineList[j, k] == 6):
            dugPlot = window.blit(mine6, (x1, y1))
            pygame.display.update(dugPlot)

        elif (mineList[j, k] == 7):
            dugPlot = window.blit(mine7, (x1, y1))
            pygame.display.update(dugPlot)

        elif (mineList[j, k] == 8):
            dugPlot = window.blit(mine8, (x1, y1))
            pygame.display.update(dugPlot)

def minePlacer():
    for i in range(mnum):
        minePicker()
    for j in range(dnum):
        for k in range(dnum):
            if (j, k) in mineList:
                mineList[j, k] = 9
            else:
                mineList[j, k] = 0

def zeroCode(m, n): #fuction that zeroClearer is dependent on. Helper function
    initList.append((m, n))
    x1 = (m*32) + (m*4) + 4
    y1 = (n*32) + (n*4) + 4
    if (mineList[m, n] == 0):
        dugPlot = pygame.draw.rect(window, (27, 94, 31), ((m*32) + (m*4) + 4, (n*32) + (n*4) + 4, block_side, block_side))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass
    elif (mineList[m, n] == 1):
        dugPlot = window.blit(mine1, (x1, y1))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass
    elif (mineList[m, n] == 2):
        dugPlot = window.blit(mine2, (x1, y1))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass
    elif (mineList[m, n] == 3):
        dugPlot = window.blit(mine3, (x1, y1))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass
    elif (mineList[m, n] == 4):
        dugPlot = window.blit(mine4, (x1, y1))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass
    elif (mineList[m, n] == 5):
        dugPlot = window.blit(mine5, (x1, y1))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass
    elif (mineList[m, n] == 6):
        dugPlot = window.blit(mine6, (x1, y1))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass
    elif (mineList[m, n] == 7):
        dugPlot = window.blit(mine7, (x1, y1))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass
    elif (mineList[m, n] == 8):
        dugPlot = window.blit(mine8, (x1, y1))
        pygame.display.update(dugPlot)
        if (m, n) not in scoreList:
            scoreList.append((m, n))
        else:
            pass

def zeroClearer():
    for (j, k) in initList:
        if (j+1, k) not in initList:
            if (j+1, k) in mineList:
                if mineList[j, k] == 0:
                    m = j+1
                    n = k
                    zeroCode(m, n)

        if (j+1, k+1) not in initList:
            if (j+1, k+1) in mineList:
                if mineList[j, k] == 0:
                    m = j+1
                    n = k+1
                    zeroCode(m, n)

        if (j, k+1) not in initList:
            if (j, k+1) in mineList:
                if mineList[j, k] == 0:
                    m = j
                    n = k+1
                    zeroCode(m, n)

        if (j-1, k) not in initList:
            if (j-1, k) in mineList:
                if mineList[j, k] == 0:
                    m = j-1
                    n = k
                    zeroCode(m, n)

        if (j-1, k-1) not in initList:
            if (j-1, k-1) in mineList:
                if mineList[j, k] == 0:
                    m = j-1
                    n = k-1
                    zeroCode(m, n)

        if (j, k-1) not in initList:
            if (j, k-1) in mineList:
                if mineList[j, k] == 0:
                    m = j
                    n = k-1
                    zeroCode(m, n)

        if (j+1, k-1) not in initList:
            if (j+1, k-1) in mineList:
                if mineList[j, k] == 0:
                    m = j+1
                    n = k-1
                    zeroCode(m, n)

        if (j-1, k+1) not in initList:
            if (j-1, k+1) in mineList:
                if mineList[j, k] == 0:
                    m = j-1
                    n = k+1
                    zeroCode(m, n)

#run game code
def runGame():
    redrawWindow()
    initialDig()
    minePlacer()
    mineScanner()
    zeroClearer()

    run = True
    while run:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
            mainmenu()

        mineDigger()

        if len(scoreList) == wnum: #Print "You Won!", Do this if you win

            time.sleep(.5)

            for i in range(51*dnum + 6):
                blackcirc = pygame.draw.circle(window, (0, 0, 0), (int((dnum/2)*block_side + 6), int((dnum/2)*block_side + 6)), i)
                pygame.display.update(blackcirc)
                if i == (36*dnum + 4):
                    yay.play()
                time.sleep((0.00001)*dnum)

            if dnum == 8:
                Wtext = font.render("YOU WON!", 1, (255, 255, 255))
                WC = Wtext.get_width()
                Wtext_render = window.blit(Wtext, (18*dnum +2 - WC/2, 4*block_side-60))

            elif dnum == 16:
                Wtext = font.render("YOU WON!", 1, (255, 255, 255))
                WC = Wtext.get_width()
                Wtext_render = window.blit(Wtext, (18*dnum +2 - WC/2, 4*block_side-64))

            elif dnum == 24:
                Wtext = font.render("YOU WON!", 1, (255, 255, 255))
                WC = Wtext.get_width()
                Wtext_render = window.blit(Wtext, (18*dnum +2 - WC/2, 4*block_side))

            pygame.display.update(Wtext_render)
            time.sleep(4)
            run = False
            mainmenu()

def blips(i):
    pygame.gfxdraw.filled_circle(window, 290, 290, 2, (0, 255, 0))
#1 Blue                                                                   Radial coordinate angles
    pygame.gfxdraw.filled_circle(window, 470, 290, 8, (0, 255, 255, 50))  #pi
    pygame.gfxdraw.filled_circle(window, 420, 340, 8, (0, 255, 255, 50))  #21.038
    pygame.gfxdraw.filled_circle(window, 300, 140, 8, (0, 255, 255, 50))  #-86.186
    pygame.gfxdraw.filled_circle(window, 290, 540, 8, (0, 255, 255, 50))  #90
    pygame.gfxdraw.filled_circle(window, 460, 160, 8, (0, 255, 255, 50))  #-37.405
    pygame.gfxdraw.filled_circle(window, 182, 300, 8, (0, 255, 255, 50))  #174.71
    pygame.gfxdraw.filled_circle(window, 125, 350, 8, (0, 255, 255, 50))  #160.02
    pygame.gfxdraw.filled_circle(window, 130, 450, 8, (0, 255, 255, 50))  #135
    pygame.gfxdraw.filled_circle(window, 50, 350, 8, (0, 255, 255, 50))   #165.96
#2
    pygame.gfxdraw.filled_circle(window, 470, 290, 5, (0, 255, 255, 100)) #pi
    pygame.gfxdraw.filled_circle(window, 420, 340, 5, (0, 255, 255, 100)) #21.038
    pygame.gfxdraw.filled_circle(window, 300, 140, 5, (0, 255, 255, 100)) #-86.186
    pygame.gfxdraw.filled_circle(window, 290, 540, 5, (0, 255, 255, 100)) #90
    pygame.gfxdraw.filled_circle(window, 460, 160, 5, (0, 255, 255, 100)) #-37.405
    pygame.gfxdraw.filled_circle(window, 182, 300, 5, (0, 255, 255, 100)) #174.71
    pygame.gfxdraw.filled_circle(window, 125, 350, 5, (0, 255, 255, 100)) #160.02
    pygame.gfxdraw.filled_circle(window, 130, 450, 5, (0, 255, 255, 100)) #135
    pygame.gfxdraw.filled_circle(window, 50, 350, 5, (0, 255, 255, 100))  #165.96
#3
    pygame.gfxdraw.filled_circle(window, 470, 290, 2, (0, 255, 255, 255)) #pi
    pygame.gfxdraw.filled_circle(window, 420, 340, 2, (0, 255, 255, 255)) #21.038
    pygame.gfxdraw.filled_circle(window, 300, 140, 2, (0, 255, 255, 255)) #-86.186
    pygame.gfxdraw.filled_circle(window, 290, 540, 2, (0, 255, 255, 255)) #90
    pygame.gfxdraw.filled_circle(window, 460, 160, 2, (0, 255, 255, 255)) #-37.405
    pygame.gfxdraw.filled_circle(window, 182, 300, 2, (0, 255, 255, 255)) #174.71
    pygame.gfxdraw.filled_circle(window, 125, 350, 2, (0, 255, 255, 255)) #160.02
    pygame.gfxdraw.filled_circle(window, 130, 450, 2, (0, 255, 255, 255)) #135
    pygame.gfxdraw.filled_circle(window, 50, 350, 2, (0, 255, 255, 255))  #165.96
#4 Red
    pygame.gfxdraw.filled_circle(window, 128, 190, 8, (255, 0, 0, 50))    #pi
    pygame.gfxdraw.filled_circle(window, 260, 120, 8, (255, 0, 0, 50))    #21.038
    pygame.gfxdraw.filled_circle(window, 300, 400, 8, (255, 0, 0, 50))    #-86.186
    pygame.gfxdraw.filled_circle(window, 290, 500, 8, (255, 0, 0, 50))    #90
    pygame.gfxdraw.filled_circle(window, 60, 250, 8, (255, 0, 0, 50))     #-37.405
    pygame.gfxdraw.filled_circle(window, 410, 470, 8, (255, 0, 0, 50))    #174.71
#5
    pygame.gfxdraw.filled_circle(window, 128, 190, 5, (255, 0, 0, 100))   #pi
    pygame.gfxdraw.filled_circle(window, 260, 120, 5, (255, 0, 0, 100))   #21.038
    pygame.gfxdraw.filled_circle(window, 300, 400, 5, (255, 0, 0, 100))   #-86.186
    pygame.gfxdraw.filled_circle(window, 290, 500, 5, (255, 0, 0, 100))   #90
    pygame.gfxdraw.filled_circle(window, 60, 250, 5, (255, 0, 0, 100))    #-37.4056
    pygame.gfxdraw.filled_circle(window, 410, 470, 5, (255, 0, 0, 100))   #174.71
#6
    pygame.gfxdraw.filled_circle(window, 128, 190, 2, (255, 0, 0, 255))   #pi
    pygame.gfxdraw.filled_circle(window, 260, 120, 2, (255, 0, 0, 255))   #21.038
    pygame.gfxdraw.filled_circle(window, 300, 400, 2, (255, 0, 0, 255))   #-86.186
    pygame.gfxdraw.filled_circle(window, 290, 500, 2, (255, 0, 0, 255))   #90
    pygame.gfxdraw.filled_circle(window, 60, 250, 2, (255, 0, 0, 255))    #-37.4056
    pygame.gfxdraw.filled_circle(window, 410, 470, 2, (255, 0, 0, 255))   #174.71

vectInUse = vectc

def preSonar2():
    window.fill(Dark_blue)
    pygame.gfxdraw.filled_circle(window, 290, 290, 270, Dark_green)
    for i in range(1, 6):
        pygame.gfxdraw.aacircle(window, 290, 290, 45*i, Light_green)
    pygame.gfxdraw.aacircle(window, 290, 290, 270, Light_green)
    pygame.gfxdraw.aacircle(window, 290, 290, 269, Light_green)
    pygame.gfxdraw.aacircle(window, 290, 290, 268, Light_green)
    for i in range(16):
        vect2 = (np.matmul(vecta, np.linalg.matrix_power(rot, i)))
        x = vect2[0] + 290
        y = vect2[1] + 290
        pygame.draw.aaline(window, Light_green, (290, 290), (x, y), 3)
    #0
    Ztext = numfont.render("0", 1, (0, 255, 0))
    ZC = Ztext.get_width()
    window.blit(Ztext, (290 - ZC/2, 5))
    #45
    Ftext = numfont.render("45", 1, (0, 255, 0))
    window.blit(Ftext, (485, 85))
    #90
    Ntext = numfont.render("90", 1, (0, 255, 0))
    NC = Ntext.get_height()
    window.blit(Ntext, (564, 290 - NC/2))
    #135
    Ttext = numfont.render("135", 1, (0, 255, 0))
    window.blit(Ttext, (485, 485))
    #180
    Etext = numfont.render("180", 1, (0, 255, 0))
    EC = Etext.get_width()
    window.blit(Etext, (290 - EC/2, 562))
    #225
    TTtext = numfont.render("225", 1, (0, 255, 0))
    window.blit(TTtext, (82, 485))
    #270
    Stext = numfont.render("270", 1, (0, 255, 0))
    SC = Stext.get_height()
    window.blit(Stext, (3, 290 - SC/2))
    #315
    FFtext = numfont.render("315", 1, (0, 255, 0))
    window.blit(FFtext, (80, 85))

def postSonar2():
    global EasyButton, MediumButton, HardButton, BackButton
    Title = font.render("Select your difficulty", 1, (255, 255, 255))
    TC = Title.get_width()
    Title_render = window.blit(Title, (290 - TC/2, 2*block_side))
    pygame.display.update(Title_render)

    EasyButton = button((148, 18, 18), 5*block_side + 20, 6*block_side, 7*block_side, 2*block_side, 'Easy - 8x8')
    EasyButton.draw(window, (0, 0, 0))

    MediumButton = button((148, 18, 18), 5*block_side + 20, 10*block_side, 7*block_side, 2*block_side, 'Medium - 16x16')
    MediumButton.draw(window, (0, 0, 0))

    HardButton = button((148, 18, 18), 5*block_side + 20, 14*block_side, 7*block_side, 2*block_side, 'Hard - 24x24')
    HardButton.draw(window, (0, 0, 0))

    BackButton = button((148, 18, 18), block_side, block_side, 3*block_side, block_side + 20, 'Back')
    BackButton.draw(window, (0, 0, 0))

    pygame.display.update()

def difficulty():
    global dnum, mnum, wnum, scoreList, initList, plotList, mineList, vectInUse
    diff = True
    while diff:
        pygame.display.set_caption("Minesweeper")
        window = pygame.display.set_mode((580, 580))

        if vectInUse is vecta:
            vectInUse = vectb
        elif vectInUse is vectb:
            vectInUse = vectc
        elif vectInUse is vectc:
            vectInUse = vectd
        else:
            vectInUse = vecta

        for i in range(90):
            preSonar2()
            pygame.time.delay(1)
            e3 = math.cos(math.radians(i))
            e4 = math.sin(math.radians(i))
            rot2 = np.array([[e3, e4], [-(e4), e3]])
            vect3 = np.matmul(vectInUse, rot2)
            x1 = vect3[0] + 290
            y1 = vect3[1] + 290
            pygame.draw.aaline(window, (0, 255, 0), (290, 290), (x1, y1), 3)
            blips(i)
            pygame.time.delay(3)
            if i == 45:
                if vectInUse is vectc:
                    sonar.play()
            postSonar2()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            diff = False
            mainmenu()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #quit by clicking "X" button with no error
                diff = False
                sys.exit()

            pos = pygame.mouse.get_pos() #Mouse clicks on screen

            if event.type == pygame.MOUSEBUTTONDOWN:

                if EasyButton.isOver(pos):
                    dnum = 8
                    mnum = 13
                    wnum = 51
                    diff = False
                    scoreList = []
                    initList = []
                    plotList = []
                    mineList = {}
                    runGame()

                if MediumButton.isOver(pos):
                    dnum = 16
                    mnum = 52
                    wnum = 204
                    diff = False
                    scoreList = []
                    initList = []
                    plotList = []
                    mineList = {}
                    runGame()

                if HardButton.isOver(pos):
                    dnum = 24
                    mnum = 117
                    wnum = 459
                    diff = False
                    scoreList = []
                    initList = []
                    plotList = []
                    mineList = {}
                    runGame()

                if BackButton.isOver(pos):
                    diff = False
                    mainmenu()

def preSonar1():
    global dnum
    window.fill(Dark_blue)
    pygame.gfxdraw.filled_circle(window, 290, 290, 270, Dark_green)
    for i in range(1, 6):
        pygame.gfxdraw.aacircle(window, 290, 290, 45*i, Light_green)
    pygame.gfxdraw.aacircle(window, 290, 290, 270, Light_green)
    pygame.gfxdraw.aacircle(window, 290, 290, 269, Light_green)
    pygame.gfxdraw.aacircle(window, 290, 290, 268, Light_green)
    for i in range(16):
        vect2 = (np.matmul(vecta, np.linalg.matrix_power(rot, i)))
        x = vect2[0] + 290
        y = vect2[1] + 290
        pygame.draw.aaline(window, Light_green, (290, 290), (x, y), 3)
    #0
    Ztext = numfont.render("0", 1, (0, 255, 0))
    ZC = Ztext.get_width()
    window.blit(Ztext, (290 - ZC/2, 5))
    #45
    Ftext = numfont.render("45", 1, (0, 255, 0))
    window.blit(Ftext, (485, 85))
    #90
    Ntext = numfont.render("90", 1, (0, 255, 0))
    NC = Ntext.get_height()
    window.blit(Ntext, (564, 290 - NC/2))
    #135
    Ttext = numfont.render("135", 1, (0, 255, 0))
    window.blit(Ttext, (485, 485))
    #180
    Etext = numfont.render("180", 1, (0, 255, 0))
    EC = Etext.get_width()
    window.blit(Etext, (290 - EC/2, 562))
    #225
    TTtext = numfont.render("225", 1, (0, 255, 0))
    window.blit(TTtext, (82, 485))
    #270
    Stext = numfont.render("270", 1, (0, 255, 0))
    SC = Stext.get_height()
    window.blit(Stext, (3, 290 - SC/2))
    #315
    FFtext = numfont.render("315", 1, (0, 255, 0))
    window.blit(FFtext, (80, 85))

def postSonar1():
    global PlayButton, ExitButton
    Title = font.render("Minesweeper by Raafi Rahman", 1, (255, 255, 255))
    TC = Title.get_width()
    window.blit(Title, (290 - TC/2, 2*block_side))

    PlayButton = button((148, 18, 18), 5*block_side + 20, 6*block_side, 7*block_side, 2*block_side, 'Play')
    PlayButton.draw(window, (0, 0, 0))

    ExitButton = button((148, 18, 18), 5*block_side + 20, 10*block_side, 7*block_side, 2*block_side, 'Exit')
    ExitButton.draw(window, (0, 0, 0))

    pygame.display.update()

def mainmenu():
    global dnum, window, vectInUse
    clock = pygame.time.Clock()
    clock.tick(120)
    menu = True
    while menu:
        pygame.display.set_caption("Minesweeper")
        window = pygame.display.set_mode((580, 580))

        if vectInUse is vecta:
            vectInUse = vectb
        elif vectInUse is vectb:
            vectInUse = vectc
        elif vectInUse is vectc:
            vectInUse = vectd
        else:
            vectInUse = vecta

        for i in range(90):
            preSonar1()
            pygame.time.delay(2)
            e3 = math.cos(math.radians(i))
            e4 = math.sin(math.radians(i))
            rot2 = np.array([[e3, e4], [-(e4), e3]])
            vect3 = np.matmul(vectInUse, rot2)
            x1 = vect3[0] + 290
            y1 = vect3[1] + 290
            pygame.draw.aaline(window, (0, 255, 0), (290, 290), (x1, y1), 3)
            blips(i)
            pygame.time.delay(3)
            if i == 45:
                if vectInUse is vectc:
                    sonar.play()
            postSonar1()

        for event in pygame.event.get():

            if event.type == pygame.QUIT: #quit by clicking "X" button with no error
                menu = False
                sys.exit()

            pos = pygame.mouse.get_pos() #Mouse clicks on screen

            if event.type == pygame.MOUSEBUTTONDOWN:

                if PlayButton.isOver(pos):
                    pygame.display.flip()
                    window.fill((27, 94, 31))
                    pygame.display.update()
                    menu = False
                    difficulty()

                if ExitButton.isOver(pos):
                    pygame.time.delay(500)
                    menu = False
                    sys.exit()

if __name__ == "__main__":
    mainmenu()