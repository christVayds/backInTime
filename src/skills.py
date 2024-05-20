import pygame
# Skills = speed, boomerang, shield, clone - other shield(back to enemy its own attack), ice spike, lightning bolt, mana drain(steal mana), clone self

class Skills:

    def __init__(self, player, screen, scale=None, animated='normal'):

        # player's rect
        self.player = player
        self.animated = animated
        self.screen = screen
        self.triggered = False
        self.level = 1

        self.image = None
        self.animatedImage = []
        self.frame = 0 # for animation
        self.scale = scale

        # check if animated or not
        if self.animated == 'animated':
            self.loadAnimation()
            # skills rect
            self.rect = pygame.Rect(self.player.rect.x, self.player.rect.y, self.scale[0], self.scale[1])
        elif self.animated == 'normal':
            self.loadImage()
            # skills rect
            self.rect = pygame.Rect(self.player.rect.x, self.player.rect.y, self.scale[0], self.scale[1])

    # draw skills
    def draw(self):
        if self.animated == 'animated':
            if (self.frame + 1) >= 21:
                self.frame = 0
            self.screen.blit(self.animatedImage[self.frame//3], self.rect)
            self.frame += 1
        else:
            self.screen.blit(self.image, self.rect)

    # for none animated skills
    def loadImage(self):
        image = f'characters/Skills/{self.player.name}/skill.png'
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
        self.image = image

    def trigger(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_r] and not(self.triggered):
            self.triggered = True

    # for animated skills
    def loadAnimation(self):
        for count in range(7):
            image = f'characters/Skills/{self.player.name}/skill_{count}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
            self.animatedImage.append(image)

    def Hit(self, enemies, damage, delay=0):
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                if delay <= 0:
                    enemy.attacked = True
                    enemy.life -= damage

class Speed(Skills):

    def __init__(self, player, screen, animated='none'):
        super().__init__(player, screen=screen, animated=animated)
        self.cooldown = 120
        self.speed = 15 # max speed: 15px

    def skill(self, enemies=[]):
        if self.triggered and self.cooldown > 0:
            self.player.speed = self.speed
            self.cooldown -= 1
        else:
            self.triggered = False
            self.cooldown = 120
            self.player.speed = 7

class Boomerang(Skills):

    def __init__(self, player, screen, scale):
        super().__init__(player, screen, scale)
        self.range = 50
        self.throw = self.range
        self.speed = 20
        self.power = 5

    def skill(self, enemies):
        if self.triggered and self.throw > 0:
            self.Move()
            self.draw()
            self.Hit(enemies, self.power)
            self.throw -= 1
        else:
            self.throw = self.range
            self.triggered = False
            self.rect.x = (self.player.rect.x + (self.rect.width - self.player.width) / 2) 
            self.rect.y = (self.player.rect.y + (self.rect.width - self.player.height) / 2)

    def Move(self):
        if self.player.up:
            self.rect.y -= self.speed
        elif self.player.down:
            self.rect.y += self.speed
        elif self.player.right:
            self.rect.x += self.speed
        elif self.player.left:
            self.rect.x -= self.speed

class Shield(Skills):

    def __init__(self, player, screen, scale, animated='animated'):
        super().__init__(player, screen, scale, animated=animated)
        self.cooldown = 150
        self.temporarySheild = 500
        self.c_shield = None
        self.delay = 30
        self.damage = 0.5

    def skill(self, enemies=[]):
        if self.triggered and self.cooldown > 0:
            self.c_shield = self.player.sheildPower
            self.player.shieldPower = self.temporarySheild

            self.rect.x = self.player.rect.x + (self.player.width - self.rect.width) / 2
            self.rect.y = self.player.rect.y + (self.player.height - self.rect.height) / 2
            self.draw()
            self.Hit(enemies, self.damage, self.delay)
            
            if self.delay <= 0:
                self.delay = 30

            self.delay -= 1
            self.cooldown -= 1
        else:
            self.cooldown = 120
            self.triggered = False
            self.player.sheildPower = self.c_shield

class Clone(Skills):

    def __init__(self, player, screen, scale, animated='animated'):
        super().__init__(player, screen, scale, animated)