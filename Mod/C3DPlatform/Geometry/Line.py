from Vector import Vector

class Line(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def step(self, step):
        import math
        step = math.fabs(step)
        v = self.end - self.start
        length = v.Length
        
        if length < 1e-8 or step < 1e-8:
            return []
        else:
            m = int(math.ceil(length / step))
            n = int(math.floor(length / step))
            if m == n:
                n -= 1
            dir = v.Normalized
            points = []
            for i in range(n):
                point = self.start + dir * step * (i+1)
                points.append(point)
            return points
        
        
            
        
        