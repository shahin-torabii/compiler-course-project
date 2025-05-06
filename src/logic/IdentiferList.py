class IdentifierList:
    def __init__(self):
        self.identifiers = []
        self.dic = {}

    def addToList(self, newIdentifier):
        self.identifiers.append(newIdentifier)

    def findByName(self, name):
        list = []
        for identifier in self.identifiers:
            if identifier.name == name:
                list.append(identifier)
        if list is not None:
            return list
        else:
            print("No identifier found with this name")

    def findByFileName(self, fileName):
        list = []
        for identifier in self.identifiers:
            if identifier.fileName == fileName:
                list.append(identifier)
        if list is not None:
            return list
        else:
            print("No identifier found with this fileName")

    def findEncrypted(self, value, fileName):
        list = []
        for identifier in self.identifiers:
            if identifier.value == value and identifier.fileName == fileName:
                list.append(identifier)
        if list is not None:
            return list
        else:
            print("No identifier found with this value")

    def findByType(self, type):
        list = []
        for identifier in self.identifiers:
            if identifier.type == type:
                list.append(identifier)
        if list is not None:
            return list
        else:
            print("No identifier found with this fileName")

    def find(self, name, type, fileName):
        for identifier in self.identifiers:
            if identifier.type == type and identifier.name == name and identifier.fileName == fileName:
                return identifier
        print("No identifier found")

    def printList(self, custom_list=None):
        if custom_list is None:
            custom_list = self.identifiers
        for identifier in custom_list:
            identifier.print()

    def makeDic(self):
        for identifier in self.identifiers:
            self.dic[identifier.name] = identifier.editedName
        return self.dic


