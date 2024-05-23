import pygame
import os

class UI(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, name='', _type='other'):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name
        self._type = _type

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.image = ((self.width, self.height))

        self.listAnimated = []
        self.selectors = []
        self.players = []
        self.selected = 0
        self.frameCount = 0
        if self._type == 'animated':
            self.loadAnimated()
        elif self._type == 'selector':
            self.loadSelector()
        elif self._type == 'selector_player':
            self.loadplayer()
        else:
            self.objectImage = self.loadImage()

    def draw(self, screen):
        if self._type == 'animated':
            self.animate(screen)
        elif self._type == 'selector':
            screen.blit(self.selectors[self.selected], self.rect)
        elif self._type == 'selector_player':
            screen.blit(self.players[0], self.rect)
        else:
            screen.blit(self.objectImage, self.rect)

        # pygame.draw.rect(screen, (255,255,255), self.rect, 2)

    def loadAnimated(self):
        for img in range(7):
            image = f'characters/animatedObj/{self.name}/frame_{img}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.width, self.height))
            self.listAnimated.append(image)

    def animate(self, screen):
        if(self.frameCount + 1) >= 63:
            self.frameCount = 0

        screen.blit(self.listAnimated[self.frameCount//9], (self.rect.x, self.rect.y))
        self.frameCount += 1
    
    def loadSelector(self):
        for i in range(2):
            image = f'characters/selectors/{self.name}/s_{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.width, self.height))
            self.selectors.append(image)

    def loadplayer(self):
        image = f'characters/selectors/players/{self.name}.png'
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (self.width, self.height))
        self.players.append(image)

    def loadImage(self):
        image = f'characters/objects/{self.name}.png'
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (self.width, self.height))
        return image
    
class GUI:

    def __init__(self, x, y, scale, screen, name):
        self.x = x
        self.y = y
        self.scale = scale
        self.screen = screen
        self.name = name
        
        self.selections = []
        self.loadImages()
        self.selected = 0

        self.sfx = None # sound effects
 
    def draw(self):
        self.screen.blit(self.selections[self.selected], (self.x, self.y))

    def Select(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_UP]:
            self.selected -= 1

            if self.selected < 0:
                self.selected = len(self.selections) -1
        elif keys[pygame.K_DOWN]:
            self.selected += 1

            if self.selected > len(self.selections) -1:
                self.selected = 0
        
        elif keys[pygame.K_SPACE]:
            return self.selected

    def loadImages(self):
        path = f'characters/GUI/{self.name}'
        for filename in os.listdir(path):
            if filename.endswith('.png'):
                image_path = os.path.join(path, filename)
                try:
                    image = pygame.image.load(image_path)
                    image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
                    self.selections.append(image)
                except pygame.error:
                    print('File not found:', image_path)