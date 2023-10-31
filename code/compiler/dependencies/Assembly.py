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
        if codeLine[0] == "#":
            return []
        if codeLine[-1] == ":":
            # self.getLabel(codeLine)
            return []
        codeLine = codeLine.replace(",", "")
        commands = codeLine.split()
        # TODO: Tratamento de erros
        return list(commands)

    def translateCommands(self, commands:list) -> bin:
        if commands[0] in ['or', 'and', 'sub', 'sltiu']: # Imediato ou com registradores?
            return self.translateRType(commands)
        elif commands[0] in ['lw', 'sw', 'beq']:
            return self.translateIType(commands)
        elif commands[0] in ['j']:
            return self.translateJType(commands)
        else:
            if (commands[0][0] != '#' and commands[0][-1] != ':'): 				# Se não começa com # ou se não termina com :
                logE(f"Erro na linha {commands}. Comando {commands[0]} não reconhecido.")

    def translateJType(self, commands:list) -> str:
        # [opCode]+[address]
        if commands[0] == 'j':
            binary = '000100'
            self.getJumpAddress(commands[1])
        else:
            logE("Comando {commands} não reconhecido.")
            binary = '-1'
            
        return binary

    def getJumpAddress(self, label:list) -> bin:
        return self.consultLabelAddress(label)
    
    def consultLabelAddress(self, label) -> str:
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

    def translateIType(self, commands:list) -> bin:#
        # [opCode]+[rs]+[rt]+[immediate]
        binary = self.translateOpCode(commands[0])
        binary += self.translateRegister(commands[1])
        binary += self.translateRegister(commands[2])
        binary += self.translateImmediate(commands[3])
        return binary

    def translateOpCode(self, opCode:str) -> bin:
        pass

    def translateRegister(self, register:str) -> str:
        if register[0] != "$":
            logE(f"Registrador {register} não reconhecido.")
            return '-1'
        #verify if is number
        register = register.replace("$", "")
        if register.isdigit():
            return str(bin(int(register)))[2:].zfill(5)
        elif register in ['zero', 'at', 'gp', 'sp', 'fp', 'ra']:
            return self.translateRegisterSpecialCases(register)
        elif register[0] == 'v':
            return self.translateRegisterV(register)
        elif register[0] == 'a':
            return self.translateRegisterA(register)
        elif register[0] == 't':
            return self.translateRegisterT(register)
        elif register[0] == 's':
            return self.translateRegisterS(register)
        elif register[0] == 'k':
            return self.translateREgisterK(register)
        else:
            logE(f"Registrador {register} não reconhecido.")
            return '-1'
            
        pass
    
    
    def appendShamt(self, opCode:str, shamt:str) -> str:
        return '00000'

    def appendFunct(self, opCode:str) -> str:
        if opCode == 'or':
            binary = '100101'
        elif opCode == 'and':
            binary = '100100'
        elif opCode == 'sub':
            binary = '100010'
        else:
            logE("Comando {opCode} não reconhecido.")
            binary = '-1'
        return binary

    def translateImmediate(self, immediate:str) -> bin:
        return bin(immediate)





