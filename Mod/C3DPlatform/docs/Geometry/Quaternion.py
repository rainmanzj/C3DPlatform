from Vector import Vector
import math
import copy

class Quaternion:
    
    def __init__(self, x = 0.0, y = 0.0, z = 0.0, w = 1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
    @staticmethod
    def identity():
        return Quaternion(0.0, 0.0, 0.0, 1.0)
        
    @staticmethod
    def AxisAngle(axis, angle):
        angleInRad = angle / 180.0 * 3.1415926
        return Quaternion.AxisAngleInRadian(axis, angleInRad)
        
    @staticmethod
    def AxisAngleInRadian(axis, angle):
        norm = copy.deepcopy(axis)
        norm.normalize()
        scale = math.sin(angle * 0.5)
        
        quat = Quaternion()
        quat.w = math.cos(angle * 0.5)
        quat.x = norm.x * scale
        quat.y = norm.y * scale
        quat.z = norm.z * scale
        
        return quat
        
    @staticmethod
    def FromToRotation(rotFrom, rotTo):
        u = rotFrom.Normalized
        v = rotTo.Normalized
        dot = u.dot(v)
        w = u.cross(v)
        
        if w.Length == 0.0:
            if dot > 0.0:
                return Quaternion(0.0, 0.0, 0.0, 1.0)
            else:
                t = u.cross(Vector(1.0, 0.0, 0.0))
                if t.Length < 1e-8:
                    t = u.cross(Vector(0.0, 1.0, 0.0))
                return Quaternion(t.x, t.y, t.z, 0.0)
        else:
            angleInRad = math.acos(dot)
            return Quaternion.AxisAngleInRadian(w, angleInRad)
            
    @staticmethod
    def Euler(x, y, z):
        # Z-->X-->Y
        rotX = Quaternion.AxisAngle(Vector(1, 0, 0), x)
        rotY = Quaternion.AxisAngle(Vector(0, 1, 0), y)
        rotZ = Quaternion.AxisAngle(Vector(0, 0, 1), z)
        return rotY * rotX * rotZ
            
    def invert(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        
    def inverse(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)
        
    def multVec(self, vec):
        x = self.x
        y = self.y
        z = self.z
        w = self.w
        x2 = self.x * self.x
        y2 = self.y * self.y
        z2 = self.z * self.z
        w2 = self.w * self.w
    
        dx = (x2+w2-y2-z2)*vec.x + 2.0*(x*y-z*w)*vec.y + 2.0*(x*z+y*w)*vec.z;
        dy = 2.0*(x*y+z*w)*vec.x + (w2-x2+y2-z2)*vec.y + 2.0*(y*z-x*w)*vec.z;
        dz = 2.0*(x*z-y*w)*vec.x + 2.0*(x*w+y*z)*vec.y + (w2-x2-y2+z2)*vec.z;
        
        return Vector(dx, dy, dz)
        
    def eulerAngles(self):
        pass
        
    def __mul__(self, other):
        return Quaternion(
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z)
            
    def multiply(self, rhs):
        return self * rhs
        
    def __str__(self):
        return "Quaternion(%f, %f, %f, %f)" % (self.x, self.y, self.z, self.w)
        
    def __repr__(self):
        return "Quaternion(%f, %f, %f, %f)" % (self.x, self.y, self.z, self.w)