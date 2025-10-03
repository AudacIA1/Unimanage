# UniManage: Sistema de Gestión de Activos Universitarios

UniManage es una aplicación web diseñada para la gestión integral de activos dentro de un entorno universitario. Permite llevar un control detallado del inventario, gestionar préstamos de equipos a usuarios y programar mantenimientos, todo a través de una interfaz web intuitiva.

Además, cuenta con un **asistente virtual (chatbot)** que permite a los usuarios realizar consultas sobre el estado de los activos de forma conversacional.

## Características Principales

-   **Gestión de Activos**: CRUD completo para activos, incluyendo información detallada, categoría y ubicación.
-   **Gestión de Préstamos**: Sistema para registrar y seguir los préstamos de activos a los usuarios del sistema.
-   **Gestión de Mantenimientos**: Permite registrar y dar seguimiento a las tareas de mantenimiento de los activos.
-   **Dashboard Interactivo**: Un panel de control (`Inicio`) que muestra estadísticas clave sobre el estado del inventario.
-   **Asistente Virtual**: Un chatbot para consultas rápidas sobre la disponibilidad y estado de los activos.
-   **Gestión de Usuarios**: Administración de usuarios y roles (superusuario, staff).

## Tecnologías Utilizadas

-   **Backend**:
    -   Python 3
    -   Django 5.2
-   **Frontend**:
    -   HTML5
    -   Tailwind CSS
    -   JavaScript
    -   Chart.js
    -   Font Awesome 
    -   jQuery & DataTables 
-   **Base de Datos**:
    -   MySQL

## Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto en un entorno de desarrollo local.

### 1. Prerrequisitos

-   Python 3.10 o superior.
-   Git.
-   Un servidor de base de datos MySQL en funcionamiento.

### 2. Clonar el Repositorio

Clona este repositorio en tu máquina local y navega hasta el directorio del proyecto.

```bash
git clone <URL_DEL_REPOSITORIO_GIT>
cd UniManage

### 3. Configurar el Entorno Virtual


```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 4. Instalar Dependencias

Con el entorno virtual activado, instala todas las dependencias del proyecto listadas en `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5. Configurar la Base de Datos

El proyecto se conecta a una base de datos MySQL. La configuración se gestiona a través de variables de entorno para mantener la seguridad de las credenciales.

**Importante:** No modifiques directamente el archivo `core/settings.py` para la configuración de la base de datos.

1.  **Crea una base de datos** en tu servidor MySQL. Puedes hacerlo con el siguiente comando SQL:
    ```sql
    CREATE DATABASE unimanage_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;
    ```
2.  En la raíz del proyecto, crea un archivo llamado `.env`.
3.  Añade las credenciales de tu base de datos al archivo `.env`. Asegúrate de que coincidan con tu configuración de MySQL (puedes necesitar un usuario y contraseña específicos con permisos para la nueva base de datos):

```
DB_NAME=unimanage_db
DB_USER=tu_usuario_mysql
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
```

### 6. Preparar la Base de Datos de Django

Aplica las migraciones para crear la estructura de tablas del proyecto.

```bash
python manage.py migrate
```

### 7. Crear un Superusuario

Para acceder al panel de administración de Django y a las secciones de gestión, necesitas una cuenta de superusuario.

```bash
python manage.py createsuperuser
```
Sigue las instrucciones en la terminal para crear tu cuenta de administrador.

### 8. Cargar Datos de Prueba (Opcional)

El proyecto incluye un archivo de `fixtures` con datos de ejemplo para poblar la base de datos. Para cargarlos, ejecuta:

```bash
python manage.py loaddata core/fixtures/initial_data.json
```

### 9. Ejecutar el Proyecto

Finalmente, inicia el servidor de desarrollo de Django.

```bash
python manage.py runserver
```

## Estructura del Proyecto

El proyecto sigue una estructura organizada para separar la configuración principal de las aplicaciones:

-   `core/`: Contiene la configuración principal del proyecto Django (`settings.py`, `urls.py`, etc.).
-   `apps/`: Contiene las diferentes aplicaciones que conforman el proyecto (e.g., `dashboard`, `assets`, `loans`, etc.).
-   `static/`: Archivos estáticos globales (CSS, JS, imágenes).
-   `templates/`: Plantillas HTML globales.
