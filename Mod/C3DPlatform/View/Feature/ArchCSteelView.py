from C3DPlatform.View.Feature import FeatureView

import ArchCSteelViewImpl

class ArchCSteelView(FeatureView):
    def __init__(self, feat, name="", create=True):
        super(ArchCSteelView, self).__init__()
        
        if create:
            self.feature = ArchCSteelViewImpl.makeCSteelPosEuler(feat.L, name = name)
        else:
            self.feature = feat
        