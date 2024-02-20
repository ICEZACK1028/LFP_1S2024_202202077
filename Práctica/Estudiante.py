class Estudiante:
    def __init__(self, carnet, nombre):
        self.carnet = carnet
        self.nombre = nombre
        self.calificaciones = []

    def agregar_calificaciones(self, calificaciones):
        self.calificaciones = calificaciones

    def calcular_promedio(self):
        if self.calificaciones:
            return round(sum(self.calificaciones) / len(self.calificaciones), 2)
        else:
            return 0

    def esta_aprobado(self):
        return self.calcular_promedio() > 61
