import tkinter as tk
from tkinter import filedialog
from Colegio import Colegio

def cargar_archivo(extension):
    root = tk.Tk(); root.attributes('-alpha',0.01)
    root.attributes('-topmost',True)
    root.tk.eval(f'tk::PlaceWindow {root._w} center')
    root.withdraw()
    filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File", 
                                            filetypes=[(f"{extension} files", f"*.{extension}")])
    
    if not filename:  
        root.destroy()
        print('Cancelado por el usuario')
        return None
    
    root.destroy()
    return filename 
    
def menu():
    programa = Colegio()
    while True:
        print()
        print("-" * 45)
        print("|{:^43}|".format("MENÚ PRINCIPAL"))
        print("-" * 45)
        print("|{:<43}|".format("1. Cargar Estudiantes"))
        print("|{:<43}|".format("2. Ingresar Calificaciones"))
        print("|{:<43}|".format("3. Reporte general de estudiantes"))
        print("|{:<43}|".format("4. Reporte de aprobación de estudiantes"))
        print("|{:<43}|".format("5. Top 3 estudiantes con mejor promedio"))
        print("|{:<43}|".format("6. Salir"))
        print("-" * 45)

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            filename = cargar_archivo('est')
            if filename:
                programa.cargar_estudiantes(filename)
        elif opcion == '2':
            filename = cargar_archivo("cali")
            if filename and programa.estudiantes:
                programa.ingresar_calificaciones(filename)
            else:
                print("No hay estudiantes cargados...")
        elif opcion == '3':
            programa.generar_reporte_general()
        elif opcion == '4':
            programa.generar_reporte_aprobacion()
        elif opcion == '5':
            programa.generar_top_tres()
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()