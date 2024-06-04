from convertidor_json import ConvertidorJSON
import webbrowser
import os

class ConvertidorHTML:
    def __init__(self):
        self.colores = {'rojo': 'red', 'amarillo': "yellow", 'azul': "blue"}
        self.title_size = {'t1': 'h1', 't2': 'h2', 't3': 'h3', 't4': 'h4', 't5': 'h5', 't6': 'h6'}
        self.posiciones = {'izquierda': 'left', 'derecha': 'right', 'centro': 'center', 'justificado': 'justify'}

    def traducir_a_html(self, entrada):
        html = ""
        html += "<!DOCTYPE html>\n"
        html += "<html lang='es'>\n"
        html += "<head>\n"
        html += "<title>" + entrada['Inicio']['Encabezado']['TituloPagina'] + "</title>\n"
        html += "<meta charset='UTF-8'>\n"
        html += "</head>\n"
        if any('Fondo' in item for item in entrada['Inicio']['Cuerpo']):
            style = next(item for item in entrada['Inicio']['Cuerpo'] if 'Fondo' in item)
            html += "<body style='background-color: " + self.colores.get(style['Fondo']['color'], style['Fondo']['color']) + "'>\n"
        else:
            html += "<body>\n"
            
        for elemento in entrada['Inicio']['Cuerpo']:
            if 'Titulo' in elemento:
                titulo = elemento['Titulo']
                html += f"<{self.title_size.get(titulo['tamaño'], 'h1')} style='text-align: {self.posiciones.get(titulo['posicion'], titulo['posicion'])}; color: {self.colores.get(titulo['color'], titulo['color'])}'>{titulo['texto']}</{self.title_size.get(titulo['tamaño'], 'h1')}>\n"
            elif 'Parrafo' in elemento:
                parrafo = elemento['Parrafo']
                html += f"<p style='text-align: {self.posiciones.get(parrafo['posicion'], parrafo['posicion'])}'>{parrafo['texto']}</p>\n"
            elif 'Texto' in elemento:
                texto = elemento['Texto']
                html += f"<span style='font-family: {texto['fuente']}; font-size: {texto['tamaño']}px; color: {self.colores.get(texto['color'], texto['color'])}'>{texto['texto']}</span>\n"
            elif 'Codigo' in elemento:
                codigo = elemento['Codigo']
                html += f"<code style='text-align: {self.posiciones.get(codigo['posicion'], codigo['posicion'])}'>{codigo['texto']}</code>\n"
            elif 'Negrita' in elemento:
                negrita = elemento['Negrita']
                html += f"<strong>{negrita['texto']}</strong>\n"
            elif 'Subrayado' in elemento:
                subrayado = elemento['Subrayado']
                html += f"<u>{subrayado['texto']}</u>\n"
            elif 'Tachado' in elemento:
                tachado = elemento['Tachado']
                html += f"<s>{tachado['texto']}</s>\n"
            elif 'Cursiva' in elemento:
                cursiva = elemento['Cursiva']
                html += f"<i>{cursiva['texto']}</i>\n"
            elif 'Salto' in elemento:
                salto = elemento['Salto']
                html += "<br>\n" * int(salto['cantidad'])
            elif 'Tabla' in elemento:
                tabla = elemento['Tabla']
                html += "<table border='1'>\n"
                for fila in range(int(tabla['filas'])):
                    html += "<tr>\n"
                    for columna in range(int(tabla['columnas'])):
                        texto = ""
                        for elem in tabla['elemento']:
                            if elem['fila'] == str(fila + 1) and elem['columna'] == str(columna + 1):
                                texto = elem['texto']
                                break
                        html += f"<td>{texto}</td>\n"
                    html += "</tr>\n"
                html += "</table>\n"
        
        html += "</body>\n"
        html += "</html>"
        
        with open('Salida_HTML.html', 'w', encoding='utf-8') as f:
            f.write(html)

        ruta_absoluta = os.path.abspath('Salida_HTML.html')
        webbrowser.open('file://' + ruta_absoluta)
        return html

    def generar_reporte_tokens(self, tokens):
        html = "<!DOCTYPE html>\n"
        html += "<html lang='es'>\n"
        html += "<head>\n"
        html += "<title>Tokens</title>\n"
        html += "<meta charset='UTF-8'>\n"
        html += "<style>"
        html += "*{font-family:courier,arial,helvética;}"
        html += "table {"
        html += "    width: 50%;"
        html += "    margin: auto;"
        html += "    border-collapse: collapse;"
        html += "}"
        html += "th, td {"
        html += "    padding: 8px;"
        html += "    text-align: left;"
        html += "    border-bottom: 1px solid #ddd;"
        html += "}"
        html += "th {"
        html += "    background-color: #000;"
        html += "}"
        html += "</style>"
        html += "</head>\n"
        html += "<body>\n"
        html += "<h1 style='text-align: center;'>Reporte general de elementos encontrados</h1>\n"
        html += "<table border='1'>\n"
        html += "<tr style='color: white; background-color: black'>\n"
        html += "<th>Token</th>\n"
        html += "<th>Lexema</th>\n"
        html += "<th>Línea</th>\n"
        html += "<th>Columna</th>\n"
        html += "</tr>\n"
        for token in tokens:
            html += "<tr>\n"
            html += f"<td>{token[0]}</td>\n"
            html += f"<td>{token[1]}</td>\n"
            html += f"<td>{token[2]}</td>\n"
            html += f"<td>{token[3]}</td>\n"
            html += "</tr>\n"
        html += "</table>\n"
        html += "</body>\n"
        html += "</html>"

        with open('Reporte_Elementos.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def generar_reporte_errores(self, tokens):
        html = "<!DOCTYPE html>\n"
        html += "<html lang='es'>\n"
        html += "<head>\n"
        html += "<title>Caracteres no permitidos</title>\n"
        html += "<meta charset='UTF-8'>\n"
        html += "<style>"
        html += "*{font-family:courier,arial,helvética;}"
        html += "table {"
        html += "    width: 50%;"
        html += "    margin: auto;"
        html += "    border-collapse: collapse;"
        html += "}"
        html += "th, td {"
        html += "    padding: 8px;"
        html += "    text-align: left;"
        html += "    border-bottom: 1px solid #ddd;"
        html += "}"
        html += "th {"
        html += "    background-color: #000;"
        html += "}"
        html += "</style>"
        html += "</head>\n"
        html += "<body>\n"
        html += "<h1 style='text-align: center;'>Reporte de caracteres no permitidos</h1>\n"
        html += "<table border='1'>\n"
        html += "<tr style='color: white; background-color: black'>\n"
        html += "<th>Caracter/Lexema</th>\n"
        html += "<th>Línea</th>\n"
        html += "<th>Columna</th>\n"
        html += "</tr>\n"
        if not tokens:
            html += "<tr>\n"
            html += "<td colspan='3' style='text-align: center;'>No se encontraron caracteres</td>\n"
            html += "</tr>\n"
        else:
            for token in tokens:
                html += "<tr>\n"
                html += f"<td>{token[1]}</td>\n"
                html += f"<td>{token[2]}</td>\n"
                html += f"<td>{token[3]}</td>\n"
                html += "</tr>\n"
        html += "</table>\n"
        html += "</body>\n"
        html += "</html>"

        with open('Reporte_Errores.html', 'w', encoding='utf-8') as f:
            f.write(html)
