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
from src.game import Game
from src.character import *
from src.object import *
from src.create import Create
from src.camera import Camera
from Data.read import Read
from src.UI import UI, GUI, CraftingBook
from src.timer import Timer

# IMPORT MAPS
# from Maps import baseMap, Map_2, Map_3, Map_4
from Maps import baseMap, Map_2, Map_3, Map_4, Battleground_1
from src.music import Music
from src import weapons
from src import inventories

# initialize pygame
pygame.mixer.pre_init()
pygame.init()
pygame.font.init()

# screen
windowSize = {'width': 700, 'height': 500} # size of the display
window = pygame.display.set_mode((windowSize['width'], windowSize['height']))
pygame.display.set_caption('Back In Time')

# clock and FPS - frame per second
clock = pygame.time.Clock()
fps = 30 # 30 frames per second

# Game State
game = Game(window)

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
walkSfx = pygame.mixer.Sound('audio/walk_1.mp3')

# TImer
timer = Timer(fps)

# Program pages
pages = [
    'intro', 'main-menu', 'settings', 'credits', 
    'selectPlayer', 'in-game', 'pause-game', 'weapons', 'vaultbox', 'craftbox', 'collectable', 'monitor', 'craftingBook', 'game-over', 'outro', 
    'error_message', 'exit']

currentPage = pages[0]

# MAP HERE
base = baseMap.TileMap(25, 0, 0)
map_2 = Map_2.TileMap(25, 0, 0)
map_3 = Map_3.TileMap(25, 0, 0)
map_4 = Map_4.TileMap(25, 0, 0)

# battle grounds
battleG1 = Battleground_1.TileMap(25, 0, 0)

#################### GUI #######################

# player Icon and health bar
playerIcon = UI(10, 10, 256, 64, 'player_frame')

listGUIs = [playerIcon] # list contain: healthbar

##### PAUSE MENU #####
pause_menu = GUI(254, 58, (192, 384), window, 'pause_game', sfx=[select_item, selected_item])
pause_menu.game = game

##### MAIN MENU #####
main_menu = GUI(254, 58, (192, 384), window, 'main_menu', sfx=[select_item, selected_item])
main_menu.game = game

##### SETTINGS #####
settings_menu = GUI(254, 58, (192, 384), window, 'settings_menu', sfx=[select_item, selected_item])
settings_menu.game = game

##### CREDITS #####
credits_menu = GUI(254, 58, (192, 384), window, 'credits', sfx=[select_item, selected_item])
credits_menu.game = game

##### MONITOR #####
monitor_ui = GUI((windowSize['width'] - 320) / 2, (windowSize['height'] - 320) / 2, (320, 320), window, 'monitor', None, [select_item, selected_item])
monitor_ui.game = game

############# PLAYER #####################

player = Player(((windowSize['width'] - 50) / 2), ((windowSize['height'] - 50) / 2), 50, 50)
game.player = player # add the player to the game class
player.walkSfx = walkSfx # walk sound effects
player.sfx = [select_item, selected_item] # other sound effects

# read object data from json file data
readData = Read('Data/data.json')
readData.read() # read all data

# get the data to game
game.readData = readData

# CREATIONS

# for intro screen
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

######## CREATE MAPS (BATTLE GROUNDS) #########

createBattleG1 = Create(window, player, readData.data['BattleGround1'], select_item, selected_item)
createBattleG1.create()

######## CREATE ENEMIES #########

# enemies for map 2
enemy_bg1 = Create(window, player, readData.data['Enemies_m2'], select_item, selected_item)
enemy_bg1.create_enemies()

# camera
camera = Camera(player, windowSize)

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

# collectables
collectable_table = inventories.Collectables(player, window, (640, 160), (30, 170))
collectable_table.sfx = inventory.sfx

# crafting Book
crafting_Book = CraftingBook((windowSize['width'] - 448) / 2, (windowSize['height'] - 224) / 2, 448, 224, window)
crafting_Book.sfx = inventory.sfx

# draw base map function
def draw_base():
    global currentPage

    window.fill((10, 10, 10))
    game.Reset(False, base, create_base)

    # map for the base map
    base.drawMap(window)

    # draw object
    create_base.draw()
    pause = create_base.pauseGame() # if player click esc - pause
    openWeapons = create_base.openWeapons() # handling event for opening a weapon
    player.Message(window)

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

    elif player.collectables:
        currentPage = pages[10] # open collectable table
    
    elif player.openMonitor:
        currentPage = pages[11]

    showfps()

    # camera
    camera.move(create_base.listofObjects+[base]+[player.equiped1, player.equiped2])

    player.loading_nav(window) # for transition in navigation

    pygame.display.flip()

# draw MAP 2 funtion
def draw_map2():
    global currentPage

    window.fill((10, 10, 10))
    game.Reset(False, map_2, create_map2)

    # camera for map 2
    camera.move(create_map2.listofObjects+[map_2]+[player.equiped1, player.equiped2])

    # draw map 2
    map_2.drawMap(window)

    # draw objects
    create_map2.draw()
    pause = create_map2.pauseGame()
    openWeapons = create_base.openWeapons()

    # drop or display weapons
    player.potion.Use()
    player.handleFight([])
    player.Message(window)

    # draw player
    player.draw(window, create_map2.listofObjects[1:])
    effects_1.effects() # effets for equiped weapon 1
    effects_2.effects() # effets for equiped weapon 2
    effects_2.Hit([player])
    effects_1.Hit([player])
    player.navigate()
    player.handleDefense()
    player.TriggerSkills([])

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

    elif player.openbook:
        currentPage = pages[12] # read the book

    showfps()

    player.loading_nav(window) # for transition in navigation

    pygame.display.flip()

# not yet done
def draw_map3():
    global currentPage

    window.fill((10, 10, 10))
    game.Reset(False, map_3, create_map3)

    # camera fot map 3
    camera.move(create_map3.listofObjects+[map_3]+[player.equiped1, player.equiped2])

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
    effects_2.Hit([player])
    effects_1.Hit([player])
    player.handleDefense()
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
    
    elif player.collectables:
        currentPage = pages[10] # open collectable table

    showfps()

    player.loading_nav(window) # for transition in navigation

    pygame.display.flip()

def draw_map4():
    global currentPage

    window.fill((10, 10, 10))
    game.Reset(False, map_4, create_map4)

    camera.move(create_map4.listofObjects+[map_4]+[player.equiped1, player.equiped2])

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
    effects_2.Hit([player]+[create_map4.practice])
    effects_1.Hit([player]+[create_map4.practice])
    player.navigate()
    player.TriggerSkills([create_map4.practice])
    player.handleDefense()
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

    player.loading_nav(window) # for transition in navigation

    pygame.display.flip()

def draw_btg1():
    global currentPage

    window.fill((10, 10, 10))
    game.Reset(True, battleG1, createBattleG1) # reset the map width enemies
    game.ResetMap(battleG1, createBattleG1)

    camera.move(createBattleG1.listofObjects+[battleG1]+game.Enemies+[player.equiped1, player.equiped2]+game.items)

    # draw the map
    battleG1.drawMap(window)
    player.handleFight(game.Enemies)

    createBattleG1.draw() # objects
    pause = createBattleG1.pauseGame()
    openWeapons = create_base.openWeapons()
    
    # draw the items from enemies in game class
    game.drawItems()

    # draw enemies
    for enemy in game.Enemies:
        if enemy.life <= 0: # enemy die
            enemy.hit_effects(window)
            if enemy.out:
                for item in enemy.items:
                    item.x = enemy.rect.x
                    item.y = enemy.rect.y
                    game.items.append(item) # append the items and the x and y pos of the enemy
                game.Enemies.remove(enemy)
        enemy.draw(window, createBattleG1.listofObjects[1:])
        enemy.follow(player)
        enemy.Attack(player)

    player.potion.Use()
    player.draw(window, createBattleG1.listofObjects[1:]) # draw player
    player.pickItems(game.items)

    effects_1.effects() # effets for equiped weapon 1
    effects_2.effects() # effets for equiped weapon 2
    effects_2.Hit([player]+game.Enemies)
    effects_1.Hit([player]+game.Enemies)

    player.navigate() # for naviagtion
    player.TriggerSkills(game.Enemies) # skills
    player.handleDefense() # shield
    player.Message(window) # notification or message

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    if pause:
        currentPage = pages[6] # game menu / pause

    elif openWeapons or player.viewVaultBox:
        currentPage = pages[7] # weapons inventory
    
    # check if game over
    if game.gameover:
        currentPage = pages[13] # game over window / page

    showfps()
    player.loading_nav(window) # for transition in navigation

    pygame.display.flip()

count = 120
def draw_gameOver():
    global currentPage, count
    window.fill((0,0,0))
    count -= 1

    if count <= 0:
        currentPage = pages[1]

    pygame.display.flip()
# for weapons
def draw_weapons():
    global currentPage

    player.potion.Use()
    player.handleDefense()
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
    player.handleDefense()
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
    player.handleDefense()
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

def draw_collectables():
    global currentPage

    player.potion.Use()
    player.handleDefense()
    collectable_table.draw()
    player.Message(window)

    if collectable_table.Close():
        currentPage = pages[5] # return to game
        player.collectables = False

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    showfps()

    pygame.display.flip()

def draw_Monitor():
    global currentPage

    player.potion.Use()
    player.handleDefense()
    player.Message(window)
    monitor_ui.draw()
    game.showMonitor_message((monitor_ui.x, monitor_ui.y), window)

    select = monitor_ui.Select()
    if select == 0:
        currentPage = pages[5] # return to game
        player.openMonitor = False

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    showfps()
    pygame.display.flip()

# crafting book draw
def draw_craftingBook():
    global currentPage

    player.potion.Use()
    player.handleDefense()
    player.Message(window)
    crafting_Book.draw()

    if crafting_Book.Actions():
        player.openbook = False
        crafting_Book.page = 0
        currentPage = pages[5] # return to game

    player.barLife(window)
    for guis in listGUIs:
        guis.draw(window)

    showfps()

    pygame.display.flip()

# pause the game
def PauseGame():
    global currentPage

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
    if not game.play: # if the game program just started
        if selected == 0:
            currentPage = pages[4]
            create_selectPlayer.create_UI() # go to select player
        elif selected == 1:
            currentPage = pages[2] # settings
        elif selected == 2:
            currentPage = pages[3] # credits
        elif selected == 3:
            currentPage = pages[-1] # exit
    else: # if the game program already started
        if selected == 0:
            currentPage = pages[5]
            music.switch = True
            music.toPlay = 0
        elif selected == 1:
            currentPage = pages[4]
            create_selectPlayer.create_UI() # fix this
        elif selected == 2:
            currentPage = pages[2]
        elif selected == 3:
            currentPage = pages[3]
        elif selected == 4:
            currentPage = pages[-1]

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
        player.Reset()
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
            weapons.Shield(player, window, (80, 80), 'armored'),
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

        # game start
        game.play = True
        game.location = player.location # get the location

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
            elif player.location == 'BattleGround1':
                draw_btg1()

        elif currentPage == pages[6]:
            PauseGame()
        elif currentPage == pages[7]:
            draw_weapons()
        elif currentPage == pages[8]:
            draw_vaultbox()
        elif currentPage == pages[9]:
            draw_craftbox()
        elif currentPage == pages[10]:
            draw_collectables()
        elif currentPage == pages[11]: # open the monitor
            draw_Monitor()
        elif currentPage == pages[12]: # craftingtable
            draw_craftingBook()
        elif currentPage == pages[13]:
            draw_gameOver()
        elif currentPage == pages[-1]: # exit game
            run = False

        # for testing
        music.switch_music()
    pygame.quit()

# main program
if __name__=='__main__':
    main()