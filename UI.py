import pygame

class UI(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, name=''):
        super().__init__()
        self.width = width
        self.height = height
        self.name = name

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.image = ((self.width, self.height))
        self.objectImage = self.loadImage()

    def draw(self, screen):
        screen.blit(self.objectImage, self.rect)
        # pygame.draw.rect(screen, (255,255,255), self.rect, 2)

    def loadImage(self):
        image = f'characters/objects/{self.name}.png'
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (self.width, self.height))
        return image