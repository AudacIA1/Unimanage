# Diagrama de Despliegue de UniManage

Este documento modela la configuración de hardware y software en tiempo de ejecución para el sistema UniManage.

## Descripción de Nodos

El sistema se despliega en una arquitectura cliente-servidor de tres niveles:

1.  **Nodo Cliente:**
    *   **Hardware:** Computadora de escritorio, portátil o dispositivo móvil del usuario.
    *   **Software:** Un navegador web moderno (ej. Chrome, Firefox, Safari) que interpreta HTML, CSS y ejecuta JavaScript.

2.  **Nodo Servidor Web:**
    *   **Hardware:** Un servidor físico o virtual (ej. en un proveedor de la nube como AWS, Azure o un servidor local).
    *   **Software:**
        *   **Servidor HTTP:** Un servidor web como Nginx o Apache que gestiona las solicitudes HTTP y sirve los archivos estáticos (CSS, JS, imágenes).
        *   **Servidor de Aplicaciones WSGI:** Un servidor como Gunicorn o uWSGI que actúa como interfaz entre el servidor HTTP y la aplicación Django.
        *   **Aplicación Django:** El backend de UniManage, que contiene toda la lógica de negocio.

3.  **Nodo Servidor de Base de Datos:**
    *   **Hardware:** Un servidor físico o virtual, que puede estar en la misma máquina que el servidor web (para entornos de desarrollo o pequeños) o en una máquina separada (para producción y escalabilidad).
    *   **Software:** Un sistema de gestión de bases de datos relacional como PostgreSQL, MySQL o MariaDB.

## Diagrama

A continuación se presenta un diagrama que visualiza la disposición de estos nodos y la comunicación entre ellos.

```
+---------------------------+         +--------------------------------+         +-----------------------------+
|       NODO CLIENTE        |         |       NODO SERVIDOR WEB        |         |  NODO SERVIDOR BASE DE DATOS  |
|---------------------------|         |--------------------------------|         |-----------------------------|
|                           |         |                                |         |                             |
|   +-------------------+   |  HTTP/S |   +--------------------------+ |         |   +-----------------------+   |
|   |  Navegador Web    |   |-------->|   | Servidor HTTP (Nginx)    | |         |   |                       |   |
|   | (HTML, CSS, JS)   |   |         |   +--------------------------+ |         |   |      Sistema de       |   |
|   +-------------------+   |         |                |               |         |   |   Gestión de Base de    |   |
|                           |         |              WSGI              |   SQL   |   |      Datos (SGBD)     |   |
|                           |         |                |               |-------->|   |     (PostgreSQL)      |   |
|                           |         |   +--------------------------+ |         |   |                       |   |
|                           |         |   | Aplicación Django (Python) | |         |   +-----------------------+   |
|                           |         |   +--------------------------+ |         |                             |
|                           |         |                                |         |                             |
+---------------------------+         +--------------------------------+         +-----------------------------+

```

## Flujo de Comunicación

1.  El **Navegador Web** del cliente envía una solicitud **HTTP/S** al **Servidor Web**.
2.  El **Servidor HTTP (Nginx)** recibe la solicitud. Si es para un archivo estático, lo sirve directamente. Si es para una ruta de la aplicación, la reenvía al servidor de aplicaciones a través de la interfaz **WSGI**.
3.  La **Aplicación Django** procesa la solicitud. Si necesita datos, se comunica con el **Servidor de Base de Datos** a través de una conexión **SQL** (manejada por el ORM).
4.  La **Base de Datos** devuelve los datos solicitados a la aplicación Django.
5.  La aplicación Django renderiza una respuesta (generalmente una página HTML o una respuesta JSON) y la devuelve al Servidor HTTP.
6.  El Servidor HTTP envía la respuesta final al Navegador Web del cliente.
