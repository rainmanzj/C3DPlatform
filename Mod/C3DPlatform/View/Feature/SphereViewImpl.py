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

def makeSphere(radius, name="Sphere"):
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)
    _Sphere(obj)
    if FreeCAD.GuiUp:
        _ViewProviderSphere(obj.ViewObject)
        
    obj.Radius = radius
        
    return obj
    
class _Sphere(ArchComponent.Component):
    "The Sphere object"
    def __init__(self, obj):
        ArchComponent.Component.__init__(self, obj)
        self.Type = "Sphere"

        obj.addProperty("App::PropertyLength", "Radius", "Arch", translate("Arch", "Radius"))
        
    def execute(self, obj):
        "builds the sphere shape"
        if self.clone(obj):
            return

        import Part
        pl = obj.Placement
        radius = obj.Radius.Value
        base = Part.makeSphere(radius)

        base = self.processSubShapes(obj,base,pl)
        self.applyShape(obj,base,pl)

    def onChanged(self,obj,prop):
        self.hideSubobjects(obj,prop)
        ArchComponent.Component.onChanged(self,obj,prop)

class _ViewProviderSphere(ArchComponent.ViewProviderComponent):
    "A View Provider for the Arch Sphere"

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