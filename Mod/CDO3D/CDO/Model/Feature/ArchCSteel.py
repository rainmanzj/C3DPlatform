from CDO.Model.Feature import Feature
from CDO.View.Feature import ArchCSteelView

class ArchCSteel(Feature):
    def __init__(self, L):
        self.L = L
        self.view = ArchCSteelView(L)