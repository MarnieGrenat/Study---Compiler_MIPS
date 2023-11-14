from Error import Error
from Debugger import logD, logE, logI, logV, logW


class Hex:
    def __init__(self, hexCode: str) -> None:
        self.binaryCode = self.generateBinary()
        self.hexCode = hexCode
        self.assembly = self.generateAssembly()
        self.labels = []

    def generateBinary(self) -> list:
        binary = []
        for hexLine in self.hexCode:
            binary.append(self.hexToBin(hexLine))
        return binary

    def hexToBin(line: str) -> str:
        line = bin(int(line, 16))
        line = line[2:].zfill(32)
        return str(line)

    def generateAssembly(self) -> str:
        assembly = ""
        for binary in self.binary:
            opCode = self.generateOpCode(binary)
            assembly += self.translateCommand(opCode, binary)
            assembly += "\n"
        return assembly

    ### GETTERS ###

    def getBinaryCode(self) -> list:
        return self.binaryCode

    def getHexCode(self) -> str:
        return self.hexCode

    def getAssemblyCode(self) -> str:
        return self.assemblyCode

    def generateOpcode(self, binary: str) -> str:
        token = self.binary[0:6]

        opCodeMapping = {
            '000000': 'or',
            '000000': 'and',
            '000000': 'sub',

            '000100': 'beq',
            '100011': 'lw',
            '101011': 'sw',
            '001011': 'sltiu',

            '000010': 'j'
        }
        if token in opCodeMapping:
            logV(
                f"OpCode encontrado no mapeamento. Retornando valor: {self.first6Bits(opCodeMapping[token])}")
            return opCodeMapping[token]
        raise Error(f"Comando {token} não reconhecido.")

    def translateCommand(self, opCode: str, binary: str) -> str:
        if opCode in ['or', 'and', 'sub']:
            return self.translateRType(binary)
        if opCode in ['beq', 'lw', 'sw', 'sltiu']:
            return self.translateIType(binary, opCode)
        if opCode in ['j']:
            return self.translateJType(binary)

    def translateRType(self, binary) -> str:
        opCode = self.generateOpCodeR(binary)
        rs = self.generateRegister(binary, 0)
        rt = self.generateRegister(binary, 1)
        rd = self.generateRegister(binary, 2)
        line = f"{opCode}, {rs}, {rt}, {rd}"
        return line

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
        registerBinary = self.getRegisterPosition(binary, position)
        return self.tokenizeRegister(registerBinary)

    def getRegisterPosition(binary: str, position: int):
        match position:
            case 0:
                return binary[7:11]
            case 1:
                return binary[11:16]
            case 2:
                return binary[16:21]

    def tokenizeRegister(self, register: str) -> str:
        token = "$" + int(register, 2)
        return token

    def generateOpCodeI(self, binary: str, CommandType: str):
        if CommandType in ['lw', 'sw']:
            return self.generateBracketsFormat(binary)
        if CommandType in ['beq', 'sltiu']:
            return self.generateImmediateFormat(binary)

    def generateBracketsFormat(self, binary: str) -> str:
        '''OP rt,offset(rs)'''
        opCode = self.getOpCodeI(binary[0:6])
        rs = self.generateRegister(binary, 1)
        rt = self.generateRegister(binary, 0)
        offset = int(binary[16:], 2)
        line = f"{opCode}, {rt}, {offset}({rs})"
        return line

    def generateImmediateFormat(self, binary) -> str:
        '''OP rs,rt,imm'''
        line = ''
        opCode = self.getOpCodeI(binary[0:6])
        rs = self.generateRegister(binary, 0)
        rt = self.generateRegister(binary, 1)
        imm = int(binary[16:], 2)

        if opCode == 'beq':  # TODO: Gerar Label
            self.generateLabel(binary[16:])
            offset  = self.getImmediateRelativeAddr(binary[16:])
            line = f"{opCode}, {rs}, {rt}, {offset}"

        elif opCode == 'sltiu':
            imm = int(imm, 2)
            line = f"{opCode}, {rt}, {rs}, {imm}"
        else:
            raise Error(f"Comando não reconhecido.{binary}")

        return line
    def getImmediateRelativeAddr(self, binary: str) -> dict:
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

    def TranslateJType(self, binary):
        opCode = self.getOpCodeJ(binary[0:6])
        address = self.generateJLabel(int(binary[6:], 2))
        return f"{opCode}, {address}"

