# Author: Gabriela Dellamora Paim
from compiler import *
'''
Programa que gera arquivos assembly a partir de arquivos em hexadecimal e vice-versa.
Todos os outros arquivos nesse script são importados do pacote compiler.
O único arquivo que o usuário precisa rodar é esse, Script.py.
'''

def main() -> None:
	UserInput = str(input("Digite 1 para gerar arquivos assembly a partir de arquivos em hexadecimal ou 2 para gerar arquivos em hexadecimal a partir de arquivos assembly: "))
	if (UserInput == "1"):
		Compiler.GenerateAss1embly(r'../test/')
	elif (UserInput == "2"):
		Compiler.GenerateHexadecimal(r'../test/')
	else:
		print("Opção inválida. Tente novamente.")

# Execução do programa
if (__name__ == '__main__'):
	main()