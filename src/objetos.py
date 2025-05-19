class Proyecto:
    def __init__(self, nombre):
        self.nombre = nombre
        self.miembros = []
        self.tareas = []

    def agregar_miembro(self, usuario):
        self.miembros.append(usuario)

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)


class Tarea:
    def __init__(self, proyecto):
        self.nombre = ""
        self.responsables = []
        self.proyecto = proyecto
        self.estado = "Por Hacer"
        self.fecha_limite = None
        self.comentarios = []

    def asignar_responsable(self, usuario):
        self.responsables.append(usuario)

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def agregar_comentario(self, comentario):
        self.comentarios.append(comentario)

    def agregar_nombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre


def verificar_permiso(usuario, permiso_requerido):
    roles_permisos = {
        'admin': ['crear_proyecto', 'editar_proyecto', 'asignar_tarea', 'crear_reporte', 'ver_proyecto'],
        'dev': ['ver_proyecto', 'comentar_tarea', 'ver_tareas']
    }
    return permiso_requerido in roles_permisos.get(usuario['clearance'], [])


def obtener_nombres_seleccionados(listbox):
    indices = listbox.curselection()
    nombres_seleccionados = [listbox.get(i) for i in indices]
    return nombres_seleccionados

