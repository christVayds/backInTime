from Data import read


class Reset:

    def __init__(self, object player, object map):
        self.player = player
        self.map = map

        self.mapObjects = read.Read('Data/data.json')
        self.mapObjects.read()
        self.mapObjects.strToTuple(self.map.name)

    def navigation(self):
        pass

    def reset(self):
        pass