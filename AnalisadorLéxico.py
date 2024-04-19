def verificar_aceitacao(lin, col, lexema_atual, estado):
  token = ()
  aceitacaoInt = [1, 2, 3, 9]
  aceitacaoFloat = [5, 7]
  aceitacaoEnd = [32]

  if estado in aceitacaoInt:
    token = (lin, col - len(lexema_atual), "TK_INT", lexema_atual)
  elif estado in aceitacaoFloat:
    token = (lin, col - len(lexema_atual), "TK_FLOAT", lexema_atual)
  elif estado in aceitacaoEnd:
    token = (lin, col - len(lexema_atual), "TK_END", lexema_atual)
  
  return token


def ler_token(cadeia: str):
  """
  Essa é a função responsável por receber a cadeia de caracteres e retornar uma lista de tokens.
  O retorno da função é uma tabela de tokens, onde cada token é representado como uma tupla contendo a linha, a coluna, o tipo e o lexema do token.
  """

  # Estado inicial do autômato
  estado = 0

  # Estados de aceitação para inteiros e floats
  aceitacaoInt = [1, 2, 3, 9]
  aceitacaoFloat = [5, 7]

  # Inicialização de variáveis que serão utilizadas para construir a lista de tokens
  lin = 1
  col = 1
  lexema_atual = ""
  tokens = []

  # Variável para controle de erro
  erro = False

  for simbolo in cadeia:
    if (simbolo.isdigit()):
      # match/case que representa as transições de estado do autômato ao consumir um dígito
      match(int(estado)):
        case 0:
          estado = 1
        case 1:
          estado = 2
        case 2:
          estado = 3
        case 3:
          estado = 9
        case 9:
          estado = 9
        case 4:
          estado = 5
        case 5:
          estado = 5
        case 6:
          estado = 7
        case 7:
          estado = 7
        case 8:
          estado = 7
        case 31:
          estado = 32
        case 32:
          estado = 32

    elif (simbolo == "."):
      # Transições de estado ao consumir um ponto
      if(estado == 0):
        estado = 4
      elif (estado == 1 or estado == 2 or estado == 3):
        estado = 5
      else:
        erro = True

    elif (simbolo == "e"):
      # Transições de estado ao consumir um 'e'
      if (estado == 5):
        estado = 6
      else:
        erro = True

    elif (simbolo == "-"):
      # Transições de estado ao consumir um '-'
      if (estado == 6):
        estado = 8
      else:
        erro = True

    elif (simbolo in ["A", "B", "C", "D", "E", "F"]):
      print(estado)
      if(estado == 0):
        estado = 14
      elif (estado == 31 or estado == 32):
        estado = 32
      else:
        erro = True

    elif (simbolo == "x"):
      if (estado == 1 or estado == 14):
        estado = 31
      else:
        erro = True

    elif (simbolo == " "):
      # Se encontrar um espaço, verificar se o estado atual é de aceitação para int ou float
      token = verificar_aceitacao(lin, col, lexema_atual, estado)
      if (token):
        tokens.append(token)
        lexema_atual = ""
        estado = 0
        col += 1
        continue
      else:
        erro = True

    else:
      erro = True

    # Se ocorrer um erro, imprimir mensagem e reiniciar análise
    if(erro):
      print(f"ERRO - Simbolo não reconhecido: {lexema_atual}{simbolo} <")
      lexema_atual = ""
      estado = 0
      col += 1
      erro = False
      continue

    # Adicionar o símbolo atual ao lexema e incrementar a coluna
    lexema_atual += simbolo
    col += 1

  # Verificar se o estado final é de aceitação para int ou float
  token = verificar_aceitacao(lin, col, lexema_atual, estado)
  if (token):
    tokens.append(token)
    lexema_atual = ""
  else:
    print(f"ERRO - Token não reconhecido: {lexema_atual} <")

  return tokens


def imprimir_linha(lin, col, token, lexema):
  # Função para imprimir uma linha da tabela de tokens
  # Utiliza formatação para alinhar os valores (exemplo: {:<4} alinha o valor à esquerda em 4 espaços)
  print("| {:<4} | {:<4} | {:<15} | {:<10} |".format(lin, col, token, lexema))


def imprimir_tabela(tabela):
  # Função para imprimir a tabela de tokens
  print("+------+-----+-----------------+-----------+")
  print("| LIN  | COL | TOKEN           | LEXEMA    |")
  print("+------+-----+-----------------+-----------+")
  for (lin, col, token, lexema) in tabela:
    imprimir_linha(lin, col, token, lexema)
  print("+------+-----+-----------------+-----------+")


def main():
  cadeia = "123 235.12321e-10 Ax321ABCDEFFFFF213"
  tokens = ler_token(cadeia)
  imprimir_tabela(tokens)


main()