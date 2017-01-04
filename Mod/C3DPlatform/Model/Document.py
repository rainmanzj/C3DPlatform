from C3DPlatform.View import DocumentView
import Feature

class Document(object):
    def __init__(self, docView):
        self.view = docView
    
    @property
    def Name(self):
        return self.view.Name
        
    def getFeatureByGUID(self, guid):
        view, type = self.view.getFeatureByGUID(guid)
        if view is not None and type is not None:
            return eval("Feature.%s(view = view)" % type)
        else:
            return None
        
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