import Debugger as debug
import FileSystem as fileSys

class Hex():
	__init(self, name:str)__:
		self.name = name
		self.fromFilePath = r"../../hexadecimal"
		self.toFilePath = r"../../assembly"
		self.content = getContent()
		self.decompiled = ""

	def getContent(self) -> str:
		with open((self.fromFilePath + "/"+ self.name), "r") as file:
			content = file.readlines()
			file.close()
		return content

	def generateAssembly(self) -> None:
		for line in content:
			self.decompiled += convertLineHex2Mips(line) #TODO: Tratamento de erros
	
	def convertLineHex2Mips(line:str) -> str:
		assembly = ""
		listOfHexCodes = breakHexCode(line)
		for opCode in listOfHexCodes:
			assembly += translateOpCode(opCode)
		return (assembly + "\n")

	def breakSingleHexCode(line) -> list:
		pass
	
	def translateSingleOpCode(line) -> str:
		commandsAssembly = ['or', 'and', 'sub', 'sltiu', 'lw', 'sw', 'beq', 'j']
		commandsHex = []
	
	def saveFile(self) -> None:
		with open((self.toFilePath + "/" + self.name), "w") as file:
			file.write(self.decompiled)
			

def generateAssemblyIfNecessary() -> int:
	'''Gera assembly caso não exista assembly dos arquivos. Retorna quantidade de decompilações. '''
	hexFileNames = fileSys.getListOfFiles(r"../../hexadecimal")
	assemblyFileNames = fileSys.getListOfFiles(r"../../assembly")
	count = 0

	for fileName in assemblyFileNames:
		fileName+= "_DEC"
		if (fileName not in hexFileNames):
			hexFile = Hex(fileName)
			hexFile.generateAssembly()
			fileSys.saveNewAssembly(hexFile)
			count+=1

	return int(count)


