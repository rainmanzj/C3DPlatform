from View import View
from Feature import *

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
        
    def getFeatureByGUID(self, guid):
        featInFreeCAD = None
        featType = None
        
        for obj in self.doc.Objects:
            if hasattr(obj, "GUID"):
                if obj.GUID == guid:
                    featInFreeCAD = obj
                    break
        
        if featInFreeCAD is None:
            return None,None
        else:
            if hasattr(featInFreeCAD, "FeatureType"):
                featType = featInFreeCAD.FeatureType
                return eval("%s%s(feat = %s, create = False)" \
                    % (featType, "View", "featInFreeCAD")), featType
            else:
                return None,None
        
        
    def recompute(self):
        self.doc.recompute()
        
    def viewFit(self):
        #self.docGui.ActiveView.
        pass
        
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