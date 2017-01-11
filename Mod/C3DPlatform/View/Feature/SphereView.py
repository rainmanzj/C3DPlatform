from C3DPlatform.View.Feature import FeatureView
import SphereViewImpl

class SphereView(FeatureView):
    def __init__(self, feat, name="", create = True):
        super(SphereView, self).__init__()
        
        if create:
            self.feature = SphereViewImpl.makeSphere(feat.Radius, name)
        else:
            self.feature = feat
    