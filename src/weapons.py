# weapons - sheild, bomb, boomerang, traps bomb, snowball, mjolnir, tredent, shuriken
import pygame
import math
import json

class Weapon:
    
    def __init__(self, player, screen, scale, name, animated=False, _type='weapon'):
        self.player = player
        self.screen = screen
        self.scale = scale
        self.name = name
        self.animated = animated
        
        self._type = _type
        self.data = None
        self.code = None

        # keys
        self.triggered = False
        self.c_triggered = False
        self.level = 1
        self.effect = False

        self.damage = 0.5 # default damage
        self.speed = 5 # default speed
        self.absorb = 0 # sheild absorb
        self.mana = 0.2

        # get mouse positions
        self.mouse = False
        self.mouseDirection = pygame.Vector2(0,0)

        self.noneAnimated = None
        self.Animated = []
        if self.animated:
            self.frame = 0
            self.loadAnimated()
            self.rect = pygame.Rect(self.player.rect.x, self.player.rect.y, self.scale[0], self.scale[1])
            self.icon = self.Animated[0]
        else:
            self.loadNoneAnimated()
            self.rect = pygame.Rect(self.player.rect.x, self.player.rect.y, self.scale[0], self.scale[1])
            self.icon = self.noneAnimated

    def draw(self):
        if self.animated:
            if (self.frame + 1) >= 12:
                self.frame = 0
            self.screen.blit(self.Animated[self.frame//3], self.rect)
            self.frame += 1
        else:
            self.screen.blit(self.noneAnimated, self.rect)

    def Hit(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.attacked = True
                enemy.life -= self.damage
                return True
        return False
    
    def decreaseMana(self):
        if self.player.mana > 1:
            self.player.mana -= self.mana

    def loadNoneAnimated(self):
        if self._type == 'weapon':
            image = f'characters/weapons/{self.name}/weapon.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
        else:
            image = f'characters/weapons/potions/{self.name}/potion.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))

        self.noneAnimated = image

    def loadAnimated(self):
        for i in range(4):
            image = f'characters/weapons/{self.name}/weapon_{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
            self.Animated.append(image)

    def Trigger(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_c] and self.player.mana > 5:
            self.c_triggered = True

    def Trigger_mouse(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and self.player.mana > 5:
            self.mouse = True
            self.triggered = True
            mx, my = pygame.mouse.get_pos()
            self.mouseDirection = pygame.Vector2(mx, my)

    def Trigger_mouse2(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[2] and self.player.mana > 5:
            self.mouse = True
            self.triggered = True
            mx, my = pygame.mouse.get_pos()
            self.mouseDirection = pygame.Vector2(mx, my)

    def Throw(self, range):
        if self.throw >= range:
            self.vectorPos = pygame.Vector2(self.player.rect.x, self.player.rect.y)
            self.direction = (self.mouseDirection - self.vectorPos).normalize()
        self.vectorPos += self.direction * self.speed
        self.rect.x = self.vectorPos.x
        self.rect.y = self.vectorPos.y

    def addLevel(self):
        pass

    def move_x(self, direction):
        self.rect.x += direction

    def move_y(self, direction):
        self.rect.y += direction

class Sheild(Weapon): # regular shield

    def __init__(self, player, screen, scale, name='sheild', animated=True, _type='shield'):
        super().__init__(player, screen, scale, name, animated, _type)
        self.duration = 120
        self.absorb = 5
        self.mana = 0.01

    def weapon(self, enemies=[]):
        if self.c_triggered and self.duration > 0:
            self.rect.x = self.player.rect.x + (self.player.width - self.rect.width) / 2
            self.rect.y = self.player.rect.y + (self.player.height - self.rect.height) / 2
            self.draw()
            self.duration -= 1
            self.decreaseMana()
        else:
            self.c_triggered = False
            self.duration = 120

class BoomShield(Weapon): # combination of weapon and shield

    def __init__(self, player, screen, scale, name='Boomerang sheild', animated=False, _type='weapon-sheild'):
        super().__init__(player, screen, scale, name, animated, _type)
        self.mana = 1

class Bomb(Weapon):

    def __init__(self, player, screen, scale, name='bomb', animated=True):
        super().__init__(player, screen, scale, name, animated)
        self.duration = 90
        self.far = 3
        self.speed = 15
        self.bframe = 0
        self.mana = 0.5

    def weapon(self, enemies=[]):
        if self.triggered and self.duration:
            if self.duration <= 20:
                self.effect = True
            else:
                self.Throw()
                self.draw()
            self.decreaseMana()
            self.duration -= 1
            self.far -= 1
        else:
            # reset
            self.triggered = False
            self.duration = 90
            self.far = 3
            self.mouse = False
            self.bframe = 0
            self.effect = False

    def Throw(self):
        if self.far >= 3:
            self.vecPos = pygame.Vector2(self.player.rect.x, self.player.rect.y)
            self.direction = (self.mouseDirection - self.vecPos).normalize()
        if self.far > 0:
            self.vecPos += self.direction * self.speed
            self.rect.x, self.rect.y = self.vecPos.x, self.vecPos.y
        

class Boomerang(Weapon):

    def __init__(self, player, screen, scale, name='boomerang', animated=True):
        super().__init__(player, screen, scale, name, animated)
        self.range = 20
        self.throw = self.range
        self.speed = 20
        self.damage = 1
        self.mana = 0.6

    def weapon(self, enemies=[]):
        if self.triggered and self.mouse:
            if self.throw >= 10:
                self.Throw(self.range)
            else:
                if self.follow():
                    self.triggered = False
            self.draw()
            self.Hit(enemies)
            self.decreaseMana()
            self.throw -= 1
        else:
            self.triggered = False
            self.mouse = False
            self.throw = self.range

    def follow(self):
        playerPos = pygame.Vector2(self.player.rect.x, self.player.rect.y)
        boomerangPos = pygame.Vector2(self.rect.x, self.rect.y)
        direction = (playerPos - boomerangPos).normalize()
        boomerangPos += direction * self.speed
        self.rect.x = boomerangPos.x
        self.rect.y = boomerangPos.y

        # check for collision
        if self.rect.colliderect(self.player.rect):
            return True
        
        return False

class SnowBall(Weapon):

    def __init__(self, player, screen, scale, name='snowball', animated=False):
        super().__init__(player, screen=screen, scale=scale, name=name, animated=animated)
        self.range = 10
        self.throw = self.range
        self.speed = 20
        self.damage = 0.8
        self.mana = 0.09

    def weapon(self, enemies=[]):
        if self.triggered and self.throw:
            self.Throw(self.range)
            self.draw()
            if self.Hit(enemies):
                self.triggered = False
            self.decreaseMana()
            self.throw -= 1
        else:
            # reset
            self.triggered = False
            self.mouse = False
            self.throw = self.range

class Trident(Weapon):

    def __init__(self, player, screen, scale, name='trident', animated=False):
        super().__init__(player, screen, scale, name, animated)
        self.range = 15
        self.throw = self.range
        self.damage = 1.5
        self.speed = 23
        self.mana = 0.9

    def weapon(self, enemies):
        if self.triggered and self.throw:
            self.Throw(self.range)
            self.rotate()
            self.Hit(enemies)
            self.decreaseMana()
            self.throw -= 1
        else:
            #reset
            self.triggered = False
            self.mouse = False
            self.throw = self.range

    def rotate(self):
        dis_x, dis_y = self.mouseDirection.x - self.player.rect.x, self.mouseDirection.y - self.player.rect.y
        angle = math.atan2(-dis_y, dis_x)
        trident = pygame.transform.rotate(self.noneAnimated, math.degrees(angle) - 90)
        trident_rect = trident.get_rect(center=(self.rect.x, self.rect.y))
        self.screen.blit(trident, trident_rect)

class Shuriken(Weapon):

    def __init__(self, player, screen, scale, name='shuriken', animated=False):
        super().__init__(player, screen, scale, name, animated)
        self.range = 20
        self.throw = self.range
        self.damage = 0.9
        self.speed = 20
        self.mana = 0.01

    def weapon(self, enemies):
        if self.triggered and self.throw:
            self.Throw(self.range)
            self.rotate()
            if self.Hit(enemies):
                self.triggered = False
                self.decreaseMana()
            self.throw -= 1
        else:
            self.triggered = False
            self.mouse = False
            self.throw = self.range

    def rotate(self):
        dis_x, dis_y = self.mouseDirection.x - self.player.rect.x, self.mouseDirection.y - self.player.rect.y
        angle = math.atan2(-dis_y, dis_x)
        trident = pygame.transform.rotate(self.noneAnimated, math.degrees(angle) - 90)
        trident_rect = trident.get_rect(center=(self.rect.x, self.rect.y))
        self.screen.blit(trident, trident_rect)

class Mjolnir(Weapon):

    def __init__(self, player, screen, scale, name='mjolnir', animated=True):
        super().__init__(player, screen, scale, name, animated)
        self.range = 30
        self.throw = self.range
        self.damage = 2
        self.speed = 25
        self.return_radius = 150
        self.angle = 0
        self.mana = 1

    def weapon(self, enemies):
        if self.triggered:
            if self.throw >= self.range / 2:
                self.Throw(self.range)
            else:
                # if self.Rotate():
                #     self.triggered = False
                if self.follow(): # temporary use the follow function
                    self.throw = 0
                    self.triggered = False
            self.decreaseMana()
            self.draw()
            self.Hit(enemies)
            self.throw -= 1
        else:
            #reset
            self.triggered = False
            self.mouse = False
            self.throw = self.range
            self.angle = 0

    def follow(self):
        playerPos = pygame.Vector2(self.player.rect.x, self.player.rect.y)
        boomerangPos = pygame.Vector2(self.rect.x, self.rect.y)
        direction = (playerPos - boomerangPos).normalize()
        boomerangPos += direction * self.speed
        self.rect.x = boomerangPos.x
        self.rect.y = boomerangPos.y

        # check for collision
        if self.rect.colliderect(self.player.rect):
            return True
        
        return False
    
    def Rotate(self): # fix this
        self.angle += 0.1
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

        self.rect.x = self.player.rect.x + self.return_radius * math.cos(self.angle)
        self.rect.y = self.player.rect.y + self.return_radius * math.sin(self.angle)

        if self.rect.colliderect(self.player.rect):
            return True


class Potions(Weapon):

    def __init__(self, player, screen, scale, name, animated=False, _type='potion'):
        super().__init__(player, screen, scale, name, animated, _type)
        self.potionData = {}
        self.applyMana = False
        self.LoadData()

    def Use(self):
        if self.player.life < self.player.defaultLife:
            self.player.life += self.potionData[self.name]['support']
        if self.player.mana < self.player.defaultMana:
            self.player.mana += self.potionData[self.name]['plus-mana']

    def Apply(self, weapon):
        weapon.damage += self.potionData[self.name]['damage']
        self.player.speed += self.potionData[self.name]['speed'] # add to your speed
        if weapon.mana > self.potionData[self.name]['weapon-support']:
            self.applyMana = True
            weapon.mana = round(weapon.mana - self.potionData[self.name]['weapon-support'], 2)
        else:
            self.applyMana = False

        print(f'name: {weapon.name} damage: {weapon.damage} - mana: {weapon.mana}') # for testing and debuging

    def Remove(self, weapon):
        weapon.damage = round(weapon.damage - self.potionData[self.name]['damage'], 2)
        self.player.speed -= self.potionData[self.name]['speed']
        if self.applyMana:
            weapon.mana += self.potionData[self.name]['weapon-support'] # theres something wrong with this

    def LoadData(self):
        with open('Data/weapons.json') as file:
            self.potionData = json.load(file)

        self.damage = self.potionData[self.name]['damage']
        self.absorb = self.potionData[self.name]['shield-support']

class Items(Weapon):

    def __init__(self, player, screen, scale, name, animated=False, _type='item'):
        super().__init__(player, screen, scale, name, animated, _type)
        self.code = None
        self.openData()

    def loadNoneAnimated(self):
        image = f'characters/icons/{self.name}.png'
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
        self.noneAnimated = image

    def openData(self):
        with open('data/items.json') as file:
            self.data = json.load(file)

    def checkItem(self):
        try:
            self.code = self.data['Items'][self.name]['code']
            self.name = self.data['Items'][self.name]['name']
            return True
        except KeyError:
            return False

class Effects:

    def __init__(self, screen):
        self.screen = screen
        self.weapons = None # the weapons

        self.loaded = []

    def effects(self):
        if self.weapons.effect: # if the weapon effects is true or the weapon is ready to effects
            self.draw() # draw the effect animation

    def draw(self):
        # draw the animation
        if (self.weapons.bframe + 1) >= 20:
            self.weapons.bframe = 0

        self.screen.blit(self.loaded[self.weapons.bframe], (self.weapons.rect.x + ((self.weapons.rect.width - 100) / 2), self.weapons.rect.y + (self.weapons.rect.height - 100) / 2))
        self.weapons.bframe+=1

    def loadEffects(self, equiped):
        self.weapons = equiped

        try: # check if the weapon has effects
            for i in range(20):
                image = f'characters/effects/{self.weapons.name}/second/{i}.png'
                image = pygame.image.load(image)
                image = pygame.transform.scale(image, (100, 100))
                self.loaded.append(image)

        except FileNotFoundError:
            print(f'{self.weapons.name} no effects')