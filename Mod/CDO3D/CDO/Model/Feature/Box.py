from CDO.Model.Feature import Feature
from CDO.View.Feature import BoxView

class Box(Feature):
    def __init__(self, length, width, height):
        self.L = length
        self.W = width
        self.H = height
        self.view = BoxView(self.L, self.W, self.H)