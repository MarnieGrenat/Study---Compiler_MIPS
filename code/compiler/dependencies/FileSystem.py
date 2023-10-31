from Debugger import logE, logW, logI, logD, logV
from Assembly import Assembly
from Hex import Hex

class File(Assembly, Hex):
	def __init__(self, name:str) -> None:
		self.name = name
		self.assembly_path = r"../../assembly"
		self.hexa_path =  r"../../hexadecimal"
		self.assembly = self.createAssemblyObject()
		self.hex = self.createHexObject()

	def createAssemblyObject(self) -> Assembly:
		return Assembly(self.getContent(self.assembly_path))
		return self.cleanAssemblyCode(content)


	def createHexObject(self) -> Hex:
		return Hex(self.getContent(self.hexa_path))

	def getListOfFiles(self, path:str) -> list:
    	return listdir(path)

	def saveFile(self) -> None:
		with open((self.to_file + "/" + self.name), "w") as file:
			file.write(self.CodeInHexa())
   
	def getContent(self, path:str) -> list:
		try:
			logI(f"Existe arquivo no path! Lendo arquivo com PATH: {path+"/"+self.name}")
			with open((path + "/"+ self.name), "r") as file:
				content = file.readlines()
				breakCodeIntoList(self, content)
		except IOError:
			logI(f"Arquivo não existente. Enviando conteúdo vazio. PATH: {path+"/"+self.name}")
			content = []
		return content
			
	def breakCodeIntoList(self, code) -> list:
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



