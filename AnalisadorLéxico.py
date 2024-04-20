def verificar_aceitacao(lin, col, lexema_atual, estado):
  token = ()
  aceitacaoInt = [1, 2, 3, 9]
  aceitacaoFloat = [5, 7]
  aceitacaoEnd = [32]
  aceitacaoCadeia = [35]
  aceitacaoId = [39, 40]
  aceitacaoPalavraReservada = [54]

  if estado in aceitacaoInt:
    token = (lin, col - len(lexema_atual), "TK_INT", lexema_atual)
  elif estado in aceitacaoFloat:
    token = (lin, col - len(lexema_atual), "TK_FLOAT", lexema_atual)
  elif estado in aceitacaoEnd:
    token = (lin, col - len(lexema_atual), "TK_END", lexema_atual)
  elif estado in aceitacaoCadeia:
    token = (lin, col - len(lexema_atual), "TK_CADEIA", lexema_atual)
  elif estado in aceitacaoId:
    token = (lin, col - len(lexema_atual), "TK_ID", lexema_atual)
  elif estado in aceitacaoPalavraReservada:
    token = (lin, col - len(lexema_atual), f"TK_{lexema_atual.upper()}", lexema_atual)
  
  return token


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
  erro = False

  for simbolo in cadeia:
    if (simbolo == '"'):
      if estado == 0:
        estado = 34
      elif estado == 34:
        estado = 35
        lexema_atual += simbolo
        token = (lin, col - len(lexema_atual), "TK_CADEIA", lexema_atual)
        if (token):
          tokens.append(token)
          estado = 0
          col += 1
          continue  
        else:
          erro = True
      else:
        erro = True

    if (estado == 34):
      lexema_atual += simbolo
      col += 1
      continue

    if (simbolo.isalpha() and estado not in [1, 5, 14, 31, 32]):
      if(estado == 0 and simbolo.islower()):
        estado = 38
      elif (estado == 38 and simbolo.isupper()):
        estado = 39
      elif (estado == 38 and simbolo.islower()):
        estado = 54
      elif (estado == 39 and simbolo.islower()):
        estado = 40
      elif (estado == 40 and simbolo.isupper()):
        estado = 39
      elif (estado == 5 and simbolo == 'e' or estado == 14 and simbolo == 'x' or estado == 54 and simbolo.islower() or estado == 0 and simbolo.isupper()):
        pass
      else:
        erro = True
      """ elif (estado not in [1, 5, 31, 32] and not (simbolo in ["A", "B", "C", "D", "E", "F"] and estado == 0)):
        erro = True """

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
        case _:
          erro = True

    if (simbolo == "."):
      # Transições de estado ao consumir um ponto
      if(estado == 0):
        estado = 4
      elif (estado == 1 or estado == 2 or estado == 3):
        estado = 5
      else:
        erro = True

    # Transições de estado ao consumir um 'e'
    if (simbolo == "e" and estado == 5):
      estado = 6

    if (simbolo == "-"):
      # Transições de estado ao consumir um '-'
      if (estado == 6):
        estado = 8
      else:
        erro = True

    if (simbolo in ["A", "B", "C", "D", "E", "F"] and estado not in [38, 39, 40]):
      if (estado == 0):
        estado = 14
      elif (estado == 31 or estado == 32):
        estado = 32
      else:
        erro = True

    if (simbolo == "x"):
      if (estado == 1 or estado == 14):
        estado = 31
      elif (estado in [0, 38, 39, 54]):
        pass
      else:
        erro = True

    if (simbolo == " "):
      print(estado, lexema_atual)
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

    """ else:
      erro = True """

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
  """ cadeia = '123 235.12321e-10 Ax321ABCDEFFFFF213 "1312" aBcDeFF' """
  cadeia = '235.12321e-10 Ax321ABCDEFFFFF213 aBcDeF sdadasda'
  tokens = ler_token(cadeia)
  imprimir_tabela(tokens)


main()