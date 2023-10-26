import Debugger as debug


def capturarAssembly(arquivo:str) -> bool:
	commandsAssembly = ['or', 'and', 'sub', 'sltiu', 'lw', 'sw', 'beq', 'j']
	commandsHex = []
	raw_assembly = capturarCodigoAssembly()
	assembly = gerarAssembly(raw_assembly)
	salvaArquivo(assembly, "../hexadecimal/" + arquivo + "_MOUNTED"+ ".txt")
	pass


def getListOfFiles(path:str) -> list:
	pass


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

def saveFile(arquivo:str, path:str) -> bool:
    return True