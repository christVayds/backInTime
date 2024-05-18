import pygame
# Skills = speed, invesibility, boomerang, smash

class Skills:

    def __init__(self, player, screen, scale=None, animated='normal'):

        # player's rect
        self.player = player
        self.animated = animated
        self.screen = screen
        self.triggered = False

        self.image = None
        self.scale = scale
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
            pass
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
        pass

    def Hit(self, enemies, power):
        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                enemy.attacked = True
                enemy.life -= power

class Speed(Skills):

    def __init__(self, player, screen, animated='none'):
        super().__init__(player, screen=screen, animated=animated)
        self.cooldown = 120
        self.speed = 15

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
        self.throw = 50
        self.speed = 20
        self.power = 50

    def skill(self, enemies):
        if self.triggered and self.throw > 0:
            self.Move()
            self.draw()
            self.Hit(enemies, self.power)
            self.throw -= 1
        else:
            self.throw = 50
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

class Invisbility(Skills):

    def __init__(self, player, screen, animated='none'):
        super().__init__(player, screen, animated=animated)
        self.cooldown = 120

    def skill(self, enemies):
        if self.triggered and self.cooldown > 0:
            for enemy in enemies: # making enemies blind
                enemy.canFollow = False
            self.cooldown -= 1
        else:
            self.triggered = False
            self.cooldown = 120
            for enemy in enemies: # enemies back to normal
                enemy.canFollow = True

    def invisibility(self):
        raise NotImplemented

class Smash(Skills):

    def __init__(self, player):
        super().__init__(player)