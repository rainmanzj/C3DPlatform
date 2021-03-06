from C3DPlatform.Model import DocumentObject
from C3DPlatform.Geometry import Placement

class Property:
    def __init__(self, name, type, group = "", value = None):
        self.name = name
        self.type = type
        self.group = group
        self.value = value
        
class PropertyType:
    Integer = "Integer"
    Float   = "Float"
    Length  = "Length"
    String  = "String"
    Vector  = "Vector"
    Placement = "Placement"

class PropertyContainer(object):
    def __init__(self):
        self._PropertiesMap = {}
    
    def addProperty(self, name, type, group = "", value = None):
        prop = Property(name, type, group, value)
        self._PropertiesMap[name] = prop
        
    def hasProperty(self, name):
        return name in self._PropertiesMap
        
    def getProperty(self, name):
        return self._PropertiesMap.get(name, None)

class Feature(DocumentObject, PropertyContainer):
    def __init__(self):
        DocumentObject.__init__(self)
        PropertyContainer.__init__(self)
        
        self.type = "Feature"
        self.view = None
        
    @staticmethod
    def _from(view):
        try:
            type = view.FeatureType
        except:
            return None
        if type is None:
            return None
        f = None
        if type == "":
            f = Feature()
            f.view = view
        else:
            exec("from %s import %s" % (type, type))
            f = eval("%s(view = view)" % type)
        return f
    
    def addProperty(self, name, type, group = "", value = None):
        PropertyContainer.addProperty(self, name, type, group, value)
        if self.view is not None:
            self.view.addProperty(name, type, group, value)
        
    def __getattr__(self, name):
        if self.hasProperty(name):
            prop = self.getProperty(name)
            return prop.value
        
    def __setattr__(self, name, value):
        if name == 'Placement' and self.view is not None:
            self.view.Placement = value
        elif name in ['type', 'view', '_PropertiesMap']:
            self.__dict__[name] = value
        elif name == "Label":
            self.view.Label = value
        elif name == "Texture":
            self.setTexture(value)
        elif self.hasProperty(name):
            prop = self.getProperty(name)
            prop.value = value
            if self.view is not None:
                self.view.setProperty(name, value)
        else:
            pass
            
    def updatePropertiesToView(self):
        for propName in self._PropertiesMap:
            prop = self._PropertiesMap[propName]
            self.view.updateProperty(prop.name, prop.type, prop.group, prop.value)
        
    def show(self):
        self.view.show()
        
    def hide(self):
        self.view.hide()
        
    def update(self):
        self.view.update()
        
    def delete(self):
        self.view.delete()
        
    @property
    def Guid(self):
        '''
        return self.view.guid
        '''
        return self.view.Name
        
    @property
    def Placement(self):
        return self.view.Placement
    
    '''
    @property
    def Name(self):
        return self.view.Name
    '''
        
    @property
    def Label(self):
        return self.view.Label
        
    @property
    def Texture(self):
        return None
        
    def setTexture(self, value):
        self.view.Texture = value
        
    def clearTexture(self):
        self.view.Texture = ""
        
    @property
    def Group(self):
        gp = self.view.Group
        if gp is not None:
            import Group
            return eval("Group.Group(view = gp)")
        else:
            return None