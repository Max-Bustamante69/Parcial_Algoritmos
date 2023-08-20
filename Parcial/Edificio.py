from time import sleep

from Ascensor import Ascensor
from Usuario import Usuario
from faker import Faker


# unicodes para tkinter de rojo verde y azul:

# Clase Edificio que contiene los ascensores y los usuarios del edificio y sus métodos para controlarlos y simularlos

class Edificio:

    def __init__(self, pisos=120, columnas=20):
        self.fake = Faker()
        self.pisos = pisos
        self.columnas = columnas
        # crear la mitad de ascensores con emergencia verdadera y la otra mitad con emergencia falsa
        self.lista_ascensores = [Ascensor(i, i % 2 == 0) for i in range(1, self.columnas + 1)]
        self.lista_usuarios = [Usuario(self.fake.first_name(), self.fake.last_name()) for _ in range(10)]
        self.estado_de_emergencia = False
        self.usuario_actual = 0
        self.estructura = [[0] * self.columnas for _ in range(self.pisos - 1)] + [self.get_lista_ascensores()]
        self.errores = {
            "select_piso": f"El piso debe ser un número entero entre 1 y {self.pisos}",
            "valor_numerico": "Ingresa valores numéricos válidos",
            "ascensores_en_uso": "Todos los ascensores están en uso",
            "usuario_en_uso": f"El usuario äun no ha llegado a su destino esta en el ascensor {self.get_usuario_actual().get_ascensor().get_columna()}",
            "usuario_en_destino": f"El usuario {self.get_usuario_actual().get_nombre()} ya se encuentra en el piso destino"
        }

    # getters

    # Devuelve la lista de usuarios
    def get_lista_usuarios(self):
        return self.lista_usuarios

    # De acuerdo con el indice del usuario actual, devuelve el usuario actual
    def get_usuario_actual(self):
        return self.lista_usuarios[self.usuario_actual]

    # Devuelve el número de pisos del edificio
    def get_pisos(self):
        return self.pisos

    # Verifica si hay ascensores que aun deben moverse
    def hay_ascensores_en_movimiento(self):
        return any(ascensor.get_recorrido_restante() != 0 for ascensor in self.lista_ascensores)

    # Verifica si todos los ascensores están en uso
    def todos_los_ascensores_estan_en_uso(self):
        return all(ascensor.get_estado() is False for ascensor in self.lista_ascensores if ascensor.get_encendido())

    # Devuelve una lista con la cantidad de ascensores que hay en el edificio
    def get_lista_ascensores(self):
        return ['x' for i in range(len(self.lista_ascensores))]

    # Devuelve el ascensor más cercano al piso que se le pasa por parámetro
    def get_ascensor_mas_cerca_con_espacio(self, piso_actual):
        if (self.todos_los_ascensores_estan_en_uso()):
            print(self.errores["ascensores_en_uso"])
            return None
        else:
            return min(self.lista_ascensores, key=lambda ascensor: abs(ascensor.get_piso() - piso_actual))

    # Verifica que el piso esté entre 1 y el número de pisos del edificio
    def verificar_piso(self, piso):
        return 1 <= piso <= self.pisos

    # Pinta el ascensor en la estructura del edificio
    def pintar_ascensor(self, piso, paso, columna):
        self.estructura[piso - paso][columna] = 'x'

    # Pide el piso actual y el piso destino al usuario, y llama a la función get_ascensor_mas_cerca_con_espacio
    def pedir_ascensor(self, piso_destino):
        # Pide el piso actual y el piso destino al usuario verificando que
        # sean números enteros y que existan en el edificio4
        usuario_actual = self.get_usuario_actual()
        if usuario_actual.get_piso() == piso_destino:
            print(f"El usuario {usuario_actual} ya se encuentra en el piso destino")
            return self.errores["usuario_en_destino"]

        if usuario_actual.get_estado():
            piso_actual = usuario_actual.get_piso()
            ascensor = self.get_ascensor_mas_cerca_con_espacio(piso_actual)
            ascensor.set_recorrido_restante_origen(piso_actual - ascensor.get_piso())
            ascensor.set_recorrido_restante_destino(piso_destino - piso_actual)
            usuario_actual.set_estado(False)
            usuario_actual.set_piso(piso_destino)
            # Llama a la función set_estado para establecer el estado del ascensor a False
            print(
                f'El ascensor {ascensor.get_columna()} ha sido llamado por: {self.get_usuario_actual().get_nombre()} hacia el piso: {piso_destino}!')
            usuario_actual.set_ascensor(ascensor)
            ascensor.set_estado(False)
            return "El ascensor más cercano es el número: " + str(ascensor.get_columna()) + "!"
        else:
            return self.errores["usuario_en_uso"]

    # Mueve el ascensor hacia arriba o hacia abajo según el recorrido restante
    def mover_ascensor(self, ascensor):
        columna = ascensor.get_columna() - 1
        piso = -ascensor.get_piso()
        paso = ascensor.get_paso()
        recorrido_restante = ascensor.get_recorrido_restante()
        self.estructura[piso][columna] = 0

        # Mover el ascensor hacia arriba
        if recorrido_restante > 0 and abs(paso) <= abs(recorrido_restante):
            self.pintar_ascensor(piso, paso, columna)
            ascensor.set_piso(-piso + paso)
            ascensor.set_recorrido_restante(recorrido_restante - paso)

        # Mover el ascensor hacia abajo
        elif recorrido_restante < 0 and abs(paso) <= abs(recorrido_restante):
            self.pintar_ascensor(piso, -paso, columna)
            ascensor.set_piso(-piso - paso)
            ascensor.set_recorrido_restante(recorrido_restante + paso)
        # Llegó al piso destino y se debe mover hacia el destino
        else:
            self.pintar_ascensor(piso, recorrido_restante, columna)
            ascensor.set_piso(-piso + recorrido_restante)
            ascensor.set_recorrido_restante(0)
        self.liberar_ascensor(ascensor) if ascensor.get_recorrido_restante_destino() == 0 else None

    # Libera el ascensor y al usuario
    def liberar_ascensor(self, ascensor):
        ascensor.set_estado(True)
        for usuario in self.lista_usuarios:
            if usuario.get_ascensor() == ascensor:
                usuario.set_estado(True)
                usuario.set_ascensor(None)
                print(
                    f'El usuario {usuario.get_nombre()} ha llegado a su destino en el piso {usuario.get_piso()} gracias al ascensor {ascensor.get_columna()}!')

    # Pide el piso actual y el piso destino al usuario, y llama a la función get_ascensor_mas_cerca_con_espacio
    # para obtener el ascensor más cercano con espacio

    # Actualiza los ascensores dentro del edificio
    def actualizar_ascensores(self):
        for ascensor in self.lista_ascensores:
            if ascensor.get_recorrido_restante_destino() != 0 and ascensor.get_encendido():
                self.mover_ascensor(ascensor)

    # Actualiza el usuario actual
    def actualizar_usuarios(self):
        self.usuario_actual = (self.usuario_actual + 1) % len(self.lista_usuarios)
        return "Bienvenido al sistema de control de ascensores " + self.get_usuario_actual().get_nombre()

    # hacer un toogle que cambie el estado de emergencia del edificio y apague los ascensores que no son de emergencia
    def toogle_estado_de_emergencia(self):
        self.estado_de_emergencia = not self.estado_de_emergencia
        for ascensor in self.lista_ascensores:
            if not ascensor.get_estado_emergency():
                ascensor.set_encendido(not self.estado_de_emergencia)

    # simular 400 peticiones de ascensor el registro de peticion debe ser desarrollado por consola
    def iniciar_simulacion(self):
        for i in range(200):
            piso_destino = self.fake.random_int(1, self.pisos)
            self.pedir_ascensor(piso_destino)
            self.actualizar_ascensores()
            self.actualizar_usuarios()
            sleep(0.5)

    # Devuelve la estructura del edificio en forma de string
    def get_estructura_str(self):
        return "\n".join(" ".join(str(piso) for piso in columna) for columna in self.estructura)

    # Devuelve la estructura del edificio en forma de string
    def __str__(self):
        return self.get_estructura_str()
