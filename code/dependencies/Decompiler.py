import Debugger as debug
import FileSystem as fileSys

def convertHex2Mips(file:str) -> bool:
	commandsAssembly = ['or', 'and', 'sub', 'sltiu', 'lw', 'sw', 'beq', 'j']
	commandsHex = []

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
	return int(contador)

