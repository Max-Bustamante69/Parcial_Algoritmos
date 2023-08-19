class Usuario:

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.piso = 1
        self.estado = True
        self.ascensor = None

    # getters



    def get_nombre(self):
        return self.nombre

    def get_apellido(self):
        return self.apellido

    def get_piso(self):
        return self.piso

    def get_ascensor(self):
        return self.ascensor

    def get_estado(self):
        return self.estado

    # setters
    def set_piso(self, piso):
        self.piso = piso

    def set_ascensor(self, ascensor):
        self.ascensor = ascensor

    def set_estado(self, estado):
        self.estado = estado
