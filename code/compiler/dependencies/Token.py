from Error import Error
class Assembly_Token:
    def __init__(self, token:str, type:int):
        self.token = token
        self.type = type
        self.translation = self.generateTokenTranslation(self.type)

    def Token(self) -> str:
        return self.token

    def Type(self) -> int:
        return self.type

    def TypeStr(self) -> str:
        match self.type:
            case 0:
                return "OpCode"
            case 1:
                return "Register"
            case 2:
                return "Immediate"
            case 3:
                return "Label"
            case _:
                return "ERROR"

    def generateTokenTranslation(self) -> str:
        match self.type:
            case 0:
                return self.generateOpcode()
            case 1:
                return self.generateRegister()
            case 2:
                return self.generateImmediate()
            case 3:
                return "LABEL"
            case _:
                return "ERROR"

    def generateOpCode(self) -> str:
        opCodeMapping = {
            'or'    : '000000',
            'and'   : '000000',
            'sub'   : '000000',

            'beq'   : '000100',
            'lw'    : '100011',
            'sw'    : '101011',
            'sltiu' : '001011',

            'j'     : '000010'
        }
        if self.token in opCodeMapping:
            return opCodeMapping[self.token]
        raise Error(f"OpCode  not found {self.token}")

    def generateImmediate(self, immediate) -> str:
        if int(immediate) < 0:
            return self.TwoComplement(immediate)
        immediate = int(immediate)
        if isinstance(immediate, int):
            bin(immediate)[2:]

    def generateLabel(self, immediate) -> str:
        return bin(immediate - 4194304)[2:]

    def generateRegister(self):
        # treat register
        if self.token[0] != "$":
            raise Error(f"Registrador {self.token} não reconhecido.")
        register = self.token.replace("$", "")
        # translate register
        if register.isdigit():
            return bin(int(register))[2:].zfill(5)
        if register in ['zero', 'at', 'gp', 'sp', 'fp', 'ra']:
            return self.translateRegisterSpecialCases(register)[2:].zfill(5)
        match register[0]:
            case 'v':
                return bin(2 + self.verifyRegister(register, maxValue=1))[2:].zfill(5)
            case 'a':
                return bin(4 + self.verifyRegister(register, maxValue=3))[2:].zfill(5)
            case 't':
                if (register <= 7 and register >= 0):
                    return bin(8 + self.verifyRegister(register, maxValue=7))[2:].zfill(5)
                return bin(16 + self.verifyRegister(register, maxValue=9, minValue=8))[2:].zfill(5)
            case 's':
                return bin(16 + self.verifyRegister(register, maxValue=6))[2:].zfill(5)
            case 'k':
                return bin(26 + self.verifyRegister(register, maxValue=1))[2:].zfill(5)
            case _:
                raise Error(f"Registrador ${register} não reconhecido.")

    def translateRegisterSpecialCases(self) -> str:
        specialRegisterMapping = {
            'zero'  : bin(0),
            'at'    : bin(1),
            'gp'    : bin(28),
            'sp'    : bin(29),
            'fp'    : bin(30),
            'ra'    : bin(31)
        }
        if self.token in specialRegisterMapping:
            return specialRegisterMapping[self.token]
        raise Error(f"Register not found {self.token}")

    def verifyRegister(self, register: int, maxValue: int, minValue: int = 0) -> int:
        if (register > maxValue) or (register < minValue):
            raise Error(f"Registrador não permitido! Valor: {register}")
        return register