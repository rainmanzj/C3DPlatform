from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import SphereView
from C3DPlatform.Geometry import Placement

class Sphere(Feature):
    def __init__(self, radius = 1.0,
                 placement = Placement(), guid="Sphere", view = None):
        super(Sphere, self).__init__()
        
        self.addProperty("FeatureType", PropertyType.String, "CDO", "Sphere")
        self.addProperty("Radius", PropertyType.Length, "CDO", radius)
        
        if view is None:
            self.view = SphereView(self, guid)
            self.updatePropertiesToView()
            self.Placement = placement
        else:
            self.view = view