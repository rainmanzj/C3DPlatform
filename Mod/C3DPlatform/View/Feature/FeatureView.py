from C3DPlatform.View import View
from C3DPlatform.Base import Placement

import FreeCAD
import FreeCADGui

class FeatureView(View):
    def __init__(self):
        super(FeatureView, self).__init__()
        
        self.feature = None
     
    @property
    def Placement(self):
        return self.feature.Placement
        
    @Placement.setter
    def Placement(self, pl):
        self.feature.Placement.Base = \
            FreeCAD.Vector(pl.position.x, pl.position.y, pl.position.z)
        self.feature.Placement.Rotation = \
            FreeCAD.Rotation(pl.rotation.x, pl.rotation.y, pl.rotation.z, pl.rotation.w)
        
    def show(self):
        self.feature.ViewObject.show()
        
    def hide(self):
        self.feature.ViewObject.hide()
        
    def update(self):
        self.feature.ViewObject.update()
        
    def delete(self):
        self.feature.Document.removeObject(self.feature.Name)
        
    def addProperty(self, name, type, group = "", value = None):
        type = "App::Property" + type
        self.feature.addProperty(type, name, group, name)
        if value is not None:
            setattr(self.feature, name, value)
            
    def setProperty(self, name, value):
        setattr(self.feature, name, value)
        
    def updateProperty(self, name, type, group, value):
        if hasattr(self.feature, name):
            self.setProperty(name, value)
        else:
            self.addProperty(name, type, group, value)
    
    