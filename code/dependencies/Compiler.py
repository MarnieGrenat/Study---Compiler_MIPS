import Debugger as debug
import FileSystem as fileSys


def convertMips2Hex(file:str) -> list:
    listaComandosAssembly = []
    return listaComandosAssembly

def gerarArquivosHexaSeNecessario() -> int:
	ArquivosHexa = capturarListaDeArquivos(r"../hexade	cimal")
	ArquivosAssembly = capturarListaDeArquivos(r"../assembly")

	for arquivo in ArquivosHexa:
		if (arquivo not in ArquivosAssembly):
			capturarHexa(arquivo)
			contador+=1
	return int(contador)

def gerarHex(listaComandosAssembly:list) -> str:
	codigoHex = ""
	return codigoHex
