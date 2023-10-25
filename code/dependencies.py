from dependencies import *

# Modifique os valores de debug
DEBUG_LEVEL = 0

ERROR  = 1
WARNING = 2
INFO = 3
DEBUG = 4
VERBOSE = 5

def setDEBUG_LEVEL(level:int) -> None:
    if level >= 0 and level <= 5

def getListOfFiles(path:str) -> list:
	pass

def gerarArquivosAssemblySeNecessario() -> int:
	ArquivosHexa = capturarListaDeArquivos(r"../hexadecimal")
	ArquivosAssembly = capturarListaDeArquivos(r"../assembly")
	contador = 0
	for arquivo in ArquivosAssembly:
		if (arquivo not in ArquivosHexa):
			codigoAssembly = capturarCodigoAssembly(arquivo)
			salvaArquivo(codigoAssembly, "../assembly/" + arquivo + "_MOUNTED"+ ".txt")
			contador+=1
	return contador

def saveFile(arquivo:str, path:str) -> bool:
    return True

def gerarArquivosHexaSeNecessario() -> int:
	ArquivosHexa = capturarListaDeArquivos(r"../hexade	cimal")
	ArquivosAssembly = capturarListaDeArquivos(r"../assembly")

	for arquivo in ArquivosHexa:
		if (arquivo not in ArquivosAssembly):
			capturarHexa(arquivo)
			contador+=1
	return contador

def capturarAssembly(arquivo:str) -> bool:
	commandsAssembly = ['or', 'and', 'sub', 'sltiu', 'lw', 'sw', 'beq', 'j']
	commandsHex = []
	raw_assembly = capturarCodigoAssembly()
	assembly = gerarAssembly(raw_assembly)
	salvaArquivo(assembly, "../hexadecimal/" + arquivo + "_MOUNTED"+ ".txt")
	pass

def gerarAssembly(listaComandosAssembly:list) -> str:
	codigoAssembly = ""
	return codigoAssembly

def convertMips2Hex(file:str) -> list:
    listaComandosAssembly = []
    return listaComandosAssembly

def convertHex2Mips(file:str) -> bool:
	commandsAssembly = ['or', 'and', 'sub', 'sltiu', 'lw', 'sw', 'beq', 'j']
	commandsHex = []

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