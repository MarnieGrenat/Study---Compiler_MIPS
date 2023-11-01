from Error import Error
from Debugger import logE, logW, logI, logD, logV
from os import listdir
from Assembly import Assembly
from Hex import Hex

class File():
	def __init__(self, name:str) -> None:
		self.name = name
		self.assembly_path = r"../../assembly"
		self.hexa_path =  r"../../hexadecimal"
		self.assembly = Assembly(self.getContent(self.assembly_path))
		self.hexa = Hex(self.getContent(self.hexa_path))

	def getListOfFiles(self, path:str) -> list:
		return listdir(path)

	def saveHexFile(self) -> None:
		path = self.hexa_path+"/"+self.name
		with open((path), "w") as file:
			file.write(self.hexa.CodeInHexa())

	def saveAssemblyFile(self) -> None:
		path = self.assembly_path+"/"+self.name
		with open((path), "w") as file:
			file.write(self.assembly.CodeInAssembly())

	def readContent(self, path:str) -> list:
		path = self.hexa_path+"/"+self.name
		try:
			logI(f"Existe arquivo no path! Lendo arquivo com PATH: {path}")
			with open((path), "r") as file:
				content = file.readlines()
				return self.breakCodeIntoList(self, content)
		except IOError:
			logI(f"Arquivo não existente. Enviando conteúdo vazio. PATH: {path}")
			content = []
		return content

	def getAssemblyContent(self) -> list:
		return self.readContent(self.assembly_path+"/"+self.name)

	def getHexaContent(self) -> list:
		return self.readContent(self.hexa_path+"/"+self.name)

	def breakCodeIntoList(self, code) -> list:
		cleanedCode = []
		for codeLine in code:
			codeLine = codeLine.strip()
			if codeLine and not codeLine.startswith("#"):
				cleanedCode.append(codeLine)
		return cleanedCode
