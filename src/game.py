import pygame
import random
from .character import Enemy
from .weapons import Items
import json

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.play = False # if the player already played
        self.location = None
        self.player = None
        self.colors = {
            "White": (255,255,255),
            "red": (232, 51, 35),
            "green": (35, 235, 88)
        }

        self.message_from_past = None
        self.font_one = pygame.font.SysFont('Arial', 13)

        self.battleG1 = 0
        self.battleG2 = 0
        self.battleG3 = 0

        self.Enemies = []
        self.items = [] # from enemies

        self.tries = 3 # only 3 tries, if 0 then game over
        self.gameover = False

        # items data
        self.itemData = list()
        self.loadItemsData()

        self.num_enemies_nLvl = [6, 8, 10]

    def Reset(self, createEnemy, map, creation_obj): 
        if self.player.life <= 0:
            if self.tries > 1:
                self.tries -= 1
                self.player.life = self.player.defaultLife
                self.player.mana = self.player.defaultMana
                self.player.loading = True
                self.player.nav = True
                self.player.loading_timer = self.player.loading_timer_max
                self.player.loading_nav(self.screen)

                if createEnemy:
                    self.Enemies = []
                    self.createEnemies()
                if creation_obj != None:
                    creation_obj.Reset()
                
                # reset the map
                map.x = 0
                map.y = 0
            else:
                self.gameover = True

    def ResetMap(self, map, creation_obj):
        if self.player.nextMap and len(self.Enemies) < 1: # check this shit
            map.x = 0
            map.y = 0

            if creation_obj != None:
                creation_obj.Reset()

            # create enemies
            self.items = [] # clear items
            self.createEnemies() 
            
            self.player.rect.x = self.player.MapObjects[f'{self.player.respawn}_{self.player.location}'].rect.x
            self.player.rect.y = self.player.MapObjects[f'{self.player.respawn}_{self.player.location}'].rect.y
            
        self.player.nextMap = False

    def showMonitor_message(self, monitor, screen):
        self.message_from_past = f'Dear {self.player.name.title()},\nThe world as we knew has fallen. Zombies\nhave conquired everything, and you are\nthe last surviving human.\nBut there is still hope. You must time travel to the\npast to stop the zombie virus from spreading.\n\n1. The missing pieces of the time machine \nare scattered around this lab. You need to find them.\n2. There\'s a book somewhere in the lab that contains\ninstructions on how to craft other essential parts \nof the machine.\n3. Be cautious, as zombies and robots roam the area.\nYou\'ll need to find weapons to defend yourself.\n\nGood luck, the world is in your hands,\nback in time to save the world.'
        text = self.font_one.render(self.message_from_past, True, self.colors['green'])
        screen.blit(text, (monitor[0]+20, monitor[1]+20))

    def createEnemies(self):
        # create 6 enemies
        num_enemies = random.choice(range(self.num_enemies_nLvl[self.player.level]))
        for _ in range(num_enemies):
            posx = random.choice(list(range(100, 650)))
            posy = random.choice(list(range(100, 400)))
            enemy = Enemy(posx, posy, 50, 50, 'zombie')
            enemy.speed = random.choice([2,3,4])
            enemy.defaultLife = random.choice([20, 50, 10, 20, 20, 20, 20])
            enemy.life = enemy.defaultLife
            enemy.items = self.generateItems() # give item
            self.Enemies.append(enemy)

    def generateItems(self):
        count = random.choice([0,0,0,0,0,0,1])
        items = []

        for _ in range(count):
            item = random.choice(self.itemData)
            item = Items(self.player, self.screen, (40,40), item)
            if item.checkItem():
                if self.findItems(item) and item not in items: # if item not in self.items and in item lists
                    items.append(item)

        return items # list of items

    def drawItems(self):
        for item in self.items:
            itemImage = pygame.transform.scale(item.icon, (20, 20))
            self.screen.blit(itemImage, (item.x, item.y))

    def loadItemsData(self):
        with open('Data/items.json') as file:
            Data = json.load(file)

            craftItems = Data['craftItems']
            item = list(Data['Items'])
            for i in item:
                if i not in craftItems:
                    self.itemData.append(i)

    def findItems(self, item):
        for i in self.items:
            if i.code == item.code:
                print('found')
                return False # return true if the item is already exist in self.items
            
        for weapon in self.player.myWeapons:
            if weapon.code == item.code:
                return False
            
        return True