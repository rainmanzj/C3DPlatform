from C3DPlatform.View.Feature import FeatureView
import BooleanCommonViewImpl

class BooleanCommonView(FeatureView):
    def __init__(self, feat, name="", create=True):
        super(BooleanCommonView, self).__init__()
        
        if create:
            self.feature = BooleanCommonViewImpl.makeCommon(None)
        else:
            self.feature = feat
            
    @property
    def Items(self):
        items = []
        for o in self.feature.Items:
            import FeatureView
            fv,type = FeatureView.FeatureView._from(o)
            items.append(fv)
        return items
        
    @Items.setter
    def Items(self, value):
        for o in self.feature.Items:
            o.ViewObject.show()
            
        items = []
        for o in value:
            o.view.feature.ViewObject.hide()
            items.append(o.view.feature)
        self.feature.Items = items