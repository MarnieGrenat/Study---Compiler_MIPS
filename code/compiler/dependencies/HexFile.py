from Debugger import logE, logW, logI, logD, logV

class Hex():
	def __init__(self, name:str):
		self.name = name
		self.fromFilePath = r"../../hexadecimal"
		self.toFilePath = r"../../assembly"
		self.content = self.getContent()
		self.decompiled = ""

	def getContent(self) -> str:
		with open((self.fromFilePath + "/"+ self.name), "r") as file:
			content = file.readlines()
			file.close()
		return content

	def generateAssembly(self) -> None:
		for line in self.content:
			self.decompiled += self.convertLineHex2Mips(line) # TODO: Tratamento de erros

	def convertLineHex2Mips(self, line:str) -> str:
		assembly = ""
		listOfHexCodes = self.breakSingleHexCode(line)
		for opCode in listOfHexCodes:
			assembly += self.translateSingleOpCode(opCode)
		return (assembly + "\n")

	def breakLineIntoListOfCommands(self, line:str) -> list:
		pass

	def translateOpCode(self, line:str) -> str:
		commandsAssembly = ['or', 'and', 'sub', 'sltiu', 'lw', 'sw', 'beq', 'j']
		commandsHex = []

	def saveFile(self) -> None:
		with open((self.toFilePath + "/" + self.name), "w") as file:
			file.write(self.decompiled)



