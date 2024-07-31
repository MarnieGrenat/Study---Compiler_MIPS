from dependencies.Error import Error
from dependencies.Debugger import logE, logW, logI, logD, logV
from dcompiler.Binary import *


class Hex:
    def __init__(self, code: str, fileName: str = 'hex_output') -> None:
        self.fileName = fileName
        self.hexCode = code
        self.labels = []
        self.binaryCode = GenerateBinary(self.hexCode)
        self.assembly = self.GenerateAssembly(self.binaryCode)



    def Decompile(self) -> str:
        return self.getAssemblyCode()

    def GenerateAssembly(self, binaryList:list) -> str:
        ## TODO: Tratar sinal de Jump ou BEQ
        assembly = ""
        for binary in binaryList:
            type = self.guessTokenType(binary)
            aux = self.getAllTokens(type, binary) + "\n"
            assembly += aux
        logI(f"Assembly base: {assembly}")
        aux = self.treatAddresses(assembly)

        return ".text:\n\nmain:\n" + aux

    def treatAddresses(self, assembly:str) -> str:
        assembly = assembly.splitlines()
        for line in assembly:
            logI(f"Tratando linha: {line}")
            if 'j' in line:
                assembly = self.generateLabels(assembly, line, 'j')
            elif 'beq' in line:
                assembly = self.generateLabels(assembly, line, 'beq')
        aux = ""
        for line in assembly:
            aux += line + "\n"
        return aux

    def generateLabels(self, assembly:list, line:str, cType:str) -> list:
        labelAddr = int(line.split()[-1])
        logI(f"Endereço do label: {labelAddr}")
        logI(f"Assembly: \n{assembly}")

        if cType == 'beq':
            index = assembly.index(line)
            if ':' in assembly[index + labelAddr + 1]:
                labelName = assembly[index+labelAddr+1].split()[0]
                labelName = labelName[:-1]
                logI(f"Label BEQ já existe: {assembly[index + labelAddr + 1]}")
            else:
                logI(f'Label BEQ não existe.')
                labelName = 'L' + str(len(self.labels))
            return self.__setLabel(assembly, line, labelAddr, labelName, 'beq')

        elif cType == 'j':
            if labelAddr < len(assembly):
                if ':' in assembly[labelAddr]:
                    labelName = assembly[labelAddr].split()[0]
                    labelName = labelName[:-1]
                    logI(f"Label J já existe: {assembly[labelAddr]}")
                else:
                    logI(f'Label J não existe.')
                    labelName = 'L' + str(len(self.labels))
            else:
                assembly.append("")
            labelName = 'L' + str(len(self.labels))
            return self.__setLabel(assembly, line, labelAddr, labelName, 'j')
        else:
            raise Error(f"Tipo de jump não reconhecido: {cType}")
    def __setLabel(self, assembly:list, line:str, labelAddr:int, labelName:str, cType:str) -> list:
        logI(assembly)
        logI(f"Tipo {type(assembly)} Linha: {line}")
        if labelName not in self.labels:
            self.labels.append(labelName)
        index = 0
        if cType == 'j':
            logV("Tipo J encontrado!")
            index = assembly.index(line)
            line = line.split()
            assembly[index] = f"{line[0]} {labelName}"    # Renomeando a linha

            if labelName not in assembly[labelAddr]:
                assembly[labelAddr] = f"{labelName}: {assembly[labelAddr]}" # adicionando o labelname no final da linha

        elif cType == 'beq':
            logV("Tipo BEQ encontrado!")
            index = assembly.index(line)
            line = line.split()
            logI(f"1: {line[0]} | 2: {line[1]} | 3: {line[2]} | 4: {line[3]}")
            if line[0] == 'beq':
                assembly[index] = f"{line[0]} {line[1]} {line[2]} {labelName}"    # Renomeando a linha
            else:
                assembly[index] = f"{line[0]} {line[1]} {line[2]} {line[3]} {labelName}"

            labelAddr = index+labelAddr+1
            if labelName not in assembly[labelAddr]:
                assembly[labelAddr] = f"{labelName}: {assembly[labelAddr]}" # adicionando o labelname no final da linha

        else:
            raise Error(f"Tipo de jump não reconhecido: {cType}")
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
        # TODO ARRUMAR ADDR
        address -= 4194304
        address //= 4
        return address