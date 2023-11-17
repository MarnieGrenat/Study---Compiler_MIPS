from compiler.dependencies.Error import Error
from compiler.dependencies.Debugger import logE, logW, logI, logD, logV
class Assembly:
    def __init__(self, assemblyCode: str) -> None:
        self.assemblyCode = assemblyCode
        self.labels = self.findAllLabels()
        self.binaryCode = self.generateBinary()
        self.hexCode = self.generateHexa()

    def findAllLabels(self) -> dict:
        ''' Itera todo o código e encontra strings que termina com ':' e adiciona em um dicionário. com o endereço da linha.'''
        labels = {}
        address = 4194304

        for codeLine in self.assemblyCode:
            codeLine = self.tokenize(codeLine)
            firstToken = codeLine[0]
            logV(f"Primeiro token: {firstToken}")
            if str(firstToken).endswith(':') and firstToken[0] != '.':           # é um label!
                labels[firstToken[:-1]] = address
                logV("Label encontrada: " + str(labels))
            else:
                if firstToken[0] != '.':
                    logV('codeline: ' + str(codeLine))
                    address += 4
            if (firstToken[:-1] in labels) and (len(codeLine) > 1):
                logV('codeline: ' + str(codeLine))
                logV("Label com código na mesma linha. Adicionando ao endereço.")
                address += 4
        return labels

    def generateHexa(self) -> str:
        hexa = ""
        binary = self.binaryCode.split("\n")
        binary = [line for line in binary if line]
        for line in binary:
            hexa += hex(int(line, 2)) + "\n"
        return hexa

    def generateBinary(self) -> str:
        binary = ""
        index = 0
        for codeLine in self.assemblyCode:
            index += 1
            tokens = self.tokenize(codeLine, echo=0)
            logV(f"Tokens: {tokens}")
            if ":" in codeLine or "." in codeLine:
                index -= 1
            binary += self.translateTokens(tokens, index)
            binary += "\n"
        logV(f"Binary gerado: {binary}")
        return binary

    def tokenize(self, codeLine: str, echo:bool=0) -> list:
        codeLine = codeLine.replace(",", "")
        tokens = codeLine.split()
        return self.removeCommentariesFromTokens(tokens, echo)

    def removeCommentariesFromTokens(self, tokens, echo:bool=0) -> list:
        if '#' in tokens:
            if echo:
                logV(f"Comentário encontrado. Retirando tokens a partir de #.")
            tokens = tokens[:tokens.index('#')]
        return tokens

    ### GETTERS ###

    def getAssemblyCode(self) -> str:
        codeInString = ""
        for code in self.assemblyCode:
            codeInString += code
        return codeInString

    def getBinaryCode(self) -> str:
        return self.binaryCode

    def getHexaCode(self) -> list:
        return self.generateHexa()

    def translateTokens(self, tokens: list, index:int) -> str:
        '''Peneira para as funções de tradução de tipos.'''
        opCodeToken = tokens[0]
        if opCodeToken[0] == '.':
            logV('Directive encontrado e ignorado com sucesso.')
            return ''
        if opCodeToken[:-1] in self.labels:
            if len(tokens) > 1:
                logV("Label encontrada com código na mesma linha. Retornando código.")
                tokens = tokens[1:]
                opCodeToken = tokens[0]

            else:
                logV("Label encontrada. Retornando vazio.")
                return ''

        logV(f"Verificando opCode: {opCodeToken}")
        if opCodeToken in ['or', 'and', 'sub']:
            return self.generateRType(tokens)
        if opCodeToken in ['lw', 'sw', 'beq', 'sltiu']:
            return self.generateIType(tokens, index)
        if opCodeToken in ['j']:
            return self.generateJType(tokens)
        else:
            raise Error(f"Comentário indesejado, label, ou linha vazia. {tokens}")

    def generateRType(self, token: list) -> str:
        '''[opCode]+[rd]+[rs]+[rt]+[shamt]+[funct]'''
        logV(f"Traduzindo R Type: {token}\n")
        binary = self.translateOpCode(token[0])
        binary += self.translateRegister(token[2])
        binary += self.translateRegister(token[3])
        binary += self.translateRegister(token[1])
        binary += self.appendShamt(token[0])
        binary += self.appendFunct(token[0])
        logV(f"Binary tipo R gerado: {binary}")
        return self.VerifyBinary(binary)

    def generateIType(self, token: list, index:int) -> str:
        '''[opCode]+[rs]+[rt]+[immediate]'''
        logV(f"Traduzindo I Type: {token}\n")
        binary = self.translateOpCode(str(token[0]))

        rsToken = immediateToken = ""
        rtToken = str(token[1])
        if "(" in token[2] and ")" in token[2]:         # LW SW
            rsToken, immediateToken = self.extractTokens(token[2])
        else:                                           # BEQ SLTIU
            rsToken, immediateToken = token[2], token[3]
            if token[0] == 'beq':
                rsToken, rtToken = token[1], token[2]
                immediateToken = self.countOperations(token, index)
                opCode = self.translateOpCode(str(token[0]))
                rs = self.translateRegister(rsToken)
                rt = self.translateRegister(rtToken)

                binary = f"{opCode}{rs}{rt}{immediateToken}"
                logI(f"Binary tipo I gerado:\n{opCode} {rs} {rt} {immediateToken}")
                return self.VerifyBinary(binary)
            else:
                rsToken, rtToken = token[2], token[1]

        binary += self.translateRegister(rsToken)
        binary += self.translateRegister(rtToken)
        binary += self.translateImmediate(immediateToken)
        logV(f"Binary tipo I gerado: {binary}")
        return self.VerifyBinary(binary)

    def extractTokens(self, token: str) -> tuple:
        try:
            immediate = token.split('(')[0]
            rs = token.split('(')[1].split(')')[0]
            logI(f"rs: {rs}, immediate: {immediate}")
            return rs, int(immediate)
        except IndexError:
            raise Error("Erro ao tentar extrair os tokens dentro e fora dos parênteses.")

    def countOperations(self, token: list, index:int) -> str:
        logV(f"Token: {token} Index: {index}")

        Labeltoken = self.consultLabelAddress(token[-1])
        Labeltoken -= 4194304
        Labeltoken //= 4
        logV(f"Labeltoken: {Labeltoken}, index: {index}")
        immediate = Labeltoken - (index)
        try:
            if int(immediate) < 0:
                logE(f"Passei aqui, immediate: {immediate}")
                return self.TwoComplement(immediate)
        except ValueError:
            raise Error(f"Label Immediate {immediate} não reconhecido.")
        return self.first16Bits(bin(immediate))

    def generateJType(self, token: list) -> str:
        '''[opCode]+[address]'''
        logV(f"Traduzindo J Type: {token}\n")
        opCode = self.translateOpCode(token[0])
        jumpAddress = self.getJumpAddress(token[1])
        binary = f"{opCode}{jumpAddress}"
        logV(f"Binary tipo J gerado: {binary}")
        return self.VerifyBinary(binary)

    def getJumpAddress(self, label: str) -> str:
        jumpAddr = bin(self.consultLabelAddress(label))
        logV(f"Retornando Label's Addr.{jumpAddr}")
        return self.first26Bits(jumpAddr)

    def consultLabelAddress(self, label: str) -> int:
        logI(f"Labels: {self.labels}")
        if label not in self.labels:
            raise Error(f"Label {label} não encontrado.")
        return self.labels[label]

    def appendShamt(self, shamtCode: str) -> str:
        logV("Não é necessário setar shamt para as funções suportadas nessa versão. Retornando '0b0'")
        #logV(f"ShamtCode: {shamtCode}")
        return '00000'

    def appendFunct(self, functionCode: str) -> str:
        match functionCode:
            case 'or':
                logV(f"Função OR encontrada. Retornando bin: {self.first6Bits(bin(37))}")
                return self.first6Bits(bin(37))
            case 'and':
                logV(f"Função AND encontrada. Retornando bin: {self.first6Bits(bin(36))}")
                return self.first6Bits(bin(36))
            case 'sub':
                logV(f"Função SUB encontrada. Retornando bin: {self.first6Bits(bin(34))}")
                return self.first6Bits(bin(34))
            case _:
                raise Error(f"Comando {functionCode} não reconhecido.")
                #### I TYPE ####

    def translateImmediate(self, immediate) -> str:
        # verificar se tem palavras dentro da string
        logV(f"Traduzindo immediate: {immediate}")
        logV(f"Type: {type(immediate)}")
        if immediate in self.labels:
            immediate = self.labels[immediate] - 4194304 # A partir do endereço 0x400000
            logV(f"Immediate encontrado no mapeamento de labels. Retornando valor: {self.first16Bits(bin(immediate))}")
            return self.first16Bits(bin(immediate))
        try:
            if int(immediate) < 0:
                logE(f"Passei aqui, immediate: {immediate}")
                return self.TwoComplement(immediate)
            immediate = int(immediate)
        except ValueError:
            raise Error(f"Label Immediate {immediate} não reconhecido.")

        if isinstance(immediate, int):
            logV(f"Immediate: {bin(immediate)}")
            logV(f"Immediate é um número. Retornando valor: {self.first16Bits(bin(immediate))}")
            return self.first16Bits(bin(immediate))
        else:
            raise Error(f"Valor Immediate {immediate} não reconhecido.")
        #### FUNCTIONS TO SUPPORT TRANSLATION OF ALL TYPES  ####

    def TwoComplement(self, immediate: int) -> str:
        '''ref: https://www.adamsmith.haus/python/answers/how-to-take-two's-complement-in-python'''
        if immediate > 0:
            raise Error(f"Valor inválido para operação de complemento de dois: {immediate}")
        immediate *=-1
        immediate -= 1

        immediateBin = ''
        immediate = bin(immediate)[2:].zfill(16)
        logI("Complemento de dois encontrado. Invertendo bits. \n {immediate}")

        for bit in immediate:
            if bit == "0":
                immediateBin += "1"
            else:
                immediateBin += "0"

        logI(f"immediate Complemento: {immediateBin}")
        return immediateBin

    def translateOpCode(self, opCode: str) -> str:
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
        if opCode in opCodeMapping:
            logV(f"OpCode encontrado no mapeamento. Retornando valor: {self.first6Bits(opCodeMapping[opCode])}")
            return self.first6Bits(opCodeMapping[opCode])
        raise Error(f"Comando {opCode} não reconhecido.")

    def VerifyBinary(self, binary: bin) -> str:
        if len(binary) > 32:
            raise Error(f"Binary code maior que 32 bits. Valor: {binary}. Hex: {hex(int(binary, 2))}")
        if len(binary) < 32:
            raise Error(f"Binary code menor que 32 bits. Valor: {binary}. Hex: {hex(int(binary, 2))}")
        if not binary.isdigit():
            raise Error(f"Binary code não é um número. Valor: {binary}. Hex: {hex(int(binary, 2))}")
        return binary

    #### Registradores ####
    def translateRegister(self, register: str) -> str:
        # treat register
        logV(f"Traduzindo registrador: {register}")
        if register[0] != "$":
            raise Error(f"Registrador {register} não reconhecido.")
        register = register.replace("$", "")

        # translate register
        if register.isdigit():
            return self.first5Bits(bin(int(register)))

        if register in ['zero', 'at', 'gp', 'sp', 'fp', 'ra']:
            registerBin = self.first5Bits(self.translateRegisterSpecialCases(register))
            logV(f'Registrador especial encontrado. {registerBin}.')
            return registerBin
        registerBin = ""
        match register[0]:
            case 'v':
                logV("Registrador tipo V")
                registerBin = self.registerTypeV(int(register[1]))
            case 'a':
                logV("Registrador tipo A")
                registerBin = self.registerTypeA(int(register[1]))
            case 't':
                logV("Registrador tipo T")
                registerBin = self.registerTypeT(int(register[1]))
            case 's':
                logV("Registrador tipo S")
                registerBin = self.registerTypeS(int(register[1]))
            case 'k':
                logV("Registrador tipo K")
                registerBin = self.registerTypeK(int(register[1]))
            case _:
                raise Error(f"Registrador ${register} não reconhecido.")
        logV(f"Registrador traduzido: {self.first5Bits(registerBin)}")
        return self.first5Bits(registerBin)

    def translateRegisterSpecialCases(self, register: str) -> str:
        match register:
            case 'zero':
                return bin(0)
            case 'at':
                return bin(1)
            case 'gp':
                return bin(28)
            case 'sp':
                return bin(29)
            case 'fp':
                return bin(30)
            case 'ra':
                return bin(31)
            case _:
                raise Error(
                    f"Registrador especial {register} não reconhecido.")

    def registerTypeV(self, register: int) -> str:
        registerValue = 2 + self.verifyRegister(register, maxValue=1)
        return bin(registerValue)

    def registerTypeA(self, register: int) -> str:
        registerValue = 4 + self.verifyRegister(register, maxValue=3)
        return bin(registerValue)

    def registerTypeT(self, register: int) -> str:
        if (register <= 7 and register >= 0):
            return bin(8 + self.verifyRegister(register, maxValue=7))
        return bin(16 + self.verifyRegister(register, maxValue=9, minValue=8))

    def registerTypeS(self, register: int) -> str:
        registerValue = 16 + self.verifyRegister(register, maxValue=6)
        return bin(registerValue)

    def registerTypeK(self, register: int) -> str:
        registerValue = 26 + self.verifyRegister(register, maxValue=1)
        return bin(registerValue)

    def verifyRegister(self, register: int, maxValue: int, minValue: int = 0) -> int:
        if (register > maxValue) or (register < minValue):
            raise Error(f"Registrador não permitido! Valor: {register}")
        return register

    def first6Bits(self, binary: str) -> str:
        return binary[2:].zfill(6)
    def first5Bits(self, binary: str) -> str:
        return (binary[2:]).zfill(5)
    def first16Bits(self, binary: str) -> str:
        return binary[2:].zfill(16)
    def first26Bits(self, binary: str) -> str:
        logI(f"BIN ADDR gerado: {'0000'+binary[2:]+'00'}")
        address = binary[2:].zfill(32)
        logI(f"address gerado: {address[4:-2]}")
        return address[4:-2]