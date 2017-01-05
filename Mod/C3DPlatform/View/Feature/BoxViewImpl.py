# coding=utf-8

import FreeCAD,Draft,ArchComponent,DraftVecUtils,ArchCommands,math
from FreeCAD import Vector
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
else:
    def translate(ctxt,txt):
        return txt

def makeBox(length, width, height, name="Box"):
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)
    _Box(obj)
    if FreeCAD.GuiUp:
        _ViewProviderBox(obj.ViewObject)
        
    obj.L = length
    obj.W = width
    obj.H = height
        
    return obj
    
class _Box(ArchComponent.Component):
    "The Box object"
    def __init__(self,obj):
        ArchComponent.Component.__init__(self,obj)
        self.Type = "Box"

        obj.addProperty("App::PropertyLength", "L", "Arch", translate("Arch", "L"))
        obj.addProperty("App::PropertyLength", "W", "Arch", translate("Arch", "W"))
        obj.addProperty("App::PropertyLength", "H", "Arch", translate("Arch", "H"))
        
    def execute(self,obj):
        "builds the box shape"
        if self.clone(obj):
            return

        import Part
        pl = obj.Placement
        L = obj.L.Value
        W = obj.W.Value
        H = obj.H.Value
        base = Part.makeBox(L, W, H)

        base = self.processSubShapes(obj,base,pl)
        self.applyShape(obj,base,pl)

    def onChanged(self,obj,prop):
        self.hideSubobjects(obj,prop)
        ArchComponent.Component.onChanged(self,obj,prop)

class _ViewProviderBox(ArchComponent.ViewProviderComponent):
    "A View Provider for the Arch Box"

    def __init__(self,vobj):
        ArchComponent.ViewProviderComponent.__init__(self,vobj)
        vobj.ShapeColor = ArchCommands.getDefaultColor("Wall")

    def getIcon(self):
        import Arch_rc
        if hasattr(self,"Object"):
            for o in self.Object.OutList:
                if Draft.getType(o) == "Wall":
                    return ":/icons/Arch_Wall_Tree_Assembly.svg"
        return ":/icons/Arch_Wall_Tree.svg"

    def attach(self,vobj):
        self.Object = vobj.Object
        return