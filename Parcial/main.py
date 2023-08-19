from Edificio import *
from GUI import *

#crear una simulación de la misma GUI, utilizando metodos propios de la clase GUI y Edificio
if __name__ == '__main__':
    print("Bienvenido al sistema de control de ascensores")
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()



