from C3DPlatform.View.Feature import FeatureView
import BooleanCutViewImpl

class BooleanCutView(FeatureView):
    def __init__(self, feat, name="", create=True):
        super(BooleanCutView, self).__init__()
        
        if create:
            self.feature = BooleanCutViewImpl.makeCut()
        else:
            self.feature = feat
    
    @property
    def Base(self):
        import FeatureView
        fv,type = FeatureView.FeatureView._from(self.feature.Base)
        return fv
        
    @Base.setter
    def Base(self, value):
        if self.feature.Base is not None:
            self.feature.Base.ViewObject.show()
        
        value.view.feature.ViewObject.hide()
        self.feature.Base = value.view.feature
        
    @property
    def Tool(self):
        import FeatureView
        fv,type = FeatureView.FeatureView._from(self.feature.Tool)
        return fv
        
    @Tool.setter
    def Tool(self, value):
        if self.feature.Tool is not None:
            self.feature.Tool.ViewObject.show()
            
        value.view.feature.ViewObject.hide()
        self.feature.Tool = value.view.feature