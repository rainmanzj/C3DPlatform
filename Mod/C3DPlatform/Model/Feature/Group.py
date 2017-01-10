from C3DPlatform.Model.Feature import Feature, PropertyType
from C3DPlatform.View.Feature import GroupView

class Group(Feature):
    def __init__(self, guid="Group", view = None):
        super(Group, self).__init__()
        
        self.addProperty("FeatureType", PropertyType.String, "CDO", "Group")
        
        if view is None:
            self.view = GroupView(self, guid)
            self.updatePropertiesToView()
        else:
            self.view = view
            
    def addChild(self, item):
        self.view.addChild(item)
        
    def removeChild(self, item):
        self.view.removeChild(item)
        
    def clear(self):
        self.view.clear()
        
    def hasChild(self, item):
        return self.view.hasChild(item)
        
    def __children(self):
        lst = []
        for o in self.view.Children:
            lst.append(Feature._from(o))
        return lst
        
    def __getattr__(self, name):
        if name == "Children":
            return self.__children()
        else:
            super(Group, self).__getattr__(name)
   