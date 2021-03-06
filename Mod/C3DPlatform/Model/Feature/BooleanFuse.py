from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import BooleanFuseView
from C3DPlatform.Geometry import Placement

class BooleanFuse(Feature):
    def __init__(self, placement = Placement(), guid="Fusion", view = None):
        super(BooleanFuse, self).__init__()
        
        self.addProperty("FeatureType", PropertyType.String, "CDO", "BooleanFuse")
        
        if view is None:
            self.view = BooleanFuseView(self, guid)
            self.updatePropertiesToView()
            self.Placement = placement
        else:
            self.view = view
        
    def __setattr__(self, name, value):
        if name == "Items" and isinstance(value, list):
            self.view.Items = value
        else:
            super(BooleanFuse, self).__setattr__(name, value)
            
    @property
    def Items(self):
        items = []
        for o in self.view.Items:
            f = Feature._from(o)
            items.append(f)
        return items