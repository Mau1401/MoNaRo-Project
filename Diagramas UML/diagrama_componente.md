# Diagrama de Componentes

Para representar la arquitectura del proyecto de forma básica, en este archivo se presenta el código fuente de del diagrama de componentes:
```plantuml
@startuml

'Se define el paquete que contiene todos los objetos
package "Herramienta para gestión de proyectos" {
  [Usuario] as user
  [Base de datos] as db
  [Gestión de Tareas \nen Tablero Kanban] as kanban
  [Canal de comunicación] as msj
  [Autentificación de usuario] as manager
  [Asignación y Seguimiento de Tareas] as tareas
  [Reportes de Progreso del Proyecto] as reportes
  [Sistema de Notificaciones] as notificaciones
}

'Enlaces del usuario
user --> kanban
user --> tareas
user --> manager
user --> msj

'Enlaces de objetos con la base de datos
kanban --> db
tareas --> db
reportes --> db
msj --> db

'Enlaces de objetos con sistema de notificaciones
tareas --> notificaciones
kanban --> notificaciones

@enduml
```
Dicho diagrama se visualiza a continuación:
<center><img src="diagrama_componentes.svg"></center>
