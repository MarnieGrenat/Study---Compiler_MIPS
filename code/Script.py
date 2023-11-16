# Author: Gabriela Dellamora Paim
## IMPORTS
import compiler.Compiler as c

'''
Programa que gera arquivos assembly a partir de arquivos em hexadecimal e vice-versa.
Todos os outros arquivos nesse script são importados do pacote compiler.
O único arquivo que o usuário precisa rodar é esse, Script.py.
'''


def main() -> None:
	t = input("Digite 1 para gerar arquivos assembly a partir de arquivos em hexadecimal ou 2 para gerar arquivos em hexadecimal a partir de arquivos assembly: ")
	if (str(t) == "1"):
		c.generateAssemblyIfNecessary()
	elif (str(t) == "2"):
		c.generateHexadecimalIfNecessary()
	else:
		print("Opção inválida. Tente novamente.")
# Execução do programa
if (__name__ == '__main__'):
	main()