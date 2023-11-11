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
        address = 4194304 - 4    # Para compensar o incremento do endereço no primeiro loop

        for codeLine in self.assemblyCode:
            codeLine = codeLine.strip()
            if codeLine.endswith(':'):
                labels[codeLine] = hex(address)
                logV("Label encontrada: " + str(labels))
            address += 4
        return labels

    def generateHexa(self) -> str:
        hexa = ""
        for codeLine in self.assemblyCode:
            logV(f"Code line: {codeLine}")
            tokens = self.tokenize(codeLine)
            logV(f"Tokens: {tokens}")

            binary = self.translateTokens(tokens)
            if binary != '':
                hexLine = hex(int(binary, 2))
                hexa += hexLine
                hexa += "\n"
                logV(f"Hex gerado: {hex}")
            else:
                logV("Linha vazia. Não adicionando ao hex.")
        return hexa

    def generateBinary(self) -> str:
        binary = ""
        for codeLine in self.assemblyCode:
            tokens = self.tokenize(codeLine)
            logV(f"Tokens: {tokens}")

            binary += self.translateTokens(tokens)
            logV(f"Binary gerado: {binary}")
            # binary to hex
            binary += "\n"
        return binary

    def tokenize(self, codeLine: str) -> list:
        codeLine = codeLine.replace(",", "")
        tokens = codeLine.split()
        return self.removeCommentariesFromTokens(tokens)

    def removeCommentariesFromTokens(self, tokens) -> list:
        if '#' in tokens:
            logV(f"Comentário encontrado. Retirando tokens a partir de #.")
            tokens = tokens[:tokens.index('#')]
        return tokens

    ### GETTERS ###

    def getAssemblyCode(self) -> str:
        codeInString = ""
        for code in self.assemblyCode:
            codeInString += code + "\n"
        return codeInString

    def getBinaryCode(self) -> str:
        return self.binaryCode

    def getHexaCode(self) -> list:
        return self.generateHexa()

    def translateTokens(self, tokens: list) -> str:  # TODO: Verificar LW e SW
        '''Peneira para as funções de tradução de tipos.'''
        opCodeToken = tokens[0]
        logV(f"Verificando opCode: {opCodeToken}")
        if opCodeToken in self.labels:
            logV("Label encontrada. Retornando vazio.")
            return ""
        if opCodeToken in ['or', 'and', 'sub']:
            return self.generateRType(tokens)
        if opCodeToken in ['lw', 'sw', 'beq', 'sltiu']:
            return self.generateIType(tokens)
        if opCodeToken in ['j']:
            return self.generateJType(tokens)
        else:
            raise Error(f"Comentário indesejado, label, ou linha vazia. {tokens}")

    def generateJType(self, token: list) -> str:
        '''[opCode]+[address]'''
        logV(f"Traduzindo J Type: {token}\n")
        opCode = self.translateOpCode(token[0])
        jumpAddress = self.getJumpAddress(token[1])
        binary = opCode + jumpAddress
        logV(f"Binary tipo J gerado: {binary}")

        return self.VerifyBinary(binary)

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

    def generateIType(self, token: list) -> str:
        '''[opCode]+[rs]+[rt]+[immediate]'''
        logV(f"Traduzindo I Type: {token}\n")
        binary = self.translateOpCode(str(token[0]))
        binary += self.translateRegister(str(token[2]))
        binary += self.translateRegister(str(token[1]))
        binary += self.translateImmediate(int(token[3]))
        logV(f"Binary tipo I gerado: {binary}")
        return self.VerifyBinary(binary)

    def getJumpAddress(self, label: str) -> str:
        logV(f"Retornando Label's Addr.{bin(self.consultLabelAddress(label))}")
        jumpAddr = bin(self.consultLabelAddress(label))
        return self.first26Bits(jumpAddr)

    def consultLabelAddress(self, label) -> int:
        return self.labels[label].value

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

    def translateImmediate(self, immediate: int) -> str:
        logV(f"Traduzindo immediate: {immediate}")
        logV(f"Binário do immediate: {bin(immediate)}")
        return self.first16Bits(bin(immediate))

        #### FUNCTIONS TO SUPPORT TRANSLATION OF ALL TYPES  ####

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
            return str(bin(int(register)))

        if register in ['zero', 'at', 'gp', 'sp', 'fp', 'ra']:
            registerBin = self.first5Bits(self.translateRegisterSpecialCases(register))
            logV(f'Registrador especial encontrado. {registerBin}.')
            return registerBin
        registerBin = ""
        match register[0]:
            case 'v':
                logV("Registrador tipo V")
                registerBin = self.translateRegisterV(int(register[1]))
            case 'a':
                logV("Registrador tipo A")
                registerBin = self.translateRegisterA(int(register[1]))
            case 't':
                logV("Registrador tipo T")
                registerBin = self.translateRegisterT(int(register[1]))
            case 's':
                logV("Registrador tipo S")
                registerBin = self.translateRegisterS(int(register[1]))
            case 'k':
                logV("Registrador tipo K")
                registerBin = self.translateRegisterK(int(register[1]))
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

    def translateRegisterV(self, register: int) -> str:
        registerValue = 2 + self.verifyRegister(register, maxValue=1)
        return bin(registerValue)

    def translateRegisterA(self, register: int) -> str:
        registerValue = 4 + self.verifyRegister(register, maxValue=3)
        return bin(registerValue)

    def translateRegisterT(self, register: int) -> str:
        if (register <= 7 and register >= 0):
            return bin(8 + self.verifyRegister(register, maxValue=7))
        return bin(24 + self.verifyRegister(register, maxValue=9, minValue=8))

    def translateRegisterS(self, register: int) -> str:
        registerValue = 16 + self.verifyRegister(register, maxValue=6)
        return bin(registerValue)

    def translateRegisterK(self, register: int) -> str:
        registerValue = 26 + self.verifyRegister(register, maxValue=1)
        return bin(registerValue)

    def verifyRegister(self, register: int, maxValue: int, minValue: int = 0) -> int:
        if (register > maxValue) or (register < minValue):
            raise Error(f"Registrador não permitido! Valor: {register}")
        return register

    def first6Bits(self, binary: str) -> str:
        return binary[2:].zfill(6)
    def first5Bits(self, binary: str) -> str:
        return binary[2:].zfill(5)
    def first16Bits(self, binary: str) -> str:
        return binary[2:].zfill(16)
    def first26Bits(self, binary: str) -> str:
        return binary[2:].zfill(26)