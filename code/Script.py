# Author: Gabriela Dellamora Paim
## IMPORTS
import compiler.Compiler as c

'''
Programa que gera arquivos assembly a partir de arquivos em hexadecimal e vice-versa.
Todos os outros arquivos nesse script são importados do pacote compiler.
O único arquivo que o usuário precisa rodar é esse, Script.py.
'''

def main() -> int:
	countGeneratedHexadecimal= c.generateHexadecimalIfNecessary()
	countGeneratedAssembly = c.generateAssemblyIfNecessary()
	return c.printLogInformationOnTerminal(countGeneratedHexadecimal,
											countGeneratedAssembly)

# Execução do programa
if (__name__ == '__main__'):
	main()
