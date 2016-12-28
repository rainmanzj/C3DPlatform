from View import View

import FreeCAD
import Arch

class DocumentView(View):
    def __init__(self, doc, docGui):
        super(DocumentView, self).__init__()
        self.doc = doc
        self.docGui = docGui
        
    @property
    def Name(self):
        return self.doc.Name
        
    def recompute(self):
        self.doc.recompute()
        
    def viewLeft(self):
        self.docGui.ActiveView.viewLeft()
        
    def viewRight(self):
        self.docGui.ActiveView.viewRight()
        
    def viewFront(self):
        self.docGui.ActiveView.viewFront()
        
    def viewBack(self):
        self.docGui.ActiveView.viewRear()
        
    def viewTop(self):
        self.docGui.ActiveView.viewTop()
        
    def viewBottom(self):
        self.docGui.ActiveView.viewBottom()