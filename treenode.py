class frequencyNode:
    def __init__(self,frequency):
        self.frequency = frequency
        self.leftNodeAddress = None
        self.rightNodeAddress = None
    
    def setFrequency(self,frequency):
        self.frequency = frequency
    
    def getFrequency(self):
        return self.frequency
    
    def setLeftNodeAddress(self,leftNodeAddress):
        self.leftNodeAddress = leftNodeAddress
    
    def getLeftNodeAddress(self):
        return self.leftNodeAddress
    
    def setRightNodeAddress(self,rightNodeAddress):
        self.rightNodeAddress = rightNodeAddress
    
    def getRightNodeAddress(self):
        return self.rightNodeAddress

class letterNode:
    def __init__(self,letter):
        self.letter = letter
        self.leftNodeAddress = None
        self.rightNodeAddress = None
    
    def getLetter(self):
        return self.letter

    def setLetter(self,letter):
        self.letter = letter
    
    def getLeftNodeAddress(self):
        return self.leftNodeAddress
    
    def getRightNodeAddress(self):
        return self.rightNodeAddress