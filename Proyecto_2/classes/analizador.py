from Token import Token

class Analizador:
  def __init__(self):
      self.palabras_reservadas = ['ID', 'ER', 'CADENAS']

  def analizador_lexico(self, entrada):
    ESTADO_INICIAL = 0
    ESTADO_TOKEN = 1
    ESTADO_NUMERO_ENTERO = 2
    ESTADO_NUMERO_DECIMAL = 3
    ESTADO_CADENA = 4
    ESTADO_COMENTARIO_LINEA = 5
    ESTADO_COMENTARIO_MULTILINEA = 6

    tokens_lexemas = []
    caracteres_no_permitidos = []
    lexema_actual = ''
    estado_actual = ESTADO_INICIAL
    posicion_actual = 0
    linea_actual = 1
    columna_actual = 1

    while posicion_actual < len(entrada):
      caracter = entrada[posicion_actual]

      if caracter == '\n':
        linea_actual += 1
        columna_actual = 1
      else:
        columna_actual += 1

      if estado_actual == ESTADO_INICIAL:
        if caracter.isspace():
          # Se ignora espacios en blanco
          pass
        elif caracter == '{':
          tokens_lexemas.append(
              Token('LLAVE_APERTURA', caracter, linea_actual, columna_actual))
        elif caracter == '}':
          tokens_lexemas.append(
              Token('LLAVE_CIERRE', caracter, linea_actual, columna_actual))
        elif caracter == ':':
          tokens_lexemas.append(
              Token('DOS_PUNTOS', caracter, linea_actual, columna_actual))
        elif caracter == ';':
          tokens_lexemas.append(
              Token('PUNTO_COMA', caracter, linea_actual, columna_actual))
        elif caracter == ',':
          tokens_lexemas.append(
              Token('COMA', caracter, linea_actual, columna_actual))
        elif caracter == '[':
          tokens_lexemas.append(
              Token('CORCHETE_APERTURA', caracter, linea_actual,
                    columna_actual))
        elif caracter == ']':
          tokens_lexemas.append(
              Token('CORCHETE_CIERRE', caracter, linea_actual, columna_actual))
        elif caracter == '?':
          tokens_lexemas.append(
              Token('INTERROGACION', caracter, linea_actual, columna_actual))
        elif caracter == '|':
          tokens_lexemas.append(
              Token('OR', caracter, linea_actual, columna_actual))
        elif caracter == '*':
          tokens_lexemas.append(
              Token('ASTERISCO', caracter, linea_actual, columna_actual))
        elif caracter == '(':
          tokens_lexemas.append(
              Token('PARENTESIS_ABRE', caracter, linea_actual, columna_actual))
        elif caracter == ')':
          tokens_lexemas.append(
              Token('PARENTESIS_CIERRA', caracter, linea_actual,
                    columna_actual))
        elif caracter == '+':
          tokens_lexemas.append(
              Token('MAS', caracter, linea_actual, columna_actual))
        elif caracter == '=':
          tokens_lexemas.append(
              Token('SIGNO_IGUAL', caracter, linea_actual, columna_actual))
        elif caracter == '"':
          lexema_actual += caracter
          estado_actual = ESTADO_CADENA
        elif caracter.isalpha():
          lexema_actual += caracter
          estado_actual = ESTADO_TOKEN
        elif caracter.isdigit():
          lexema_actual += caracter
          estado_actual = ESTADO_NUMERO_ENTERO
        elif caracter == '-':
          lexema_actual += caracter
          estado_actual = ESTADO_NUMERO_ENTERO
        elif caracter == '#':
          estado_actual = ESTADO_COMENTARIO_LINEA
        elif caracter == "'":
          estado_actual = ESTADO_COMENTARIO_MULTILINEA
        else:
          caracteres_no_permitidos.append(
              (caracter, linea_actual, columna_actual))

      elif estado_actual == ESTADO_TOKEN:
        if caracter.isalpha() or caracter.isdigit() or caracter == '_':
          lexema_actual += caracter
        else:
          if lexema_actual in self.palabras_reservadas:
            tokens_lexemas.append(
                Token('PALABRA_RESERVADA_' + lexema_actual, lexema_actual,
                      linea_actual, columna_actual))
          else:
            caracteres_no_permitidos.append(
                (lexema_actual, linea_actual, columna_actual))
          lexema_actual = ''
          estado_actual = ESTADO_INICIAL
          continue

      elif estado_actual == ESTADO_NUMERO_ENTERO:
        if caracter.isdigit():
          lexema_actual += caracter
        elif caracter == '.':
          lexema_actual += caracter
          estado_actual = ESTADO_NUMERO_DECIMAL
        else:
          tokens_lexemas.append(
              Token('NUMERO_ENTERO', lexema_actual, linea_actual,
                    columna_actual))
          lexema_actual = ''
          estado_actual = ESTADO_INICIAL
          continue

      elif estado_actual == ESTADO_NUMERO_DECIMAL:
        if caracter.isdigit():
          lexema_actual += caracter
        else:
          tokens_lexemas.append(
              Token('NUMERO_DECIMAL', lexema_actual, linea_actual,
                    columna_actual))
          lexema_actual = ''
          estado_actual = ESTADO_INICIAL
          continue

      elif estado_actual == ESTADO_CADENA:
        if caracter == '"':
          lexema_actual += caracter
          tokens_lexemas.append(
              Token('CADENA', lexema_actual, linea_actual, columna_actual))
          lexema_actual = ''
          estado_actual = ESTADO_INICIAL
        else:
          lexema_actual += caracter

      elif estado_actual == ESTADO_COMENTARIO_LINEA:
        if caracter == '\n':
          tokens_lexemas.append(
              Token('COMENTARIO_LINEA', lexema_actual, linea_actual,
                    columna_actual))
          lexema_actual = ''
          estado_actual = ESTADO_INICIAL
        else:
          lexema_actual += caracter

      elif estado_actual == ESTADO_COMENTARIO_MULTILINEA:
        if caracter == "'":
          lexema_actual += caracter
          if lexema_actual.endswith("'''"):
            tokens_lexemas.append(
                Token('COMENTARIO_MULTILINEA', lexema_actual, linea_actual,
                      columna_actual))
            lexema_actual = ''
            estado_actual = ESTADO_INICIAL
        else:
          lexema_actual += caracter

      posicion_actual += 1

    return tokens_lexemas, caracteres_no_permitidos
