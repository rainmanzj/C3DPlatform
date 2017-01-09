from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import ArchTriangularView
from C3DPlatform.Geometry import Placement

class ArchTriangular(Feature):
    def __init__(self, L = 100.0, W = 100.0, H = 100.0, placement = Placement(),
                 guid="ArchTriangular", view = None):
        super(ArchTriangular, self).__init__()
        
        self.addProperty("L", PropertyType.Length, "CDO", L)
        self.addProperty("W", PropertyType.Length, "CDO", W)
        self.addProperty("H", PropertyType.Length, "CDO", H)
        
        if view is None:
            self.view = ArchTriangularView(self, guid)
            self.updatePropertiesToView()
            self.Placement = placement
        else:
            self.view = view
        