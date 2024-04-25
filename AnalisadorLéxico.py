from estadosDeAceitação import estados # lista de estados de aceitação
from erros import listaErros # lista de erros

def verificar_aceitacao(lin, col, lexema_atual, estado):
  # Verifica se o estado atual é de aceitação e retorna o token correspondente

  if estado in estados['TK_INT']:
    return (lin, col - len(lexema_atual), "TK_INT", lexema_atual)
  elif estado in estados['TK_FLOAT']:
    return (lin, col - len(lexema_atual), "TK_FLOAT", lexema_atual)
  elif estado in estados['TK_END']:
    return (lin, col - len(lexema_atual), "TK_END", lexema_atual)
  elif estado in estados['TK_CADEIA']:
    return (lin, col - len(lexema_atual), "TK_CADEIA", lexema_atual)
  elif estado in estados['TK_ID']:
    return (lin, col - len(lexema_atual), "TK_ID", lexema_atual)
  elif estado in estados['TK_DATA']:
    return (lin, col - len(lexema_atual), "TK_DATA", lexema_atual)
  elif estado in estados['TK_COMENT_LINHA']:
    return (lin, col - len(lexema_atual), "TK_COMENT_LINHA", lexema_atual)
  elif estado in estados['TK_COMENT_BLOCO']:
    for simbolo in lexema_atual:
      if simbolo == "\n":
        lin -= 1
    return (lin, 1, "TK_COMENT_BLOCO", lexema_atual)
  elif lexema_atual in estados['palavrasReservadas']:
    return (lin, col - len(lexema_atual), f"TK_{lexema_atual.upper()}", '')
  else:
    # Verifica se o lexema atual é um operador ou delimitador
    for operador, nome_operador in estados['operadores']:
        if lexema_atual == operador:
            return (lin, col - len(lexema_atual), f"TK_{nome_operador.upper()}", '')

    for delimitador, nome_delimitador in estados['delimitadores']:
        if lexema_atual == delimitador:
            return (lin, col - len(lexema_atual), f"TK_{nome_delimitador.upper()}", '')
  
  return ()

def getPrimeiraTransicao(simbolo):
    # Retorna a transição a partir do estado 0 para o símbolo recebido como parâmetro

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
        return -1 # Símbolo não reconhecido

def analisador_lexico(codigo: str):
  """
  Função responsável por realizar a análise léxica do código fonte, simulando o funcionamento do autômato.
  O retorno da função é uma lista de tokens, uma lista de erros e um somatório de tokens.
  """

  # Estado inicial do autômato
  estado = 0

  # Variáveis que serão utilizadas para construir a lista de tokens
  lin = 1
  col = 1
  lexema_atual = ""
  tokens = []

  # Variáveis de controle
  semTransicao = False
  erro = False

  # Variáveis para armazenar os erros e o somatório de tokens
  erros = []
  somatorio = {}

  for simbolo in codigo:
    # Realiza a transição de estado de acordo com o simbolo consumido
    # Cada 'case' representa um estado do autômato e as transições possíveis
    # semTransicao é uma variável de controle que indica se houve transição de estado ou não
    # Se não houver transição, o autômato tenta reconhecer o lexema atual
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
                estado = 79
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
        # Se não houver transição de estado, verificar se o lexema atual é um token válido
        if (lexema_atual not in ["", " ", "\n"]):
            token = verificar_aceitacao(lin, col, lexema_atual, estado)
            if (token):
                # Se o lexema atual for um token válido, adicionar à lista de tokens e incrementar o somatório
                # Reiniciar o lexema atual e o estado
                tokens.append(token)
                if token[2] in somatorio:
                    somatorio[token[2]] += 1
                else:
                    somatorio[token[2]] = 1
                lexema_atual = ""
                estado = 0
                semTransicao = False
                # Se o símbolo atual for um espaço, incrementar a coluna e continuar a análise
                # Se o símbolo atual for um \n, incrementar a linha e reiniciar a coluna
                if simbolo == " ":
                    col += 1
                    continue
                elif simbolo == "\n":
                    lin += 1
                    col = 1
                    continue
                # Se o símbolo atual não for um espaço ou \n, tentar realizar a primeira transição de estado
                estado = getPrimeiraTransicao(simbolo)
            else:
                erro = True
                semTransicao = False
        else:
            # Se o lexema atual for vazio, espaço ou \n, reiniciar o lexema atual e o estado
            # Se o símbolo atual for um espaço, incrementar a coluna e continuar a análise
            # Se o símbolo atual for um \n, incrementar a linha e reiniciar a coluna
            if simbolo in [" ", "\t"]:
                lexema_atual = ""
                col += 1
                continue
            elif simbolo == "\n":
                lexema_atual = ""
                lin += 1
                col = 1
                continue

            # Se o símbolo atual não for um espaço ou \n, tentar realizar a primeira transição de estado
            # Se o símbolo não for reconhecido, adicionar um erro à lista de erros
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

    if(erro):
      # Se ocorrer um erro, imprimir mensagem e reiniciar análise
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

      # Se o símbolo atual não for um espaço ou \n, tentar realizar a primeira transição de estado
      estado = getPrimeiraTransicao(simbolo)
      if (estado == -1):
        erros.append((lin, col, f"Erro lin {lin} col {col}: simbolo não reconhecido"))
        estado = 0
        lexema_atual = ""
      else:
        lexema_atual = simbolo  
      erro = False
      continue

    # Adicionar o símbolo atual ao lexema, incrementar a coluna ou pular linha e continuar a análise
    lexema_atual += simbolo
    if (simbolo == "\n"):
      lin += 1
      col = 1
    else:
      col += 1


  # Ao sair do loop, verificar se o estado final para o lexema restante é de aceitação
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
      erros.append((lin, col, f"Erro lin {lin} col {col}: Token inválido"))


  return tokens, erros, somatorio

def imprimir_tabela(tabela):
  # Função para imprimir a tabela de tokens
  print("+------+-----+------------------+---------------------------+")
  print("| LIN  | COL | TOKEN            | LEXEMA                    |")
  print("+------+-----+------------------+---------------------------+")
  for (lin, col, token, lexema) in tabela:
    print("| {:<4} | {:<4} | {:<15} | {:<25} |".format(lin, col, token, lexema))
  print("+------+-----+------------------+---------------------------+")
  
def imprimir_somatorio(dados):
  # Função para imprimir a tabela de somatório
  dados = dict(sorted(dados.items(), key=lambda item: item[1], reverse=True))

  print("+------------------+------+")
  print("| TOKEN            | USOS |")
  print("+------------------+------+")
  for (token, usos) in dados.items():
    print("| {:<16} | {:>4} |".format(token, usos))
  print("+------------------+------+")

def imprimir_codigo(arquivo, erros):
    # Função para imprimir o código fonte com os erros
    codigo = open(arquivo, "r").readlines()
    codigo = [linha.strip("\n") for linha in codigo]
    
    for index, linha in enumerate(codigo, start=1):
        codigo[index - 1] = f"[{index}] {linha}"
    
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


def main():
  # Definir o arquivo a ser analisado
  arquivo = "Ex-01-correto.cic"

  codigo = open(arquivo, "r").read()

  tokens, erros, somatorio = analisador_lexico(codigo)

  imprimir_codigo(arquivo, erros)
  imprimir_tabela(tokens)
  imprimir_somatorio(somatorio)


main()