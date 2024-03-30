class Analizador:
    def __init__(self):
        self.palabras_reservadas = ['Inicio', 'Encabezado', 'Cuerpo', 'Titulo', 'Fondo', 'Parrafo', 'Texto', 'Codigo', 'Negrita',
                                    'Subrayado', 'Tachado', 'Cursiva', 'Salto', 'Tabla', 'elemento', 'filas', 'columnas', 'elemento',
                                    'TituloPagina', 'texto', 'posicion', 'tamaño', 'color', 'fuente', 'cantidad']

    def analizador_lexico(self, entrada):
        ESTADO_INICIAL = 0
        ESTADO_TOKEN = 1
        ESTADO_NUMERO = 2
        ESTADO_CADENA = 3

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
                    tokens_lexemas.append(('LLAVE_APERTURA', caracter, linea_actual, columna_actual))
                elif caracter == '}':
                    tokens_lexemas.append(('LLAVE_CIERRE', caracter, linea_actual, columna_actual))
                elif caracter == ':':
                    tokens_lexemas.append(('DOS_PUNTOS', caracter, linea_actual, columna_actual))
                elif caracter == ';':
                    tokens_lexemas.append(('PUNTO_COMA', caracter, linea_actual, columna_actual))
                elif caracter == ',':
                    tokens_lexemas.append(('COMA', caracter, linea_actual, columna_actual))
                elif caracter == '[':
                    tokens_lexemas.append(('CORCHETE_APERTURA', caracter, linea_actual, columna_actual))
                elif caracter == ']':
                    tokens_lexemas.append(('CORCHETE_CIERRE', caracter, linea_actual, columna_actual))
                elif caracter == '=':
                    tokens_lexemas.append(('SIGNO_IGUAL', caracter, linea_actual, columna_actual))
                elif caracter == '"':
                    lexema_actual += caracter
                    estado_actual = ESTADO_CADENA
                elif caracter.isalpha():
                    lexema_actual += caracter
                    estado_actual = ESTADO_TOKEN
                elif caracter.isdigit():
                    lexema_actual += caracter
                    estado_actual = ESTADO_NUMERO
                else:
                    caracteres_no_permitidos.append((caracter, linea_actual, columna_actual))
                
            elif estado_actual == ESTADO_TOKEN:
                if caracter.isalpha() or caracter.isdigit() or caracter == '_':
                    lexema_actual += caracter
                else:
                    if lexema_actual in self.palabras_reservadas:
                        tokens_lexemas.append(('PALABRA_RESERVADA', lexema_actual, linea_actual, columna_actual))
                    else:
                        caracteres_no_permitidos.append((lexema_actual, linea_actual, columna_actual))
                    lexema_actual = ''
                    estado_actual = ESTADO_INICIAL
                    continue
            
            elif estado_actual == ESTADO_NUMERO:
                if caracter.isdigit():
                    lexema_actual += caracter
                else:
                    tokens_lexemas.append(('NUMERO', lexema_actual, linea_actual, columna_actual))
                    lexema_actual = ''
                    estado_actual = ESTADO_INICIAL
                    continue
            
            elif estado_actual == ESTADO_CADENA:
                if caracter == '"':
                    lexema_actual += caracter
                    tokens_lexemas.append(('CADENA', lexema_actual, linea_actual, columna_actual))
                    lexema_actual = ''
                    estado_actual = ESTADO_INICIAL
                else:
                    lexema_actual += caracter
            
            posicion_actual += 1
        return tokens_lexemas, caracteres_no_permitidos