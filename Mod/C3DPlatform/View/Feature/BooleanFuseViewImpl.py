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

def makeFuse(items, name="Fusion"):
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)
    _Fuse(obj)
    if FreeCAD.GuiUp:
        _ViewProviderFuse(obj.ViewObject)
    if items:
        obj.Items = items
        
    return obj
    
class _Fuse(ArchComponent.Component):
    "The Fuse object"
    def __init__(self, obj):
        ArchComponent.Component.__init__(self, obj)
        obj.addProperty("App::PropertyLinkList","Items","Arch","Items")
        self.Type = "Fuse"
        self.Object = obj
        
    def execute(self, obj):
        "builds the fuse shape"
        if self.clone(obj):
            return
            
        if len(obj.Items) < 1:
            import Part
            obj.Shape = Part.Shape()
            return
        
        base = obj.Items[0].Shape
        for i in range(1, len(obj.Items)):
            base = base.fuse(obj.Items[i].Shape)
        pl = obj.Placement
        base = self.processSubShapes(obj,base,pl)
        self.applyShape(obj,base,pl)

    def onChanged(self,obj,prop):
        self.hideSubobjects(obj,prop)
        ArchComponent.Component.onChanged(self,obj,prop)

class _ViewProviderFuse(ArchComponent.ViewProviderComponent):
    "A View Provider for the Fuse"

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