from dependencies.Error import Error
from dependencies.Debugger import logE, logW, logI, logD, logV

import os
class File():
	def __init__(self, FilePath: str) -> None:
		self.Name, self.FileExtension = self.StripFileExtension(FilePath)
		self.Path = FilePath
		self.Content = self.readContent()

	def Save(self, code: str) -> None:
		path = os.path.join(self.Path, self.Name)
		with open((path + self.FileExtension), 'w') as File:
			File.write(self.ProcessedCode)

	def GetContent(self) -> list:
		return self.readContent(os.path.join(self.Path, self.Name))

	def readContent(self) -> list:
		try:
			logI(f"Existe arquivo no path! Lendo arquivo com PATH: {self.Path}")
			with open((self.Path), "r") as file:
				content = file.readlines()
				return self.ProcessFile(content)
		except IOError:
			logI(f"Arquivo não existente. Enviando conteúdo vazio. PATH: {self.Path}")
			return []

	def ProcessFile(self, code) -> list:
		'''Process text into codelines'''
		cleanedCode = []
		for codeLine in code:
			codeLine = codeLine.strip()
			if codeLine and not codeLine.startswith("#"):
				cleanedCode.append(codeLine)
		return cleanedCode

	def StripFileExtension(self, fileName: str) -> str:
		return fileName.rstrip('.'), fileName.lstrip('.')

def GetListOfFiles(path: str, dir: str) -> list:
	files = []
	path = os.path.join(path, dir)
	for fileName in os.listdir(path):
		print(fileName)
		document = File(fileName)
		files.append(document)
	return files