class Estudiante:
    def _init_(self, carnet, nombre):
        self.carnet = carnet
        self.nombre = nombre
        self.calificaciones = []

    def agregar_calificaciones(self, calificaciones):
        self.calificaciones = calificaciones

    def calcular_promedio(self):
        if self.calificaciones:
            return sum(self.calificaciones) / len(self.calificaciones)
        else:
            return 0

    def esta_aprobado(self):
        return self.calcular_promedio() > 61
