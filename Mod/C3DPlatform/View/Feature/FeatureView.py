from C3DPlatform.View import View
from C3DPlatform.Geometry import Placement,Vector,Quaternion

import FreeCAD
import FreeCADGui

class FeatureView(View):
    def __init__(self):
        super(FeatureView, self).__init__()
        
        self.feature = None
        
    @staticmethod
    def _from(feat):
        f = None
        featType = getattr(feat, "FeatureType", "")
        
        if featType == "":
            f = FeatureView()
            f.feature = feat
        else:
            viewType = "%sView" % featType
            exec("from %s import %s" % (viewType, viewType))
            expression = "%s(feat = %s, create = False)" \
                % (viewType, "feat")
            f = eval(expression)
        
        return f,featType
        
    @property
    def FeatureType(self):
        return getattr(self.feature, "FeatureType", "")
    
    @property
    def Placement(self):
        if self.feature is not None:
            pl = Placement()
            pl.position = Vector(self.feature.Placement.Base.x,
                                 self.feature.Placement.Base.y,
                                 self.feature.Placement.Base.z)
            rot = self.feature.Placement.Rotation
            pl.rotation = Quaternion(rot.Q[0], rot.Q[1], rot.Q[2], rot.Q[3])
            return pl
        else:
            return None
        
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
    
    @property
    def guid(self):
        if self.feature is not None:
            if hasattr(self.feature, "GUID"):
                return self.feature.GUID
            else:
                return None
        else:
            return None
            
    @property
    def Name(self):
        return self.feature.Name
        
    @property
    def Label(self):
        return self.feature.Label
        
    @Label.setter
    def Label(self, value):
        self.feature.Label = value
        
    @property
    def Group(self):
        for o in self.feature.InList:
            if str(o) == '<group object>':
                import GroupView
                return eval("GroupView.GroupView(o, create=False)")
                
        return None