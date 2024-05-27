import pygame

class TileMap():
    def __init__(self, tilesize):
        pygame.init()
        self.tilesize = tilesize
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load("C:/Users/Admin/OneDrive/Documents/backInTime/characters/objects/wall_2.png"), (self.tilesize, self.tilesize)))
        self.images.append(pygame.transform.scale(pygame.image.load("C:/Users/Admin/OneDrive/Documents/pygame_project/characters/objects/wall_4.png"), (self.tilesize, self.tilesize)))
        self.images.append(pygame.transform.scale(pygame.image.load("C:/Users/Admin/OneDrive/Documents/backInTime/characters/objects/tile_2.png"), (self.tilesize, self.tilesize)))
        self.images.append(pygame.transform.scale(pygame.image.load("C:/Users/Admin/OneDrive/Documents/pygame_project/characters/objects/wall_3.png"), (self.tilesize, self.tilesize)))
        self.images.append(pygame.transform.scale(pygame.image.load("C:/Users/Admin/OneDrive/Documents/pygame_project/characters/objects/wall_1.png"), (self.tilesize, self.tilesize)))
        self.images.append(pygame.transform.scale(pygame.image.load("C:/Users/Admin/OneDrive/Documents/pygame_project/characters/objects/border_1.png"), (self.tilesize, self.tilesize)))
        self.array = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0],
[1,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,1,3,3,3,3,3,3,3,3,1,0,0,0,0,0,0,0],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,6,6,6,6,6,6,6,6,1,0,0,0,5,5,5,5],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,6,6,6,6,6,6,6,6,1,0,0,0,5,5,5,5],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,6,6,6,6,6,6,6,6,1,0,0,0,5,5,5,5],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,6,6,6,6,6,6,6,6,1,0,0,0,2,2,2,2],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,2,6,6,6,6,6,6,6,6,1,0,0,0,4,4,4,4],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,2,6,6,6,6,6,6,6,6,1,0,0,0,0,0,0,0],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,6,6,6,6,6,6,6,6,1,0,0,0,0,0,0,0],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0],
[1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0],
[1,1,5,5,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
[2,1,5,5,5,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0],
[4,1,5,5,5,1,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0],
[0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    def drawMap(self, surface, location):
            for i,row in enumerate(self.array):
                for j,tile in enumerate(row):
                    if tile > 0:
                        surface.blit(self.images[tile - 1], (location[0] + j * self.tilesize, location[1] + i * self.tilesize))