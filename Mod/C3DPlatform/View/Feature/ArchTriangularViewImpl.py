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
        
def make(length, width, height, name="TriangularPrism"):
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)
    _ArchTriangularPrism(obj)
    if FreeCAD.GuiUp:
        _ViewProviderTriangularPrism(obj.ViewObject)
        
    obj.L = length
    obj.W = width
    obj.H = height
        
    return obj
        
class _ArchTriangularPrism(ArchComponent.Component):
    """三棱柱"""
    
    def __init__(self,obj):
        ArchComponent.Component.__init__(self, obj)
        self.Type = "TriangularPrism"

        obj.addProperty("App::PropertyLength", "L", "Arch", translate("Arch", "L"))
        obj.addProperty("App::PropertyLength", "W", "Arch", translate("Arch", "W"))
        obj.addProperty("App::PropertyLength", "H", "Arch", translate("Arch", "H"))
        
    def execute(self,obj):
        "builds the triangular prism shape"
        if self.clone(obj):
            return

        pl = obj.Placement
        base = None
        L = obj.L.Value
        W = obj.W.Value
        H = obj.H.Value
        
        import Part
        pntA = FreeCAD.Vector(0, 0, 0)
        pntB = FreeCAD.Vector(L, 0, 0)
        pntC = FreeCAD.Vector(L / 2, W, 0)
        lineAB = Part.makeLine(pntA, pntB)
        lineBC = Part.makeLine(pntB, pntC)
        lineCA = Part.makeLine(pntC, pntA)
        wire = Part.Wire([lineAB, lineBC, lineCA])
        face = Part.Face([wire])
        base = face.extrude(FreeCAD.Vector(0, 0, 1) * L)
        
        base = self.processSubShapes(obj, base, pl)
        self.applyShape(obj, base, pl)

    def onChanged(self,obj,prop):
        self.hideSubobjects(obj,prop)
        ArchComponent.Component.onChanged(self,obj,prop)
        
class _ViewProviderTriangularPrism(ArchComponent.ViewProviderComponent):
    "A View Provider for the Arch Triangular Prism"

    def __init__(self,vobj):
        ArchComponent.ViewProviderComponent.__init__(self, vobj)
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