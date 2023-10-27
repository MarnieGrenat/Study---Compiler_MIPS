# Modifique os valores de debug
ERROR  = 1
WARNING = 2
INFO = 3
DEBUG = 4
VERBOSE = 5

class debugger():
    '''
    Classe para debugar o compilador. Possui 5 níveis de debug, sendo 1 o mais importante e 5 o menos importante.
    Segue padrão ESP32.
    '''
    def __init__(self, debug_level:int):
        if debug_level > 0 and debug_level <= 5:
            self.debug_level = debug_level
        else:
            debug_level = 0

    def setDebugLevel(self, debug_level:int):
        if debug_level > 0 and debug_level <= 5:
            self.debug_level = debug_level
        else:
            debug_level = 0

    def debug(self, message:str, debug_level:int):
        if (debug_level <= self.debug_level):
            print(message)

    def logE(self, message:str):
        self.debug(message, ERROR)

    def logW(self, message:str):
        self.debug(message, WARNING)

    def logI(self, message:str):
        self.debug(message, INFO)

    def logD(self, message:str):
        self.debug(message, DEBUG)

    def logV(self, message:str):
        self.debug(message, VERBOSE)

debugger = debugger()