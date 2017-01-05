from C3DPlatform.View.Feature import FeatureView

import ArchTriangularViewImpl

class ArchTriangularView(FeatureView):
    def __init__(self, feat, name="", create = True):
        super(ArchTriangularView, self).__init__()
        
        if create:
            self.feature = ArchTriangularViewImpl.make(feat.L, feat.W, feat.H, name)
        else:
            self.feature = feat