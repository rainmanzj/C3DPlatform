from CDO.Model import DocumentObject

class Feature(DocumentObject):
    def __init__(self):
        super(Feature, self).__init__()
        self.type = "Feature"