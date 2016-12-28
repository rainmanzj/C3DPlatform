import Vector
import Quaternion

class Placement:
    def __init__(self, pos = Vector(), rot = Quaternion()):
        self.position = pos
        self.rotation = rot