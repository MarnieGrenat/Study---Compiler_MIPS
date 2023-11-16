from compiler.dependencies.Error import Error
from compiler.dependencies.Debugger import logE, logW, logI, logD, logV


class Hex:
    def __init__(self, hexCode: str) -> None:
        self.hexCode = hexCode
        self.labels = []
        self.binaryCode = self.generateBinary(self.hexCode)
        self.assembly = self.generateAssembly(self.binaryCode)

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
        ## TODO: Tratar sinal de Jump ou BEQ
        assembly = ""
        for binary in binaryList:
            type = self.guessTokenType(binary)
            aux = self.getAllTokens(type, binary) + "\n"
            logI(f"Comando traduzido: \n{aux}")
            assembly += aux
        return ".text:\n\nmain:\n" + self.treatAddresses(assembly)

    def treatAddresses(self, assembly:str) -> str:
        assembly = assembly.splitlines()
        for line in assembly:
            logI(f"Commando de jump {line[0]} ou beq: {line[:4]}")
            if line[-1] == ":":
            if line[0] == 'j' or line[:4] == 'beq':
                assembly = self.generateLabels(assembly, line, line[0])
        logI(f"Assembly com labels: \n{assembly}")
        return assembly

    def generateLabels(self, assembly:list, line:str, type:str) -> str:
        labelAddr = int(line[-1])
        labelName = 'L' + str(len(self.labels))
        assembly = self.__setLabel(assembly, line, labelAddr, labelName)
        #list to str
        codeLine = ""
        for command in assembly:
            codeLine += command + '\n'
        return codeLine


    def __setLabel(self, assembly:list, line:str, labelAddr:int, labelName:str) -> list:
        if labelName not in self.labels:
            self.labels.append(labelName)
            logV(f"Label adicionada. ao array de labels. {labelName}")
        else:
            raise Error(f"Label {labelName} já existe.")
        assembly[labelAddr] = f"{labelName}: \n {assembly[labelAddr]}"
        for command in assembly:
            if command == line:
                command = command.split()
                command[-1] = labelName
                command = ' '.join(command)

        logI (f"Label {labelName} adicionada na linha: {assembly[labelAddr-1]}")
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
        if self.binaryCode:
            return self.binaryCode
        raise Error("Código binário não gerado.")

    def getHexCode(self) -> str:
        if self.hexCode:
            return self.hexCode
        raise Error("Hex code não capturado. Verifique arquivo.")

    def getAssemblyCode(self) -> str:
        if self.assembly:
            return self.assembly
        raise Error("Assembly não gerado.")

    def getAllTokens(self, type: str, binary: str) -> str:
        logI(f"Traduzindo tipo {type}. Comando: {binary}")
        logI(f'Binário recebido: {binary[0:6]}-{binary[6:11]}-{binary[11:16]}-{binary[16:22]}-{binary[22:31]}')
        if type == 'R':
            return self.translateRType(binary)
        if type == 'I':
            return self.translateIType(binary)
        if type == 'J':
            return self.translateJType(binary)
        raise Error(f"Tipo de binário não encontrado.")

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
        if len(binary) < 32:
            raise Error(f"Binário inválido: {binary}")
        match position:
            case 1:
                return binary[6:11]       # primeiro reg
            case 2:
                return binary[11:16]      # segundo reg
            case 3:
                return binary[16:21]      # terceiro reg
            case _:
                raise Error(f"Posição {position} não encontrada. Parâmetro inválido.")

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
        line = ''
        opCode = self.getOpCodeI(binary)
        rs = self.generateRegister(binary, 1)
        rt = self.generateRegister(binary, 2)

        if opCode == 'beq':
            #self.generateLabel(binary[16:])
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
            return self.twosComplement(binary)
        return int(binary, 2)

    def twosComplement(self, immediate: str) -> int:
        '''ref: https://www.adamsmith.haus/python/answers/how-to-take-two's-complement-in-python'''
        immediateBin = '' #Fazer operações bitwise no python é horroroso...
        for b in immediate:
            if b == "0":
                immediateBin += "1"
            else:
                immediateBin += "0"

        immediate = int(immediateBin, 2)

        immediate *=-1
        immediate -= 1
        logI(f"immediate: {immediate}")
        if immediate >= 0:
            raise Error(f"Valor inválido para operação de complemento de dois: {immediate}")
        return immediate

    def translateJType(self, binary):
        opCode = self.getOpCodeJ(binary)
        address = self.generateJLabel(binary[6:])
        return f"{opCode} {address}"

    def getOpCodeJ(self, token:str):
        token = token[0:6]
        if token == '000010':
            return 'j'
        raise Error(f"Comando não reconhecido: {token}")

    def generateJLabel(self, address: str) -> str:
        address = f"0000{address}00"
        logV(f"Endereço recebido: {address}")
        address = int(address, 2)
        address -= 4194304
        address //= 4
        return address