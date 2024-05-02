from collections import defaultdict, deque

class Analizador_expresiones:
    def __init__(self):
        self.palabras_reservadas = ['ID', 'ER', 'CADENAS']
        self.caracteres_especiales = "( ) [ ] { } | ? * +".split()

    def obtener_expresiones_cadenas(self, tokens):
        resultado = []
        elemento_actual = {}
        leyendo_er = False
        er_tokens = []
        id_actual = None
    
        for i, token in enumerate(tokens):
            if token.get_name() == 'LLAVE_APERTURA':
                elemento_actual = {}
            elif token.get_name() == 'PALABRA_RESERVADA_ID':
                id_actual = tokens[i+2].get_value()
            elif token.get_name() == 'PALABRA_RESERVADA_ER':
                leyendo_er = True
                er_tokens = []
            elif leyendo_er:
                if token.get_name() == 'PUNTO_COMA':
                    leyendo_er = False
                    elemento_actual['ER'] = ''.join([t.get_value() for t in er_tokens])[1:]
                    er_tokens = []
                    elemento_actual['ID'] = id_actual
                    id_actual = None
                else:
                    er_tokens.append(token)
            elif token.get_name() == 'CADENA':
                if 'CADENAS' not in elemento_actual:
                    elemento_actual['CADENAS'] = []
                elemento_actual['CADENAS'].append(token.get_value())
            elif token.get_name() == 'LLAVE_CIERRE':
                resultado.append(elemento_actual)
    
        return resultado

    def rango_texto(self, inicio, fin):
        return "".join([chr(num) for num in range(ord(inicio), ord(fin) + 1)])

    def tokenizar(self, expresion_regular):
        simbolos_expresion = deque(expresion_regular)
        tokens_expresion = []

        def procesar_corchete_cuadrado():
            tokens_expresion.append(simbolo)
            siguiente_simbolo = simbolos_expresion.popleft()
            texto_corchete = []
            while siguiente_simbolo != "]":
                texto_corchete.append(siguiente_simbolo)
                siguiente_simbolo = simbolos_expresion.popleft()
            texto_corchete = "".join(texto_corchete)
            tokens_expresion.append(texto_corchete)
            # agregar corchete cuadrado de cierre
            tokens_expresion.append(siguiente_simbolo)

        def procesar_corchete_curvo(self):
            token_repeticion = tokens_expresion[-1]

            if token_repeticion == "]":
                token_repeticion = ["[", tokens_expresion[-2], "]"]

            elif token_repeticion == ")":
                grupo_coincidencia = deque()
                for token in reversed(tokens_expresion):
                    if token == "(":
                        grupo_coincidencia.appendleft(token)
                        break
                    grupo_coincidencia.appendleft(token)
                token_repeticion = list(grupo_coincidencia)

            else:
                token_repeticion = [token_repeticion]

            # obtener número que representa el mínimo número de repeticiones
            reps_min = int(simbolos_expresion.popleft())
            simbolos_expresion.popleft()  # eliminar coma
            # obtener número que representa el máximo número de repeticiones
            reps_max = int(simbolos_expresion.popleft())

            # agregar tokens de texto y ? donde sea necesario
            [tokens_expresion.extend(token_repeticion) for _ in range(reps_min - 1)]
            [tokens_expresion.extend(token_repeticion + ["?"]) for _ in range(reps_max - reps_min)]

            # eliminar el corchete curvo de cierre
            simbolos_expresion.popleft()

        while simbolos_expresion:
            simbolo = simbolos_expresion.popleft()
            if simbolo == "{":
                self.procesar_corchete_curvo()
            elif simbolo == "[":
                self.procesar_corchete_cuadrado()
            else:
                tokens_expresion.append(simbolo)

        return tokens_expresion

    def transiciones_match(self, expresion_regular):
        transiciones_coincidencia = defaultdict(list)
        for i, unidad in enumerate(expresion_regular):
            if i > 0 and expresion_regular not in self.caracteres_especiales:
                transiciones_coincidencia[i - 1].append(i)
        return transiciones_coincidencia

    def transiciones_epsilon(self, expresion_regular):
        transiciones_epsilon_dict = defaultdict(list)

        pila_indices_operadores = []
        for i, unidad in enumerate(expresion_regular):
            indice_parentesis_izq = i
            if unidad == "(" or unidad == "|":
                pila_indices_operadores.append(i)
            elif unidad == ")":
                lista_indices_o = []
                while True:
                    indice_op = pila_indices_operadores.pop(-1)
                    if expresion_regular[indice_op] == "|":
                        lista_indices_o.append(indice_op)
                    elif expresion_regular[indice_op] == "(":
                        indice_parentesis_izq = indice_op
                        # aristas de paréntesis izquierdo
                        [transiciones_epsilon_dict[indice_parentesis_izq].append(indice_o + 1) for indice_o in lista_indices_o]

                        # aristas de | 
                        [transiciones_epsilon_dict[indice_o].append(i) for indice_o in lista_indices_o]

                        break

            elif unidad == "]":
                indice_parentesis_izq = i - 2

            if (i < (len(expresion_regular) - 1)) and expresion_regular[i + 1] == "*":
                transiciones_epsilon_dict[indice_parentesis_izq].append(i + 1)
                transiciones_epsilon_dict[i + 1].append(indice_parentesis_izq)

            if (i < (len(expresion_regular) - 1)) and expresion_regular[i + 1] == "+":
                transiciones_epsilon_dict[i + 1].append(indice_parentesis_izq)

            if (i < (len(expresion_regular) - 1)) and expresion_regular[i + 1] == "?":
                transiciones_epsilon_dict[indice_parentesis_izq].append(i + 2)

            if unidad in self.caracteres_especiales and i < len(expresion_regular):
                transiciones_epsilon_dict[i].append(i + 1)

        return transiciones_epsilon_dict

    def dfs_digrafo(self, grafo, nodo):
        estados_alcanzables = []

        def encontrar_estados(grafo, nodo):
            if nodo not in grafo.keys():
                estados_alcanzables.append(nodo)
                return
            elif nodo in estados_alcanzables:
                return
            else:
                estados_alcanzables.append(nodo)
                for estado in grafo[nodo]:
                    encontrar_estados(grafo, estado)

        encontrar_estados(grafo, nodo)
        return estados_alcanzables

    def reconocer(self, texto, expresion_regular, transiciones_coincidencia, transiciones_epsilon, mostrar=False):
        estados_epsilon = self.dfs_digrafo(transiciones_epsilon, 0)

        if mostrar:
            print()
            print(f"Estados antes de escanear: {estados_epsilon}")

        # verificar si el NFA ha llegado a un estado de aceptación
        if len(expresion_regular) in estados_epsilon:
            return True

        caracteres_epsilon = [expresion_regular[estado] for estado in estados_epsilon]
        for i, letra in enumerate(texto):
            # obtener estados de transición de épsilon que coinciden con la letra del texto de entrada
            estados_coincidentes = []
            for estado, grupo_caracteres in zip(estados_epsilon, caracteres_epsilon):
                if letra in grupo_caracteres or "." in grupo_caracteres:
                    estados_coincidentes.append(estado)
                elif "-" in grupo_caracteres:
                    rangos = ""
                    for i, char in enumerate(grupo_caracteres):
                        if char == "-":
                            rangos += self.rango_texto(grupo_caracteres[i - 1], grupo_caracteres[i + 1])
                    if letra in rangos:
                        estados_coincidentes.append(estado)

            # tomar la transición de coincidencia del estado coincidente al siguiente estado
            estados_siguientes = []
            [estados_siguientes.extend(transiciones_coincidencia[nodo]) for nodo in estados_coincidentes]

            # obtener las siguientes transiciones epsilon
            estados_epsilon = []
            [estados_epsilon.extend(self.dfs_digrafo(transiciones_epsilon, nodo)) for nodo in estados_siguientes]

            if mostrar:
                print()
                print(f"Estados antes de escanear: {estados_epsilon}")
                print(f"Letra: {letra}")
                print(f"Estados Coincidentes: {estados_coincidentes}")
                print(f"Transiciones de Coincidencia: {estados_siguientes}")
                print(f"Transiciones de Épsilon: {estados_epsilon}", end=" ")
                print()

            # verificar si el NFA ha llegado a un estado de aceptación
            if len(expresion_regular) in estados_epsilon:
                return True

            caracteres_epsilon = [expresion_regular[estado] for estado in estados_epsilon]

        return False

    def buscar(self, texto, expresion_regular, mostrar=False):
        # la expresión regular debe estar envuelta entre paréntesis. Si ya está envuelta, una capa adicional no hará daño
        expresion_regular = "(" + expresion_regular + ")"
        expresion_regular = self.tokenizar(expresion_regular)
        transiciones_coincidencia_dict = self.transiciones_match(expresion_regular)
        transiciones_epsilon_dict = self.transiciones_epsilon(expresion_regular)

        return self.reconocer(texto, expresion_regular, transiciones_coincidencia_dict, transiciones_epsilon_dict, mostrar)


    def evaluar_expresiones_cadenas(self, expresiones):
        resultados = []

        for expresion in expresiones:
            id_expresion = expresion['ID']
            er = expresion['ER']
            cadenas = expresion['CADENAS']

            for cadena in cadenas:
                cumple = 'Sí' if self.buscar(cadena.strip('"').replace(" ", ""), self.reemplazar_comillas(er).replace(" ","")) else 'No'
                resultados.append({
                    'ID': id_expresion,
                    'Expresión Regular': er,
                    'Cadena': cadena.strip('"'),
                    'Cumple': cumple
                })

        return resultados

    def reemplazar_comillas(self, texto):
        nuevo_texto = ""
        dentro_comillas = False

        for caracter in texto:
            if caracter == '"':
                dentro_comillas = not dentro_comillas
                if dentro_comillas:
                    nuevo_texto += '('
                else:
                    nuevo_texto += ')'
            else:
                nuevo_texto += caracter

        return nuevo_texto