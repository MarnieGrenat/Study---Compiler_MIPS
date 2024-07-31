from dependencies.Error import Error
from dependencies.Debugger import logE, logW, logI, logD, logV

import os
class File():
	def __init__(self, FilePath: str) -> None:
		self.Name, self.FileExtension = os.path.splitext(FilePath)
		self.FilePath = FilePath
		self.Content: list = self.readContent()
		logI(f'Name={self.Name} : FileExtension={self.FileExtension} : Path={self.FilePath} : Content={self.Content}')

	def GetContent(self) -> list:
		return self.readContent(os.path.join(self.FilePath, self.Name))

	def readContent(self) -> list:
		content = []
		try:
			with open(self.FilePath, "r") as f:
				content = self.ProcessFile(f.readlines())
		except IOError:
			logE(f"Arquivo não existente. Enviando conteúdo vazio. PATH: {self.FilePath}")
		return content

	def ProcessFile(self, code) -> list:
		'''Process text into codelines'''
		cleanedCode = []
		for codeLine in code:
			codeLine = codeLine.strip()
			if codeLine and not codeLine.startswith("#"):
				cleanedCode.append(codeLine)
		return cleanedCode

def Save(code: str, path: str) -> None:
	with open(path, 'w') as f:
		f.write(code)

def GetListOfFiles(path: str, dir: str) -> list:
	files = []
	path = os.path.join(path, dir)
	for fileName in os.listdir(path):
		document = File( path + '/' + fileName) # os.path.join(path, fileName))
		files.append(document)
	return files