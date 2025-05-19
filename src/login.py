# Primero se importan las librerias necesarias
import customtkinter as ctk
import tkinter.messagebox as tkmb

# Programas necesarios
from project_management import VentanaProjectManagement
from database import query


class VentanaLogin(ctk.CTk):
    """Clase con la ventana inicial de Login"""

    def __init__(self):
        super().__init__()  # Se parte del constructor de clase CTk
        self.title("Monarro")  # Título de la aplicación
        self.geometry("800x500")  # Tamaño de las pantallas
        # Se definen previamente los usuarios dentro de un diccionario
        self.usuarios = {usuario['name']:usuario for usuario in query("select * from users")}
        # Se crean objetos para la pantalla
        self.label = ctk.CTkLabel(self, text="Monarro Soluciones")
        self.label.pack(pady=20)

        # Se crea un marco, que es una formar de agrupar los objetos
        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label = ctk.CTkLabel(master=self.frame, text='Ingrese con su usuario y contraseña')
        self.label.pack(pady=12, padx=10)
        self.user_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Usuario")
        self.user_entry.pack(pady=12, padx=10)

        self.user_pass = ctk.CTkEntry(master=self.frame, placeholder_text="Contraseña", show="*")
        self.user_pass.pack(pady=12, padx=10)

        self.boton_login = ctk.CTkButton(master=self.frame, text='Login', command=self.check_login)
        self.boton_login.pack(pady=12, padx=10)

        self.checkbox = ctk.CTkCheckBox(master=self.frame, text='Recordarme')  # BOTÓN NO FUNCIONAL
        self.checkbox.pack(pady=12, padx=10)

    def check_login(self):
        """Función para revisar si datos de ingreso son correctos"""
        try:
            if self.usuarios[self.user_entry.get()]['password'] == self.user_pass.get():
                tkmb.showinfo(title="¡Ingreso Exitoso!",
                              message="Usted ha ingresado como {}".format(self.user_entry.get()))
                usuario = self.usuarios[self.user_entry.get()]
                self.abrir_ventana_proyectos_admin(usuario=usuario)

        except KeyError:
            tkmb.showerror(title="Error", message="Usuario o contraseña incorrecta")

    def abrir_ventana_proyectos_admin(self, usuario):
        """Función para abrir pantalla de proyectos para persona con permisos de Administrador"""
        self.withdraw()  # Se oculta la pantalla actual
        VentanaProjectManagement(self, usuario=usuario)


if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()