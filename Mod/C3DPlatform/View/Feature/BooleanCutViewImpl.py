import FreeCAD,Draft,ArchComponent,DraftVecUtils,ArchCommands,math
from FreeCAD import Vector
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
else:
    def translate(ctxt,txt):
        return txt
        
def makeCut(base=None, tool=None, name="Cut"):
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)
    _Cut(obj)
    if FreeCAD.GuiUp:
        _ViewProviderCut(obj.ViewObject)
    if base != None:
        obj.Base = base
    if tool != None:
        obj.Tool = tool
        
    return obj
        
class _Cut(ArchComponent.Component):
    "The Cut object"
    def __init__(self, obj):
        ArchComponent.Component.__init__(self, obj)
        obj.addProperty("App::PropertyLink", "Base", "Arch", "Base")
        obj.addProperty("App::PropertyLink", "Tool", "Arch", "Tool")
        self.Type = "Cut"
        self.Object = obj
        
    def execute(self, obj):
        "builds the cut shape"
        if self.clone(obj):
            return
            
        if obj.Base == None:
            import Part
            obj.Shape = Part.Shape()
            return
        
        base = obj.Base.Shape
        if obj.Tool != None:
            base = base.cut(obj.Tool.Shape)
        pl = obj.Placement
        base = self.processSubShapes(obj,base,pl)
        self.applyShape(obj,base,pl)

    def onChanged(self,obj,prop):
        self.hideSubobjects(obj,prop)
        ArchComponent.Component.onChanged(self,obj,prop)

class _ViewProviderCut(ArchComponent.ViewProviderComponent):
    "A View Provider for the Cut"

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