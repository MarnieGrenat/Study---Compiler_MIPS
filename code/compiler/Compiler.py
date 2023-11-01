from dependencies.FileSystem import File as File
from dependencies.Debugger import logE, logW, logI, logD, logV

def generateHexadecimalIfNecessary() -> int:
    assemblyFileNames = File.getListOfFiles(r"../../assembly")
    hexFileNames = File.getListOfFiles(r"../../hexadecimal")

    count = 0
    for fileName in assemblyFileNames:
        if fileName not in hexFileNames:
            newHexFile = File(fileName)
            newHexFile.generateHexadecimal()
            newHexFile.saveFile()
            count+=1

    return int(count)

def generateAssemblyIfNecessary() -> int:
    assemblyFileNames = File.getListOfFiles(r"../../assembly")
    hexFileNames = File.getListOfFiles(r"../../hexadecimal")
    count = 0

    for fileName in hexFileNames:
        if fileName not in assemblyFileNames:
            newAssemblyFile = File(fileName)
            newAssemblyFile.generateAssembly()
            newAssemblyFile.saveFile()
            count+=1
    return int(count)


def printLogInformationOnTerminal(countHexa:int, countAssembly:int) -> int:
	if	(not countAssembly and not countHexa):
		logW("Não foi gerado nenhum arquivo. Verifique se você adicionou o arquivo no local correto.")
		logW("Verifique se o arquivo está no formato correto ou no repositório adequado.")
	else:
		logI("Por favor, cheque as pastas para acessar os arquivos gerados!")
	if (countHexa):
		logI(f"{countHexa} arquivo(s) hexa gerado(s).")
	if (countAssembly):
		logI(f"{countAssembly} arquivo(s) assembly gerado(s).")
	return 0