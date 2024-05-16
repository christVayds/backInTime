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
from character_cython import *
from object_cython import *
from create_cython import *
from camera_cython import Camera
from Data.read import Read
from ui_cython import UI
from loading_cython import Loading
from timer_cython import Timer
from music_cython import Music

# IMPORT MAPS
import base_cython
import map2_cython
import map3_cython
import map4_cython

print("This is cythonized version (Optimized powered by C programming language)")

# initialize pygame
pygame.init()
pygame.mixer.init()

# screen
cdef windowSize = {'width': 700, 'height': 500} # size of the display
cdef window = pygame.display.set_mode((windowSize['width'], windowSize['height']))
pygame.display.set_caption('Back In Time')

# clock and FPS - frame per second
cdef clock = pygame.time.Clock()
cdef int fps = 30 # 30 frames per second

# audios / sfx / bg musics
cdef music = Music()
cdef select_item = pygame.mixer.Sound('audio/select.wav') # for selecting items, etc.
cdef selected_item = pygame.mixer.Sound('audio/selected.wav') # selected items, etc.

# TImer
cdef timer = Timer(fps)

# Program pages
cdef pages = ['intro', 'main-menu', 'settings', 'credits', 'selectPlayer', 'in-game', 'pause-game', 'outro', 'exit', 'error_message']
cdef currentPage = pages[0]

# loading and checking resources
cdef load = Loading((windowSize['width'] - 500) / 2, (windowSize['height'] - 200), 500, 15)

# MAP
cdef base = base_cython.TileMap(25, 0, 0)
cdef map_2 = map2_cython.TileMap(25, 0, 0)
cdef map_3 = map3_cython.TileMap(25, 0, 0)
cdef map_4 = map4_cython.TileMap(25, 0, 0)

# GUIs (not yet draw)
cdef itemsGUI = UI((windowSize['width'] - 244) / 2, (windowSize['height'] - 70), 244, 60, 'itemsbar_6')

# pause button
cdef pauseButton = UI((windowSize['width'] - 60), 10, 40, 40, 'pause_btn')

# player Icon and health bar
cdef playerIcon = UI(10, 10, 90, 90, 'player_frame2')
# healthbar = UI(100, 10, 128, 32, 'life_bar4') # uncomment this later

cdef listGUIs = [itemsGUI, pauseButton, playerIcon] # healthbar

# PLAYER
cdef player = Player(((windowSize['width'] - 50) / 2), ((windowSize['height'] - 50) / 2), 50, 50)

# read object data from json file data
cdef readData = Read('Data/data.json')
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
cdef title = [
    Object((windowSize['width'] - 200) / 2, (windowSize['height'] - 350) / 2, 200, 200, 'animated', 'title_3'),
    Object((windowSize['width'] - 192) / 2, windowSize['height'] - 150, 192, 48, 'other', 'credits')
]

######## CREATE MAIN MENU #########
cdef create_menu = Create(window, player, readData.data['mainMenu'])
create_menu.create_UI()

######## CREATE SETTINGS #########
cdef create_settings = Create(window, player, readData.data['settings'])
create_settings.create_UI()

######## CREATE CREDITS #########
cdef create_credits = Create(window, player, readData.data['credits'])
create_credits.create_UI()

######## CREATE PAUSE #########
cdef create_pause = Create(window, player, readData.data['pauseGame'])
create_pause.create_UI()

######## CREATE SELECT PLAYER #########
cdef create_selectPlayer = Create(window, player, readData.data['SelectPlayer'])
create_selectPlayer.create_UI()

######## CREATE MAPS #########

# create objects for blocks and other objects - Map 1 / base
cdef create_base = Create(window, player, readData.data['Base'])
create_base.create()

# create objects for blocks and other objects - Map 2
cdef create_map2 = Create(window, player, readData.data['Map2'])
create_map2.create()

# create objects for blocks and other objects - Map 3
cdef create_map3 = Create(window, player, readData.data['Map3'])
create_map3.create()

cdef create_map4 = Create(window, player, readData.data['Map4'])
create_map4.create()

######## CREATE ENEMIES #########

# enemies for map 2
cdef enemies_map2 = Create(window, player, readData.data['Enemies_m2'])
enemies_map2.create_enemies()

# camera
cdef camera = Camera(player, windowSize)

# Listed all objects, maps and enemies for camera tracking
cdef allObjects1 = create_base.allobjs()+[base]
cdef allObjects2 = create_map2.allobjs()+[map_2]+enemies_map2.allenemies()
cdef allObjects3 = create_map3.allobjs()+[map_3]
cdef allObjects4 = create_map4.allobjs()+[map_4]

# create.listofObjects is a list of all objecst
# listenemies is a list of all enemies
# listOfMap is a list of map tiles

# draw base map function
cdef void draw_base():
    global currentPage

    window.fill((10, 10, 10))

    # camera
    camera.move(allObjects1)

    # map for the base map
    base.drawMap(window)

    # draw object
    create_base.draw()
    cdef pause = create_base.pauseGame() # if player click esc - pause

    # draw player
    player.draw(window, create_base.allobjs()[1:])
    player.navigate()

    for guis in listGUIs:
        guis.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    pygame.display.flip()

# draw MAP 2 funtion
cdef void draw_map2():
    global currentPage
    window.fill((10, 10, 10))

    # camera for map 2
    camera.move(allObjects2)

    # draw map 2
    map_2.drawMap(window)

    # draw objects
    create_map2.draw()
    cdef pause = create_map2.pauseGame()

    # enemies
    enemies_map2.draw_enemy(create_map2.allobjs()[1:]) # uncomment later

    # draw player
    player.handleFight(enemies_map2.allenemies(), window)
    player.draw(window, create_map2.allobjs()[1:])
    player.navigate()

    for guis in listGUIs:
        guis.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    pygame.display.flip()

# not yet done
cdef void draw_map3(): 
    global currentPage
    window.fill((10, 10, 10))

    map_3.drawMap(window)

    create_map3.draw()
    cdef pause = create_map3.pauseGame()

    # draw player in map3
    player.draw(window, create_map3.allobjs()[1:])
    player.navigate()

    # camera fot map 3
    camera.move(allObjects3)

    for gui in listGUIs:
        gui.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    pygame.display.flip()

cdef void draw_map4():
    global currentPage

    window.fill((10, 10, 10))

    # draw the map
    map_4.drawMap(window)

    create_map4.draw()
    pause = create_map4.pauseGame()

    player.draw(window, create_map4.allobjs()[1:])
    player.navigate()


    camera.move(allObjects4)

    for gui in listGUIs:
        gui.draw(window)

    if pause:
        currentPage = pages[6]

    pygame.display.flip()

# pause the game
cdef void PauseGame():
    global currentPage
    window.fill((10, 10, 10))

    create_pause.draw_ui()
    cdef selected = create_pause.Select()

    cdef keys = pygame.key.get_just_pressed()

    if keys[pygame.K_ESCAPE]: # back to game
        selected_item.play()
        currentPage = pages[5]
    
    if selected == 0:
        currentPage = pages[5] # back to game
    elif selected == 1:
        currentPage = pages[1] # navigate to main menu
        music.switch = True
        music.toPlay = 1

    pygame.display.flip()

# main menu of the game
cdef void mainMenu():
    global currentPage

    window.fill((10, 10, 10))

    create_menu.draw_ui()
    cdef selected = create_menu.Select()

    if selected == 0: # navigate to Select player 
        if player.name != "":
            currentPage = pages[5]
            music.switch = True
            music.toPlay = 0
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
cdef void settings():
    global currentPage

    window.fill((10, 10, 10))

    create_settings.draw_ui()
    cdef selected = create_settings.Select()

    if selected == 2: # if save is selected
        currentPage = pages[1] # back to main menu
        selected = 0

    pygame.display.flip()

# display credits
cdef void credits():
    global currentPage
    window.fill((10, 10, 10))

    create_credits.draw_ui()

    cdef keys = pygame.key.get_just_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
        selected_item.play() # play audio selected
        currentPage = pages[1]

    pygame.display.flip()

# display selecting players / characters
cdef void selectPlayer():
    global currentPage
    window.fill((10, 10, 10))

    create_selectPlayer.draw_ui()
    cdef character = create_selectPlayer.Select()

    cdef keys = pygame.key.get_just_pressed()

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
        music.switch = True
        music.toPlay = 0
        currentPage = pages[5] # navigate to game page
    elif keys[pygame.K_ESCAPE]:
        selected_item.play() # play audio selected
        currentPage = pages[1] # back to main menu

    pygame.display.flip()

# opening scene function / credits and loading
cdef void Opening():
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
                music.switch = True
                music.toPlay = 1
                #del title # remove or delete all loaded images

    pygame.display.flip()

# for testing
cdef fpsCollected = [] # collecting frames per second value

# main function
def main():
    cdef int run = 1

    while run:

        # fps of the game
        clock.tick(fps)

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0

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
            run = 0

        # for testing
        chechFPS(round(clock.get_fps(), 2))
        music.switch_music()

    # quit program after the loop
    print('fps timeline:',fpsCollected)
    print('lowest:', min(fpsCollected), '\nHighest:', max(fpsCollected), '\nLocation:', player.location)
    pygame.quit()

# function for testing

# frame drops test
cdef void chechFPS(frames):
    if frames not in fpsCollected and frames >= 1:
        fpsCollected.append(frames)