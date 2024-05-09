import pygame

class TileMap():
    def __init__(self, tilesize, x, y):
        pygame.init()
        self.tilesize = tilesize
        self.images = []
        self.x = x
        self.y = y
        self.name = 'Map2'
        self.images.append(pygame.transform.scale(pygame.image.load("characters/objects/border_1.png").convert(), (self.tilesize, self.tilesize)))
        self.images.append(pygame.transform.scale(pygame.image.load("characters/objects/floor_2.png").convert(), (self.tilesize, self.tilesize)))
        self.images.append(pygame.transform.scale(pygame.image.load("characters/objects/wall_1.png").convert(), (self.tilesize, self.tilesize)))
        self.array = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    def drawMap(self, surface):
            for i,row in enumerate(self.array):
                for j,tile in enumerate(row):
                    if tile > 0:
                        surface.blit(self.images[tile - 1], (self.x + j * self.tilesize, self.y + i * self.tilesize))

    def move_x(self, direction):
         self.x += direction
        
    def move_y(self, direction):
         self.y += direction