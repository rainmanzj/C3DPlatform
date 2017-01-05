from C3DPlatform.View.Feature import FeatureView

import FreeCAD
import Part

class BooleanFuseView(FeatureView):
    def __init__(self, name):
        super(BooleanFuseView, self).__init__()
        
        self.addProperty("FeatureType", PropertyType.String, "CDO", "BooleanFuseView")
        
        self.feature = FreeCAD.ActiveDocument.addObject("Part::MultiFuse", name)