from Error import Error
from Debugger import logE, logW, logI, logD, logV
from os.path import join
from Assembly import Assembly
from Hex import Hex
class File():
	def __init__(self, fileName: str) -> None:
		self.name = fileName
		self.assembly = Assembly(self.getAssemblyContent())
		self.hexa = Hex(self.getHexaContent())

	def saveHexFile(self) -> None:
		path = join(r"../../hexadecimal", self.name)
		with open((path), "w") as file:
			file.write(self.hexa.CodeInHexa())

	def saveAssemblyFile(self) -> None:
		path = join(r"../../assembly", self.name)
		with open((path), "w") as file:
			file.write(self.assembly.CodeInAssembly())

	def getAssemblyContent(self) -> list:
		path = join(r"../../assembly", self.name)
		return self.readContent(path)

	def getHexaContent(self) -> list:
		path = join(r"../../hexadecimal", self.name)
		return self.readContent(path)

	def readContent(self, path: str) -> list:
		path = join(path, self.name)
		try:
			logI(f"Existe arquivo no path! Lendo arquivo com PATH: {path}")
			with open((path), "r") as file:
				content = file.readlines()
				return self.breakCodeIntoList(self, content)
		except IOError:
			logI(f"Arquivo não existente. Enviando conteúdo vazio. PATH: {path}")
			content = []
		return content

	def breakCodeIntoList(self, code) -> list:
		cleanedCode = []
		for codeLine in code:
			codeLine = codeLine.strip()
			if codeLine and not codeLine.startswith("#"):
				cleanedCode.append(codeLine)
		return cleanedCode
