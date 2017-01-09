from C3DPlatform.Model import Document
from C3DPlatform.View import DocumentView

import FreeCADGui

class Selection(object):
    def __init__(self, feat):
        self.feature = feat
        
    @staticmethod
    def getSelection():
        ss = []
        sels = FreeCADGui.Selection.getSelection()
        for sel in sels:
            from C3DPlatform.View.Feature import FeatureView
            view,type = FeatureView._from(sel)
            from C3DPlatform.Model.Feature import Feature
            f = Feature._from(view)
            ss.append(f)
        return ss
        
    @staticmethod
    def addSelection(feat):
        FreeCADGui.Selection.addSelection(feat.view.feature)