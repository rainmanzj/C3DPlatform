from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import BoxView

class Box(Feature):
    def __init__(self, length = 1.0, width = 1.0, height = 1.0):
        super(Box, self).__init__()
        
        self.addProperty("L", PropertyType.Length, "CDO", length)
        self.addProperty("W", PropertyType.Length, "CDO", width)
        self.addProperty("H", PropertyType.Length, "CDO", height)
        self.view = BoxView(self.L, self.W, self.H)