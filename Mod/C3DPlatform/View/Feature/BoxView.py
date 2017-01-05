from C3DPlatform.View.Feature import FeatureView

import BoxViewImpl

class BoxView(FeatureView):
    def __init__(self, feat, name="", create = True):
        super(BoxView, self).__init__()
        
        if create:
            self.feature = BoxViewImpl.makeBox(feat.L, feat.W, feat.H, name)
        else:
            self.feature = feat