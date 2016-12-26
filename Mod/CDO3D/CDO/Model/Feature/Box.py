from CDO.Model.Feature import Feature
from CDO.View.Feature import BoxView

class Box(Feature):
    def __init__(self, length = 1.0, width = 1.0, height = 1.0):
        super(Box, self).__init__()
        self.L = length
        self.W = width
        self.H = height
        self.view = BoxView(self.L, self.W, self.H)