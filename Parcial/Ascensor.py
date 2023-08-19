# Clase Ascensor que contiene los atributos y métodos de los ascensores del edificio y sus métodos para controlarlos y simularlos
class Ascensor:

    def __init__(self, columna: int, estado_emergency: bool = False):
        self.piso = 1
        self.columna = columna
        self.estado = True
        self.recorrido_restante_destino = 0
        self.recorrido_restante_origen = 0
        self.paso = 1
        self.estado_emergency = estado_emergency
        self.encendido = True


    #getters

    # Devuelve el piso actual del ascensor
    def get_piso(self):
        return self.piso

    # Devuelve la columna del ascensor
    def get_columna(self):
        return self.columna

    # Devuelve el estado del ascensor
    def get_estado(self):
        return self.estado

    # Devuelve el paso del ascensor
    def get_paso(self):
        return self.paso

    # Devuelve el recorrido restante al origen
    def get_recorrido_restante_origen(self):
        return self.recorrido_restante_origen

    # Devuelve el recorrido restante al destino
    def get_recorrido_restante_destino(self):
        return self.recorrido_restante_destino

    # Devuelve el recorrido restante al origen si es distinto de 0, sino devuelve el recorrido restante al destino
    def get_recorrido_restante(self):
        return self.get_recorrido_restante_origen() if self.get_recorrido_restante_origen() != 0 else self.get_recorrido_restante_destino()

    # Devuelve el estado de emergencia del ascensor
    def get_estado_emergency(self):
        return self.estado_emergency

    # Devuelve el estado de encendido del ascensor
    def get_encendido(self):
        return self.encendido

    #setters

    # Establece el piso del ascensor
    def set_piso(self, piso):
        self.piso = piso

    # Establece la columna del ascensor
    def set_estado(self, estado):
        self.estado = estado

    # Establece el paso del ascensor
    def set_estado_emergency(self, estado_emergency):
        self.estado_emergency = estado_emergency

    # Establece el paso del ascensor
    def set_encendido(self, encendido):
        self.encendido = encendido

    # Establece el recorrido restante al origen
    def set_recorrido_restante_origen(self, recorrido_restante_origen):
        self.recorrido_restante_origen = recorrido_restante_origen

    # Establece el recorrido restante al destino
    def set_recorrido_restante_destino(self, recorrido_restante_destino):
        self.recorrido_restante_destino = recorrido_restante_destino

    # Establece el recorrido restante al origen si es distinto de 0, sino establece el recorrido restante al destino
    def set_recorrido_restante(self, param):
        if self.get_recorrido_restante_origen() != 0:
            self.set_recorrido_restante_origen(param)
        else:
            self.set_recorrido_restante_destino(param)
