import pygame
from . import weapons

class Object(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, _type = '', name='', animated=False):
        super().__init__()
        self.width = width
        self.height = height
        self._type = _type
        self.name = name
        self.animated = animated

        # if player is above or bellow the object
        self.front = False

        # enemies in front of abj
        self.e_front = []

        self.rect = pygame.Rect((x, y), (self.width, self.height)) # oject rect
        self.image = pygame.Surface((self.width, self.height)) # object surface

        # non animated object/image
        self.nonAnimated = ''
        self.loadNonAnimated() # all all non animated objects

        # for animated object
        self.animation = 0
        self.animatedObjects = [] # load all animated image here
        if self._type in ['animated', 'animated_once']:
            self.loadAnimated() # all animated image loaded

        # for chestboxes
        self.loaded = []

    def draw(self, screen):
        # Optimizing rendering objects - rendering the object when the object is in the display
        # if x position is greater than the negative side of the object and if x position is less than the size of the width of the screen and y position is greater than the size of the object and y position is less than the height of the screen then render the image of tile

        if self._type in ['other', 'other2', 'bg_image']:
            if self.rect.x > -self.rect.width and self.rect.x < 700 and self.rect.y > -self.height and self.rect.y < 500:
                screen.blit(self.nonAnimated, self.rect)

        elif self._type == 'animated':
            if self.rect.x > -self.rect.width and self.rect.x < 700 and self.rect.y > -self.height and self.rect.y < 500:
                self.animate(screen) # auto animating if the object is animated(note animated_once)

        # for debuging or testing
        # else:
        #     pygame.draw.rect(screen, (255,0,0), self.rect, 1)

        # pygame.draw.rect(screen, (255,255,255), self.rect, 1)

    def move_x(self, direction):
        self.rect.x += direction

    def move_y(self, direction):
        self.rect.y += direction

    def animate(self, screen):
        if(self.animation + 1) >= 63:
            self.animation = 0

        screen.blit(self.animatedObjects[self.animation//9], (self.rect.x, self.rect.y))
        self.animation += 1

    # load animated objects here
    def loadAnimated(self):
        for i in range(7):
            image = f'characters/animatedObj/{self.name}/frame_{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.width, self.height))
            self.animatedObjects.append(image)
    
    # load non animated objects here
    def loadNonAnimated(self):
        if self._type in ['other', 'other2']:
            image = pygame.image.load(f'characters/objects/{self.name}.png')
            self.nonAnimated = pygame.transform.scale(image, (self.width, self.height))

        elif self._type == 'bg_image':
            image = pygame.image.load(f'characters/objects/{self.name}.jpg')
            self.nonAnimated = pygame.transform.scale(image, (self.width, self.height))

    # for chestbox
    def loadChestBox(self, items, player, screen):
        for item in items:
            item = weapons.Items(player, screen, (25,25), item)
            self.loaded.append(item)