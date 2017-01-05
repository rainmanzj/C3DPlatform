from C3DPlatform.View import DocumentView
import Feature

class Document(object):
    def __init__(self, docView):
        self.view = docView
    
    @property
    def Name(self):
        return self.view.Name
    
    def getFeatureByName(self, name):
        view, type = self.view.getFeatureByName(name)
        if view is not None and type is not None:
            if type == "":
                f = Feature.Feature()
                f.view = view
                return f
            else:
                f = eval("Feature.%s(view = view)" % type)
                return f
        else:
            return None
            
    def getFeatureByGUID(self, guid):
        return self.getFeatureByName(guid)
        '''
        view, type = self.view.getFeatureByGUID(guid)
        if view is not None and type is not None:
            return eval("Feature.%s(view = view)" % type)
        else:
            return None
        '''
            
    @property
    def Features(self):
        feats = []
        lst = self.view.Features
        for item in lst:
            view = item[0]
            type = item[1]
            if type == "":
                f = Feature.Feature()
                f.view = view
                feats.append(f)
            else:
                f = eval("Feature.%s(view = view)" % type)
                feats.append(f)
        return feats
            
    def clear(self):
        if self.view is not None:
            self.view.clear()
        
    def recompute(self):
        self.view.recompute()
        
    def viewFit(self):
        self.view.viewFit()
        
    def viewLeft(self):
        self.view.viewLeft()
        
    def viewRight(self):
        self.view.viewRight()
        
    def viewFront(self):
        self.view.viewFront()
        
    def viewBack(self):
        self.view.viewBack()
        
    def viewTop(self):
        self.view.viewTop()
        
    def viewBottom(self):
        self.view.viewBottom()