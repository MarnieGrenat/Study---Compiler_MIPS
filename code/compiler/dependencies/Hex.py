class Hex:
    def __init__(self, hexCode:str) -> None:
        self.binaryCode = self.generateBinary()
        self.hexCode = hexCode.splitLines()
        self.labels = self.findAllLabels()
        
        def generateBinary(self) -> list:
            binary = []
            for hexLine in self.hexCode:
                binary.append(self.hexToBin(hexLine))
            return binary
        
        def hexToBin(line:str) -> str:
            line = bin(int(line, 16))                   # hex -> dec -> bin
            line = line[2:].zfill(32)                   # 32 bits only and remove 0b
            return str(line)
      
        ### GETTERS ###
        def getBinaryCode(self) -> str:
            return self.binaryCode

        def getHexCode(self) -> str:
            return self.hexCode

    ######################### TRADUÇÃO BINÁRIO PARA ASSEMBLY #########################
    
    