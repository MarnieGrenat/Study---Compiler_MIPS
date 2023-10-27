# Author: Gabriela Dellamora Paim

## IMPORTS
import dependencies.Compiler as compiler
import dependencies.Decompiler as decompiler
import dependencies.FileSystem as fileSys
from dependencies.Debugger import *
'''
Programa que gera arquivos assembly a partir de arquivos em hexadecimal e vice-versa.
'''
ERROR  = 1
WARNING = 2
INFO = 3
DEBUG = 4
VERBOSE = 5


def main(DEBUG_LEVEL:int=ERROR) -> int:
	debugger.setDebugLevel(DEBUG_LEVEL)

	countGeneratedAssembly = decompiler.generateAssemblyIfNecessary()
	countGeneratedHex = compiler.generateHexIfNecessary()

	return fileSys.printINFO_onTerminal(countGeneratedHex,
										countGeneratedAssembly)

# Execução do programa
if (__name__ == '__main__'):
	main(DEBUG_LEVEL=VERBOSE)









