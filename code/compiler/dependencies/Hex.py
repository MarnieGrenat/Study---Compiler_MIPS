from Error import Error
from Debugger import logD, logE, logI, logV, logW
class Hex:
    def __init__(self, hexCode:str) -> None:
        self.binaryCode = self.generateBinary()
        self.hexCode = hexCode
        self.assembly = self.generateAssembly()

        def generateBinary(self) -> list:
            binary = []
            for hexLine in self.hexCode:
                binary.append(self.hexToBin(hexLine))
            return binary

        def hexToBin(line:str) -> str:
            line = bin(int(line, 16))
            line = line[2:].zfill(32)
            return str(line)

        def generateAssembly(self) -> str:
            opCodeBin = self.generateOpCode()
            self.translateCommand(opCodeBin)

        ### GETTERS ###
        def getBinaryCode(self) -> list:
            return self.binaryCode

        def getHexCode(self) -> str:
            return self.hexCode

        def getAssemblyCode(self) -> str:
            return self.assemblyCode

    ######################### TRADUÇÃO BINÁRIO PARA ASSEMBLY #########################

        def getOpcode(self) -> str:
            token = self.binaryCode[0:6]
            return token

        def translateCommand(token:str) -> str: #TODO: trocar values
            opCodeMapping = {
                'or': '0b000000',
                'and': '0b000000',
                'sub': '0b000000',

                'beq': '0b000100',
                'lw': '0b100011',
                'sw': '0b101011',
                'sltiu': '0b001011',

                'j': '0b000010'
            }
            if token in opCodeMapping:
                logV(f"OpCode encontrado no mapeamento. Retornando valor: {self.first6Bits(opCodeMapping[token])}")
                return self.first6Bits(opCodeMapping[token])
            raise Error(f"Comando {token} não reconhecido.")