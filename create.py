from object import Object
from character import Enemy

class Create:

    def __init__(self, screen, player, list_obj):
        self.screen = screen
        self.player = player
        self.list_obj = list_obj #list of objects for map

        # retun this list
        self.listofObjects = [player]
        self.listEnemies = []

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

    # for enemies
    def create_enemies(self):
        for enemy in self.list_obj:
            enmy = Enemy(enemy['rect'][0], enemy['rect'][1], enemy['rect'][2], enemy['rect'][3], enemy['name'])
            self.listEnemies.append(enmy)

    def draw_enemy(self, objects):
        for enemy in self.listEnemies:
            enemy.draw(self.screen, objects)
            enemy.follow(self.player) # follow the player