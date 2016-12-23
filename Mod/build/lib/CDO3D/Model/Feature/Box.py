from Feature import Feature

class Box(Feature):
    def __init__(self, length, width, height):
        self.L = length
        self.W = width
        self.H = height