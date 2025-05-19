# Se importan las librerias necesarias
import customtkinter as ctk
import tkinter as tk
from tkinter.messagebox import showinfo

# Programas necesarios
from objetos import *
from task_management import *


class VentanaProjectManagement(ctk.CTkToplevel):
    """Clase con la ventana de gestión de proyectos para administradores y desarrolladores"""

    def __init__(self, master=None, usuario=None):
        super().__init__(master)  # Se parte del constructor de clase CTkToplevel
        self.lista_usuarios = None
        self.nombre_proyecto = None
        self.confirmar_proyecto = None
        self.ventana_crear_proyecto = None
        self.agregar_miembro_proyecto = None
        self.usuario_actual = usuario
        self.title("Monarro")
        self.geometry("800x500")
        self.protocol("WM_DELETE_WINDOW", self.salir_ventana)
        # Proyectos definidos
        proyecto_1 = Proyecto("Base de datos")
        proyecto_1.agregar_miembro("Carlos")
        tarea_1 = Tarea(proyecto_1)
        tarea_1_2 = Tarea(proyecto_1)
        tarea_1.agregar_nombre("Diseñar esquema")
        tarea_1_2.agregar_nombre("Enlazar base de datos")
        tarea_1.asignar_responsable("Luis")
        tarea_1_2.asignar_responsable("Ana")
        tarea_1_2.cambiar_estado("En Progreso")
        proyecto_1.agregar_tarea(tarea_1)
        proyecto_1.agregar_tarea(tarea_1_2)
        proyecto_2 = Proyecto("Interfaz gráfica")
        proyecto_2.agregar_miembro("Ana")
        proyecto_2.agregar_miembro("Luis")
        tarea_2 = Tarea(proyecto_2)
        tarea_2.agregar_nombre("Diseñar")
        tarea_2.asignar_responsable("Carlos")
        tarea_2.cambiar_estado("Completado")
        proyecto_2.agregar_tarea(tarea_2)
        proyecto_3 = Proyecto("Administrador de Usuarios")
        proyecto_3.agregar_miembro("Carlos")
        proyecto_3.agregar_miembro("Ana")
        proyecto_3.agregar_miembro("Luis")
        tarea_3 = Tarea(proyecto_3)
        tarea_3.agregar_nombre('Planear')
        tarea_3.asignar_responsable("Luis")
        proyecto_3.agregar_tarea(tarea_3)
        self.proyectos = [proyecto_1, proyecto_2, proyecto_3]  # Arreglo con los proyectos
        # Marcos para agrupar objetos en la pantalla
        self.marco_izquierdo = ctk.CTkFrame(self, width=200)
        self.marco_izquierdo.pack(side="left", fill="y")
        self.marco_derecho = ctk.CTkFrame(self)
        self.marco_derecho.pack(side="right", fill="both", expand=True)

        if verificar_permiso(self.usuario_actual, 'crear_proyecto'):
            self.boton_crear_proyecto = ctk.CTkButton(self.marco_izquierdo, text="Crear nuevo proyecto",
                                                      command=self.crear_proyecto)
            self.boton_crear_proyecto.pack(pady=10, padx=10)

        if verificar_permiso(self.usuario_actual, 'crear_reporte'):
            self.boton_crear_reporte = ctk.CTkButton(self.marco_izquierdo, text="Generar reporte",
                                                     command=self.crear_reporte_general)
            self.boton_crear_reporte.pack(pady=10, padx=10)

        self.detalles_label = ctk.CTkLabel(self.marco_derecho,
                                           text="Seleccione un proyecto para ver más información",
                                           font=("Arial", 16))
        self.detalles_label.pack(pady=20)

        self.lista_proyectos = tk.Listbox(self.marco_derecho, width=50, height=10, font=("Arial", 16))
        self.lista_proyectos.pack(pady=20)
        for proyect in self.proyectos:
            self.lista_proyectos.insert("end", proyect.nombre)

        if verificar_permiso(self.usuario_actual, 'ver_proyecto'):
            self.boton_tareas_proyecto = ctk.CTkButton(self.marco_derecho,
                                                         text="Ventana de tareas del proyecto",
                                                         command=self.tareas_proyecto)
            self.boton_tareas_proyecto.pack(pady=10, padx=10)
        self.boton_detalles_proyecto = ctk.CTkButton(self.marco_derecho,
                                                     text="Detalles del proyecto",
                                                     command=self.detalles_proyecto)
        self.boton_detalles_proyecto.pack(pady=10, padx=10)

    def salir_ventana(self):
        self.quit()
        self.destroy()

    def crear_proyecto(self):
        if not verificar_permiso(self.usuario_actual, 'crear_proyecto'):
            showinfo("Permiso denegado", "No tiene permiso para realizar esta acción.")
            return

        self.ventana_crear_proyecto = ctk.CTkToplevel(self)
        self.ventana_crear_proyecto.title("Nuevo Proyecto")
        self.ventana_crear_proyecto.geometry("300x300")
        self.ventana_crear_proyecto.attributes('-topmost', True)
        ctk.CTkLabel(self.ventana_crear_proyecto, text="Nuevo Proyecto").pack()
        self.nombre_proyecto = ctk.CTkEntry(master=self.ventana_crear_proyecto, placeholder_text="Nombre: ")
        self.nombre_proyecto.pack(pady=12, padx=10)
        self.lista_usuarios = tk.Listbox(self.ventana_crear_proyecto, width=50, height=3, font=("Arial", 16),
                                         selectmode=tk.MULTIPLE)
        self.lista_usuarios.insert("end", "Carlos")
        self.lista_usuarios.insert("end", "Ana")
        self.lista_usuarios.insert("end", "Luis")
        self.lista_usuarios.pack()
        self.confirmar_proyecto = ctk.CTkButton(self.ventana_crear_proyecto,
                                                text="Crear proyecto", command=self.crear_proyecto_confirmado)
        self.confirmar_proyecto.pack(pady=10, padx=10)

    def crear_proyecto_confirmado(self):
        nombre_proyecto = self.nombre_proyecto.get()
        proyecto = Proyecto(nombre_proyecto)
        agregar_usuarios_proyecto(self.lista_usuarios, proyecto)
        self.proyectos.append(proyecto)
        self.lista_proyectos.insert("end", proyecto.nombre)
        self.ventana_crear_proyecto.destroy()

    def tareas_proyecto(self):
        if not verificar_permiso(self.usuario_actual, 'ver_proyecto'):
            showinfo("Permiso denegado", "No tiene permiso para realizar esta acción.")
            return
        proyecto_seleccionado = self.lista_proyectos.get("active")
        proyecto_seleccionado = obtener_nombre_proyecto(self.proyectos, proyecto_seleccionado)
        VentanaTaskManagement(proyecto=proyecto_seleccionado, usuario=self.usuario_actual)

    def crear_reporte_general(self):
        if not verificar_permiso(self.usuario_actual, 'crear_reporte'):
            showinfo("Permiso denegado", "No tiene permiso para realizar esta acción.")
            return

        reporte = "Reporte General:\n"
        for proyecto in self.proyectos:
            reporte += f"\nProyecto: {proyecto.nombre}\n"
            for tarea in proyecto.tareas:
                reporte += f"- {tarea.nombre} ({tarea.estado})\n"
        showinfo("Reporte General", reporte)

    def detalles_proyecto(self):
        if not verificar_permiso(self.usuario_actual, 'ver_proyecto'):
            showinfo("Permiso denegado", "No tiene permiso para realizar esta acción.")
            return

        proyecto_seleccionado = self.lista_proyectos.get("active")
        for proyecto in self.proyectos:
            if proyecto.nombre == proyecto_seleccionado:
                detalles = f"Nombre: {proyecto.nombre}\nMiembros: {', '.join(proyecto.miembros)}\nTareas:"
                for tarea in proyecto.tareas:
                    detalles += f"\n- {tarea.nombre} ({tarea.estado})"
                showinfo("Detalles del Proyecto", detalles)
                break


def obtener_nombre_proyecto(proyectos, nombre):
    for i in proyectos:
        if i.nombre == nombre:
            return i


def agregar_usuarios_proyecto(listbox, proyecto):
    usuarios_seleccionados = obtener_nombres_seleccionados(listbox)
    for usuario in usuarios_seleccionados:
        proyecto.agregar_miembro(usuario)
