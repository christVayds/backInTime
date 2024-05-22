import pygame

class Inventory:

    def __init__(self, player, screen, scale, pos, name):
        self.player = player
        self.screen = screen
        self.scale = scale
        self.name = name

        self.selected = 0
        self.guis = []
        self.weaponsgui = [] # for items gui viewing player's weapons
        self.loadGUIs()
        self.rect = pygame.Rect(pos[0], pos[1], self.scale[0], self.scale[1])

        self.items = []

        # sfx
        self.sfx = []

        self.font = pygame.font.SysFont('arial', 15)
        self.message = ''

    def draw(self):
        self.screen.blit(self.guis[self.selected], self.rect)

    def loadGUIs(self):
        for i in range(8):
            image = f'characters/GUI/{self.name}/s_{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
            self.guis.append(image)

    def showLabel(self):
        try:
            text = self.player.myWeapons[self.selected]
            text = self.font.render(f'Name: {text.name.title()}\nLevel: {text.level}\nDamage: {text.damage}\nAbsorb: {text.absorb}\n{self.message}', True, (255, 255, 255))
        except IndexError:
            text = self.font.render(f'Name: Empty\nLevel: 0\nDamage: 0\nAbsorb: 0', True, (255,255,255))
        self.screen.blit(text, (210,110))

class Items(Inventory):

    def __init__(self, player, screen, scale, pos, name='items_gui'):
        super().__init__(player, screen, scale, pos, name)
        self.chestGrid = []
        self.weaponGrid = []
        self.name = 'items_gui'
        self.focus = 'chestGrid'
        self.selectedWeapons = 0

    def draw(self):
        if self.focus == 'chestGrid':
            self.screen.blit(self.guis[self.selected], self.rect)
        else:
            self.screen.blit(self.weaponsgui[self.selectedWeapons], self.rect)

    def Select(self):
        pass

    def loadGUIs(self): # temporary
        for i in range(20):
            image = f'characters/GUI/{self.name}/s_{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
            self.guis.append(image)

        for i in range(8):
            image = f'characters/GUI/{self.name}/e_{i}.png'
            image = pygame.image.load(image)
            image = pygame.transform.scale(image, (self.scale[0], self.scale[1]))
            self.weaponsgui.append(image)

    def Select(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_TAB]:
            self.sfx[0].play()
            if self.focus == 'chestGrid':
                self.focus = 'weaponGrid'
            else:
                self.focus = 'chestGrid'

        if keys[pygame.K_RIGHT]:
            self.sfx[0].play()
            if self.focus == 'chestGrid':
                self.selected += 1 # increment selected

                if self.selected > (len(self.guis) -1): # if selected is greater than the number of boxes, reset to 0
                    self.selected = 0
            else:
                self.selectedWeapons += 1 # increment selected

                if self.selectedWeapons > (len(self.weaponsgui) -1): # if selected is greater than the number of boxes, reset to 0
                    self.selectedWeapons = 0

        elif keys[pygame.K_LEFT]:
            self.sfx[0].play()
            if self.focus == 'chestGrid':
                self.selected -= 1

                if self.selected < 0:
                    self.selected = len(self.guis) -1
            else:
                self.selectedWeapons -= 1 # increment selected

                if self.selectedWeapons < 0: # if selected is greater than the number of boxes, reset to 0
                    self.selectedWeapons = len(self.weaponsgui) -1

        elif keys[pygame.K_UP]:
            self.sfx[0].play()
            if self.focus == 'chestGrid':
                tmp = self.selected
                self.selected -= 5

                if self.selected < 0:
                    self.selected = tmp + 15

        elif keys[pygame.K_DOWN]:
            self.sfx[0].play()
            if self.focus == 'chestGrid':
                tmp = self.selected
                self.selected += 5

                if self.selected > len(self.guis) -1:
                    self.selected = tmp - 15

        # exit inventory
        elif keys[pygame.K_f] or keys[pygame.K_ESCAPE]:
            self.sfx[1].play()
            return True


class Weapon(Inventory):

    def __init__(self, player, screen, scale, pos, name='weapons_gui'):
        super().__init__(player, screen, scale, pos, name)
        self.name = 'weapon_gui'
        self.positions = [ # grid for all weapons and items - 8 items
            (225,280), (292,280), (358, 280), (424, 280),
            (225, 346), (292, 346), (358, 346), (424, 346)
            ]
        self.equiped = [(360, 195), (443, 195), (443, 108), (360, 108)] # for weapons equiped - 4 items

    def Select(self):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_TAB] or keys[pygame.K_RIGHT]:
            self.message = ''
            self.sfx[0].play()
            self.selected += 1 # increment selected

            if self.selected > (len(self.guis) -1): # if selected is greater than the number of boxes, reset to 0
                self.selected = 0

        elif keys[pygame.K_LEFT]:
            self.message = ''
            self.sfx[0].play()
            self.selected -= 1

            if self.selected < 0:
                self.selected = len(self.guis) -1

        elif keys[pygame.K_UP]:
            self.message = ''
            self.sfx[0].play()
            tmp = self.selected
            self.selected -= 4

            if self.selected < 0:
                self.selected = tmp + 4

        elif keys[pygame.K_DOWN]:
            self.message = ''
            self.sfx[0].play()
            tmp = self.selected
            self.selected += 4

            if self.selected > len(self.guis) -1:
                self.selected = tmp - 4

        # exit inventory
        elif keys[pygame.K_f] or keys[pygame.K_ESCAPE]:
            self.message = ''
            self.sfx[1].play()
            return True
        
        self.showLabel()
        self.SelectEquiped()
        
        return False
    
    def SelectEquiped(self):
        keys = pygame.key.get_just_pressed()

        try:
            if keys[pygame.K_q]:
                self.sfx[1].play() # play sfx
                if self.player.myWeapons[self.selected]._type not in ['potion', 'shield', 'item']:
                    if self.player.myWeapons[self.selected] != self.player.equiped2:
                        self.player.equiped1.effect = False # reset the effect
                        self.player.equiped1 = self.player.myWeapons[self.selected] # equiped the weapon
                    else:
                        self.message = 'You can\'t use \nalready equiped\nweapon'
                else:
                    self.message = f'You can\'t use \n{self.player.myWeapons[self.selected]._type}\nas a weapon'
            elif keys[pygame.K_w]:
                self.sfx[1].play()
                if self.player.myWeapons[self.selected]._type not in ['potion', 'shield', 'item']:
                    if self.player.myWeapons[self.selected] != self.player.equiped1:
                        self.player.equiped2.effect = False # reset the effect
                        self.player.equiped2 = self.player.myWeapons[self.selected]
                    else:
                        self.message = 'You can\'t use \nalready equiped\nweapon'
                else:
                    self.message = f'You can\'t use \n{self.player.myWeapons[self.selected]._type}\nas a weapon'
            elif keys[pygame.K_a]:
                self.sfx[1].play()
                if self.player.myWeapons[self.selected]._type not in ['shield', 'weapon', 'weapon-shield', 'item']:
                    self.player.potion.effect = False # reset the effect
                    self.player.potion = self.player.myWeapons[self.selected]
                else:
                    self.message = f'You can\'t use \n{self.player.myWeapons[self.selected]._type}\nas a potion'
            elif keys[pygame.K_s]:
                self.sfx[1].play()
                if self.player.myWeapons[self.selected]._type not in ['potion', 'weapon', 'item']:
                    self.player.shield.effect = False # reset the effect
                    self.player.shield = self.player.myWeapons[self.selected]
                else:
                    self.message = f'You can\'t use \n{self.player.myWeapons[self.selected]._type}\nas a shield'

        except IndexError:
            print('empty')
    
    def drawWeapons(self):
        eq1 = pygame.transform.scale(self.player.equiped1.icon, (45, 45))
        eq2 = pygame.transform.scale(self.player.equiped2.icon, (45, 45))
        eq_S = pygame.transform.scale(self.player.shield.icon, (45, 45))
        eq_P = pygame.transform.scale(self.player.potion.icon, (45, 45))
        self.screen.blit(eq1, self.equiped[0]) # left mouse
        self.screen.blit(eq2, self.equiped[1]) # right mouse
        self.screen.blit(eq_S, self.equiped[2]) # shield
        self.screen.blit(eq_P, self.equiped[3]) # potions

        for weapon in range(len(self.player.myWeapons)):
            wp = pygame.transform.scale(self.player.myWeapons[weapon].icon, (45, 45))
            self.screen.blit(wp, self.positions[weapon])