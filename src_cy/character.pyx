import pygame
import random

import pygame.locals

class Player(pygame.sprite.Sprite):

    def __init__(self, int x, int y, int width, int height, str name=''):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name

        # Fonts
        self.font = pygame.font.SysFont('consolas', 15)

        # player life
        self.defaultLife = 100
        self.life = 50
        self.power = 10
        self.weapons = ['sword']
        self.equiped = self.weapons[0]
        self.attack = False
        self.attacking = 3

        # speed
        self.speed = 10
        self.walk = 0

        # rect and surface
        self.rect = pygame.Rect((x, y), (self.width, self.height)) # for player rect
        self.image = pygame.Surface((self.width, self.height)) # surface

        # facing
        self.left = False
        self.right = True
        self.up = False
        self.down = False

        # image and animation
        self.c_left = []
        self.c_right = []
        self.c_up = []
        self.c_down = []
        self.sword = [
            pygame.transform.scale(pygame.image.load(f'characters/objects/sway_top.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load(f'characters/objects/right_sway.png'), (80, 80)),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'characters/objects/sway_top.png'), (80, 80)), False, True),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'characters/objects/right_sway.png'), (80, 80)), True, False)
        ]

        # inventories / items list
        self.inventories = []

        # handling location
        self.location = 'base'

        # map objects
        self.nav = False
        self.MapObjects = {}
        self.respawn = 'base'

    def draw(self, object screen, list allObj):

        # handle collision
        self.handleCollision(allObj)
        self.displayName = self.font.render(self.name.title(), True, (0,0,0)) # temporary 
        screen.blit(self.displayName, (self.rect.x, self.rect.y - (self.width / 2), self.displayName.get_width(), self.displayName.get_height()))

        # get key events
        cdef keys = pygame.key.get_pressed()

        # left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.left = True
            self.right = False
            self.up = False
            self.down = False

            self.move_x((self.speed * -1))

        # right
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # print('player.rect.x',self.rect.x)
            self.left = False
            self.right = True
            self.up = False
            self.down = False

            self.move_x(self.speed)

        # up
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.left = False
            self.right = False
            self.up = True
            self.down = False

            self.move_y((self.speed * -1))

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.left = False
            self.right = False
            self.up = False
            self.down = True

            self.move_y(self.speed)
        else: 
            self.walk = 0

        self.Facing(screen)
        
        # player rect
        # pygame.draw.rect(screen, (255,255,10), self.rect, 1)
        self.barLife(screen)

    def barLife(self, screen):
        # player's life bar
        pygame.draw.rect(screen, (207, 208, 255), (self.rect.x, self.rect.y - (self.height / 2) + 15, self.width, 5))
        pygame.draw.rect(screen, (225, 252, 68), (self.rect.x, self.rect.y - (self.height / 2) + 15, (self.life / self.defaultLife) * self.width, 5))

    
    def Facing(self, screen):
        # self.walk is the number of walk of character
        if (self.walk + 1) >= 21:
            self.walk = 0
            
        if self.left:
            screen.blit(self.c_left[self.walk//3], (self.rect.x, self.rect.y))
            self.walk += 1
        elif self.right:
            screen.blit(self.c_right[self.walk//3], (self.rect.x, self.rect.y))
            self.walk += 1
        elif self.up:
            screen.blit(self.c_up[self.walk//3], (self.rect.x, self.rect.y))
            self.walk += 1
        elif self.down:
            screen.blit(self.c_down[self.walk//3], (self.rect.x, self.rect.y))
            self.walk += 1
        else:
            if self.left:
                screen.blit(self.c_left[0], (self.rect.x, self.rect.y))
            elif self.right:
                screen.blit(self.c_right[0], (self.rect.x, self.rect.y))

    # load all image in list of images [right, left, and down]
    def loadImages(self):
        cdef list images = ['D_Walk_', 'S_Walk_', 'U_Walk_']

        for image in images:
            for count in range(7):
                img = f'characters/{self.name}/{image}{count}.png'
                img = pygame.image.load(img)
                img = pygame.transform.scale(img, (self.width, self.height))
                if image == 'D_Walk_':
                    self.c_down.append(img)
                elif image == 'U_Walk_':
                    self.c_up.append(img)
                elif image == 'S_Walk_':
                    self.c_left.append(img)

    # flip all characters to right
    def flipImage(self):
        for character in self.c_left:
            self.c_right.append(pygame.transform.flip(character, True, False))
    
    # [direction] positive number going to right, negative going to left
    def move_x(self, int direction):
        self.rect.x += direction

    # [direction] positive number going down, negative going up
    def move_y(self, int direction):
        self.rect.y += direction

    def handleCollision(self, list objects):
        for obj in objects:

            # handle facing of the player
            if self.left or self.right:
                if self.rect.y > obj.rect.y:
                    obj.front = True
                elif self.rect.y <= obj.rect.y:
                    obj.front = False

            # if the player collide with the objects
            if pygame.sprite.collide_rect(self, obj):
                if obj._type in ['hidden2', 'other2']: # no y-sorting objects
                    if self.left:
                        self.rect.left = obj.rect.right
                    elif self.right:
                        self.rect.right = obj.rect.left
                    elif self.up:
                        self.rect.top = obj.rect.bottom
                    elif self.down:
                        self.rect.bottom = obj.rect.top
                elif obj._type in ['other', 'hidden', 'animated', 'animated_once']: # with y-sorting objects
                    # check if item is chestbox
                    if obj.name in ['box_1']:
                        self.pick(obj) # pick the item with space bar

                    # handle facing and collision for object - with y-sorting
                    if self.left:
                        if self.rect.y <= obj.rect.y:
                            self.rect.left = obj.rect.right
                    elif self.right:
                        if self.rect.y <= obj.rect.y:
                            self.rect.right = obj.rect.left

                    elif self.up and obj.front:
                        if self.rect.top <= obj.rect.bottom - 40:
                            self.rect.top = obj.rect.bottom - 40
                    elif self.down and not(obj.front):
                        self.rect.bottom = obj.rect.top

                # example door or the time machine
                elif obj._type == 'navigation':
                    self.checkLocation(obj)
    
    # handling navigating to other location
    def checkLocation(self, obj):
        # locations: Base, Map2[zombies are enemies], Map1[Boss fight ethan], Map3[Boss fight Christian], Map4[Boss fight Aeron with Zombies (void)]
        
        # press spcae bar to open door
        cdef keys = pygame.key.get_just_pressed()

        if keys[pygame.K_SPACE]: # fix this shit
            if obj.name == 'base':
                self.right, self.left, self.up, self.down, = False, True, False, False
                self.respawn = self.location
                self.location = obj.name
                self.nav = True

            elif obj.name == 'map2':
                self.right, self.left, self.up, self.down, = False, False, True, False
                self.respawn = self.location
                self.location = obj.name
                self.nav = True

            elif obj.name == 'map3':
                self.right, self.left, self.up, self.down, = False, False, True, False
                self.respawn = self.location
                self.location = obj.name
                self.nav = True

            elif obj.name == 'map4':
                self.right, self.left, self.up, self.down, = False, False, False, True
                self.respawn = self.location
                self.location = obj.name
                self.nav = True

            self.walk = 0

    def navigate(self):
        if self.nav:
            self.rect.x, self.rect.y = self.MapObjects[f'{self.respawn}_{self.location}'].rect.x, self.MapObjects[f'{self.respawn}_{self.location}'].rect.y

        self.nav = False

    # for picking items and opening a chestboxes
    def pick(self, obj):
        # click space bar to pick the object or open the object
        cdef keys = pygame.key.get_just_pressed()

        if keys[pygame.K_SPACE]:
            for item in obj.loaded:
                self.inventories.append(item)
                print(f'inventory: {self.inventories}')
                obj.loaded = []

            # print(self.inventories, len(self.inventories))

    # animate the fight
    def handleFight(self, enemies, screen):
        # use space bar to fight
        cdef keys = pygame.key.get_just_pressed()

        if self.equiped == self.weapons[0]:
            self.Sword(screen)

        if keys[pygame.K_SPACE]:
            self.attack = True
            for enemy in enemies:
                if pygame.sprite.collide_rect(self, enemy):
                    if self.left and self.rect.x > enemy.rect.x:
                        enemy.attacked = True
                        enemy.life -= self.power
                        enemy.push = 10
                    elif self.right and self.rect.x < enemy.rect.x:
                        enemy.attacked = True
                        enemy.life -= self.power
                        enemy.push = 10
                    elif self.down and self.rect.y < enemy.rect.y:
                        enemy.attacked = True
                        enemy.life -= self.power
                        enemy.push = 10
                    elif self.up and self.rect.y > enemy.rect.y:
                        enemy.attacked = True
                        enemy.life -= self.power
                        enemy.push = 10

    def Sword(self, screen):
        if self.attack and self.attacking > 0:
            if self.up:
                screen.blit(self.sword[0], (self.rect.x, self.rect.y))
            elif self.down:
                screen.blit(self.sword[2], (self.rect.x, self.rect.y))
            elif self.right:
                screen.blit(self.sword[1], (self.rect.x, self.rect.y))
            elif self.left:
                screen.blit(self.sword[3], (self.rect.x-25, self.rect.y))
            self.attacking -= 1
        else:
            self.attacking = 3
            self.attack = False

# enemy variant 1
class Enemy(pygame.sprite.Sprite):

    def __init__(self, int x, int y, int width, int height, str name=''):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name

        # rect
        self.rect = pygame.Rect((x, y), (self.width, self.height))
        self.image = pygame.Surface((self.width, self.height))

        self.speed = random.choice([2.5, 3, 3.5])
        self.attacked = False # attacked by the player
        self.defaultLife = 20
        self.life = 0
        self.push = 10
        self.pushed = False

        # facing
        self.left = True
        self.right = False
        self.up = False
        self.down = False
        self.walk = 0 # count of walk

        # images / character
        self.e_left = []
        self.e_right = []
        # load and flip image
        self.loadImages()
        self.flipImage()

    # draw the enemy
    def draw(self, object screen, list objects):

        # handle collision
        self.hit()
        self.handlePushed()
        self.handleCollision(objects)
        
        if (self.walk + 1) >= 21:
            self.walk = 0

        if self.left or self.up:
            if self.rect.x > -self.width and self.rect.x < 700 and self.rect.y > -self.height and self.rect.y < 500:
                screen.blit(self.e_left[self.walk//3], (self.rect.x, self.rect.y))
            self.walk += 1
        elif self.right or self.down:
            if self.rect.x > -self.width and self.rect.x < 700 and self.rect.y > -self.height and self.rect.y < 500:
                screen.blit(self.e_right[self.walk//3], (self.rect.x, self.rect.y))
            self.walk += 1
        else:
            if self.rect.x > -self.width and self.rect.x < 700 and self.rect.y > -self.height and self.rect.y < 500:
                if self.left:
                    screen.blit(self.e_left[0], (self.rect.x, self.rect.x))
                elif self.right:
                    screen.blit(self.e_right[0], self.rect.x, self.rect.y)

        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

        self.barLife(screen)

    def barLife(self, screen):
        pygame.draw.rect(screen, (207, 208, 255), (self.rect.x, self.rect.y - (self.height / 2) + 10, self.width, 5))
        pygame.draw.rect(screen, (252, 78, 15), (self.rect.x, self.rect.y - (self.height / 2) + 10, (self.life / self.defaultLife) * self.width, 5))

    # enemy x and y move directions
    def move_x(self, int direction):
        self.rect.x += direction

    def move_y(self, int direction):
        self.rect.y += direction

    # enemy follow player until player's life is 0
    def follow(self, player):
        if player.life > 0 and not(self.pushed):
            if self.rect.x > player.rect.x + 35:
                self.left = True
                self.right = False
                self.up = False
                self.down = False
                self.move_x(self.speed * -1)
            elif self.rect.x < player.rect.x - 35:
                self.left = False
                self.right = True
                self.up = False
                self.down = False
                self.move_x(self.speed)
            elif self.rect.y > player.rect.y + 35:
                self.left = False
                self.right = False
                self.up = True
                self.down = False
                self.move_y(self.speed * -1)
            elif self.rect.y < player.rect.y - 35:
                self.left = False
                self.right = False
                self.up = False
                self.down = True
                self.move_y(self.speed)
            else:
                self.walk = 0

    # load enemies image
    def loadImages(self):
        for character in range(7):
            image = f'characters/goblin/S_Walk_{character+1}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.width, self.height))
            self.e_left.append(image)

    # flip the image of enemy
    def flipImage(self):
        for character in self.e_left:
            self.e_right.append(pygame.transform.flip(character, True, False))

    # enemies collision
    def handleCollision(self, objects):
        for object in objects:
            if object._type not in ['hidden2', 'other2']:
                if self.left or self.right:
                    if self.rect.y > object.rect.y:
                        object.e_front.append(self)
                    elif self.rect.y <= object.rect.y:
                        if self in object.e_front:
                            object.e_front.remove(self)
            if pygame.sprite.collide_rect(self, object):
                if object._type not in ['hidden2', 'other2']:
                    if self.left:
                        if self.rect.y <= object.rect.y:
                            self.rect.left = object.rect.right
                    elif self.right:
                        if self.rect.y <= object.rect.y:
                            self.rect.right = object.rect.left

                    elif self.up and self in object.e_front:
                        if self.rect.top < object.rect.bottom - 40:
                            self.rect.top = object.rect.bottom - 40
                    elif self.down and self not in object.e_front:
                        self.rect.bottom = object.rect.top
                else:
                    if self.right:
                        self.rect.right = object.rect.left
                    elif self.left:
                        self.rect.left = object.rect.right
                    elif self.up:
                        self.rect.top = object.rect.bottom
                    elif self.down:
                        self.rect.bottom = object.rect.top
                        
    def hit(self):
        if self.attacked:
            if self.down:
                self.up = True
                self.down = False
            elif self.up:
                self.up = False
                self.down = True
            elif self.right:
                self.right = False
                self.left = True
            elif self.left:
                self.left = False
                self.right = True
            self.pushed = True
        self.attacked = False

    def handlePushed(self):
        if self.pushed and self.push > 0:
            if self.up:
                self.move_y(-15)
            elif self.down:
                self.move_y(15)
            elif self.left:
                self.move_x(-15)
            elif self.right:
                self.move_x(15)
            self.push -= 1
        else:
            self.pushed = False

class NPC(pygame.sprite.Sprite):

    def __init__(self, int x, int y, int width, int height, str name=''):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.image = pygame.Surface((self.width, self.height))

        self.c_left = []
        self.c_right = []
        self.c_up = []
        self.c_down = []
        if self.name != '':
            self.loadImages()
            self.flip()

    def draw(self, screen):
        if self.name != '':
            screen.blit(self.c_down[0], self.rect)
        else:
            pygame.draw.rect(screen, (255,255,255), self.rect)

    def loadImages(self):
        sides = ['D_Walk_', 'S_Walk_', 'U_Walk_']

        for side in sides:
            for i in range(7):
                image = f'characters/NPC/{self.name}/{side}{i}.png'
                image = pygame.image.load(image)
                image = pygame.transform.scale(image, (self.width, self.height))
                if side == sides[0]:
                    self.c_down.append(image)
                elif side == sides[1]:
                    self.c_left.append(image)
                elif side == sides[2]:
                    self.c_up.append(image)
                else:
                    print('not found')

    def flip(self):
        for image in self.c_left:
            c_right = pygame.transform.flip(image, True, False)
            self.c_right.append(c_right)