# weapons - sword, sheild, bomb, boomerang

import pygame

class Weapon:
    
    def __init__(self, player, screen, scale, name, animated=False):
        self.player = player
        self.screen = screen
        self.scale = scale
        self.name = name
        self.animated = animated

        self.triggered = False
        self.level = 1

        self.noneAnimated = None
        self.Animated = []
        if self.animated:
            self.frame = 0
            self.loadAnimated()
            self.rect = pygame.Rect(self.player.rect.x, self.player.rect.y, self.scale[0], self.scale[1])
        else:
            self.loadNoneAnimated()
            self.rect = pygame.Rect(self.player.rect.x, self.player.rect.y, self.scale[0], self.scale[1])

    def draw(self):
        if self.animated:
            if (self.frame + 1) >= 21:
                self.frame = 0
            self.screen.blit(self.Animated[self.frame//3], self.rect)
            self.frame += 1
        else:
            self.screen.blit(self.noneAnimated, self.rect)

    def Hit(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.attacked = True
                enemy.life -= 3

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

        if keys[pygame.K_SPACE]:
            self.triggered = True

    def move_x(self, direction):
        self.rect.x += direction

    def move_y(self, direction):
        self.rect.y += direction

class Sheild(Weapon):

    def __init__(self, player, screen, scale, name='sheild', animated=True):
        super().__init__(player, screen, scale, name, animated)
        self.duration = 120

    def weapon(self, enemies=[]):
        if self.triggered and self.duration > 0:
            self.rect.x = self.player.rect.x + (self.player.width - self.rect.width) / 2
            self.rect.y = self.player.rect.y + (self.player.height - self.rect.height) / 2
            self.draw()
            self.duration -= 1
        else:
            self.triggered = False
            self.duration = 120

class Boomerang(Weapon):

    def __init__(self, player, screen, scale, name='boomerang', animated=True):
        super().__init__(player, screen, scale, name, animated)
        self.defaultThrow = 60
        self.throw = self.defaultThrow
        self.speed = 20
        self.throwed = True

        self.dx = 0
        self.dy = 0

    def weapon(self, enemies=[]):
        if self.triggered:
            if self.throw >= 30:
                self.Throw()
                self.Move()
                self.draw()
                self.Hit(enemies)
            else:
                if not self.follow():
                    self.draw()
                    self.Hit(enemies)
                else:
                    self.triggered = False
            self.throw -= 1
        else:
            self.triggered = False
            self.throw = self.defaultThrow

    def follow(self):
        if self.player.rect.x > self.rect.x:
            self.rect.x += self.speed
        if self.player.rect.x < self.rect.x:
            self.rect.x -= self.speed
        if self.player.rect.y > self.rect.y:
            self.rect.y += self.speed
        if self.player.rect.y < self.rect.y:
            self.rect.y -= self.speed

        # check for collision
        if self.rect.colliderect(self.player.rect):
            return True
        
        return False

    def Throw(self):
        if self.throw >= self.defaultThrow:
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y
            if self.player.up:
                self.dx = 0
                self.dy = -1
            elif self.player.down:
                self.dy = 1
                self.dx = 0
            elif self.player.right:
                self.dy = 0
                self.dx = 1
            elif self.player.left:
                self.dy = 0
                self.dx = -1

    def Move(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy