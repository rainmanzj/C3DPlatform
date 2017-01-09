import FreeCAD,Draft,ArchComponent,DraftVecUtils,ArchCommands,math
from FreeCAD import Vector
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
else:
    def translate(ctxt,txt):
        return txt
    
def makeGroup(objectslist=None, name="Group"):
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", name)
    obj.Label = name
    _Group(obj)
    if FreeCAD.GuiUp:
        _ViewProviderGroup(obj.ViewObject)
    if objectslist:
        obj.Group = objectslist
    return obj

class _Group:
    "The Floor object"
    def __init__(self,obj):
        obj.addProperty("App::PropertyPlacement","Placement","Arch",translate("Arch","The placement of this group"))
        self.Type = "Group"
        obj.Proxy = self
        self.Object = obj

    def __getstate__(self):
        return self.Type

    def __setstate__(self,state):
        if state:
            self.Type = state

    def execute(self,obj):
        # move children with this floor
        if hasattr(obj,"Placement"):
            if not hasattr(self,"OldPlacement"):
                self.OldPlacement = obj.Placement.copy()
            else:
                pl = obj.Placement.copy()
                if not DraftVecUtils.equals(pl.Base,self.OldPlacement.Base):
                    print "placement moved"
                    delta = pl.Base.sub(self.OldPlacement.Base)
                    for o in obj.Group:
                        if hasattr(o,"Placement"):
                            o.Placement.move(delta)
                    self.OldPlacement = pl

    def addObject(self,child):
        if hasattr(self,"Object"):
            g = self.Object.Group
            if not child in g:
                g.append(child)
                self.Object.Group = g

    def removeObject(self,child):
        if hasattr(self,"Object"):
            g = self.Object.Group
            if child in g:
                g.remove(child)
                self.Object.Group = g

class _ViewProviderGroup:
    "A View Provider for the Floor object"
    def __init__(self,vobj):
        vobj.Proxy = self

    def getIcon(self):
        import Arch_rc
        return ":/icons/Arch_Floor_Tree.svg"

    def attach(self,vobj):
        self.Object = vobj.Object
        return

    def claimChildren(self):
        return self.Object.Group

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None
