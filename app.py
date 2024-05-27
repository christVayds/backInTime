"""
Game name: Back in Time
Project: Application Development and Emerging Technology
Professor: Gary Bato-ey

developers:
    1. Christian Vaydal
    2. Aeron Segobia
    3. Ethan Diego Lim

Date started: April 16, 2024
Date submited: 
"""

import pygame
from src.character import *
from src.object import *
from src.create import Create
from src.camera import Camera
from Data.read import Read
from src.UI import UI, GUI
from src.timer import Timer

# IMPORT MAPS
from Maps import baseMap, Map_2, Map_3, Map_4
from src.music import Music
from src import weapons
from src import navigation
from src import inventories

# initialize pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# screen
windowSize = {'width': 700, 'height': 500} # size of the display
window = pygame.display.set_mode((windowSize['width'], windowSize['height']))
pygame.display.set_caption('Back In Time')

# clock and FPS - frame per second
clock = pygame.time.Clock()
fps = 30 # 30 frames per second

showFPS = pygame.font.SysFont('arial', 20)

#function for fps / for testing the fps
def showfps():
    getfps = round(clock.get_fps(), 2)
    ftext = showFPS.render(f'FPS: {getfps}', True, (255,255,255))
    if getfps < float(29.50):
        pygame.draw.rect(window, (255,0,0), (600, 10, 100, 30))
    else:
        pygame.draw.rect(window, (0,0,0), (600, 10, 100, 30))
    window.blit(ftext, (600, 15))

####################### audios / sfx / bg musics ####################### AERON
music = Music() # load music inside MUSIC CLASS

####################### SOUND EFFECTS (SFX) HERE ####################### AERON

select_item = pygame.mixer.Sound('audio/select.wav') # for selecting items, etc.
selected_item = pygame.mixer.Sound('audio/selected.wav') # selected items, etc.

# TImer
timer = Timer(fps)

# Program pages
pages = [
    'intro', 'main-menu', 'settings', 'credits', 
    'selectPlayer', 'in-game', 'pause-game', 'weapons', 'vaultbox', 'craftbox', 'outro', 
    'error_message', 'exit']

currentPage = pages[0]

# MAP HERE
base = baseMap.TileMap(25, 0, 0)
map_2 = Map_2.TileMap(25, 0, 0)
map_3 = Map_3.TileMap(25, 0, 0)
map_4 = Map_4.TileMap(25, 0, 0)

#################### GUI #######################

# player Icon and health bar
playerIcon = UI(10, 10, 256, 64, 'player_frame')

listGUIs = [playerIcon] # list contain: healthbar

##### PAUSE MENU #####
pause_menu = GUI(254, 58, (192, 384), window, 'pause_game', sfx=[select_item, selected_item])

##### MAIN MENU #####
main_menu = GUI(254, 58, (192, 384), window, 'main_menu', sfx=[select_item, selected_item])

##### SETTINGS #####
settings_menu = GUI(254, 58, (192, 384), window, 'settings_menu', sfx=[select_item, selected_item])

##### CREDITS #####
credits_menu = GUI(254, 58, (192, 384), window, 'credits', sfx=[select_item, selected_item])

############# PLAYER #####################

player = Player(((windowSize['width'] - 50) / 2), ((windowSize['height'] - 50) / 2), 50, 50)

# read object data from json file data
readData = Read('Data/data.json')
readData.read() # read all data

readData.strToTuple('Base')# make all string tuple in Map1 to tuple
readData.strToTuple('Map2')
readData.strToTuple('Map3')
readData.strToTuple('Map4')
readData.strToTuple('Enemies_m2')# read the tuple(positions) of the enemies
# Other page
readData.strToTuple('SelectPlayer')

# CREATIONS

# for loading screen / intro
title = [
    Object(0, 0, 700, 700, 'bg_image', 'test_bg'),
    Object((windowSize['width'] - 200) / 2, (windowSize['height'] - 350) / 2, 200, 200, 'animated', 'title_3'),
    Object(508, 0, 192, 48, 'other', 'credits'),
    Object(254, 350, 192, 24, 'animated', 'enter_game')
]

######## CREATE SELECT PLAYER #########
create_selectPlayer = Create(window, player, readData.data['SelectPlayer'], select_item, selected_item)

######## CREATE MAPS #########

# create objects for blocks and other objects - Map 1 / base
create_base = Create(window, player, readData.data['Base'], select_item, selected_item)
create_base.create()

# create objects for blocks and other objects - Map 2
create_map2 = Create(window, player, readData.data['Map2'], select_item, selected_item)
create_map2.create()

# create objects for blocks and other objects - Map 3
create_map3 = Create(window, player, readData.data['Map3'], select_item, selected_item)
create_map3.create()

# create objects for blocks and other objects - Map 4
create_map4 = Create(window, player, readData.data['Map4'], select_item, selected_item)
create_map4.create()

######## CREATE ENEMIES #########

# enemies for map 2
enemies_map2 = Create(window, player, readData.data['Enemies_m2'], select_item, selected_item)
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

# For navigation to maps
nav = navigation.Navigation(player) # not yet done

# initialized effects fo equiped weapons
effects_1 = weapons.Effects(window)
effects_2 = weapons.Effects(window)

# Inventories Items and Weapons GUI
inventory = inventories.Weapon(player, window, (350, 350), (175, 75))
inventory.sfx = [select_item, selected_item] # add sfx in inventory

# vault box
vaultbox = inventories.Items(player, window, (640, 320), ((windowSize['width'] - 640) / 2, (windowSize['height'] - 320) / 2))
vaultbox.sfx = inventory.sfx

# Crafting Table
crafting_table = inventories.CraftingTable(player, window, (512, 256), (94, 122))
crafting_table.sfx = inventory.sfx

# draw base map function
def draw_base():
    global currentPage

    window.fill((10, 10, 10))

    # map for the base map
    base.drawMap(window)

    # draw object
    create_base.draw()
    pause = create_base.pauseGame() # if player click esc - pause
    openWeapons = create_base.openWeapons()

    # draw player
    player.potion.Use() # use the potion
    player.handleFight()
    player.draw(window, create_base.listofObjects[1:])
    effects_1.effects() # effets for equiped weapon 1
    effects_2.effects() # effets for equiped weapon 2
    effects_2.Hit([player])
    effects_1.Hit([player])
    player.navigate()
    player.handleDefense()
    player.TriggerSkills()
    player.Message(window)

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    elif openWeapons or player.viewVaultBox:
        currentPage = pages[7] # weapons inventory

    elif player.viewInventory:
        currentPage = pages[8] # items inventory

    elif player.craft:
        currentPage = pages[9] # open craftbox

    showfps()

    # camera
    camera.move(allObjects1+[player.equiped1, player.equiped2])

    pygame.display.flip()

# draw MAP 2 funtion
def draw_map2():
    global currentPage

    window.fill((10, 10, 10))

    # camera for map 2
    camera.move(allObjects2+[player.equiped1, player.equiped2])

    # draw map 2
    map_2.drawMap(window)

    # draw objects
    create_map2.draw()
    pause = create_map2.pauseGame()
    openWeapons = create_base.openWeapons()

    # drop or display weapons
    player.potion.Use()
    player.handleFight(enemies_map2.listEnemies)
    player.Message(window)

    # enemies
    enemies_map2.draw_enemy(create_map2.listofObjects[1:]) # uncomment later

    # draw player
    player.draw(window, create_map2.listofObjects[1:])
    effects_1.effects() # effets for equiped weapon 1
    effects_2.effects() # effets for equiped weapon 2
    effects_2.Hit([player]+enemies_map2.listEnemies)
    effects_1.Hit([player]+enemies_map2.listEnemies)
    player.navigate()
    player.TriggerSkills(enemies_map2.listEnemies)

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    elif openWeapons or player.viewVaultBox:
        currentPage = pages[7] # weapons inventory

    elif player.viewInventory:
        currentPage = pages[8] # items inventory

    elif player.craft:
        currentPage = pages[9] # open craftbox

    showfps()

    pygame.display.flip()

# not yet done
def draw_map3():
    global currentPage

    window.fill((10, 10, 10))

    # camera fot map 3
    camera.move(allObjects3+[player.equiped1, player.equiped2])

    map_3.drawMap(window)

    create_map3.draw()
    pause = create_map3.pauseGame()
    openWeapons = create_base.openWeapons()

    # draw player in map3
    player.potion.Use()
    player.handleFight([])
    player.draw(window, create_map3.listofObjects[1:])
    effects_1.effects() # effets for equiped weapon 1
    effects_2.effects() # effets for equiped weapon 2
    player.navigate()
    player.Message(window)

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    # temporary
    if pause:
        currentPage = pages[6] # game menu / pause

    elif openWeapons or player.viewVaultBox:
        currentPage = pages[7] # weapons inventory

    elif player.viewInventory:
        currentPage = pages[8] # items inventory

    elif player.craft:
        currentPage = pages[9] # open craftbox

    showfps()

    pygame.display.flip()

def draw_map4():
    global currentPage

    window.fill((10, 10, 10))

    camera.move(allObjects4+[player.equiped1, player.equiped2])

    # draw the map
    map_4.drawMap(window)

    create_map4.draw()
    pause = create_map4.pauseGame()
    openWeapons = create_base.openWeapons()

    player.potion.Use()
    player.handleFight([create_map4.practice])
    player.draw(window, create_map4.listofObjects[1:])
    effects_1.effects() # effets for equiped weapon 1
    effects_2.effects() # effets for equiped weapon 2
    player.navigate()
    player.TriggerSkills([create_map4.practice])
    player.Message(window)

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    if pause:
        currentPage = pages[6] # game menu / pause

    elif openWeapons or player.viewVaultBox:
        currentPage = pages[7] # weapons inventory

    elif player.viewInventory:
        currentPage = pages[8] # items inventory

    elif player.craft:
        currentPage = pages[9] # open craftbox

    showfps()

    pygame.display.flip()

# for weapons
def draw_weapons():
    global currentPage

    player.potion.Use()
    inventory.draw()
    inventory.drawWeapons()
    player.Message(window)

    if inventory.Select():
        currentPage = pages[5]
        player.viewVaultBox = False

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    showfps()

    pygame.display.flip()

def draw_vaultbox():
    global currentPage

    player.potion.Use()
    vaultbox.draw()
    vaultbox.drawInventories()
    player.Message(window)

    if vaultbox.Select():
        currentPage = pages[5]
        player.viewInventory = False
    
    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    showfps()

    pygame.display.flip()

def draw_craftbox():
    global currentPage

    player.potion.Use()
    crafting_table.draw()
    crafting_table.drawItems()
    player.Message(window)

    if crafting_table.Select():
        currentPage = pages[5]
        player.craft = False

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    showfps()

    pygame.display.flip()

# pause the game
def PauseGame():
    global currentPage
    # window.fill((10, 10, 10))

    pause_menu.draw()
    selected = pause_menu.Select()
    if selected == 0:
        currentPage = pages[5] # back to game
    elif selected == 1:
        pause_menu.selected = 0
        currentPage = pages[1] # to main menu

    pygame.display.flip()

# main menu of the game
def mainMenu():
    global currentPage

    window.fill((10, 10, 10))

    main_menu.draw()
    selected = main_menu.Select()
    if selected == 0:
        if player.name != "":
            currentPage = pages[5]
            music.switch = True
            music.toPlay = 0
        else:
            currentPage = pages[4]
            create_selectPlayer.create_UI()
    elif selected == 1:
        currentPage = pages[2] # settings
    elif selected == 2:
        currentPage = pages[3] # credits
    elif selected == 3:
        currentPage = pages[-1] # exit

    pygame.display.flip()

# settings
def settings():
    global currentPage

    window.fill((10, 10, 10))

    settings_menu.draw()
    selected = settings_menu.Select()
    if selected == 2:
        currentPage = pages[1]

    pygame.display.flip()

# display credits
def credits():
    global currentPage
    window.fill((10, 10, 10))

    credits_menu.draw()
    selected = credits_menu.Select()
    if selected == 0:
        currentPage = pages[1]

    pygame.display.flip()

# display selecting players / characters
def selectPlayer():
    global currentPage
    window.fill((20, 6, 79))

    create_selectPlayer.draw_ui()
    character = create_selectPlayer.Select()

    keys = pygame.key.get_just_pressed()

    if keys[pygame.K_SPACE]:
        player.location = 'base'
        if character == 0:
            player.name = 'johny'
        elif character == 1:
            player.name = 'ricky'
        elif character == 2:
            player.name = 'jp'
        elif character == 3:
            player.name = 'jayson'
        else:
            raise Exception('Player not found')
        
        # player's other initializations here
        player.loadImages() # load the image of the player
        player.initSkill(window) # initialized skills
        player.myWeapons = [
            weapons.SnowBall(player, window, (20, 20)),
            weapons.Trident(player, window, (50, 50)),
            weapons.Mjolnir(player, window, (30, 30)),
            weapons.Shuriken(player, window, (30, 30)),
            weapons.Potions(player, window, (25, 25), 'weaponize'),
            weapons.Potions(player, window, (25, 25), 'speed'),

        ]

        player.inventories = [
            weapons.Potions(player, window, (25, 25), 'durability'),
            weapons.Shield(player, window, (80, 80), 'protektor'),
            ] # load at least one item or weapon in inventory

        # give player equipment
        player.equiped1 = weapons.Boomerang(player, window, (30, 30)) # equiped the weapon 1
        player.equiped2 = weapons.Bomb(player, window, (30, 30)) # equiped the weapon 2
        player.shield = weapons.Shield(player, window, (80, 80)) # equiped the shield
        player.potion = weapons.Potions(player, window, (25, 25), 'power')
        player.potion.Apply(player.equiped1)
        player.potion.Apply(player.equiped2)
        player.potion.Apply(player.shield)

        music.switch = True # switching music
        music.toPlay = 0 # switch bg music

        effects_1.loadEffects(player.equiped1) # load effects - no effects yet to equiped 1(boomerang)
        effects_2.loadEffects(player.equiped2) # load effects

        currentPage = pages[5] # navigate to game page
        create_selectPlayer.destory_UI() # destroy this page
    
    elif keys[pygame.K_ESCAPE]:
        selected_item.play() # play audio selected
        currentPage = pages[1] # back to main menu
        create_selectPlayer.destory_UI()

    pygame.display.flip()

# opening scene function / credits and loading
def Opening():
    global currentPage, title

    window.fill((10, 10, 10))

    # draw animated title 
    for ttle in title:
        ttle.draw(window)

    keys = pygame.key.get_just_pressed()
    if keys[pygame.K_SPACE]:
        player.location = 'base'
        music.switch = True
        music.toPlay = 1
        del title
        currentPage = pages[1]

    pygame.display.flip()

# main function
def main():
    run = True

    while run:

        # fps of the game
        clock.tick(fps)

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # exit the game

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
            # draw the map display
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
        elif currentPage == pages[7]:
            draw_weapons()
        elif currentPage == pages[8]:
            draw_vaultbox()
        elif currentPage == pages[9]:
            draw_craftbox()
        elif currentPage == pages[-1]: # exit game
            run = False

        # for testing
        music.switch_music()
    pygame.quit()

# main program
if __name__=='__main__':
    main()