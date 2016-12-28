from C3DPlatform.View.Feature import FeatureView

import Arch

class ArchCSteelView(FeatureView):
    def __init__(self, L):
        super(ArchCSteelView, self).__init__()
    
        self.feature = Arch.makeCSteelPosEuler(L)