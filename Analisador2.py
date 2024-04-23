from estadosDeAceitação import estados
from erros import listaErros

def verificar_aceitacao(lin, col, lexema_atual, estado):
  token = ()

  if estado in estados['TK_INT']:
    token = (lin, col - len(lexema_atual), "TK_INT", lexema_atual)
  elif estado in estados['TK_FLOAT']:
    token = (lin, col - len(lexema_atual), "TK_FLOAT", lexema_atual)
  elif estado in estados['TK_END']:
    token = (lin, col - len(lexema_atual), "TK_END", lexema_atual)
  elif estado in estados['TK_CADEIA']:
    token = (lin, col - len(lexema_atual), "TK_CADEIA", lexema_atual)
  elif estado in estados['TK_ID']:
    token = (lin, col - len(lexema_atual), "TK_ID", lexema_atual)
  elif estado in estados['TK_DATA']:
    token = (lin, col - len(lexema_atual), "TK_DATA", lexema_atual)
  elif estado in estados['TK_COMENT_LINHA']:
    token = (lin, col - len(lexema_atual), "TK_COMENT_LINHA", lexema_atual)
  elif estado in estados['TK_COMENT_BLOCO']:
    token = (lin, col - len(lexema_atual), "TK_COMENT_BLOCO", lexema_atual)
  elif lexema_atual in estados['palavrasReservadas']:
    token = (lin, col - len(lexema_atual), f"TK_{lexema_atual.upper()}", lexema_atual)
  elif lexema_atual in estados['operadores']:
    token = (lin, col - len(lexema_atual), f"TK_{lexema_atual.upper()}", lexema_atual)
  elif lexema_atual in estados['delimitadores']:
    token = (lin, col - len(lexema_atual), f"TK_{lexema_atual.upper()}", lexema_atual)
  
  return token

def getPrimeiraTransicao(simbolo):
    if simbolo.isdigit():
        return 1
    elif simbolo == ".":
        return 4
    elif simbolo in ["A", "B", "C", "D", "E", "F"]:
        return 14
    elif simbolo == '"':
        return 34
    elif simbolo.isalpha() and simbolo.islower():
        return 38
    elif simbolo == "<":
        return 63
    elif simbolo == ">":
        return 71
    elif simbolo == "#":
        return 79
    elif simbolo == "<":
        return 63
    elif simbolo == ">":
        return 71
    elif simbolo == "+":
        return 56
    elif simbolo == "*":
        return 57
    elif simbolo == "-":
        return 58
    elif simbolo == "&":
        return 59
    elif simbolo == "%":
        return 60
    elif simbolo == "~":
        return 61
    elif simbolo == "|":
        return 62
    elif simbolo == ":":
        return 84
    elif simbolo == "(":
        return 86
    elif simbolo == ")":
        return 88
    elif simbolo in [" ", "\t"]:
        return 0
    elif simbolo == "\n":
        return 0
    else:
        return -1

def ler_token(cadeia: str):
  """
  Essa é a função responsável por receber a cadeia de caracteres e retornar uma lista de tokens.
  O retorno da função é uma tabela de tokens, onde cada token é representado como uma tupla contendo a linha, a coluna, o tipo e o lexema do token.
  """

  # Estado inicial do autômato
  estado = 0

  # Inicialização de variáveis que serão utilizadas para construir a lista de tokens
  lin = 1
  col = 1
  lexema_atual = ""
  tokens = []

  # Variável para controle de erro
  semTransicao = False
  erro = False
  erros = []
  somatorio = {}

  for simbolo in cadeia:
    match (estado):
        case 0:
            if simbolo.isdigit():
                estado = 1
            elif simbolo == ".":
                estado = 4
            elif simbolo in ["A", "B", "C", "D", "E", "F"]:
                estado = 14
            elif simbolo == '"':
                estado = 34
            elif simbolo.isalpha() and simbolo.islower():
                estado = 38
            elif simbolo == "<":
                estado = 63
            elif simbolo == ">":
                estado = 71
            elif simbolo == "+":
                estado = 56
            elif simbolo == "*":
                estado = 57
            elif simbolo == "-":
                estado = 58
            elif simbolo == "&":
                estado = 59
            elif simbolo == "%":
                estado = 60
            elif simbolo == "~":
                estado = 61
            elif simbolo == "|":
                estado = 62
            elif simbolo == ":":
                estado = 84
            elif simbolo == "(":
                estado = 86
            elif simbolo == ")":
                estado = 88
            elif simbolo in ["+", "-", "*", "|", "&", "%", "~", ":", "(", ")"]:
                tokens.append((lin, col, f"TK_{simbolo.upper()}", simbolo))
                col += 1
                continue
            elif simbolo == "#":
                estado = 79
            elif simbolo in [" ", "\t"]:
                col += 1
                continue
            elif simbolo == "\n":
                lin += 1
                col = 1
                continue
            else:
                semTransicao = True
        case 1:
            if simbolo.isdigit():
                estado = 2
            elif simbolo == ".":
                estado = 5
            elif simbolo == "x":
                estado = 31
            else:
                semTransicao = True
        case 2:
            if simbolo.isdigit():
                estado = 3
            elif simbolo == ".":
                estado = 5
            elif simbolo == "/":
                estado = 15
            elif simbolo == "_":
                estado = 23
            else:
                semTransicao = True
        case 3:
            if simbolo.isdigit():
                estado = 9
            elif simbolo == ".":
                estado = 5
            else:
                semTransicao = True
        case 4:
            if simbolo.isdigit():
                estado = 5
            else:
                semTransicao = True
        case 5:
            if simbolo.isdigit():
                estado = 5
            elif simbolo == "e":
                estado = 6
            else:
                semTransicao = True
        case 6:
            if simbolo.isdigit():
                estado = 7
            elif simbolo == "-":
                estado = 8
            else:
                semTransicao = True
        case 7:
            if simbolo.isdigit():
                estado = 7
            else:
                semTransicao = True
        case 8:
            if simbolo.isdigit():
                estado = 7
            else:
                semTransicao = True
        case 9:
            if simbolo.isdigit():
                estado = 9
            else:
                semTransicao = True
        case 12:
            semTransicao = True
        case 14:
            if simbolo == "x":
                estado = 31
            else:
                semTransicao = True
        case 15:
            if simbolo.isdigit():
                estado = 16
            else:
                semTransicao = True
        case 16:
            if simbolo.isdigit():
                estado = 17
            else:
                semTransicao = True
        case 17:
            if simbolo == "/":
                estado = 18
            else:
                semTransicao = True
        case 18:
            if simbolo.isdigit():
                estado = 19
            else:
                semTransicao = True
        case 19:
            if simbolo.isdigit():
                estado = 20
            else:
                semTransicao = True
        case 20:
            if simbolo.isdigit():
                estado = 21
            else:
                semTransicao = True
        case 21:
            if simbolo.isdigit():
                estado = 12
            else:
                semTransicao = True
        case 23:
            if simbolo.isdigit():
                estado = 24
            else:
                semTransicao = True
        case 24:
            if simbolo.isdigit():
                estado = 25
            else:
                semTransicao = True
        case 25:
            if simbolo == "_":
                estado = 26
            else:
                semTransicao = True
        case 26:
            if simbolo.isdigit():
                estado = 27
            else:
                semTransicao = True
        case 27:
            if simbolo.isdigit():
                estado = 28
            else:
                semTransicao = True
        case 28:
            if simbolo.isdigit():
                estado = 29
            else:
                semTransicao = True
        case 29:
            if simbolo.isdigit():
                estado = 12
            else:
                semTransicao = True
        case 31:
            if simbolo.isdigit() or simbolo in ["A", "B", "C", "D", "E", "F"]:
                estado = 32
            else:
                semTransicao = True
        case 32:
            if simbolo.isdigit() or simbolo in ["A", "B", "C", "D", "E", "F"]:
                estado = 32
            else:
                semTransicao = True
        case 34:
            if simbolo == '"':
                estado = 35
            elif simbolo == "\n":
                semTransicao = True
            else:
                estado = 34
        case 35:
            semTransicao = True
        case 38:
            if simbolo.isalpha() and simbolo.isupper():
                estado = 39
            elif simbolo.isalpha() and simbolo.islower():
                estado = 54
            else:
                semTransicao = True
        case 39:
            if simbolo.isalpha() and simbolo.islower():
                estado = 40
            else:
                semTransicao = True
        case 40:
            if simbolo.isalpha() and simbolo.isupper():
                estado = 39
            else:
                semTransicao = True
        case 48:
            if simbolo != ">":
                estado = 48
            elif simbolo == ">":
                estado = 49
        case 49:
            if simbolo != ">":
                estado = 48
            elif simbolo == ">":
                estado = 50
        case 50:
            if simbolo != ">":
                estado = 48
            elif simbolo == ">":
                estado = 52
        case 51:
            if simbolo == "<":
                estado = 48
            else:
                semTransicao = True
        case 52:
            semTransicao = True
        case 54:
            if simbolo.isalpha() and simbolo.islower() or simbolo == "_":
                estado = 54
            else:
                semTransicao = True
        case 56:
            semTransicao = True
        case 57:
            semTransicao = True
        case 58:
            semTransicao = True
        case 59:
            semTransicao = True
        case 60:
            semTransicao = True
        case 61:
            semTransicao = True
        case 62:
            semTransicao = True
        case 63:
            if simbolo == "<":
                estado = 51
            elif simbolo == ">":
                estado = 64
            elif simbolo == "=":
                estado = 65
            else:
                semTransicao = True
        case 64:
            semTransicao = True
        case 65:
            if simbolo == "=":
                estado = 66
            else:
                semTransicao = True
        case 66:
            semTransicao = True
        case 71:
            if simbolo == "=":
                estado = 72
            else:
                semTransicao = True
        case 72:
            semTransicao = True
        case 79:
            if simbolo != "\n":
                estado = 80
            else:
               semTransicao = True
        case 80:
            if simbolo != "\n":
                pass
            else:
                semTransicao = True
        case 84:
            semTransicao = True
        case 86:
            semTransicao = True
        case 88:
            semTransicao = True
        case _:
            erro = True

    if (semTransicao):
        print(estado, lexema_atual, simbolo, "dsa")
        print(lexema_atual == " ")
        if (lexema_atual not in ["", " ", "\n"]):
            token = verificar_aceitacao(lin, col, lexema_atual, estado)
            if (token):
                tokens.append(token)
                if token[2] in somatorio:
                    somatorio[token[2]] += 1
                else:
                    somatorio[token[2]] = 1
                lexema_atual = ""
                estado = 0
                semTransicao = False
                if simbolo == " ":
                    col += 1
                    continue
                elif simbolo == "\n":
                    lin += 1
                    col = 1
                    continue
                estado = getPrimeiraTransicao(simbolo)
            else:
                erro = True
                semTransicao = False
        else:
            if simbolo in [" ", "\t"]:
                lexema_atual = ""
                col += 1
                continue
            elif simbolo == "\n":
                lexema_atual = ""
                lin += 1
                col = 1
                continue

            estado = getPrimeiraTransicao(simbolo)
            if (estado == -1):
                erros.append((lin, col, f"Erro lin {lin} col {col}: simbolo não reconhecido"))
                estado = 0
                lexema_atual = ""
                semTransicao = False
                col += 1
                continue
            else:
                semTransicao = False

    # Se ocorrer um erro, imprimir mensagem e reiniciar análise
    if(erro):
      print(f"ERRO - Simbolo não reconhecido: {lexema_atual}{simbolo} <")
      erros.append((lin, col, f"Erro lin {lin} col {col}: {listaErros[estado]}"))

      estado = 0

      if (simbolo == " "):
        col += 1
        lexema_atual = ""
        erro = False
        continue
      elif (simbolo == "\n"):
        lin += 1
        col = 1
        lexema_atual = ""
        erro = False
        continue
      else:
        col += 1
        
      estado = getPrimeiraTransicao(simbolo)
      if (estado == -1):
        erros.append((lin, col, f"Erro lin {lin} col {col}: simbolo não reconhecido"))
        estado = 0
        lexema_atual = ""
      else:
        lexema_atual = simbolo  
      erro = False
      continue

    # Adicionar o símbolo atual ao lexema e incrementar a coluna
    lexema_atual += simbolo
    if (simbolo == "\n"):
      lin += 1
      col = 1
    else:
      col += 1


  # Verificar se o estado final é de aceitação
  if (lexema_atual):
    token = verificar_aceitacao(lin, col, lexema_atual, estado)
    if (token):
      tokens.append(token)
      if token[2] in somatorio:
        somatorio[token[2]] += 1
      else:
        somatorio[token[2]] = 1
      lexema_atual = ""
    else:
      print(f"ERRO - Token não reconhecido: {lexema_atual} <")
      erros.append((lin, col, f"Erro lin {lin} col {col}: Token inválido"))


  return tokens, erros, somatorio


def imprimir_linha(lin, col, token, lexema):
  # Função para imprimir uma linha da tabela de tokens
  # Utiliza formatação para alinhar os valores (exemplo: {:<4} alinha o valor à esquerda em 4 espaços)
  print("| {:<4} | {:<4} | {:<15} | {:<25} |".format(lin, col, token, lexema))


def imprimir_tabela(tabela):
  # Função para imprimir a tabela de tokens
  print("+------+-----+------------------+---------------------------+")
  print("| LIN  | COL | TOKEN            | LEXEMA                    |")
  print("+------+-----+------------------+---------------------------+")
  for (lin, col, token, lexema) in tabela:
    imprimir_linha(lin, col, token, lexema)
  print("+------+-----+------------------+---------------------------+")
  
def imprimir_somatorio(dados):
  # Função para imprimir a tabela de somatório
  print("+------------------+------+")
  print("| TOKEN            | USOS |")
  print("+------------------+------+")
  for (token, usos) in dados.items():
    print("| {:<16} | {:>4} |".format(token, usos))
  print("+------------------+------+")


def main():
  cadeia = open("Ex-03-incorreto.cic", "r").read()
  
  codigo = open("Ex-03-incorreto.cic", "r").readlines()
  codigo = [linha.strip("\n") for linha in codigo]
  
  for index, linha in enumerate(codigo, start=1):
    codigo[index - 1] = f"[{index}] {linha}"

  tokens, erros, somatorio = ler_token(cadeia)
  imprimir_tabela(tokens)
  imprimir_somatorio(somatorio)

  for linha, index in enumerate(codigo, start=1):
    print(codigo[linha - 1])

    for erro in erros:
      if (erro[0] == linha):
        print("   ", end="")
        for _ in range(erro[1] - 1):
          print("-", end="")
        print("^")
    for erro in erros:
      if (erro[0] == linha):
        print(f"   {erro[2]}")

main()