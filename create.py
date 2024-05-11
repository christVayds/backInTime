from object import Object
from character import Enemy
from UI import UI
import pygame
class Create:

    def __init__(self, screen, player, list_obj):
        self.screen = screen
        self.player = player
        self.list_obj = list_obj #list of objects for map

        # retun this list
        self.listofObjects = [player]
        self.listEnemies = []

        self.selected = 0
        self.selectors = []
        self.listUIs = []

    def create(self):
        for obj in self.list_obj:
            object = Object(obj['rect'][0], obj['rect'][1], obj['rect'][2], obj['rect'][3], obj['type'], obj['name'])
            if obj['name'] in ['box_1']:
                object.loadChestBox(obj['items'])
            if obj['type'] == 'navigation':
                self.player.MapObjects[obj['distination']] = object
            self.listofObjects.append(object)
                    
    def draw(self):
        for obj in self.listofObjects:
            if obj != self.listofObjects[0]:
                obj.draw(self.screen)

    #  for UI
    def create_UI(self):
        for obj in self.list_obj:
            ui = UI(obj['rect'][0], obj['rect'][1], obj['rect'][2], obj['rect'][3], obj['name'], obj['type'])
            if ui._type == 'selector':
                ui.selected = obj['selected']
                self.selectors.append(ui)
            self.listUIs.append(ui)

    def draw_ui(self):
        for uis in self.listUIs:
            uis.draw(self.screen)
        # self.Select()

    def Select(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_TAB] or keys[pygame.K_DOWN]:
            self.selected += 1
            if self.selected > 3:
                self.selected = 0

            for ui in self.selectors:
                ui.selected = 1
            self.selectors[self.selected].selected = 0

        elif keys[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = 3

            for ui in self.selectors:
                ui.selected = 1
            self.selectors[self.selected].selected = 0
        
        elif keys[pygame.K_SPACE]:
            return self.selected

    # for enemies
    def create_enemies(self):
        for enemy in self.list_obj:
            enmy = Enemy(enemy['rect'][0], enemy['rect'][1], enemy['rect'][2], enemy['rect'][3], enemy['name'])
            self.listEnemies.append(enmy)

    def draw_enemy(self, objects):
        for enemy in self.listEnemies:
            if enemy.life <= 0:
                self.listEnemies.remove(enemy)
            enemy.draw(self.screen, objects)
            enemy.follow(self.player) # follow the player