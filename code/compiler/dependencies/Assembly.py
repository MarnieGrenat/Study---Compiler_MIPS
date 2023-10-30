from Debugger import logE, logW, logI, logD, logV

class Assembly:
    def __init__(self, assemblyCode:str) -> None:
        self.assemblyCode = assemblyCode
        self.labels = self.getLabels()
        self.binaryCode = self.GenerateBinary()


    ### GETTERS ###
    def getAssemblyCode(self) -> str:
        return self.assemblyCode

    def getBinaryCode(self) -> str:
        return self.binaryCode

    # Não vou produzir setters, já que não pretendo dar liberdade de gerar assembly ou binário sem ser pelo construtor.

    def GenerateBinary(self) -> str:
        '''Gera o código binário a partir do código assembly.'''
        binary = ""
        for codeLine in self.assemblyCode:
            commands = self.breakLineIntoCommands(codeLine)
            binary+= self.translateCommands(commands)

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

    def translateJType(self, commands:list) -> bin:
        # [opCode]+[address]
        if commands[0] == 'j':
            return self.translateInconditionalJump(commands)
        elif commands[0] == 'beq':
            return self.translateConditionalJump(commands)

    def translateInconditionalJump(self, command:list) -> bin:
        pass

    def translateConditionalJump(self, command:list) -> bin:
        pass

    def translateRType(self, commands:list) -> bin:
        # [opCode]+[rd]+[rs]+[rt]+[shamt]+[funct]
        binary = self.translateOpCode(commands[0])
        binary += self.translateRegister(commands[1])
        binary += self.translateRegister(commands[2])
        binary += self.translateRegister(commands[3])
        binary += self.translateShamt(commands[4])
        binary += self.translateFunct(commands[5])
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

    def translateRegister(self, register:str) -> bin:
        pass
    def traslateShamt(self, shamt:str) -> bin:
        pass

    def translateFunct(self, function:str) -> bin:
        pass

    def translateImmediate(self, immediate:str) -> bin:
        pass





