import tkinter as tk
import webbrowser
from tkinter import filedialog
from analizador import Analizador
from convertidor_html import ConvertidorHTML
from convertidor_json import ConvertidorJSON
from Parser import Parser
from Analizador_expresiones import Analizador_expresiones
import graphviz

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LFP - Proyecto 2")
        self.geometry("1466x868")
        self.crear_estructura()
        self.configure(bg="#F5F7F8")
        self.filename = None

    def crear_estructura(self):
        title = tk.Label(self, text="LFP - Proyecto 2", font=("Arial", 30), fg="#0F2B46", bg="#F5F7F8")
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self.insert_line()

        # input_label = tk.Label(self, text="Texto de Entrada:", font=("Arial", 12, "bold"), fg="#0F2B46", bg="#F5F7F8")
        # input_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # output_label = tk.Label(self, text="Texto de Salida:", font=("Arial", 12, "bold"), fg="#0F2B46", bg="#F5F7F8")
        # output_label.grid(row=3, column=1, sticky="w", padx=10, pady=5)

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
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f'No se pudo analizar el archivo.\n{texto_error} \n{texto_error_sintáctico}')
        else:
            resultados = analizador_expresiones.evaluar_expresiones_cadenas(expresiones_cadena)
            self.mostrar_resultados(resultados)
        
        convertidor_html.generar_reporte_tokens(tokens_lexemas)
        convertidor_html.generar_reporte_errores(caracteres_no_permitidos, error_sintacticos)
    
    def abrir_reporte_tokens(self):
        filename = 'D:/USAC/5to. SEMESTRE/LENGUAJES FORMALES Y DE PROGRAMACIÓN/Práctica 1/Proyecto_2/reports/Reporte_Elementos.html'
        webbrowser.open('file://' + filename, new=2)

    def abrir_reporte_errores(self):
        filename = 'D:/USAC/5to. SEMESTRE/LENGUAJES FORMALES Y DE PROGRAMACIÓN/Práctica 1/Proyecto_2/reports/Reporte_Errores.html'
        webbrowser.open('file://' + filename, new=2)

    def generar_arbol_derivacion(self):
        pass  # Implementa la lógica para generar el reporte de árbol de derivación

    def mostrar_resultados(self, resultados):
        # Encabezados de la tabla
        table_header = ["ID", "Expresión Regular", "Cadena", "Cumple"]

        # Construir la tabla
        table_data = []
        for resultado in resultados:
            fila = [resultado['ID'], resultado['Expresión Regular'], resultado['Cadena'], resultado['Cumple']]
            table_data.append(fila)

        # Longitud máxima de cada columna para ajustar el ancho de la tabla
        column_widths = [max(len(str(row[i])) for row in table_data) for i in range(len(table_header))]

        # Construir la tabla con formato
        table = ""
        table += "|".join(f"{header.ljust(column_widths[i])}" for i, header in enumerate(table_header)) + "\n"
        table += "|".join("-" * width for width in column_widths) + "\n"
        for row in table_data:
            table += "|".join(f"{str(item).ljust(column_widths[i])}" for i, item in enumerate(row)) + "\n"

        # Mostrar la tabla en self.output_text
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, table)

    def generar_grafo(self):
        dot_code = """
        digraph G {
            node [shape=circle, fontsize=10];
            rankdir=LR;

            // Estados
            q0 [shape=circle]; 
            q1 [shape=doublecircle]; 
            q2 [shape=doublecircle];
            q3 [shape=circle]; 
            q4 [shape=circle];
            q5 [shape=doublecircle];

            // Transiciones
            q0 -> q1 [label="a-zA-Z"];
            q1 -> q1 [label="a-zA-Z"];
            q0 -> q2 [label="[ ]{ }:;,="]
            q0 -> q3 [label="''"]
            q3 -> q4 [label="a-zA-Z"]
            q4 -> q4 [label="a-zA-Z"]
            q4 -> q2 [label="''"]
            q0 -> q5 [label="0...9"]
        }
        """
        graph = graphviz.Source(dot_code)
        graph.render('DFA', format='png', cleanup=True)

