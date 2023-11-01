from Error import Error
from Debugger import logE, logW, logI, logD, logV

'''
R-Type - OR, AND, SUB
I-Type - LW, SW, SLTIU, BEQ
J-Type - J
'''

class Assembly:
    def __init__(self, assemblyCode:str) -> None:
        self.assemblyCode = self.cleanAssemblyCode()
        self.labels = self.findAllLabels()
        self.binaryCode = self.GenerateBinary()

    def findAllLabels(self) -> dict:
        '''Encontra todos os labels do código assembly e os retorna em um dicionário.'''
        labels = {}
        for codeLine in self.assemblyCode:
            if codeLine[-1] == ':':
                labels[codeLine[:-1]] = self.getCommandAddress(codeLine)
        return labels

    def GenerateBinary(self) -> str:
        '''Gera o código binário a partir do código assembly.'''
        binary = ""
        for codeLine in self.assemblyCode:
            commands = self.breakLineIntoCommands(codeLine)
            binary+= self.translateCommands(commands)

    ### GETTERS ###

    def getAssemblyCode(self) -> str:
        return self.assemblyCode

    def getBinaryCode(self) -> str:
        return self.binaryCode

    # Não vou produzir setters, já que não pretendo dar liberdade de gerar assembly ou binário sem ser pelo construtor.

    def breakLinesIntoCommands(self, codeLine:str) -> list:
        '''
        Essa função será depreciada, já que pretendo fazer uma limpar o assembly previamente e iterar o arquivo
        da direita para esquerda, não necessitando dessa função.
        '''
        if codeLine[0] == "#":
            return []
        if codeLine[-1] == ":":
            # self.getLabel(codeLine)
            return []
        codeLine = codeLine.replace(",", "")
        commands = codeLine.split()
        # TODO: Tratamento de erros
        return list(commands)

    ######################### TRADUÇÃO ASSEMBLY PARA BINÁRIO #########################

    def translateCommands(self, commands:list) -> str:                          #TODO: Verificar LW e SW
        logV(f"Lendo linha: {commands}")
        logV(f"Verificando opCode: {commands[0]}")
        if commands[0] in ['or', 'and', 'sub']: # Imediato ou com registradores?
            return self.translateRType(commands)                                # [opCode]+[rd]+[rs]+[rt]+[shamt]+[funct]
        elif commands[0] in ['lw', 'sw', 'beq', 'sltiu']:
            return self.translateIType(commands)                                # [opCode]+[rs]+[rt]+[immediate]
        elif commands[0] in ['j']:
            return self.translateJType(commands)                                # [opCode]+[address]
        else:
            if (commands[0][0] != '#' and commands[0][-1] != ':'): 				# Se não começa com # ou se não termina com :
                raise Error(f"Comando {commands[0]} não reconhecido.")
            raise Error(f"Comentário indesejado, label, ou linha vazia. {commands}")



    def translateJType(self, commands:list) -> str:
        # [opCode]+[address]
        if commands[0] == 'j':
            return '000100' + self.getJumpAddress(commands[1])
        else:
            raise Error(f"Comando {commands} não reconhecido.")

    def getJumpAddress(self, label:list) -> bin:
        return self.consultLabelAddress(label)

    def consultLabelAddress(self, label) -> str:                                        #TODO: Iterar lista e pegar todos labels; Adicionar labels em DICT {label:address}
        return self.labels[label]

    def translateRType(self, commands:list) -> bin:
        # [opCode]+[rd]+[rs]+[rt]+[shamt]+[funct]
        binary = self.translateOpCode(commands[0])
        binary += self.translateRegister(commands[1])
        binary += self.translateRegister(commands[2])
        binary += self.translateRegister(commands[3])
        binary += self.appendShamt(commands[0])
        binary += self.appendFunct(commands[0])
        return binary

    def translateIType(self, commands:list) -> bin:
        # [opCode]+[rs]+[rt]+[immediate]
        binary = self.translateOpCode(commands[0])
        binary += self.translateRegister(commands[1])
        binary += self.translateRegister(commands[2])
        binary += self.translateImmediate(commands[3])
        return binary

    def translateOpCode(self, opCode:str) -> bin:                                       #TODO: Traduzir OpCode
        if opCode in ['or', 'and', 'sub']:                                              # R-Type - OR, AND, SUB
            return 0b000000[2:].zfill(5)
        if opCode == 'beq':                                                             # I-Type - LW, SW, SLTIU, BEQ
            return 0b000010[2:].zfill(5)
        if opCode in ['lw', 'sw']:                                                      # I-Type - LW, SW, SLTIU, BEQ
            return 0b100011[2:].zfill(5)
        if opCode in ['sltiu']:                                                         # I-Type - LW, SW, SLTIU, BEQ
            return 0b001011[2:].zfill(5)
        if opCode == 'j':                                                               # J-Type - J
            return 0b000010[2:].zfill(5)


    def appendShamt(self, opCode:str, shamt:str) -> bin:
        logV("Não é necessário setar shamt.. retornando '00000'")
        return 0b00000[2:].zfill(5)


    def appendFunct(self, opCode:str) -> bin:
        if opCode == 'or':
            binary = 0b100101
        elif opCode == 'and':
            binary = 0b100100
        elif opCode == 'sub':
            binary = 0b100010
        else:
            raise Error(f"Comando {opCode} não reconhecido.")
            binary = 0b111111
        return binary[2:].zfill(5)

    def translateImmediate(self, immediate:str) -> bin:
        return bin(immediate)

    def translateRegister(self, register:str) -> bin:
        if register[0] != "$":
            raise Error(f"Registrador {register} não reconhecido.")
            return '-1'
        #verify if is number
        register = register.replace("$", "")
        if register.isdigit():
            return str(bin(int(register)))[2:].zfill(5)
        elif register in ['zero', 'at', 'gp', 'sp', 'fp', 'ra']:
            return self.translateRegisterSpecialCases(register)
        elif (int(register[1]) < 0):
            raise Error(f"Registrador ${register} não reconhecido.")
        else:
            if register[0] == 'v':
                return self.translateRegisterV(register[1])
            if register[0] == 'a':
                return self.translateRegisterA(register[1])
            if register[0] == 't':
                return self.translateRegisterT(register[1])
            if register[0] == 's':
                return self.translateRegisterS(register[1])
            if register[0] == 'k':
                return self.translateRegisterK(register[1])
            else:
                raise Error(f"Registrador ${register} não reconhecido.")
    def translateRegisterSpecialCases(self, register) -> bin:
        if register == 'zero':
            return bin(0)[2:].zfill(5)
        if register == 'at':
            return bin(1)[2:].zfill(5)
        if register == 'gp':
            return bin(28)[2:].zfill(5)
        if register == 'sp':
            return bin(29)[2:].zfill(5)
        if register == 'fp':
            return bin(30)[2:].zfill(5)
        if register == 'ra':
            return bin(31)[2:].zfill(5)

    def translateRegisterV(self, register:int) -> bin:
        if int(register > 1):
            raise Error(f"Registrador não permitido! Valor: {register}")

        aux = 2 + int(register)
        return bin(aux)[2:].zfill(5)

    def translateRegisterA(self, register:int) -> bin:
        if int(register > 3):
            raise Error(f"Registrador não permitido! Valor: {register}")

        aux = 4 + int(register)
        return bin(aux)[2:].zfill(5)

    def translateRegisterT(self, register:int) -> bin:                                  #TODO: Verificar valores e checar questão to $t7
        if (register < 8):
            aux =  8 + int(register)
        elif register > 6 and register < 10:
            aux = 16 + int(register)

        else:
            raise Error(f"Registrador ${register} não reconhecido.")
        return bin(aux)[2:].zfill(5)

    def translateRegisterS(self, register:int) -> bin:
        if int(register > 6):
            raise Error(f"Registrador não permitido! Valor: {register}")

        aux = 16 + int(register)
        return bin(aux)[2:].zfill(5)

    def translateRegisterK(self, register:int) -> bin:
        if int(register > 1):
            raise Error(f"Registrador não permitido! Valor: {register}")

        aux = 26 + int(register)
        return bin(aux)[2:].zfill(5)
