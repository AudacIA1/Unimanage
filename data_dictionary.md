
# Diccionario de Datos

Este documento describe las entidades y sus atributos en el sistema UniManage.

## Entidad: UserProfile

**Descripción:** Extiende el modelo de usuario de Django para incluir información adicional.

| Campo | Tipo de Dato | Longitud | Obligatorio | Valores Específicos | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **user** | OneToOneField | - | Sí | - | Llave foránea al modelo User de Django. |
| role | CharField | 20 | Sí | 'admin', 'tech', 'staff', 'user' | Rol del usuario en el sistema. |
| phone | CharField | 30 | No | - | Número de teléfono del usuario. |
| department | CharField | 100 | No | - | Departamento al que pertenece el usuario. |

**Llave Primaria:** `user` (implícita a través de OneToOneField)

## Entidad: AssetCategory

**Descripción:** Organiza los activos en una jerarquía de categorías.

| Campo | Tipo de Dato | Longitud | Obligatorio | Valores Específicos | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | AutoField | - | Sí | - | Identificador único de la categoría. |
| name | CharField | 100 | Sí | - | Nombre de la categoría. |
| description | TextField | - | No | - | Descripción de la categoría. |
| icon | CharField | 50 | No | - | Ícono para la categoría. |
| **parent** | TreeForeignKey | - | No | - | Llave foránea a `self` para crear la jerarquía. |

**Llave Primaria:** `id`
**Llave Foránea:** `parent` -> `AssetCategory(id)`

## Entidad: Asset

**Descripción:** Representa un activo físico o digital que puede ser gestionado.

| Campo | Tipo de Dato | Longitud | Obligatorio | Valores Específicos | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | AutoField | - | Sí | - | Identificador único del activo. |
| name | CharField | 100 | Sí | - | Nombre del activo. |
| code | CharField | 50 | No | - | Código único del activo (generado automáticamente). |
| **category** | ForeignKey | - | Sí | - | Llave foránea a `AssetCategory`. |
| location | CharField | 100 | Sí | - | Ubicación del activo. |
| status | CharField | 20 | Sí | 'disponible', 'en_uso', 'mantenimiento' | Estado actual del activo. |
| created_at | DateTimeField | - | Sí | - | Fecha y hora de creación del activo. |
| updated_at | DateTimeField | - | Sí | - | Fecha y hora de la última actualización del activo. |

**Llave Primaria:** `id`
**Llave Foránea:** `category` -> `AssetCategory(id)`

## Entidad: Evento

**Descripción:** Almacena información sobre eventos y visitas.

| Campo | Tipo de Dato | Longitud | Obligatorio | Valores Específicos | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | AutoField | - | Sí | - | Identificador único del evento. |
| titulo | CharField | 150 | Sí | - | Título del evento. |
| descripcion | TextField | - | No | - | Descripción del evento. |
| tipo | CharField | 10 | Sí | 'evento', 'visita' | Tipo de evento. |
| fecha_inicio | DateTimeField | - | Sí | - | Fecha y hora de inicio del evento. |
| fecha_fin | DateTimeField | - | No | - | Fecha y hora de finalización del evento. |
| lugar | CharField | 200 | No | - | Lugar del evento. |
| **responsable** | ForeignKey | - | No | - | Llave foránea al modelo User de Django. |
| visitante | CharField | 200 | No | - | Nombre del visitante (si aplica). |
| creado_en | DateTimeField | - | Sí | - | Fecha y hora de creación del evento. |

**Llave Primaria:** `id`
**Llave Foránea:** `responsable` -> `User(id)`

## Entidad: Loan

**Descripción:** Registra el préstamo de un activo a un usuario.

| Campo | Tipo de Dato | Longitud | Obligatorio | Valores Específicos | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | AutoField | - | Sí | - | Identificador único del préstamo. |
| **asset** | ForeignKey | - | Sí | - | Llave foránea a `Asset`. |
| **user** | ForeignKey | - | Sí | - | Llave foránea al modelo User de Django. |
| loan_date | DateTimeField | - | Sí | - | Fecha y hora del préstamo. |
| return_date | DateTimeField | - | No | - | Fecha y hora de devolución del activo. |
| status | CharField | 20 | Sí | 'Activo', 'Devuelto' | Estado del préstamo. |

**Llave Primaria:** `id`
**Llaves Foráneas:**
* `asset` -> `Asset(id)`
* `user` -> `User(id)`

## Entidad: Maintenance

**Descripción:** Almacena información sobre las tareas de mantenimiento de los activos.

| Campo | Tipo de Dato | Longitud | Obligatorio | Valores Específicos | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | AutoField | - | Sí | - | Identificador único del mantenimiento. |
| **asset** | ForeignKey | - | Sí | - | Llave foránea a `Asset`. |
| description | TextField | - | Sí | - | Descripción del trabajo de mantenimiento. |
| performed_by | CharField | 100 | Sí | - | Persona o empresa que realiza el mantenimiento. |
| status | CharField | 20 | Sí | 'Pendiente', 'En proceso', 'Finalizado' | Estado de la tarea de mantenimiento. |
| created_at | DateTimeField | - | Sí | - | Fecha y hora de creación de la tarea. |

**Llave Primaria:** `id`
**Llave Foránea:** `asset` -> `Asset(id)`

## Entidad: LoanRequest

**Descripción:** Gestiona las solicitudes de préstamo de activos por parte de los usuarios.

| Campo | Tipo de Dato | Longitud | Obligatorio | Valores Específicos | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **id** | AutoField | - | Sí | - | Identificador único de la solicitud. |
| **user** | ForeignKey | - | Sí | - | Llave foránea al modelo User de Django. |
| **asset** | ForeignKey | - | Sí | - | Llave foránea a `Asset`. |
| reason | TextField | - | No | - | Motivo de la solicitud. |
| request_date | DateTimeField | - | Sí | - | Fecha y hora de la solicitud. |
| status | CharField | 20 | Sí | 'pending', 'approved', 'rejected' | Estado de la solicitud. |
| admin_comment | TextField | - | No | - | Comentario del administrador sobre la solicitud. |
| response_date | DateTimeField | - | No | - | Fecha y hora de la respuesta a la solicitud. |

**Llave Primaria:** `id`
**Llaves Foráneas:**
* `user` -> `User(id)`
* `asset` -> `Asset(id)`
