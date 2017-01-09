from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import BoxView
from C3DPlatform.Geometry import Placement

class Box(Feature):
    def __init__(self, length = 1.0, width = 1.0, height = 1.0,
                 placement = Placement(), guid="Box", view = None):
        super(Box, self).__init__()
        
        self.addProperty("FeatureType", PropertyType.String, "CDO", "Box")
        self.addProperty("L", PropertyType.Length, "CDO", length)
        self.addProperty("W", PropertyType.Length, "CDO", width)
        self.addProperty("H", PropertyType.Length, "CDO", height)
        
        if view is None:
            self.view = BoxView(self, guid)
            self.updatePropertiesToView()
            self.Placement = placement
        else:
            self.view = view