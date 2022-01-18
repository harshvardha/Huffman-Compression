import treenode
import huffmanDecoder
import sys
class compressor:
    def __init__(self,filepath):
        self.filepath = open(filepath,'r').read()
        self.orignalInputSize = len(self.filepath)*8
    
    def inputProcessor(self):
        #this function process the input file and extracts all the unique characters form the text file
        frequency_dictionary = {}
        for letter in self.filepath:
            count = 0
            if letter not in frequency_dictionary:
                index = self.filepath.index(letter)
                for i in range(index,len(self.filepath)):
                    if letter==self.filepath[i]:
                        count += 1
                frequency_dictionary[letter] = count
        self.dictionarySorter(frequency_dictionary)
    
    def dictionarySorter(self,dictionary):
        #function to sort the dictinary extracted from the text file
        keyList = list(dictionary)
        copyKeyList = []
        valueList = []
        keyList = self.mergeSort(keyList[:len(keyList)//2],keyList[len(keyList)//2:],dictionary)
        for key in keyList:
            valueList.append(dictionary[key])
            copyKeyList.append(key)
        dictionary.clear()
        for key in keyList:
            dictionary[key] = valueList[keyList.index(key)]
        print(dictionary)
        print("\n")
        root = self.huffmanEncoder(keyList,dictionary,copyKeyList)
        self.Preorder_Traversal(root)
        encodedBitsDictionary = self.bitWiseEncoder(root)
        print("\n")
        print(encodedBitsDictionary)
        encodedContent = self.contentEncoder(encodedBitsDictionary)
        print("\n")
        print(encodedContent)
        treeDictionary = self.huffmanTreeStore(root)
        print("\n")
        print(treeDictionary)
        obj = huffmanDecoder.decompressor(encodedContent[0],treeDictionary,encodedContent[1])
        obj.decodeContent()
        print(obj.getDecodedBits())
        print(len(obj.getDecodedBits()))
        obj.produceOriginalData()
        print("\n")
        print(obj.getOriginalData())

    def mergeSort(self,leftPart,rightPart,dictionary):
        #merge sort algorithm used to sort the keyList from the dictionary
        if(len(leftPart)!=1):
            leftPart = self.mergeSort(leftPart[:(len(leftPart)//2)],leftPart[(len(leftPart)//2):],dictionary)
        if(len(rightPart)!=1):
            rightPart = self.mergeSort(rightPart[:(len(rightPart)//2)],rightPart[(len(rightPart)//2):],dictionary)
        return self.sort(leftPart,rightPart,dictionary)

    def sort(self,leftPart,rightPart,dictionary):
        #this function sorts the keyList for the frequency dictionary
        combinedKeyList = leftPart+rightPart
        for i in range(len(combinedKeyList)):
            temp = None
            for j in range(0,len(combinedKeyList)-i-1):
                if(dictionary[combinedKeyList[j]]>dictionary[combinedKeyList[j+1]]):
                    temp = combinedKeyList[j+1]
                    combinedKeyList[j+1] = combinedKeyList[j]
                    combinedKeyList[j] = temp
        return combinedKeyList

    def huffmanEncoder(self,keyList,dictionary,copyKeyList):
        #this function creates the huffman tree recursively
        print(dictionary)
        print(keyList)
        print("\n")
        key_1 = keyList[0]
        key_2 = keyList[1]
        rootNode = treenode.frequencyNode(frequency = dictionary[key_1]+dictionary[key_2])
        if(key_1 in copyKeyList):
            leftNode = treenode.letterNode(letter = key_1)
            rootNode.setLeftNodeAddress(leftNode)
        else:
            rootNode.setLeftNodeAddress(key_1)
        if(key_2 in copyKeyList):
            rightNode = treenode.letterNode(letter = key_2)
            rootNode.setRightNodeAddress(rightNode)
        else:
            rootNode.setRightNodeAddress(key_2)
        del dictionary[key_1]
        del dictionary[key_2]
        del keyList[0]
        del keyList[0]
        if(len(keyList)!=0):
            dictionary[rootNode] = rootNode.getFrequency()
            keyList = self.binarySearch(rootNode,keyList,dictionary)
            rootNode = self.huffmanEncoder(keyList,dictionary,copyKeyList)
        return rootNode
    
    def binarySearch(self,key,keyList,dictionary):
        #using the binary search algorithm to find the correct place for the newly created rootNode in the keyList so that it remains sorted in ascending arder
        startingIndex = 0
        lastIndex = len(keyList)-1
        correctIndex = 0
        while(lastIndex>=startingIndex):
            midIndex = (startingIndex+lastIndex)//2
            if(key.getFrequency()<dictionary[keyList[midIndex]]):
                lastIndex = midIndex-1
            elif(key.getFrequency()>=dictionary[keyList[midIndex]]):
                startingIndex = midIndex+1
                correctIndex = midIndex+1
        keyList.insert(correctIndex,key)
        return keyList
    
    def bitWiseEncoder(self,root,encodedBits="",encodedBitsDictionary={}):
        if(type(root.getLeftNodeAddress())==treenode.frequencyNode):
            encodedBits += '0'
            encodedBitsDictionary = self.bitWiseEncoder(root.getLeftNodeAddress(),encodedBits,encodedBitsDictionary)
        elif(type(root.getLeftNodeAddress())==treenode.letterNode):
            encodedBits += '0'
            encodedBitsDictionary[root.getLeftNodeAddress().getLetter()] = encodedBits
        
        if(type(root.getRightNodeAddress())==treenode.frequencyNode):
            if(type(root.getLeftNodeAddress())==treenode.frequencyNode or type(root.getLeftNodeAddress())==treenode.letterNode):
                encodedBits = encodedBits[:len(encodedBits)-1]+'1'
            else:
                encodedBits += '1'
            encodedBitsDictionary = self.bitWiseEncoder(root.getRightNodeAddress(),encodedBits,encodedBitsDictionary)
        elif(type(root.getRightNodeAddress())==treenode.letterNode):
            if(root.getLeftNodeAddress()==None):
                encodedBits += '1'
            elif(type(root.getLeftNodeAddress())==treenode.letterNode or type(root.getLeftNodeAddress())==treenode.frequencyNode):
                encodedBits = encodedBits[:len(encodedBits)-1]+'1'
            encodedBitsDictionary[root.getRightNodeAddress().getLetter()] = encodedBits
        return encodedBitsDictionary

    def Preorder_Traversal(self,root):
        if(root==None):
            return
        else:
            if(type(root)==treenode.frequencyNode):
                print(root.getFrequency())
                if(root.getLeftNodeAddress()==None):
                    self.Preorder_Traversal(root.getRightNodeAddress())
                else:
                    self.Preorder_Traversal(root.getLeftNodeAddress())
                    self.Preorder_Traversal(root.getRightNodeAddress())
            elif(type(root)==treenode.letterNode):
                pass
                print(root.getLetter())
    
    def contentEncoder(self,compressedBitsDictionary):
        compressedString = ''
        encodedContent = ''
        compressedStringLength = 0
        for letter in self.filepath:
            compressedString += compressedBitsDictionary[letter]
        print(compressedString)
        compressedStringLength = len(compressedString)
        partsCount = len(compressedString)//8
        while(partsCount>0):
            decimalEquivalent = self.binary_To_decimal(int(compressedString[:8]))
            compressedString = compressedString[8:]
            partsCount -= 1
            encodedContent += chr(decimalEquivalent)
        encodedContent += chr(self.binary_To_decimal(int(compressedString)))
        return (encodedContent,compressedStringLength)
    
    def huffmanTreeStore(self,root,treeDictionary={},rootIndex = 0):
        if(rootIndex==0):
            treeDictionary[0]=root.getFrequency()
        if(root.getLeftNodeAddress()!=None):
            if(type(root.getLeftNodeAddress())==treenode.frequencyNode):
                treeDictionary[2*rootIndex+1] = root.getLeftNodeAddress().getFrequency()
            elif(type(root.getLeftNodeAddress())==treenode.letterNode):
                treeDictionary[2*rootIndex+1] = root.getLeftNodeAddress().getLetter()
            treeDictionary = self.huffmanTreeStore(root.getLeftNodeAddress(),treeDictionary,2*rootIndex+1)
        if(root.getRightNodeAddress()!=None):
            if(type(root.getRightNodeAddress())==treenode.frequencyNode):
                treeDictionary[2*rootIndex+2] = root.getRightNodeAddress().getFrequency()
            elif(type(root.getRightNodeAddress())==treenode.letterNode):
                treeDictionary[2*rootIndex+2] = root.getRightNodeAddress().getLetter()
            treeDictionary = self.huffmanTreeStore(root.getRightNodeAddress(),treeDictionary,2*rootIndex+2)
        return treeDictionary

    def binary_To_decimal(self,num):
        result = 0
        counter = 0
        while num!=0:
            result = result+(num%10)*2**counter
            counter += 1
            num = int(num/10)
        return result

if __name__=='__main__':
    obj = compressor("compressionAlgorithm.txt")
    obj.inputProcessor()