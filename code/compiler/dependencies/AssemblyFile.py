from Debugger import logE, logW, logI, logD, logV
from Assembly import Assembly

class AssemblyFile(Assembly):
	def __init__(self, name:str) -> None:
		self.name = name
		self.from_file = r"../../assembly"
		self.to_file =  r"../../hexadecimal"
		self.assembly = Assembly(self.get_content())

	def get_content(self) -> str:
		with open((self.from_file + "/"+ self.name), "r") as file:
			self.content = file.readlines()
			file.close()
		return self.content

	def save_file(self) -> None:
		with open((self.to_file + "/" + self.name), "w") as file:
			file.write(self.CodeInHexa())

   ###### Generating HEXA ######
	def CodeInHexa(self) -> str:
		return hex(int(self.assembly.getBinary()))

	def generate_all_hex(self) -> None:
		'''Gera o código hexadecimal a partir do código assembly.'''
		for line in self.content:
			self.decompiled += self.convert_line_mips_to_hex(line) 						# TODO: Tratamento de erros

	def convert_line_mips_to_hex(self, line:str) -> str:
		'''Converte uma linha de código assembly para binário'''
		listOfAssemblyCodesInASingleCommand = self.break_line_into_commands(line) 		# Quebra a linha em comandos assembly

		hexa = ""
		for opCode in listOfAssemblyCodesInASingleCommand: 								# Quebra o comando em opcode e operandos
			hexa += self.translate_op_code(opCode)
		return (str(self.bin_to_hexa(hexa)) + "\n")

	def break_line_into_commands(self, line:str) -> list:
		'''Quebra uma linha de código assembly em uma lista de comandos assembly.'''
		listOfCommands = []
		return listOfCommands

	def bin_to_hexa(self, hexa:str) -> str:
		return hex(int(hexa, 2))

	#### TRANSLATING MIPS TO BIN ####
	def translate_line(self, line:str) -> str:
		'''Traduz um único comando assembly para binário'''
		opCode = line.split()[0]

		if opCode in ['or', 'and', 'sub', 'sltiu']:
			return self.M2H_R_type(line)
		elif opCode in ['lw', 'sw', 'beq']:
			return self.M2H_I_type(line)
		elif opCode in ['j']:
			return self.M2H_J_type(line)
		else:
			# Verifica se é um label ou comentario. se não for, é um erro.
			if (opCode[0] != '#' and opCode[-1] != ':'): 				# Se não começa com # ou se não termina com :
				logE(f"Erro na linha {line}. Comando {opCode} não reconhecido.")
			else:
				logW(f"Comentário ou label encontrado na linha {line}.")
		commandTranslated = ""

		return (commandTranslated + "\n")

	def M2H_I_type(self, line:str) -> str:
		'''Traduz um comando assembly do tipo I para binário'''
		command = line.split()

		opCode = self.__translate_opCode(command[0]) 						# 6 bits
		rs = self.__translate_register(command[1])						# 5 bits
		rt = self.__translate_register(command[2])						# 5 bits
		immediate = self.__translate_immediate(command[-1])				# 16 bits
		return ""

	def M2H_J_type(self, line:str) -> str:
		opCode = 	bin(4)									 	# 6 bits 	TODO: cortar os primeiros 3 bits
		address = self.__get_address_from_label(line.split()[-1])		# 26 bits	TODO: Cortar os ulti
		return ""

	def M2H_R_type(self, line:str) -> str:
		command = line.split()

		opCode = self.__translate_opCode(command[0]) 							# 6 bits
		rs = self.__translate_register(command[1])						# 5 bits
		rt = self.__translate_register(command[2])						# 5 bits
		rd = self.__translate_register(command[3])						# 5 bits
		shamt = # 5 bits
		funct = # 6 bits
		return ""

	def __translate_opCode(command:str) -> bin:
		return -1

	def __get_address_from_label(self, label:str) -> bin:
		return -1
	def __translate_register(self, register) -> int:
		'''Traduz um registrador assembly para binário'''
		if (register[0] != '$'):
			logE(f"Erro na linha {line}. Registrador {register} não reconhecido.")
			return -1

		elif (register[1:-1] == zero or register[1:-1] == "0"):
			return 0
		elif (register[1] == "v"):
			return self.__translate_register_v(register)
		elif (register[1] == "s"):
			return self.__translate_register_s(register)
		elif (register[1] == "t"):
			return self.__translate_register_t(register)
		elif (register[1] == "a"):
			return self.__translate_register_a(register)
		elif (register[1] == "k"):
			return self.__translate_register_k(register)
		elif register[1:-1] in ['gp', 'sp', 'fp', 'ra']:
			return self.__translate_register_special_cases(register)
		logE(f"Registrador {register} não reconhecido. Retorno -1")
		return -1

	def __translate_register_v(self, register) -> int:
		'''Traduz um registrador assembly do tipo v para binário'''
		if (register[2:-1] in [0, 1]):
			return (2 + int(register[2:-1]))
		logE(f"Registrador {register} não reconhecido. Retorno -1")
		return -1

	def __translate_register_s(self, register) -> int:
		return -1

	def __translate_register_t(self, register) -> int:
		return -1

	def __translate_register_a(self, register) -> int:
		return -1

	def __translate_register_k(self, register) -> int:
		return -1

	def __translate_register_special_cases(self, register) -> int:
		return -1