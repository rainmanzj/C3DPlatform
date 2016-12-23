class Property:
    def __init__(self, name, type, value = None):
        self.name = name
        self.type = type
        self.value = value

class PropertyContainer:
    def __init__(self):
        self.Properties = []
    
    def addProperty(self, name, type, value = None):
        prop = Property(name, type, value)
        self.Properties.append(prop)

class DocumentObject:
    pass