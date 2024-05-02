from Token import Token
from Error import Error

class Parser():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.tokens.append(Token("EOF", "EOF", -1, -1))
        self.errores = []

    def recuperar(self, nombreTokenSincronizacion):
        while self.tokens[0].name != "EOF":
            tk = self.tokens.pop(0)
            if tk.name == nombreTokenSincronizacion:
                break

    def parse(self):
        self.inicio()
        return self.errores

    def agregar_error(self, error):
        self.errores.append(error)

    #<inicio> ::= <elemento> <otro_elemento>
    def inicio(self):
        self.elemento()
        self.otro_elemento()
        if not self.errores:
            self.errores = []

    #<elemento> ::= LLAVE_APERTURA <instruccionID> <instruccionER> <instruccionCadenas> LLAVE_CIERRE
    def elemento(self):
        if self.tokens[0].name == "LLAVE_APERTURA":
            self.tokens.pop(0) #Se extrae el token validado

            self.instruccionID()
            self.instruccionER()
            self.instruccionCadenas()

            if self.tokens[0].name == "LLAVE_CIERRE":
                self.tokens.pop(0)
            else:
                error = Error("Se esperaba una llave de cierre '}'", self.tokens[0].line, self.tokens[0].column)
                self.agregar_error(error)
                self.recuperar("LLAVE_CIERRE")
        else:
            error = Error("Se esperaba una llave de apertura '{'", self.tokens[0].line, self.tokens[0].column)
            self.agregar_error(error)
            self.recuperar("LLAVE_APERTURA")

    # <otro_elemento> ::= COMA <elemento> <otro_elemento>
    #                  | epsilon
    def otro_elemento(self):
        if self.tokens[0].name == "COMA":
            self.tokens.pop(0)
            self.elemento()
            self.otro_elemento()

    #<instruccionID> ::= PALABRA_RESERVADA_ID DOS_PUNTOS NUMERO_ENTERO PUNTO_COMA
    def instruccionID(self):
        if self.tokens[0].name == "PALABRA_RESERVADA_ID":
            self.tokens.pop(0)
            if self.tokens[0].name == "DOS_PUNTOS":
                self.tokens.pop(0)
                if self.tokens[0].name == "NUMERO_ENTERO":
                    self.tokens.pop(0)
                    if self.tokens[0].name == "PUNTO_COMA":
                        self.tokens.pop(0)
                    else:
                        error = Error("Se esperaba ';'", self.tokens[0].line, self.tokens[0].column)
                        self.agregar_error(error)
                else:
                    error = Error("Se esperaba un entero", self.tokens[0].line, self.tokens[0].column)
                    self.agregar_error(error)
                    self.recuperar("PUNTO_COMA")
            else:
                error = Error("Se esperaba ':'", self.tokens[0].line, self.tokens[0].column)
                self.agregar_error(error)
                self.recuperar("PUNTO_COMA")
        else:
            error = Error("Se esperaba la palabra reservada 'ID'", self.tokens[0].line, self.tokens[0].column)
            self.agregar_error(error)
            self.recuperar("PUNTO_COMA")

    #<instruccionER> ::= PALABRA_RESERVADA_ER DOS_PUNTOS <expresion> <otraExpresion> PUNTO_COMA
    def instruccionER(self):
        if self.tokens[0].name == "PALABRA_RESERVADA_ER":
            self.tokens.pop(0)
            if self.tokens[0].name == "DOS_PUNTOS":
                self.tokens.pop(0)

                self.expresion()
                self.otraExpresion()

                if self.tokens[0].name == "PUNTO_COMA":
                    self.tokens.pop(0)
                else:
                    error = Error("Se esperaba ';' y se obtuvo '" + self.tokens[0].value + "'", self.tokens[0].line, self.tokens[0].column)
                    self.agregar_error(error)
            else:
                error = Error("Se esperaba ':'", self.tokens[0].line, self.tokens[0].column)
                self.agregar_error(error)
        else:
            error = Error("Se esperaba la palabra reservada 'ER'", self.tokens[0].line, self.tokens[0].column)
            self.agregar_error(error)

    #<expresion> ::= parA <expresion> parC <operador>
    #              | <elementoER> <operador>
    def expresion(self):
        if self.tokens[0].name == "PARENTESIS_ABRE":
            self.tokens.pop(0)

            self.expresion()

            if self.tokens[0].name == "PARENTESIS_CIERRA":
                self.tokens.pop(0)

                self.operador()
            else:
                error = Error("Se esperaba un parentesis de cierre", self.tokens[0].line, self.tokens[0].column)
                self.agregar_error(error)
        else:
            self.elementoER()
            self.operador()

    #<otraExpresion> ::= <expresion> <otraExpresion>
    #                  | epsilon
    def otraExpresion(self):
        if self.tokens[0].name == "PARENTESIS_ABRE" or self.tokens[0].name == "CADENA" or self.tokens[0].name == "NUMERO_ENTERO" or self.tokens[0].name == "NUMERO_DECIMAL":
            self.expresion()
            self.otraExpresion()

    #<operador> ::= <operadorUnario>
    #             | OR <expresion>
    #             | epsilon
    def operador(self):
        if self.tokens[0].name == "MAS" or self.tokens[0].name == "ASTERISCO" or self.tokens[0].name == "INTERROGACION":
            self.operadorUnario()
        elif self.tokens[0].name == "OR":
            self.tokens.pop(0)
            self.expresion()

    # <operadorUnario> ::= MAS
    #                    | ASTERISCO
    #                    | INTERROGACION
    def operadorUnario(self):
        if self.tokens[0].name == "MAS" or self.tokens[0].name == "ASTERISCO" or self.tokens[0].name == "INTERROGACION":
            self.tokens.pop(0)
        else:
            error = Error("Se esperaba un operador unario", self.tokens[0].line, self.tokens[0].column)
            self.agregar_error(error)

    # <elementoER> ::= CADENA
    #                | NUMERO_ENTERO
    #                | NUMERO_DECIMAL
    def elementoER(self):
        if self.tokens[0].name == "CADENA" or self.tokens[0].name == "NUMERO_ENTERO" or self.tokens[0].name == "NUMERO_DECIMAL":
            self.tokens.pop(0)
        else:
            error = Error("Se esperaba cadena, entero o decimal", self.tokens[0].line, self.tokens[0].column)
            self.agregar_error(error)

    #<instruccionCadenas> ::= CADENAs DOS_PUNTOS CADENA <otraCadena> PUNTO_COMA
    def instruccionCadenas(self):
        if self.tokens[0].name == "PALABRA_RESERVADA_CADENAS":
            self.tokens.pop(0)
            if self.tokens[0].name == "DOS_PUNTOS":
                self.tokens.pop(0)
                if self.tokens[0].name == "CADENA":
                    self.tokens.pop(0)

                    self.otraCadena()

                    if self.tokens[0].name == "PUNTO_COMA":
                        self.tokens.pop(0)
                    else:
                        error = Error("Se esperaba ';' y se obtuvo '" + self.tokens[0].value + "'", self.tokens[0].line, self.tokens[0].column)
                        self.agregar_error(error)
                else:
                    error = Error("Se esperaba una cadena", self.tokens[0].line, self.tokens[0].column)
                    self.agregar_error(error)
            else:
                error = Error("Se esperaba ':'", self.tokens[0].line, self.tokens[0].column)
                self.agregar_error(error)
        else:
            error = Error("Se esperaba la palabra reservada 'CADENAS'", self.tokens[0].line, self.tokens[0].column)
            self.agregar_error(error)

    # <otraCadena> ::= COMA CADENA <otraCadena>
    #                | epsilon
    def otraCadena(self):
        if self.tokens[0].name == "COMA":
            self.tokens.pop(0)
            if self.tokens[0].name == "CADENA":
                self.tokens.pop(0)
                self.otraCadena()
            else:
                error = Error("Se esperaba una cadena y se obtuvo " + self.tokens[0].name, self.tokens[0].line, self.tokens[0].column)
                self.agregar_error(error)
