from compiler.dependencies.Error import Error
from compiler.dependencies.Debugger import logE, logW, logI, logD, logV


class Assembly:
    def __init__(self, assemblyCode: str) -> None:
        self.assemblyCode = assemblyCode
        self.labels = self.findAllLabels()
        self.binaryCode = self.GenerateBinary()

    def findAllLabels(self) -> dict:
        ''' Itera todo o código e encontra strings que termina com ':' e adiciona em um dicionário. com o endereço da linha.'''
        labels = {}
        address = 0

        for codeLine in self.assemblyCode:
            codeLine = codeLine.strip()
            if codeLine.endswith(':'):
                labels[codeLine[:-1]] = address
            address += 1
        return labels

    def GenerateBinary(self) -> str:
        binary = ""
        for codeLine in self.assemblyCode:
            codeLine = codeLine.replace(",", "")
            binary += self.translateCommands(codeLine.split())

    ### GETTERS ###

    def getAssemblyCode(self) -> str:
        ## TODO: Transformar listas em string com \n
        codeInString = ""
        for code in self.assemblyCode:
            codeInString += code + "\n"
        return codeInString

    def getBinaryCode(self) -> str:
        return self.binaryCode

    def getHexaCode(self) -> list:
        return self.getBinaryCode()
        # return self.binaryToHexa()


    ######################### TRADUÇÃO BINÁRIO PARA HEXA #########################
    def binaryToHexa(self) -> list:
        hexa = []
        # for i in range(0, len(self.binaryCode), 4):
        #     hexa.append(hex(int(self.binaryCode[i:i+4], 2)))
        return hexa

    ######################### TRADUÇÃO ASSEMBLY PARA BINÁRIO #########################
    def translateCommands(self, commands: list) -> str:  # TODO: Verificar LW e SW
        '''Peneira para as funções de tradução de tipos.'''
        logV(f"Lendo linha: {commands}")
        logV(f"Verificando opCode: {commands[0]}")
        if commands[0] in self.labels or ":" in commands[0]:
            logV("Label encontrada. Retornando vazio.")
            return ""
        match commands[0]:
            case 'or':
                return self.translateRType(commands)
            case 'and':
                return self.translateRType(commands)
            case 'sub':
                return self.translateRType(commands)

            case 'lw':
                return self.translateIType(commands)
            case 'sw':
                return self.translateIType(commands)
            case 'beq':
                return self.translateIType(commands)
            case 'sltiu':
                return self.translateIType(commands)

            case 'j':
                return self.translateJType(commands)

            case _:
                raise Error(
                    f"Comentário indesejado, label, ou linha vazia. {commands}")

                #### J TYPE ####

    def translateJType(self, commands: list) -> str:
        '''[opCode]+[address]'''
        logV(f"Traduzindo J Type: {commands}")
        binary = self.translateOpCode(commands[0])[:2].zfill(6) + self.getJumpAddress(commands[1])[.2:].zfill(26)
        logV(f"Binary tipo J gerado: {binary}")

        return self.binaryVerified(binary)

    def getJumpAddress(self, label: str) -> str:
        return bin(self.consultLabelAddress(label))

    def consultLabelAddress(self, label) -> int:
        return self.labels[label].value

        #### R TYPE ####

    def translateRType(self, commands: list) -> str:
        '''[opCode]+[rd]+[rs]+[rt]+[shamt]+[funct]'''
        logV(f"Traduzindo R Type: {commands}")
        binary = (self.translateOpCode(commands[0], type='R'))[2:].zfill(6)
        binary += self.translateRegister(commands[1])[2:].zfill(5)
        binary += self.translateRegister(commands[2])[2:].zfill(5)
        binary += self.translateRegister(commands[3])[2:].zfill(5)
        binary += self.appendShamt(commands[0])[2:].zfill(5)
        binary += self.appendFunct(commands[0])[2:].zfill(6)
        logV(f"Binary tipo R gerado: {binary}")
        return self.binaryVerified(binary)

    def appendShamt(self, shamtCode: str) -> str:
        logV("Não é necessário setar shamt para as funções suportadas nessa versão. Retornando '0b0'")
        return bin(0)

    def appendFunct(self, functionCode: str) -> str:
        match functionCode:
            case 'or':
                return bin(37)
            case 'and':
                return bin(36)
            case 'sub':
                return bin(34)
            case _:
                raise Error(f"Comando {functionCode} não reconhecido.")
                #### I TYPE ####

    def translateIType(self, commands: list) -> str:
        '''[opCode]+[rs]+[rt]+[immediate]'''
        logV(f"Traduzindo I Type: {commands}")
        binary = self.translateOpCode(str(commands[0]), type='I')[2:].zfill(6)
        binary += self.translateRegister(str(commands[1]))[2:].zfill(5)
        binary += self.translateRegister(str(commands[2]))[2:].zfill(5)
        binary += self.translateImmediate(int(commands[3]))[2:].zfill(16)
        logV(f"Binary tipo I gerado: {binary}")
        return self.binaryVerified(binary)

    def translateImmediate(self, immediate: int) -> str:
        return bin(immediate)[2:].zfill(16)

        #### FUNCTIONS TO SUPPORT TRANSLATION OF ALL TYPES  ####

    def translateOpCode(self, opCode: str, type: chr) -> str:
        if type == 'R':
            match opCode:
                case "or":
                    return bin(0)
                case "and":
                    return bin(0)
                case "sub":
                    return bin(0)
                case _:
                    raise Error(f"Comando {opCode} não reconhecido.")
        elif type == 'I':
            match opCode:
                case "beq":
                    return bin(4)
                case "lw":
                    return bin(35)
                case "sw":
                    return bin(43)
                case "sltiu":
                    return bin(11)
                case _:
                    raise Error(f"Comando {opCode} não reconhecido.")
        elif type == 'J':
            match opCode:
                case "j":
                    return bin(2)
                case _:
                    raise Error(f"Comando {opCode} não reconhecido.")
        else:
            raise Error(f"Tipo {type} não reconhecido. Opcode: {opCode}")

    def binaryVerified(self, binary: bin) -> str:
        if len(binary) > 32:
            raise Error(f"Binary code maior que 32 bits. Valor: {binary}")
        if len(binary) < 32:
            raise Error(f"Binary code menor que 32 bits. Valor: {binary}")
        if not binary.isdigit():
            raise Error(f"Binary code não é um número. Valor: {binary}")
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
            return self.translateRegisterSpecialCases(register)

        logV(f"Traduzindo registrador por tipo. {register[0]}")
        match register[0]:
            case 'v':
                logV("Registrador tipo V")
                return self.translateRegisterV(int(register[1]))
            case 'a':
                logV("Registrador tipo A")
                return self.translateRegisterA(int(register[1]))
            case 't':
                logV("Registrador tipo T")
                return self.translateRegisterT(int(register[1]))
            case 's':
                logV("Registrador tipo S")
                return self.translateRegisterS(int(register[1]))
            case 'k':
                logV("Registrador tipo K")
                return self.translateRegisterK(int(register[1]))
            case _:
                raise Error(f"Registrador ${register} não reconhecido.")

    def translateRegisterSpecialCases(self, register:str) -> str:
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

    # TODO: Verificar valores e checar questão to $t7
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
