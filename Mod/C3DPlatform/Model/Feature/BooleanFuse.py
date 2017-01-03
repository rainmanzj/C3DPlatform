from C3DPlatform.Model.Feature import Feature
from C3DPlatform.View.Feature import BooleanFuseView

class BooleanFuse(Feature):
    def __init__(self):
        super(BooleanFuse, self).__init__()
    
        self.Items = []
        self.view = BooleanFuseView("Fuse")
        
    def __setattr__(self, name, value):
        if name == "Items" and isinstance(value, list):
            self.__dict__[name] = value
        else:
            super(BooleanFuse, self).__setattr__(name, value)