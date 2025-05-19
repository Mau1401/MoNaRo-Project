# Se importan las librerias necesarias
import customtkinter as ctk
import tkinter as tk
from tkinter.messagebox import showinfo

# Programas necesarios
from objetos import *


class VentanaTaskManagement(ctk.CTkToplevel):
    """Clase con la ventana de gestión de proyectos para administradores y desarrolladores"""

    def __init__(self, master=None, usuario=None, proyecto=None):
        super().__init__(master)  # Se parte del constructor de clase CTkToplevel
        self.confirmar_tarea = None
        self.nombre_tarea = None
        self.ventana_crear_tarea = None
        self.lista_usuarios = None
        self.attributes("-topmost", True)
        self.agregar_miembro_proyecto = None
        self.usuario_actual = usuario
        self.proyecto_seleccionado = proyecto
        self.title("Administrador de tareas")
        self.geometry("800x500")
        self.tareas = []  # Arreglo con las tareas
        for tareas in self.proyecto_seleccionado.tareas:
            self.tareas.append(tareas)
        # Marcos para agrupar objetos en la pantalla
        self.marco_izquierdo = ctk.CTkFrame(self, width=200)
        self.marco_izquierdo.pack(side="left", fill="y")
        self.marco_derecho = ctk.CTkFrame(self)
        self.marco_derecho.pack(side="right", fill="both", expand=True)

        self.boton_crear_proyecto = ctk.CTkButton(self.marco_izquierdo, text="Crear nueva tarea",
                                                  command=self.crear_tarea)
        self.boton_crear_proyecto.pack(pady=10, padx=10)

        self.boton_crear_reporte = ctk.CTkButton(self.marco_izquierdo, text="Editar estado\nde tarea seleccionada",
                                                 command=self.editar_estado)
        self.boton_crear_reporte.pack(pady=10, padx=10)

        self.detalles_label = ctk.CTkLabel(self.marco_derecho,
                                           text=self.proyecto_seleccionado.nombre,
                                           font=("Arial", 16))
        self.detalles_label.pack(pady=20)

        self.lista_tareas = tk.Listbox(self.marco_derecho, width=50, height=10, font=("Arial", 16))
        self.lista_tareas.pack(pady=20)
        for tarea in self.proyecto_seleccionado.tareas:
            self.lista_tareas.insert("end", tarea.nombre)

        if verificar_permiso(self.usuario_actual, 'ver_proyecto'):
            self.boton_detalles_proyecto = ctk.CTkButton(self.marco_derecho,
                                                         text="Detalles sobre tarea seleccionada",
                                                         command=self.detalles_tarea)
            self.boton_detalles_proyecto.pack(pady=10, padx=10)

    def editar_estado(self):
        tarea_seleccionada = self.lista_tareas.get("active")
        for tarea in self.tareas:
            if tarea.nombre == tarea_seleccionada:
                nombre_viejo = tarea.estado
                if tarea.estado == "Por Hacer":
                    tarea.cambiar_estado("En Progreso")
                elif tarea.estado == "En Progreso":
                    tarea.cambiar_estado("Completado")
                elif tarea.estado == "Completado":
                    tarea.cambiar_estado("Por Hacer")
                showinfo("Cambio de estado","Se ha cambiado el estado de " +nombre_viejo +" a " + tarea.estado)

    def crear_tarea(self):
        if not verificar_permiso(self.usuario_actual, 'crear_proyecto'):
            showinfo("Permiso denegado", "No tiene permiso para realizar esta acción.")
            return

        self.ventana_crear_tarea = ctk.CTkToplevel(self)
        self.ventana_crear_tarea.title("Nueva Tarea")
        self.ventana_crear_tarea.geometry("300x200")
        self.ventana_crear_tarea.attributes('-topmost', True)
        ctk.CTkLabel(self.ventana_crear_tarea, text="Nueva Tarea").pack()
        self.nombre_tarea = ctk.CTkEntry(master=self.ventana_crear_tarea, placeholder_text="Nombre: ")
        self.nombre_tarea.pack(pady=12, padx=10)
        self.lista_usuarios = tk.Listbox(self.ventana_crear_tarea, width=50, height=3, font=("Arial", 16),
                                         selectmode=tk.MULTIPLE)
        self.lista_usuarios.insert("end", "Carlos")
        self.lista_usuarios.insert("end", "Ana")
        self.lista_usuarios.insert("end", "Luis")
        self.lista_usuarios.pack()
        self.confirmar_tarea = ctk.CTkButton(self.ventana_crear_tarea,
                                             text="Crear Tarea", command=self.crear_tarea_confirmada)
        self.confirmar_tarea.pack(pady=10, padx=10)

    def crear_tarea_confirmada(self):
        nombre_tarea = self.nombre_tarea.get()
        tarea = Tarea(self.proyecto_seleccionado)
        tarea.nombre = nombre_tarea
        agregar_usuarios_tarea(self.lista_usuarios, tarea)
        self.tareas.append(tarea)
        self.lista_tareas.insert("end", tarea.nombre)
        self.ventana_crear_tarea.destroy()

    def detalles_tarea(self):
        if not verificar_permiso(self.usuario_actual, 'ver_proyecto'):
            showinfo("Permiso denegado", "No tiene permiso para realizar esta acción.")
            return
        tarea_seleccionada = self.lista_tareas.get("active")
        for tarea in self.tareas:
            if tarea.nombre == tarea_seleccionada:
                detalles = (f"Nombre: {tarea.nombre}\nResponsables: {', '.join(tarea.responsables)}\nProyecto: "
                            f"{''.join(tarea.proyecto.nombre)}\nEstado: {''.join(tarea.estado)}\n")
                showinfo("Detalles de la Tarea", detalles)
                break


def obtener_nombre_tarea(tareas, nombre):
    for i in tareas:
        if i.nombre == nombre:
            return i


def agregar_usuarios_tarea(listbox, tarea):
    usuarios_seleccionados = obtener_nombres_seleccionados(listbox)
    for usuario in usuarios_seleccionados:
        tarea.asignar_responsable(usuario)
