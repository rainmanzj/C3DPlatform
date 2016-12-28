from C3DPlatform.View import DocumentView

class Document(object):
    def __init__(self, docView):
        self.view = docView
    
    @property
    def Name(self):
        return self.view.Name
        
    def recompute(self):
        self.view.recompute()
        
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