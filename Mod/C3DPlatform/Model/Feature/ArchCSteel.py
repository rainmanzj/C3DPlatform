from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import ArchCSteelView

class ArchCSteel(Feature):
    def __init__(self, L = 100.0):
        super(ArchCSteel, self).__init__()
    
        self.addProperty("L", PropertyType.Length, "CDO", L)
        self.view = ArchCSteelView(self.L)