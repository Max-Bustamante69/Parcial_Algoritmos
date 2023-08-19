import tkinter as tk
from tkinter import messagebox
from Edificio import Edificio


# Clase GUI que contiene los elementos de la interfaz gráfica y sus métodos para controlarlos y simularlos
class GUI:
    def __init__(self, root):
        self.root = root
        self.edificio = Edificio()

        self.label = tk.Label(root, text="Control de Ascensores")
        self.label.pack()

        self.piso_actual_label = tk.Label(root,
                                          text="Bienvenido al sistema de control de ascensores " + self.edificio.get_usuario_actual().get_nombre() + "!")
        self.piso_actual_label.pack()

        self.piso_destino_label = tk.Label(root, text="Piso Destino:")
        self.piso_destino_label.pack()

        self.piso_destino_entry = tk.Entry(root)
        self.piso_destino_entry.pack()

        self.pedir_ascensor_button = tk.Button(root, text="Pedir Ascensor", command=self.pedir_ascensor)
        self.pedir_ascensor_button.pack()

        self.iniciar_simulacion_button = tk.Button(root, text="Iniciar Simulación", command=self.simulacion)
        self.iniciar_simulacion_button.pack()

        self.emergency_checkbox = tk.Checkbutton(root, text="Modo Emergencia", command=self.toggle_emergency)
        self.emergency_checkbox.pack()

        self.estructura_text = tk.Text(root, height=60, width=60)
        self.estructura_text.pack()

        self.errores_text = tk.Text(root, height=5, width=30)
        self.errores_text.pack()

        self.actualizar_ascensores()  # Iniciar la actualización automáticamente
        self.mostrar_estructura()  # Mostrar la estructura inicial

    # crear una simulación de la misma GUI, utilizando metodos propios de la clase
    def simulacion(self):
        self.edificio.iniciar_simulacion()

    # pedir un ascensor para el usuario actual y mostrarlo en la interfaz gráfica con sus respectivos cambios de estado
    def pedir_ascensor(self):

        try:
            piso_destino = int(self.piso_destino_entry.get())
            if not self.edificio.todos_los_ascensores_estan_en_uso():
                if self.edificio.verificar_piso(piso_destino):
                    messagebox.showinfo("Ascensor", self.edificio.pedir_ascensor(piso_destino))
                    self.piso_destino_entry.delete(0, tk.END)  # Limpiar la entrada de piso destino
                    self.piso_actual_label["text"] = self.edificio.actualizar_usuarios()
                    self.mostrar_estructura()
                else:
                    messagebox.showerror("Error", self.edificio.errores["select_piso"])
            else:
                messagebox.showerror("Error", self.edificio.errores["ascensores_en_uso"])
        except ValueError:
            messagebox.showerror("Error", self.edificio.errores["valor_numerico"])

    def actualizar_ascensores(self):
        ascensores_en_movimiento = self.edificio.hay_ascensores_en_movimiento()
        if ascensores_en_movimiento:
            self.edificio.actualizar_ascensores()
            self.mostrar_estructura()
        self.root.after(500, self.actualizar_ascensores)  # Actualizar cada 2 segundos

    def toggle_emergency(self):
        self.edificio.toogle_estado_de_emergencia()
        self.mostrar_estructura()

    def get_estructura_str(self):
        return "\n".join(" ".join(str(piso) for piso in columna) for columna in self.edificio.estructura)

    def mostrar_estructura(self):
        self.estructura_text.tag_configure("red", foreground="red")
        self.estructura_text.tag_configure("green", foreground="green")
        self.estructura_text.tag_configure("blue", foreground="blue")

        self.estructura_text.delete("1.0", tk.END)  # Limpiar el texto
        estructura_str = self.edificio.get_estructura_str()  # Obtener la estructura en forma de string
        self.estructura_text.insert(tk.END, estructura_str)

        for ascensor in self.edificio.lista_ascensores:
            if ascensor.get_encendido() and ascensor.get_estado():
                tag_name = "green"
            elif ascensor.get_encendido() and not ascensor.get_estado():
                tag_name = "blue"
            else:
                tag_name = "red"
            piso = (self.edificio.pisos - ascensor.get_piso()) + 1
            columna = (((ascensor.get_columna() - 1) * 2))  # Restamos 1 para que solo se coloree el número
            start_index = f"{piso}.{columna}"  # Calcula el índice de inicio
            self.estructura_text.tag_add(tag_name, start_index)  # Agrega el tag al texto
