import json

class ConvertidorJSON:
    def __init__(self, tokens):
        self.tokens = tokens

    def extraer_seccion(self, keyword, start=0, seccion=None):
        section = []
        abrir_corchetes = 0
        abrir_parentesis = 0
        start_section = 0

        if start != 0:
            start_section = start
        else:
            for i, token in enumerate(self.tokens):
                if token[0] == 'PALABRA_RESERVADA' and token[1] == keyword:
                    start_section = i
                    break

        if start_section == 0:
            return None

        if seccion:
            for j, token in enumerate(seccion[start_section:]):
                section.append(token)

                if token[0] == 'CORCHETE_APERTURA':
                    abrir_corchetes += 1
                elif token[0] == 'CORCHETE_CIERRE':
                    abrir_corchetes -= 1

                if token[0] == 'LLAVE_APERTURA':
                    abrir_parentesis += 1
                elif token[0] == 'LLAVE_CIERRE':
                    abrir_parentesis -= 1

                    if abrir_parentesis == 0 and abrir_corchetes == 0:
                        break
        else:
            for j, token in enumerate(self.tokens[start_section:]):
                section.append(token)

                if token[0] == 'CORCHETE_APERTURA':
                    abrir_corchetes += 1
                elif token[0] == 'CORCHETE_CIERRE':
                    abrir_corchetes -= 1

                if token[0] == 'LLAVE_APERTURA':
                    abrir_parentesis += 1
                elif token[0] == 'LLAVE_CIERRE':
                    abrir_parentesis -= 1

                    if abrir_parentesis == 0 and abrir_corchetes == 0:
                        break
        return section

    def convertir_estrutura_tabla(self, section):
        structure = {}
        element = []

        for i, token in enumerate(section):
            if token[0] == 'PALABRA_RESERVADA':
                if token[1] == 'filas' or token[1] == 'columnas':
                    structure[token[1]] = section[i + 2][1].strip('"')
                elif token[1] == 'elemento':
                    element.append({})
            elif token[0] == 'CADENA':
                if token[1] == '"fila"' or token[1] == '"columna"':
                    element[-1][token[1].strip('"')] = section[i + 2][1].strip('"')
                elif element.__len__() > 0:
                    if 'fila' in element[-1] and 'columna' in element[-1]:
                        element[-1]['texto'] = token[1].strip('"')

        structure['elemento'] = element
        return {'Tabla': structure}

    def convertir_estructura(self, section, section_title):
        structure = {}
        element = []
        current_token = ''
        for i, token in enumerate(section):
            if token[1] == 'Tabla':
                table_section = self.extraer_seccion('Tabla', i, section)
                new_element = self.convertir_estrutura_tabla(table_section)
                element.append(new_element)
                structure['Cuerpo'] = element

            if token[0] == 'PALABRA_RESERVADA':
                if section[i + 2][0].strip('"') == 'LLAVE_APERTURA' or section[i + 2][0].strip('"') == 'CORCHETE_APERTURA':
                    if token[1] == 'Cuerpo':
                        structure[token[1]] = []
                    elif token[1] == 'Tabla' or token[1] == 'elemento':
                        pass
                    else:
                        element.append({token[1]: {}})
                        structure['Cuerpo'] = element
                        current_token = token[1]
                else:
                    if structure['Cuerpo'].__len__() > 0:
                        if token[1] == 'filas' or token[1] == 'columnas':
                            pass
                        else:
                            structure['Cuerpo'][-1][current_token][token[1]] = section[i + 2][1].strip('"')

        return structure

    def convertir_estructura_encabezado(self, section, section_title):
        structure = {}

        for i, token in enumerate(section):
            if token[0] == 'PALABRA_RESERVADA':
                if section[i + 2][0].strip('"') == 'LLAVE_APERTURA' or section[i + 2][0].strip('"') == 'CORCHETE_APERTURA':
                    pass
                else:
                    structure[token[1]] = section[i + 2][1].strip('"')

        return structure

    def convertir_json(self):
        json_structure = {}
        perform_json = 0
        header_index = 0
        body_index = 0

        for i, token in enumerate(self.tokens):
            if token[1] == 'Encabezado':
                header_index = i
                perform_json += 1
            elif token[1] == 'Cuerpo':
                body_index = i
                perform_json += 1

        if perform_json == 2:
            body_section = self.extraer_seccion('Cuerpo')
            header_section = self.extraer_seccion('Encabezado')

            body_structure = self.convertir_estructura(body_section, 'Cuerpo')
            header_structure = self.convertir_estructura_encabezado(header_section, 'Encabezado')

            if header_index < body_index:
                json_structure['Inicio'] = {'Encabezado': header_structure, 'Cuerpo': body_structure['Cuerpo']}
            else:
                json_structure['Inicio'] = {'Cuerpo': body_structure['Cuerpo'], 'Encabezado': header_structure}
        else:
            print('La entrada no contiene el encabezado o el cuerpo')

        return json_structure

# Ejemplo de uso
# tokens = [('PALABRA_RESERVADA', 'Inicio', 1, 8), ('DOS_PUNTOS', ':', 1, 9), ('LLAVE_APERTURA', '{', 1, 10), ('PALABRA_RESERVADA', 'Cuerpo', 2, 9), ('DOS_PUNTOS', ':', 2, 10), ('CORCHETE_APERTURA', '[', 2, 11), ('PALABRA_RESERVADA', 'Titulo', 3, 10), ('DOS_PUNTOS', ':', 3, 11), ('LLAVE_APERTURA', '{', 3, 12), ('PALABRA_RESERVADA', 'texto', 4, 10), ('DOS_PUNTOS', ':', 4, 11), ('CADENA', '"Este es un titulo"', 4, 30), ('PUNTO_COMA', ';', 4, 31), ('PALABRA_RESERVADA', 'posicion', 5, 13), ('DOS_PUNTOS', ':', 5, 14), ('CADENA', '"izquierda"', 5, 25), ('PUNTO_COMA', ';', 5, 26), ('PALABRA_RESERVADA', 'tamaño', 6, 11), ('DOS_PUNTOS', ':', 6, 12), ('CADENA', '"t1"', 6, 16), ('PUNTO_COMA', ';', 6, 17), ('PALABRA_RESERVADA', 'color', 7, 10), ('DOS_PUNTOS', ':', 7, 11), ('CADENA', '"rojo"', 7, 17), ('PUNTO_COMA', ';', 7, 18), ('LLAVE_CIERRE', '}', 8, 4), ('COMA', ',', 8, 5), ('PALABRA_RESERVADA', 'Fondo', 9, 9), ('DOS_PUNTOS', ':', 9, 10), ('LLAVE_APERTURA', '{', 9, 11), ('PALABRA_RESERVADA', 'color', 10, 10), ('DOS_PUNTOS', ':', 10, 11), ('CADENA', '"cyan"', 10, 17), ('PUNTO_COMA', ';', 10, 18), ('LLAVE_CIERRE', '}', 11, 4), ('COMA', ',', 11, 5), ('PALABRA_RESERVADA', 'Parrafo', 12, 11), ('DOS_PUNTOS', ':', 12, 12), ('LLAVE_APERTURA', '{', 12, 13), ('PALABRA_RESERVADA', 'texto', 13, 10), ('DOS_PUNTOS', ':', 13, 11), ('CADENA', '"Este es un parrafo de ejemplo."', 13, 43), ('PUNTO_COMA', ';', 13, 44), ('PALABRA_RESERVADA', 'posicion', 14, 13), ('DOS_PUNTOS', ':', 14, 14), ('CADENA', '"izquierda"', 14, 25), ('PUNTO_COMA', ';', 14, 26), ('LLAVE_CIERRE', '}', 15, 4), ('COMA', ',', 15, 5), ('PALABRA_RESERVADA', 'Texto', 16, 9), ('DOS_PUNTOS', ':', 16, 10), ('LLAVE_APERTURA', '{', 16, 11), ('PALABRA_RESERVADA', 'fuente', 17, 11), ('SIGNO_IGUAL', '=', 17, 12), ('CADENA', '"Arial"', 17, 19), ('PUNTO_COMA', ';', 17, 20), ('PALABRA_RESERVADA', 'color', 18, 10), ('SIGNO_IGUAL', '=', 18, 11), ('CADENA', '"azul"', 18, 17), ('PUNTO_COMA', ';', 18, 18), ('PALABRA_RESERVADA', 'tamaño', 19, 11), ('SIGNO_IGUAL', '=', 19, 12), ('CADENA', '"11"', 19, 16), ('PUNTO_COMA', ';', 19, 17), ('LLAVE_CIERRE', '}', 20, 4), ('COMA', ',', 20, 5), ('PALABRA_RESERVADA', 'Codigo', 21, 10), ('DOS_PUNTOS', ':', 21, 11), ('LLAVE_APERTURA', '{', 21, 12), ('PALABRA_RESERVADA', 'texto', 22, 10), ('DOS_PUNTOS', ':', 22, 11), ('CADENA', '"Muestra el texto con fuente de codigo de ordenador."', 22, 64), ('PUNTO_COMA', ';', 22, 65), ('PALABRA_RESERVADA', 'posicion', 23, 13), ('DOS_PUNTOS', ':', 23, 14), ('CADENA', '"centro"', 23, 22), ('PUNTO_COMA', ';', 23, 23), ('LLAVE_CIERRE', '}', 24, 4), ('COMA', ',', 24, 5), ('PALABRA_RESERVADA', 'Negrita', 25, 11), ('DOS_PUNTOS', ':', 25, 12), ('LLAVE_APERTURA', '{', 25, 13), ('PALABRA_RESERVADA', 'texto', 26, 10), ('DOS_PUNTOS', ':', 26, 11), ('CADENA', '"Este texto aparecerá en negrita."', 26, 45), ('PUNTO_COMA', ';', 26, 46), ('LLAVE_CIERRE', '}', 27, 4), ('COMA', ',', 27, 5), ('PALABRA_RESERVADA', 'Subrayado', 28, 13), ('DOS_PUNTOS', ':', 28, 14), ('LLAVE_APERTURA', '{', 28, 15), ('PALABRA_RESERVADA', 'texto', 29, 10), ('DOS_PUNTOS', ':', 29, 11), ('CADENA', '"Este texto aparecerá Subrayado."', 29, 44), ('PUNTO_COMA', ';', 29, 45), ('LLAVE_CIERRE', '}', 30, 4), ('COMA', ',', 30, 5), ('PALABRA_RESERVADA', 'Tachado', 31, 11), ('DOS_PUNTOS', ':', 31, 12), ('LLAVE_APERTURA', '{', 31, 13), ('PALABRA_RESERVADA', 'texto', 32, 10), ('DOS_PUNTOS', ':', 32, 11), ('CADENA', '"Este texto aparecerá tachado."', 32, 42), ('PUNTO_COMA', ';', 32, 43), ('LLAVE_CIERRE', '}', 33, 4), ('COMA', ',', 33, 5), ('PALABRA_RESERVADA', 'Cursiva', 34, 11), ('DOS_PUNTOS', ':', 34, 12), ('LLAVE_APERTURA', '{', 34, 13), ('PALABRA_RESERVADA', 'texto', 35, 10), ('DOS_PUNTOS', ':', 35, 11), ('CADENA', '"Este texto aparecerá en cursiva."', 35, 45), ('PUNTO_COMA', ';', 35, 46), ('LLAVE_CIERRE', '}', 36, 4), ('COMA', ',', 36, 5), ('PALABRA_RESERVADA', 'Salto', 37, 9), ('DOS_PUNTOS', ':', 37, 10), ('LLAVE_APERTURA', '{', 37, 11), ('PALABRA_RESERVADA', 'cantidad', 38, 13), ('DOS_PUNTOS', ':', 38, 14), ('CADENA', '"5"', 38, 17), ('PUNTO_COMA', ';', 38, 18), ('LLAVE_CIERRE', '}', 39, 4), ('COMA', ',', 39, 5), ('PALABRA_RESERVADA', 'Tabla', 40, 9), ('DOS_PUNTOS', ':', 40, 10), ('LLAVE_APERTURA', '{', 40, 11), ('PALABRA_RESERVADA', 'filas', 41, 10), ('DOS_PUNTOS', ':', 41, 11), ('CADENA', '"4"', 41, 14), ('PUNTO_COMA', ';', 41, 15), ('PALABRA_RESERVADA', 'columnas', 42, 13), ('DOS_PUNTOS', ':', 42, 14), ('CADENA', '"3"', 42, 17), ('PUNTO_COMA', ';', 42, 18), ('PALABRA_RESERVADA', 'elemento', 43, 13), ('DOS_PUNTOS', ':', 43, 14), ('LLAVE_APERTURA', '{', 43, 15), ('CADENA', '"fila"', 43, 21), ('DOS_PUNTOS', ':', 43, 22), ('CADENA', '"1"', 43, 25), ('COMA', ',', 43, 26), ('CADENA', '"columna"', 43, 35), ('DOS_PUNTOS', ':', 43, 36), ('CADENA', '"1"', 43, 39), ('COMA', ',', 43, 40), ('CADENA', '"Texto mostrado en fila 1 columna 1"', 43, 76), ('LLAVE_CIERRE', '}', 43, 77), ('PUNTO_COMA', ';', 43, 78), ('PALABRA_RESERVADA', 'elemento', 44, 13), ('DOS_PUNTOS', ':', 44, 14), ('LLAVE_APERTURA', '{', 44, 15), ('CADENA', '"fila"', 44, 21), ('DOS_PUNTOS', ':', 44, 22), ('CADENA', '"1"', 44, 25), ('COMA', ',', 44, 26), ('CADENA', '"columna"', 44, 35), ('DOS_PUNTOS', ':', 44, 36), ('CADENA', '"2"', 44, 39), ('COMA', ',', 44, 40), ('CADENA', '"Texto mostrado en fila 1 columna 2"', 44, 76), ('LLAVE_CIERRE', '}', 44, 77), ('PUNTO_COMA', ';', 44, 78), ('PALABRA_RESERVADA', 'elemento', 45, 13), ('DOS_PUNTOS', ':', 45, 14), ('LLAVE_APERTURA', '{', 45, 15), ('CADENA', '"fila"', 45, 21), ('DOS_PUNTOS', ':', 45, 22), ('CADENA', '"1"', 45, 25), ('COMA', ',', 45, 26), ('CADENA', '"columna"', 45, 35), ('DOS_PUNTOS', ':', 45, 36), ('CADENA', '"3"', 45, 39), ('COMA', ',', 45, 40), ('CADENA', '"Texto mostrado en fila 1 columna 3"', 45, 76), ('LLAVE_CIERRE', '}', 45, 77), ('PUNTO_COMA', ';', 45, 78), ('LLAVE_CIERRE', '}', 46, 4), ('COMA', ',', 46, 5), ('PALABRA_RESERVADA', 'Negrita', 47, 11), ('DOS_PUNTOS', ':', 47, 12), ('LLAVE_APERTURA', '{', 47, 13), ('PALABRA_RESERVADA', 'texto', 48, 10), ('DOS_PUNTOS', ':', 48, 11), ('CADENA', '"Este texto 2 aparecerá en negrita."', 48, 47), ('PUNTO_COMA', ';', 48, 48), ('LLAVE_CIERRE', '}', 49, 4), ('COMA', ',', 49, 5), ('CORCHETE_CIERRE', ']', 50, 3), ('COMA', ',', 50, 4), ('PALABRA_RESERVADA', 'Encabezado', 51, 13), ('DOS_PUNTOS', ':', 51, 14), ('LLAVE_APERTURA', '{', 51, 15), ('PALABRA_RESERVADA', 'TituloPagina', 52, 16), ('DOS_PUNTOS', ':', 52, 17), ('CADENA', '"Ejemplo titulo"', 52, 33), ('PUNTO_COMA', ';', 52, 34), ('LLAVE_CIERRE', '}', 53, 3), ('LLAVE_CIERRE', '}', 54, 2)]
# converter = ConvertidorJSON(tokens)
# print(converter.convertir_json())
