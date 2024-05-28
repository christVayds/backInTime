import pygame

# ENEMY BOSS FIGHT

class Boss(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.defaulLife = None
        self.life = self.defaulLife
        self.damage = 0

class Ethan(Boss):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

class Christian(Boss):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

class Aeron(Boss):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)