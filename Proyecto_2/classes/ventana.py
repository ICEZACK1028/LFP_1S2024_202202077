import tkinter as tk
import webbrowser
from tkinter import Toplevel, ttk, filedialog, messagebox
from analizador import Analizador
from convertidor_html import ConvertidorHTML
from Parser import Parser
from Analizador_expresiones import Analizador_expresiones
import graphviz

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reconocimiento de Expresiones Regulares")
        self.geometry("1466x868")
        self.crear_estructura()
        self.configure(bg="#F5F7F8")
        self.filename = None

    def crear_estructura(self):
        title = tk.Label(self, text="Expresiones Regulares", font=("Arial", 30), fg="#0F2B46", bg="#F5F7F8")
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self.insert_line()

        self.input_text = tk.Text(self, height=35, width=88, highlightbackground='gray90', highlightthickness=2, relief=tk.FLAT)
        self.input_text.grid(row=4, column=0, padx=10, pady=5)

        self.output_text = tk.Text(self, height=35, width=88, highlightbackground='gray90', highlightthickness=2, relief=tk.FLAT)
        self.output_text.grid(row=4, column=1, padx=10, pady=5)

        menu_bar = tk.Menu(self)

        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Guardar Como", command=self.guardar_archivo_como)

        reportes_menu = tk.Menu(menu_bar, tearoff=0)
        reportes_menu.add_command(label="Tokens", command=self.abrir_reporte_tokens)
        reportes_menu.add_command(label="Errores", command=self.abrir_reporte_errores)
        reportes_menu.add_command(label="Árbol de derivación", command=self.generar_arbol_derivacion)


        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        menu_bar.add_cascade(label="Reportes", menu=reportes_menu)

        self.config(menu=menu_bar)

        translate_button = tk.Button(self, text="Ejecutar", command=self.analizar_archivo, bg="#006494", fg="white", font=("Arial", 12,"bold"), relief=tk.FLAT) 
        translate_button.grid(row=5, column=0, columnspan=1, padx=10, pady=5)

    def insert_line(self):
        # Creating a Canvas widget to draw the line
        canvas = tk.Canvas(self, width=1466, height=5, bg="#F5F7F8", highlightthickness=0)
        canvas.grid(row=1, column=0, columnspan=4)

        # Drawing a line on the canvas
        canvas.create_line(5, 5, 1466, 5, fill="#E0E0E0", width=5)

    def abrir_archivo(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select a File")

        if not self.filename:
            print('Cancelado por el usuario')
            return None

        self.read_file(self.filename)

    def guardar_archivo(self):
        if not self.filename:
            self.guardar_archivo_como()
        else:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file_content = self.input_text.get(1.0, tk.END)
                file.write(file_content)

    def guardar_archivo_como(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])

        if not filename:
            print('Cancelado por el usuario')
            return None

        with open(filename, 'w', encoding='utf-8') as file:
            file_content = self.input_text.get(1.0, tk.END)
            file.write(file_content)
        self.filename = filename

    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(tk.END, file_content)

    def analizar_archivo(self):
        input_text_value = self.input_text.get(1.0, tk.END)
        analizador = Analizador()
        convertidor_html = ConvertidorHTML()
        analizador_expresiones = Analizador_expresiones()
        tokens_lexemas, caracteres_no_permitidos = analizador.analizador_lexico(input_text_value)
        tokens_a_analizar = [token for token in tokens_lexemas if token.name not in ['COMENTARIO_LINEA', 'COMENTARIO_MULTILINEA']]
        expresiones_cadena = analizador_expresiones.obtener_expresiones_cadenas(tokens_a_analizar)
        parser = Parser(tokens_a_analizar)
        error_sintacticos = parser.parse()
        if caracteres_no_permitidos or error_sintacticos:
            texto_error = ''
            for error in caracteres_no_permitidos:
                if error[0].isalpha():
                    texto_error += f'Identificador no válido: {error[0]}. Línea: {error[1]}. Columna: {error[2]}\n'
                else:
                    texto_error += f'Caracter no permitido: {error[0]}. Línea: {error[1]}. Columna: {error[2]}\n'
            
            texto_error_sintáctico = 'Errores sintácticos:\n'
            for error in error_sintacticos:
                texto_error_sintáctico += f'Error: {error.value}. Línea: {error.line}. Columna: {error.column}\n'
        
            self.output_text = tk.Text(self, height=35, width=88, highlightbackground='gray90', highlightthickness=2, relief=tk.FLAT)
            self.output_text.grid(row=4, column=1, padx=10, pady=5)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f'No se pudo analizar el archivo.\n{texto_error} \n{texto_error_sintáctico}')
        else:
            resultados = analizador_expresiones.evaluar_expresiones_cadenas(expresiones_cadena)
            self.output_text.grid_remove()
            self.mostrar_resultados(resultados)
        
        convertidor_html.generar_reporte_tokens(tokens_lexemas)
        convertidor_html.generar_reporte_errores(caracteres_no_permitidos, error_sintacticos)
    
    def abrir_reporte_tokens(self):
        filename = 'D:/USAC/5to. SEMESTRE/LENGUAJES FORMALES Y DE PROGRAMACIÓN/Práctica 1/Proyecto_2/reports/Reporte_Elementos.html'
        webbrowser.open('file://' + filename, new=2)

    def abrir_reporte_errores(self):
        filename = 'D:/USAC/5to. SEMESTRE/LENGUAJES FORMALES Y DE PROGRAMACIÓN/Práctica 1/Proyecto_2/reports/Reporte_Errores.html'
        webbrowser.open('file://' + filename, new=2)

    def mostrar_resultados(self, resultados):
        # Encabezados de la tabla
        table_header = ["ID", "Expresión Regular", "Cadena", "Cumple"]

        # Construir la tabla
        table = ttk.Treeview(self, columns=table_header, show="headings")
        for header in table_header:
            table.heading(header, text=header)
            table.column(header, width=155, anchor="center") 

        for resultado in resultados:
            table.insert("", "end", values=(resultado['ID'], resultado['Expresión Regular'], resultado['Cadena'], resultado['Cumple']))

        # Mostrar la tabla en lugar de self.output_text
        table.grid(row=4, column=1, padx=10, pady=5, sticky="nsew")

    def generar_arbol_derivacion(self):
        input_text_value = self.input_text.get(1.0, tk.END)
        analizador_expresiones = Analizador_expresiones()
        analizador = Analizador()
        tokens_lexemas, caracteres_no_permitidos = analizador.analizador_lexico(input_text_value)
        tokens_a_analizar = [token for token in tokens_lexemas if token.name not in ['COMENTARIO_LINEA', 'COMENTARIO_MULTILINEA']]
        expresiones_cadena = analizador_expresiones.obtener_expresiones_cadenas(tokens_a_analizar)
        parser = Parser(tokens_a_analizar)
        error_sintacticos = parser.parse()
        if caracteres_no_permitidos or error_sintacticos:
            texto_error = ''
            for error in caracteres_no_permitidos:
                if error[0].isalpha():
                    texto_error += f'Identificador no válido: {error[0]}. Línea: {error[1]}. Columna: {error[2]}\n'
                else:
                    texto_error += f'Caracter no permitido: {error[0]}. Línea: {error[1]}. Columna: {error[2]}\n'
            
            texto_error_sintáctico = 'Errores sintácticos:\n'
            for error in error_sintacticos:
                texto_error_sintáctico += f'Error: {error.value}. Línea: {error.line}. Columna: {error.column}\n'
        
            self.output_text = tk.Text(self, height=35, width=88, highlightbackground='gray90', highlightthickness=2, relief=tk.FLAT)
            self.output_text.grid(row=4, column=1, padx=10, pady=5)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f'No se pudo analizar el archivo.\n{texto_error} \n{texto_error_sintáctico}')
        else:
            with open('arbol_derivacion.dot', 'w') as dot_file:
                dot_file.write(self.generar_dot_arbol_derivacion(expresiones_cadena))

            messagebox.showinfo("Árbol de Derivaciones", "El árbol de derivaciones se ha generado exitosamente en formato DOT.")

    def generar_dot_arbol_derivacion(self,expresiones_cadena):
        dot_code = """
        digraph G {
            node [shape=circle, fontsize=10];
            rankdir=TB;
        """

        for expresion in expresiones_cadena:
            dot_code += f"\n\n    // Expresion Regular: {expresion['ER']}\n"
            dot_code += f"    q0 [shape=circle];\n"
            dot_code += f"    q{len(expresion['ER'])} [shape=doublecircle];\n"

            for i in range(len(expresion['ER'])):
                dot_code += f"    q{i+1} [shape=circle];\n"
                label = expresion['ER'][i]
                label = label.replace('"', '\\"')
                label = label.replace('á', '\\u00e1').replace('é', '\\u00e9').replace('í', '\\u00ed').replace('ó', '\\u00f3').replace('ú', '\\u00fa')
                dot_code += f"    q{i} -> q{i+1} [label=\"{label}\"];\n"

        dot_code += "\n}"
        return dot_code




