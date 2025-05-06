class Identifier:

    def __init__(self, name: str, type: int, exactType: int, line, fileName, value="NO_VALUE"):
        try:
            self.name = name
            self.type = type
            self.exactType = exactType
            self.line = line
            self.fileName = fileName
            self.editedName = None
            self.value = value
            self.newValue = None
            self.varOrReturnType = None
            self.isEncrypted = False
            self.isStringified = False
            self.implementList = None
            self.extend = None
            self.isRenamed = False

        except:
            print("Wrong format for making identifier")

    def print(self):
        print("name:", self.name, "| type:", self.type,"| exactType",self.exactType ,"| fileName:", self.fileName, "| line:", self.line, "| varOrReturnType:", self.varOrReturnType)

    def getAtr(self):
        return self.name, self.type, self.fileName

    def getName(self):
        return self.name

    def setEditedName(self, name):
        self.editedName = name

    def getValue(self):
        return self.value

    def setEditedValue(self, newValue):
        self.newValue = newValue

    def setVarType(self, varType):
        self.varType = varType

    def setVarOrReturnType(self, varOrReturnType):
        self.varOrReturnType = varOrReturnType
    def __eq__(self, other):

        if self.name == other.name and self.value == other.value and self.type == other.type and self.exactType == other.exactType and self.fileName == other.fileName and self.line == other.line:
            return True
        else:
            return False

