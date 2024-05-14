"""
Game name: Back in Time
Project: Application Development and Emerging Technology
Professor: Gary Bato-ey

Frames: 30 fps
walking animation(character and enemy): 7 frames/images
characters size(character and enemy): 130x80 pixels

developers:
    1. Christian Vaydal
    2. Aeron Segobia
    3. Ethan Diego Lim

Date started: April 16, 2024
"""

import pygame
from character import *
from object import *
from create import Create 
from camera import Camera
from Data.read import Read
from UI import UI
from loading import Loading
from timer import Timer

# IMPORT MAPS
from Maps import baseMap, Map_2, Map_3, Map_4

# initialize pygame
pygame.init()
pygame.mixer.init()

# screen
windowSize = {'width': 700, 'height': 500} # size of the display
window = pygame.display.set_mode((windowSize['width'], windowSize['height']))
pygame.display.set_caption('Back In Time')

# clock and FPS - frame per second
clock = pygame.time.Clock()
fps = 30 # 30 frames per second

# audios / sfx / bg musics
bg1 = pygame.mixer.music.load('audio/bg2.mp3') # audio
pygame.mixer.music.play(-1) # play bg music in loop

select_item = pygame.mixer.Sound('audio/select.wav') # for selecting items, etc.
selected_item = pygame.mixer.Sound('audio/selected.wav') # selected items, etc.

# TImer
timer = Timer(fps)

# Program pages
pages = ['intro', 'main-menu', 'settings', 'credits', 'selectPlayer', 'in-game', 'pause-game', 'outro', 'exit', 'error_message']
currentPage = pages[0]

# loading and checking resources
load = Loading((windowSize['width'] - 500) / 2, (windowSize['height'] - 200), 500, 15)

# MAP
base = baseMap.TileMap(25, 0, 0)
map_2 = Map_2.TileMap(25, 0, 0)
map_3 = Map_3.TileMap(25, 0, 0)
map_4 = Map_4.TileMap(25, 0, 0)

# GUIs (not yet draw)
itemsGUI = UI((windowSize['width'] - 244) / 2, (windowSize['height'] - 70), 244, 60, 'itemsbar_6')

# pause button
pauseButton = UI((windowSize['width'] - 60), 10, 40, 40, 'pause_btn')

# player Icon and health bar
playerIcon = UI(10, 10, 90, 90, 'player_frame2')
# healthbar = UI(100, 10, 128, 32, 'life_bar4') # uncomment this later

listGUIs = [itemsGUI, pauseButton, playerIcon] # healthbar

# PLAYER
player = Player(((windowSize['width'] - 50) / 2), ((windowSize['height'] - 50) / 2), 50, 50)

# read object data from json file data
readData = Read('Data/data.json')
readData.read() # read all data

readData.strToTuple('Base') # make all string tuple in Map1 to tuple
readData.strToTuple('Map2')
readData.strToTuple('Map3')
readData.strToTuple('Map4')
readData.strToTuple('Enemies_m2') # read the tuple(positions) of the enemies
readData.strToTuple('mainMenu')
readData.strToTuple('settings')
readData.strToTuple('credits')
readData.strToTuple('pauseGame')
readData.strToTuple('SelectPlayer')

# CREATIONS

# for loading screen / intro
title = [
    Object((windowSize['width'] - 200) / 2, (windowSize['height'] - 350) / 2, 200, 200, 'animated', 'title_3'),
    Object((windowSize['width'] - 192) / 2, windowSize['height'] - 150, 192, 48, 'other', 'credits')
]

######## CREATE MAIN MENU #########
create_menu = Create(window, player, readData.data['mainMenu'])
create_menu.create_UI()

######## CREATE SETTINGS #########
create_settings = Create(window, player, readData.data['settings'])
create_settings.create_UI()

######## CREATE CREDITS #########
create_credits = Create(window, player, readData.data['credits'])
create_credits.create_UI()

######## CREATE PAUSE #########
create_pause = Create(window, player, readData.data['pauseGame'])
create_pause.create_UI()

######## CREATE SELECT PLAYER #########
create_selectPlayer = Create(window, player, readData.data['SelectPlayer'])
create_selectPlayer.create_UI()

######## CREATE MAPS #########

# create objects for blocks and other objects - Map 1 / base
create_base = Create(window, player, readData.data['Base'])
create_base.create()

# create objects for blocks and other objects - Map 2
create_map2 = Create(window, player, readData.data['Map2'])
create_map2.create()

# create objects for blocks and other objects - Map 3
create_map3 = Create(window, player, readData.data['Map3'])
create_map3.create()

create_map4 = Create(window, player, readData.data['Map4'])
create_map4.create()

######## CREATE ENEMIES #########

# enemies for map 2
enemies_map2 = Create(window, player, readData.data['Enemies_m2'])
enemies_map2.create_enemies()

# camera
camera = Camera(player, windowSize)

# Listed all objects, maps and enemies for camera tracking
allObjects1 = create_base.listofObjects+[base]
allObjects2 = create_map2.listofObjects+[map_2]+enemies_map2.listEnemies
allObjects3 = create_map3.listofObjects+[map_3]
allObjects4 = create_map4.listofObjects+[map_4]

# create.listofObjects is a list of all objecst
# listenemies is a list of all enemies
# listOfMap is a list of map tiles

# draw base map function
def draw_base():
    global currentPage

    window.fill((10, 10, 10))

    # camera
    camera.move(allObjects1)

    # map for the base map
    base.drawMap(window)

    # draw object
    create_base.draw()
    pause = create_base.pauseGame() # if player click esc - pause

    # draw player
    player.draw(window, create_base.listofObjects[1:])
    player.navigate()

    for guis in listGUIs:
        guis.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    pygame.display.flip()

# draw MAP 2 funtion
def draw_map2():
    global currentPage
    window.fill((10, 10, 10))

    # camera for map 2
    camera.move(allObjects2)

    # draw map 2
    map_2.drawMap(window)

    # draw objects
    create_map2.draw()
    pause = create_map2.pauseGame()

    # enemies
    enemies_map2.draw_enemy(create_map2.listofObjects[1:]) # uncomment later

    # draw player
    player.draw(window, create_map2.listofObjects[1:])
    player.navigate()
    player.handleFight(enemies_map2.listEnemies)

    for guis in listGUIs:
        guis.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    pygame.display.flip()

# not yet done
def draw_map3(): 
    global currentPage
    window.fill((10, 10, 10))

    map_3.drawMap(window)

    create_map3.draw()
    pause = create_map3.pauseGame()

    # draw player in map3
    player.draw(window, create_map3.listofObjects[1:])
    player.navigate()

    # camera fot map 3
    camera.move(allObjects3)

    for gui in listGUIs:
        gui.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    pygame.display.flip()

def draw_map4():
    global currentPage

    window.fill((10, 10, 10))

    # draw the map
    map_4.drawMap(window)

    create_map4.draw()
    pause = create_map4.pauseGame()

    player.draw(window, create_map4.listofObjects[1:])
    player.navigate()


    camera.move(allObjects4)

    for gui in listGUIs:
        gui.draw(window)

    if pause:
        currentPage = pages[6]

    pygame.display.flip()

# pause the game
def PauseGame():
    global currentPage
    window.fill((10, 10, 10))

    create_pause.draw_ui()
    selected = create_pause.Select()

    keys = pygame.key.get_just_pressed()

    if keys[pygame.K_ESCAPE]: # back to game
        selected_item.play()
        currentPage = pages[5]
    
    if selected == 0:
        currentPage = pages[5] # back to game
    elif selected == 1:
        currentPage = pages[1] # navigate to main menu

    pygame.display.flip()

# main menu of the game
def mainMenu():
    global currentPage

    window.fill((10, 10, 10))

    create_menu.draw_ui()
    selected = create_menu.Select()

    if selected == 0: # navigate to Select player 
        if player.name != "":
            currentPage = pages[5]
        else:
            currentPage = pages[4]
    elif selected == 1: # credits
        currentPage = pages[3]
    elif selected == 2: # settings
        currentPage = pages[2]
    elif selected == 3: # exit game
        currentPage = pages[-1]

    pygame.display.flip()

# settings
def settings():
    global currentPage

    window.fill((10, 10, 10))

    create_settings.draw_ui()
    selected = create_settings.Select()

    if selected == 2: # if save is selected
        currentPage = pages[1] # back to main menu
        selected = 0

    pygame.display.flip()

# display credits
def credits():
    global currentPage
    window.fill((10, 10, 10))

    create_credits.draw_ui()

    keys = pygame.key.get_just_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
        selected_item.play() # play audio selected
        currentPage = pages[1]

    pygame.display.flip()

# display selecting players / characters
def selectPlayer():
    global currentPage
    window.fill((10, 10, 10))

    create_selectPlayer.draw_ui()
    character = create_selectPlayer.Select()

    keys = pygame.key.get_just_pressed()

    if keys[pygame.K_SPACE]:
        player.location = 'base'
        if character == 0:
            player.name = 'johny'
        elif character == 1:
            player.name = 'jicky'
        elif character == 2:
            player.name = 'jp'
        elif character == 3:
            player.name = 'jayson'
        else:
            raise Exception('Player not found')
        player.loadImages()
        player.flipImage()
        currentPage = pages[5] # navigate to game page
    elif keys[pygame.K_ESCAPE]:
        selected_item.play() # play audio selected
        currentPage = pages[1] # back to main menu

    pygame.display.flip()

# opening scene function / credits and loading
def Opening():
    global currentPage, title

    window.fill((10, 10, 10))

    # draw animated title
    for ttle in title:
        ttle.draw(window)

    # slow down the loading animation
    load.draw(window)
    if timer.coolDown(5):
        check = load.checkResources()
        if check:
            if timer.coolDown(5):
                player.location = 'base'
                currentPage = pages[1] # navigate to main menu
                del title # remove or delete all loaded images

    pygame.display.flip()

# for testing
fpsCollected = [] # collecting frames per second value

# main function
def main():
    run = True

    while run:

        # fps of the game
        clock.tick(fps)

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # draw the display
        # intro
        if currentPage == pages[0]:
            Opening() # opening screen / loading and checking all resources
        elif currentPage == pages[1]:
            mainMenu() # main menu
        elif currentPage == pages[2]: # settings
            settings()
        elif currentPage == pages[3]: # show credits
            credits()
        elif currentPage == pages[4]: # select player or characters
            selectPlayer()
        # in-game
        elif currentPage == pages[5]: # go to game screen
        # draw the display
            if player.location == 'base': # map 1
                draw_base()
            elif player.location == 'map2': # map 2
                draw_map2()
            elif player.location == 'map3': # map 3 - not yet done
                draw_map3()
            elif player.location == 'map4':
                draw_map4()
        elif currentPage == pages[6]:
            PauseGame()
        elif currentPage == pages[-1]: # exit game
            run = False

        # for testing
        chechFPS(round(clock.get_fps(), 2))

    # quit program after the loop
    print('fps timeline:',fpsCollected)
    print('lowest:', min(fpsCollected), '\nHighest:', max(fpsCollected), '\nLocation:', player.location)
    pygame.quit()

# function for testing

# frame drops test
def chechFPS(frames):
    if frames not in fpsCollected and frames >= 1:
        fpsCollected.append(frames)

# main program
if __name__=='__main__':
    main()