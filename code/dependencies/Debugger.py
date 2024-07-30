# Modifique os valores de DEBUG_LEVEL para alterar o nível de debug.
ERROR  = 1
WARNING = 2
INFO = 3
DEBUG = 4
VERBOSE = 5

DEBUG_LEVEL = VERBOSE

"""
    Debugar o compilador. Possui 5 níveis de debug, sendo 1 o mais importante e 5 o menos importante.
    Segue padrão ESP32.
"""

def logE(message:str):
    debug(message, ERROR)

def logW(message:str):
    debug(message, WARNING)

def logI(message:str):
    debug(message, INFO)

def logD(message:str):
    debug(message, DEBUG)

def logV(message:str):
    debug(message, VERBOSE)

def debug(message:str, debug_level:int):
    if (debug_level <= DEBUG_LEVEL):
        print(message)