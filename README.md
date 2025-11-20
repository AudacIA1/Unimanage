# UniManage: Sistema de Gestión de Activos Universitarios

UniManage es una aplicación web diseñada para la gestión integral de activos dentro de un entorno universitario. Permite llevar un control detallado del inventario, gestionar préstamos de equipos a usuarios y programar mantenimientos, todo a través de una interfaz web intuitiva.

Además, cuenta con un **asistente virtual (chatbot)** que permite a los usuarios realizar consultas sobre el estado de los activos de forma conversacional y un **sistema de reportes** que permite a los administradores generar informes en formato PDF y Excel.

## Características Principales

-   **Gestión de Activos**: CRUD completo para activos, incluyendo información detallada, categoría y ubicación.
-   **Gestión de Préstamos**: Sistema para registrar y seguir los préstamos de activos a los usuarios del sistema.
-   **Gestión de Mantenimientos**: Permite registrar y dar seguimiento a las tareas de mantenimiento de los activos.
-   **Dashboard Interactivo**: Un panel de control (`Inicio`) que muestra estadísticas clave sobre el estado del inventario.
-   **Asistente Virtual (Chatbot)**: Un chatbot basado en `spaCy` para consultas rápidas sobre la disponibilidad y estado de los activos.
-   **Generación de Reportes**: Módulo para generar reportes en PDF y Excel sobre activos, préstamos, mantenimientos y eventos.
-   **Gestión de Usuarios y Roles**: Administración de usuarios y asignación de roles (Admin, Staff, etc.) a través de una interfaz gráfica.
-   **Gestión de Eventos**: Permite registrar y gestionar eventos en la universidad.
-   **Sistema de Solicitudes**: Módulo para que los usuarios puedan solicitar activos.
-   **API REST**: Endpoints de API para interactuar con los datos del sistema (e.g., para el chatbot).

## Tecnologías Utilizadas

-   **Backend**:
    -   Python 3
    -   Django 5.2
    -   Django REST Framework
    -   spaCy (para el chatbot)
    -   ReportLab (para reportes en PDF)
    -   Openpyxl (para reportes en Excel)
    -   Gunicorn & Whitenoise (para despliegue)
-   **Frontend**:
    -   HTML5
    -   Tailwind CSS
    -   JavaScript
    -   Chart.js
    -   Font Awesome
    -   jQuery & DataTables
-   **Base de Datos**:
    -   MySQL (para desarrollo)
    -   PostgreSQL (soportado, ver `requirements.txt`)
-   **Librerías Adicionales**:
    -   `django-mptt` (para estructuras de árbol, e.g., categorías de activos)
    -   `django-autocomplete-light` (para autocompletado en formularios)
    -   `django-widget-tweaks` (para renderizar campos de formulario)

## Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto en un entorno de desarrollo local.

### 1. Prerrequisitos

-   Python 3.10 o superior.
-   Git.
-   Un servidor de base de datos MySQL o PostgreSQL en funcionamiento.

### 2. Clonar el Repositorio

Clona este repositorio en tu máquina local y navega hasta el directorio del proyecto.

```bash
git clone <URL_DEL_REPOSITORIO_GIT>
cd UniManage
```

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

El proyecto se conecta a una base de datos (MySQL por defecto en desarrollo) a través de variables de entorno.

1.  **Crea una base de datos** en tu servidor MySQL.
    ```sql
    CREATE DATABASE unimanage_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```
2.  En la raíz del proyecto, crea un archivo llamado `.env`.
3.  Añade las credenciales de tu base de datos al archivo `.env`.

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

### 8. Cargar Datos de Prueba (Opcional)

El proyecto incluye un archivo de `fixtures` con datos de ejemplo para poblar la base de datos.

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
-   `apps/`: Contiene las diferentes aplicaciones que conforman el proyecto:
    -   `accounts`: Gestión de autenticación de usuarios.
    -   `assets`: Gestión de activos.
    -   `chatbot`: Asistente virtual.
    -   `dashboard`: Panel de control principal.
    -   `events`: Gestión de eventos.
    -   `loans`: Gestión de préstamos de activos.
    -   `maintenance`: Gestión de mantenimientos.
    -   `reports`: Generación de reportes.
    -   `request`: Sistema de solicitudes de activos.
    -   `usermanagement`: Gestión de usuarios y roles.
-   `static/`: Archivos estáticos globales (CSS, JS, imágenes).
-   `templates/`: Plantillas HTML globales.
