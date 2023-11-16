from compiler.dependencies.Error import Error
from compiler.dependencies.Debugger import logE, logW, logI, logD, logV


class Hex:
    def __init__(self, hexCode: str) -> None:
        self.hexCode = hexCode
        self.binaryCode = self.generateBinary(self.hexCode)
        self.assembly = self.generateAssembly(self.binaryCode)
        self.labels = []

    def generateBinary(self, hexCode) -> list:
        binary = []
        for hexLine in hexCode:
            binary.append(self.formatBinary(hexLine))
        return binary

    def formatBinary(self, line: str) -> str:
        line = bin(int(line, 16))
        line = line[2:].zfill(32)
        return str(line)

    def generateAssembly(self, binaryList:list) -> str:
        assembly = ".text:\n\nmain:\n"
        for binary in binaryList:
            type = self.guessTokenType(binary)
            aux = self.getAllTokens(type, binary) + "\n"
            logI(f"Comando traduzido: \n{aux}")
            assembly += aux
        return assembly

    def guessTokenType(self, binary: str) -> str:
        token = binary[0:6]
        if token in ['000000']:
            return 'R'
        if token in ['000100', '100011', '101011', '001011']:
            return 'I'
        if token in ['000010']:
            return 'J'
        raise Error(f"Comando {token} não reconhecido.")

    ### GETTERS ###

    def getBinaryCode(self) -> list:
        return self.binaryCode

    def getHexCode(self) -> str:
        return self.hexCode

    def getAssemblyCode(self) -> str:
        return self.assembly

    def getAllTokens(self, type: str, binary: str) -> str:
        logI(f"Traduzindo tipo {type}. Comando: {binary}")
        logI(f'Binário recebido: {binary[0:6]}-{binary[6:11]}-{binary[11:16]}-{binary[16:22]}-{binary[22:31]}')
        if type == 'R':
            return self.translateRType(binary)
        if type == 'I':
            return self.translateIType(binary)
        if type == 'J':
            return self.translateJType(binary)

    def translateRType(self, binary) -> str:
        opCode = self.generateOpCodeR(binary)
        rs = self.generateRegister(binary, 1)
        rt = self.generateRegister(binary, 2)
        rd = self.generateRegister(binary, 3)
        lineCode = f"{opCode} {rd}, {rs}, {rt}"
        return lineCode

    def generateOpCodeR(self, binary: str):
        funct = binary[-6:]
        match funct:
            case '100101':
                return 'or'
            case '100100':
                return 'and'
            case '100010':
                return 'sub'
            case _:
                raise Error(f"Função não conhecida: {funct}")

    def generateRegister(self, binary: str, position: int) -> str:
        binary = self.getRegisterBinary(binary, position)
        token = self.tokenizeRegister(binary)
        logV(f'Registrador {position}: {binary} -> {token}')
        return token

    def getRegisterBinary(self, binary: str, position: int):
        match position:
            case 1:
                return binary[6:11]      # primeiro reg
            case 2:
                return binary[11:16]      # segundo reg
            case 3:
                return binary[16:21]      # terceiro reg

    def tokenizeRegister(self, binary: str) -> str:
        register =  int(binary, 2)
        token = "$" + str(register)
        return token

    def translateIType(self, binary: str) -> str:
        token = self.generateOpCodeI(binary)
        if token in ['lw', 'sw']:
            return self.generateBracketsFormat(binary)
        if token in ['beq', 'sltiu']:
            return self.generateImmediateFormat(binary)
        raise Error(f"Comando I não reconhecido: {token}")

    def generateOpCodeI(self, binary: str) -> str:
        token = binary[0:6]
        tokenMapping = {
            '000100': 'beq',
            '001011': 'sltiu',
            '100011': 'lw',
            '101011': 'sw'
        }
        if token in tokenMapping:
            return tokenMapping[token]
        raise Error(f"Comando I não reconhecido: {token}")

    def generateBracketsFormat(self, binary: str) -> str:
        '''OP rt,offset(rs)'''
        opCode = self.getOpCodeI(binary)
        rs = self.generateRegister(binary, 1)
        rt = self.generateRegister(binary, 2)
        offset = int(binary[16:], 2)
        line = f"{opCode} {rt}, {offset}({rs})"
        return line

    def generateImmediateFormat(self, binary) -> str:
        '''OP rs,rt,imm'''
        line = ''
        opCode = self.getOpCodeI(binary)
        rs = self.generateRegister(binary, 1)
        rt = self.generateRegister(binary, 2)

        if opCode == 'beq':  # TODO: Gerar Label
            self.generateLabel(binary[16:])
            offset  = self.getOffsetLabel(binary[16:])
            line = f"{opCode} {rs}, {rt}, {offset}"

        elif opCode == 'sltiu':
            imm = int(binary[16:], 2)
            line = f"{opCode} {rt}, {rs}, {imm}"
        else:
            raise Error(f"Comando não reconhecido.{binary}")
        return line

    def getOpCodeI(self, token:str):
        token = token[0:6]
        tokenMapping = {
            '000100': 'beq',
            '001011': 'sltiu',
            '100011': 'lw',
            '101011': 'sw'
        }
        if token in tokenMapping:
            return tokenMapping[token]
        raise Error(f"Comando I não reconhecido: {token}")

    def getOffsetLabel(self, binary: str) -> dict:
        if binary[0] == '1':
            binary = self.twosComplement(binary)
        else:
            labelName = 'L' + str(len(self.labelCounter))

            return {labelName: binary}

    def twosComplement(self, immediate: str) -> int:
        '''ref: https://www.adamsmith.haus/python/answers/how-to-take-two's-complement-in-python'''
        immediateBin = ''
        for b in immediate:
            if b == "0":
                immediateBin += "1"
            else:
                immediateBin += "0"

        immediate = int(immediateBin, 2)

        immediate *=-1
        immediate += 1
        logI(f"immediate Complemento: {immediateBin}")
        if immediate > 0:
            raise Error(f"Valor inválido para operação de complemento de dois: {immediate}")
        return immediateBin

    def generateLabel(self, binary: str) -> str:
        #TODO: Iterar sobre o arquivo final e gerar label
        pass

    def translateJType(self, binary):
        opCode = self.getOpCodeJ(binary)
        address = self.generateJLabel(int(binary[6:], 2))
        return f"{opCode} {address}"

    def getOpCodeJ(self, token:str):
        token [0:6]
        if token == '000010':
            return '000010'
        raise Error(f"Comando não reconhecido: {token}")

    def generateJLabel(self, address: int) -> str:
        address = int(address, 2)
        address -= 4194304
        aux = self.binaryCode[address]
        self.binaryCode[address] = 'L' + str(len(self.labels))
        for line in self.binaryCode[address+1:]:
            aux2 = line