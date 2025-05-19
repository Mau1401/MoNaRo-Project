# Se importan las librerías necesarias
import customtkinter as ctk

# Programas necesarios
from login import VentanaLogin

# Selección del tema de la GUI
ctk.set_appearance_mode("dark")

# Selección del color temático
ctk.set_default_color_theme("blue")

# Se corre la aplicación, iniciando con la ventana de Login
# Cada pantalla corresponde a un objeto
if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()