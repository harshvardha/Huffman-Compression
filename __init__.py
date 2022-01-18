import os
import sys
DIRECTORY = None
if(getattr(sys,"frozen",False)):
    DIRECTORY = os.path.join(os.path.dirname(sys.executable),"compressionEngine")
else:
    DIRECTORY = os.path.join(__file__)
huffmanEncoder = os.path.join(DIRECTORY,"huffmanEncoder")
huffmanDecoder = os.path.join(DIRECTORY,"huffmanDecoder")
treenode = os.path.join(DIRECTORY,"treenode")
