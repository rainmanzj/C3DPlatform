from C3DPlatform.Model import Document
from C3DPlatform.View import DocumentView

import FreeCADGui

class Selection(object):
    def __init__(self, feat):
        self.feature = feat
        
    @staticmethod
    def getSelection():
        sels = FreeCADGui.Selection.getSelection()
        for sel in sels:
            pass