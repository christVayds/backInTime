# weapons - sheild, bomb, boomerang, traps bomb, fire ball

import pygame

class Weapon:
    
    def __init__(self, player, screen, scale, name, animated=False):
        self.player = player
        self.screen = screen
        self.scale = scale
        self.name = name
        self.animated = animated

        # keys
        self.triggered = False
        self.c_triggered = False
        self.level = 1

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
            if (self.frame + 1) >= 21:
                self.frame = 0
            self.screen.blit(self.Animated[self.frame//3], self.rect)
            self.frame += 1
        else:
            self.screen.blit(self.noneAnimated, self.rect)

    def Hit(self, enemies, damage=0.5):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.attacked = True
                enemy.life -= damage

    def loadNoneAnimated(self):
        image = f'characters/weapons/{self.name}/weapon.png'
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
        self.noneAnimated = image

    def loadAnimated(self):
        for i in range(7):
            image = f'characters/weapons/{self.name}/weapon_{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
            self.Animated.append(image)

    def Trigger(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_c]:
            self.c_triggered = True

    def Trigger_mouse(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            self.mouse = True
            self.triggered = True
            mx, my = pygame.mouse.get_pos()
            self.mouseDirection = pygame.Vector2(mx, my)

    def Trigger_mouse2(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[2]:
            self.mouse = True
            self.triggered = True
            mx, my = pygame.mouse.get_pos()
            self.mouseDirection = pygame.Vector2(mx, my)

    def move_x(self, direction):
        self.rect.x += direction

    def move_y(self, direction):
        self.rect.y += direction

class Sheild(Weapon):

    def __init__(self, player, screen, scale, name='sheild', animated=True):
        super().__init__(player, screen, scale, name, animated)
        self.duration = 120

    def weapon(self, enemies=[]):
        if self.c_triggered and self.duration > 0:
            self.rect.x = self.player.rect.x + (self.player.width - self.rect.width) / 2
            self.rect.y = self.player.rect.y + (self.player.height - self.rect.height) / 2
            self.draw()
            self.duration -= 1
        else:
            self.c_triggered = False
            self.duration = 120

class Bomb(Weapon):

    def __init__(self, player, screen, scale, name='bomb', animated=True):
        super().__init__(player, screen, scale, name, animated)
        self.duration = 90
        self.far = 3
        self.speed = 15
        self.particles = []
        self.bframe = 0
        self.loadExplosion()

    def weapon(self, enemies=[]):
        if self.triggered and self.duration > 0 and self.mouse:
            if self.duration <= 20:
                self.Explode()
            else:
                self.Throw()
                self.draw()
            self.duration -= 1
            self.far -= 1
        else:
            self.triggered = False
            self.duration = 90
            self.far = 3
            self.mouse = False
            self.bframe = 0

    def Throw(self):
        if self.far >= 3:
            self.vecPos = pygame.Vector2(self.player.rect.x, self.player.rect.y)
            self.direction = (self.mouseDirection - self.vecPos).normalize()
        if self.far > 0:
            self.vecPos += self.direction * self.speed
            self.rect.x, self.rect.y = self.vecPos.x, self.vecPos.y

    def Explode(self):
        if (self.bframe + 1) >= 20:
            self.bframe = 0

        self.screen.blit(self.particles[self.bframe], (self.rect.x + ((self.rect.width - 100) / 2), self.rect.y + (self.rect.height - 100) / 2))
        self.bframe += 1

    def loadExplosion(self):
        for i in range(20):
            image = f'characters/weapons/explosion/{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (100, 100))
            self.particles.append(image)
        

class Boomerang(Weapon):

    def __init__(self, player, screen, scale, name='boomerang', animated=True):
        super().__init__(player, screen, scale, name, animated)
        self.range = 20
        self.throw = self.range
        self.speed = 20
        self.throwed = True
        self.damage = 1

    def weapon(self, enemies=[]):
        if self.triggered and self.mouse:
            if self.throw >= 10:
                self.mouse_Throw()
                self.draw()
                self.Hit(enemies, self.damage)
            else:
                if not self.follow():
                    self.draw()
                    self.Hit(enemies)
                else:
                    self.triggered = False
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
    
    def mouse_Throw(self):
        if self.throw >= self.range:
            self.vectorPos = pygame.Vector2(self.player.rect.x, self.player.rect.y)
            self.direction = (self.mouseDirection - self.vectorPos).normalize()
        self.vectorPos += self.direction * self.speed
        self.rect.x = self.vectorPos.x
        self.rect.y = self.vectorPos.y

class Items(Weapon):

    def __init__(self, player, screen, scale, name, animated=False):
        super().__init__(player, screen, scale, name, animated)