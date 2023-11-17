# Montagem e Desmontagem de Código Assembly MIPS
**Autor:** Gabriela Dellamora Paim

**Versão:** 1.0.2

## Descrição
O projeto `Montagem e Desmontagem de Código Assembly MIPS` consiste em um script que realiza a conversão entre código assembly e código binário (salvo em hexadecimal), bem como a conversão inversa de (hexadecimal para binário e de) binário para assembly.

### Instruções Suportadas
Para este projeto, estamos focando em um conjunto limitado de instruções MIPS:

- or
- and
- sub
- sltiu
- lw
- sw
- beq
- j

## Como Utilizar
Para utilizar este script, siga as seguintes etapas:

1. Existem dois diretórios essenciais na pasta principal do projeto: `./hexadecimal` e `./assembly`. Envie seu arquivo `.txt` para o diretório `./hexadecimal` e seu arquivo `.asm` para o diretório `./assembly`.

2. Execute o script. Ele automatizará o processo de compilação e decompilação. Para os arquivos `.mips`, o script gerará o código hexadecimal no diretório `./hexadecimal`. Para os arquivos `.txt`, ele gerará o código assembly no diretório `./assembly`. Basta escolher a opção desejada no terminal.

3. Não é necessário excluir os arquivos gerados anteriormente, pois o script fará comparações para determinar se a compilação ou decompilação é necessária.

## Como Executar o Script

#### WINDOWS
    Para executar o script, basta rodar o arquivo `run.bat`.

#### LINUX ou MacOS
    Para executar o script, basta rodar o arquivo `run.bash`.

#### Outras alternativas
Caso os arquivos .bat e .bash não estejam funcionais, é possível rodar o script utilizando o terminal, entrando no repositório do projeto e enviando o comando `python code\Script.py`.


## Observações
- Mantenha nomes únicos e autodescritivos para seus arquivos. O script faz comparações com base nos nomes dos arquivos, portanto, isso é importante para evitar problemas de compilação.

## Limitações da aplicação:
- O Assembler não aceita duas instruções exatamente iguais. Todas instruções devem ter alguma diferença entre si.
- O Assembler não compila linhas com label ao lado. Labels devem estar em linhas separadas
- O Assembler não suporta tradução de dois ou mais labels sequenciais, quando o primeiro é vazio.

## Licença
Este projeto é distribuído sob a Licença Apache. Consulte o arquivo LICENSE para obter mais informações
