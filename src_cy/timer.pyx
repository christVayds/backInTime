class Timer:

    def __init__(self, int fps):
        self.fps = fps
        self.wait = self.fps
        self.second = 0
        self.minute = 0
        self.countDown = 0

    # return true
    def coolDown(self, int duration):
        if self.wait <= 0:
            self.countDown += 1
            self.wait = self.fps

        if self.countDown == duration:
            return True

        self.wait -= 1
    
    def Timer(self):
        if self.wait <= 0:
            self.wait = self.fps
            self.second += 1

        if self.second == 60:
            self.minute += 1
            self.second = 0
        self.wait += 1
        return str(self.minute), str(self.second)