import tkinter as tk
from tkinter import filedialog
from analizador import Analizador
from convertidor_html import ConvertidorHTML
from convertidor_json import ConvertidorJSON
import graphviz

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Traductor")
        self.geometry("1466x868")
        self.crear_estructura()
        self.configure(bg="mint cream")

    def crear_estructura(self):
        title = tk.Label(self, text="Traductor", font=("Arial", 30), bg="mint cream")
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        input_label = tk.Label(self, text="Texto de Entrada:", font=("Arial", 12), bg="mint cream")
        input_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        output_label = tk.Label(self, text="Texto de Salida:", font=("Arial", 12), bg="mint cream")
        output_label.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.input_text = tk.Text(self, height=35, width=88, highlightbackground='gray90', highlightthickness=2)
        self.input_text.grid(row=3, column=0, padx=10, pady=5)

        self.output_text = tk.Text(self, height=35, width=88, highlightbackground='gray90', highlightthickness=2)
        self.output_text.grid(row=3, column=1, padx=10, pady=5)

        add_file_button = tk.Button(self, text="Agregar Archivo", command=self.add_file, bg="cadet blue", fg="white", font=("Arial", 12))
        add_file_button.grid(row=1, column=0, columnspan=1, padx=10, pady=5)

        translate_button = tk.Button(self, text="Traducir", command=self.analizar_archivo, bg="cadet blue", fg="white", font=("Arial", 12)) 
        translate_button.grid(row=4, column=0, columnspan=1, padx=10, pady=5)

        translate_button = tk.Button(self, text="Generar Grafo", command=self.generar_grafo, bg="cadet blue", fg="white", font=("Arial", 12)) 
        translate_button.grid(row=4, column=1, columnspan=1, padx=10, pady=5)


    def add_file(self):
        root = tk.Tk()
        root.attributes('-alpha',0.01)
        root.attributes('-topmost',True)
        root.tk.eval(f'tk::PlaceWindow {root._w} center')
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=[("txt files", "*.txt")])

        if not filename:
            root.destroy()
            print('Cancelado por el usuario')
            return None

        root.destroy()
        self.read_file(filename)

    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(tk.END, file_content)

    def analizar_archivo(self):
        input_text_value = self.input_text.get(1.0, tk.END)
        analizador = Analizador()
        convertidor_html = ConvertidorHTML()
        tokens_lexemas, caracteres_no_permitidos = analizador.analizador_lexico(input_text_value)
        if caracteres_no_permitidos:
            texto_error = ''
            for error in caracteres_no_permitidos:
                if error[0].isalpha():
                    texto_error += f'Identificador no válido: {error[0]}. Línea: {error[1]}. Columna: {error[2]}\n'
                else:
                    texto_error += f'Caracter no permitido: {error[0]}. Línea: {error[1]}. Columna: {error[2]}\n'
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f'No se pudo analizar el archivo.\n{texto_error}')
        else:
            convertidor_json = ConvertidorJSON(tokens_lexemas)
            json = convertidor_json.convertir_json()
            print("inicio_json",json)
            texto_html = convertidor_html.traducir_a_html(json)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, texto_html)
        
        convertidor_html.generar_reporte_tokens(tokens_lexemas)
        convertidor_html.generar_reporte_errores(caracteres_no_permitidos)
    
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

        