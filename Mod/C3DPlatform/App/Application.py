from C3DPlatform.View import ApplicationView
from C3DPlatform.Model import Document

class Application(object):
    _instance = None
    
    def __init__(self):
        self.view = ApplicationView()
    
    @staticmethod
    def Instance():
        if Application._instance is None:
            Application._instance = Application()
        return Application._instance
    
    @property
    def ActiveDocument(self):
        docView = self.view.activeDocument()
        if docView is None:
            return None
        else:
            return Document(docView)