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
        return Feature.Feature._from(view)
            
    def getFeatureByGUID(self, guid):
        return self.getFeatureByName(guid)
        '''
        view, type = self.view.getFeatureByGUID(guid)
        return Feature.Feature._from(view)
        '''
            
    @property
    def Features(self):
        feats = []
        lst = self.view.Features
        
        for item in lst:
            f = Feature.Feature._from(item[0])
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