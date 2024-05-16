import pygame
import csv
import os

# for loading screen

class Loading:

    def __init__(self, int x, int y, int width, int height):
        self.width = width
        self.height = height
        self.rect_max = pygame.Rect(x, y, self.width, self.height)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        self.loaded = 0
        self.resources = []
        self.load()

        self.count = self.width / len(self.resources)

        self.check = 30

    def draw(self, object screen):
        pygame.draw.rect(screen, (255,255,255), self.rect_max)
        pygame.draw.rect(screen, (121, 168, 242), (self.rect.x, self.rect.y, self.loaded, self.height))

    def load(self):
        with open('Data/resources.csv', newline='') as sources_files:
            resourcesData = csv.reader(sources_files, quoting=csv.QUOTE_NONE)

            for row in resourcesData:
                self.resources.append(row)
        
    def checkResources(self):
        for path in self.resources:
            if self.loaded < self.rect.width:
                if self.check <= 0:
                    if os.path.exists(f'{path[1]}/{path[0]}'):  
                        self.loaded += self.count
                        self.check = 30
                self.check-=1
            else:
                return True