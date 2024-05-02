import webbrowser
import os

class ConvertidorHTML:
    def __init__(self):
        pass

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
            html += f"<td>{token.get_name()}</td>\n"
            html += f"<td>{token.get_value()}</td>\n"
            html += f"<td>{token.get_line()}</td>\n"
            html += f"<td>{token.get_column()}</td>\n"
            html += "</tr>\n"
        html += "</table>\n"
        html += "</body>\n"
        html += "</html>"

        with open('D:/USAC/5to. SEMESTRE/LENGUAJES FORMALES Y DE PROGRAMACIÓN/Práctica 1/Proyecto_2/reports/Reporte_Elementos.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def generar_reporte_errores(self, tokens, tokens_semantico):
        html = "<!DOCTYPE html>\n"
        html += "<html lang='es'>\n"
        html += "<head>\n"
        html += "<title>Errores</title>\n"
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
        html += "<h1 style='text-align: center;'>Errores léxicos</h1>\n"
        html += "<table border='1'>\n"
        html += "<tr style='color: white; background-color: black'>\n"
        html += "<th>Caracter</th>\n"
        html += "<th>Fila</th>\n"
        html += "<th>Columna</th>\n"
        html += "</tr>\n"
        if not tokens:
            html += "<tr>\n"
            html += "<td colspan='3' style='text-align: center;'>No se encontraron caracteres</td>\n"
            html += "</tr>\n"
        else:
            for token in tokens:
                html += "<tr>\n"
                html += f"<td>{token[0]}</td>\n"
                html += f"<td>{token[1]}</td>\n"
                html += f"<td>{token[2]}</td>\n"
                html += "</tr>\n"
        html += "</table>\n"
        html += "<h1 style='text-align: center;'>Errores sintácticos</h1>\n"
        html += "<table border='1'>\n"
        html += "<tr style='color: white; background-color: black'>\n"
        html += "<th>Token de error</th>\n"
        html += "<th>Fila</th>\n"
        html += "<th>Columna</th>\n"
        html += "</tr>\n"
        if not tokens_semantico:
            html += "<tr>\n"
            html += "<td colspan='3' style='text-align: center;'>No se encontraron errores</td>\n"
            html += "</tr>\n"
        else:
            for token in tokens_semantico:
                html += "<tr>\n"
                html += f"<td>{token.value}</td>\n"
                html += f"<td>{token.line}</td>\n"
                html += f"<td>{token.column}</td>\n"
                html += "</tr>\n"
        html += "</table>\n"
        html += "</body>\n"
        html += "</html>"

        with open('D:/USAC/5to. SEMESTRE/LENGUAJES FORMALES Y DE PROGRAMACIÓN/Práctica 1/Proyecto_2/reports/Reporte_Errores.html', 'w', encoding='utf-8') as f:
            f.write(html)
