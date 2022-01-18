class decompressor:
    def __init__(self,encodedContent,treeDictionary,compressedSize):
        self.encodedContent = encodedContent
        self.treeDictionary = treeDictionary
        self.compressedSize = compressedSize
        self.decodedBits = ''
        self.originalData = ''
    
    def decodeContent(self):
        noOf8BitParts = self.compressedSize//8
        remainingParts = self.compressedSize%8
        originalCompressedBits = ''
        for i in range(noOf8BitParts):
            originalCompressedBits = str(bin(ord(self.encodedContent[i])))[2:]
            if(len(originalCompressedBits)<8):
                difference = 8-len(originalCompressedBits)
                while(difference>0):
                    originalCompressedBits = '0'+originalCompressedBits
                    difference -= 1
            self.decodedBits += originalCompressedBits
        originalCompressedBits = str(bin(ord(self.encodedContent[noOf8BitParts])))[2:]
        if(len(originalCompressedBits)<remainingParts):
            while(remainingParts>0):
                originalCompressedBits = '0'+originalCompressedBits
                remainingParts -= 1
        self.decodedBits += originalCompressedBits
    
    def produceOriginalData(self):
        rootIndex = 0
        for bit in self.decodedBits:
            if(bit=='1'):
                rootIndex = 2*rootIndex+2
            elif(bit=='0'):
                rootIndex = 2*rootIndex+1
            if(type(self.treeDictionary[rootIndex])==str):
                self.originalData += self.treeDictionary[rootIndex]
                rootIndex = 0
                self.decodedBits = self.decodedBits[self.decodedBits.index(bit)+1:]
    
    def getOriginalData(self):
        return self.originalData
    
    def getDecodedBits(self):
        return self.decodedBits