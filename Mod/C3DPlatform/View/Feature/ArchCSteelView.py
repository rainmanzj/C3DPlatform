from C3DPlatform.View.Feature import FeatureView

import Arch

class ArchCSteelView(FeatureView):
    def __init__(self, feat, create = True):
        super(ArchCSteelView, self).__init__()
        
        if create:
            self.feature = Arch.makeCSteelPosEuler(feat.L)
        else:
            self.feature = feat
        