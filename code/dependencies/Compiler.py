import Debugger as debug
import FileSystem as fileSys
from Debugger import *

class Assembly():
	__init(self, name:str)__:
	self.name = name
	self.fromFilePath = r"../../assembly"
	self.toFilePath = r"../../hexadecimal"
	self.content = getContent(self.name)
	self.compiled = ""

def gerarArquivosHexaSeNecessario() -> int:
	ArquivosHexa = fileSys.capturarListaDeArquivos(r"../../hexadecimal")
	ArquivosAssembly = fileSys.capturarListaDeArquivos(r"../../assembly")

	for arquivo in ArquivosHexa:
		if (arquivo not in ArquivosAssembly):
			capturarHexa(arquivo)
			contador+=1
	return int(contador)

	

def convertLineMips2Hex(file:str) -> list:
    listaComandosAssembly = []
    return listaComandosAssembly


