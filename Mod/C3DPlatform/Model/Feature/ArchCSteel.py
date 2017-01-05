from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import ArchCSteelView
from C3DPlatform.Geometry import Placement

class ArchCSteel(Feature):
    def __init__(self, L = 100.0, placement = Placement(), name="ArchCSteel", view = None):
        super(ArchCSteel, self).__init__()
    
        self.addProperty("FeatureType", PropertyType.String, "CDO", "ArchCSteel")
        self.addProperty("L", PropertyType.Length, "CDO", L)
        
        if view is None:
            self.view = ArchCSteelView(self, name)
            self.updatePropertiesToView()
            self.Placement = placement
        else:
            self.view = view