from View import View
from DocumentView import DocumentView

import FreeCAD
import FreeCADGui

class ApplicationView(View):
    def __init__(self):
        super(ApplicationView, self).__init__()
        
    def activeDocument(self):
        activeDoc = FreeCAD.ActiveDocument
        activeDocGui = FreeCADGui.ActiveDocument
        docView = DocumentView(activeDoc, activeDocGui)
        return docView