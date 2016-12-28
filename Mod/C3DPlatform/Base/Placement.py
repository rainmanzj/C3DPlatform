from Vector import Vector
from Quaternion import Quaternion

class Placement(object):
    def __init__(self, pos = Vector(), rot = Quaternion()):
        self.position = pos
        self.rotation = rot
        
    def multVec(self, src):
        dst = self.rotation.multVec(src)
        dst += self.position
        return dst
        
    def __str__(self):
        return "Placement [Position=(%f,%f,%f) Rotation=(%f,%f,%f,%f)]" % \
            (self.position.x, self.position.y, self.position.z, \
             self.rotation.x, self.rotation.y, self.rotation.z, self.rotation.w)
        
    def __repr__(self):
        return "Placement [Position=(%f,%f,%f) Rotation=(%f,%f,%f,%f)]" % \
            (self.position.x, self.position.y, self.position.z, \
             self.rotation.x, self.rotation.y, self.rotation.z, self.rotation.w)