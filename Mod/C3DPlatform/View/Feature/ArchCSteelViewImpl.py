#coding=gbk

import FreeCAD,Draft,ArchComponent,DraftVecUtils,ArchCommands,math
from FreeCAD import Vector
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
else:
    def translate(ctxt,txt):
        return txt

def makeSteel(baseobj=None,side=20,length=None,width=None,height=None,align="Center",face=None,name="CSteel"):
    '''makeWall([obj],[length],[width],[height],[align],[face],[name]): creates a wall based on the
    given object, which can be a sketch, a draft object, a face or a solid, or no object at
    all, then you must provide length, width and height. Align can be "Center","Left" or "Right",
    face can be an index number of a face in the base object to base the wall on.'''
    p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Arch")
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
    #obj = FreeCAD.ActiveDocument.addObject("Part::Feature",name)
    obj.Label = translate("Arch",name)
    _CSteel(obj)
    if FreeCAD.GuiUp:
        _ViewProviderWall(obj.ViewObject)
    if baseobj:
        if baseobj.isDerivedFrom("Part::Feature") or baseobj.isDerivedFrom("Mesh::Feature"):
            obj.Base = baseobj
        else:
            FreeCAD.Console.PrintWarning(str(translate("Arch","Walls can only be based on Part or Mesh objects")))
    if face:
        obj.Face = face
    if length:
        obj.Length = length
    if width:
        obj.Width = width
    else:
        obj.Width = p.GetFloat("WallWidth",200)
    if height:
        obj.Height = height
    else:
        obj.Height = p.GetFloat("WallHeight",3000)
    if side:
        obj.Side = side


    obj.H = 100
    obj.B = 50
    obj.C = 20
    obj.T = 2

    obj.Align = align
    if obj.Base and FreeCAD.GuiUp:
        if Draft.getType(obj.Base) != "Space":
            obj.Base.ViewObject.hide()
    return obj

class CSteelCut(ArchComponent.Component):
    def __init__(self, obj, base, tool):
        ArchComponent.Component.__init__(self,obj)
        obj.addProperty("App::PropertyLink", "Base", "Arch", "Base")
        obj.addProperty("App::PropertyLink", "Tool", "Arch", "Tool")
        obj.addProperty("App::PropertyString", "GUID", "Arch", "GUID")
        import random
        obj.GUID = str(random.randint(1, 10000000))
        obj.Base = base
        obj.Tool = tool

        self.Type = "CSteelCut"

    def execute(self, obj):
        if self.clone(obj):
            return

        import Part
        pl = obj.Placement
        base = obj.Base.Shape.cut(obj.Tool.Shape)

        base = self.processSubShapes(obj,base,pl)
        self.applyShape(obj,base,pl)

    def onChanged(self,obj,prop):
        self.hideSubobjects(obj,prop)
        ArchComponent.Component.onChanged(self,obj,prop)


class _CSteel(ArchComponent.Component):
    "The Triangle Prism object"
    def __init__(self,obj):
        ArchComponent.Component.__init__(self,obj)
        obj.addProperty("App::PropertyLength","Length","Arch",translate("Arch","The length of this wall. Not used if this wall is based on an underlying object"))
        obj.addProperty("App::PropertyLength","Width","Arch",translate("Arch","The width of this wall. Not used if this wall is based on a face"))
        obj.addProperty("App::PropertyLength","Height","Arch",translate("Arch","The height of this wall. Keep 0 for automatic. Not used if this wall is based on a solid"))
        obj.addProperty("App::PropertyLength","Side","Arch",translate("Arch","The side of triangle"))
        obj.addProperty("App::PropertyEnumeration","Align","Arch",translate("Arch","The alignment of this wall on its base object, if applicable"))
        obj.addProperty("App::PropertyVector","Normal","Arch",translate("Arch","The normal extrusion direction of this object (keep (0,0,0) for automatic normal)"))
        obj.addProperty("App::PropertyInteger","Face","Arch",translate("Arch","The face number of the base object used to build this wall"))
        obj.addProperty("App::PropertyDistance","Offset","Arch",translate("Arch","The offset between this wall and its baseline (only for left and right alignments)"))
        obj.Align = ['Left','Right','Center']
        self.Type = "CSteel"

        obj.addProperty("App::PropertyLength","H","Arch",translate("Arch","H"))
        obj.addProperty("App::PropertyLength","B","Arch",translate("Arch","B"))
        obj.addProperty("App::PropertyLength","C","Arch",translate("Arch","C"))
        obj.addProperty("App::PropertyLength","T","Arch",translate("Arch","T"))
        obj.addProperty("App::PropertyLength","L","Arch",translate("Arch","L"))
        obj.addProperty("App::PropertyString", "GUID", "Arch", "GUID")
        import random
        obj.GUID = str(random.randint(1, 10000000))

    def execute(self,obj):
        "builds the triangle prism shape"
        if self.clone(obj):
            return

        import Part, DraftGeomUtils
        pl = obj.Placement
        normal,length,width,height = self.getDefaultValues(obj)
        base = None
        face = None

        H = obj.H.Value
        B = obj.B.Value
        C = obj.C.Value
        T = obj.T.Value
        L = obj.L.Value

        if obj.Base:
            # computing a shape from a base object
            if obj.Base.isDerivedFrom("Part::Feature"):
                if obj.Base.Shape.isNull():
                    return
                if not obj.Base.Shape.isValid():
                    if not obj.Base.Shape.Solids:
                        # let pass invalid objects if they have solids...
                        return
                
                if hasattr(obj,"Face"):
                    if obj.Face > 0:
                        if len(obj.Base.Shape.Faces) >= obj.Face:
                            face = obj.Base.Shape.Faces[obj.Face-1]
                if face:
                    # case 1: this wall is based on a specific face of its base object
                    normal = face.normalAt(0,0)
                    if normal.getAngle(Vector(0,0,1)) > math.pi/4:
                        normal.multiply(width)
                        base = face.extrude(normal)
                        if obj.Align == "Center":
                            base.translate(normal.negative().multiply(0.5))
                        elif obj.Align == "Right":
                            base.translate(normal.negative())
                    else:
                        normal.multiply(height)
                        base = face.extrude(normal)
                elif obj.Base.Shape.Solids:
                    # case 2: the base is already a solid
                    base = obj.Base.Shape.copy()
                elif obj.Base.Shape.Edges:
                    dir = DraftGeomUtils.vec(obj.Base.Shape.Edges[0])
                    dvec = dir.cross(normal).normalize()
                    cenPnt = obj.Base.Shape.Edges[0].Vertexes[0].Point
        
                    pntA0 = cenPnt - dvec * H * 0.5
                    pntB0 = pntA0 - normal* B
                    pntC0 = pntB0 + dvec * C
                    pntD0 = pntC0 + normal * T
                    pntE0 = pntD0 - dvec * (C - T)
                    pntF0 = pntE0 + normal * (B - 2 * T)

                    pntA1 = cenPnt + dvec * H * 0.5
                    pntB1 = pntA1 - normal * B
                    pntC1 = pntB1 - dvec * C
                    pntD1 = pntC1 + normal * T
                    pntE1 = pntD1 + dvec * (C - T)
                    pntF1 = pntE1 + normal * (B - 2 * T)

                    lineA0A1 = Part.makeLine(pntA0, pntA1)
                    lineA1B1 = Part.makeLine(pntA1, pntB1)
                    lineB1C1 = Part.makeLine(pntB1, pntC1)
                    lineC1D1 = Part.makeLine(pntC1, pntD1)
                    lineD1E1 = Part.makeLine(pntD1, pntE1)
                    lineE1F1 = Part.makeLine(pntE1, pntF1)
                    lineF1F0 = Part.makeLine(pntF1, pntF0)
                    lineF0E0 = Part.makeLine(pntF0, pntE0)
                    lineE0D0 = Part.makeLine(pntE0, pntD0)
                    lineD0C0 = Part.makeLine(pntD0, pntC0)
                    lineC0B0 = Part.makeLine(pntC0, pntB0)
                    lineB0A0 = Part.makeLine(pntB0, pntA0)

                    wire = Part.Wire([lineA0A1, lineA1B1, lineB1C1, lineC1D1, lineD1E1, lineE1F1, lineF1F0, 
                         lineF0E0, lineE0D0, lineD0C0, lineC0B0, lineB0A0])
                    f = Part.Face([wire])
                    base = f.extrude(dir)
                    
                else:
                    base = None
                    FreeCAD.Console.PrintError(str(translate("Arch","Error: Invalid base object")))
        else:
            import Part
            zdir = FreeCAD.Base.Vector(0, 0, 1)
            xdir = FreeCAD.Base.Vector(1, 0, 0)
            ydir = FreeCAD.Base.Vector(0, 1, 0)
            basePnt = FreeCAD.Base.Vector(0, B/2, 0)

            pntA0 = basePnt - xdir * H * 0.5
            pntB0 = pntA0 - ydir * B
            pntC0 = pntB0 + xdir * C
            pntD0 = pntC0 + ydir * T
            pntE0 = pntD0 - xdir * (C - T)
            pntF0 = pntE0 + ydir * (B - 2 * T)

            pntA1 = basePnt + xdir * H * 0.5
            pntB1 = pntA1 - ydir * B
            pntC1 = pntB1 - xdir * C
            pntD1 = pntC1 + ydir * T
            pntE1 = pntD1 + xdir * (C - T)
            pntF1 = pntE1 + ydir * (B - 2 * T)

            lineA0A1 = Part.makeLine(pntA0, pntA1)
            lineA1B1 = Part.makeLine(pntA1, pntB1)
            lineB1C1 = Part.makeLine(pntB1, pntC1)
            lineC1D1 = Part.makeLine(pntC1, pntD1)
            lineD1E1 = Part.makeLine(pntD1, pntE1)
            lineE1F1 = Part.makeLine(pntE1, pntF1)
            lineF1F0 = Part.makeLine(pntF1, pntF0)
            lineF0E0 = Part.makeLine(pntF0, pntE0)
            lineE0D0 = Part.makeLine(pntE0, pntD0)
            lineD0C0 = Part.makeLine(pntD0, pntC0)
            lineC0B0 = Part.makeLine(pntC0, pntB0)
            lineB0A0 = Part.makeLine(pntB0, pntA0)

            wire = Part.Wire([lineA0A1, lineA1B1, lineB1C1, lineC1D1, lineD1E1, lineE1F1, lineF1F0, 
                 lineF0E0, lineE0D0, lineD0C0, lineC0B0, lineB0A0])
            f = Part.Face([wire])
            base = f.extrude(zdir * L)

        base = self.processSubShapes(obj,base,pl)
        self.applyShape(obj,base,pl)

    def onChanged(self,obj,prop):
        self.hideSubobjects(obj,prop)
        ArchComponent.Component.onChanged(self,obj,prop)

class _ViewProviderWall(ArchComponent.ViewProviderComponent):
    "A View Provider for the Wall object"

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

class SteelHole:
    def __init__(self, position):
        self.Position = position

class CircleSteelHole(SteelHole):
    def __init__(self, position = FreeCAD.Vector(0, 0, 0), radius = 1):
        SteelHole.__init__(self, position)
        self.Radius = radius

class RectSteelHole(SteelHole):
    def __init__(self, position = FreeCAD.Vector(0, 0, 0), side = 1):
        SteelHole.__init__(self, position)
        self.Side = side

def makeCSteelPosEuler(L,
                 position = FreeCAD.Base.Vector(0, 0, 0), 
                 rotation = FreeCAD.Base.Vector(0, 0, 0),
                 name=""):
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return

    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", name)

    _CSteel(obj)
    _ViewProviderWall(obj.ViewObject)
    obj.H = 100
    obj.B = 50
    obj.C = 20
    obj.T = 2
    obj.L = L

    obj.Placement.Base = position
    
    rotX = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), rotation.x)
    rotY = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), rotation.y)
    rotZ = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), rotation.z)
    obj.Placement.Rotation = rotY.multiply(rotX).multiply(rotZ)
    
    doc.recompute()

    return obj

def makeCSteelPosRot(L,
                 position = FreeCAD.Base.Vector(0, 0, 0), 
                 rotation = FreeCAD.Base.Rotation()):
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return

    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CSteel")

    _CSteel(obj)
    _ViewProviderWall(obj.ViewObject)
    obj.H = 100
    obj.B = 50
    obj.C = 20
    obj.T = 2
    obj.L = L

    obj.Placement.Base = position
    obj.Placement.Rotation = rotation
    
    doc.recompute()

    return obj

def makeCSteelPlacement(L, pl = FreeCAD.Placement()):
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return

    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "CSteel")

    _CSteel(obj)
    _ViewProviderWall(obj.ViewObject)
    obj.H = 100
    obj.B = 50
    obj.C = 20
    obj.T = 2
    obj.L = L

    obj.Placement = pl
    
    doc.recompute()

    return obj    

def makeCSteel(name = "CSteel", H = 100, B = 50, C = 20, T = 2, L = 500, 
               position = FreeCAD.Base.Vector(0, 0, 0), 
               rotation = FreeCAD.Base.Rotation(),
               holes = []):
    doc = FreeCAD.ActiveDocument
    if doc is None:
        return

    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)

    _CSteel(obj)
    _ViewProviderWall(obj.ViewObject)
    obj.H = H
    obj.B = B
    obj.C = C
    obj.T = T
    obj.L = L

    obj.Placement.Base = position
    obj.Placement.Rotation = rotation
    doc.recompute()

    retObj = obj
    feat = obj

    for hole in holes:
        if hole.__class__ is CircleSteelHole:
            c = doc.addObject("Part::Cylinder", "Cylinder")
            c.Radius = hole.Radius
            c.Height = B

            pl = FreeCAD.Placement()
            pl.Base = hole.Position
            pl.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -90)
            c.Placement = feat.Placement.multiply(pl)

            '''
            cut = doc.addObject("Part::Cut","Cut")
            cut.Base = retObj
            cut.Tool = c
            retObj = cut
            doc.recompute()
            '''

            cut = doc.addObject("Part::FeaturePython", "Cut")
            CSteelCut(cut, retObj, c)
            retObj.ViewObject.hide()
            c.ViewObject.hide()
            _ViewProviderWall(cut.ViewObject)
            doc.recompute()
            retObj = cut
        elif hole.__class__ is RectSteelHole:
            b = doc.addObject("Part::Box", "Box")
            b.Length = hole.Side
            b.Width = hole.Side
            b.Height = hole.Side

            pl = FreeCAD.Placement()
            pl.Base = hole.Position
            pl.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), -90)
            pl2 = FreeCAD.Placement()
            pl2.Base = FreeCAD.Vector(-b.Length.Value / 2, -b.Width.Value / 2, 0)
            pl = pl.multiply(pl2)
            b.Placement = feat.Placement.multiply(pl)

            '''
            cut = doc.addObject("Part::Cut","Cut")
            cut.Base = retObj
            cut.Tool = b
            retObj = cut
            doc.recompute()
            '''

            cut = doc.addObject("Part::FeaturePython", "Cut")
            CSteelCut(cut, retObj, b)
            retObj.ViewObject.hide()
            b.ViewObject.hide()
            _ViewProviderWall(cut.ViewObject)
            doc.recompute()
            retObj = cut

    return retObj

def _mackeCSteelByXmlFile(xmlFileFullPath):
    import ArchInterface
    import Unity.Io.SticksXmlUtil
    framecad = Unity.Io.SticksXmlUtil.ReadXml(xmlFileFullPath)
    for plan in framecad.Plans:
        for frame in plan.Frames:
            for stick in frame.Sticks:
                if stick.Type == "Plate":
                    # ��X����ת90��
                    plRef = FreeCAD.Placement()
                    plRef.Base = FreeCAD.Vector(0, 0, 0)
                    plRef.Rotation = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90)
                    plRefInverse = plRef.inverse()

                    # �����յ�λ��
                    startInWorld = stick.Start
                    endInWorld = stick.End
                    startInRefCsys = plRefInverse.multVec(startInWorld)
                    endInRefCsys = plRefInverse.multVec(endInWorld)

                    # ƽ��+Z����ת
                    pl = FreeCAD.Placement()
                    pl.Base = startInRefCsys
                    pl.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), endInRefCsys - startInRefCsys)

                    plStickInWorld = plRef.multiply(pl)

                    # ��ת
                    if stick.Flipped:
                        plFlipped = FreeCAD.Placement()
                        plFlipped.Base = FreeCAD.Vector(0, 0, 0)
                        plFlipped.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 180)
                        plStickInWorld = plRef.multiply(pl).multiply(plFlipped)
                    else:
                        plStickInWorld = plRef.multiply(pl)

                    H = stick.Web
                    B = stick.LFlange
                    C = stick.LLip
                    T = stick.Gauge
                    L = (endInRefCsys - startInRefCsys).Length
                    makeCSteel(
                        name = frame.Name + "__" + stick.Name + "__Plate", H = H, B = B, C = C, T = T, L = L, 
                        position = plStickInWorld.Base, rotation = plStickInWorld.Rotation)
                elif stick.Type == "Stud":
                    # ��Z����ת90��
                    plA = FreeCAD.Placement()
                    plA.Base = FreeCAD.Vector(0, 0, 0)
                    plA.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 90)

                    # ǽ������λ����Ϣ
                    wallPntStartInWorld = FreeCAD.Vector(frame.Envelope.Vertexes[0].x, frame.Envelope.Vertexes[0].y, 0);
                    wallPntEndInWorld = FreeCAD.Vector(frame.Envelope.Vertexes[1].x, frame.Envelope.Vertexes[1].y, 0);
                    wallPntStartInA = plA.inverse().multVec(wallPntStartInWorld);
                    wallPntEndInA = plA.inverse().multVec(wallPntEndInWorld);

                    # ��ת�������ڷ���
                    plB = FreeCAD.Placement()
                    plB.Base = FreeCAD.Vector(0, 0, 0)
                    plB.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), wallPntEndInA - wallPntStartInA)

                    # �����յ�λ��
                    startInWorld = stick.Start
                    endInWorld = stick.End
                    startInB = plA.multiply(plB).inverse().multVec(startInWorld)
                    endInB = plA.multiply(plB).inverse().multVec(endInWorld)

                    # 
                    plC = FreeCAD.Placement()
                    plC.Base = startInB
                    plC.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), endInB - startInB)

                    # ��ת
                    if stick.Flipped:
                        plD = FreeCAD.Placement()
                        plD.Base = FreeCAD.Vector(0, 0, 0)
                        plD.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), 180)
                        plStickInWorld = plA.multiply(plB).multiply(plC).multiply(plD)
                    else:
                        plStickInWorld = plA.multiply(plB).multiply(plC)

                    H = stick.Web
                    B = stick.LFlange
                    C = stick.LLip
                    T = stick.Gauge
                    L = (endInWorld - startInWorld).Length
                    makeCSteel(
                        name = frame.Name + "__" + stick.Name + "__Stud", H = H, B = B, C = C, T = T, L = L, 
                        position = plStickInWorld.Base, rotation = plStickInWorld.Rotation)

def makeCSteelTest():
    xmlFiles = [FreeCAD.getResourceDir() + "/Xmls/it-Panel_1.xml",
                FreeCAD.getResourceDir() + "/Xmls/it-Floor_1.xml",
                FreeCAD.getResourceDir() + "/Xmls/it-Truss.1.xml"]
    for xmlFile in xmlFiles:
        _mackeCSteelByXmlFile(xmlFile)
