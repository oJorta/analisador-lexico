from estadosDeAceitação import estados

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
  erros = []

  for simbolo in cadeia:
    if (simbolo == '"'):
      if estado == 0:
        estado = 34
      elif estado == 34:
        estado = 35
        lexema_atual += simbolo
        tokens.append((lin, col, lexema_atual, "TK_CADEIA"))
        estado = 0
        lexema_atual = ""
        col += 1
        continue
      elif estado == 54:
        token = verificar_aceitacao(lin, col, lexema_atual, estado)
        if (token):
          tokens.append(token)
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col - len(lexema_atual)}: Palavra reservada não encontrada"))
        erros.append((lin, col, f"Erro lin {lin} col {col}: Cadeia não fechada"))
      elif estado in [48, 49, 50]:
        pass
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Cadeia não fechada"))

    if (simbolo == '\n'):
      if (estado == 34):
        erros.append((lin, col, f"Erro lin {lin} col {col}: Cadeia não fechada"))
        erro = True
        lin += 1
        col = 1
      elif (estado in [48, 49, 50]):
        pass
      else:
        if (lexema_atual):
          token = verificar_aceitacao(lin, col, lexema_atual, estado)
          if (token):
            tokens.append(token)
          else:
            erros.append((lin, col, f"Erro lin {lin} col {col}: Token inválido"))
            """ erro = True """
        
        lexema_atual = ""
        estado = 0
        lin += 1
        col = 1
        continue

    if (estado == 34 and simbolo != '\n'):
      lexema_atual += simbolo
      col += 1
      continue
    
    if (estado == 79):
      estado = 80
    
    if (estado == 80):
      lexema_atual += simbolo
      col += 1
      continue

    if (estado in [48, 49, 50] and simbolo != '>'):
      estado = 48
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
      elif (estado == 54 and simbolo.islower() or estado == 0 and simbolo.isupper()):
        pass
      else:
        erros.append((lin, col, f"Erro lin {lin} col {col}: Identificador inválido"))
        erro = True

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
        case 15:
          estado = 16
        case 16:
          estado = 17
        case 18:
          estado = 19
        case 19:
          estado = 20
        case 20:
          estado = 21
        case 21:
          estado = 12
        case 23:
          estado = 24
        case 24:
          estado = 25
        case 26:
          estado = 27
        case 27:
          estado = 28
        case 28:
          estado = 29
        case 29:
          estado = 12
        case _:
          erro = True
          if estado in [12, 17, 25]:
            erros.append((lin, col, f"Erro lin {lin} col {col}: Data mal formatada"))
          

    if (simbolo == "."):
      # Transições de estado ao consumir um ponto
      if(estado == 0):
        estado = 4
      elif (estado == 1 or estado == 2 or estado == 3):
        estado = 5
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Ponto inválido"))

    # Transições de estado ao consumir um 'e'
    if (simbolo == "e" and estado == 5):
      estado = 6

    # Transições de estado ao consumir um '-'
    if (simbolo == "-" and estado == 6):
      estado = 8
      lexema_atual += simbolo
      col += 1
      continue

    if (simbolo in ["A", "B", "C", "D", "E", "F"] and estado not in [38, 39, 40]):
      if (estado == 0):
        estado = 14
      elif (estado == 31 or estado == 32):
        estado = 32
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Hexadecimal inválido"))
    elif (simbolo.isalpha() and simbolo.isupper() and estado not in [38, 39, 40]):
      erro = True
      erros.append((lin, col, f"Erro lin {lin} col {col}: Identificador inválido"))

    if (simbolo == "x"):
      if (estado == 1 or estado == 14):
        estado = 31
      elif (estado in [0, 38, 39, 54]):
        pass
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Hexadecimal inválido"))

    if (simbolo == '/'):
      if (estado == 2):
        estado = 15
      elif (estado == 17):
        estado = 18
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Símbolo inválido"))

    if (simbolo == '_'):
      if (estado == 2):
        estado = 23
      elif (estado == 25):
        estado = 26
      elif (estado == 54):
        pass
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Símbolo inválido"))

    if (simbolo == '<'):
      if (estado == 0):
        estado = 63
      elif (estado == 63):
        estado = 51
      elif (estado == 51):
        estado = 48
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Símbolo inválido"))
    
    if (simbolo == '>'):
      if (estado == 0):
        estado = 71
      elif (estado == 48):
        estado = 49
      elif (estado == 49):
        estado = 50
      elif (estado == 50):
        tokens.append((lin, col - len(lexema_atual), "TK_COMENT", lexema_atual + simbolo))
        lexema_atual = ""
        estado = 0
        col += 1
        continue
      elif (estado == 63):
        tokens.append((lin, col - len(lexema_atual), "TK_DIFERENTE", lexema_atual + simbolo))
        lexema_atual = ""
        estado = 0
        col += 1
        continue
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Símbolo inválido"))

    if (simbolo == '='):
      if (estado == 0):
        estado = 75
      elif (estado == 75):
        tokens.append((lin, col - len(lexema_atual), "TK_IGUAL_A", lexema_atual + simbolo))
        lexema_atual = ""
        estado = 0
        col += 1
        continue
      elif (estado == 71):
        tokens.append((lin, col - len(lexema_atual), "TK_MAIOR_IGUAL", lexema_atual + simbolo))
        lexema_atual = ""
        estado = 0
        col += 1
        continue
      elif (estado == 63):
        estado = 65
      elif (estado == 65):
        tokens.append((lin, col - len(lexema_atual), "TK_ATRIBUICAO", lexema_atual + simbolo))
        lexema_atual = ""
        estado = 0
        col += 1
        continue
      else:
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Símbolo inválido"))

    if (simbolo in ['+', '-', '*', '&', '%', '~', '|', ':', '(', ')']):
      if (estado == 0):
        tokens.append((lin, col - len(lexema_atual), f"TK_{simbolo}", lexema_atual + simbolo))
        lexema_atual = ""
        estado = 0
        col += 1
        continue
      else:
        token = verificar_aceitacao(lin, col, lexema_atual, estado)
        if (token):
          tokens.append(token)
          lexema_atual = ""
          estado = 0
          col += 1
          tokens.append((lin, col, f"TK_{simbolo}", simbolo))
          continue
        else:
          erro = True
          erros.append((lin, col, f"Erro lin {lin} col {col}: Símbolo inválido"))

    if (simbolo == '#'):
      if (estado == 0):
        estado = 79
      elif (estado == 79):
        estado = 80
      elif (estado not in [34, 48, 79, 80]):
        erro = True
        erros.append((lin, col, f"Erro lin {lin} col {col}: Símbolo inválido"))

    """ if (simbolo == '\n'):
      token = verificar_aceitacao(lin, col, lexema_atual, estado)
      if (token):
        tokens.append(token)
        lexema_atual = ""
        estado = 0

      lin += 1
      col = 1
      continue """

    if (simbolo == " " or simbolo == "\t"):
      # Se encontrar um espaço, verificar se o estado atual é de aceitação
      if (estado == 79):
        estado = 80
      elif (estado in [48, 49, 50, 80]):
        lexema_atual += simbolo
        col += 1
        continue
      elif (lexema_atual):
        token = verificar_aceitacao(lin, col, lexema_atual, estado)
        if (token):
          tokens.append(token)
          lexema_atual = ""
          estado = 0
          col += 1
          continue
        else:
          erros.append((lin, col, f"Erro lin {lin} col {col}: Token inválido"))
          erro = True
      else:
        col += 1
        continue
    
    
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

  # Verificar se o estado final é de aceitação
  if (lexema_atual):
    token = verificar_aceitacao(lin, col, lexema_atual, estado)
    if (token):
      tokens.append(token)
      lexema_atual = ""
    else:
      print(f"ERRO - Token não reconhecido: {lexema_atual} <")
      erros.append((lin, col, f"Erro lin {lin} col {col}: Token inválido"))


  return tokens, erros


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


def main():
  """ codigo = open("Ex-01-correto.cic", "r") """
  cadeia = open("Ex-03-incorreto.cic", "r").read()
  
  codigo = open("Ex-03-incorreto.cic", "r").readlines()
  codigo = [linha.strip("\n") for linha in codigo]
  
  for index, linha in enumerate(codigo, start=1):
    codigo[index - 1] = f"[{index}] {linha}"

  """ for linha in codigo:
    print(linha) """

  tokens, erros = ler_token(cadeia)
  imprimir_tabela(tokens)

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