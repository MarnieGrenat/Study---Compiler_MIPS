import unittest

from code.compiler.dependencies.HexFile import Hex
from code.compiler.dependencies.AssemblyFile import Assembly
import compiler.Compiler as compiler

class TestAssembly(unittest.TestCase):
    def setUp(self):
        self.assembly = Assembly("sample.mips")

    def testTranslation(self):
        self.assertEqual(self.assembly.convertLineMips2Hex("add $t0, $t1, $t2"), "0000002409000018\n")
