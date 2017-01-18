from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import BooleanCutView
from C3DPlatform.Geometry import Placement

class BooleanCut(Feature):
    def __init__(self, placement = Placement(), guid="Cut", view = None):
        super(BooleanCut, self).__init__()
        
        self.addProperty("FeatureType", PropertyType.String, "CDO", "BooleanCut")
        
        if view is None:
            self.view = BooleanCutView(self, guid)
            self.updatePropertiesToView()
            self.Placement = placement
        else:
            self.view = view
    
    def __setattr__(self, name, value):
        if name == "Base":
            self.view.Base = value
        elif name == "Tool":
            self.view.Tool = value
        else:
            super(BooleanCut, self).__setattr__(name, value)
            
    @property
    def Base(self):
        f = Feature._from(self.view.Base)
        return f
        
    @property
    def Tool(self):
        f = Feature._from(self.view.Tool)
        return f