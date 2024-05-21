
import pygame

class Inventory:

    def __init__(self, player, screen, scale, pos):
        self.player = player
        self.screen = screen
        self.scale = scale

        self.selected = 0
        self.guis = []
        self.loadGUIs()
        self.rect = pygame.Rect(pos[0], pos[1], self.scale[0], self.scale[1])

        self.items = []

        # sfx
        self.sfx = []

    def draw(self):
        self.screen.blit(self.guis[self.selected], self.rect)

    def loadGUIs(self):
        for i in range(8):
            image = f'characters/GUI/weapons_gui/s_{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
            self.guis.append(image)

class Weapon(Inventory):

    def __init__(self, player, screen, scale, pos):
        super().__init__(player, screen, scale, pos)
        self.positions = [(225,280), (292,280), (358, 280), (424, 280)] # grid for all weapons and items - 8 items
        self.equiped = [(365, 195), (448, 195), (448, 108)] # for weapons equiped - 4 items

    def Select(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_TAB]:
            self.sfx[0].play()
            self.selected += 1
            if self.selected > (len(self.guis) -1):
                self.selected = 0
        elif keys[pygame.K_f]:
            self.sfx[1].play()
            return True
        return False
    
    def drawWeapons(self):
        eq1 = pygame.transform.scale(self.player.equiped1.icon, (45, 45))
        eq2 = pygame.transform.scale(self.player.equiped2.icon, (45, 45))
        eq_S = pygame.transform.scale(self.player.shield.icon, (45, 45))
        self.screen.blit(eq1, self.equiped[0])
        self.screen.blit(eq2, self.equiped[1])
        self.screen.blit(eq_S, self.equiped[2])
        for weapon in range(len(self.player.myWeapons)):
            wp = pygame.transform.scale(self.player.myWeapons[weapon].icon, (45, 45))
            self.screen.blit(wp, self.positions[weapon])