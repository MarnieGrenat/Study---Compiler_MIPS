# Author: Gabriela Dellamora Paim
'''
Programa que gera arquivos assembly a partir de arquivos em hexadecimal e vice-versa.
'''
def capturarListaDeArquivos(path:str) -> list:
	pass


def gerarAssembly(arquivo:str) -> bool:
	commandsAssembly = ['or', 'and', 'sub', 'sltiu', 'lw', 'sw', 'beq', 'j']
	commandsHex = []
	pass
	pass

def gerarHexa(arquivo:str) -> bool:
	commandsAssembly = ['or', 'and', 'sub', 'sltiu', 'lw', 'sw', 'beq', 'j']
	commandsHex = []
	pass
	pass


def gerarArquivosAssemblySeNecessario() -> int:
	ArquivosHexa = capturarListaDeArquivos(r"../hexadecimal")
	ArquivosAssembly = capturarListaDeArquivos(r"../assembly")

	for arquivo in ArquivosAssembly:
		if (arquivo not in ArquivosHexa):
			gerarAssembly(arquivo)
			contador+=1
	return contador

def gerarArquivosHexaSeNecessario() -> int:
	ArquivosHexa = capturarListaDeArquivos(r"../hexadecimal")
	ArquivosAssembly = capturarListaDeArquivos(r"../assembly")

	for arquivo in ArquivosHexa:
		if (arquivo not in ArquivosAssembly):
			gerarHexa(arquivo)
			contador+=1
	return contador

def InformacoesNoTerminal(countHexa:int, countAssembly:int) -> int:
	if	(not countAssembly and not countHexa):
		print("Não foi gerado nenhum arquivo. Verifique se você adicionou o arquivo no local correto. Leia o manual em Documentacao")
	else:
		print("Por favor, cheque as pastas para acessar os arquivos gerados!")
	if (countHexa):
		print(f"{countHexa} arquivo(s) hexa gerado(s).")
	if (countAssembly):
		print(f"{countAssembly} arquivo(s) assembly gerado(s).")
	return 0

def main() -> int:
	QuantidadeArquivosHexaGerados = gerarArquivosHexaSeNecessario()
	QuantidadeArquivosAssemblyGerados = gerarArquivosAssemblySeNecessario()

	return InformacoesNoTerminal(QuantidadeArquivosHexaGerados,
								QuantidadeArquivosAssemblyGerados)

# Execução do programa
if (__name__ == '__main__'):
	main()








