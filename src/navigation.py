import pygame

class Navigation:

    def __init__(self, player):
        self.player = player

        self.mapData = {}

        # check for the map address
        # get the map data (backup)
        # destroy current map
        # create the map
        # check if the map is already created before - if true apply all data else just create
        # navigate the player to the map

    def Navigate(self, address, _from, _to):
        _to.create()
        _from.destroy()