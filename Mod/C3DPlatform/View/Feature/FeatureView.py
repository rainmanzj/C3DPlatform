from C3DPlatform.View import View

class FeatureView(View):
    def __init__(self):
        super(FeatureView, self).__init__()
        
        self.feature = None
        
    def show(self):
        self.feature.ViewObject.show()
        
    def hide(self):
        self.feature.ViewObject.hide()
        
    def update(self):
        self.feature.ViewObject.update()
        
    def delete(self):
        self.feature.Document.removeObject(self.feature.Name)
        
    def addProperty(self, name, type, group = "", value = None):
        type = "App::Property" + type
        self.feature.addProperty(type, name, group, name)
        if value is not None:
            setattr(self.feature, name, value)
            
    def setProperty(self, name, value):
        setattr(self.feature, name, value)