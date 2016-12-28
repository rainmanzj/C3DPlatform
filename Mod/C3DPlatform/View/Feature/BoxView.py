from C3DPlatform.View.Feature import FeatureView

import Arch

class BoxView(FeatureView):
    def __init__(self, length, width, height):
        super(BoxView, self).__init__()
        
        self.feature = Arch.makeBox(length, width, height)