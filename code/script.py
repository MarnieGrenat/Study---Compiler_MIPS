# Author: Gabriela Dellamora Paim

from dependencies import *
'''
Programa que gera arquivos assembly a partir de arquivos em hexadecimal e vice-versa.
'''



def main(DEBUG_LEVEL:int) -> int:
    setDEBUG_LEVEL(DEBUG_LEVEL)
	QuantidadeArquivosHexaGerados = gerarArquivosHexaSeNecessario()
	QuantidadeArquivosAssemblyGerados = gerarArquivosAssemblySeNecessario()

	return InformacoesNoTerminal(QuantidadeArquivosHexaGerados,
								QuantidadeArquivosAssemblyGerados)

# Execução do programa
if (__name__ == '__main__'):
	main(VERBOSE)








