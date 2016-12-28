import math

class Vector(object):
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = x
        self.y = y
        self.z = z
    
    @property
    def Length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        
    @property
    def LengthSquared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z
        
    def normalize(self):
        length = self.Length
        if length > 1e-8:
            self.x /= length
            self.y /= length
            self.z /= length
    
    @property
    def Normalized(self):
        length = self.Length
        if length > 1e-8:
            return Vector(self.x / length, self.y / length, self.z / length)
        else:
            return Vector()
        
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector):
            return self.dot(other)
        else:
            return None
        
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
        
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
        
    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x)
        
    def __str__(self):
        return "Vector(%f, %f, %f)" % (self.x, self.y, self.z)
        
    def __repr__(self):
        return "Vector(%f, %f, %f)" % (self.x, self.y, self.z)