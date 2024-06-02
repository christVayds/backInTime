import pygame
import random

# ENEMY BOSS FIGHT

class Boss(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, name):
        self.width = width
        self.height = height
        self.name = name
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.defaulLife = None
        self.life = self.defaulLife
        self.damage = 0
        self.walk = 0
        self.speed = 7

        self.weapon = []

        self.attack = False
        self.follow = False # true to follow the toFocus
        self.toFocus = None # player or other objects
        self.FocusList = []
        self.change = False # changing what to focus or to attack

        self.init_boss()

    def draw(self, screen):
        if (self.walk + 1) >= 9:
            self.walk = 0

        self.Facing()
        screen.blit(self.c_facing[self.walk//3], self.rect)
        self.walk += 1

    def Facing(self):
        if self.direction == 'left':
            self.c_facing = self.c_left
        elif self.direction == 'right':
            self.c_facing = self.c_right
        elif self.direction == 'up':
            self.c_facing = self.c_up
        elif self.direction == 'down':
            self.c_facing = self.c_down

    def Follow(self):
        if self.follow and self.toFocus != None:
            if self.toFocus.rect.x > self.rect.x:
                self.rect.x += self.speed
                self.direction = 'right'
            if self.toFocus.rect.x < self.rect.x:
                self.rect.x -= self.speed
                self.direction = 'left'
            if self.toFocus.rect.y > self.rect.y:
                self.rect.y += self.speed
                self.direction = 'down'
            if self.toFocus.rect.y < self.rect.y:
                self.rect.y -= self.speed
                self.direction = 'up'

    def loadImages(self):
        sides = ['D_', 'U_', 'S_']

        for side in sides:
            for i in range(3):
                image = f'characters/test/{side}{i}.png'
                image = pygame.image.load(image)
                image = pygame.transform.scale(image, (self.width, self.height))
                if side == 'D_':
                    self.c_down.append(image)
                elif side == 'U_':
                    self.c_up.append(image)
                elif side == 'S_':
                    self.c_left.append(image)

        for i in self.c_left:
            image = pygame.transform.flip(i, True, False)
            self.c_right.append(image)

    def init_boss(self):
        
        # Boss images loaded, facing and direction
        self.c_left = []
        self.c_right = []
        self.c_up = []
        self.c_down = []
        self.c_facing = self.c_left
        self.direction = 'left'
        self.loadImages()

    def change_focus(self):
        if self.change:
            self.toFocus = random.choice(self.FocusList)
            self.change = False

    def addLevel(self, player):
        if player.level <= 3: # level 1 to 3 only
            player.level += 1
            self.player.myWeapons += self.weapon # give to the player the weapons

class Ethan(Boss):

    def __init__(self, x, y, width, height, name='ethan'):
        super().__init__(x, y, width, height, name)
        self.defaulLife = 500

class Christian(Boss):

    def __init__(self, x, y, width, height, name='christian'):
        super().__init__(x, y, width, height, name)
        self.defaulLife = 800

class Aeron(Boss):

    def __init__(self, x, y, width, height, name='aeron'):
        super().__init__(x, y, width, height, name)
        self.defaulLife = 1200