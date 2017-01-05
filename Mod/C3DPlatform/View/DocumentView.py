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
                
    def getFeatureByName(self, name):
        item = None
        featType = None
        
        for obj in self.doc.Objects:
            if obj.Name == name:
                item = obj
                featType = getattr(obj, "FeatureType", "")
                break
                
        if item is None:
            return None,None
        else:
            if featType == "":
                f = FeatureView()
                f.feature = item
                return (f, featType)
            else:
                f = eval("%s%s(feat = %s, create = False)" \
                    % (featType, "View", "item"))
                return (f, featType)
                
    @property
    def Features(self):
        lst = []
        for obj in self.doc.Objects:
            featType = getattr(obj, "FeatureType", "")
            if featType == "":
                f = FeatureView()
                f.feature = obj
                lst.append((f, featType))
            else:
                f = eval("%s%s(feat = %s, create = False)" \
                    % (featType, "View", "obj"))
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