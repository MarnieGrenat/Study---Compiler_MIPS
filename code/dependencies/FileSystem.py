import FileSystem as fileSys
from Debugger import *

def getListOfFiles(path:str) -> list:
	pass

def printINFO_onTerminal(countHexa:int, countAssembly:int) -> int:
	if	(not countAssembly and not countHexa):
		logI("Não foi gerado nenhum arquivo. Verifique se você adicionou o arquivo no local correto. Leia o manual em Documentacao")
	else:
		logI("Por favor, cheque as pastas para acessar os arquivos gerados!")
	if (countHexa):
		logI(f"{countHexa} arquivo(s) hexa gerado(s).")
	if (countAssembly):
		logI(f"{countAssembly} arquivo(s) assembly gerado(s).")
	return 0