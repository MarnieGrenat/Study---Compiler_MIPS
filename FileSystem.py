from compiler.dependencies.Error import Error
from compiler.dependencies.Debugger import logE, logW, logI, logD, logV
from compiler.dependencies.Assembly import Assembly
from compiler.dependencies.Hex import Hex
from os.path import join
class File():
	def __init__(self, fileName: str, type:str) -> None:
		self.name = fileName
		if type == 'a2h':
			self.assembly = Assembly(self.getAssemblyContent())
			self.hexa = self.assembly.getHexaCode()

		elif type == 'h2a':
			self.hexa = Hex(self.getHexaContent())
			self.assembly = self.hexa.getAssemblyCode()

		else:
			logE(f"Tipo de arquivo inválido: {type}")
			raise Error("Tipo de arquivo inválido.")

	def saveBinaryFile(self) -> None:
		path = join(r"binary", self.name)
		with open((path[:-4]+"bin"), "w") as file:
			file.write(self.assembly.getBinaryCode())

	def saveHexFile(self) -> None:
		path = join(r"hexadecimal", self.name)
		with open((path[:-4]+"txt"), "w") as file:
			file.write(self.hexa)#concatCode(self.hexa))
		#self.saveBinaryFile()

	def saveAssemblyFile(self) -> None:
		path = join("assembly", self.name)
		with open((path), "w") as file:
			file.write(self.assembly.getAssemblyCode())


	def getAssemblyContent(self) -> list:
		path = join(r"assembly", self.name)
		return self.readContent(path)

	def getHexaContent(self) -> list:
		path = join(r"hexadecimal", self.name)
		return self.readContent(path)

	def concatCode(self, codeList:list) -> str:
		code = ""
		for line in codeList:
			code += line + "\n"
		return code

	def readContent(self, path: str) -> list:
		# path = join(path, self.name)
		try:
			logI(f"Existe arquivo no path! Lendo arquivo com PATH: {path}")
			with open((path), "r") as file:
				content = file.readlines()
				return self.breakCodeIntoList(content)
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
