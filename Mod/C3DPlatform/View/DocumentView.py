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
        for obj in self.doc.Objects:
            if hasattr(obj, "GUID"):
                if obj.GUID == guid:
                    featInFreeCAD = obj
                    break
        
        if featInFreeCAD is None:
            return None,None
        else:
            return FeatureView._from(featInFreeCAD)
                
    def getFeatureByName(self, name):
        feat = None
        for obj in self.doc.Objects:
            if obj.Name == name:
                feat = obj
                break
        
        if feat is None:
            return None,None
        else:
            return FeatureView._from(feat)
                
    @property
    def Features(self):
        lst = []
        for obj in self.doc.Objects:
            f,featType = FeatureView._from(obj)
            lst.append((f, featType))
        return lst
    
    def clear(self):
        if self.doc is not None:
            for o in self.doc.Objects:
                self.doc.removeObject(o.Name)
        
    def recompute(self):
        self.doc.recompute()
        
    def viewFit(self):
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