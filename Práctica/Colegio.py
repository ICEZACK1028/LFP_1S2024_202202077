from Estudiante import Estudiante

class Colegio:
    def __init__(self):
        self.estudiantes = []

    def cargar_estudiantes(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                carnet, nombre = line.strip().split(':')
                self.estudiantes.append(Estudiante(carnet, nombre.strip('"')))
        print("Estudiantes cargados correctamente.")

    def ingresar_calificaciones(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                carnet, calificaciones = line.strip().split(':')
                calificaciones = list(map(int, calificaciones.split(',')))
                for estudiante in self.estudiantes:
                    if estudiante.carnet == carnet:
                        estudiante.agregar_calificaciones(calificaciones)
                        break
        print("Calificaciones ingresadas correctamente...")
    
    def mostrar_estudiantes_inexistentes(self, filename):
        carnet_estudiantes = []
        with open(filename, 'r') as file:
            for line in file:
                carnet, calificaciones = line.strip().split(':')
                carnet_estudiantes.append(carnet)
            
        inexistentes = [carnet for carnet in carnet_estudiantes if carnet not in [estudiante.carnet for estudiante in self.estudiantes]]

        for carnet_inexistente in inexistentes:
            print(f"El estudiante con carnet {carnet_inexistente} no existe en el sistema.")

    def generar_reporte_general(self):
        with open("reporte_general.html", 'w') as file:
            file.write("<html><head><style>")
            file.write("body { font-family: Arial, sans-serif; }")
            file.write("h1 { color: navy; }")
            file.write("p { margin-bottom: 10px; }")
            file.write("</style></head><body><h1>Reporte General de Estudiantes</h1>")
            for estudiante in self.estudiantes:
                file.write(f"<p><strong>Carnet:</strong> {estudiante.carnet}</p>")
                file.write(f"<p><strong>Nombre:</strong> {estudiante.nombre}</p>")
                file.write("<p><strong>Calificaciones:</strong> ")
                file.write(", ".join(map(str, estudiante.calificaciones)))
                file.write("</p><br>")
            file.write("</body></html>")
        print("Reporte general generado correctamente.")

    def generar_reporte_aprobacion(self):
        with open("reporte_aprobacion.html", 'w') as file:
            file.write("<html><head><style>")
            file.write("body { font-family: Arial, sans-serif; }")
            file.write("h1 { color: navy; }")
            file.write("p { margin-bottom: 10px; }")
            file.write(".aprobado { color: green; font-weight: bold;}")
            file.write(".reprobado { color: red; font-weight: bold;}")
            file.write("</style></head><body><h1>Reporte de Aprobación de Estudiantes</h1>")
            for estudiante in self.estudiantes:
                file.write(f"<p><strong>Carnet:</strong> {estudiante.carnet}</p>")
                file.write(f"<p><strong>Nombre:</strong> {estudiante.nombre}</p>")
                file.write(f"<p><strong>Promedio:</strong> {estudiante.calcular_promedio()}</p>")
                if estudiante.esta_aprobado():
                    file.write("<p class='aprobado'> Aprobado</p><br>")
                else:
                    file.write("<p class='reprobado'> Reprobado </p><br>")
            file.write("</body></html>")
        print("Reporte de aprobación generado correctamente.")

    def generar_top_tres(self):
        sorted_estudiantes = self.ordenar_por_promedio()[:3]
        with open("top_tres.html", 'w') as file:
            file.write("<html><head><style>")
            file.write("body { font-family: Arial, sans-serif; }")
            file.write("h1 { color: navy; }")
            file.write("p { margin-bottom: 10px; }")
            file.write("</style></head><body><h1>Top 3 Estudiantes con Mejor Promedio</h1>")
            for estudiante in sorted_estudiantes:
                file.write(f"<p><strong>Carnet:</strong> {estudiante.carnet}</p>")
                file.write(f"<p><strong>Nombre:</strong> {estudiante.nombre}</p>")
                file.write(f"<p><strong>Promedio:</strong> {estudiante.calcular_promedio()}</p><br>")
            file.write("</body></html>")
        print("Top 3 generado correctamente.")


    def ordenar_por_promedio(self):
        estudiantes = self.estudiantes[:]
        n = len(estudiantes)
        for i in range(n):
            max_idx = i
            for j in range(i+1, n):
                if estudiantes[j].calcular_promedio() > estudiantes[max_idx].calcular_promedio():
                    max_idx = j
            estudiantes[i], estudiantes[max_idx] = estudiantes[max_idx], estudiantes[i]
            
        return estudiantes