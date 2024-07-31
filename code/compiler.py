from dependencies.FileSystem import *
from dependencies.Debugger import *

from dcompiler.Assembly import Assembly
from dcompiler.Hex import Hex

class Compiler:
    def GenerateHexadecimal(path: str) -> int:
        '''Assembly to Hexadecimal'''
        counter = 0
        asmFiles = GetListOfFiles(path, r'assembly')
        for doc in asmFiles:
            asm = Assembly(doc.Content, doc.Name)
            Save(asm.Compile(), (path + '/' + asm.fileName + '.txt'))
            counter += 1
        return counter

    def GenerateAssembly(path: str) -> int:
        '''Hexadecimal to Assembly'''
        counter = 0
        hexFiles = GetListOfFiles(path, r'hexadecimal')
        for doc in hexFiles:
            hex = Hex(doc.Content)
            Save(hex.Decompile(), (path + '/' + hex.fileName + '.asm'))
            counter += 1
        return counter