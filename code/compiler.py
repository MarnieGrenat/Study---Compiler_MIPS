from dependencies.FileSystem import *
from dependencies.Debugger import *

from dcompiler.Assembly import Assembly
from dcompiler.Hex import Hex

class Compiler:
    def GenerateHexadecimal(path: str) -> int:
        '''Assembly to Hexadecimal'''
        counter = 0
        asmFiles = GetListOfFiles(path, r'assembly')
        for file in asmFiles:
            assembly = Assembly(file.Content())
            file.Save(assembly.CompileCode())
            counter += 1
        return counter

    def GenerateAssembly(path: str) -> int:
        '''Hexadecimal to Assembly'''
        counter = 0
        hexFiles = GetListOfFiles(path, r'assembly')
        for file in hexFiles:
            hexadecimal = Hex(file.Content())
            file.Save(hexadecimal.DecompileCode())
            counter += 1
        return counter