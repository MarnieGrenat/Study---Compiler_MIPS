from Debugger import logE, logW, logI, logD, logV
from Assembly import Assembly
from Hex import Hex

class File(Assembly, Hex):
	def __init__(self, name:str) -> None:
		self.name = name
		self.assembly_path = r"../../assembly"
		self.hexa_path =  r"../../hexadecimal"
		self.assembly = Assembly(self.get_content())
		self.hex = self.createHexObject()
  
	def createHexObject(self) -> Hex:
		if get_

	def save_file(self) -> None:
		with open((self.to_file + "/" + self.name), "w") as file:
			file.write(self.CodeInHexa())
   
	def get_content(path1:str,) -> str:
		with open((path1 + "/"+ path2), "r") as file:
			content = file.readlines()
		return self.cleanAssemblyCode(content)

	def cleanAssemblyCode(self, code) -> list:
		'''Remove comentários e linhas vazias do código assembly.'''
		cleanedCode = []
		for codeLine in code:
			# Remover espaços em branco à esquerda e à direita da linha
			codeLine = codeLine.strip()
			# Verificar se a linha não está vazia após a remoção de espaços
			if codeLine and not codeLine.startswith("#"):
				# Adicionar a linha limpa à lista
				cleanedCode.append(codeLine)
		return cleanedCode


from Debugger import logE, logW, logI, logD, logV

class HexFile(Hex):
	def __init__(self, name:str):
		self.name = name
		self.fromFilePath = r"../../hexadecimal"
		self.toFilePath = r"../../assembly"
		self.hex = Hex(self.getContent())
		self.decompiled = ""

	def getContent(self) -> str:
		with open((self.fromFilePath + "/"+ self.name), "r") as file:
			content = file.readlines()
			file.close()
		return content

	def saveFile(self) -> None:
		with open((self.toFilePath + "/" + self.name), "w") as file:
			file.write(self.decompiled)




