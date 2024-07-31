
# class Binary:
    # def __init__(self, hex):
    #     self.HexCode = hex
    #     self.Binary  = self.GenerateBinary()

def GenerateBinary(Hex: str) -> list:
    binary = []
    for hexLine in Hex:
        binary.append(formatBinary(hexLine))
    return binary

def formatBinary(line: str) -> str:
    line = bin(int(line, 16))
    line = line[2:].zfill(32)
    return str(line)