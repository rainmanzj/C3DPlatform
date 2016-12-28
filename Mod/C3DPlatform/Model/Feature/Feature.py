from C3DPlatform.Model import DocumentObject
from C3DPlatform.Base import Placement

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
        self.placement = Placement()
    
    def addProperty(self, name, type, group = "", value = None):
        PropertyContainer.addProperty(self, name, type, group, value)
        if self.view is not None:
            self.view.addProperty(name, type, group, value)
        
    def __getattr__(self, name):
        if self.hasProperty(name):
            prop = self.getProperty(name)
            return prop.value
        
    def __setattr__(self, name, value):
        if name in ['placement', 'type', 'view', '_PropertiesMap']:
            self.__dict__[name] = value
            if name == 'placement' and self.view is not None:
                self.view.Placement = value
        elif self.hasProperty(name):
            prop = self.getProperty(name)
            prop.value = value
            if self.view is not None:
                self.view.setProperty(name, value)
        else:
            pass
        
    def show(self):
        self.view.show()
        
    def hide(self):
        self.view.hide()
        
    def update(self):
        self.view.update()
        
    def delete(self):
        self.view.delete()