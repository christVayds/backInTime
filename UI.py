import pygame

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