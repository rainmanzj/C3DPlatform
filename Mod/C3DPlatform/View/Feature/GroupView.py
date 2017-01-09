import FeatureView
import GroupViewImpl

class GroupView(FeatureView.FeatureView):
    def __init__(self, feat, name="", create=True):
        super(GroupView, self).__init__()
        
        if create:
            self.feature = GroupViewImpl.makeGroup(name = name)
        else:
            self.feature = feat
                
    def addChild(self, item):
        self.feature.addObject(item.view.feature)
        
    def removeChild(self, item):
        self.feature.removeObject(item.view.feature)
        
    def hasChild(self, item):
        for o in self.feature.Group:
            if o.Name == item.Guid:
                return True
        
        return False
        
    @property
    def Children(self):
        lst = []
        for o in self.feature.Group:
            lst.append(FeatureView.FeatureView._from(o)[0])
        return lst
